---
id: TASK-95
title: 브리핑 페이지 용량 상한 500KB
status: To Do
assignee: []
created_date: '2026-07-26 09:45'
labels: []
milestone: m-10
dependencies: []
priority: high
ordinal: 95000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
MAX_BYTES 가 100KB 라 현재 99.7KB 인 페이지는 다음 회차부터 매일 경고를 낸다. 매일 뜨는 경고는 곧 무시되므로 상한을 500KB 로 올려 '경고가 뜨면 진짜 이상한 것' 인 상태로 되돌린다. 근거 문장이 남아 있는 backlog/assets/briefing/README.md 도 함께 고친다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 render.py 의 MAX_BYTES 가 500KB 이고 왜 그 값인지 주석에 남는다
- [ ] #2 README.md 의 자산·용량 문단이 새 상한과 어긋나지 않는다
- [ ] #3 현재 회차를 재렌더했을 때 경고가 나오지 않는다
<!-- AC:END -->
