---
id: TASK-88
title: 팔로업 패널 (어제 이후의 후속)
status: To Do
assignee: []
created_date: '2026-07-26 07:27'
labels:
  - solo
milestone: m-9
dependencies:
  - TASK-85
  - TASK-82
priority: medium
ordinal: 88000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
브리핑을 1회성에서 연속물로 만든다. 오늘의 개요 패널 아래에 2-3행으로 (1) 어제 이후 TIL 만들기로 접수된 건의 처리 상태와 완성된 페이지 링크, (2) 지난 브리핑에 실었던 항목의 후속 소식(그 프로젝트가 v2 를 냈다, 그 주장이 반박됐다 등)을 보여 준다.

데이터 출처는 til-inbox 이슈 상태와 이전 브리핑의 state 파일이다. 파일럿 때는 데이터가 없어 보류했던 항목이며(Fable 자문 C안), 발행이 며칠 쌓인 뒤에 착수한다. 빈 날에는 패널 자체를 렌더링하지 않는다 — 매일 '없음'이 찍히면 그 자리가 죽는다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 전날 이후 접수된 TIL 요청의 상태가 브리핑에 보인다
- [ ] #2 완성된 til 페이지로 바로 갈 수 있다
- [ ] #3 보여 줄 것이 없는 날에는 패널이 아예 렌더링되지 않는다
<!-- AC:END -->
