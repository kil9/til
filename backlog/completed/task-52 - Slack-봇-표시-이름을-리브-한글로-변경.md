---
id: TASK-52
title: Slack 봇 표시 이름을 '리브' 한글로 변경
status: Done
assignee: []
created_date: '2026-07-18 06:52'
updated_date: '2026-07-18 10:14'
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
완료 (2026-07-18, Chrome). App Home > Your App's Presence 에서 표시명 분리 설정: Display Name (Bot Name)='리브'(한글), Default username='liv'(ASCII 핸들 유지). 매니페스트 bot_user.display_name 은 username 파생 때문에 한글 불가(에러 'cannot be converted to a username')였고, App Home UI 가 표시명↔핸들을 분리해 해결(삐약이와 동일 방식). 검증: App Home 'Display Name (Bot Name): 리브', auth.test user=liv. AC#2(코드 감사)는 이미 완료 — 멘션 파싱 user-ID 기반이라 코드 무영향.

[정정 2026-07-18] AC#1(작성자명 '리브' 표시)은 **기존 liv 앱에서 불가**로 판명. 실측: App Home Display='리브'+username 변경·재설치 후에도 봇 users.info 는 name/real_name='liv' 유지(기존 봇 정체성 immutable). users.profile.set 은 봇토큰 not_allowed_token_type. 한글 표시는 새 앱을 handle(ASCII)≠표시(한글)로 생성해야 가능(삐약이 방식) → **TASK-53 으로 이관**. AC#2(멘션 파싱 코드 무영향)는 완료 유지. 현 앱 App Home 에 inert 로 남은 변경(username=livbot·Display=리브)은 TASK-53 에서 구앱 은퇴 시 함께 정리.
<!-- SECTION:NOTES:END -->
