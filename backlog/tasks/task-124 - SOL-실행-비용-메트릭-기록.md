---
id: TASK-124
title: SOL 실행 비용 메트릭 기록
status: To Do
assignee: []
created_date: '2026-08-09 06:11'
labels:
  - solo
milestone: m-14
dependencies:
  - TASK-123
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
모델·effort 선택의 근거를 쌓기 위해 submit/research 실행마다 경과시간과 Codex가 보고한 토큰 사용량을 구조화 로그로 남긴다. Slack 성공 알림은 과밀해지지 않도록 경과시간만 짧게 표시하고 토큰은 로컬 로그에 둔다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 각 run_agent 호출의 경과시간과 실행기·모델·effort가 로그에 한 줄로 남는다
- [ ] #2 Codex 로그에 tokens used가 있으면 토큰 수를 구조화 로그에 기록하고 없으면 unknown으로 기록한다
- [ ] #3 성공 Slack 알림에 경과시간이 포함되고 실패 처리 semantics는 유지된다
- [ ] #4 mock 회귀 테스트가 메트릭 출력까지 검사한다
<!-- AC:END -->
