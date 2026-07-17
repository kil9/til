---
id: TASK-21
title: 관리자 URL 제출 기능의 정적 페이지 실현 가능성 조사(확인만)
status: Done
assignee: []
created_date: '2026-07-17 06:23'
updated_date: '2026-07-17 06:37'
labels: []
dependencies: []
priority: low
ordinal: 21000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
관리자가 사이트 페이지에서 URL 을 던지면(제출하면) 접수되는 흐름이 GitHub Pages 정적 호스팅에서 가능한지 조사만 한다. 구현하지 않는다. 검토 후보: GitHub Issues 템플릿 딥링크, repository_dispatch/workflow_dispatch + PAT, 외부 폼·서버리스 엔드포인트, PWA share target 등. 각 방식의 성립 조건(인증·공개 repo 노출 범위·비용)과 장단점을 정리해 보고한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 가능/불가 판단과 대안 옵션별 장단점이 정리되어 보고된다
- [x] #2 구현·커밋은 하지 않는다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
조사 결론: **가능하다.** 관리자 1인 전용이라면 GitHub Pages 정적 호스팅만으로 URL 제출 접수 흐름이 성립한다. 옵션별 정리:

## 옵션 1 — GitHub Issues 템플릿 딥링크 (권장 시작점)
정적 페이지의 폼이 `https://github.com/kil9/til/issues/new?template=submit-url.yml&<필드id>=<값>` 딥링크를 만들어 열고, 관리자가 GitHub 화면에서 Submit 클릭. issue forms 는 query param 으로 필드 프리필을 지원한다.
- 성립 조건: 관리자가 GitHub 로그인 상태. 토큰·시크릿 불필요.
- 장점: 코드·시크릿 0, 무료, 접수함(이슈)·알림·후속 자동화(Actions on issues:opened)가 공짜로 따라옴.
- 단점: 제출이 2단계(딥링크 → GitHub 에서 확인 클릭), 공개 repo 라 제출 내용 전부 공개.

## 옵션 2 — 정적 페이지 + GitHub API 직접 호출 (fine-grained PAT)
api.github.com 은 CORS 허용을 실측 확인(`access-control-allow-origin: *`, Authorization 헤더·POST 허용, 2026-07-17 preflight 실측). 정적 페이지 JS 가 PAT 로 `repository_dispatch`(contents:write) / `workflow_dispatch`(actions:write) / contents API(큐 파일 커밋)를 직접 호출 가능. PAT 는 관리자가 최초 1회 입력해 localStorage 보관.
- 성립 조건: kil9/til 한정 최소 권한 fine-grained PAT 발급, 관리자 본인 브라우저에만 저장, 접수 처리용 workflow 1개.
- 장점: 페이지 안 원클릭 제출(UX 최상), 서버·비용 0.
- 단점: PAT 가 브라우저 평문 보관(기기 분실·XSS 시 유출 — 단 이 사이트는 외부 스크립트가 beacon 뿐), 토큰 만료 관리 필요, 공개 repo 라 dispatch payload 가 Actions 로그·커밋으로 공개됨.

## 옵션 3 — 외부 폼/서버리스 엔드포인트 (Cloudflare Workers, Formspree 등)
- 성립 조건: 외부 서비스 계정 + 엔드포인트 운영. 무료 티어로 충분.
- 장점: 시크릿이 서버 측에 있어 브라우저에 안 남음, 제출 내용 비공개 가능, 스팸 방어 통제.
- 단점: repo 밖 인프라가 생김(운영 부담). 관리자 1인 용도로는 과함.

## 옵션 4 — PWA share target
manifest `share_target` 등록 시 모바일 공유 시트에서 URL 접수 가능. GitHub Pages 는 HTTPS 라 PWA 성립.
- 장점: 모바일 "공유 → 사이트" 흐름이 가장 자연스러움.
- 단점: 접수 UI 일 뿐 영속화는 옵션 1-3 과 조합해야 완결. Chromium/Android 중심 지원, iOS Safari 미지원(2026 현재). 단독 대안이 아니라 조합 부품.

## 권장
최소 마찰 시작은 옵션 1(딥링크). 원클릭이 필요해지면 옵션 2(PAT + dispatch)로 승격. 3·4 는 현 규모에 과함. AC #2 에 따라 구현·커밋은 하지 않았다(이 태스크 파일은 이후 backlog 정리 커밋에만 포함).
<!-- SECTION:NOTES:END -->
