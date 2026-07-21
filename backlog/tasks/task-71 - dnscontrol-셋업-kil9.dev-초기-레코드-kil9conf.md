---
id: TASK-71
title: dnscontrol 셋업 + kil9.dev 초기 레코드 (kil9conf)
status: Done
assignee: []
created_date: '2026-07-21 02:20'
updated_date: '2026-07-21 02:53'
labels: []
milestone: m-7
dependencies:
  - TASK-70
priority: high
ordinal: 71000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
전용 private repo kil9dev-infra(github.com/kil9/kil9dev-infra)에 dnsconfig.js·creds 구조를 만들고 dnscontrol 로 kil9.dev 레코드를 선언형 관리한다. 레코드 변경 = 커밋+push 흐름. 초기 레코드는 이후 태스크에서 추가될 항목의 뼈대만 둔다. creds.json 은 env 참조($CLOUDFLARE_APITOKEN)라 시크릿 없이 커밋한다. (원래 kil9conf 예정이었으나 사내 리모트 유출 우려로 변경 — decision 참조)
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 dnscontrol preview/push 가 nuc14 에서 동작한다
- [x] #2 kil9.dev 의 실제 레코드가 dnsconfig.js 선언과 일치한다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
kil9conf 대신 전용 private repo kil9dev-infra(github.com/kil9/kil9dev-infra, ~/work/kil9/kil9dev-infra) 신설 — 사내 리모트 유출 우려(decision-7). 구성: bootstrap/install-dnscontrol.sh(v4.43.3 핀·멱등), dns/dnsconfig.js(kil9.dev zone, 초기 레코드 0건 + 후속 태스크 자리 주석), dns/creds.json(env 참조만, 시크릿 없음), dns/dnsctl(로컬 토큰 주입 래퍼). 검증: preview·push 모두 'Done. 0 corrections.' — 선언과 실제(0건) 일치. 커밋 e29ed41 push 완료. repo 로컬 user.email 은 noreply 로 설정.
<!-- SECTION:NOTES:END -->
