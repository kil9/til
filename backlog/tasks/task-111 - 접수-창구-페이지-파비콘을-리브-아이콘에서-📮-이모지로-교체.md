---
id: TASK-111
title: "접수 창구 페이지 파비콘을 리브 아이콘에서 \U0001F4EE 이모지로 교체"
status: In Progress
assignee: []
created_date: '2026-07-26 18:39'
updated_date: '2026-07-26 18:42'
labels: []
dependencies: []
priority: low
ordinal: 5000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
p/submit-96a2d1c7e19e8a09/index.html 은 리브 원형 아이콘 파비콘(전 페이지 공통 base64 WebP)을 쓰고 있는데, 이 페이지만 성격이 다르다. 콘텐츠 페이지가 아니라 제출 폼이라 브라우저 탭에서 til 본문 페이지와 구분되는 편이 낫다. 리브 얼굴 대신 우편함 이모지(📮)를 파비콘으로 쓴다.

접근: SVG data URI 파비콘(<svg xmlns=...><text y=".9em" font-size="90">📮</text></svg>)으로 <link rel="icon"> 을 교체한다. 외부 파일을 만들지 않아 단일 파일 원칙(AGENTS.md §2)을 지킨다. 이 페이지는 갤러리 카드가 없어 relink-pages.py 의 og:image 대상이 아니므로 재생성 스크립트와 충돌하지 않는다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 p/submit-96a2d1c7e19e8a09/index.html 의 rel="icon" 이 📮 를 담은 SVG data URI 로 바뀌고, 리브 파비콘 base64 는 그 자리에서 사라진다
- [ ] #2 브라우저(또는 로컬 http.server)에서 해당 페이지를 열어 탭 아이콘이 우편함으로 보이는 것을 확인한다
- [x] #3 다른 페이지(루트 index.html·아티클·p/ 하위)의 리브 파비콘은 변경되지 않는다
- [x] #4 python3 backlog/assets/site-check.py 가 통과한다
<!-- AC:END -->
