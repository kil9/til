---
id: TASK-49
title: 별도 게이트웨이 systemd + 기존 리브 데몬 전환
status: To Do
assignee: []
created_date: '2026-07-18 05:55'
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
- [ ] #1 hermes-liv-gateway.service(리브 프로필) systemd user 유닛 신설·enable·상시구동
- [ ] #2 기존 liv-bot.service disable/stop 은퇴, 두 인스턴스 동시 수신 방지
- [ ] #3 워크스페이스 인스턴스 충돌(중복 알림 등) 없음 확인, 재부팅 후 자동기동
<!-- AC:END -->
