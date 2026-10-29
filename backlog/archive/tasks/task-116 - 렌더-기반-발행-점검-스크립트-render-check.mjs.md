---
id: TASK-116
title: 렌더 기반 발행 점검 스크립트 render-check.mjs
status: Done
assignee: []
created_date: '2026-07-28 18:31'
updated_date: '2026-07-28 18:34'
labels: []
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
loop-backlog/afk 자동 추가: TASK-115 를 검증하면서 헤드리스 렌더 측정 스크립트를 임시로 만들어 썼는데(레일 위치·폴백·하이라이트·오버플로), scratchpad 라 사라진다. site-check.py 는 파일만 읽어 렌더 결과를 못 보고, impeccable 의 URL 스캔은 이 머신에서 puppeteer 샌드박스로 죽어 대안이 없다. 다음 UI 작업에서 또 필요하므로 backlog/assets/ 에 살린다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 로컬 서버 URL 을 받아 뷰포트 5조건에서 목차 레일/인라인 폴백/현재 절 하이라이트/레일 오버플로를 자동 판정하고 위반 시 비영 종료코드로 끝난다
- [x] #2 puppeteer 경로를 하드코딩하지 않고 찾아 쓰며, 없으면 skip 을 찍고 0 으로 끝난다(발행을 막지 않는다)
- [x] #3 AGENTS.md 에 사용법과 site-check.py 와의 역할 구분이 기록된다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
afk 자율 진행분. backlog/assets/render-check.mjs 추가.
뷰포트 5조건(1440x900 / 1440x600 짧은 창 / 1280x900 분기 바로 위 / 1199x900 분기 바로 아래 / 700x900)에서 목차 가시성·레일 전환·인라인 폴백·본문 침범·화면 밖 이탈·뷰포트 넘침·현재 절 하이라이트를 판정하고 위반 시 exit 1.
puppeteer 는 ~/.npm/_npx/*/node_modules 를 훑어 찾는다 — 경로에 해시가 박혀 있어 하드코딩하면 impeccable 갱신 때마다 깨진다. 못 찾으면 skip + exit 0(HOME 을 없는 경로로 두고 실측 확인).
판정 함정 하나: <main> 이 없는 자체 스타일 페이지(2026-07-plan-pipeline)는 하이라이트 스크립트가 'main > .pagetoc' 을 못 찾아 안 도는 것이 정상인데, 첫 판본이 이를 위반으로 셌다(5건 오탐). railEligible 일 때만 검사하도록 고쳤다.
검증: 정상 4페이지 0 위반 / 레일 폭을 420px 로 깨뜨린 사본에서 '화면 왼쪽 밖으로 나갔다' 3건 검출 + exit 1. 오탐·미탐 양쪽을 확인했다.
AGENTS.md 퍼블리시 런북 §5 에 사용법과 site-check.py 와의 역할 구분 기록.
<!-- SECTION:NOTES:END -->
