#!/usr/bin/env bash
# liv-briefing 주간 리캡 (task-91) — 일요일에 그 주 브리핑을 관통하는 산문 한 편을 발행한다.
# 브리핑 발행(run.sh)과 같은 전용 클론·push 재시도 배관을 쓴다. 갤러리에는 올리지 않는다.
set -euo pipefail
export PATH="$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin"

BASE="$HOME/jobs/liv-briefing"
# 데일리(run.sh)와 클론을 나눠 쓴다. 예전에는 $BASE/repo 를 공유했는데 둘 다 reset --hard 를
# 치므로, 일요일 09:00 데일리가 push 재시도로 늘어져 09:20 을 넘기면 리캡의 reset 이 진행 중인
# 작업을 밟는다. 락은 서로 다른 파일이라 막아 주지 못했다. 공용 락으로 묶으면 이번엔 한쪽이
# 다른 쪽의 발행을 건너뛰게 만든다(task-117 AC#5 가 금지하는 것). 클론을 나누면 공유 상태
# 자체가 없어져 어느 쪽이 죽든 다른 쪽과 무관해진다. 값은 디스크 76MB 다.
REPO="$BASE/repo-recap"
REPO_URL="https://github.com/kil9/til.git"
TODAY="${BRIEFING_DATE:-$(date '+%F')}"
export BRIEFING_DATE="$TODAY"
export TIL_REPO="$REPO"
ts() { date '+%F %T'; }

exec 9>"$BASE/.lock-recap"
flock -n 9 || { echo "$(ts) 이미 실행 중 — 종료"; exit 0; }

if [ -f "$BASE/state/recap-published-$TODAY" ]; then
  echo "$(ts) $TODAY 리캡은 이미 발행됨 — 종료"
  exit 0
fi

if [ ! -d "$REPO/.git" ]; then
  git clone --quiet "$REPO_URL" "$REPO"
  git -C "$REPO" config user.name kil9
  git -C "$REPO" config user.email "61569+kil9@users.noreply.github.com"
fi

pushed=0
for attempt in 1 2 3; do
  git -C "$REPO" fetch --quiet origin
  git -C "$REPO" reset --quiet --hard origin/main

  echo "$(ts) 리캡 생성 (시도 $attempt)"
  BRIEFING_DRYRUN=1 python3 "$BASE/recap.py" "$REPO" "$TODAY"
  [ -d "$REPO/p/briefing/recap/$TODAY" ] || { echo "$(ts) 이번 주는 리캡 없음"; exit 0; }

  git -C "$REPO" add "p/briefing/recap/$TODAY/index.html"
  if git -C "$REPO" diff --cached --quiet; then
    pushed=1; break
  fi
  git -C "$REPO" commit --quiet -m "[auto] 리브 주간 리캡 $TODAY"
  if git -C "$REPO" push --quiet origin main 2>/dev/null; then
    pushed=1; break
  fi
  echo "$(ts) push 밀림 — 다시 시도 ($attempt/3)"
  sleep 5
done

[ "$pushed" = "1" ] || { echo "$(ts) push 3회 실패"; exit 1; }
touch "$BASE/state/recap-published-$TODAY"
echo "$(ts) 리캡 발행 완료 — https://til.kil9.dev/p/briefing/recap/$TODAY/"
python3 "$BASE/recap.py" "$REPO" "$TODAY" --announce || echo "$(ts) Slack 알림 실패 — 발행 자체는 성공"
