---
id: TASK-73
title: cloudflared Tunnel systemd 구성 (nuc14 서비스 노출)
status: Done
assignee: []
created_date: '2026-07-21 02:20'
updated_date: '2026-07-21 04:45'
labels:
  - solo
milestone: m-7
dependencies:
  - TASK-70
priority: medium
ordinal: 73000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
cloudflared 를 nuc14 에 설치해 터널을 만들고 systemd 서비스로 상시 구동한다. family-reports 등 내부 서비스를 서브도메인으로 노출한다. 인증 게이트는 후속 Access 태스크 몫이므로, 그 전까지 민감 서비스는 노출하지 않거나 임시 보호를 둔다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 터널이 systemd 로 재부팅 후에도 자동 기동된다
- [x] #2 지정 서브도메인으로 외부에서 대상 서비스에 접속된다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
remotely-managed 터널 'nuc14'(4c0eb030-ab10-40e0-8496-7eb81a3c450d)를 API 로 생성(브라우저 로그인 불필요). 구성 일체는 kil9dev-infra: install-cloudflared.sh(2026.7.2 핀), tunnel/config.json(ingress 진실원본: tdb.kil9.dev→localhost:18000 family-reports), tunnelctl(apply/show/status), systemd 유닛 원본. 실행 토큰은 ~/.config/cloudflare/tunnel-nuc14.env(600). systemd 시스템 서비스 cloudflared-nuc14 enabled+active(AC#1), 외부에서 https://tdb.kil9.dev/ 200·본문 확인(AC#2). DNS 는 dnscontrol 로 tdb CNAME(proxy on) push. 서브도메인 tdb 는 서비스 성격 비노출 목적의 사용자 선택. Access 게이트 전까지 무방비 창 최소화를 위해 task-76 을 즉시 후속 진행하기로 결정.
<!-- SECTION:NOTES:END -->
