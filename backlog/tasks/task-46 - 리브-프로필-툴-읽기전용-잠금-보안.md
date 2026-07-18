---
id: TASK-46
title: 리브 프로필 툴 읽기전용 잠금 (보안)
status: To Do
assignee: []
created_date: '2026-07-18 05:54'
labels: []
milestone: m-4
dependencies:
  - TASK-44
priority: high
ordinal: 46000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
hermes-slack 기본 툴셋은 terminal/file/execute/browser 풀 접근이고 안전장치는 파괴적 명령 denylist 뿐(exfil 미차단), Tirith 미설치. 임의 Slack 입력 RCE 를 막으려 리브 프로필 툴셋을 읽기전용으로 축소한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 리브 프로필 platform_toolsets.slack 을 읽기전용 세트([web,vision] 등)로 축소, terminal/process/file/execute/browser 등 위험 툴 미포함
- [ ] #2 임의 Slack 입력으로 셸 실행·파일 읽기(cat ~/.claude/.credentials.json 등) 시도가 차단됨을 실증
- [ ] #3 아카이브 조회(웹) 기능은 유지
<!-- AC:END -->
