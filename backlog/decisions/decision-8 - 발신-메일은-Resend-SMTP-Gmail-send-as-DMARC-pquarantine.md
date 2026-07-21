---
id: decision-8
title: '발신 메일은 Resend SMTP + Gmail send-as, DMARC p=quarantine'
date: '2026-07-21 07:10'
status: accepted
---
## Context

task-74 로 @kil9.dev 수신(CF Email Routing → Gmail)은 구성됐으나 발신 경로가 없었다.
Gmail send-as 는 외부 SMTP 를 붙여야 SPF·DKIM·DMARC 정렬이 되므로(자체 gmail.com 경유는
d=gmail.com 서명이라 정렬 실패) 발신용 SMTP 프로바이더가 필요했다. 2026-07 기준 무료 티어 조사:

- Resend: 3,000통/월(100/일), 도메인 1개, 브랜딩 없음, SMTP relay 포함
- SMTP2GO: 1,000통/월(200/일), 발신 도메인 5개, 브랜딩 없음
- Brevo: 300통/일이지만 무료 플랜은 "Sent by Brevo" 푸터 강제(제거 유료) → 개인 서신 부적합
- AWS SES: 최저가($0.10/1천통)지만 무료는 신규 12개월 한정 + sandbox 해제·IAM 등 셋업 과중

## Decision

- 프로바이더는 Resend (region ap-northeast-1/Tokyo, 도메인 kil9.dev verified).
- Gmail send-as: kil9@kil9.dev, smtp.resend.com:587 TLS, 사용자명 `resend`,
  비밀번호는 발신 전용(Sending access, kil9.dev 한정) API 키 `gmail-send-as`.
- DMARC 는 p=quarantine 로 시작(rua=mailto:dmarc@kil9.dev, catch-all 로 Gmail 수신).
  발신 경로가 방금 구성한 한 곳뿐이라 오탐 위험이 낮아 p=none 단계를 건너뛰었다.
- DNS 4레코드(resend._domainkey DKIM TXT, send MX/SPF TXT, _dmarc TXT)는 kil9dev-infra
  dnscontrol 선언 관리(f2b35bc).

## Consequences

- mail-tester 10/10, SPF(send.kil9.dev 정렬)·DKIM(d=kil9.dev)·DMARC 모두 pass.
- Return-Path 가 send.kil9.dev(SES 경유)라 SPF 는 send 서브도메인에서 평가된다 — apex SPF
  (_spf.mx.cloudflare.net, 수신 포워딩용)와 서로 간섭하지 않는다.
- 무료 100통/일 한도는 개인 서신엔 충분. 초과가 필요해지면 유료 전환 또는 SMTP2GO 병행.
- API 키가 Gmail 설정에만 저장돼 있으므로 유출 시 Resend 대시보드에서 키 폐기로 차단 가능.
  키는 로컬/repo 어디에도 저장하지 않았다(1회 노출 후 사용자 클립보드 → Gmail 직행).
- DMARC 집계 리포트가 dmarc@kil9.dev 로 오기 시작하면 catch-all 을 타고 Gmail 에 쌓인다.
  소음이 되면 필터로 정리하거나 rua 를 제거한다.
