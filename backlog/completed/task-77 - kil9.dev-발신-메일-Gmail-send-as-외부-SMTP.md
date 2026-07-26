---
id: TASK-77
title: '@kil9.dev 발신 메일 (Gmail send-as + 외부 SMTP)'
status: Done
assignee: []
created_date: '2026-07-21 02:20'
updated_date: '2026-07-21 08:01'
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
- [x] #1 Gmail 에서 @kil9.dev 명의로 발신되고 SPF·DKIM·DMARC 를 통과한다
- [x] #2 관련 레코드가 dnscontrol 선언에 들어 있다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Resend(ap-northeast-1, kil9.dev verified) SMTP + Gmail send-as(kil9@kil9.dev) 구성 완료. DNS 4레코드(DKIM·send MX/SPF·DMARC quarantine)는 kil9dev-infra dnscontrol 반영(f2b35bc, preview 0 corrections — AC#2). 검증: mail-tester 10/10, SPF(send.kil9.dev 정렬)·DKIM(d=kil9.dev)·DMARC 모두 pass(AC#1). 자기수신 테스트는 Gmail dedupe 로 인증헤더가 없어 외부 검증으로 대체. API 키는 발신 전용(Sending access, kil9.dev 한정) 'gmail-send-as', 값은 미보관(Gmail 설정에만 존재). 상세는 decision-8.
<!-- SECTION:NOTES:END -->
