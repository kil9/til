---
id: TASK-73
title: cloudflared Tunnel systemd 구성 (nuc14 서비스 노출)
status: To Do
assignee: []
created_date: '2026-07-21 02:20'
labels:
  - solo
milestone: m-7
dependencies:
  - TASK-70
priority: medium
ordinal: 73000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
cloudflared 를 nuc14 에 설치해 터널을 만들고 systemd 서비스로 상시 구동한다. family-reports 등 내부 서비스를 서브도메인으로 노출한다. 인증 게이트는 후속 Access 태스크 몫이므로, 그 전까지 민감 서비스는 노출하지 않거나 임시 보호를 둔다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 터널이 systemd 로 재부팅 후에도 자동 기동된다
- [ ] #2 지정 서브도메인으로 외부에서 대상 서비스에 접속된다
<!-- AC:END -->
