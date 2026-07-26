---
id: TASK-79
title: 관심사 프로필 자동 추출
status: To Do
assignee: []
created_date: '2026-07-26 03:55'
labels:
  - solo
milestone: m-8
dependencies:
  - TASK-78
priority: medium
ordinal: 79000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
루트 index.html 의 카드 data-topic·.tag·제목에서 관심사 프로필을 뽑는 스크립트를 만든다. 파일럿에서는 손으로 뽑았다(AI 15·워크플로 10·하드웨어 7·터미널 5·시스템 3·경제 3·사이트 2·읽을거리 2 + 세부 축). 자동화하면 글이 쌓일수록 프로필이 따라 움직인다. 최근 글에 가중치를 주는 방식(예: 최근 3개월 2배)을 검토한다. 출력은 선별 프롬프트에 그대로 끼울 수 있는 텍스트/JSON.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 til 카드에서 주제 분포와 세부 축을 뽑는 스크립트가 있다
- [ ] #2 최근 글 가중 여부를 결정하고 근거를 남겼다
- [ ] #3 출력이 선별 단계 프롬프트에 그대로 들어가는 형태다
<!-- AC:END -->
