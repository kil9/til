---
id: TASK-65
title: 스티커 파스텔 단독 운용 + 장식 기호 전면 삭제
status: Done
assignee: []
created_date: '2026-07-19 15:54'
updated_date: '2026-07-19 15:54'
labels:
  - sticker
dependencies: []
ordinal: 65000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
표시 크기에서 작은 장식 기호가 정체불명 얼룩으로 보여 18종 전부 재생성한다. 낙서풍 병용도 철회하고 파스텔 단독으로 간다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 18종 재생성, 장식 기호 0 (전구·물음표·느낌표 팻말 3컷만 큰 기호 1개)
- [ ] #2 낙서풍 legacy 이관 + 공개 페이지 단일 섹션 복원
- [ ] #3 AGENTS.md·doc-3 반영(병용 철회 경위 포함)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
grill 에서 '기호를 적극적으로 늘린다'로 정했던 것을 실물 보고 반전. 작은 장식 기호는 원본 크기에서만 귀엽고 128px 에서는 노이즈다 — doc-3 §4-6 의 '검수는 실제 표시 크기에서' 원칙이 기호에도 적용된다. 병용 철회로 공개 페이지는 828KB -> 663KB.
<!-- SECTION:NOTES:END -->
