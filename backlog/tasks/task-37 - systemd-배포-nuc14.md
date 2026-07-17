---
id: TASK-37
title: systemd 배포 (nuc14)
status: Done
assignee: []
created_date: '2026-07-17 20:30'
updated_date: '2026-07-17 21:57'
labels: []
milestone: m-2
dependencies:
  - TASK-35
priority: medium
ordinal: 37000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
데몬을 nuc14 systemd 서비스로 상시 구동. 종량제 방지 가드 포함.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 systemd 유닛으로 상시 구동·실패 시 재시작
- [x] #2 UnsetEnvironment=ANTHROPIC_API_KEY 로 종량제 전환 차단
- [x] #3 토큰 런타임 참조, 재부팅/재시작 후 정상 재기동 확인
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
til-inbox bot/liv-bot.service(커밋 55aad1d), ~/.config/systemd/user/liv-bot.service 로 심링크+enable. systemd user 서비스(Linger=yes → 부팅 자동 기동). Restart=always/RestartSec=5, network-online 의존, KillMode=mixed+TimeoutStopSec=15(slack_bolt graceful shutdown 지연 대비). AC#1: enable --now → active(running), Socket Mode 연결. AC#2: UnsetEnvironment=ANTHROPIC_API_KEY, 실행 프로세스 /proc/PID/environ 에 API키 부재 실측 확인(데몬 subprocess env 제거와 이중). AC#3: systemctl restart → 재연결 확인. 재부팅은 enabled(default.target.wants)+Linger=yes 조합으로 부팅 자동 기동 보장(세션 비파괴 위해 실제 재부팅 대신 assert). 라이브 검증: #til 멘션→리브 응답 실동작 확인(테스트 allowlist drop-in 으로 실증 후 프로덕션 복귀·테스트 메시지 정리). 프로덕션은 봇 무시(사람만 응답).
<!-- SECTION:NOTES:END -->
