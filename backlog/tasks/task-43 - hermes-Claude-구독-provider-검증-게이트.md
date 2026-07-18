---
id: TASK-43
title: hermes Claude 구독 provider 검증 (게이트)
status: To Do
assignee: []
created_date: '2026-07-18 05:54'
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
- [ ] #1 임시/격리 hermes 프로필에서 anthropic provider 를 구독 자격증명(~/.claude/.credentials.json 또는 OAuth setup-token)으로 구성해 응답 생성 성공
- [ ] #2 그 호출이 구독으로 소모되고 종량제 API 키 경로로 넘어가지 않음을 확인(auth 모드·사용량 근거)
- [ ] #3 종량제로만 가능하다고 판명되면 근거를 기록하고 이 마일스톤 전체를 Blocked 로 전환
<!-- AC:END -->
