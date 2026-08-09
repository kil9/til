---
id: TASK-121
title: publish-til 저장소 경로 계약 고정
status: Done
assignee: []
created_date: '2026-08-09 06:11'
updated_date: '2026-08-09 06:15'
labels:
  - solo
milestone: m-14
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
워처가 전용 클론에서 Codex를 시작해도 publish-til 프리플라이트와 스킬 지시가 ~/work/kil9/til로 되돌리는 결함을 고친다. 명시적 환경변수로 게시 저장소를 전달하고, 워처는 전용 클론의 로컬 HEAD가 실제로 전진했는지 확인한 뒤에만 성공 처리한다. skills와 til-inbox 두 저장소 변경 SHA를 notes에 남긴다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 publish-til 프리플라이트가 명시적 게시 저장소 환경변수를 우선하고 미지정 시 기존 기본 경로를 유지한다
- [x] #2 til-submit 워처가 Codex에 전용 클론 경로를 전달하고 실행 후 해당 클론의 HEAD 전진을 확인한다
- [x] #3 실전과 같은 전용 클론 조건에서 ~/work/kil9/til을 건드리지 않고 게시 경로가 전용 클론으로 해석됨을 검증한다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
구현: publish-til은 TIL_PUBLISH_REPO 절대경로를 우선하고 미지정 시 기존 기본 경로를 유지한다. 워처는 Codex/Claude 양쪽에 전용 클론 경로를 전달하고, 실행 전후 로컬 HEAD가 선형으로 전진하지 않으면 URL이 있어도 failed 처리한다. skills ae33cfc, til-inbox dbebda3. 검증: bash -n, Codex skill quick_validate, 명시/기본/상대경로 프리플라이트, 주 작업 트리 상태 해시 불변.
<!-- SECTION:NOTES:END -->
