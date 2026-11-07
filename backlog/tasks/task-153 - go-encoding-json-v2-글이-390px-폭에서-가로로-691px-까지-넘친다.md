---
id: TASK-153
title: go-encoding-json-v2 글이 390px 폭에서 가로로 691px 까지 넘친다
status: To Do
assignee: []
created_date: '2026-11-07T05:57:00Z'
labels: []
dependencies: []
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
TASK-150 검증(2026-11-07) 중 발견. puppeteer 390x844 에서 documentElement.scrollWidth=691. 오늘 작업 전 커밋 6d17391 의 같은 파일도 691 이라 기존 결함이다. overflow 로 잘리지 않은 요소 중 오른쪽 끝이 392 를 넘는 것은 찾지 못했다 — 의사 요소·긴 단어·표 폭 등을 의심. 다른 글에도 같은 패턴이 있는지 함께 본다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 go-encoding-json-v2 가 390px 폭에서 scrollWidth 가 390 이하다
- [ ] #2 같은 원인을 가진 다른 글을 찾아 함께 고치거나, 없음을 notes 에 남긴다
<!-- AC:END -->
