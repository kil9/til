---
id: TASK-115
title: 긴 글 목차를 본문 왼쪽 sticky 레일로
status: Done
assignee: []
created_date: '2026-07-28 17:13'
updated_date: '2026-07-28 18:27'
labels: []
dependencies: []
priority: medium
ordinal: 9000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
TASK-108 이 넣은 목차(.pagetoc)는 첫 h2 앞 인라인 블록이라 스크롤하면 사라진다. 넓은 화면에서는 본문 왼쪽 여백에 sticky 레일로 붙여 글 내내 위치를 보여준다.

접근(인터뷰 확정):
- 배치: 본문 main(max-width 720px 중앙 정렬)은 그대로 두고, 레일만 왼쪽 빈 여백에 fixed/absolute 로 띄운다. 기존 페이지 레이아웃을 건드리지 않고, 폭이 모자라면 자동으로 걷히게 하기 쉽다.
- 동작: sticky 로 스크롤을 따라가며 IntersectionObserver 짧은 인라인 스크립트로 현재 절을 액센트 하이라이트.
- 좁은 화면: 레일 폭이 안 나오면 지금의 인라인 목차(첫 h2 앞 블록)로 폴백. 마크업 하나를 CSS 로 두 모습으로 쓰거나 두 벌을 내보낸다.
- 생성 자리는 backlog/assets/relink-pages.py 의 PAGETOC_CSS·TOC_MARK/TOC_CSS_MARK 구간이고 마커 밖은 건드리지 않아 재실행 멱등이어야 한다. 대상 조건(h2 5개 이상 아티클)은 그대로.
- 단일 파일 원칙상 CSS·JS 는 마커 구간에 인라인. DESIGN.md 에 새 색·크기를 도입하면 같은 커밋에서 갱신한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 넓은 화면에서 목차가 본문 왼쪽 여백에 sticky 레일로 표시되고, 본문 max-width·중앙 위치는 변하지 않는다
- [x] #2 스크롤에 따라 현재 읽는 절이 레일에서 액센트로 하이라이트된다
- [x] #3 레일 폭이 안 나오는 좁은 화면에서는 기존 인라인 목차로 폴백하고 목차가 사라지지 않는다
- [x] #4 relink-pages.py 를 두 번 돌려도 결과가 같고(멱등), 마커 밖 마크업은 변하지 않는다
- [x] #5 라이트·다크 모두에서 대비가 맞고, 목차 대상 아티클 전체를 재생성한 뒤 site-check.py 가 통과한다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
구현: relink-pages.py 의 PAGETOC_CSS 에 @media (min-width: 1200px) 레일 블록 추가, toc_html 에 .pagetoc-inner 래퍼와 하이라이트 스크립트(PAGETOC_JS) 추가. 56개 아티클 재생성.

설계 결정 셋(전부 근거를 코드 주석에 남겼다):
- position: fixed 가 아니라 main 기준 absolute 박스(top:0/bottom:0)를 본문 높이만큼 늘리고 그 안을 sticky(top:48px). fixed 면 본문이 끝난 뒤 footer·하단 내비 구간까지 레일이 따라온다.
- 셀렉터를 'main > .pagetoc' 으로 한정. <main> 이 없는 페이지(2026-07-plan-pipeline 1편)에서 absolute 를 걸면 기준이 body 로 올라가 레일이 엉뚱한 자리에 뜬다. 그 페이지는 인라인 목차로 남는 것을 실측 확인했다.
- 마크업 두 벌이 아니라 한 벌 + CSS. 두 벌이면 같은 절 제목이 search-index.py 색인에 중복으로 들어간다.

검증(headless puppeteer 로 실제 렌더 측정, 4페이지 x 5조건):
- 1440/1280: pos=absolute, inner=sticky, stickyTop=48, 본문과 겹침 없음, 화면 밖으로 안 나감(1280 에서 left=56).
- 1199/700: pos=static 인라인 블록 폴백, 목차 사라지지 않음.
- 현재 절 하이라이트: 라이트 #1A5FC8 / 다크 #82B1F0, 나머지는 muted.
- 멱등: relink-pages.py 2회 실행 후 전 페이지 md5 동일. diff 에 삭제 라인이 없어 마커 밖 무변경 확인.

대비 사고 하나 잡았다: 처음에 레일 링크를 --tc-faint 로 뒀는데 13px 라이트에서 4.38:1 로 AA 미달이었다(task-113 에서 막 고친 부류를 새로 만들 뻔했다). --tc-muted 로 올려 7.05:1 / 8.45:1 확보.

DESIGN.md 갱신: Layout 반응형 분기에 1200px 추가, Components 에 목차 시그니처 컴포넌트 절 추가(세 함정 포함). 사이드카 breakpoints 에 toc-rail.
site-check.py 통과, impeccable detect 는 레일 관련 findings 0.
<!-- SECTION:NOTES:END -->
