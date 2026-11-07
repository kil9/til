---
id: TASK-135
title: 루트 목록 카드에 글별 원형 아이콘
status: Done
assignee: []
created_date: '2026-10-04 07:04'
updated_date: '2026-10-04 07:06'
labels: []
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
til.kil9.dev 루트 목록이 글씨뿐이라 단조롭다는 사용자 요청(2026-10-04). 카드 제목 왼쪽에 작은 원형 아이콘을 단다. 글마다 내용에 맞는 이모지, 회사·제품 글이면 로고(Simple Icons), 맞는 이모지가 없으면 직접 그린 SVG(예: 뿌요뿌요). 진실원본은 카드의 data-icon 속성 하나이고 /p/archive/ 도 같은 값을 읽는다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 루트 카드 116건 전부에 data-icon 이 있고 데스크톱·모바일(560px 이하) 모두 제목 왼쪽에 원형 아이콘이 보인다
- [x] #2 이미지 아이콘(로고·뿌요·리브)은 p/icons/ 사이드카로 두고, 라이트·다크 모드 모두 식별된다
- [x] #3 site-check.py 가 data-icon 누락과 없는 아이콘 파일을 위반으로 잡는다
- [x] #4 AGENTS.md 퍼블리시 런북에 새 글의 data-icon 규칙이 적혀 있다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
루트 카드 116건에 data-icon 을 달고 JS 가 제목 왼쪽 원형 배지로 그린다(데스크톱은 날짜|아이콘|제목 3칼럼, 560px 이하는 제목 앞 float). 이모지 위주, 회사·제품 글은 Simple Icons 로고(브랜드색 fill), 뿌요는 직접 그린 SVG, 리브 소개는 리브 아바타 — 그림 19종을 p/icons/ 사이드카(80KB)로 둔다. 배지 바탕은 두 모드 모두 밝은 회색이라 검정 로고가 다크에서도 보인다. site-check.py 에 check_icons 추가(누락·없는 파일). 검증: puppeteer 스크린샷 1280px 라이트·400px 다크 육안 확인, site-check 정상/음성(아이콘 삭제·없는 파일) 둘 다 확인, render-check 위반 없음, site-feed·search-index 재생성 diff 없음.
<!-- SECTION:NOTES:END -->
