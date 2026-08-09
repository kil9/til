---
id: TASK-123
title: 리브 문체 기준 컨텍스트 경량화
status: To Do
assignee: []
created_date: '2026-08-09 06:11'
labels:
  - solo
milestone: m-14
dependencies:
  - TASK-122
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
agent-first-docs 전체 HTML의 base64 이미지까지 모델 컨텍스트에 넣어 첫 실행이 272k 토큰을 사용한 경로를 줄인다. 워처가 도입부와 .liv 텍스트만 안전하게 추출해 프롬프트에 직접 제공하고, 모델에는 전체 HTML을 읽히지 않는다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 기준 HTML에서 data URI를 모델에 노출하지 않고 lede와 모든 .liv 문장을 추출한다
- [ ] #2 submit 프롬프트가 추출된 기준 문장을 포함하고 전체 agent-first-docs 파일 읽기를 요구하지 않는다
- [ ] #3 추출 실패 시 문체 지시를 잃지 않는 명시적 폴백이 있다
- [ ] #4 한글과 여러 .liv 블록을 포함한 테스트가 통과한다
<!-- AC:END -->
