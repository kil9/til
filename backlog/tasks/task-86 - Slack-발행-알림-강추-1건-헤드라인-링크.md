---
id: TASK-86
title: Slack 발행 알림 (강추 1건 + 헤드라인 + 링크)
status: To Do
assignee: []
created_date: '2026-07-26 07:27'
labels:
  - solo
milestone: m-9
dependencies:
  - TASK-85
priority: high
ordinal: 86000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
브리핑이 push 되면 Slack #til 로 리브가 알린다. 형식은 강추 1건(제목 + 왜 권하는지 한 줄) + 나머지 항목 제목을 한 줄로 압축 + 페이지 링크. 전문을 싣지 않는 이유는 알림 피로를 만들지 않고 실제로 페이지를 열게 하기 위함이다.

기존 자산: til-submit 워처가 이미 Slack #til 로 접수·완료를 알리고 있고, 리브 봇(hermes-gateway-liv, 표시명 '리브')이 있다. 같은 앱·같은 말투로 보낸다. 발행 실패 시에도 같은 채널로 알린다(task-85 의 실패 통지).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 발행 성공 시 강추 1건 + 헤드라인 + 링크가 #til 로 간다
- [ ] #2 리브 봇 계정·말투로 나가며 기존 접수 알림과 톤이 일관된다
- [ ] #3 발행 실패 시 원인 요약이 같은 채널로 간다
<!-- AC:END -->
