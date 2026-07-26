---
id: TASK-75
title: apex 랜딩 구성 (kil9.dev 루트)
status: Done
assignee: []
created_date: '2026-07-21 02:20'
updated_date: '2026-07-21 06:55'
labels: []
milestone: m-7
dependencies:
  - TASK-71
priority: low
ordinal: 75000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
kil9.dev 루트에 둘 것을 결정하고 구현한다: 단순 til 리다이렉트 vs 간단한 명함/랜딩 페이지. 서빙 방식(Cloudflare Redirect Rule / Pages / 터널)도 이때 정한다. 방향 결정은 사용자 확인을 거친다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 kil9.dev 접속 시 결정된 목적지(리다이렉트 또는 랜딩)가 뜬다
- [x] #2 www.kil9.dev 도 동일하게 동작한다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
방향: 사용자 확인으로 미니멀 명함 랜딩(til 디자인 언어 재사용— 무채색+블루 액센트, 다크모드, 자체 완결 1페이지) + GitHub Pages 서빙(kil9/kil9.dev public repo, main 루트, CNAME kil9.dev). til·GitHub 링크 수록, 이메일은 스팸 수집 우려로 미기재. DNS 는 dnscontrol: apex A×4·AAAA×4(GitHub Pages 고정 대역)+www CNAME, 전부 DNS-only. 검증: https apex 200·www→apex 301 후 200·http→https 301(AC#1·#2). 함정: 초기 활성화 후 인증서 발급이 시작되지 않아(state none, 10분 대기) 커스텀 도메인 제거→재등록으로 재트리거하니 즉시 발급됨. dnsconfig.js 직전 레코드 쉼표 누락으로 preview 문법 오류 1회 — 레코드 추가 시 주의.
<!-- SECTION:NOTES:END -->
