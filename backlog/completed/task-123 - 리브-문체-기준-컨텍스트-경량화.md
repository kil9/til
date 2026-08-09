---
id: TASK-123
title: 리브 문체 기준 컨텍스트 경량화
status: Done
assignee: []
created_date: '2026-08-09 06:11'
updated_date: '2026-08-09 06:21'
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
- [x] #1 기준 HTML에서 data URI를 모델에 노출하지 않고 lede와 모든 .liv 문장을 추출한다
- [x] #2 submit 프롬프트가 추출된 기준 문장을 포함하고 전체 agent-first-docs 파일 읽기를 요구하지 않는다
- [x] #3 추출 실패 시 문체 지시를 잃지 않는 명시적 폴백이 있다
- [x] #4 한글과 여러 .liv 블록을 포함한 테스트가 통과한다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
구현: stdlib HTMLParser 기반 extract-style-reference.py가 명시 .lede 또는 h1 뒤 첫 본문과 모든 .liv 문장을 텍스트로만 추출한다. 워처는 이 1.25KB 발췌를 프롬프트에 넣고, 실패하면 내장 문체 요약을 사용한다. 테스트 fixture의 한글·중첩 태그·다중 코멘트·SECRET_BASE64 비노출과 실제 agent-first-docs 발췌를 검증했다. til-inbox 327c711.
<!-- SECTION:NOTES:END -->
