---
id: TASK-10
title: docs-ai-summary 잡이 comm 정렬 오류로 죽는 버그 수정
status: Done
assignee: []
created_date: '2026-07-15 10:49'
updated_date: '2026-07-15 10:52'
labels: []
dependencies: []
priority: high
ordinal: 10000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
loop-task 자동 추가: TASK-9 의 AC#3(잡 1회 실행 검증)을 시도하다 발견했다. ~/jobs/docs-ai-summary/run.sh 가 prev(state/pages.list)와 current 를 comm 으로 비교하는데, state 파일이 정렬돼 있지 않아(옛 스크립트가 남긴 파일 목록 블록 + 새 디렉터리 목록 블록이 이어붙어 있음) comm 이 'input is not in sorted order' 로 실패하고, set -e 때문에 잡이 그 줄에서 죽는다. cron.log 상 2026-07-12 09:00 이후 성공 기록이 없고 comm 에러만 3회 반복 — 즉 잡이 사흘째 무동작이었다. TASK-9 의 AC#3 이 이 버그에 막히므로 선행 수정한다. 잡은 repo 밖 머신 로컬이고 git 미관리라 repo 커밋에는 backlog 변경만 담긴다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 run.sh 가 comm 양쪽 입력을 정렬해 넘겨, state 가 어떤 순서로 들어와도 죽지 않는다
- [x] #2 state/pages.list 를 정렬된 형태로 복구한다
- [x] #3 잡을 1회 실행해 comm 에러 없이 끝까지 진행됨을 확인한다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
근인은 정렬 기준 불일치였다. run.sh 는 prev/current 를 sort(로케일 정렬)로 만들어 comm 에 넘겼는데, comm 은 바이트 순으로 비교한다. LANG=en_US.UTF-8 에서 sort 는 'ai-capex-hedge' < 'CLAUDE.md' 로 놓지만 comm 은 대문자를 먼저 보므로 file 1 을 미정렬로 판정하고 실패했고, set -e 가 잡을 그 줄에서 죽였다. state 가 옛 포맷(파일까지 포함된 목록) + 새 포맷 두 블록으로 어긋나 있던 것이 이 불일치를 처음 노출시킨 계기다.

수정: 비교 구간만 LC_ALL=C 로 고정해 sort 와 comm 의 순서 기준을 맞췄다(전역 LC_ALL=C 는 요약문 UTF-8 처리를 건드릴 수 있어 피함). state/pages.list 는 LC_ALL=C sort -u 로 복구(원본은 pages.list.bak 보관). 첫 시도에서 로케일 sort 로만 복구했다가 같은 에러가 재현돼 원인을 다시 잡았다.

검증: bash run.sh 1회 실행 → comm 에러 없이 신규 9건 감지, injected: intro, 175b00f push 완료. 사흘치(2026-07-12~15) 밀린 페이지를 한 번에 따라잡았다.
<!-- SECTION:NOTES:END -->
