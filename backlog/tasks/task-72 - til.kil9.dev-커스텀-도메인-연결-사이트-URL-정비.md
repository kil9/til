---
id: TASK-72
title: til.kil9.dev 커스텀 도메인 연결 + 사이트 URL 정비
status: In Progress
assignee: []
created_date: '2026-07-21 02:20'
updated_date: '2026-07-21 03:05'
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
- [ ] #1 https://til.kil9.dev/ 가 서빙되고 구 github.io URL 이 새 도메인으로 리다이렉트된다
- [ ] #2 AGENTS.md 템플릿·기존 페이지 og:url·README 가 새 도메인 기준으로 갱신됐다
- [ ] #3 Web Analytics 가 til.kil9.dev 트래픽을 집계한다
<!-- AC:END -->
