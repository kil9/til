---
id: DRAFT-4
title: Hacker News 를 두 번째 소스로 추가
status: Draft
assignee: []
created_date: '2026-07-26 06:01'
labels:
  - solo
milestone: m-8
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
현재 브리핑 소스는 GeekNews(news.hada.io) 하나다. https://news.ycombinator.com/ 을 두 번째 소스로 붙여 한 브리핑에 함께 싣는다.

검토할 것:
- 수집: HN 은 공식 Firebase API(hacker-news.firebaseio.com)와 Algolia 검색 API 가 있어 RSS 보다 점수·댓글수를 정확히 얻기 쉽다. GeekNews 는 첫 페이지 스크레이핑이 필요했던 것과 대비된다.
- 인기 축 정규화: GeekNews 추천수(오늘 실측 중앙값 7, 최대 56)와 HN points(수백 단위)는 스케일이 다르다. 절대값을 섞지 말고 각 소스 내부의 백분위로 환산해 비교해야 한다. task-80 의 롤링 백분위 컷을 소스별로 따로 유지하는 형태.
- 중복 제거: 같은 원문이 양쪽에 오르는 일이 잦다(오늘도 오픈 웨이트·Opus 5 관련 글이 겹쳤다). 원문 URL 정규화로 합치고 양쪽 점수를 함께 표시할지 결정한다.
- 지면 배분: 소스별 섹션으로 나눌지, 한 목록에 섞고 출처만 표기할지. 리브의 개요 패널(오늘의 강추·미니 목차)은 소스와 무관하게 하나로 유지하는 편이 읽기 흐름에 맞다.
- 언어: HN 은 영문이라 요약 부담이 커진다. 정리 모델은 동일하게 Opus 5.

파일럿 평가(task-78) 통과 후, GeekNews 단일 소스가 안정된 다음에 착수한다.
<!-- SECTION:DESCRIPTION:END -->
