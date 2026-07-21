---
id: TASK-70
title: Cloudflare API 토큰 발급·nuc14 저장·검증
status: Done
assignee: []
created_date: '2026-07-21 02:20'
updated_date: '2026-07-21 02:37'
labels:
  - solo
milestone: m-7
dependencies: []
priority: high
ordinal: 70000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
관리자 1회 작업으로 대시보드에서 API 토큰을 발급받는다(필요 스코프 안내 포함: Zone-DNS Edit·Zone Read + Account-Cloudflare Tunnel Edit·Email Routing Edit). nuc14 에 600 퍼미션·git 비추적 경로로 저장하고 kil9.dev zone 조회 호출로 검증한다. 이후 DNS·터널·메일 태스크의 공통 전제.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 발급된 토큰이 nuc14 에 600 퍼미션·비커밋 경로로 저장돼 있다
- [x] #2 토큰으로 kil9.dev zone 조회 API 호출이 성공한다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
토큰을 ~/.config/cloudflare/token (600, git 밖 XDG 경로)에 저장. 스코프: Zone Read·DNS Edit·Email Routing Rules Edit(zone=kil9.dev) + Cloudflare Tunnel Edit·Email Routing Addresses Edit(account). /user/tokens/verify → active, /zones?name=kil9.dev → success·status active(zone id a85ac7eb7e6c8d1ac9fae521292b2b2e, NS bradley/jillian.ns.cloudflare.com) 확인. Access(task-76)는 대시보드 수동 구성 예정이라 스코프 미포함.
<!-- SECTION:NOTES:END -->
