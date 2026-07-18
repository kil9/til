---
id: TASK-53
title: 리브 한글 표시명용 새 Slack 앱 생성·전환
status: Done
assignee: []
created_date: '2026-07-18 10:13'
updated_date: '2026-07-18 10:43'
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
- [x] #1 새 Slack 앱이 real_name='리브'(한글)·handle=ASCII 로 생성됨(users.info 확인)
- [x] #2 새 xapp·xoxb 토큰을 ~/.liv/.env 와 리브 프로필 .env 에 반영, 게이트웨이가 새 앱으로 Socket Mode 연결
- [x] #3 기존 'liv' 앱 은퇴(이중 수신 없음), #til 에서 봇 작성자명이 '리브'로 표시
- [x] #4 E2E 재검증: 대화·스레드무멘션·툴잠금·아카이브조회·디스패치 정상
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
완료 (2026-07-18). 새 Slack 앱 A0BJ1H0HH0B 생성·전환, 한글 표시명 확보.
- 생성: manifest(from a manifest, display_name=livtoday ASCII) → 첫 설치 전 App Home 에서 Display Name='리브'/username=livtoday 분리 → 설치. users.info: name=livtoday, real_name=리브 (AC#1). 매니페스트 에디터에 한글 display_name 넣으면 'Fix errors (line 9)' 로 저장 거부되는 것 실측 재확인 — App Home 분리 설정이 유일 경로.
- 토큰: 새 xapp(socket, connections:write)·xoxb 를 ~/.liv/.env·~/.hermes/profiles/liv/.env 반영, hermes-gateway-liv 재시작 → 'Authenticated as @livtoday' + Socket Mode connected (AC#2).
- #til 초대: channels:join 스코프 추가(재설치) 후 conversations.join 으로 자가 join. 참고: 구 UI /oauth·/app-manifest 경로는 app.slack.com 새 설정 UI 로 넘어가며 첫 로드가 간헐 실패 — 재시도로 해결.
- 은퇴: 구 앱(A0BJ3JMGBJA) xoxb auth.revoke → account_inactive, 봇유저 liv deleted=True. 이중 수신 없음. #til 작성자명 '리브' 표시 확인(참여 메시지·응답 모두) (AC#3).
- E2E (AC#4): 멘션 대화 ✅ / 스레드 무멘션 후속 ✅ / 아카이브 조회 ✅(web_extract=plainfetch 로 kil9.github.io/til 실조회, 최신 2건 제목 실제와 일치) / 툴잠금 ✅(cat ~/.liv/.env injection → api_calls=1 툴 미호출 텍스트 거부) / 디스패치 ✅(dry-run 테스트 스위트 ALL PASS + 툴잠금 스위트 ALL PASS). model=claude-sonnet-5 구독 소모 유지.
- til-inbox: liv-new-app-manifest.json 실생성값 동기화(display_name ASCII, channels:join) 커밋 4d3d58e.
<!-- SECTION:NOTES:END -->
