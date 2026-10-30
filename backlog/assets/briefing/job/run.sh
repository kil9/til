#!/usr/bin/env bash
# liv-briefing — 리브의 아침 브리핑을 만들어 til 에 발행한다 (task-80 재료, task-85 발행).
#   수집(collect.py) → 1차 선별(select.py) → 상세 + 2차 정리(compose.py)
#   → 렌더(render.py) → 전용 클론에서 commit·push → Slack 알림
#
# 조용히 죽지 않는 것이 이 잡의 1번 요구사항이다. docs-ai-summary 가 로케일 정렬과
# pipefail 로 두 번 무동작·무로그로 죽은 전례가 있어, 단계마다 종료코드를 보고
# 무슨 일이 있었는지 한 줄씩 남기고, 실패는 Slack #til 로도 알린다.
set -euo pipefail
export PATH="$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin"
# claude 자격증명은 대화형 세션과 같은 것을 쓴다. cron 은 CLAUDE_CONFIG_DIR 를
# 물려받지 못해 기본 ~/.claude 를 보는데, 그쪽 OAuth 가 조용히 만료돼 2026-08-26
# 발행이 통째로 죽었다(claude 가 만료 메시지를 stdout 으로 뱉어 stderr 로그도 비었다).
export CLAUDE_CONFIG_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.ccs/instances/personal}"

BASE="$HOME/jobs/liv-briefing"
STATE="$BASE/state"
REPO="$BASE/repo"                 # 전용 클론. 사람이 쓰는 워킹트리를 절대 건드리지 않는다
REPO_URL="https://github.com/kil9/til.git"
MIN_NEW="${MIN_NEW:-5}"           # 신규가 이보다 적으면 collect.py 가 목록 전체로 backfill 한다
export MIN_NEW
PUBLISH="${BRIEFING_PUBLISH:-1}"  # 0 이면 재료만 만들고 멈춘다(수동 점검용)
TODAY="${BRIEFING_DATE:-$(date '+%F')}"
export BRIEFING_DATE="$TODAY"
export TIL_REPO="$REPO"           # 관심사 프로필·til 목록도 전용 클론에서 읽는다
ts() { date '+%F %T'; }

# Slack #til — 화자는 리브여야 하므로 liv 프로필 토큰을 먼저 쓴다(til-submit 과 같은 배관).
SLACK_CHANNEL="${BRIEFING_SLACK_CHANNEL:-C0BJUAH0Y7J}"
notify() {
  local msg="$1" tok
  tok=$(grep '^SLACK_BOT_TOKEN=' "$HOME/.hermes/profiles/liv/.env" 2>/dev/null | cut -d= -f2-) || true
  [ -z "$tok" ] && tok=$(grep '^SLACK_BOT_TOKEN=' "$HOME/.hermes/.env" 2>/dev/null | cut -d= -f2-) || true
  [ -z "$tok" ] && return 0
  curl -s -m 10 -X POST "https://slack.com/api/chat.postMessage" \
    -H "Authorization: Bearer $tok" -H "Content-Type: application/json; charset=utf-8" \
    --data "$(python3 -c 'import json,sys; print(json.dumps({"channel": sys.argv[1], "text": sys.argv[2]}))' "$SLACK_CHANNEL" "$msg")" \
    >/dev/null 2>&1 || true
}
fail() {  # ERR 트랩. 어느 줄에서 죽었는지 로그와 Slack 양쪽에 남긴다
  local line="$1"
  echo "$(ts) 실패 — run.sh:$line (직전 명령 rc=$2)"
  notify "브리핑 발행에 실패했습니다. $TODAY · run.sh:$line 에서 멈췄고 cron.log 에 남겨 두었습니다."
}
trap 'fail "$LINENO" "$?"' ERR

mkdir -p "$STATE"
exec 9>"$BASE/.lock"
flock -n 9 || { echo "$(ts) 이미 실행 중 — 종료"; exit 0; }

if [ -f "$STATE/published-$TODAY" ]; then
  echo "$(ts) $TODAY 은 이미 발행됨 — LLM 호출 없이 종료"
  exit 0
fi

# ── 재료 ────────────────────────────────────────────────────────────────
if [ -f "$STATE/briefing-$TODAY.json" ]; then
  echo "$(ts) $TODAY 재료가 이미 있다 — 발행 단계로 건너뛴다"
else
  echo "$(ts) 수집 시작"
  python3 "$BASE/collect.py"

  new_count="$(python3 -c "
import json, sys
print(len(json.load(open(sys.argv[1]))['items']))" "$STATE/collected-$TODAY.json")"
  # 후보가 아예 0건일 때만 멈춘다(목록 파싱이 깨졌다는 뜻). 신규가 얇은 날은
  # collect.py 가 목록 전체로 backfill 하므로 여기서 걸러 발행을 거르지 않는다.
  if [ "$new_count" -eq 0 ]; then
    echo "$(ts) 후보 0건 — LLM 호출 없이 종료"
    exit 0
  fi

  echo "$(ts) 선별 피드백 수거"
  python3 "$BASE/feedback.py" || echo "$(ts) 피드백 수거 실패 — 기존 규칙으로 진행"

  echo "$(ts) 1차 선별"
  python3 "$BASE/select.py"

  echo "$(ts) 상세 수집 + 2차 정리"
  python3 "$BASE/compose.py"
fi

if [ "$PUBLISH" != "1" ]; then
  echo "$(ts) BRIEFING_PUBLISH=0 — 재료까지만 만들고 종료"
  exit 0
fi

# ── 발행 ────────────────────────────────────────────────────────────────
if [ ! -d "$REPO/.git" ]; then
  echo "$(ts) 전용 클론 생성"
  git clone --quiet "$REPO_URL" "$REPO"
  git -C "$REPO" config user.name kil9
  git -C "$REPO" config user.email "61569+kil9@users.noreply.github.com"
fi

# push 는 밀릴 수 있다. docs-ai-summary(09:00)도 같은 저장소에 push 하므로
# non-fast-forward 를 만나면 최신을 받아 다시 렌더·커밋해서 올린다.
pushed=0
for attempt in 1 2 3; do
  git -C "$REPO" fetch --quiet origin
  git -C "$REPO" reset --quiet --hard origin/main
  git -C "$REPO" clean -qfd p/briefing 2>/dev/null || true

  echo "$(ts) 렌더 (시도 $attempt)"
  python3 "$BASE/render.py" "$REPO" "$TODAY"

  # p/briefing 통째로 add 한다 — 새 회차가 나오면 직전 회차 페이지의 이동 내비도
  # 함께 바뀌므로(task-92) 파일을 하나씩 나열하면 그 변경이 빠진다.
  # 이 클론은 매 시도마다 origin/main 으로 reset --hard 하므로 남의 변경이 섞이지 않는다.
  git -C "$REPO" add "p/briefing" "p/liv-briefing/index.html"
  if git -C "$REPO" diff --cached --quiet; then
    echo "$(ts) 바뀐 것이 없다 — 커밋 생략"
    pushed=1
    break
  fi
  git -C "$REPO" commit --quiet -m "[auto] 리브 아침 브리핑 $TODAY"
  if git -C "$REPO" push --quiet origin main 2>/dev/null; then
    pushed=1
    break
  fi
  echo "$(ts) push 밀림 — 최신을 받아 다시 시도 ($attempt/3)"
  sleep 5
done

if [ "$pushed" != "1" ]; then
  echo "$(ts) push 3회 실패 — 중단"
  notify "브리핑 push 가 3번 밀려 발행하지 못했습니다. $TODAY · nuc14 cron.log 를 봐 주세요."
  exit 1
fi

touch "$STATE/published-$TODAY"
python3 "$BASE/seen.py" "$TODAY"    # 발행에 성공한 뒤에만 처리 완료로 찍는다

echo "$(ts) 발행 완료 — https://til.kil9.dev/p/briefing/ ($(git -C "$REPO" rev-parse --short HEAD))"
# 발행 알림(task-86). 하루 한 번만 — 같은 날 다시 발행해도 알림을 두 번 보내지 않는다.
if [ -f "$BASE/announce.py" ] && [ ! -f "$STATE/announced-$TODAY" ]; then
  if python3 "$BASE/announce.py" "$TODAY"; then
    touch "$STATE/announced-$TODAY"
  else
    echo "$(ts) Slack 알림 실패 — 발행 자체는 성공"
  fi
fi
