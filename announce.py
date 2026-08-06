#!/usr/bin/env python3
"""발행 알림 — 브리핑이 올라갔다고 Slack #til 로 리브가 알린다 (task-86).

전문을 싣지 않는다. 강추 1건(제목 + 왜 권하는지 한 줄) + 나머지 헤드라인 압축 +
페이지 링크까지다. 알림에서 다 읽히면 페이지를 안 연다.

사용법: python3 announce.py [YYYY-MM-DD] [--dry-run]
"""

import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
STATE = BASE / "state"
KST = timezone(timedelta(hours=9))
CHANNEL = os.environ.get("BRIEFING_SLACK_CHANNEL", "C0BJUAH0Y7J")   # #til
PAGE = "https://til.kil9.dev/p/briefing/"


def token():
    """til-submit 과 같은 순서: 리브 프로필 토큰 먼저, 기본 프로필은 폴백."""
    for p in (Path.home() / ".hermes/profiles/liv/.env", Path.home() / ".hermes/.env"):
        if not p.exists():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.startswith("SLACK_BOT_TOKEN="):
                return line.split("=", 1)[1].strip()
    return ""


def short(title, limit=26):
    """헤드라인 압축 — 부제(' - ', ' — ')를 떼고 길면 자른다. 폰에서 읽는 알림이다."""
    for sep in (" - ", " — ", " – ", ": "):
        if sep in title:
            title = title.split(sep, 1)[0]
            break
    return title if len(title) <= limit else title[:limit - 1].rstrip() + "…"


def compose(data):
    items = data["items"]
    pick = data.get("pick") or {}
    top = next((it for it in items if it["anchor"] == pick.get("anchor")), items[0] if items else None)

    lines = [f"*{data['date_ko']} 아침 브리핑* 올려 두었습니다. GeekNews {data['scanned']}건에서 {data['picked']}건입니다."]
    if top:
        why = pick.get("line", "").split("—", 1)[-1].strip() or top.get("liv") or top["lede"]
        lines += ["", f"오늘 하나만 고르신다면 *{top['rank']} {top['title']}*", f"{why}"]
    # 번호를 붙여 두는 이유는 스레드에서 '3번 파봐' 로 항목을 특정할 수 있게 하기 위함이다(task-89).
    rest = [f"{it['rank']} {short(it['title'], 34)}" for it in items if not top or it["anchor"] != top["anchor"]]
    if rest:
        lines += ["", "나머지는 " + " · ".join(rest) + " 입니다."]
    lines += ["", PAGE, "이 스레드에 \"3번 파봐\" 처럼 답글을 달면 그 건으로 til 을 만들겠습니다."]
    return "\n".join(lines)


def post(text, channel=CHANNEL, thread_ts=None):
    tok = token()
    if not tok:
        print("Slack 토큰을 못 찾았다 — 알림 생략", file=sys.stderr)
        return None
    payload = {"channel": channel, "text": text}
    if thread_ts:
        payload["thread_ts"] = thread_ts
    req = urllib.request.Request(
        "https://slack.com/api/chat.postMessage",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json; charset=utf-8"},
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        res = json.loads(r.read().decode())
    if not res.get("ok"):
        print(f"Slack 실패: {res.get('error')}", file=sys.stderr)
        return None
    return res.get("ts")


def save_thread(data, ts):
    """스레드 답글로 항목을 특정할 수 있게 발행 메시지 ↔ 항목 매핑을 남긴다 (task-89)."""
    d = STATE / "threads"
    d.mkdir(exist_ok=True)
    (d / f"{data['date']}.json").write_text(json.dumps({
        "date": data["date"], "channel": CHANNEL, "ts": ts,
        "items": [{"n": int(it["rank"]), "title": it["title"], "url": it["source_url"],
                   "angle": it["angle"], "action_topic": it["action_topic"]} for it in data["items"]],
        "replied": [],
    }, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    date = (args[0] if args else os.environ.get("BRIEFING_DATE") or datetime.now(KST).date().isoformat())
    src = STATE / f"briefing-{date}.json"
    if not src.exists():
        print(f"브리핑 재료가 없다: {src}", file=sys.stderr)
        return 2
    data = json.loads(src.read_text(encoding="utf-8"))
    text = compose(data)
    if dry:
        print(text)
        return 0
    ts = post(text)
    if not ts:
        return 1
    save_thread(data, ts)
    return 0


if __name__ == "__main__":
    sys.exit(main())
