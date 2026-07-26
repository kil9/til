---
id: TASK-87
title: 사이트 진입점과 브리핑 아카이브
status: To Do
assignee: []
created_date: '2026-07-26 07:27'
labels:
  - solo
milestone: m-9
dependencies:
  - TASK-81
priority: medium
ordinal: 87000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
브리핑을 사이트에서 찾아갈 수 있게 한다. 루트 index.html 사이드바에 '오늘의 브리핑' 링크 한 줄을 추가하되(리브 소개 블록 근처), 루트 갤러리 카드에는 넣지 않는다. p/briefing/archive/ 에 날짜별 목록을 두어 과거분을 훑을 수 있게 한다.

정리할 것: 보존 기간(무기한 누적 vs N일 후 정리), sitemap·robots 처리, 404.html 리다이렉트 맵 등록 여부, 그리고 브리핑 페이지가 검색엔진에 til 본문 글보다 많이 잡히지 않게 할지. 매일 1건이라 1년이면 365 디렉터리가 되므로 이 판단을 미루면 나중에 되돌리기 어렵다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 루트 사이드바에서 오늘의 브리핑으로 갈 수 있다
- [ ] #2 p/briefing/archive/ 에서 과거 브리핑을 날짜로 찾을 수 있다
- [ ] #3 보존 기간과 검색엔진 노출 정책이 정해져 문서에 적혔다
<!-- AC:END -->
