---
id: TASK-97
title: RSS 피드·sitemap.xml·robots.txt 생성
status: Done
assignee: []
created_date: '2026-07-26 10:23'
updated_date: '2026-07-26 10:59'
labels: []
milestone: m-11
dependencies: []
priority: high
ordinal: 97000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
루트에 feed.xml·sitemap.xml·robots.txt 가 전부 없어 발행물이 사이트 밖으로 나가는 경로가 없다. 루트 index.html 의 갤러리 카드(href·data-date·data-topic·제목·설명)를 진실원본 삼아 세 파일을 생성하는 스크립트를 backlog/assets/ 에 두고, 발행 런북(§4 목록 갱신)에 실행 단계를 넣는다.

- 피드는 Atom 1.0. 항목은 아티클(<YYYY>/<slug>/)과 공개 지원 페이지만. p/briefing/ 은 noindex 정책이라 피드·sitemap 양쪽에서 제외한다.
- 본문 전문을 싣지 않고 카드 설명을 summary 로 낸다(페이지가 자체 완결형 HTML 이라 본문 추출이 지저분하고, 용량도 커진다).
- 발행 시각은 data-date 값(YYYY-MM-DDTHH:MM)에 KST 오프셋을 붙여 쓴다.
- robots.txt 는 전체 허용 + Sitemap 줄. 브리핑 경로는 Disallow 하지 않는다(noindex, follow 를 이미 meta 로 주고 있고, Disallow 하면 크롤러가 meta 를 읽지 못해 오히려 색인될 수 있다).
- 루트 index.html 에 <link rel="alternate" type="application/atom+xml"> 를 넣고 사이드바에 피드 링크를 노출한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 index.html 카드만으로 feed.xml·sitemap.xml·robots.txt 가 재생성되고, 스크립트를 두 번 돌려도 결과가 동일하다
- [x] #2 브리핑 회차가 피드·sitemap 어디에도 들어가지 않는다
- [x] #3 생성된 Atom·sitemap 이 XML 파싱을 통과하고 피드 리더에서 최신 글이 최신으로 뜬다
- [x] #4 루트에 rel=alternate 링크와 사람이 클릭할 수 있는 피드 링크가 있다
- [x] #5 AGENTS.md 퍼블리시 런북 §4 에 재생성 단계가 적혔다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
루트 index.html 카드를 진실원본으로 삼는 공용 파서 backlog/assets/sitelib.py 와 생성기 backlog/assets/site-feed.py 를 추가했다. 생성물은 feed.xml(Atom 1.0)·sitemap.xml·robots.txt.

- 시각 함수를 안 써서 두 번 돌려도 바이트가 같다(멱등).
- 브리핑은 카드가 없어 구조적으로 못 들어간다. 갤러리 미링크 페이지(herdr-pane-tradeoffs-anime)도 같은 이유로 빠진다.
- robots.txt 는 전체 허용 + Sitemap 줄. 브리핑을 Disallow 하지 않는다 — 크롤러가 페이지를 못 읽으면 meta noindex 도 못 읽어 오히려 URL-only 색인이 될 수 있다.
- 검증: 두 번 실행 후 동일, xml.etree 파싱 통과, 엔트리 50건 발행 내림차순, 피드·sitemap 의 고유 URL 52건 전부 로컬 서버에서 200.
- Fable 자문 결과 CARD_RE 가 카드 속성 순서·개수를 고정해 속성이 하나만 늘어도 무증상 탈락한다는 지적을 받아, 여는 태그를 통으로 잡고 속성을 따로 뽑는 방식으로 바꾸고 여는 태그 개수와 파싱 건수를 대조하는 가드를 넣었다.
<!-- SECTION:NOTES:END -->
