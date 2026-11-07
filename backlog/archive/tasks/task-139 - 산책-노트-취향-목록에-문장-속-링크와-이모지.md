---
id: TASK-139
title: 산책 노트 취향 목록에 문장 속 링크와 이모지
status: Done
assignee: []
created_date: '2026-10-23 16:07'
updated_date: '2026-10-23 16:21'
labels: []
milestone: m-15
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
관리자 요청(2026-10-24): 상단 '좋아하게 된 것' 등 취향 목록 문장에 출처 링크를 건다 — 딱딱한 출처 표기가 아니라 지금 문장 일부에 하이퍼링크만 단다. 노트 몇 개에는 어울리는 이모지를 앞이나 뒤에 하나 붙인다. notes.jsonl 은 덧붙이기 전용이라 표시용 꾸밈은 사이드카(liv-notes/decor.json)에 둔다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 취향 목록의 각 항목이 문장 속 구절 하나에 source.url 링크를 갖는다(구절이 원문에 있을 때만)
- [x] #2 기존 취향 노트 전부에 링크 구절이 백필되고 일부에 이모지가 붙는다
- [x] #3 산책 출력이 새 노트의 링크 구절·이모지를 내고 검증을 거쳐 decor.json 에 쌓인다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
취향 노트 59건에 문장 속 링크 구절을 백필(전부 원문 부분문자열 확인)하고 21건에 이모지. 표시층은 decor.json 사이드카(원본 덧붙이기 전용 유지). 산책 출력 link·emoji 필드 → apply-walk 가 원문 포함 여부·이모지 유니코드 범주를 검증. 실측 2026-10-24 산책: 6건 전부 링크 구절, 3건 이모지(37ae153).
<!-- SECTION:NOTES:END -->
