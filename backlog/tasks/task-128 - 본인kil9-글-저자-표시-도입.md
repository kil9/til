---
id: TASK-128
title: 본인(kil9) 글 저자 표시 도입
status: In Progress
assignee: []
created_date: '2026-09-19 10:26'
labels: []
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
til 의 모든 글이 리브 명의였다. 글쓰기 워크플로(topics→drafts)에서 나온 사용자 본인 글이 처음 게시되므로 리브 글과 구분되는 저자 표시를 만든다. 사이드바 .human 의 kil9 도트 아바타를 재사용한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 카드에 data-author 속성이 있으면 루트 갤러리 카드에 kil9 아바타가 붙는다
- [ ] #2 p/archive 격자에도 같은 표시가 붙는다
- [ ] #3 본인 글 페이지 바이라인 마크업(.byline + 아바타)이 AGENTS.md 와 DESIGN.md 에 문서화된다
- [ ] #4 feed.xml 의 해당 entry author 가 kil9 로 나간다
- [ ] #5 site-check.py 통과, render-check 로 루트·아카이브 확인
<!-- AC:END -->
