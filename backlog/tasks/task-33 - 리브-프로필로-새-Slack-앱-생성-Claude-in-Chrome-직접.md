---
id: TASK-33
title: 리브 프로필로 새 Slack 앱 생성 (Claude in Chrome 직접)
status: Blocked
assignee: []
created_date: '2026-07-17 20:30'
updated_date: '2026-07-17 20:47'
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
- [ ] #1 기존 #til 워크스페이스에 리브 프로필(이름·아바타)의 새 Slack 앱 생성
- [ ] #2 Socket Mode 활성화 + app-level token(xapp-) 발급
- [ ] #3 Bot token(xoxb-) 발급 + 필요한 스코프(app_mentions:read, chat:write, im:history, im:read, im:write)
- [ ] #4 Event Subscriptions 로 app_mention·message.im 구독
- [ ] #5 발급 토큰을 nuc14 시크릿(~/.hermes/.env 패턴)에 저장, repo 평문 커밋 금지
- [ ] #6 Slack 앱 생성·설정을 Claude in Chrome 브라우저 자동화로 수행
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
loop-task 자율 드레인 판정: 사용자 입회 필요. Claude in Chrome 으로 실 워크스페이스(#til)에 리브 앱 생성 + xapp/xoxb 실 토큰 발급 + ~/.hermes/.env 저장은 (1)인증된 브라우저 세션, (2)외부·비가역 앱 생성, (3)실 시크릿 취급이라 무인 헤드리스 루프에서 수행 부적합. nuc14 엔 Chrome 부재(Firefox 만). 사용자가 브라우저를 직접 몰아 진행해야 하며, 이 태스크가 m-2 임계경로(35→36/37→38→39)를 게이트한다.
<!-- SECTION:NOTES:END -->
