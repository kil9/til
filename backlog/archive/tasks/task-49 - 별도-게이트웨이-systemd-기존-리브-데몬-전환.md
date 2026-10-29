---
id: TASK-49
title: 별도 게이트웨이 systemd + 기존 리브 데몬 전환
status: Done
assignee: []
created_date: '2026-07-18 05:55'
updated_date: '2026-07-18 09:44'
labels: []
milestone: m-4
dependencies:
  - TASK-45
  - TASK-46
  - TASK-47
priority: medium
ordinal: 49000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
리브 프로필 게이트웨이를 상시 구동하고 기존 standalone liv-bot.service 를 은퇴시킨다. 워크스페이스에 hermes 인스턴스 난입·중복 알림 이력(todolbi task-6)이 있어 인스턴스 충돌에 유의.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 hermes-liv-gateway.service(리브 프로필) systemd user 유닛 신설·enable·상시구동
- [x] #2 기존 liv-bot.service disable/stop 은퇴, 두 인스턴스 동시 수신 방지
- [x] #3 워크스페이스 인스턴스 충돌(중복 알림 등) 없음 확인, 재부팅 후 자동기동
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
완료 (2026-07-18). hermes-gateway-liv.service 커토버 완료.
- AC#1: systemd user 유닛 hermes-gateway-liv.service 신설·enable(부팅 자동기동). ExecStart '--profile liv', Environment HERMES_HOME=/home/kil9/.hermes/profiles/liv. 런타임 /proc/PID/environ 검증 → 어드바이저 MUST-FIX #1(전용 HERMES_HOME 이라야 툴잠금 유효) 충족.
- AC#2: 기존 liv-bot.service stop+disable. Slack Socket Mode 연결(@liv, workspace todolbi). 재설치가 토큰 미로테이트라 이중수신 없음.
- AC#3: 라이브 E2E 로 단일 인스턴스 정상수신 확인(DM·채널·스레드 모두 1회 응답). 재부팅 자동기동 enable.
- 응답 정책: slack.dm_policy/group_policy=open + require_mention(스레드 무멘션 팔로우) + GATEWAY_ALLOW_ALL_USERS=true. 홈채널 #til(C0BJUAH0Y7J).
- 트러블슈팅 기록: (1) 로그는 journal 이 WARNING만 — 상세는 프로필 logs/gateway.log(INFO). (2) 포그라운드 nohup 게이트웨이가 데몬화(PPID=1)해 gateway.lock 을 쥐면 systemd 가 'Another gateway instance' 로 크래시루프 → 고아 프로세스 kill + lock 제거로 해소. (3) 'status=1/FAILURE' 는 SIGTERM 종료 아티팩트(크래시 아님).
<!-- SECTION:NOTES:END -->
