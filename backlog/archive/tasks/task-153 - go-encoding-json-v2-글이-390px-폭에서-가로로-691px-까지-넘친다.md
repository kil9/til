---
id: TASK-153
title: go-encoding-json-v2 글이 390px 폭에서 가로로 691px 까지 넘친다
status: Done
assignee: []
created_date: '2026-11-07T05:57:00Z'
updated_date: '2026-11-07T07:01:00Z'
labels: []
dependencies: []
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
TASK-150 검증(2026-11-07) 중 발견. puppeteer 390x844 에서 documentElement.scrollWidth=691. 오늘 작업 전 커밋 6d17391 의 같은 파일도 691 이라 기존 결함이다. overflow 로 잘리지 않은 요소 중 오른쪽 끝이 392 를 넘는 것은 찾지 못했다 — 의사 요소·긴 단어·표 폭 등을 의심. 다른 글에도 같은 패턴이 있는지 함께 본다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 go-encoding-json-v2 가 390px 폭에서 scrollWidth 가 390 이하다
- [x] #2 같은 원인을 가진 다른 글을 찾아 함께 고치거나, 없음을 notes 에 남긴다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
원인: '(CanadaGeometry·CITMCatalog·…·StringUnicode)' 처럼 가운뎃점으로만 이은 나열은 줄바꿈 기회가 없어 문단 밖으로 삐져나왔다(요소 상자는 390 이라 rect 검사로는 안 잡히고, main 자식을 하나씩 숨겨 찾았다).
전수 측정(390x844, 269페이지): 20페이지가 넘쳤다. 원인 둘 — (1) 끊을 곳 없는 긴 낱말·경로·식별자 code(13페이지+브리핑 2), (2) 스크롤 상자 없는 표(7페이지: agent-device, ai-math-proofs-verified-vs-understood, codex-code-mode-batching, dijkstra-mathematics-inc-ai-proof-factory, ecdsa-curve-seeds-lrand48, graph-engineering, opus5-model-choice).
수정: relink-pages.py 공통 CSS(PAGENAV-CSS)에 main{overflow-wrap:anywhere}·main table{overflow-wrap:break-word}·.tbl-scroll{overflow-x:auto} 를 넣어 135개 글에 재생성. 위 7페이지의 맨 표 24개를 div.tbl-scroll 로 감쌌다. 공통 CSS 밖인 plan-pipeline/parallel-plan.html 은 직접 넣었다. 브리핑 템플릿(template·recap·archive)과 기존 브리핑 페이지 104개의 main 규칙에 overflow-wrap:anywhere 추가.
재발 방지: render-check.mjs 에 390x844 뷰와 scrollWidth 가로 넘침 검사 추가(수정 전 go-encoding 은 위반 691 로 잡고 수정 후 통과 확인). AGENTS.md 에 '표는 스크롤 상자로 감싼다' 규약 추가.
검증: 269페이지 전부 scrollWidth<=392. 1280 폭에서 표 폭(672=본문 폭) 그대로. site-check.py 위반 없음. go-encoding·graph-engineering 390 스크린샷 육안 확인.
<!-- SECTION:NOTES:END -->
