---
id: TASK-119
title: 접수창구를 PWA 로 만들어 안드로이드 공유 시트에 share_target 등록
status: To Do
assignee: []
created_date: '2026-08-06 12:33'
labels: []
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
2026/web-share-target/ 조사 보고서의 A안(본선)을 구현한다. 안드로이드 크롬·갤러리 등에서 공유 시트로 URL 을 넘기면 접수창구(p/submit-96a2d1c7e19e8a09/)가 항목으로 뜨고, 공유된 내용이 채워진 폼에서 접수까지 이어지게 한다.

접근: 접수창구 디렉터리에 manifest.webmanifest 와 아이콘을 두고 페이지 head 에 link rel=manifest 를 건다. share_target 은 method GET, action 은 절대 경로(안드로이드 캐시·상대경로 함정). 공유로 열려도 같은 오리진이라 localStorage 의 PAT 를 그대로 쓴다. 파일 공유(POST + multipart + 서비스 워커)는 이번 범위 밖.

결정사항:
- 공유 진입 시 기본 동작은 자동 접수가 아니라 프리필 폼이다(오발 방지, 구현 단순).
- 아이콘 192/512 파일은 접수창구 디렉터리 사이드카로 둔다. thumbs/·og/ 와 같은 결의 단일 파일 원칙 의도적 예외이며 AGENTS.md 에 명시한다.
- 안드로이드는 URL 을 url 파라미터로 주지 않는다 — text 에 실려 오므로 text 에서 URL 을 골라내는 처리가 필수.

근거 문서: 2026/web-share-target/index.html 의 '구현 체크리스트 (다음 에이전트용)' 절.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 p/submit-96a2d1c7e19e8a09/manifest.webmanifest 가 있고 name·icons(192/512)·start_url·scope·display:standalone·share_target(method GET, 절대 경로 action, params title/text/url)을 갖춘다
- [ ] #2 접수 페이지 head 에 link rel=manifest 가 걸리고, 아이콘 파일이 같은 디렉터리에 사이드카로 존재한다
- [ ] #3 공유 진입(?title/?text/?url)이면 그 내용으로 채워진 접수 폼이 뜬다. 자동 접수하지 않는다. text 파라미터에 URL 이 실려 온 경우를 골라내 처리한다
- [ ] #4 접수 성공 후 history.replaceState 로 공유 쿼리를 지워, 새로고침해도 같은 내용이 다시 프리필되지 않는다
- [ ] #5 접수 본문에 SOURCE: share-sheet 표식이 들어가 워처 쪽에서 유입 경로를 구분할 수 있다
- [ ] #6 접수창구·매니페스트·아이콘 모두 비공개 유지: noindex 그대로이고 루트 갤러리·README 표·sitemap.xml·search-index.json·feed.xml 어디에도 노출되지 않는다
- [ ] #7 AGENTS.md 에 PWA 아이콘·매니페스트 사이드카가 단일 파일 원칙의 의도적 예외임을 기록한다
- [ ] #8 site-check.py 통과
- [ ] #9 관리자 실기 검증: 안드로이드 크롬에서 홈 화면에 추가 → 크롬에서 URL 공유 → 공유 시트에 항목이 뜨고 → 접수 폼이 프리필되고 → til-inbox 에 pending 이슈가 생기는 것까지 확인
<!-- AC:END -->
