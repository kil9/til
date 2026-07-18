---
id: TASK-50
title: E2E 검증·운용 기록 (hermes 리브)
status: To Do
assignee: []
created_date: '2026-07-18 05:55'
updated_date: '2026-07-18 06:48'
labels: []
milestone: m-4
dependencies:
  - TASK-48
  - TASK-49
priority: medium
ordinal: 50000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
리브-hermes 전체 흐름 검증 및 운용 노트.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 스레드 무멘션 대화·대기 렌더링·Claude 구독 소모·툴 잠금·(있으면)Tier-2 디스패치 E2E 확인
- [ ] #2 종량제 아님 재확인(구독 소모)
- [ ] #3 운용 노트 기록(프로필 관리·재기동·인스턴스 충돌·트러블슈팅)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
[TASK-48 인계] E2E 시 pre_gateway_dispatch 세션키 ↔ transform_llm_output session_id 실매칭 확인 필수(매칭돼야 owner 자연어/명시 커맨드가 실제 gh 디스패치). 미매칭이면 liv-dispatch/__init__.py _session_key_for_source 튜닝.
<!-- SECTION:NOTES:END -->
