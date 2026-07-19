---
id: TASK-33
title: 리브 프로필로 새 Slack 앱 생성 (Claude in Chrome 직접)
status: Done
assignee: []
created_date: '2026-07-17 20:30'
updated_date: '2026-07-17 21:11'
labels:
  - solo
milestone: m-2
dependencies: []
priority: high
ordinal: 33000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
기존 #til 워크스페이스에 tdb_bot 과 별개인 리브 전용 앱을 만든다. 사용자 지시대로 Claude in Chrome 브라우저 자동화로 api.slack.com 을 직접 조작한다. 이름 리브, 아바타는 리브 원형 아이콘.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 기존 #til 워크스페이스에 리브 프로필(이름·아바타)의 새 Slack 앱 생성
- [x] #2 Socket Mode 활성화 + app-level token(xapp-) 발급
- [x] #3 Bot token(xoxb-) 발급 + 필요한 스코프(app_mentions:read, chat:write, im:history, im:read, im:write)
- [x] #4 Event Subscriptions 로 app_mention·message.im 구독
- [x] #5 발급 토큰을 nuc14 시크릿(~/.hermes/.env 패턴)에 저장, repo 평문 커밋 금지
- [x] #6 Slack 앱 생성·설정을 Claude in Chrome 브라우저 자동화로 수행
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Claude in Chrome(사용자 Windows Chrome, 사용자 입회)으로 api.slack.com 직접 조작해 완료. manifest 방식으로 todolbi 워크스페이스에 앱 '리브'(App ID A0BJ3JMGBJA) 생성 — bot username liv(한글 username 불가로 ASCII), App Home 표시 이름은 '리브'로 설정, 아바타는 리브 원형 아이콘(avatar-expression-base 512px PNG 업스케일) 업로드. Socket Mode 활성 + app-level token liv-socket(connections:write, xapp-) 발급, 워크스페이스 설치로 xoxb 발급(스코프 5종: app_mentions:read/chat:write/im:history/im:read/im:write — x-oauth-scopes 헤더로 확인). Event Subscriptions 는 bot events app_mention·message.im 구독. 토큰 2종은 nuc14 ~/.liv/.env(디렉터리 700/파일 600, hermes .env 패턴)에 저장, repo 커밋 없음. 검증: auth.test ok(team todolbi, user liv, U0BHQ831C9M), apps.connections.open ok(wss URL 발급 — Socket Mode 실동작 확인).
<!-- SECTION:NOTES:END -->
