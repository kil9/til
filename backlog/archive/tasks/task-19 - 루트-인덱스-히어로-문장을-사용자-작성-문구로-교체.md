---
id: TASK-19
title: 루트 인덱스 히어로 문장을 사용자 작성 문구로 교체
status: Done
assignee: []
created_date: '2026-07-17 06:22'
updated_date: '2026-07-17 06:40'
labels:
  - solo
dependencies: []
ordinal: 19000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
index.html 히어로의 .site-intro(index.html:224 부근) 문장을 사용자가 직접 쓴 다음 문구로 교체한다: '매일 새로운 지식을 AI 큐레이터가 조사하고 정리합니다.' 기존 문장은 폐기한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 .site-intro 텍스트가 '매일 새로운 지식을 AI 큐레이터가 조사하고 정리합니다.' 로 교체된다
- [x] #2 히어로의 다른 요소(제목·레이아웃)는 변경되지 않는다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
index.html .site-intro 를 사용자 작성 문구로 교체. 제목·레이아웃 불변, 헤드리스 렌더 확인.
<!-- SECTION:NOTES:END -->
