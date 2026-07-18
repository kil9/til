---
id: TASK-48
title: Tier-2 글쓰기 디스패치 재현 (툴 잠금 하)
status: Done
assignee: []
created_date: '2026-07-18 05:55'
updated_date: '2026-07-18 06:48'
labels: []
milestone: m-4
dependencies:
  - TASK-46
priority: medium
ordinal: 48000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
리브 LLM 은 읽기전용이라 gh 를 직접 못 쓴다(TASK-46). 글쓰기 요청(!til/자연어) 감지 → til-inbox pending 이슈 생성을 hermes 에서 어떻게 할지 설계·구현. LLM 은 신호만 뱉고 이슈 생성은 데몬/훅/제한 커스텀 skill 코드가 수행(인젝션으로 이슈 조작 불가).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 글쓰기 요청 감지(명시 커맨드 + 자연어) → til-inbox pending 이슈 생성 경로 구현(제한 커스텀 skill 또는 외부 훅)
- [x] #2 게시 트리거는 사이트 주인만(owner 게이트) 유지, 비주인 거절
- [x] #3 리브 LLM 이 GitHub 접근 툴을 직접 갖지 않음(디스패치는 코드가 수행)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
완료 (2026-07-18). 읽기전용 툴 잠금(TASK-46) 하 Tier-2 글쓰기 디스패치를 hermes 게이트웨이 훅으로 재현. 코드: til-inbox bot/hermes/liv-dispatch/ (공개 repo, 커밋 1ccde80), 리브 프로필에 심링크 설치+enable.

## 설계 (AC#1: 명시+자연어 두 경로, 외부 훅)
- liv_dispatch.py: 순수 로직(detect_explicit_command, extract_publish_marker[마지막줄한정], sanitize_embedded, dispatch_writing[gh issue create], resolve_dispatch[단일 판단 진입점]). 기존 standalone bot/liv_daemon.py 와 동일 감지·마커 규약.
- 플러그인 __init__.py: pre_gateway_dispatch(수신 text·user_id 를 세션키로 stash) + transform_llm_output(LLM 응답에서 마커 추출→owner 확인→dispatch_writing→ACK 로 변형출력). reply-API 비의존(ACK 를 변형출력으로 반환).
- 명시 커맨드(!til/!publish-til//publish-til) + 자연어(SOUL 이 owner 게시요청 시 응답 마지막줄 PUBLISH_REQUEST: <주제> 방출) 둘 다 처리.

## owner 게이트 (AC#2, fail-closed)
- transform 훅엔 user_id 가 없어 pre_gateway_dispatch(user_id 보유)에서 세션키로 stash→transform 이 조회. 미매칭 시 디스패치 안 함(안전). 마커는 매칭 무관 항상 제거(사용자 미노출).
- 검증: 순수로직 단위테스트 20종 PASS(owner dispatch / stranger reject / user_id None reject / 자연어 마커 owner-only / 중간줄 마커 무시 / 멘션제거 / 커맨드 오탐방지 등). 플러그인 훅체인 통합 6종 PASS(dry-run).

## LLM 툴 부재 (AC#3)
- 리브 슬랙 툴셋은 [web,vision] 뿐(TASK-46)이라 gh/터미널 없음. 디스패치는 전적으로 플러그인 코드 수행. 인젝션으로 이슈 조작 불가(비주인은 마커 방출해도 미디스패치).

## 검증됨
- 플러그인 로드·훅 등록(pre_gateway_dispatch+transform_llm_output) 확인. sibling import 버그(sys.path) 수정.
- LLM 마커 방출 확인(owner 게시요청 → 응답 마지막줄 PUBLISH_REQUEST 방출), transform 훅이 -z 경로에서 마커 제거·미노출 확인.
- 테스트 중 실제 til-inbox 이슈 생성 0(fail-closed+dry-run).

## 잔여(→TASK-50 E2E)
라이브 게이트웨이에서 pre_gateway_dispatch 세션키 ↔ transform session_id 실매칭으로 실제 gh 디스패치가 도는지 최종 확인·튜닝(현재 fail-closed 라 미매칭 시 안전하게 미디스패치). 이는 게이트웨이 상시구동(TASK-49) 후 검증.
<!-- SECTION:NOTES:END -->
