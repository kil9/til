---
id: TASK-47
title: liv Slack 앱 스코프·이벤트 확장
status: To Do
assignee: []
created_date: '2026-07-18 05:54'
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
