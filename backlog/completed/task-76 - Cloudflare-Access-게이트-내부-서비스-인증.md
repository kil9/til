---
id: TASK-76
title: Cloudflare Access 게이트 (내부 서비스 인증)
status: Done
assignee: []
created_date: '2026-07-21 02:20'
updated_date: '2026-07-21 06:05'
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
- [x] #1 보호 대상 서비스가 인증 없이는 접근 불가하다
- [x] #2 관리자 인증 후에는 정상 접근된다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
토큰에 Access 스코프 2종(Apps and Policies Edit, Orgs·IdP·Groups Edit) 추가 후 전부 API 자동화. Zero Trust 는 기온보딩 상태(팀 black-night-d3bc, Free). One-time PIN IdP 생성(16199775), tdb self-hosted 앱(8dda83e5, session 24h) + admin only allow 정책(krieiter@gmail.com, 541b23d4). 비인증 302→Access 로그인 확인(AC#1), 관리자 OTP 로그인 후 정상 접근 사용자 확인(AC#2). kil9dev-infra 에 access/accessctl(list/protect) 추가(2b1abed) — 이후 노출 서비스는 protect 한 줄로 동일 게이트. 서비스별 공개/보호 분류: 현재 노출은 tdb 뿐이며 보호 완료, 추가 노출 시 protect 를 기본 동선으로 README 에 명문화.
<!-- SECTION:NOTES:END -->
