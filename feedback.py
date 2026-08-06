#!/usr/bin/env python3
"""선별 피드백 수거 → 규칙화 (task-90).

브리핑의 '이건 왜' 링크가 til-inbox 에 feedback 라벨 이슈를 만든다(워처는 이 라벨을
건드리지 않는다). 이 스크립트가 열린 피드백을 모아 축약된 선별 규칙으로 정리하고
state/rules.json 에 남긴 뒤 이슈를 닫는다. select.py 가 그 규칙을 프롬프트에 넣는다.

원문을 그대로 쌓으면 프롬프트가 계속 길어지므로 규칙 형태로 줄이고, 개수 상한과
만료를 둔다. 오래된 취향이 새 취향을 계속 눌러서도 안 된다.

사용법: python3 feedback.py    (run.sh 가 선별 직전에 부른다)
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import llm

STATE = Path(__file__).resolve().parent / "state"
RULES = STATE / "rules.json"
KST = timezone(timedelta(hours=9))
INBOX = os.environ.get("LIV_INBOX_REPO", "kil9/til-inbox")
MAX_RULES = 12           # 프롬프트가 무한정 길어지지 않게
EXPIRE_DAYS = 60         # 이보다 오래되고 다시 확인되지 않은 규칙은 버린다


def load_rules():
    if not RULES.exists():
        return []
    try:
        return json.loads(RULES.read_text(encoding="utf-8"))["rules"]
    except (json.JSONDecodeError, KeyError):
        return []


def active_rules(today=None):
    """만료되지 않은 규칙 텍스트. select.py 가 쓴다."""
    today = today or datetime.now(KST).date().isoformat()
    cutoff = (datetime.fromisoformat(today) - timedelta(days=EXPIRE_DAYS)).date().isoformat()
    return [r["rule"] for r in load_rules() if r.get("updated", "") >= cutoff][:MAX_RULES]


def open_feedback():
    p = subprocess.run(["gh", "issue", "list", "-R", INBOX, "--state", "open", "--label", "feedback",
                        "--limit", "30", "--json", "number,title,body"],
                       capture_output=True, text=True, timeout=60)
    if p.returncode != 0:
        print(f"  피드백 조회 실패 — 규칙 갱신 없이 진행: {p.stderr.strip()[:200]}", file=sys.stderr)
        return []
    return json.loads(p.stdout)


def build_prompt(rules, issues):
    cur = "\n".join(f"- {r['rule']} (기록 {r['updated']})" for r in rules) or "- (없음)"
    new = "\n".join(f"- #{i['number']} {i['title']}\n  {(i.get('body') or '')[:500]}" for i in issues)
    return f"""너는 til 사이트의 아침 브리핑 선별 규칙을 관리한다. 관리자가 남긴 피드백을
다음 브리핑 선별에 바로 쓸 수 있는 짧은 규칙으로 정리하라.

# 지금 규칙
{cur}

# 새로 들어온 피드백
{new}

# 규칙
- 규칙 하나는 한 문장이고 판단 가능해야 한다. 예: "프론트엔드 빌드 도구 소개는 뺀다",
  "Show GN 자작 도구는 가중치를 올린다".
- 같은 취지의 기존 규칙이 있으면 새로 만들지 말고 그 규칙을 다듬어 합친다.
- 서로 모순되면 새 피드백 쪽을 남긴다.
- 전체 {MAX_RULES}개를 넘기지 마라. 넘치면 가장 좁고 덜 쓰일 규칙부터 버린다.
- 피드백이 특정 항목에 대한 감상일 뿐 일반화할 수 없으면 규칙으로 만들지 않는다.

# 출력 (JSON 만, 설명·코드블록 금지)
{{"rules": ["규칙 문장", "…"]}}"""


def main():
    today = os.environ.get("BRIEFING_DATE") or datetime.now(KST).date().isoformat()
    issues = open_feedback()
    if not issues:
        print("  새 피드백 없음 — 규칙 그대로")
        return 0
    print(f"  피드백 {len(issues)}건 수거")

    rules = load_rules()
    merged = llm.ask_json(build_prompt(rules, issues)).get("rules", [])[:MAX_RULES]
    # 문장이 그대로면 처음 기록한 날짜를 유지한다 — 그래야 손대지 않은 규칙이 만료된다.
    # 다듬어졌거나 새로 생긴 규칙은 오늘로 갱신된다.
    was = {r["rule"]: r.get("updated", today) for r in rules}
    out = [{"rule": r, "updated": was.get(r, today)} for r in merged]
    RULES.write_text(json.dumps({"rules": out, "updated": today}, ensure_ascii=False, indent=2),
                     encoding="utf-8")
    print(f"  규칙 {len(rules)}개 → {len(out)}개")

    for i in issues:
        subprocess.run(["gh", "issue", "comment", str(i["number"]), "-R", INBOX,
                        "-b", "선별 규칙에 반영했습니다. 다음 브리핑부터 적용됩니다."],
                       capture_output=True, text=True, timeout=60)
        subprocess.run(["gh", "issue", "close", str(i["number"]), "-R", INBOX],
                       capture_output=True, text=True, timeout=60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
