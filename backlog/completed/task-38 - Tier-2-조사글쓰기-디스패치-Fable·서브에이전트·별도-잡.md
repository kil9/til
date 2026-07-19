---
id: TASK-38
title: Tier-2 조사+글쓰기 디스패치 (Fable·서브에이전트·별도 잡)
status: Done
assignee: []
created_date: '2026-07-17 20:30'
updated_date: '2026-07-17 22:09'
labels: []
milestone: m-2
dependencies:
  - TASK-36
priority: medium
ordinal: 38000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
글쓰기 요청을 대화 감지와 명시 커맨드 둘 다로 받아 Fable 조사·집필 잡을 별도 프로세스로 비동기 시작. 산출물은 공개 TIL 게시(기존 fable /publish-til 파이프라인 재사용). 시작·완료 Slack 통지.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 명시 커맨드(!til, /publish-til, !publish-til)와 대화 감지 둘 다로 글쓰기 요청 트리거
- [x] #2 Fable 잡을 별도 프로세스로 비동기 시작(대화 턴 블로킹 안 함), 조사 서브에이전트 팬아웃 후 리브 문체로 집필
- [x] #3 산출물은 공개 TIL 게시(기존 fable /publish-til 파이프라인 재사용)
- [x] #4 시작·완료(게시 URL) Slack 통지
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
til-inbox bot/liv_daemon.py(커밋 522fedd). 명시 커맨드(!til/!publish-til/publish-til <주제>, 멘션·DM 기준 prefix 파싱) + 대화 감지(build_prompt 디스패치 지침 → 모델이 명시 게시 요청에만 PUBLISH_REQUEST 마커 → 데몬 파싱·제거·디스패치). 디스패치=gh issue create(SOURCE: liv-slack/REQUEST: 포맷, label pending) → 기존 til-submit 워처가 Fable /publish-til 로 조사(서브에이전트 팬아웃)·집필·공개게시·통지(접수/시작/완료/실패) 이어받음(비동기, 대화 논블로킹). 오탐 공개게시 방지: 게시 트리거는 사이트 주인(LIV_OWNER_IDS 기본 U0B54E64FNW=kil9)만, 비주인 거절, 빈주제 안내. 검증: 순수함수 유닛(감지·마커·포맷 = 워처 소비 포맷 일치) + Slack E2E(mock gh, 실게시 없이): 명시·대화감지 디스패치 O, 일반질문·빈주제·비주인 디스패치 X 확인. 실게시 전체 흐름 E2E 는 TASK-39.
<!-- SECTION:NOTES:END -->
