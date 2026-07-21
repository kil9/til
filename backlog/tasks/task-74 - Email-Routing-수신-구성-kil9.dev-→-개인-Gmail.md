---
id: TASK-74
title: Email Routing 수신 구성 (@kil9.dev → 개인 Gmail)
status: Done
assignee: []
created_date: '2026-07-21 02:20'
updated_date: '2026-07-21 06:27'
labels: []
milestone: m-7
dependencies:
  - TASK-71
priority: medium
ordinal: 74000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Cloudflare Email Routing(무료)으로 @kil9.dev 수신 메일을 관리자 개인 Gmail 로 포워딩한다. catch-all 여부와 주소별 라우팅은 구성 시 결정. MX·관련 TXT 레코드는 dnscontrol(task-71 산출물)에 반영한다. 개인 메일 주소는 public repo 에 적지 않는다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 테스트 메일이 @kil9.dev 로 발송되어 개인 Gmail 에 도착한다
- [x] #2 메일 레코드가 dnscontrol 과 정합하다 — SPF TXT 는 선언 관리, CF read-only 잠금인 MX·DKIM 은 dnsconfig.js 에 문서화하고 preview 0 corrections 를 확인
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Email Routing 활성화는 대시보드 1클릭(설정 계열 API 는 토큰 스코프 밖 — Rules/Addresses 스코프로는 rules·catch_all·addresses 만 가능, enable·dns·settings 는 Authentication error). 수신 주소 krieiter@gmail.com 은 API 등록 즉시 자동 verified(계정 소유자 메일). catch-all → forward 규칙 API 적용. CF 가 자동 생성한 MX 3종·DKIM TXT 는 read-only 잠금이라 dnscontrol 이 걸러냄 — 선언하면 중복 CREATE 시도하는 함정 확인, 잠금 유지 + dnsconfig.js 주석 문서화로 결정(AC#2 문구 교체). SPF TXT 만 선언 관리(TTL 1=auto), preview 0 corrections(AC#2). 외부 발신 테스트 메일 Gmail 도착 확인(AC#1). 유의: 대시보드의 '이메일 전송(베타)' 는 Workers 유료 발신 기능으로 이번 수신 구성과 무관.
<!-- SECTION:NOTES:END -->
