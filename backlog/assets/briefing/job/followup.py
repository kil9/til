#!/usr/bin/env python3
"""팔로업 — 지난 브리핑 이후 접수된 til 요청의 처리 상태 (task-88).

브리핑을 1회성에서 연속물로 만드는 조각이다. til-inbox 이슈를 지난 브리핑 시각
이후로 훑어 상태(접수·처리 중·완성·실패)와 완성된 페이지 링크를 모은다.

보여 줄 것이 없으면 빈 목록을 돌려준다 — 렌더는 그때 패널 자체를 그리지 않는다.
매일 '없음' 이 찍히면 그 자리가 죽는다.

사용법: python3 followup.py [YYYY-MM-DD]   (그 날짜 브리핑 기준으로 조회)
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

STATE = Path(__file__).resolve().parent / "state"
KST = timezone(timedelta(hours=9))
INBOX = os.environ.get("LIV_INBOX_REPO", "kil9/til-inbox")
LABEL_STATE = {"done": "완성", "processing": "작업 중", "failed": "실패", "pending": "접수됨"}
PUB_RE = re.compile(r"게시 완료:\s*(\S+)")


def previous_date(today):
    """직전 브리핑 날짜. 없으면 None."""
    dates = sorted(p.stem.replace("briefing-", "") for p in STATE.glob("briefing-*.json"))
    prev = [d for d in dates if d < today]
    return prev[-1] if prev else None


def previous_items(today):
    """직전 브리핑에 실었던 항목들(제목·URL). 오늘 재료의 후속 판정에 쓴다."""
    prev = previous_date(today)
    if not prev:
        return []
    data = json.loads((STATE / f"briefing-{prev}.json").read_text(encoding="utf-8"))
    return [{"title": it["title"], "url": it["source_url"]} for it in data.get("items", [])]


def gather(today):
    """직전 브리핑 이후 움직인 til 요청들. gh 가 없거나 실패하면 빈 목록."""
    prev = previous_date(today)
    since = f"{prev}T00:00:00+09:00" if prev else (
        datetime.now(KST) - timedelta(days=1)).isoformat(timespec="seconds")
    try:
        p = subprocess.run(
            ["gh", "issue", "list", "-R", INBOX, "--state", "all", "--limit", "30",
             "--json", "number,title,labels,updatedAt,url,body,comments"],
            capture_output=True, text=True, timeout=60)
        if p.returncode != 0:
            print(f"  til-inbox 조회 실패 — 팔로업 없이 진행: {p.stderr.strip()[:200]}", file=sys.stderr)
            return []
        issues = json.loads(p.stdout)
    except Exception as e:
        print(f"  til-inbox 조회 실패 — 팔로업 없이 진행: {e}", file=sys.stderr)
        return []

    rows = []
    for it in issues:
        if it["updatedAt"] < since:
            continue
        labels = {l["name"] for l in it.get("labels", [])}
        state = next((LABEL_STATE[k] for k in ("done", "failed", "processing", "pending") if k in labels), None)
        if not state:
            continue
        page = ""
        for c in reversed(it.get("comments", []) or []):
            m = PUB_RE.search(c.get("body", ""))
            if m:
                page = m.group(1)
                break
        title = re.sub(r"^\[(submit|research)\]\s*", "", it["title"])
        rows.append({"number": it["number"], "title": title, "state": state,
                     "page": page, "issue": it["url"],
                     "from_briefing": "SOURCE: briefing" in (it.get("body") or "")})
    rows.sort(key=lambda r: (r["state"] != "완성", r["number"]))
    return rows[:6]


if __name__ == "__main__":
    day = sys.argv[1] if len(sys.argv) > 1 else datetime.now(KST).date().isoformat()
    print(json.dumps({"previous": previous_date(day), "rows": gather(day)}, ensure_ascii=False, indent=2))
