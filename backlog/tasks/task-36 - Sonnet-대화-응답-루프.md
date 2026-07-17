---
id: TASK-36
title: Sonnet 대화 응답 루프
status: To Do
assignee: []
created_date: '2026-07-17 20:30'
updated_date: '2026-07-17 20:31'
labels: []
milestone: m-2
dependencies:
  - TASK-34
  - TASK-35
priority: high
ordinal: 36000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
수신 메시지 + 스레드 맥락 + 리브 페르소나로 claude -p --model claude-sonnet-5 를 호출(구독 OAuth, API 키 미설정)해 스레드에 응답. TIL 근거 Q&A 동작.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 메시지+스레드 히스토리+페르소나로 claude -p --model claude-sonnet-5 호출, 응답을 스레드에 게시
- [ ] #2 구독 OAuth 로 동작(ANTHROPIC_API_KEY 미설정 확인) — 종량제로 안 넘어감
- [ ] #3 TIL 저장소 근거 Q&A(최근 글·특정 주제 등)가 동작
<!-- AC:END -->
