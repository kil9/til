---
id: TASK-126
title: SOL 퍼블리시 effort 기본값을 high로 조정
status: Done
assignee: []
created_date: '2026-08-09 06:30'
updated_date: '2026-08-09 06:32'
labels:
  - solo
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
첫 실전은 gpt-5.6-sol xhigh로 검증했지만 이후 비용·시간을 비교하기 위해 워처 기본 effort를 high로 낮춘다. TIL_SUBMIT_EFFORT 환경변수 오버라이드는 유지해 부족할 때 xhigh로 즉시 되돌릴 수 있게 한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 codex submit/research 기본 effort가 high로 설정된다
- [x] #2 README의 실행기 설명과 롤백·조정 안내가 high 기본값을 반영한다
- [x] #3 mock 회귀 테스트가 high 인자와 RUN_METRICS effort=high를 검증한다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
til-inbox f6b9316에서 watcher 기본 effort를 high로 낮추고 TIL_SUBMIT_EFFORT=xhigh 오버라이드를 유지했다.
검증: bash -n watcher/run.sh watcher/test-run.sh, watcher/test-run.sh, git diff --check 통과.
<!-- SECTION:NOTES:END -->
