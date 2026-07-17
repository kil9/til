---
id: TASK-35
title: Socket Mode 데몬 뼈대 (til-inbox repo)
status: To Do
assignee: []
created_date: '2026-07-17 20:30'
updated_date: '2026-07-17 20:31'
labels: []
milestone: m-2
dependencies:
  - TASK-33
priority: high
ordinal: 35000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
til-inbox repo 에 slack_bolt Socket Mode 데몬을 얹는다. 멘션·DM 수신 → 에코까지 되는 최소 골격.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 til-inbox repo 에 리브 봇 데몬 스캐폴딩
- [ ] #2 slack_bolt Socket Mode 로 app_mention·DM 수신 확인(에코 응답)
- [ ] #3 토큰은 ~/.hermes/.env 런타임 참조, 평문 커밋 금지
<!-- AC:END -->
