---
id: TASK-118
title: 브리핑 항목 반응 온도 배지
status: In Progress
assignee: []
created_date: '2026-08-06 05:51'
updated_date: '2026-08-06 06:06'
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
- [x] #1 수집 단계가 GeekNews 댓글수를 항목 데이터에 남긴다
- [x] #2 compose 가 반응 온도 배지 여부·종류를 판정하되 임계를 둬 회차당 소수 항목에만 붙는다
- [x] #3 item.html 에 배지 토큰이 추가되고 값이 없으면 빈 문자열로 렌더된다
- [x] #4 배지 종류·판정 기준이 backlog/assets/briefing/README.md 에 문서화된다
- [ ] #5 실제 발행 회차 1건 이상에서 배지가 표시된다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
구현 완료(2026-08-06). 잡 코드(nuc14 ~/jobs/liv-briefing/, 비버전)는 compose.py 의 HEAT_FLOOR/HEAT_TOP_N/HEAT_KINDS·heat_candidates()·heat_value() 와 render.py 의 BADGE 토큰이고, repo 쪽은 item.html·template.html(.heat)·README 다.

착수 전 확인에서 계획 전제 하나가 틀린 것을 잡았다 — select.py 의 decorate() 가 collect 항목을 dict() 로 통째 복사하므로 comments 는 이미 selected-*.json 에 있었다. 빠진 곳은 compose 출력 dict 한 곳뿐이라 실제 배관 작업은 한 줄이었다.

임계 설계: 절대 하한(댓글 10개) AND 회차 상위 2건. 상대 순위만 두면 안 되는 근거는 실측이다 — 최근 7회차의 회차별 최대 댓글수가 12/3/6/6/6/3/10 이라 5회차는 한 자리다. 이 임계로 7회차 중 2회차에만 후보가 생긴다. 종류 판정만 모델이 하고 heat_value() 가 후보 밖·모르는 값을 뗀다.

검증: 임계·관문 단위 검증(경계값·빈 입력·comments 필드 부재 포함)과 실데이터 렌더 dry-run 통과. 값 없으면 배지·구분점이 함께 빠지고, 값 있으면 span 1개(용량 +36B)다.

AC#5(실제 발행 회차에서 표시)만 남았다. 내일 09:00 정기 발행이 검증 창이다 — 오늘 회차를 재compose 해 덮어쓰면 이미 발행·Slack 공지된 페이지가 바뀌는데 얻는 것이 AC 를 하루 일찍 닫는 것뿐이라 하지 않는다. 오늘 회차 후보는 id=32164(댓글 10개)로 이미 산출된다.
<!-- SECTION:NOTES:END -->
