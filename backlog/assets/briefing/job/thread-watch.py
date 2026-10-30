#!/usr/bin/env python3
"""브리핑 Slack 스레드의 답글을 til 접수로 넘긴다 (task-89).

폰으로 브리핑 알림을 읽다가 "3번 파봐" 라고 답글을 달면 그것이 til-inbox 이슈가 된다.
요청 본문 규약은 페이지 버튼(task-82)과 같다 — 워처의 기본 경로(submit)로 간다.

항목 특정:
  숫자 1개  → 그 항목
  제목 일부 → 그 항목
  없거나 여럿 → 스레드에서 되묻고 이번 답글은 넘긴다

관리자(OWNER)의 답글만 본다. 리브 자신의 답글은 무시한다.

사용법: python3 thread-watch.py   (cron 5분 간격)
"""

import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

import announce

BASE = Path(__file__).resolve().parent
THREADS = BASE / "state" / "threads"
KST = timezone(timedelta(hours=9))
OWNER = os.environ.get("LIV_OWNER_IDS", "U0B54E64FNW").split(",")[0]
INBOX = os.environ.get("LIV_INBOX_REPO", "kil9/til-inbox")
WATCH_DAYS = 3           # 이보다 오래된 스레드는 더 보지 않는다
ASK = "몇 번 건인지 알려 주시면 접수하겠습니다. 번호나 제목 일부면 됩니다."


def slack(method, params):
    tok = announce.token()
    if not tok:
        raise RuntimeError("Slack 토큰을 못 찾았다")
    url = f"https://slack.com/api/{method}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {tok}"})
    with urllib.request.urlopen(req, timeout=20) as r:
        res = json.loads(r.read().decode())
    if not res.get("ok"):
        raise RuntimeError(f"{method} 실패: {res.get('error')}")
    return res


def pick_item(text, items):
    """답글에서 항목을 특정한다. 못 하면 None."""
    nums = {int(n) for n in re.findall(r"\b0?(\d{1,2})\s*번", text)}
    if not nums:
        nums = {int(n) for n in re.findall(r"\b0?(\d{1,2})\b", text)}
    nums = {n for n in nums if any(it["n"] == n for it in items)}
    if len(nums) == 1:
        want = nums.pop()               # 제너레이터 안에서 pop 하면 매 비교마다 빠져나가 비어 버린다
        return next(it for it in items if it["n"] == want)
    if nums:
        return None                     # 여러 개를 가리키면 되묻는다
    hits = [it for it in items if any(w and w in it["title"] for w in re.findall(r"[\w가-힣]{3,}", text))]
    return hits[0] if len(hits) == 1 else None


def create_issue(item, note, date):
    body = (f"SOURCE: briefing-slack ({date})\nREQUEST:\n"
            f"{item['action_topic']} — {item['url']}\n"
            "원문을 직접 읽고 til 페이지로 만들어 주세요.\n"
            f"조사 방향: {item['angle']}")
    if note:
        body += f"\n관리자 지시: {note}"
    if os.environ.get("BRIEFING_DRYRUN") == "1":
        print(f"  [dry-run] 이슈 생성 생략\n{body}")
        return "dry-run://issue"
    p = subprocess.run(["gh", "issue", "create", "-R", INBOX, "--label", "pending",
                        "--title", f"[submit] {item['action_topic'][:60]}", "--body", body],
                       capture_output=True, text=True, timeout=60)
    if p.returncode != 0:
        raise RuntimeError(f"gh issue create rc={p.returncode}: {p.stderr[-300:]}")
    return p.stdout.strip()


def handle(path):
    st = json.loads(path.read_text(encoding="utf-8"))
    replies = slack("conversations.replies", {"channel": st["channel"], "ts": st["ts"], "limit": 50})
    done = set(st.get("replied", []))
    changed = False
    for msg in replies.get("messages", []):
        ts = msg.get("ts")
        if ts == st["ts"] or ts in done or msg.get("bot_id") or msg.get("user") != OWNER:
            continue
        text = re.sub(r"<@[A-Z0-9]+>", "", msg.get("text", "")).strip()
        item = pick_item(text, st["items"])
        if not item:
            announce.post(ASK, st["channel"], thread_ts=st["ts"])
            done.add(ts)                # 되물은 답글은 다시 묻지 않는다. 다음 답글에서 확정된다
            changed = True
            print(f"  {path.stem} {ts}: 항목 특정 실패 — 되물음")
            continue
        url = create_issue(item, text, st["date"])
        announce.post(f"{item['n']:02d}번 「{item['title']}」 으로 접수했습니다. 완성되면 이 채널에 올리겠습니다.",
                      st["channel"], thread_ts=st["ts"])
        done.add(ts)
        changed = True
        print(f"  {path.stem} {ts}: {item['n']:02d}번 접수 → {url}")
    if changed:
        st["replied"] = sorted(done)
        path.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    if not THREADS.exists():
        return 0
    cutoff = (datetime.now(KST) - timedelta(days=WATCH_DAYS)).date().isoformat()
    for path in sorted(THREADS.glob("*.json")):
        if path.stem < cutoff:
            continue
        try:
            handle(path)
        except Exception as e:                    # 한 스레드가 죽어도 나머지는 본다
            print(f"  {path.stem}: {e}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
