---
id: TASK-125
title: 퍼블리시 대형 data URI 출력 억제
status: Done
assignee: []
created_date: '2026-08-09 06:26'
updated_date: '2026-08-09 06:27'
labels:
  - solo
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
첫 SOL 발행 로그가 약 1MB까지 커진 두 번째 원인은 신규 HTML의 base64 이미지가 포함된 전체 diff 출력이었다. publish-til 스킬과 무인 프롬프트가 이미지 임베드 이후에는 data URI 본문이나 전체 git diff를 출력하지 않고 stat, status, 경로 한정 검사로 검증하도록 고정한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 publish-til 스킬이 base64 임베드 이후 data URI 본문과 전체 diff 출력 금지를 명시한다
- [x] #2 til-submit 프롬프트가 같은 출력 위생 규칙을 전달한다
- [x] #3 Claude/Codex 미러 검증과 watcher mock 테스트가 통과한다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
구현: publish-til Claude/Codex 미러와 til-submit 프롬프트에 data URI 본문·전체 git diff 출력 금지, status·diff --stat·경로 검사·placeholder 사용을 명시했다. mock 프롬프트 검증과 Codex skill quick_validate 통과. skills 3b11f1f, til-inbox 11a7fab.
<!-- SECTION:NOTES:END -->
