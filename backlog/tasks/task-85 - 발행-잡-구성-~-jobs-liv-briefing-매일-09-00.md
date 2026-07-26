---
id: TASK-85
title: '발행 잡 구성 (~/jobs/liv-briefing/, 매일 09:00)'
status: To Do
assignee: []
created_date: '2026-07-26 07:27'
labels:
  - solo
milestone: m-9
dependencies:
  - TASK-80
  - TASK-81
priority: high
ordinal: 85000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
nuc14 cron 이 매일 09:00 KST 에 브리핑을 생성해 til 에 push 한다. 기존 ~/jobs/docs-ai-summary·til-submit 과 같은 배관을 쓴다: run.sh + state/ + flock + cron.log, 실패해도 조용히 죽지 말고 로그를 남긴다.

파이프라인: GeekNews 수집(task-80) → 선별·정리(headless claude -p --model opus) → 페이지 렌더(task-81 템플릿) → p/briefing/ 과 p/briefing/<날짜>/ 에 쓰기 → git commit·push → Pages 반영.

함정: (1) docs-ai-summary 가 로케일 정렬과 pipefail 로 두 번 조용히 죽은 전례가 있다. 같은 실수를 반복하지 않도록 비교 구간은 LC_ALL=C, 루프 끝 종료코드는 고정한다. (2) 같은 날 두 번 도는 것을 state 로 막는다. (3) til 워킹트리가 dirty 하면 push 가 남의 변경을 삼킬 수 있으므로 전용 클론(repo/)을 쓰고 git add 는 경로 명시로만 한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 cron 0 9 * * * 로 등록돼 매일 09:00 에 돈다
- [ ] #2 run.sh 가 수집→선별→렌더→push 를 한 번에 수행하고 flock 으로 중복 실행을 막는다
- [ ] #3 같은 날 이미 발행됐으면 LLM 호출 없이 조기 종료한다
- [ ] #4 실패 시 cron.log 에 원인이 남고 Slack 으로 실패가 통지된다
- [ ] #5 전용 클론에서만 커밋하며 add 는 경로를 명시한다
<!-- AC:END -->
