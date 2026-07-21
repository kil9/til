---
id: TASK-74
title: Email Routing 수신 구성 (@kil9.dev → 개인 Gmail)
status: To Do
assignee: []
created_date: '2026-07-21 02:20'
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
- [ ] #1 테스트 메일이 @kil9.dev 로 발송되어 개인 Gmail 에 도착한다
- [ ] #2 MX·관련 TXT 레코드가 dnscontrol 선언에 들어 있다
<!-- AC:END -->
