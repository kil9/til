---
id: TASK-77
title: '@kil9.dev 발신 메일 (Gmail send-as + 외부 SMTP)'
status: To Do
assignee: []
created_date: '2026-07-21 02:20'
labels: []
milestone: m-7
dependencies:
  - TASK-74
priority: low
ordinal: 77000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
발신용 SMTP 후보(Resend·SES 등 무료 티어)를 조사해 사용자 결정을 받고, Gmail send-as 로 @kil9.dev 발신을 구성한다. SPF·DKIM·DMARC 레코드는 dnscontrol 에 반영한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Gmail 에서 @kil9.dev 명의로 발신되고 SPF·DKIM·DMARC 를 통과한다
- [ ] #2 관련 레코드가 dnscontrol 선언에 들어 있다
<!-- AC:END -->
