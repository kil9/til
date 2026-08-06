#!/usr/bin/env python3
"""그날 훑은 항목을 처리 완료로 표시한다 (task-80).

collect.py 가 이 목록으로 신규 여부를 가르므로, 브리핑이 실제로 완성된 뒤에만
찍어야 한다. 중간에 실패한 날의 항목은 다음 날 다시 후보가 된다.

사용법: python3 seen.py [YYYY-MM-DD]
"""

import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

STATE = Path(__file__).resolve().parent / "state"
KST = timezone(timedelta(hours=9))
KEEP = 3000        # 오래된 id 는 버린다. GeekNews 하루 20-40건이면 두세 달치다


def main():
    today = (sys.argv[1] if len(sys.argv) > 1 else
             os.environ.get("BRIEFING_DATE") or datetime.now(KST).date().isoformat())
    src = STATE / f"collected-{today}.json"
    if not src.exists():
        print(f"수집 파일이 없다: {src}", file=sys.stderr)
        return 2
    ids = [it["id"] for it in json.loads(src.read_text(encoding="utf-8"))["items"]]
    path = STATE / "seen.json"
    prev = json.loads(path.read_text(encoding="utf-8"))["ids"] if path.exists() else []
    merged = list(dict.fromkeys(prev + ids))[-KEEP:]
    path.write_text(json.dumps({"ids": merged}, ensure_ascii=False), encoding="utf-8")
    print(f"  처리 완료 표시 {len(ids)}건 (누적 {len(merged)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
