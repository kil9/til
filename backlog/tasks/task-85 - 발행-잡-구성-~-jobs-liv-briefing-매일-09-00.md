---
id: TASK-85
title: '발행 잡 구성 (~/jobs/liv-briefing/, 매일 09:00)'
status: Done
assignee: []
created_date: '2026-07-26 07:27'
updated_date: '2026-07-26 08:05'
labels:
  - solo
milestone: m-9
dependencies:
  - TASK-80
  - TASK-81
priority: high
ordinal: 85000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
nuc14 cron 이 매일 09:00 KST 에 브리핑을 생성해 til 에 push 한다. 기존 ~/jobs/docs-ai-summary·til-submit 과 같은 배관을 쓴다: run.sh + state/ + flock + cron.log, 실패해도 조용히 죽지 말고 로그를 남긴다.

파이프라인: GeekNews 수집(task-80) → 선별·정리(headless claude -p --model opus) → 페이지 렌더(task-81 템플릿) → p/briefing/ 과 p/briefing/<날짜>/ 에 쓰기 → git commit·push → Pages 반영.

함정: (1) docs-ai-summary 가 로케일 정렬과 pipefail 로 두 번 조용히 죽은 전례가 있다. 같은 실수를 반복하지 않도록 비교 구간은 LC_ALL=C, 루프 끝 종료코드는 고정한다. (2) 같은 날 두 번 도는 것을 state 로 막는다. (3) til 워킹트리가 dirty 하면 push 가 남의 변경을 삼킬 수 있으므로 전용 클론(repo/)을 쓰고 git add 는 경로 명시로만 한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 cron 0 9 * * * 로 등록돼 매일 09:00 에 돈다
- [x] #2 run.sh 가 수집→선별→렌더→push 를 한 번에 수행하고 flock 으로 중복 실행을 막는다
- [x] #3 같은 날 이미 발행됐으면 LLM 호출 없이 조기 종료한다
- [x] #4 실패 시 cron.log 에 원인이 남고 Slack 으로 실패가 통지된다
- [x] #5 전용 클론에서만 커밋하며 add 는 경로를 명시한다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
run.sh 를 재료 단계(task-80) 위에 확장했다: 렌더(render.py) → 전용 클론 fetch/reset → p/briefing/{index.html,<날짜>/index.html} 경로 명시 add → commit → push.

cron 은 두 줄로 갈랐다.
  40 8 * * *  BRIEFING_PUBLISH=0 (재료만: 수집·선별·정리, 약 4분)
  0  9 * * *  전체 (재료가 있으면 렌더·발행만 하므로 09:00 정각에 페이지가 뜬다)
한 줄로 09:00 에 다 돌리면 페이지가 09:05 에나 뜬다. 08:40 에 발행까지 해 버리면 09:00 발행이 아니게 된다.

함정 대응:
- push 밀림: docs-ai-summary 가 09:00 에 같은 저장소로 push 한다. 실패하면 fetch/reset 후 다시 렌더·커밋해 최대 3회 재시도하고, 그래도 안 되면 Slack 으로 알리고 rc=1 로 죽는다.
- 중복 발행: state/published-<날짜> 마커로 막는다. 재료 파일이 아니라 발행 마커를 기준으로 삼아, push 가 실패한 날은 재실행이 다시 시도한다.
- seen 표시는 push 성공 뒤로 옮겼다(task-80 에서는 재료 생성 직후였다). 중간에 실패한 날의 항목이 다음 날 다시 후보가 되어야 한다.
- ERR 트랩이 죽은 줄 번호를 로그와 Slack 양쪽에 남긴다. LC_ALL·pipefail 관련 조용한 죽음은 단계별 echo 로 위치가 드러난다.
- 전용 클론은 ~/jobs/liv-briefing/repo, add 는 항상 경로 명시다.

검증: 로컬 bare 저장소를 remote 로 두고 클론 생성 → 렌더 → 커밋 → push 를 완주했고, 헤드리스 Firefox 스크린샷으로 레이아웃(2칼럼·개요·til 연관·리브 한마디·훑고 넘긴 것)을 눈으로 확인했다. 실제 공개 저장소로의 첫 발행은 아직 하지 않았다 — 내일 09:00 cron 이 첫 판을 올린다.

페이지 용량은 84KB 로 task-81 에서 잡은 40KB 목표를 넘겼다. 실측해 보니 용량을 정하는 것은 자산(29KB)이 아니라 본문(57KB)이라 자산만 줄여서는 못 내려간다. 상한을 100KB 로 고쳐 잡고 보존 정책(무기한 누적, 연 30MB)은 유지했다 — README 와 render.py 에 반영.
<!-- SECTION:NOTES:END -->
