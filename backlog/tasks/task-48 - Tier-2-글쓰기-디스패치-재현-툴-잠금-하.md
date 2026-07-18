---
id: TASK-48
title: Tier-2 글쓰기 디스패치 재현 (툴 잠금 하)
status: To Do
assignee: []
created_date: '2026-07-18 05:55'
labels: []
milestone: m-4
dependencies:
  - TASK-46
priority: medium
ordinal: 48000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
리브 LLM 은 읽기전용이라 gh 를 직접 못 쓴다(TASK-46). 글쓰기 요청(!til/자연어) 감지 → til-inbox pending 이슈 생성을 hermes 에서 어떻게 할지 설계·구현. LLM 은 신호만 뱉고 이슈 생성은 데몬/훅/제한 커스텀 skill 코드가 수행(인젝션으로 이슈 조작 불가).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 글쓰기 요청 감지(명시 커맨드 + 자연어) → til-inbox pending 이슈 생성 경로 구현(제한 커스텀 skill 또는 외부 훅)
- [ ] #2 게시 트리거는 사이트 주인만(owner 게이트) 유지, 비주인 거절
- [ ] #3 리브 LLM 이 GitHub 접근 툴을 직접 갖지 않음(디스패치는 코드가 수행)
<!-- AC:END -->
