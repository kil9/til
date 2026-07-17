---
id: TASK-37
title: systemd 배포 (nuc14)
status: To Do
assignee: []
created_date: '2026-07-17 20:30'
updated_date: '2026-07-17 20:31'
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
- [ ] #1 systemd 유닛으로 상시 구동·실패 시 재시작
- [ ] #2 UnsetEnvironment=ANTHROPIC_API_KEY 로 종량제 전환 차단
- [ ] #3 토큰 런타임 참조, 재부팅/재시작 후 정상 재기동 확인
<!-- AC:END -->
