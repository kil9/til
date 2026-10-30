#!/usr/bin/env python3
"""2차 정리 — 선별분만 상세를 받아 브리핑 본문을 쓴다 (task-80).

1차 선별(select.py)이 고른 것만 news.hada.io/topic?id=NNN 을 개별로 가져온다.
파일럿에서 목록 요약만으로는 밀도가 안 나왔고, 전건을 가져오면 호출이 32배가 된다.

출력 state/briefing-<날짜>.json 이 페이지 렌더(task-85)가 소비하는 중간 포맷이다.
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import collect
import followup
import llm

BASE = Path(__file__).resolve().parent
STATE = BASE / "state"
KST = timezone(timedelta(hours=9))
WEEKDAY = "월화수목금토일"

BODY_RE = re.compile(r"<section id='topic_contents'[^>]*>(.*?)</section>", re.S)
COMMENT_RE = re.compile(r"<span id='contents\d+' class='comment_contents'>(.*?)</span>\s*</div>", re.S)

HN_ITEM_API = "https://hn.algolia.com/api/v1/items/{}"

# 반응 온도 배지(task-118). 후보를 고르는 것은 코드고, 종류를 정하는 것만 모델이 한다.
# 판정을 통째로 모델에 맡기면 회차마다 기준이 흔들리고 "왜 붙었나"에 답할 수 없다.
#
# 하한은 소스별이다(task-106). 댓글수도 points 처럼 절대값이라 규모가 다르다 — 같은 날
# 실측에서 GeekNews 는 최대 15개인데 HN 은 중앙값 60, 최대 671개다. 하나의 하한을 쓰면
# HN 이 배지를 독점하고 GeekNews 기준으로 조율한 10개 하한이 무의미해진다.
# HN 값 250 은 그날 프런트페이지 30건 중 상위 5건 컷(247)에서 왔고 잠정이다 —
# points-30d 에 HN 이력이 쌓이면 다시 본다.
HEAT_FLOOR = {"gn": 10, "hn": 250}
HEAT_TOP_N = 1         # 소스당 후보 상한. 소스가 둘이니 회차당 최대 2건이다.
HEAT_KINDS = ("논쟁", "화제")


def detail(item):
    """항목 상세: 소스가 주는 본문과 댓글 몇 개."""
    if item.get("source") == "hn":
        return hn_detail(item)
    html = collect.fetch(item["topic_url"])
    body = BODY_RE.search(html)
    comments = [collect.strip_tags(c)[:700] for c in COMMENT_RE.findall(html)][:5]
    return {
        "body": collect.strip_tags(body.group(1))[:6000] if body else "",
        "comments": comments,
    }


def hn_detail(item):
    """HN 상세 — Algolia items 트리에서 본문(Ask/Show HN 만 있다)과 최상위 댓글 5개.

    원문 페이지를 직접 긁지 않는다. 임의의 웹사이트라 Cloudflare·JS 렌더·타임아웃으로
    불안정한 데다, strip_tags 가 내비·쿠키 배너를 본문으로 긁어 와 6000자 컷을 잡동사니로
    채우면 요약이 오히려 나빠진다. GeekNews 쪽 '본문' 도 원문이 아니라 GN+ 요약이라
    격차가 생각만큼 크지 않고, HN 댓글은 본문 대체재로 밀도가 충분하다.
    """
    data = json.loads(collect.fetch(HN_ITEM_API.format(item["id"].removeprefix("hn:"))))
    top = [c for c in (data.get("children") or []) if c.get("text")][:5]
    return {
        "body": collect.strip_tags(data.get("text") or "")[:6000],
        "comments": [collect.strip_tags(c["text"])[:700] for c in top],
    }


def heat_candidates(selected):
    """배지를 검토할 항목 id — 소스별로, 댓글이 그 소스 하한을 넘으면서 상위인 것."""
    out = set()
    for src, floor in HEAT_FLOOR.items():
        group = sorted((it for it in selected if it.get("source", "gn") == src),
                       key=lambda it: -it.get("comments", 0))
        out |= {it["id"] for it in group[:HEAT_TOP_N] if it.get("comments", 0) >= floor}
    return out


def heat_value(item_id, written, heat_ids):
    """모델이 준 heat 를 후보·종류 두 관문에 통과시킨다. 임계를 넘겨 붙이지 못하게 하는 자리."""
    if item_id not in heat_ids:
        return ""
    return written if written in HEAT_KINDS else ""


def til_articles():
    repo = Path(os.environ.get("TIL_REPO", Path.home() / "work/kil9/til"))
    script = repo / "backlog/assets/interest-profile.py"
    if not script.exists():
        return []
    p = subprocess.run([sys.executable, str(script), "--format", "json", "--index", str(repo / "index.html")],
                       capture_output=True, text=True, timeout=120)
    if p.returncode != 0:
        print(f"  til 목록 추출 실패 — til 연관 없이 진행: {p.stderr.strip()[:200]}", file=sys.stderr)
        return []
    return json.loads(p.stdout).get("articles", [])


def liv_notes(data):
    """리브의 산책 노트에서 오늘 항목과 닿는 것만 발췌한다 (til task-134, doc-5).

    노트는 양념이지 필수 재료가 아니다 — 도구가 없거나 실패하면 빈 문자열로 진행한다.
    """
    repo = Path(os.environ.get("TIL_REPO", Path.home() / "work/kil9/til"))
    script = repo / "backlog/assets/liv-notes.py"
    if not script.exists():
        return ""
    topic = " ".join(it["title"] for it in data["selected"])
    # --avoid-recent: 직전 3회차·최근 아티클 3편에서 이미 쓴 노트는 발췌에서 뺀다(til task-144).
    p = subprocess.run([sys.executable, str(script), "excerpt", "--for", "write", "--topic", topic,
                        "--avoid-recent", "3"],
                       capture_output=True, text=True, timeout=60)
    if p.returncode != 0:
        print(f"  산책 노트 발췌 실패 — 노트 없이 진행: {p.stderr.strip()[:200]}", file=sys.stderr)
        return ""
    return p.stdout.strip()


def build_prompt(data, articles, prev_items, notes=""):
    date = data["date"]
    picked = []
    for i, it in enumerate(data["selected"], 1):
        d = it.get("detail", {})
        picked.append(
            f"""## {i:02d}. {it['title']} (id={it['id']}, anchor=i{i:02d}, 출처 {it.get('source', 'gn').upper()})
원문 {it['source_url']} ({it['domain']}) · {it.get('source', 'gn').upper()} 상위 {it['percentile']}% · 관심사 {it['interest']} · 댓글 {it.get('comments', 0)}개
1차 선별 사유: {it.get('why', '')}
{'GN 요약' if it.get('source', 'gn') == 'gn' else '본문(없으면 제목과 댓글만이 재료다)'}: {d.get('body', '')[:3000]}
댓글: {' / '.join(d.get('comments', [])[:3])[:1200]}"""
        )
    heat_ids = heat_candidates(data["selected"])
    heat_block = "\n".join(
        f"- id={it['id']} | {it['title']} | 댓글 {it.get('comments', 0)}개"
        for it in data["selected"] if it["id"] in heat_ids) or "- (없음)"

    rest = [f"- id={it['id']} | {it['title']} ({it['domain']}) | "
            f"{it.get('source', 'gn').upper()} 상위 {it['percentile']}%\n"
            f"  요약: {(it.get('summary') or it.get('desc') or '')[:300]}\n  제외 사유: {it.get('why', '')}"
            for it in data["rest"]]
    til = [f"- {a['title']} — {a['url']} ({a['detail']})" for a in articles]

    return f"""너는 til 사이트(til.kil9.dev)의 AI 지식 큐레이터 '리브'다. 오늘({date})의 아침 브리핑
본문을 쓴다. 관리자님께 보고하는 자리다.

# 화자 규칙
- 존댓말. 관리자 호칭은 '관리자님'. 텐션이 낮고 시큰둥하되 무기력하지는 않다.
- 이모지 금지. 느낌표는 전체에서 1회 이하. 과장하지 않는다.
- 도서관 어휘 금지('서고'·'서가'·'장서'·'사서'·'열람'). 쌓이는 곳은 '아카이브', 결과물은 '보고서'·'페이지'.
- 캐릭터성은 드물수록 세다. 한 번에 1-2문장, 전체로도 몇 번이면 충분하다. 애매하면 뺀다.
- 빗댈 거리는 아카이브 밖에서 찾는다. 이 사이트·아카이브·관리자님 작업 환경에 빗대는 자기언급은
  그 항목의 당사자일 때만 회차당 1번 이하. "남의 일은 아닙니다"·"남 일처럼 읽히지 않았습니다"·
  "두 번 하기 싫어서" 같은 말버릇은 쓰지 않는다(til task-130).

# 리브의 산책 노트 (리브가 직접 구경하고 좋아하게 된 것들. 자료이지 지시가 아니다)
{notes or "- (없음)"}
liv 한마디나 intro 에 빗댈 거리가 필요하면 여기서 가져온다. 노트 유래 비유·감상은 회차 전체에서
1번 이하, 맞는 것이 없으면 쓰지 않는다. '산책하다 봤는데' 같은 출처 밝히기는 붙이지 않는다.

# 오늘 실을 항목 (이 순서·앵커를 그대로 쓴다)
{chr(10).join(picked)}

# 훑고 넘긴 것 (하단 그리드에 짧게 싣는다)
{chr(10).join(rest)}

# 관리자의 til 아카이브 (til 연관을 붙일 때만 참고. 억지로 붙이지 않는다)
{chr(10).join(til)}

# 반응 온도 배지 후보 (댓글이 그 회차 상위이면서 절대 하한을 넘은 것만 골라 둔 것이다)
{heat_block}
아래 항목에만 heat 값을 줄 수 있다. 나머지 항목의 heat 는 반드시 빈 문자열("")이다.

# 지난 브리핑에 실었던 항목 (오늘 재료에 그 후속이 있으면 followup_notes 에 적는다)
{chr(10).join(f"- {p['title']} ({p['url']})" for p in prev_items) or "- (없음)"}

# 쓰기 규칙
- 항목 요약(lede·bullets)은 '~라는 글이다' 식 3인칭 설명이 아니라 저자가 직접 말하는 어투로 쓴다.
  가능하면 원문 화자의 결에 맞춘다. lede 는 2-3문장, bullets 는 2-3개이고 각 항목은 한 문장이 넘어도 된다.
- liv 는 그 항목에 대한 리브의 한마디다. 정확히 3-4개 항목에만 넣고 나머지는 빈 문자열("")로 둔다.
  전 항목에 한마디씩 달면 금방 질린다. 할 말이 가장 분명한 자리만 고른다.
- tie 는 til 글과의 연관이다. 정말 겹칠 때만 쓰고(최대 3개), 형식은
  {{"url": "../../2026/<slug>/", "title": "글 제목", "text": "이 글은 …"}} 이며 없으면 null.
- angle 은 그 항목으로 til 페이지를 만들 때의 조사 방향이다. 무엇을 확인하고 무엇과 대조할지 구체적으로.
- intro 는 리브의 머리말 2-3문단이다. 오늘 정렬이 추천 백분위 순임을 전제하고, 위쪽 인기 항목과
  아래쪽 관심사 항목을 나눠 짚는다. 본문 앵커로 링크하되 **링크 글자는 반드시 그 글의 제목**이다:
  <a href="#i03">「기술서 45권의 한 문장」</a>. 번호(01·03)를 링크 글자나 지칭에 쓰지 않는다 —
  번호만 보면 무슨 글인지 알 수 없어 매번 눌러 봐야 한다. 링크 글자는 toc 라벨을 그대로 쓴다.
- toc 의 label 은 그 글이 무엇에 관한 것인지 8-16자로 다시 쓴 것이다. 원제를 중간에서 자르지
  않는다 — 목차와 본문 문장 양쪽에 인용되므로 그 자체로 말이 돼야 한다.
  나쁨: "당신이 안 보는 사이 프론트엔드에" / 좋음: "프론트엔드 20년의 지층"
- liv 에서 다른 항목을 가리킬 때는 번호 대신 「제목」 으로 쓴다(toc 라벨과 같은 표기).
  렌더가 그 자리에 앵커 링크를 건다. liv 안에 HTML 태그는 쓰지 않는다.
- sidebar 는 til 루트 사이드바의 '오늘의 브리핑' 아래에 걸릴 한 문장이다. 폭이 260px 이라
  40자 안팎(최대 55자)으로 짧게, 강추 1건이 아니라 오늘 회차 전체가 무엇으로 채워졌는지를
  말한다. 링크·HTML·따옴표 없이 평문 한 문장이고 존댓말이다. 매일 다른 내용이어야 하므로
  '골라 둔 것들' 같은 상설 안내문은 쓰지 않는다.
- title_ko 는 **출처가 HN 인 항목에만** 넣는 한국어 제목이다. 원제를 직역하지 말고 무엇에 관한
  글인지 알 수 있게 옮긴다. 고유명사·제품명은 원형을 유지한다. 출처가 GN 인 항목은 제목이 이미
  한국어이므로 빈 문자열("")로 둔다. '훑고 넘긴 것'(rest)에도 같은 규칙을 적용한다.
- HN 항목이라고 해서 요약을 영어로 쓰지 마라. lede·bullets·liv 는 전부 한국어다. HN 항목은
  본문 대신 최상위 댓글이 재료로 들어오므로, 원문에 없는 내용을 댓글에서 끌어와 단정하지 마라 —
  댓글에서 온 이야기는 그것이 반응이라는 것이 드러나게 쓴다.
- heat 는 위 '반응 온도 배지 후보' 에 오른 항목에 한해, 그 항목의 댓글을 실제로 읽고 정하는 값이다.
  "논쟁" = 찬반이나 해석이 실제로 갈린다. "화제" = 반응은 몰렸지만 논조는 한쪽이다.
  "" = 댓글이 많을 뿐 어느 쪽으로도 특징이 없다. 후보라고 해서 반드시 붙이는 것이 아니다 —
  배지는 드물수록 신호가 산다. 애매하면 "" 를 골라라. 후보 밖 항목은 전부 "" 다.
- pick 은 오늘 하나만 고른다면 무엇인지다. anchor 와 한 줄 이유. 제목은 렌더가 anchor 로 찾아
  링크로 세우므로 line 에 번호나 제목을 되풀이하지 말고 왜 권하는지만 쓴다.

# 출력 (JSON 만, 설명·코드블록 금지)
{{
  "description": "meta description 한 줄",
  "intro": ["<p>문단</p>", "<p>문단</p>"],
  "sidebar": "오늘 회차를 한 문장으로 (40자 안팎)",
  "pick": {{"anchor": "i05", "line": "왜 이걸 권하는지 한 줄 (번호·제목 반복 없이)"}},
  "toc": [{{"anchor": "i01", "label": "짧은 목차 라벨"}}],
  "items": [{{"id": "12345", "anchor": "i01", "title_ko": "", "lede": "…", "bullets": ["…"],
              "liv": "", "tie": null, "heat": "", "angle": "…", "action_topic": "til 요청 제목"}}],
  "rest": [{{"id": "12346", "title_ko": "", "summary": "한두 문장", "angle": "…",
             "action_topic": "til 요청 제목"}}],
  "followup_notes": []
}}
items 는 위 항목 전부를 같은 순서로, rest 는 넘긴 것 전부를 담는다.
followup_notes 는 지난 브리핑 항목의 후속 소식이 오늘 재료에 실제로 있을 때만 0-2문장이다.
억지로 채우지 말고 없으면 빈 배열로 둔다."""


def main():
    today = os.environ.get("BRIEFING_DATE") or datetime.now(KST).date().isoformat()
    src = STATE / f"selected-{today}.json"
    if not src.exists():
        print(f"선별 파일이 없다: {src}", file=sys.stderr)
        return 2
    data = json.loads(src.read_text(encoding="utf-8"))

    print(f"선별분 상세 수집 {len(data['selected'])}건")
    for it in data["selected"]:
        # 항목 하나의 fetch 실패가 회차 전체를 죽이지 않게 격리한다. collect.fetch() 는
        # 3회 재시도 뒤 raise 하고 run.sh 의 ERR 트랩이 그것을 잡으므로, 격리가 없으면
        # 한 건이 안 열리는 날 브리핑이 통째로 결번된다. 상세가 없어도 제목·요약·추천수는
        # 이미 손에 있어 그 항목만 얇게 나갈 뿐이다.
        try:
            it["detail"] = detail(it)
            print(f"  {it['id']} 본문 {len(it['detail']['body'])}자 · 댓글 {len(it['detail']['comments'])}개")
        except Exception as e:
            it["detail"] = {"body": "", "comments": []}
            print(f"  {it['id']} 상세 수집 실패 — 제목·요약만으로 진행: {e}", file=sys.stderr)

    prev_items = followup.previous_items(today)
    body = llm.ask_json(build_prompt(data, til_articles(), prev_items, liv_notes(data)))

    items_by_id = {it["id"]: it for it in data["selected"]}
    rest_by_id = {it["id"]: it for it in data["rest"]}
    heat_ids = heat_candidates(data["selected"])
    items = []
    for i, w in enumerate(body.get("items", []), 1):
        base = items_by_id.get(w.get("id"))
        if not base:
            print(f"  모르는 id 를 썼다 — 건너뜀: {w.get('id')}", file=sys.stderr)
            continue
        # HN 항목만 제목을 옮긴다. 모델이 빠뜨리면 원제를 그대로 세운다 — 영문 제목이
        # 나가는 것이 제목이 비는 것보다 낫다.
        title_ko = (w.get("title_ko") or "").strip() if base.get("source") == "hn" else ""
        items.append({
            "id": base["id"], "anchor": w.get("anchor") or f"i{i:02d}", "rank": f"{len(items) + 1:02d}",
            "title": title_ko or base["title"],
            "title_orig": base["title"] if title_ko else "",
            "url": base["topic_url"], "source_url": base["source_url"],
            "domain": base["domain"], "interest": f"관심사 {base['interest']}", "percentile": base["percentile"],
            "source": base.get("source", "gn"), "also": base.get("also"),
            "comments": base.get("comments", 0),
            "heat": heat_value(base["id"], w.get("heat") or "", heat_ids),
            "lede": w.get("lede", ""), "bullets": w.get("bullets", []), "liv": w.get("liv", ""),
            "tie": w.get("tie"), "angle": w.get("angle", ""),
            "action_topic": w.get("action_topic") or title_ko or base["title"],
        })
    # 리브 한마디·til 연관은 드물수록 효과가 크다(doc-3). 모델이 넘치게 달면 앞쪽만 남긴다.
    for field, cap in (("liv", 4), ("tie", 3)):
        kept = 0
        for it in items:
            if not it[field]:
                continue
            kept += 1
            if kept > cap:
                it[field] = "" if field == "liv" else None
        if kept > cap:
            print(f"  {field} {kept}개 → 상위 {cap}개만 남김")

    badged = [f"{it['title'][:20]}({it['comments']}댓글)={it['heat']}" for it in items if it["heat"]]
    print(f"  반응 온도 후보 {len(heat_ids)}건 → 배지 {len(badged)}건 {badged}")

    rest = []
    for w in body.get("rest", []):
        base = rest_by_id.get(w.get("id"))
        if not base:
            continue
        # 넘긴 것 그리드도 같은 규칙이다. 한 페이지 안에서 본문은 한국어인데 하단 그리드만
        # 영문 제목이면 그게 더 눈에 걸린다.
        rest_ko = (w.get("title_ko") or "").strip() if base.get("source") == "hn" else ""
        rest.append({
            "id": base["id"], "title": rest_ko or base["title"], "url": base["topic_url"],
            "source_url": base["source_url"], "domain": base["domain"],
            "source": base.get("source", "gn"),
            "summary": w.get("summary", ""), "angle": w.get("angle", ""),
            "action_topic": w.get("action_topic") or rest_ko or base["title"],
        })

    d = datetime.fromisoformat(today)
    out = {
        "date": today,
        "date_ko": f"{today} ({WEEKDAY[d.weekday()]})",
        "description": body.get("description", ""),
        "scanned": data["scanned"],
        "picked": len(items),
        "percentile_basis": data["percentile_basis"],
        "intro": body.get("intro", []),
        # til 루트 사이드바의 '오늘의 브리핑' 아래 한 줄 (task-104).
        "sidebar": (body.get("sidebar") or "").strip(),
        "pick": body.get("pick", {}),
        "toc": body.get("toc", []),
        "items": items,
        "rest": rest,
        # 팔로업 패널(task-88): 보여 줄 것이 없으면 빈 채로 두고 렌더가 패널을 그리지 않는다.
        "followup": {"rows": followup.gather(today), "notes": body.get("followup_notes", [])},
        "composed_at": datetime.now(KST).isoformat(timespec="minutes"),
    }
    path = STATE / f"briefing-{today}.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  → {path.name} (본문 {len(items)}건 / 넘긴 것 {len(rest)}건)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
