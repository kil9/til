---
id: TASK-26
title: 제출 파이프라인 E2E 검증 및 운용 기록
status: To Do
assignee: []
created_date: '2026-07-17 07:27'
labels:
  - solo
milestone: m-1
dependencies:
  - TASK-23
  - TASK-24
  - TASK-25
priority: medium
ordinal: 26000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
실제 제출 1건으로 전 구간을 왕복 검증한다: 관리자 페이지 폼 제출 → til-inbox 이슈 생성 → 워처 감지·claim → headless /publish-til 게시 → 이슈 클로즈 → Slack #TIL 알림 4종. 운용법(잡 위치·재시작·PAT 재발급·트러블슈팅)을 auto-memory 와 til-inbox README 에 기록한다. til 공개 repo 쪽 문서에는 비밀 슬러그를 남기지 않는다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 실제 제출 1건이 페이지→이슈→워처→게시→클로즈→Slack 까지 완주한다
- [ ] #2 운용 런북이 auto-memory 와 til-inbox README 에 기록된다
- [ ] #3 til 공개 repo 문서에 비밀 슬러그가 노출되지 않는다
<!-- AC:END -->
