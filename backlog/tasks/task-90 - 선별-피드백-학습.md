---
id: TASK-90
title: 선별 피드백 학습
status: To Do
assignee: []
created_date: '2026-07-26 07:28'
labels:
  - solo
milestone: m-9
dependencies:
  - TASK-85
  - TASK-79
priority: medium
ordinal: 90000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
관심사 프로필을 til 분포(task-79)만으로 뽑으면 실제 반응이 반영되지 않는다. 브리핑에 '이건 왜 넣었냐 / 이건 왜 뺐냐' 를 한 번 눌러 남길 수 있게 하고, 그 이력을 다음 브리핑의 선별 프롬프트에 넣는다.

주의: 피드백이 쌓일수록 프롬프트가 길어지므로 원문을 다 넣지 말고 축약된 규칙 형태로 정리해 유지한다(예: '프론트엔드 빌드 도구 소개는 뺀다', 'Show GN 자작 도구는 가중치 올린다'). 규칙 수에 상한을 두고 오래된 것은 만료시킨다. 하단 '훑고 넘긴 것' 쪽에도 같은 피드백 경로를 둔다 — 거기서 건진 것이 가장 값진 신호다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 브리핑에서 항목별로 선별 피드백을 남길 수 있다
- [ ] #2 피드백이 축약된 규칙으로 정리돼 저장된다
- [ ] #3 다음 브리핑의 선별 프롬프트가 그 규칙을 반영한다
- [ ] #4 규칙 수에 상한과 만료가 있어 프롬프트가 무한정 길어지지 않는다
<!-- AC:END -->
