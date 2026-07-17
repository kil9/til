---
id: TASK-38
title: Tier-2 조사+글쓰기 디스패치 (Fable·서브에이전트·별도 잡)
status: To Do
assignee: []
created_date: '2026-07-17 20:30'
updated_date: '2026-07-17 20:31'
labels: []
milestone: m-2
dependencies:
  - TASK-36
priority: medium
ordinal: 38000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
글쓰기 요청을 대화 감지와 명시 커맨드 둘 다로 받아 Fable 조사·집필 잡을 별도 프로세스로 비동기 시작. 산출물은 공개 TIL 게시(기존 fable /publish-til 파이프라인 재사용). 시작·완료 Slack 통지.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 명시 커맨드(!til, /publish-til, !publish-til)와 대화 감지 둘 다로 글쓰기 요청 트리거
- [ ] #2 Fable 잡을 별도 프로세스로 비동기 시작(대화 턴 블로킹 안 함), 조사 서브에이전트 팬아웃 후 리브 문체로 집필
- [ ] #3 산출물은 공개 TIL 게시(기존 fable /publish-til 파이프라인 재사용)
- [ ] #4 시작·완료(게시 URL) Slack 통지
<!-- AC:END -->
