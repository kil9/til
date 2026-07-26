---
id: DRAFT-1
title: 공통 요소 소급 후처리 스크립트
status: Draft
assignee: []
created_date: '2026-07-13 14:10'
labels: []
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
기존 전 페이지(`*/index.html`)에 OG 메타·분석 beacon 등 공통 헤드 요소의 누락을 검사·삽입하는 경량 스크립트(빌드 시스템 없이). 구 PLAN I-4.

SSG 미도입 결정(decision-1)의 선택 보완안 — 페이지 10건 이상으로 늘 때 착수를 검토한다.

PLAN 이관: 2026-07-13. 착수 전 상세 인터뷰 필요.
<!-- SECTION:DESCRIPTION:END -->

2026-07-26 흡수 완료: TASK-98·TASK-100 이 이 draft 가 말하던 '공통 헤드 요소 소급 삽입 스크립트'를 `backlog/assets/relink-pages.py` 로 실현했다(마커 구간 기반, 멱등). 지금 그 스크립트가 관리하는 것 — og:image 메타(카드 있는 전 페이지), 하단 이전/다음·주제 역링크(아티클), twitter:card 승격, 용량 경고. 남은 공통 요소(canonical 등)의 검사·삽입은 DRAFT-7 소관이다.
