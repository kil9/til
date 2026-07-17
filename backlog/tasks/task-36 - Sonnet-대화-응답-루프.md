---
id: TASK-36
title: Sonnet 대화 응답 루프
status: Done
assignee: []
created_date: '2026-07-17 20:30'
updated_date: '2026-07-17 21:51'
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
- [x] #1 메시지+스레드 히스토리+페르소나로 claude -p --model claude-sonnet-5 호출, 응답을 스레드에 게시
- [x] #2 구독 OAuth 로 동작(ANTHROPIC_API_KEY 미설정 확인) — 종량제로 안 넘어감
- [x] #3 TIL 저장소 근거 Q&A(최근 글·특정 주제 등)가 동작
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
til-inbox bot/liv_daemon.py generate 로직 교체(커밋 2a1e002). claude -p --model claude-sonnet-5, persona.md 주입(--append-system-prompt), --output-format text, --no-session-persistence. 구독 OAuth: subprocess env 에서 ANTHROPIC_API_KEY 제거(실측 시 base 환경도 unset). 보안(decision-5): --allowedTools WebFetch WebSearch(조회 pre-approve) + --disallowedTools 로 Bash/Read/Agent 등 제거. 맥락: 스레드별 자체 트랜스크립트를 프롬프트 주입(#til 채널은 channels:history 스코프 없음). 동시성: placeholder→ThreadPoolExecutor(3)→chat.update. 검증(#til E2E): (1) 멘션 2턴 대명사 맥락 유지 확인, (2) 구독 OAuth 응답, (3) '최근 글' 질문에 WebFetch 로 실제 최신글 'LingBot-Map…'+정확 URL 조회. Bash 강제 시도 차단 재확인. 테스트 대화 삭제 정리.
<!-- SECTION:NOTES:END -->
