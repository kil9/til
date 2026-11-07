---
id: TASK-152
title: 갤러리 카드 제목이 글 페이지 제목으로 이어지는 페이지 전환
status: Done
assignee: []
created_date: '2026-11-07T05:22:00Z'
updated_date: '2026-11-07T05:27:00Z'
labels: []
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
사용자 요청(2026-11-07) 모션그래픽 도입의 두 번째. 카드를 눌러 글로 갈 때 누른 카드 제목이 글의 h1 자리로 옮겨 가 어느 글로 들어왔는지 이어 보이게 한다(뒤로 가기는 역방향). 교차 문서 View Transitions(@view-transition navigation:auto + pageswap/pagereveal). 글 쪽 CSS 는 relink-pages.py 가 관리하는 마커 구간에 넣어 136개 페이지에 소급하고 새 글에도 자동으로 붙게 한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 루트 갤러리 카드 → 글 이동 때 카드 h2 가 글 h1 로 이어져 움직이고, 글에서 뒤로 가면 그 카드로 돌아간다
- [x] #2 글 하단 이전/다음 이동은 짧은 페이드만 하고 레이아웃이 튀지 않는다
- [x] #3 글 쪽 CSS 는 relink-pages.py 마커 구간으로 들어가 재실행이 멱등이다
- [x] #4 prefers-reduced-motion: reduce 에서는 전환이 없고, 미지원 브라우저는 지금과 같다. site-check.py 통과
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
교차 문서 View Transitions. 글 135건에 relink-pages.py 의 새 PAGEVT 구간(</head> 직전, style+script)으로 소급했고 재실행 시 갱신 0건(멱등). 이름(page-title)은 루트에서 오가는 때만 붙인다: 글은 pagereveal 에서 activation.from 이 루트일 때, pageswap 에서 목적지가 루트이고 h1 이 화면 안일 때. 루트는 index.html 에서 그 글의 카드가 보이고 화면 안일 때만 h2 에 붙이고, 돌아올 때 카드 정렬·숨김이 끝난 뒤 그리도록 rel=expect blocking=render(#gallery-ready). 이전/다음은 이름 없이 root 160ms 페이드 — 아래쪽 링크에서 넘어가면 화면 밖 h1 이 날아오기 때문. DESIGN.md 에 Motion 절 추가. 검증: puppeteer(Chrome 151) 로 루트→글→다음 글→뒤로→뒤로를 1280·390 × reduced-motion 두 값으로 돌려 이벤트 로그 확인(루트↔글만 h1/h2 이름, 글↔글 없음, reduce 는 전환 자체 없음), 재생 속도 0.08 로 중간 화면 캡처, pageerror 없음. site-check.py·render-check.mjs 위반 없음.
<!-- SECTION:NOTES:END -->
