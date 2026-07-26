---
id: TASK-72
title: til.kil9.dev 커스텀 도메인 연결 + 사이트 URL 정비
status: Done
assignee: []
created_date: '2026-07-21 02:20'
updated_date: '2026-07-21 04:22'
labels: []
milestone: m-7
dependencies:
  - TASK-71
priority: high
ordinal: 72000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
GitHub Pages(kil9/til)에 커스텀 도메인 til.kil9.dev 를 설정한다: repo CNAME 파일 + DNS CNAME→kil9.github.io + Enforce HTTPS. 구 kil9.github.io/til/... URL 은 GitHub 이 자동 리다이렉트한다. 사이트 내 URL 정비 포함: AGENTS.md 공통 셸의 og:url 템플릿, 기존 전체 페이지 og:url, README 라이브 링크, Cloudflare Web Analytics 사이트 도메인 추가.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 https://til.kil9.dev/ 가 서빙되고 구 github.io URL 이 새 도메인으로 리다이렉트된다
- [x] #2 AGENTS.md 템플릿·기존 페이지 og:url·README 가 새 도메인 기준으로 갱신됐다
- [x] #3 Web Analytics 가 til.kil9.dev 트래픽을 집계한다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
DNS: kil9dev-infra dnscontrol 에 til CNAME→kil9.github.io(DNS-only) 추가·push(76e4563). Pages: CNAME 파일 커밋(1cd1aa1) + API 로 cname 지정, 인증서 발급 후 https_enforced=true — https 200·http 301·구 github.io URL 301(경로 보존) 확인. URL 정비(45b24b0): 전 페이지 39건 og:url·AGENTS.md(템플릿·호스팅·구조 트리 CNAME)·README 치환, 404.html 리다이렉트 베이스(/til/ vs /) 경로 감지로 도메인 중립화 — 배포본에서 재검증. 함정: grep -v backlog 필터가 backlog-md-vs-plan-md 페이지까지 걸러 1건 누락됐다가 보완. Web Analytics 는 관리자가 대시보드에서 site hostname 을 til.kil9.dev 로 변경, 방문 집계 확인(AC#3).
<!-- SECTION:NOTES:END -->
