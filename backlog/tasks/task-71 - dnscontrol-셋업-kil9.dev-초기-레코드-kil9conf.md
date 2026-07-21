---
id: TASK-71
title: dnscontrol 셋업 + kil9.dev 초기 레코드 (kil9conf)
status: To Do
assignee: []
created_date: '2026-07-21 02:20'
labels: []
milestone: m-7
dependencies:
  - TASK-70
priority: high
ordinal: 71000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
kil9conf(private 확인 완료, remote 이름은 github)에 dnsconfig.js·creds 구조를 만들고 dnscontrol 로 kil9.dev 레코드를 선언형 관리한다. 레코드 변경 = 커밋+push 흐름. 초기 레코드는 이후 태스크에서 추가될 항목의 뼈대만 둔다. creds(토큰 참조)는 커밋하지 않는다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 dnscontrol preview/push 가 nuc14 에서 동작한다
- [ ] #2 kil9.dev 의 실제 레코드가 dnsconfig.js 선언과 일치한다
<!-- AC:END -->
