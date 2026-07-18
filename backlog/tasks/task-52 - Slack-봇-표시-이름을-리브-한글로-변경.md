---
id: TASK-52
title: Slack 봇 표시 이름을 '리브' 한글로 변경
status: Blocked
assignee: []
created_date: '2026-07-18 06:52'
updated_date: '2026-07-18 06:54'
labels: []
dependencies: []
priority: medium
ordinal: 52000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Slack 앱 프로필 이름은 이미 '리브'인데, 메시지 작성자·멘션(@liv)에 쓰이는 봇 유저 표시 이름은 여전히 영문 'liv' 로 뜬다. Slack 앱 설정의 Bot User display name(App Home > Your App's Presence in Slack)을 한글 '리브'로 바꾼다. 멘션 핸들이 바뀌면 봇 코드·문서에서 'liv' 리터럴로 멘션을 파싱·표기하는 곳이 있는지 til-inbox bot/ 에서 확인해 함께 갱신한다. Slack 설정 변경은 사용자 조치가 필요할 수 있다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Slack #til 에서 봇 메시지 작성자명이 '리브'로 표시된다
- [x] #2 멘션 핸들 변경 여부를 확인하고, 바뀌었다면 til-inbox bot/ 코드·문서의 'liv' 멘션 참조를 갱신했다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
AC#2 완료(코드 감사): til-inbox bot/ 멘션 파싱은 user ID 기반(strip_mention 정규식 <@[A-Z0-9]+>, app_mention 이벤트도 user id). 표시 이름을 '리브'로 바꿔도 멘션 핸들·파싱 무관 → 봇 코드 변경 불필요. 내부 'liv' 리터럴(스레드명·이슈 SOURCE 태그·히스토리 라벨)은 Slack 표시명과 무관.

AC#1 사용자 조치 필요(Blocked): Slack 앱 Bot User display name 을 '리브'로 변경. TASK-47 재설치와 커플링 — 스테이징 매니페스트(til-inbox bot/hermes/liv-slack-manifest.json)의 display_information.name·features.bot_user.display_name 을 '리브'로 갱신해 둠. 재설치 시 반영되거나, api.slack.com → 리브 앱 → App Home > Your App's Presence in Slack > Display Name 에서 직접 '리브'로 변경. (Slack 핸들/username 은 ASCII 제약이라 @liv 로 유지될 수 있음 — 표시 이름만 한글화.)
<!-- SECTION:NOTES:END -->
