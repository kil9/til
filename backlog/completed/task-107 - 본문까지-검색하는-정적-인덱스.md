---
id: TASK-107
title: 본문까지 검색하는 정적 인덱스
status: Done
assignee: []
created_date: '2026-07-26 10:25'
updated_date: '2026-07-26 16:00'
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
- [x] #1 발행 파이프라인이 search-index.json 을 생성한다 — 갤러리 카드가 있는 페이지만 대상이고 p/briefing/ 회차는 제외한다
- [x] #2 색인 텍스트에서 코드 블록·base64 data URI·script/style 을 제외해 인덱스가 비대해지지 않는다
- [x] #3 루트 index.html 의 검색이 제목·설명·태그에 더해 본문까지 매치한다
- [x] #4 인덱스는 검색창 첫 입력 시점에 지연 로딩되어 초기 페이지 로딩에 영향을 주지 않는다
- [x] #5 본문 매치 시 카드 아래에 매치 구간 스니펫 한 줄을 키워드 강조와 함께 보여준다
- [x] #6 인덱스가 없거나 fetch 에 실패해도 기존 카드 텍스트 검색으로 동작한다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
확정 사항(2026-07-27 승격 인터뷰):
- 결과 표시: 카드 아래 스니펫 한 줄 + 키워드 강조. 왜 걸렸는지 보이지 않으면 본문 검색의 값이 반감된다.
- 색인 범위: 갤러리 카드가 있는 페이지만. 브리핑 회차는 제외한다(매일 늘고 noindex 라 인덱스만 부풀린다) — feed.xml·sitemap 과 같은 기준이라 일관된다.

생성 위치는 다른 생성물(feed.xml·sitemap.xml·og/)과 같은 발행 재생성 단계에 얹는 것이 자연스럽다. 진실원본은 루트 index.html 카드.

완료(2026-07-27):
- backlog/assets/search-index.py 신설 — 카드가 있는 페이지 본문을 긁어 루트 search-index.json(51건, 556KB / gzip 210KB)을 굽는다. <main> 안에서 script·style·pre·code·nav·footer·상단 복귀 링크를 걷어내고 태그를 지워 base64 속성값까지 함께 사라진다. 시각 함수 미사용으로 멱등.
- 색인 용량 경고 임계 1MB(stderr, 발행은 막지 않음). 상한이 아니라 '코드 블록 제외가 깨졌다'를 잡는 사고 감지용 — 본문 증가만으로는 약 2배 여유가 있다.
- index.html: matches() 를 matchInfo() 로 바꿔 카드 텍스트로 못 찾은 토큰만 본문에서 다시 찾는다. 본문에서 걸린 경우에만 카드 아래 .snippet 한 줄을 붙이고 <mark> 로 강조하며, 스니펫 창은 '카드에 없던 토큰' 위치를 중심으로 자른다(카드에 이미 보이는 단어를 되보여 주면 왜 걸렸는지가 설명되지 않는다).
- 지연 로딩: 검색창 첫 입력(또는 ?q= 딥링크) 때 한 번만 fetch. 로딩 중에는 '결과 없음'을 띄우지 않는다.
- 검증(헤드리스 Firefox + geckodriver, 로컬 서버): 기본 로드 시 색인 요청 0건·카드 10건 / 본문 전용 어절 '스파게티를' → 1건 + 스니펫·mark / 카드로 충족되는 질의는 스니펫 없음 / 색인 404 환경에서 카드 검색은 그대로 동작하고 본문 전용 어절은 '결과 없음' / 다중 토큰 AND 는 카드+본문에 걸쳐 매치.
- 런북 §4 에 재생성 단계 추가(AGENTS.md), README 명령 목록·구조 목록 갱신.
<!-- SECTION:NOTES:END -->
