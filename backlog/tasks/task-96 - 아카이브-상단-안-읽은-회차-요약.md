---
id: TASK-96
title: 아카이브 상단 안 읽은 회차 요약
status: To Do
assignee: []
created_date: '2026-07-26 09:45'
labels: []
milestone: m-10
dependencies:
  - TASK-93
priority: medium
ordinal: 96000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
task-93 의 읽음 기록(localStorage liv-briefing-read)을 아카이브 목록 상단에서 한 줄로 요약한다. 안 읽은 건수와 가장 오래된 안 읽은 회차로 가는 링크. 전부 읽었으면 줄 자체를 감춘다. JS 없이/저장소가 막힌 브라우저에서는 기존 모습 그대로여야 한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 안 읽은 회차가 있으면 목록 위에 건수와 가장 오래된 안 읽은 회차 링크가 나온다
- [ ] #2 전부 읽었거나 저장소를 못 읽으면 그 줄이 보이지 않고 레이아웃도 그대로다
- [ ] #3 링크를 따라간 회차가 읽음 처리돼 다음 방문 때 건수가 줄어든다(로직 검증)
<!-- AC:END -->
