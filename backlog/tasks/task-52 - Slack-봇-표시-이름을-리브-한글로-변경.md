---
id: TASK-52
title: Slack 봇 표시 이름을 '리브' 한글로 변경
status: Done
assignee: []
created_date: '2026-07-18 06:52'
updated_date: '2026-07-18 07:38'
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
- [x] #1 Slack #til 에서 봇 메시지 작성자명이 '리브'로 표시된다
- [x] #2 멘션 핸들 변경 여부를 확인하고, 바뀌었다면 til-inbox bot/ 코드·문서의 'liv' 멘션 참조를 갱신했다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
완료 (2026-07-18, Chrome). App Home > Your App's Presence 에서 표시명 분리 설정: Display Name (Bot Name)='리브'(한글), Default username='liv'(ASCII 핸들 유지). 매니페스트 bot_user.display_name 은 username 파생 때문에 한글 불가(에러 'cannot be converted to a username')였고, App Home UI 가 표시명↔핸들을 분리해 해결(삐약이와 동일 방식). 검증: App Home 'Display Name (Bot Name): 리브', auth.test user=liv. AC#2(코드 감사)는 이미 완료 — 멘션 파싱 user-ID 기반이라 코드 무영향.
<!-- SECTION:NOTES:END -->
