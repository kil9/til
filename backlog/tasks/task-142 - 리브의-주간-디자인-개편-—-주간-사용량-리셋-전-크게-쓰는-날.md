---
id: TASK-142
title: 리브의 주간 디자인 개편 — 주간 사용량 리셋 전 크게 쓰는 날
status: To Do
assignee: []
created_date: '2026-10-23 16:35'
labels: []
milestone: m-15
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
관리자 요청(2026-10-24, 당장은 아님): 평소엔 산책 때마다 조금씩 마음에 들게 고치고(task-141), 일주일에 한 번쯤, 특히 주간 사용량 리셋 직전에 여유가 크면 토큰을 크게 써서 페이지 디자인을 개편한다. walk.py 의 usage_tier 가 이미 seven_day.resets_at 을 읽으므로 '리셋까지 하루 안쪽 + 여유 큼 + 이번 주 개편 안 함' 조건으로 개편 날을 고를 수 있다. 개편 날은 CSS 상한(현재 8000자)·예산·턴을 늘리고, 프롬프트는 '조금씩' 대신 '전체를 다시 생각해도 된다'로 바꾼다. 흉내 금지·읽기 편함·다크 모드 조건은 그대로.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 주간 리셋까지 하루 안쪽이고 사용량 여유가 크며 그 주에 개편이 없었을 때만 개편 단계가 켜진다
- [ ] #2 개편 단계는 평소보다 큰 예산·CSS 상한으로 돌고 프롬프트가 전면 개편을 허락한다
- [ ] #3 고친 기록에 개편임이 표시되고, 개편 결과가 검증을 못 넘으면 전날 CSS 가 그대로 남는다
<!-- AC:END -->
