---
id: DRAFT-8
title: 접수창구 경로를 404 리다이렉트 맵에서 뺀다
status: Draft
assignee: []
created_date: '2026-08-06 15:22'
labels: []
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
loop-backlog 자동 추가(task-119 Fable 자문에서 발견). 404.html 의 리다이렉트 맵에 "submit-96a2d1c7e19e8a09":"p/submit-96a2d1c7e19e8a09" 항목이 있어 비공개 접수창구 경로가 공개 파일에 그대로 실려 있다. 다만 저장소가 public 이라 경로는 git 소스·히스토리로 이미 공개이고 실제 게이트는 처음부터 PAT 였다 — 보안 개선이 아니라 위생 정리이며 우선순위는 낮다. 구 평면 URL(/til/submit-…)로 실제 유입이 있었을 리 없어 제거 비용도 낮다. 완료 조건: 404.html 맵에서 그 항목을 지우고 site-check.py 가 통과한다(맵 검사는 갤러리 카드가 있는 페이지만 대상이라 카드 없는 이 경로는 누락으로 잡히지 않는다). 경로 은닉을 진지하게 원한다면 토큰 디렉터리 회전이 유일한 수단인데 PAT 게이트가 있는 이상 그 가치는 낮다고 봤다.
<!-- SECTION:DESCRIPTION:END -->
