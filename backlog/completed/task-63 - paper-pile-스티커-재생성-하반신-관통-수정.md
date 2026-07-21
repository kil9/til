---
id: TASK-63
title: paper-pile 스티커 재생성 (하반신 관통 수정)
status: Done
assignee: []
created_date: '2026-07-19 12:48'
updated_date: '2026-07-19 12:48'
labels:
  - sticker
dependencies: []
ordinal: 63000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
낙서풍 paper-pile 컷이 종이 더미를 캐릭터 뒤에만 깔고 다리를 그 앞에 얹어, 파묻힌 게 아니라 종이 앞에 서 있는 것으로 읽혔다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 하반신이 더미에 완전히 가려지고 다리·발이 보이지 않음
- [ ] #2 512/256 자산 + 공개 설정화 페이지 반영
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
gen.sh 에 buried 크롭 모드를 추가해 재생성. '소품 더미가 허리 아래를 통째로 덮어 가리고 그 더미가 스티커 아랫부분을 이루어 실루엣을 닫는다' + '다리·바지·발을 아예 그리지 않는다(조금이라도 보이면 실패)' 부정형이 필요했다. 파묻힘 계열은 소품이 캐릭터를 가린다는 것을 명시하지 않으면 소품을 배경으로 깔고 캐릭터를 그 앞에 세운다.
<!-- SECTION:NOTES:END -->
