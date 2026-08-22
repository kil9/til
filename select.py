#!/usr/bin/env python3
"""1차 선별 — 수집분에서 오늘 실을 7-10건을 고른다 (task-80).

선별은 두 축이다.
  인기 축  최근 30일 롤링 분포의 백분위 상위 10%(p90) 를 통과한 것. 관심사와
           무관해도 무조건 싣되 2-5건으로 clamp 한다.
  관심사 축 til 분포에서 뽑은 관심사 프로필(interest-profile.py)과의 매칭.
           모델이 나머지 자리를 채운다.

정렬은 출처가 1순위다. 관리자의 2026-08-22 결정으로 GeekNews 를 HN 보다 먼저 두고,
같은 출처 안에서 추천 백분위와 관심사 보정을 쓴다. 품질보다 출처를 우선하는 의도적 편향이다.

입력: state/collected-<날짜>.json    출력: state/selected-<날짜>.json
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import collect
import feedback
import llm

BASE = Path(__file__).resolve().parent
STATE = BASE / "state"
KST = timezone(timedelta(hours=9))

POPULAR_CUT = 10.0        # 백분위 상위 N% = p90
POPULAR_MIN, POPULAR_MAX = 2, 5
# 인기 축의 소스별 상한(task-106). HN 백분위는 프런트페이지 30건 안의 순위라 매일 반드시
# 3건이 p90 컷 안에 들어오는 반면, GeekNews 는 조용한 날 0건이다. 합산 정렬로 뽑으면
# 확정 슬롯이 만성적으로 HN 차지가 된다. 소스 균형을 강제하지 않기로 한 것은 선별 전체
# 얘기였지 확정 슬롯까지 한쪽에 넘기자는 뜻이 아니었다.
POPULAR_MAX_BY_SOURCE = {"gn": 3, "hn": 2}
TOTAL_MIN, TOTAL_MAX = 7, 10
CANDIDATE_LIMIT = 55      # 프롬프트에 싣는 후보 수 상한. 소스가 둘이 되며 40 에서 올렸다

# 관심사 등급이 순위에 끼치는 보정폭(백분위 포인트). 인접한 항목끼리만 뒤집히도록 작게 둔다.
INTEREST_BONUS = {"최상": 2.0, "상": 1.2, "중": 0.4, "밖": 0.0}
GN_PRIORITY_MIN = 3       # 새 GN 후보가 있으면 품질과 무관하게 상위 3건을 본문에 확정한다

AIRED_LOOKBACK = 30       # 재등장 판정에 볼 지난 회차 범위(일)
REAIR_PENALTY = 40.0      # 이전 회차에 실린 항목의 백분위 패널티. 관심사 보정(최대 2.0)과
                          # 자릿수가 달라 사실상 새 항목 뒤로 밀린다.


def aired_before(today):
    """지난 회차에 실제로 실린 항목 → 그 회차 날짜. 키는 항목 id 와 정규화된 원문 URL 둘 다다.

    collect.py 는 신규가 얇은 날 목록 전체로 backfill 한다(매일 발행이 중복 회피보다
    우선이라는 결정). 그 대가로 어제 실은 글이 오늘 후보에 다시 올라오고, 추천수가
    높으면 인기 축으로 또 실린다 — 2026-07-30/31 에 2건이 그렇게 연달아 나갔다.
    수집을 조이는 대신 여기서 순위를 크게 눌러 새 항목에 자리를 내준다.

    소스가 둘이 되면서 id 만으로는 못 잡는 경로가 생겼다(task-106). 같은 글이 오늘 HN 에,
    내일 GeekNews 에 오르면 id 가 달라 재등장 판정을 통과해 이틀 연속 나간다. 회차 안의
    중복은 collect 의 URL 병합이 잡지만 날짜를 건너뛴 것은 여기서만 잡을 수 있다.
    """
    cutoff = (datetime.fromisoformat(today) - timedelta(days=AIRED_LOOKBACK)).date().isoformat()
    out = {}
    for path in sorted(STATE.glob("selected-*.json")):     # 오름차순 — 가장 최근 회차가 남는다
        day = path.stem[len("selected-"):]
        if not cutoff <= day < today:
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print(f"  {path.name} 파손 — 재등장 판정에서 제외", file=sys.stderr)
            continue
        for it in data.get("selected", []):
            out[it["id"]] = day
            # url_key 는 task-106 이후 회차에만 있다. 없으면 원문 URL 에서 그때 만든다.
            key = it.get("url_key") or collect.url_key(it.get("source_url"))
            if key:
                out[key] = day
    return out


def aired_on(item, aired):
    """이 항목이 지난 회차에 실렸는가 — id 로도 원문 URL 로도 본다."""
    return aired.get(item["id"]) or (aired.get(item["url_key"]) if item.get("url_key") else None)


def interest_profile():
    """til 저장소에서 관심사 프로필을 뽑는다. 실패하면 빈 문자열로 진행한다."""
    repo = Path(os.environ.get("TIL_REPO", Path.home() / "work/kil9/til"))
    script = repo / "backlog/assets/interest-profile.py"
    if not script.exists():
        print(f"  관심사 프로필 스크립트 없음({script}) — 관심사 축 없이 진행", file=sys.stderr)
        return ""
    p = subprocess.run([sys.executable, str(script), "--index", str(repo / "index.html")],
                       capture_output=True, text=True, timeout=120)
    if p.returncode != 0:
        print(f"  관심사 프로필 추출 실패 — 관심사 축 없이 진행: {p.stderr.strip()[:200]}", file=sys.stderr)
        return ""
    return p.stdout.strip()


def source_order(it):
    """작을수록 먼저다. 2026-08-22 부터 출처가 품질보다 앞선다."""
    return 0 if it.get("source", "gn") == "gn" else 1


def ask_complete_verdict(prompt, candidate_ids):
    """모델 판정이 후보 전체를 정확히 한 번씩 다룰 때까지 한 번 재시도한다.

    두 번째도 불완전하면 발행을 버리지 않고 selected 를 우선해 중복·미지 id 를 걷고,
    누락 후보는 rest 로 정규화한다. 이전에는 작은 GN 묶음이 통째로 빠져도 조용히 `중`으로
    떨어져 출처 쏠림을 키웠다.
    """
    expected = set(candidate_ids)
    verdict = {}
    for attempt in range(2):
        suffix = ""
        if attempt:
            suffix = ("\n\n직전 응답은 후보 일부를 누락하거나 중복했다. 이번에는 위 후보 id를 "
                      "selected와 rest에 정확히 한 번씩 전부 넣어라.")
        raw = llm.ask_json(prompt + suffix)
        verdict = {"selected": [], "rest": []}
        for name in verdict:
            rows = raw.get(name, []) if isinstance(raw, dict) else []
            if not isinstance(rows, list):
                continue
            for row in rows:
                if not isinstance(row, dict):
                    continue
                clean = dict(row)
                clean["id"] = str(row.get("id", ""))
                verdict[name].append(clean)
        rows = verdict.get("selected", []) + verdict.get("rest", [])
        ids = [r["id"] for r in rows]
        got = set(ids)
        missing = expected - got
        unknown = got - expected
        duplicate = len(ids) != len(set(ids))
        if not missing and not unknown and not duplicate:
            return verdict
        print(f"  모델 판정 불완전 (시도 {attempt + 1}/2): "
              f"누락 {len(missing)} · 미지 {len(unknown)} · 중복 {int(duplicate)}", file=sys.stderr)

    selected, rest, seen = [], [], set()
    for bucket, target in ((verdict.get("selected", []), selected),
                           (verdict.get("rest", []), rest)):
        for row in bucket:
            item_id = str(row.get("id", ""))
            if item_id not in expected or item_id in seen:
                continue
            clean = dict(row)
            clean["id"] = item_id
            target.append(clean)
            seen.add(item_id)
    for item_id in candidate_ids:
        if item_id not in seen:
            rest.append({"id": item_id, "interest": "중", "why": ""})
    print(f"  모델 판정 정규화 — 누락 {len(expected - seen)}건을 rest 로 보냄", file=sys.stderr)
    return {"selected": selected, "rest": rest}


def build_prompt(profile, candidates, popular_ids, gn_priority_ids, aired, want, rules):
    lines = []
    for it in candidates:
        mark = " [인기축 확정]" if it["id"] in popular_ids else ""
        if it["id"] in gn_priority_ids:
            mark += " [GN 출처 우선 확정]"
        if aired.get(it["id"]):
            mark += f" [{aired[it['id']]} 브리핑에 이미 실림]"
        if it.get("also"):
            mark += f" [양쪽에 올랐다: HN {it['also']['points']}표]"
        src = "GN" if it.get("source", "gn") == "gn" else "HN"
        body = (it.get("summary") or it.get("desc") or "")[:400]
        lines.append(
            f"- id={it['id']}{mark} | {src} 추천 상위 {it['percentile']}%"
            f" ({it['points']}표, 댓글 {it['comments']})"
            f" | {it['domain']}\n  제목: {it['title']}\n  요약: {body}"
        )
    return f"""너는 kil9 의 til 사이트 큐레이터다. 오늘 GeekNews(GN)와 Hacker News(HN)에 올라온
아래 후보 중에서 관리자가 읽을 만한 것을 고른다.

{profile}

# 후보
{chr(10).join(lines)}

# 지난 피드백에서 나온 규칙 (관리자가 직접 남긴 것이다. 아래 일반 규칙보다 우선한다)
{chr(10).join("- " + r for r in rules) or "- (없음)"}

# 규칙
- [인기축 확정] 표시가 붙은 것은 관심사와 무관해도 반드시 포함한다(이미 확정이니 다시 고르지 않아도 된다).
- [GN 출처 우선 확정] 표시가 붙은 것도 품질과 무관하게 반드시 포함한다.
- 출처 우선순위는 GN > HN 이다. 품질·추천 백분위·관심사가 다소 낮아도 GN 후보를 HN보다 먼저 고른다.
- 확정분을 포함해 총 {want}건 안팎이 되도록 나머지를 관심사 프로필 매칭으로 고른다.
  재료가 빈약하면 {TOTAL_MIN}건, 좋으면 {TOTAL_MAX}건까지 그날 사정에 맞춰 정하라.
- 같은 사건을 다룬 중복 항목은 하나만 남긴다. 원문 URL 이 같은 것은 이미 합쳐 두었지만,
  다른 URL 로 같은 사건을 다룬 GN·HN 항목이 따로 올라올 수 있다. 그때는 한쪽만 고른다.
- 백분위는 소스 안에서의 순위다. GN 상위 5% 와 HN 상위 5% 는 모집단이 다르니 그 수만 보고
  둘을 견주지 마라. 무엇을 고를지는 관심사 프로필과 내용으로 판단한다.
- [… 브리핑에 이미 실림] 표시가 붙은 것은 기본적으로 뺀다. 그날 이후 실제로 달라진 것
  (중요한 후속 소식, 논의가 크게 붙은 댓글)이 있을 때만 남기고, why 에 무엇이 새로운지 적는다.
  재료가 모자라 자리를 못 채우겠으면 {TOTAL_MIN}건에 못 미쳐도 좋으니 재탕으로 채우지 마라.
- 홍보성 글, 내용 없는 공지, 관리자가 이미 til 에서 다룬 주제의 재탕은 뺀다.
- 모든 후보에 관심사 등급을 매긴다: 최상 / 상 / 중 / 밖.

# 출력 (JSON 만, 설명·코드블록 금지)
{{
  "selected": [{{"id": "12345", "interest": "최상", "why": "왜 골랐는지 한 줄"}}],
  "rest": [{{"id": "12346", "interest": "중", "why": "왜 뺐는지 한 줄"}}]
}}
selected 는 고른 것, rest 는 나머지 전부다. 두 목록을 합치면 후보 전체가 되어야 한다."""


def main():
    today = os.environ.get("BRIEFING_DATE") or datetime.now(KST).date().isoformat()
    src = STATE / f"collected-{today}.json"
    if not src.exists():
        print(f"수집 파일이 없다: {src}", file=sys.stderr)
        return 2
    data = json.loads(src.read_text(encoding="utf-8"))
    items = {it["id"]: it for it in data["items"]}
    if not items:
        print("신규 항목 없음 — 선별 생략")
        return 3

    aired = aired_before(today)
    # id 로도 원문 URL 로도 본다. 항목마다 한 번만 판정해 두고 아래에서 재사용한다.
    aired_by_item = {i: aired_on(it, aired) for i, it in items.items()}
    reaired = [i for i, day in aired_by_item.items() if day]
    if reaired:
        by_url = sum(1 for i in reaired if i not in aired)
        tail = f" (그중 {by_url}건은 원문 URL 로 잡았다)" if by_url else ""
        print(f"  지난 회차에 실렸던 {len(reaired)}건 재등장 — 순위 {REAIR_PENALTY} 포인트 강등{tail}")

    def effective(it):
        """정렬·컷에 쓰는 백분위. 재등장 항목은 크게 뒤로 민다(낮을수록 앞)."""
        return it["percentile"] + (REAIR_PENALTY if aired_by_item.get(it["id"]) else 0.0)

    ranked = sorted(items.values(), key=lambda it: (source_order(it), effective(it), -it["points"]))
    fresh = [it for it in ranked if not aired_by_item.get(it["id"])]
    # 인기 축은 새 항목에서만 뽑는다. 재등장 항목이 추천수만으로 다시 확정되면
    # 위 패널티가 무의미해진다. 소스별 상한을 함께 걸어 한쪽이 확정 슬롯을 독점하지 못하게 한다.
    popular, taken = [], {}
    for it in fresh:
        if it["percentile"] > POPULAR_CUT or len(popular) >= POPULAR_MAX:
            continue
        isrc = it.get("source", "gn")
        if taken.get(isrc, 0) >= POPULAR_MAX_BY_SOURCE.get(isrc, POPULAR_MAX):
            continue
        popular.append(it)
        taken[isrc] = taken.get(isrc, 0) + 1
    if len(popular) < POPULAR_MIN:
        popular = (fresh or ranked)[:POPULAR_MIN]   # 컷을 넘긴 게 없으면 상위 2건으로 폴백
    popular_ids = {it["id"] for it in popular}
    gn_priority = [it for it in fresh if it.get("source", "gn") == "gn"][:GN_PRIORITY_MIN]
    gn_priority_ids = {it["id"] for it in gn_priority}
    forced = popular_ids | gn_priority_ids
    print(f"인기 축 확정 {len(popular_ids)}건 {taken or ''} "
          f"(백분위 컷 {POPULAR_CUT}%, 기준 {data['percentile_basis']})")
    print(f"GN 출처 우선 확정 {len(gn_priority_ids)}건 (목표 {GN_PRIORITY_MIN}건)")

    candidates = ranked[:CANDIDATE_LIMIT]
    want = min(TOTAL_MAX, max(TOTAL_MIN, len(forced) + 5))
    rules = feedback.active_rules(today)
    if rules:
        print(f'  선별 규칙 {len(rules)}개 적용')
    verdict = ask_complete_verdict(
        build_prompt(interest_profile(), candidates, popular_ids, gn_priority_ids,
                     aired_by_item, want, rules),
        [it["id"] for it in candidates],
    )

    grades = {r["id"]: r.get("interest", "중") for r in verdict.get("selected", []) + verdict.get("rest", [])}
    whys = {r["id"]: r.get("why", "") for r in verdict.get("selected", []) + verdict.get("rest", [])}
    chosen_ids = {r["id"] for r in verdict.get("selected", [])} | forced
    chosen_ids = {i for i in chosen_ids if i in items}
    if len(chosen_ids) > TOTAL_MAX:      # 넘치게 골랐으면 인기 확정분 먼저, 그다음 백분위 순으로 자른다
        keep = sorted((items[i] for i in chosen_ids),
                      key=lambda it: (it["id"] not in forced, source_order(it), effective(it)))[:TOTAL_MAX]
        chosen_ids = {it["id"] for it in keep}

    def sort_key(it):
        return (source_order(it),
                effective(it) - INTEREST_BONUS.get(grades.get(it["id"], "중"), 0.0),
                -it["points"])

    def decorate(it):
        it = dict(it)
        it["interest"] = grades.get(it["id"], "중")
        it["why"] = whys.get(it["id"], "")
        it["forced_popular"] = it["id"] in forced
        it["aired_on"] = aired_by_item.get(it["id"]) or ""
        return it

    selected = sorted((decorate(items[i]) for i in chosen_ids), key=sort_key)
    rest = sorted((decorate(it) for it in items.values() if it["id"] not in chosen_ids), key=sort_key)

    out = dict(data)
    out.pop("items")                        # 선별 결과(selected/rest)로 대체한다
    out.update({"selected": selected, "rest": rest, "popular_cut": POPULAR_CUT,
                "source_priority": ["gn", "hn"], "gn_priority_min": GN_PRIORITY_MIN,
                "selected_at": datetime.now(KST).isoformat(timespec="minutes")})
    path = STATE / f"selected-{today}.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    # 소스 구성을 남긴다. 균형을 강제하지는 않지만(task-106 확정 사항) 한쪽으로 쏠린 회차가
    # 이어지는지는 보여야 한다 — GeekNews 가 얇은 날은 관심사 축이 HN 으로 채워진다.
    mix = {s: sum(1 for it in selected if it.get("source", "gn") == s) for s in ("gn", "hn")}
    print(f"  선별 {len(selected)}건 (GN {mix['gn']} / HN {mix['hn']}) / 제외 {len(rest)}건 → {path.name}")
    for it in selected:
        tail = f"  (재등장 {it['aired_on']})" if it["aired_on"] else ""
        print(f"   {it['percentile']:>5}% {it['interest']:<2} {it['title'][:44]}{tail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
