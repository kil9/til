---
id: TASK-47
title: liv Slack 앱 스코프·이벤트 확장
status: Done
assignee: []
created_date: '2026-07-18 05:54'
updated_date: '2026-07-18 07:38'
labels: []
milestone: m-4
dependencies: []
priority: medium
ordinal: 47000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
hermes 스레드 무멘션 대화는 channels:history + message.channels 스코프/이벤트가 전제. 현재 liv 앱은 app_mentions:read·chat:write·im:* 뿐이라 확장·재설치 필요(api.slack.com, Chrome 필요분·사용자 조치).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 liv Slack 앱에 channels:history·channels:read + message.channels(및 groups 등 hermes 매니페스트 요구분) 스코프/이벤트 추가
- [x] #2 앱 재설치로 새 토큰 반영, x-oauth-scopes 로 확인
- [x] #3 채널 스레드 무멘션 메시지가 게이트웨이에 수신됨 확인
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
완료 (2026-07-18, Chrome 자동화). 매니페스트로 스코프·이벤트 추가 + 재설치.
- 스코프 추가: channels:history, channels:read, groups:history, groups:read, mpim:history, mpim:read, users:read (기존 app_mentions:read·chat:write·im:* 위에). 총 12종.
- 이벤트 추가: message.channels, message.groups, message.mpim, assistant_thread_started, assistant_thread_context_changed (기존 app_mention·message.im 위에). 총 7종.
- 재설치(허용) 후 x-oauth-scopes 로 12 스코프 전부 확인, conversations.list(channels:read) ok(이전 missing_scope 해소).
- **중요: 같은 워크스페이스 스코프추가 재설치는 봇 토큰을 로테이트하지 않음** — .env 토큰 프리픽스 동일, auth.test ok(user=liv). 구동 중 liv-bot 불간섭, .env 갱신 불필요. → TASK-49 커토버의 토큰 긴급 커플링 해소.
<!-- SECTION:NOTES:END -->
