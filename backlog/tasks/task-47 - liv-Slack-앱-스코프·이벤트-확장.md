---
id: TASK-47
title: liv Slack 앱 스코프·이벤트 확장
status: Blocked
assignee: []
created_date: '2026-07-18 05:54'
updated_date: '2026-07-18 06:50'
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
- [ ] #1 liv Slack 앱에 channels:history·channels:read + message.channels(및 groups 등 hermes 매니페스트 요구분) 스코프/이벤트 추가
- [ ] #2 앱 재설치로 새 토큰 반영, x-oauth-scopes 로 확인
- [ ] #3 채널 스레드 무멘션 메시지가 게이트웨이에 수신됨 확인
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
사용자 조치 필요(§3): 라이브 Slack 앱(리브, A0BJ3JMGBJA, workspace todolbi) 스코프 추가 + 재설치. 재설치는 **봇 토큰(xoxb) 로테이트**→구동 중 liv-bot.service 를 깨뜨리므로 TASK-49 커토버와 한 세션에서 함께 수행해야 함.

hermes 요구 매니페스트 저장: til-inbox bot/hermes/liv-slack-manifest.json (401줄, socket_mode_enabled=true).

## 추가할 봇 스코프 (현재: app_mentions:read,chat:write,im:write,im:history,im:read)
필수(스레드 무멘션 대화):
  channels:history, channels:read, groups:history, groups:read, mpim:history, mpim:read, users:read
+ 이벤트: message.channels, message.groups, message.mpim, app_mention, assistant_thread_started, assistant_thread_context_changed
선택(읽기전용 리브엔 불필요 권고 — 최소권한): assistant:write, commands, files:read, files:write
  → files:write 는 리브가 파일 안 올리므로 생략 권장. commands 는 hermes 슬래시(/new 등) 쓰려면 추가.

## 절차 (Chrome, api.slack.com 관리자 세션)
1. api.slack.com/apps → 리브 → OAuth & Permissions → Bot Token Scopes 에 위 필수 스코프 추가.
2. Event Subscriptions → Subscribe to bot events 에 위 이벤트 추가(Socket Mode 라 Request URL 불필요).
3. 'Reinstall to Workspace' → 새 Bot User OAuth Token(xoxb-) 발급.
4. 새 xoxb 를 ~/.liv/.env 와 ~/.hermes/profiles/liv/.env **양쪽** 의 SLACK_BOT_TOKEN 에 반영. (xapp App-Level Token 은 재설치로 안 바뀜.)
5. 즉시 TASK-49(커토버: 기존 liv-bot stop/disable → hermes-liv-gateway 기동)로 이어감. 두 인스턴스 동시 수신 방지.
6. 검증: 채널 스레드에서 멘션 없이 남긴 메시지가 게이트웨이에 수신되는지(TASK-44 에서 확인된 missing_scope: channels:read 해소).
<!-- SECTION:NOTES:END -->
