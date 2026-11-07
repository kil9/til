---
id: TASK-152
title: 갤러리 카드 제목이 글 페이지 제목으로 이어지는 페이지 전환
status: To Do
assignee: []
created_date: '2026-11-07T05:22:00Z'
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
- [ ] #1 루트 갤러리 카드 → 글 이동 때 카드 h2 가 글 h1 로 이어져 움직이고, 글에서 뒤로 가면 그 카드로 돌아간다
- [ ] #2 글 하단 이전/다음 이동은 짧은 페이드만 하고 레이아웃이 튀지 않는다
- [ ] #3 글 쪽 CSS 는 relink-pages.py 마커 구간으로 들어가 재실행이 멱등이다
- [ ] #4 prefers-reduced-motion: reduce 에서는 전환이 없고, 미지원 브라우저는 지금과 같다. site-check.py 통과
<!-- AC:END -->
