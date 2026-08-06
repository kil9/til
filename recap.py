#!/usr/bin/env python3
"""주간 리캡 — 그 주 브리핑을 관통하는 흐름 한 편 (task-91).

일간 브리핑은 그날 안에서만 본다. 며칠에 걸쳐 이어지는 추세는 일간으로는 안 보인다.
형식도 다르다 — 항목 나열이 아니라 산문 한 편이다.

잘 나오면 til 정식 페이지로 승격할 만하다. 다만 자동으로 갤러리에 올리지는 않는다.
모델이 승격 여부를 판단해 근거와 함께 Slack 으로 제안하고, 결정은 관리자가 한다.

사용법: python3 recap.py <til-repo> [YYYY-MM-DD]   (일요일 cron)
"""

import base64
import html
import json
import os
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
INBOX = "https://github.com/kil9/til-inbox/issues/new"


def week(today):
    """최근 DAYS 일치 브리핑 재료(최신순)."""
    start = (datetime.fromisoformat(today) - timedelta(days=DAYS - 1)).date().isoformat()
    out = []
    for p in sorted(STATE.glob("briefing-*.json"), reverse=True):
        date = p.stem.replace("briefing-", "")
        if start <= date <= today:
            out.append(json.loads(p.read_text(encoding="utf-8")))
    return out


def build_prompt(days, rng):
    blocks = []
    for d in days:
        items = "\n".join(
            f"  - [{it['percentile']}%] {it['title']} — {it['lede'][:200]}" for it in d["items"])
        blocks.append(f"## {d['date_ko']} (훑은 {d['scanned']}건 중 {d['picked']}건)\n{items}")
    return f"""너는 til 사이트의 AI 지식 큐레이터 '리브'다. {rng} 의 아침 브리핑을 모아
그 주를 관통하는 흐름 한 편을 쓴다.

# 이번 주 브리핑
{chr(10).join(blocks)}

# 쓰기 규칙
- 항목 나열이 아니라 산문이다. '월요일에는 …, 화요일에는 …' 식으로 날짜를 따라가지 마라.
  며칠에 걸쳐 반복되거나 서로 맞물린 주제를 골라 그것으로 글을 짠다.
- 흐름이 둘 이상이면 소제목으로 나눠도 된다. 억지로 하나로 묶지 마라.
- 이번 주 재료로 뒷받침되지 않는 일반론을 쓰지 마라. 근거는 실린 항목이다.
- 존댓말, 관리자 호칭은 '관리자님'. 시큰둥하되 무기력하지 않게. 이모지 금지, 느낌표는 전체 1회 이하.
- 본문 3-6문단. closing 은 마무리 한두 문장(리브 코멘트 자리).

# 승격 판단
이 글이 til 아카이브에 정식 페이지로 올릴 값이 있는지 판단하라. 기준은
"브리핑을 안 읽은 사람이 읽어도 남는 것이 있는가" 다. 주간 소식 요약에 그치면 승격하지 않는다.

# 출력 (JSON 만, 설명·코드블록 금지)
{{
  "title": "글 제목(날짜 없이)",
  "description": "meta description 한 줄",
  "body": ["<p>문단</p>", "<h2>소제목</h2>", "<p>문단</p>"],
  "closing": "마무리 한두 문장",
  "promote": {{"recommend": false, "why": "왜 그렇게 판단했는지 한 줄", "slug": "kebab-case-슬러그-영문"}}
}}"""


def render_page(repo, data, days, date, rng):
    tpl = (repo / "backlog/assets/briefing/recap.html").read_text(encoding="utf-8")
    avatar = repo / "backlog/assets/liv/avatar-expression-satisfied-72.webp"
    sources = "\n".join(
        f'      <li><a href="../../{d["date"]}/">{d["date_ko"]}</a> — {html.escape(d["description"][:90])}</li>'
        for d in days)
    page = R.fill(tpl, {
        "TITLE": html.escape(data["title"]), "DESCRIPTION": html.escape(data["description"]),
        "DATE": date, "RANGE": rng, "COUNT": str(len(days)),
        "FAVICON_B64": R.favicon(repo), "AVATAR_B64": base64.b64encode(avatar.read_bytes()).decode(),
        "BODY": "\n".join("  " + b for b in data["body"]),
        "CLOSING": html.escape(data["closing"]), "SOURCES": sources,
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
    out = render_page(repo, data, days, date, rng)
    print(f"  {out.relative_to(repo)} ({len(out.read_text(encoding='utf-8').encode()) // 1024}KB)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
