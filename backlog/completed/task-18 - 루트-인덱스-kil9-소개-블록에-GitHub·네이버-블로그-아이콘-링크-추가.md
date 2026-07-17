---
id: TASK-18
title: 루트 인덱스 kil9 소개 블록에 GitHub·네이버 블로그 아이콘 링크 추가
status: Done
assignee: []
created_date: '2026-07-17 06:22'
updated_date: '2026-07-17 06:39'
labels:
  - solo
dependencies: []
ordinal: 18000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
index.html 사이드바 .human 블록(현재 링크 없음, index.html:459 부근)에 https://github.com/kil9 와 https://blog.naver.com/pas2v 로 가는 작은 아이콘 링크 2개를 추가한다. 아이콘은 공식 로고 형상(GitHub 옥토캣 마크, 네이버 N 로고)을 단순화한 인라인 SVG 로 넣는다(외부 리소스 금지). 기본 색은 무채색(--text-faint 계열), hover/focus 시 액센트 컬러. fill 에 CSS 변수를 써 다크모드 자동 대응.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 kil9 블록에 GitHub·네이버 블로그 아이콘 링크 2개가 인라인 SVG 로 추가되고 각각 올바른 URL 로 연결된다
- [x] #2 아이콘은 기본 무채색·hover/focus 시 액센트이며 라이트/다크 모두 자연스럽다
- [x] #3 각 링크에 aria-label 등 접근 가능한 이름이 있다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
index.html .human 블록에 GitHub·네이버 블로그 인라인 SVG 아이콘 링크 추가. fill: var(--text-faint), hover/focus 시 var(--accent), focus-visible 아웃라인 포함. 헤드리스 Firefox 다크모드 렌더 확인.
<!-- SECTION:NOTES:END -->
