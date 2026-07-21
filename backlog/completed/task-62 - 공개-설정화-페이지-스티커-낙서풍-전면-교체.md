---
id: TASK-62
title: 공개 설정화 페이지 스티커 낙서풍 전면 교체
status: Done
assignee: []
created_date: '2026-07-19 12:40'
updated_date: '2026-07-19 12:40'
labels:
  - sticker
dependencies: []
ordinal: 62000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
/p/liv-today/sheet/ 의 스티커 18칸을 stickers-doodle/ 세트로 교체한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 18칸 base64 교체 + 디코드 검증(WebP 헤더·md5 일치)
- [ ] #2 설명 문구에 크롭 변경 반영
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
18칸 전부 교체·검증 완료. 페이지 611KB→633KB. 구 세트는 공개 노출 없이 stickers/ 에 자산으로만 잔존.
<!-- SECTION:NOTES:END -->
