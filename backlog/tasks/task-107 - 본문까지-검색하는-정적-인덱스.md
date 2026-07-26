---
id: TASK-107
title: 본문까지 검색하는 정적 인덱스
status: To Do
assignee: []
created_date: '2026-07-26 10:25'
updated_date: '2026-07-26 15:48'
labels:
  - solo
milestone: m-11
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
루트 index.html 의 matches() 가 보는 것은 카드 텍스트 + href + data-topic 뿐이다. 즉 제목·한 줄 설명·태그까지만이고 본문은 못 본다. 50건 규모에선 '그 글 어디 있었지' 가 본문 키워드로 기억되는 경우가 많다. 발행 시 각 페이지 본문을 긁어 search-index.json(수십 KB 예상)을 만들고 검색이 그것까지 보게 한다. 지연 로딩(검색창 첫 입력 때 fetch)이면 초기 로딩에 영향이 없다. 색인 대상에서 코드 블록·base64 를 제외해야 인덱스가 터지지 않는다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 발행 파이프라인이 search-index.json 을 생성한다 — 갤러리 카드가 있는 페이지만 대상이고 p/briefing/ 회차는 제외한다
- [ ] #2 색인 텍스트에서 코드 블록·base64 data URI·script/style 을 제외해 인덱스가 비대해지지 않는다
- [ ] #3 루트 index.html 의 검색이 제목·설명·태그에 더해 본문까지 매치한다
- [ ] #4 인덱스는 검색창 첫 입력 시점에 지연 로딩되어 초기 페이지 로딩에 영향을 주지 않는다
- [ ] #5 본문 매치 시 카드 아래에 매치 구간 스니펫 한 줄을 키워드 강조와 함께 보여준다
- [ ] #6 인덱스가 없거나 fetch 에 실패해도 기존 카드 텍스트 검색으로 동작한다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
확정 사항(2026-07-27 승격 인터뷰):
- 결과 표시: 카드 아래 스니펫 한 줄 + 키워드 강조. 왜 걸렸는지 보이지 않으면 본문 검색의 값이 반감된다.
- 색인 범위: 갤러리 카드가 있는 페이지만. 브리핑 회차는 제외한다(매일 늘고 noindex 라 인덱스만 부풀린다) — feed.xml·sitemap 과 같은 기준이라 일관된다.

생성 위치는 다른 생성물(feed.xml·sitemap.xml·og/)과 같은 발행 재생성 단계에 얹는 것이 자연스럽다. 진실원본은 루트 index.html 카드.
<!-- SECTION:NOTES:END -->
