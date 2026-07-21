---
id: TASK-67
title: 전구 컷 후디 앞주머니 색 교정
status: Done
assignee: []
created_date: '2026-07-19 16:14'
updated_date: '2026-07-19 16:14'
labels:
  - sticker
dependencies: []
ordinal: 67000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
idea-bulb 컷의 후디 앞주머니가 네이비로 칠해졌다. 프롬프트 괄호 안에 색과 부위를 나열해 생성기가 오독한 것이 원인.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 앞주머니가 후디 몸통과 같은 파우더 블루
- [ ] #2 512/256 자산 + 공개 페이지 반영(전수 검증)
- [ ] #3 doc-3 에 프롬프트 문구 함정 기록
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
'연한 파우더 블루 후디(진한 블루 #1A5FC8 끈, 앞주머니, 살짝 오버사이즈)' 라는 문구를 생성기가 '진한 블루인 끈과 앞주머니'로 읽었다. 색과 부위를 한 괄호에 나열하지 말고 문장을 끊어 쓴다. TASK-66 검수 때 이것을 하의 네이비로 오독해 정상으로 넘긴 것도 실수였다 — 하의만 보고 상의를 안 본 탓.
<!-- SECTION:NOTES:END -->
