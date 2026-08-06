#!/usr/bin/env python3
"""1차 선별 — 수집분에서 오늘 실을 7-10건을 고른다 (task-80).

선별은 두 축이다.
  인기 축  최근 30일 롤링 분포의 백분위 상위 10%(p90) 를 통과한 것. 관심사와
           무관해도 무조건 싣되 2-5건으로 clamp 한다.
  관심사 축 til 분포에서 뽑은 관심사 프로필(interest-profile.py)과의 매칭.
           모델이 나머지 자리를 채운다.

정렬은 추천 백분위가 1순위다. 관심사는 동률·인접 보정에만 쓴다 — 관심사가 맞아도
추천이 낮으면 아래로 내려간다(파일럿 v6 확정).

입력: state/collected-<날짜>.json    출력: state/selected-<날짜>.json
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import feedback
import llm

BASE = Path(__file__).resolve().parent
STATE = BASE / "state"
KST = timezone(timedelta(hours=9))

POPULAR_CUT = 10.0        # 백분위 상위 N% = p90
POPULAR_MIN, POPULAR_MAX = 2, 5
TOTAL_MIN, TOTAL_MAX = 7, 10
CANDIDATE_LIMIT = 40      # 프롬프트에 싣는 후보 수 상한

# 관심사 등급이 순위에 끼치는 보정폭(백분위 포인트). 인접한 항목끼리만 뒤집히도록 작게 둔다.
INTEREST_BONUS = {"최상": 2.0, "상": 1.2, "중": 0.4, "밖": 0.0}

AIRED_LOOKBACK = 30       # 재등장 판정에 볼 지난 회차 범위(일)
REAIR_PENALTY = 40.0      # 이전 회차에 실린 항목의 백분위 패널티. 관심사 보정(최대 2.0)과
                          # 자릿수가 달라 사실상 새 항목 뒤로 밀린다.


def aired_before(today):
    """지난 회차에 실제로 실린 항목 → 그 회차 날짜.

    collect.py 는 신규가 얇은 날 목록 전체로 backfill 한다(매일 발행이 중복 회피보다
    우선이라는 결정). 그 대가로 어제 실은 글이 오늘 후보에 다시 올라오고, 추천수가
    높으면 인기 축으로 또 실린다 — 2026-07-30/31 에 2건이 그렇게 연달아 나갔다.
    수집을 조이는 대신 여기서 순위를 크게 눌러 새 항목에 자리를 내준다.
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
    return out


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


def build_prompt(profile, candidates, forced_ids, aired, want, rules):
    lines = []
    for it in candidates:
        mark = " [인기축 확정]" if it["id"] in forced_ids else ""
        if it["id"] in aired:
            mark += f" [{aired[it['id']]} 브리핑에 이미 실림]"
        body = (it.get("summary") or it.get("desc") or "")[:400]
        lines.append(
            f"- id={it['id']}{mark} | 추천 상위 {it['percentile']}% ({it['points']}표, 댓글 {it['comments']})"
            f" | {it['domain']}\n  제목: {it['title']}\n  요약: {body}"
        )
    return f"""너는 kil9 의 til 사이트 큐레이터다. 오늘 GeekNews 에 올라온 아래 후보 중에서
관리자가 읽을 만한 것을 고른다.

{profile}

# 후보
{chr(10).join(lines)}

# 지난 피드백에서 나온 규칙 (관리자가 직접 남긴 것이다. 아래 일반 규칙보다 우선한다)
{chr(10).join("- " + r for r in rules) or "- (없음)"}

# 규칙
- [인기축 확정] 표시가 붙은 것은 관심사와 무관해도 반드시 포함한다(이미 확정이니 다시 고르지 않아도 된다).
- 확정분을 포함해 총 {want}건 안팎이 되도록 나머지를 관심사 프로필 매칭으로 고른다.
  재료가 빈약하면 {TOTAL_MIN}건, 좋으면 {TOTAL_MAX}건까지 그날 사정에 맞춰 정하라.
- 같은 사건을 다룬 중복 항목은 하나만 남긴다.
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
    reaired = [i for i in items if i in aired]
    if reaired:
        print(f"  지난 회차에 실렸던 {len(reaired)}건 재등장 — 순위 {REAIR_PENALTY} 포인트 강등")

    def effective(it):
        """정렬·컷에 쓰는 백분위. 재등장 항목은 크게 뒤로 민다(낮을수록 앞)."""
        return it["percentile"] + (REAIR_PENALTY if it["id"] in aired else 0.0)

    ranked = sorted(items.values(), key=lambda it: (effective(it), -it["points"]))
    fresh = [it for it in ranked if it["id"] not in aired]
    # 인기 축은 새 항목에서만 뽑는다. 재등장 항목이 추천수만으로 다시 확정되면
    # 위 패널티가 무의미해진다.
    popular = [it for it in fresh if it["percentile"] <= POPULAR_CUT][:POPULAR_MAX]
    if len(popular) < POPULAR_MIN:
        popular = (fresh or ranked)[:POPULAR_MIN]   # 컷을 넘긴 게 없으면 상위 2건으로 폴백
    forced = {it["id"] for it in popular}
    print(f"인기 축 확정 {len(forced)}건 (백분위 컷 {POPULAR_CUT}%, 기준 {data['percentile_basis']})")

    candidates = ranked[:CANDIDATE_LIMIT]
    want = min(TOTAL_MAX, max(TOTAL_MIN, len(forced) + 5))
    rules = feedback.active_rules(today)
    if rules:
        print(f'  선별 규칙 {len(rules)}개 적용')
    verdict = llm.ask_json(build_prompt(interest_profile(), candidates, forced, aired, want, rules))

    grades = {r["id"]: r.get("interest", "중") for r in verdict.get("selected", []) + verdict.get("rest", [])}
    whys = {r["id"]: r.get("why", "") for r in verdict.get("selected", []) + verdict.get("rest", [])}
    chosen_ids = {r["id"] for r in verdict.get("selected", [])} | forced
    chosen_ids = {i for i in chosen_ids if i in items}
    if len(chosen_ids) > TOTAL_MAX:      # 넘치게 골랐으면 인기 확정분 먼저, 그다음 백분위 순으로 자른다
        keep = sorted((items[i] for i in chosen_ids),
                      key=lambda it: (it["id"] not in forced, effective(it)))[:TOTAL_MAX]
        chosen_ids = {it["id"] for it in keep}

    def sort_key(it):
        return (effective(it) - INTEREST_BONUS.get(grades.get(it["id"], "중"), 0.0), -it["points"])

    def decorate(it):
        it = dict(it)
        it["interest"] = grades.get(it["id"], "중")
        it["why"] = whys.get(it["id"], "")
        it["forced_popular"] = it["id"] in forced
        it["aired_on"] = aired.get(it["id"], "")
        return it

    selected = sorted((decorate(items[i]) for i in chosen_ids), key=sort_key)
    rest = sorted((decorate(it) for it in items.values() if it["id"] not in chosen_ids), key=sort_key)

    out = dict(data)
    out.pop("items")                        # 선별 결과(selected/rest)로 대체한다
    out.update({"selected": selected, "rest": rest, "popular_cut": POPULAR_CUT,
                "selected_at": datetime.now(KST).isoformat(timespec="minutes")})
    path = STATE / f"selected-{today}.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  선별 {len(selected)}건 / 제외 {len(rest)}건 → {path.name}")
    for it in selected:
        tail = f"  (재등장 {it['aired_on']})" if it["aired_on"] else ""
        print(f"   {it['percentile']:>5}% {it['interest']:<2} {it['title'][:44]}{tail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
