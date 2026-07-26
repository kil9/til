---
id: TASK-96
title: 아카이브 상단 안 읽은 회차 요약
status: Done
assignee: []
created_date: '2026-07-26 09:45'
updated_date: '2026-07-26 09:49'
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
- [x] #1 안 읽은 회차가 있으면 목록 위에 건수와 가장 오래된 안 읽은 회차 링크가 나온다
- [x] #2 전부 읽었거나 저장소를 못 읽으면 그 줄이 보이지 않고 레이아웃도 그대로다
- [x] #3 링크를 따라간 회차가 읽음 처리돼 다음 방문 때 건수가 줄어든다(로직 검증)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
아카이브 목록 위에 .unread-line 한 줄(안 읽은 건수 + 가장 오래된 안 읽은 회차 링크)을 넣었다. 기본 hidden 이고 안 읽은 것이 있을 때만 JS 가 켠다. 목록이 최신 순이라 미독 배열의 마지막이 가장 오래된 회차다. 검증: 회차 3건(07-24·25·26)을 임시로 렌더한 뒤 페이지에 박힌 스크립트를 스텁 DOM(node)에서 4가지 상태로 돌렸다 — 읽음[24]→2건·링크 07-25, 읽음[24,25]→1건·링크 07-26(따라가 읽으면 건수가 준다), 전부 읽음→줄 숨김, localStorage 예외→줄 숨김에 행 클래스도 안 붙어 원래 모습 유지. 임시 회차는 정리했다.
<!-- SECTION:NOTES:END -->
