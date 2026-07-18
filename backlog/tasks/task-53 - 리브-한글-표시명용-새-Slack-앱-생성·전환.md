---
id: TASK-53
title: 리브 한글 표시명용 새 Slack 앱 생성·전환
status: To Do
assignee: []
created_date: '2026-07-18 10:13'
labels: []
dependencies: []
priority: medium
ordinal: 53000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
TASK-52 결론: 기존 봇(생성 시 handle=real_name='liv'로 굳음)의 이름은 App Home 변경·재설치·users.profile.set(봇토큰 not_allowed_token_type) 어느 것으로도 못 바꾼다(실측). 한글 '리브' 표시를 얻으려면 삐약이(handle=tdb_bot, real_name=삐약)처럼 **생성 시점부터 handle(ASCII)≠표시(한글)** 로 새 앱을 만들어야 한다. 사용자 결정=새 앱 생성.
핵심: 새 봇은 첫 설치 전에 App Home Display Name='리브' + Default username=ASCII(예: livtoday) 로 설정해야 real_name='리브' 로 생성된다(매니페스트 bot_user.display_name='리브'는 username 파생 에러 → ASCII 로 두고 App Home 에서 분리). 준비된 스코프/이벤트/소켓 매니페스트: til-inbox bot/hermes/liv-new-app-manifest.json(12 스코프·7 이벤트·socket_mode).
절차: (1)api.slack.com Create New App(from scratch 또는 manifest, name='리브') (2)Bot User Display='리브'/username=ASCII 를 첫 설치 전 설정 (3)App-Level Token(connections:write) 생성→xapp (4)Install→xoxb, users.info 로 real_name='리브' 확인 (5)App Home Messages Tab + 'Allow users to send messages' 체크 (6)새 xapp·xoxb 를 ~/.liv/.env·~/.hermes/profiles/liv/.env 반영 (7)slack.home_channel 유지(#til C0BJUAH0Y7J) (8)hermes-gateway-liv 재시작 (9)새 봇 #til 초대 (10)기존 'liv' 앱 uninstall/은퇴 (11)E2E 재검증(대화·스레드무멘션·툴잠금·디스패치).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 새 Slack 앱이 real_name='리브'(한글)·handle=ASCII 로 생성됨(users.info 확인)
- [ ] #2 새 xapp·xoxb 토큰을 ~/.liv/.env 와 리브 프로필 .env 에 반영, 게이트웨이가 새 앱으로 Socket Mode 연결
- [ ] #3 기존 'liv' 앱 은퇴(이중 수신 없음), #til 에서 봇 작성자명이 '리브'로 표시
- [ ] #4 E2E 재검증: 대화·스레드무멘션·툴잠금·아카이브조회·디스패치 정상
<!-- AC:END -->
