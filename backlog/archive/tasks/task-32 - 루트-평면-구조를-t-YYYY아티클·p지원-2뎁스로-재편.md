---
id: TASK-32
title: 루트 평면 구조를 t/YYYY(아티클)·p(지원) 2뎁스로 재편
status: Done
assignee: []
created_date: '2026-07-17 20:24'
updated_date: '2026-07-17 20:36'
labels:
  - solo
dependencies: []
priority: medium
ordinal: 32000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
루트에 페이지 dir 이 무한정 쌓이는 문제 해소(TASK-31 조사 후속). URL 무손실 포기(개인용·외부 미공유 확인됨). 날짜 아티클 21개는 t/<연도>/<slug>/ (til, 현재 전부 2026), 비-날짜 지원 페이지 3개(liv-today+sheet, til-archive, submit-96a2d1c7e19e8a09)는 p/<slug>/ (pages) 로 이동. 루트에는 t/·p/·backlog/ + 루트 파일만 남긴다. 모든 상대링크(복귀 ../, 페이지 상호링크 ../<slug>/)·og:url 절대경로·루트 갤러리 카드 href·README 표 링크를 새 경로로 정합화. 404.html 에 옛 slug→새 경로 리다이렉트 맵을 넣어 개인 북마크 안전망 제공. 자동화(publish-til·publish-naver 스킬, AGENTS.md 런북)를 신규 아티클→t/<현재연도>/, 비-날짜 신규→p/ 규약으로 개정(이 저장소 밖 스킬 파일은 별도 반영).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 날짜 아티클 21개를 t/2026/<slug>/ 로, 비-날짜 3개(liv-today+sheet/, til-archive, submit-96a2d1c7e19e8a09)를 p/<slug>/ 로 이동하고 루트에는 t/·p/·backlog/·루트파일만 남는다
- [x] #2 이동한 전 페이지의 내부 상대링크(인덱스 복귀 ../, 페이지 상호링크)와 og:url 절대경로가 새 경로로 정합화되어 깨진 링크가 0이다
- [x] #3 루트 index.html 갤러리 카드 href 22개와 README 표 링크가 새 경로로 갱신되고 data-date·data-topic·Published 카운트는 유지된다
- [x] #4 404.html 에 옛 slug→새 경로 리다이렉트 맵 JS 가 추가되어 옛 /til/<slug>/ 접근이 새 위치로 자동 이동한다
- [x] #5 AGENTS.md 퍼블리시 런북과 publish-til·publish-naver 스킬이 신규 아티클→t/<현재연도>/·비-날짜 신규→p/ 규약으로 개정된다
- [x] #6 python3 -m http.server 로 새 아티클 경로·지원 페이지 경로·옛 URL 리다이렉트가 실제로 열리는지 확인한다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
루트 평면 24 dir → t/(아티클 21, 연도 버킷 t/2026/)·p/(지원 3: liv-today+sheet, til-archive, submit-*) 2뎁스로 재편. Python 마이그레이션 스크립트로 git mv + 링크 정합화(아티클 복귀링크 ../→../../../, 지원 ../→../../, sheet 루트링크 ../../→../../../, og:url 전수 갱신, 아티클↔아티클 상호링크는 동일 버킷이라 무변). 루트 index.html 카드 href 22개·README 표 링크·404.html 리다이렉트 맵(24항목) 갱신. 검증: 페이지 상대링크 57개 깨짐 0, http.server 로 새 경로 전부 200, 404 리다이렉트 로직 node 시뮬로 하위경로·앵커 보존 확인, Published 22 유지. 자동화: AGENTS.md 런북(구조도·§2 템플릿 복귀링크·§3 배치·§4 목록·URL 예시)·publish-til(SKILL+til-preflight/til-verify 스크립트를 reldir 인자로) 개정. publish-naver 는 별도 내부 repo(kil9/docs, 미재편) 대상이라 규약 유지하고 범위 주석만 추가. 구 URL 은 개인용·외부 미공유라 파기 감수(사용자 확인).
<!-- SECTION:NOTES:END -->
