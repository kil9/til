---
id: m-7
title: "kil9.dev 도메인 인프라"
---

## Description

Cloudflare 에서 등록한 kil9.dev 의 DNS·서빙·메일을 nuc14 중심으로 구성한다. DNS 는 kil9conf(private)에 dnscontrol 선언형으로 관리, til 은 til.kil9.dev 서브도메인으로 연결(apex 는 별도 랜딩), nuc14 서비스는 cloudflared Tunnel 로 노출 후 Access 로 보호, 메일은 수신 포워딩과 발신 send-as 까지 다룬다. 도메인 구매(2026-07)는 완료 상태.
