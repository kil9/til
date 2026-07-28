---
id: TASK-113
title: 전체 페이지 detect 전수 스캔과 triage — 발행물 대량 리라이트 금지
status: To Do
assignee: []
created_date: '2026-07-28 16:25'
labels: []
milestone: m-12
dependencies:
  - TASK-112
priority: medium
ordinal: 7000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
index.html(갤러리)·404.html 과 2026/ 전체(53페이지)를 npx impeccable detect 로 전수 스캔한다. 자체 완결형 페이지가 많아 수 분 이상 걸리니 백그라운드로 돌린다. 규칙별로 집계한 뒤 (1) 갤러리·공용 자산은 수정, (2) 이미 발행된 개별 글은 가독성·명도 대비처럼 실해가 있는 것만 고치고 나머지는 inline ignore 로 waive 하거나 방치한다 — 발행물 대량 리라이트 작업을 만들지 않는다. 집계와 처리 방침은 backlog doc 으로 남긴다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 전수 스캔의 규칙별 집계와 처리 방침이 backlog doc 으로 남는다
- [ ] #2 갤러리(index.html)와 공용 자산이 detect 를 통과한다
- [ ] #3 기존 글 수정은 가독성·대비 등 실해가 있는 것으로 한정된다
<!-- AC:END -->
