---
id: TASK-122
title: til-submit 무인 회귀 테스트 추가
status: Done
assignee: []
created_date: '2026-08-09 06:11'
updated_date: '2026-08-09 06:17'
labels:
  - solo
milestone: m-14
dependencies:
  - TASK-121
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
임시 git 원격과 gh/codex mock으로 submit 성공 경로를 끝까지 실행한다. 전용 클론 cwd, 최종 답변 -o 분리, URL 파싱, 라벨 완료, 주 작업 트리 비변경을 자동 확인한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 외부 이슈나 공개 저장소를 건드리지 않는 로컬 회귀 테스트가 추가된다
- [x] #2 테스트가 Codex cwd와 게시 저장소 환경변수가 전용 클론임을 검사한다
- [x] #3 진행 로그와 최종 답변 분리 및 PUBLISHED_URL 성공 처리를 검사한다
- [x] #4 회귀 테스트와 bash 문법 검사가 통과한다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
구현: 임시 bare origin, decoy 기본 클론, gh/codex mock으로 submit 성공 경로를 외부 부작용 없이 실행하는 watcher/test-run.sh를 추가했다. 전용 cwd와 TIL_PUBLISH_REPO, 로컬 커밋·push, stdout 진행 로그와 -o 최종 답변 분리, URL 코멘트·done·close를 검증한다. til-inbox 526e2f6. bash -n과 테스트 통과.
<!-- SECTION:NOTES:END -->
