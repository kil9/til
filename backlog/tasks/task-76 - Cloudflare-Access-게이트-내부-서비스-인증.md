---
id: TASK-76
title: Cloudflare Access 게이트 (내부 서비스 인증)
status: To Do
assignee: []
created_date: '2026-07-21 02:20'
labels: []
milestone: m-7
dependencies:
  - TASK-73
priority: medium
ordinal: 76000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
터널로 노출한 내부 서비스(family-reports 등)에 Cloudflare Access 인증(이메일 OTP 기본, 필요시 IdP)을 건다. 서비스별 공개/보호 분류를 먼저 정리한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 보호 대상 서비스가 인증 없이는 접근 불가하다
- [ ] #2 관리자 인증 후에는 정상 접근된다
<!-- AC:END -->
