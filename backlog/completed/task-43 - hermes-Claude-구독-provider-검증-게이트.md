---
id: TASK-43
title: hermes Claude 구독 provider 검증 (게이트)
status: Done
assignee: []
created_date: '2026-07-18 05:54'
updated_date: '2026-07-18 06:09'
labels:
  - solo
milestone: m-4
dependencies: []
priority: high
ordinal: 43000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
B 전체의 게이트. hermes anthropic provider 가 ~/.claude/.credentials.json 구독 OAuth 로 돌고 실제로 구독 한도로 청구되는지(종량제 sk-ant-api 로 안 넘어가는지) 라이브 1회 검증. kobo 조사상 코드 의도는 구독 지원(claude-code 별칭·CLAUDE_CODE_OAUTH_TOKEN·credentials 직접 읽기)이나 청구 반영은 미검증.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 임시/격리 hermes 프로필에서 anthropic provider 를 구독 자격증명(~/.claude/.credentials.json 또는 OAuth setup-token)으로 구성해 응답 생성 성공
- [x] #2 그 호출이 구독으로 소모되고 종량제 API 키 경로로 넘어가지 않음을 확인(auth 모드·사용량 근거)
- [ ] #3 종량제로만 가능하다고 판명되면 근거를 기록하고 이 마일스톤 전체를 Blocked 로 전환
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
게이트 PASS (2026-07-18). hermes anthropic provider 가 ~/.claude/.credentials.json 구독 OAuth(sk-ant-oat0, subscriptionType=max)로 정상 서빙 확인. 3중 근거:
(1) 어댑터 레벨: build_anthropic_client 가 종량제 x-api-key 없이(api_key=None) auth_token(Bearer/OAuth)만 설정, anthropic-beta 에 claude-code-20250219,oauth-2025-04-20, user-agent claude-code/2.1.214 (external, cli) — Anthropic OAuth 라우팅 헤더.
(2) 라이브 SDK 호출: claude-sonnet-5 응답 GATE_OK, service_tier=standard, 성공. OAuth 전용 클라이언트가 성공 = 종량제였다면 Bearer 토큰 거부됨.
(3) 격리 HERMES_HOME + hermes -z CLI: GATE_OK2, exit 0. 격리 홈에 auth.json/.env/sk-ant-api 전무, 환경변수 ANTHROPIC_API_KEY 없음 — 유일한 anthropic 자격증명은 전역 구독 OAuth 뿐이라 성공은 구독 서빙일 수밖에 없음.
AC#3(종량제만 가능 시 Blocked)은 해당 없음 — 구독 경로 동작 확인, 마일스톤 진행 가능.
<!-- SECTION:NOTES:END -->
