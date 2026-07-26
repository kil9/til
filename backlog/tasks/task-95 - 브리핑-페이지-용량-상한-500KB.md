---
id: TASK-95
title: 브리핑 페이지 용량 상한 500KB
status: Done
assignee: []
created_date: '2026-07-26 09:45'
updated_date: '2026-07-26 09:47'
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
- [x] #1 render.py 의 MAX_BYTES 가 500KB 이고 왜 그 값인지 주석에 남는다
- [x] #2 README.md 의 자산·용량 문단이 새 상한과 어긋나지 않는다
- [x] #3 현재 회차를 재렌더했을 때 경고가 나오지 않는다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
MAX_BYTES 100_000 → 500_000, 초과 문구도 상수에서 뽑아 쓰게 바꿔 다음에 값만 고치면 되게 했다. 근거는 주석에 남겼다(구 상한이 실측치와 붙어 매 회차 경고 → 경고가 일상이 되면 죽는다, 500KB×365=178MB 로 Pages 1GB 한도 안). README 의 자산·용량 문단과 누적 추정치(90KB→100KB)도 새 실측에 맞췄다. 검증: 현재 회차(99.7KB) 재렌더에서 경고 없음.
<!-- SECTION:NOTES:END -->
