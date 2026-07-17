---
id: TASK-22
title: til-inbox private 접수함 repo 생성 및 접수 규약 정의
status: To Do
assignee: []
created_date: '2026-07-17 07:27'
labels:
  - solo
milestone: m-1
dependencies: []
priority: medium
ordinal: 22000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
관리자 URL 제출 파이프라인의 접수함. github.com/kil9/til-inbox private repo 를 만들고, 이슈 기반 큐 규약을 정한다. 제출 내용 비공개와 PAT 피해 반경 축소를 위해 til 본 repo 가 아닌 별도 private repo 를 쓴다(TASK-21 조사 결론).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 kil9/til-inbox private repo 가 생성된다
- [ ] #2 이슈 접수 포맷(제목·본문 필드: URL·메모)과 라벨 세트(pending/processing/done/failed)가 정의되어 라벨이 실제 생성된다
- [ ] #3 README 에 접수 규약과 파이프라인 개요 런북이 기록된다
<!-- AC:END -->
