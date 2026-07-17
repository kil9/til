---
id: TASK-29
title: 전 페이지 파비콘을 리브 아이콘으로 교체
status: Done
assignee: []
created_date: '2026-07-17 09:13'
labels: []
dependencies: []
ordinal: 29000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
사용자 요청: til 페이지 파비콘을 리브 아이콘으로. 기존 SVG 리스트 아이콘(공통 셸)과 kb16 두 페이지의 커스텀 SVG 를 모두 리브 원형 아이콘으로 통일.
<!-- SECTION:DESCRIPTION:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
avatar-expression-base.webp(256px)에서 얼굴 크롭(0.76W, top 2%) 후 원형 마스크(4x 슈퍼샘플링), 64px WebP q90 = 2.4KB 생성. 교체 26 + 파비콘 없던 plan-pipeline 하위 8 페이지 신규 삽입 = 34 파일, backlog legacy 아카이브 페이지는 제외. 각 파일 rel=icon 1개·base64 디코드 RIFF/WEBP 헤더 검증 통과. AGENTS.md 템플릿은 base64 비대화를 피해 '루트 index.html 에서 복사' 포인터로 갱신.
<!-- SECTION:NOTES:END -->
