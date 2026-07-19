---
id: TASK-69
title: 설정화 외출복 2컷 라벨 OL 폐기 (접수원·회사원)
status: Done
assignee: []
created_date: '2026-07-19 16:30'
updated_date: '2026-07-19 16:30'
labels:
  - sheet
dependencies: []
ordinal: 69000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
공개 설정화 페이지 SD 섹션의 외출복 2컷 라벨이 "OL 룩"·"OL 룩 (카디건)" 이었다. 한국어에서 쓰이지 않는 표현이라 사용자 지정으로 폐기한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 공개 라벨이 각각 "접수원"·"회사원"
- [ ] #2 doc-3 컷 표와 공개 라벨 규칙 반영
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
블라우스+H라인 스커트+스카프 판이 접수원, 셔츠+블루 카디건 판이 회사원이다.

바꾼 것은 공개 라벨과 doc-3 표뿐이다. 파일명(`sheet-chibi-ol.webp`·`-ol-cardigan`)과 스티커 복장 배분 표기("OL 7/후디 11")는 내부용이라 그대로 뒀다 — 파일명은 페이지 임베드가 base64 라 URL 에 박히지는 않지만, 태스크 이력·doc-3 곳곳이 이 이름으로 서로를 가리키고 있어 개명 이득보다 churn 이 크다.
<!-- SECTION:NOTES:END -->
