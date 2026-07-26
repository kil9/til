---
id: DRAFT-5
title: 본문까지 검색하는 정적 인덱스
status: Draft
assignee: []
created_date: '2026-07-26 10:25'
labels: []
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
루트 index.html 의 matches() 가 보는 것은 카드 텍스트 + href + data-topic 뿐이다. 즉 제목·한 줄 설명·태그까지만이고 본문은 못 본다. 50건 규모에선 '그 글 어디 있었지' 가 본문 키워드로 기억되는 경우가 많다. 발행 시 각 페이지 본문을 긁어 search-index.json(수십 KB 예상)을 만들고 검색이 그것까지 보게 한다. 지연 로딩(검색창 첫 입력 때 fetch)이면 초기 로딩에 영향이 없다. 색인 대상에서 코드 블록·base64 를 제외해야 인덱스가 터지지 않는다.
<!-- SECTION:DESCRIPTION:END -->
