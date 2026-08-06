---
id: TASK-118
title: 브리핑 항목 반응 온도 배지
status: To Do
assignee: []
created_date: '2026-08-06 05:51'
labels:
  - solo
milestone: m-13
dependencies: []
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
AIwitness 커뮤니티 인사이트(https://aiwitness.kr/community)의 🔥논쟁 배지를 참고. 항목의 커뮤니티 반응 온도(논쟁 중·화제 등)를 GeekNews 댓글수·논조 근거로 판정해 브리핑 항목 메타에 작은 배지로 표시한다.

검토할 것:
- collect.py(nuc14 ~/jobs/liv-briefing/)가 이미 GeekNews 추천수를 수집한다 — 댓글수도 같은 자리에서 얻을 수 있는지 확인.
- 논조 판정은 compose(Opus 5)가 댓글 페이지를 근거로 한다. 댓글 본문까지 수집할지, 수만 볼지 결정.
- 배지는 드물어야 효과가 있다(스티커·삽화와 같은 원칙). 임계 없이 전 항목에 붙이면 장식이 된다.
- item.html 의 우측 메타(관심사·백분위 옆)가 자연스러운 자리다. 토큰은 없을 때 빈 문자열 규칙({{TIEBOX}}·{{LIV}}와 동일).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 수집 단계가 GeekNews 댓글수를 항목 데이터에 남긴다
- [ ] #2 compose 가 반응 온도 배지 여부·종류를 판정하되 임계를 둬 회차당 소수 항목에만 붙는다
- [ ] #3 item.html 에 배지 토큰이 추가되고 값이 없으면 빈 문자열로 렌더된다
- [ ] #4 배지 종류·판정 기준이 backlog/assets/briefing/README.md 에 문서화된다
- [ ] #5 실제 발행 회차 1건 이상에서 배지가 표시된다
<!-- AC:END -->
