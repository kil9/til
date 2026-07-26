---
id: TASK-80
title: GeekNews 수집·선별 잡 구성
status: To Do
assignee: []
created_date: '2026-07-26 03:55'
updated_date: '2026-07-26 06:35'
labels:
  - solo
milestone: m-8
dependencies:
  - TASK-79
priority: medium
ordinal: 80000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
~/jobs/ 아래 docs-ai-summary 와 같은 구조로 데일리 잡을 만든다. RSS(https://news.hada.io/rss/news)를 받아 이미 처리한 항목을 state 로 걸러내고, 관심사 프로필과 함께 headless claude 에 넘겨 상위 N건 선별 + 항목당 요약 3-4줄 + 제외 사유를 생성한다. 파일럿에서 항목 상세는 news.hada.io/topic?id=NNN 을 개별로 가져와야 밀도가 나왔다 - 선별 후에만 상세를 가져오는 2단 구성으로 호출 수를 줄인다. 신규 항목이 임계 미만이면 LLM 호출 없이 조기 종료(docs-ai-summary 의 패턴).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 cron 으로 매일 아침 1회 도는 run.sh 와 state 가 있다
- [ ] #2 RSS 수집 → 1차 선별 → 선별분만 상세 fetch 의 2단 구성으로 동작한다
- [ ] #3 신규 없음/실패 시 조용히 종료하고 로그를 남긴다
- [ ] #4 선별 결과가 페이지 생성 단계가 소비할 중간 포맷(JSON)으로 떨어진다
- [ ] #5 선별·정리 모델은 Claude Opus 5 를 기본으로 쓴다 (fable 아님)
- [ ] #6 선별 건수는 7-10건 범위에서 모델이 그날 재료에 맞춰 정한다
- [ ] #7 선별은 두 축이다: 관심사 프로필 매칭 + GeekNews 추천수. 추천 상위 2-5건은 관심사와 무관해도 무조건 포함한다
- [ ] #8 RSS 만으로는 인기 순위를 알 수 없으므로 첫 페이지(추천수·노출 순서)도 함께 수집한다
- [ ] #9 인기 축 컷은 절대 추천수가 아니라 최근 30일 롤링 분포의 백분위(p90)로 잡고, 통과 건수를 2-5건으로 clamp 한다. 데이터가 없는 초기에는 그날 수집분 내부 분위수로 폴백
- [ ] #10 수집 범위는 첫 페이지에 그치지 않는다(오늘 실측: 상위 6% 항목이 2페이지에 있었다)
- [ ] #11 정렬은 추천 백분위가 1순위이고 관심사는 동률·인접 보정에만 쓴다. 관심사가 맞아도 추천이 낮으면 아래로 내려간다(파일럿 v6 에서 확정)
<!-- AC:END -->
