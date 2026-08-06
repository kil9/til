---
id: DRAFT-6
title: HN 항목의 원문 본문 수집
status: Draft
assignee: []
created_date: '2026-08-06 08:05'
labels: []
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
loop-backlog 자동 추가(2026-08-06, task-106 작업 중 분리).

task-106 v1 은 HN 항목의 상세를 Algolia items 의 본문(Ask/Show HN 만 있다)과 최상위 댓글 5개로만 만든다. 외부 링크 글은 본문이 0자라 모델이 제목과 댓글만으로 요약을 쓴다. GeekNews 항목은 GN+ 요약 본문이 1,600자쯤 들어오는 것과 대비된다.

원문 URL 을 직접 fetch 하지 않은 이유: 임의의 웹사이트라 Cloudflare·JS 렌더·타임아웃으로 불안정하고, strip_tags 가 내비·쿠키 배너를 본문으로 긁어 와 6000자 컷을 잡동사니로 채우면 요약이 오히려 나빠진다.

하게 된다면 조건: 1회 시도(재시도 없음), 짧은 타임아웃, content-type 이 text/html 인지 확인, per-item 격리(이미 있다), 본문 추출을 strip_tags 가 아니라 readability 류로. 실패하면 지금 경로로 폴백.

착수 판단은 실제 회차 몇 개를 읽어 보고 한다 — 댓글만으로 쓴 HN 요약이 실제로 얇은지가 근거다. 지금은 그 근거가 없다.
<!-- SECTION:DESCRIPTION:END -->
