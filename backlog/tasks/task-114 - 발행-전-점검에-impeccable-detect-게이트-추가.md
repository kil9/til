---
id: TASK-114
title: 발행 전 점검에 impeccable detect 게이트 추가
status: To Do
assignee: []
created_date: '2026-07-28 16:25'
labels: []
milestone: m-12
dependencies:
  - TASK-112
priority: medium
ordinal: 8000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
발행 전 자동 점검(TASK-109 로 완료된 canonical·링크·용량 점검)에 새 페이지 디렉터리 대상 npx impeccable detect 를 게이트로 추가해 신규 페이지부터 0 failures 를 기본으로 한다. advisory(em-dash 등)는 발행을 막지 않는다 — advisory 는 exit code 에 반영되지 않으므로 failures 만 기준으로 삼으면 된다. 점검 스크립트가 til repo 쪽에 있으면 여기서, /publish-til 스킬 쪽 변경이 필요하면 skills repo(~/work/skills)에서 커밋한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 발행 플로에 detect 게이트가 들어가 신규 페이지가 0 failures 여야 발행된다
- [ ] #2 advisory 는 발행을 막지 않는다
<!-- AC:END -->
