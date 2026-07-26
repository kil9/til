---
id: TASK-89
title: Slack 에서 바로 조사 지시
status: To Do
assignee: []
created_date: '2026-07-26 07:28'
labels:
  - solo
milestone: m-9
dependencies:
  - TASK-86
  - TASK-82
priority: medium
ordinal: 89000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
폰으로 Slack 브리핑을 읽다가 바로 조사를 시킬 수 있게 한다. 발행 메시지의 스레드에 답글을 달면 그것이 til-inbox 이슈(KIND: submit)가 되고, 리브가 회신한다. 항목을 특정할 수 있게 메시지에 항목 번호를 넣거나 Block Kit 버튼을 단다.

기존 자산이 절반쯤 있다: til-inbox 워처가 SOURCE/KIND/REQUEST 규약으로 이슈를 소비하고, 리브 봇(hermes-gateway-liv)이 이미 Slack 대화를 받는다. 새로 필요한 것은 발행 메시지 스레드를 브리핑 항목과 묶는 매핑과, 어느 항목을 가리키는지 모호할 때 리브가 되묻는 경로다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 발행 메시지 스레드에 답글을 달면 til-inbox 이슈가 생성된다
- [ ] #2 어느 항목에 대한 지시인지 항목 번호나 버튼으로 특정된다
- [ ] #3 모호하면 리브가 스레드에서 되묻고, 확정되면 진행한다
- [ ] #4 페이지 버튼(task-82)과 같은 요청 규약을 쓴다
<!-- AC:END -->
