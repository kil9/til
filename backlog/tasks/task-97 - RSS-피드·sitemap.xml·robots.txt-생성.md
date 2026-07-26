---
id: TASK-97
title: RSS 피드·sitemap.xml·robots.txt 생성
status: To Do
assignee: []
created_date: '2026-07-26 10:23'
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
- [ ] #1 index.html 카드만으로 feed.xml·sitemap.xml·robots.txt 가 재생성되고, 스크립트를 두 번 돌려도 결과가 동일하다
- [ ] #2 브리핑 회차가 피드·sitemap 어디에도 들어가지 않는다
- [ ] #3 생성된 Atom·sitemap 이 XML 파싱을 통과하고 피드 리더에서 최신 글이 최신으로 뜬다
- [ ] #4 루트에 rel=alternate 링크와 사람이 클릭할 수 있는 피드 링크가 있다
- [ ] #5 AGENTS.md 퍼블리시 런북 §4 에 재생성 단계가 적혔다
<!-- AC:END -->
