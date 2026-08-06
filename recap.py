#!/usr/bin/env python3
"""주간 리캡 — 그 주 브리핑을 관통하는 흐름 한 편 (task-91, task-117 로 형식 개편).

일간 브리핑은 그날 안에서만 본다. 며칠에 걸쳐 이어지는 추세는 일간으로는 안 보인다.
형식도 다르다 — 항목 나열이 아니라 산문 한 편이다.

회차 구성은 셋이다(task-117).
  헤드라인   제목 + 한 줄. 모델의 title·description 을 그대로 크게 세운다.
  타임라인   요일별 한 줄. 각 회차의 sidebar 문장을 그대로 옮기는 결정적 생성이라
             모델을 거치지 않는다 — 모델에 맡기면 이미 있는 정보를 지어낼 수 있는
             형태로 두 번 싣게 된다.
  이야기     2편 이상. 여기만 모델이 쓰고, 주장의 근거는 그 주 데일리 회차의 항목
             앵커로 링크한다. 링크는 대조표로 검증해 지어낸 것을 떼어 낸다.

잘 나오면 til 정식 페이지로 승격할 만하다. 다만 자동으로 갤러리에 올리지는 않는다.
모델이 승격 여부를 판단해 근거와 함께 Slack 으로 제안하고, 결정은 관리자가 한다.

사용법: python3 recap.py <til-repo> [YYYY-MM-DD]   (일요일 cron)
"""

import base64
import html
import json
import os
import re
import sys
import urllib.parse
from datetime import datetime, timedelta, timezone
from pathlib import Path

import announce
import llm
import render as R

BASE = Path(__file__).resolve().parent
STATE = BASE / "state"
KST = timezone(timedelta(hours=9))
DAYS = 7
MIN_BRIEFINGS = 3        # 이보다 적으면 관통할 흐름이 없다
MIN_STORIES = 2          # 이야기가 이보다 적으면 일간 회차와 다를 것이 없다
INBOX = "https://github.com/kil9/til-inbox/issues/new"

# 이야기 본문의 근거 링크. 모델은 [[2026-08-04#i03|링크 글자]] 로만 쓰고,
# 렌더가 그 주 회차의 실제 앵커와 대조해 통과한 것만 <a> 로 세운다.
REF_RE = re.compile(r"\[\[(\d{4}-\d{2}-\d{2})#(i\d{2})\|([^\]|]+)\]\]")


def week(today):
    """최근 DAYS 일치 브리핑 재료(최신순)."""
    start = (datetime.fromisoformat(today) - timedelta(days=DAYS - 1)).date().isoformat()
    out = []
    for p in sorted(STATE.glob("briefing-*.json"), reverse=True):
        date = p.stem.replace("briefing-", "")
        if start <= date <= today:
            out.append(json.loads(p.read_text(encoding="utf-8")))
    return out


def anchor_index(days):
    """(날짜, 앵커) -> 그 항목 제목. 모델이 지어낸 근거 링크를 걸러 내는 대조표다."""
    return {(d["date"], it["anchor"]): it["title"] for d in days for it in d["items"]}


def link_refs(text, index, dropped):
    """[[날짜#앵커|글자]] 를 데일리 회차 링크로. 대조표에 없으면 링크를 벗기고 글자만 남긴다."""
    def sub(m):
        date, anchor, label = m.groups()
        if (date, anchor) in index:
            return f'<a href="../../{date}/#{anchor}">{label}</a>'
        dropped.append(f"{date}#{anchor}")
        return label
    return REF_RE.sub(sub, text)


def timeline(days):
    """요일별 한 줄. 각 회차의 sidebar 문장을 그대로 옮기므로 모델을 거치지 않는다.

    같은 항목이 여러 회차에 반복 등장하는 날이 흔해(collect 의 backfill 정책) 모델에게
    '월요일에 무슨 일' 을 시키면 같은 사건이 며칠에 걸쳐 반복된다. 회차 한 줄은 이미
    그 회차가 무엇으로 채워졌는지를 말하도록 쓰인 문장이라 그대로가 가장 정확하다.
    """
    rows = []
    for d in sorted(days, key=lambda x: x["date"]):
        line = (d.get("sidebar") or d.get("description") or "").strip()
        weekday = d["date_ko"][-2] if d.get("date_ko") else ""
        rows.append(
            f'      <li><a href="../../{d["date"]}/"><span class="wd">{html.escape(weekday)}</span>'
            f'<span class="dt">{d["date"][5:]}</span></a>'
            f'<span class="ln">{html.escape(line)}</span></li>')
    return "\n".join(rows)


def build_prompt(days, rng):
    blocks = []
    for d in days:
        items = "\n".join(
            f"  - [{d['date']}#{it['anchor']}] 추천 상위 {it['percentile']}% · {it['title']}\n"
            f"    {it['lede'][:200]}" for it in d["items"])
        blocks.append(f"## {d['date_ko']} (훑은 {d['scanned']}건 중 {d['picked']}건)\n{items}")
    return f"""너는 til 사이트의 AI 지식 큐레이터 '리브'다. {rng} 의 아침 브리핑을 모아
그 주를 관통하는 이야기 몇 편을 쓴다.

# 이번 주 브리핑
{chr(10).join(blocks)}

# 무엇을 쓰는가
회차 페이지에는 요일별 한 줄 타임라인이 이미 결정적으로 붙는다. 그러니 너는 타임라인을
쓰지 않는다. 네가 쓰는 것은 그 타임라인이 못 하는 일, 즉 며칠에 흩어진 항목을 하나의
판단으로 엮는 이야기다.

- 이야기 {MIN_STORIES}편 이상. 각 편은 소제목 하나와 본문 2-4문단이다.
- 항목 나열이 아니다. '월요일에는 …, 화요일에는 …' 식으로 날짜를 따라가지 마라.
  며칠에 걸쳐 반복되거나 서로 맞물린 주제를 골라 그것으로 한 편을 짠다.
- 억지로 편수를 채우지 마라. 이번 주 재료로 뒷받침되는 것만 쓴다.
- 이번 주 재료로 뒷받침되지 않는 일반론을 쓰지 마라. 근거는 실린 항목이다.

# 근거 링크 (반드시 지킬 것)
주장에는 그 근거가 된 항목을 링크한다. 형식은 정확히 이것 하나다.

  [[날짜#앵커|링크로 보일 글자]]      예: [[2026-08-04#i03|MCP 중복 실행 실측]]

- 날짜와 앵커는 위 '이번 주 브리핑' 의 각 항목 앞 대괄호에 적힌 것을 그대로 쓴다.
  거기 없는 조합을 지어내면 링크가 통째로 벗겨진다.
- 링크 글자는 그 항목이 무엇인지 알 수 있는 말이어야 한다. '여기'·'이 글' 로 쓰지 마라.
- 이야기 한 편에 최소 하나, 주장이 여럿이면 그만큼 건다.
- 이 형식 밖에서 <a> 태그를 직접 쓰지 마라.

# 화자 규칙
- 존댓말, 관리자 호칭은 '관리자님'. 시큰둥하되 무기력하지 않게. 이모지 금지, 느낌표는 전체 1회 이하.
- 도서관 어휘 금지('서고'·'서가'·'장서'·'사서'·'열람'). 쌓이는 곳은 '아카이브', 결과물은 '보고서'·'페이지'.
- em 대시(—)를 쓰지 마라. 공개 페이지라 금지돼 있다. 쉼표를 쓰거나 문장을 끊어라.
- title 은 이번 주를 한 문장으로 잡아채는 제목이다. 날짜를 넣지 않는다.
  description 은 그 아래 한 줄로, 제목이 말하지 않은 것을 보탠다. 둘이 같은 말을 하지 않게 한다.

# 승격 판단
이 글이 til 아카이브에 정식 페이지로 올릴 값이 있는지 판단하라. 기준은
"브리핑을 안 읽은 사람이 읽어도 남는 것이 있는가" 다. 주간 소식 요약에 그치면 승격하지 않는다.

# 출력 (JSON 만, 설명·코드블록 금지)
{{
  "title": "이번 주를 잡아채는 제목(날짜 없이)",
  "description": "제목 아래 한 줄. meta description 도 겸한다",
  "stories": [
    {{"heading": "이야기 소제목",
      "body": ["<p>본문 문단. 근거는 [[2026-08-04#i03|이런 식]]으로 링크한다.</p>"]}}
  ],
  "closing": "마무리 한두 문장",
  "promote": {{"recommend": false, "why": "왜 그렇게 판단했는지 한 줄", "slug": "kebab-case-슬러그-영문"}}
}}"""


def stories_html(data, index):
    """이야기 본문. 근거 링크는 대조표를 통과한 것만 <a> 로 선다.

    stories 가 없으면 구 형식(body 한 덩어리)으로 캐시된 회차다 — 그대로 렌더한다.
    """
    dropped = []
    if not data.get("stories"):
        out = [link_refs(b, index, dropped) for b in data.get("body", [])]
    else:
        out = []
        for s in data["stories"]:
            if s.get("heading"):
                out.append(f'<h2>{html.escape(s["heading"])}</h2>')
            out += [link_refs(b, index, dropped) for b in s.get("body", [])]
    if dropped:
        print(f"  없는 앵커 {len(dropped)}건 — 링크를 벗겼다: {dropped}", file=sys.stderr)
    return "\n".join("  " + b for b in out), len(dropped)


def render_page(repo, data, days, date, rng):
    tpl = (repo / "backlog/assets/briefing/recap.html").read_text(encoding="utf-8")
    avatar = repo / "backlog/assets/liv/avatar-expression-satisfied-72.webp"
    body, _ = stories_html(data, anchor_index(days))
    page = R.fill(tpl, {
        "TITLE": html.escape(data["title"]), "DESCRIPTION": html.escape(data["description"]),
        "DATE": date, "RANGE": rng, "COUNT": str(len(days)),
        "FAVICON_B64": R.favicon(repo), "AVATAR_B64": base64.b64encode(avatar.read_bytes()).decode(),
        "BODY": body,
        "CLOSING": html.escape(data["closing"]), "TIMELINE": timeline(days),
    })
    out = repo / "p/briefing/recap" / date / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    return out


def promote_url(data, date):
    """승격 요청 프리필 — 누르는 것은 관리자다. 자동 게시하지 않는다."""
    body = (f"SOURCE: briefing-recap ({date})\nREQUEST:\n{data['title']} — "
            f"https://til.kil9.dev/p/briefing/recap/{date}/\n"
            "이 주간 리캡을 til 정식 페이지로 옮겨 주세요. 슬러그 제안: "
            f"{data['promote'].get('slug', '')}\n"
            "브리핑을 안 읽은 사람도 읽을 수 있게 배경을 보충하고, 근거 링크를 확인해 주세요.")
    return (INBOX + "?labels=pending&title="
            + urllib.parse.quote(f"[submit] {data['title'][:60]}")
            + "&body=" + urllib.parse.quote(body))


def announce_recap(data, days, date, rng):
    """리캡 링크와 승격 제안을 Slack 으로. 승격 여부를 정하는 것은 관리자다."""
    p = data.get("promote") or {}
    msg = (f"*이번 주 리캡* 올려 두었습니다. {rng} 브리핑 {len(days)}회를 관통해서 봤습니다.\n"
           f"{data['title']}\nhttps://til.kil9.dev/p/briefing/recap/{date}/")
    if p.get("recommend"):
        msg += (f"\n\n이건 til 정식 페이지로 올릴 값이 있어 보입니다. {p.get('why', '')}\n"
                f"승격하시려면: {promote_url(data, date)}")
    else:
        msg += f"\n\n정식 페이지로 올릴 정도는 아니라고 봤습니다. {p.get('why', '')}"
    if os.environ.get("BRIEFING_DRYRUN") == "1":
        print(msg)
        return 0
    return 0 if announce.post(msg) else 1


def main():
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    repo = Path(sys.argv[1]).resolve()
    date = (sys.argv[2] if len(sys.argv) > 2 else
            os.environ.get("BRIEFING_DATE") or datetime.now(KST).date().isoformat())
    days = week(date)
    if len(days) < MIN_BRIEFINGS:
        print(f"이번 주 브리핑 {len(days)}회 — {MIN_BRIEFINGS}회 미만이라 리캡을 만들지 않는다")
        return 0

    rng = f"{days[-1]['date']} ~ {days[0]['date']}"
    cache = STATE / f"recap-{date}.json"
    if cache.exists():        # push 재시도로 다시 들어온 경우 모델을 두 번 부르지 않는다
        data = json.loads(cache.read_text(encoding="utf-8"))
        print("  이미 쓴 리캡을 다시 렌더한다")
    else:
        data = llm.ask_json(build_prompt(days, rng))
        cache.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    if "--announce" in sys.argv:      # 발행이 끝난 뒤에 부른다. 링크가 살아 있어야 한다
        return announce_recap(data, days, date, rng)

    n = len(data.get("stories") or [])
    if n < MIN_STORIES:
        # 발행은 막지 않는다. 리캡이 안 나가는 것보다 짧게라도 나가는 편이 낫다.
        print(f"  경고: 이야기가 {n}편이다 ({MIN_STORIES}편 이상이어야 한다)", file=sys.stderr)
    out = render_page(repo, data, days, date, rng)
    print(f"  {out.relative_to(repo)} ({len(out.read_text(encoding='utf-8').encode()) // 1024}KB)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
