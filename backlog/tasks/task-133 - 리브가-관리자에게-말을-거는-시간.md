---
id: TASK-133
title: 리브가 관리자에게 말을 거는 시간
status: In Progress
assignee: []
created_date: '2026-10-04 03:00'
updated_date: '2026-10-04 03:31'
labels: []
milestone: m-15
dependencies:
  - TASK-132
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
관리자 구상: 리브가 알아서 찾아본 뒤 관리자와 얘기할 시간을 갖는다. 산책에서 건진 것 중 관리자와 나누고 싶은 것을 리브가 골라 먼저 말을 걸고(채널 후보: 기존 리브 Slack 봇 m-2), 관리자의 답·반응을 노트에 반영해 다음 산책과 글에 이어지게 한다. 일방 보고(브리핑)가 아니라 대화라는 점이 핵심이다 — 리브가 의견을 갖고 묻거나 권한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 산책 뒤 리브가 이야기할 거리를 골라 관리자에게 먼저 말을 거는 경로가 동작한다
- [ ] #2 관리자의 답이 노트에 기록되어 다음 산책·글쓰기에 반영된다
- [x] #3 말 걸기 빈도에 상한이 있어 관리자가 답하지 않아도 쌓여서 부담을 주지 않는다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
2026-10-04 구현: nuc14 ~/jobs/liv-walk/talk.py (send 12:30 · collect 07-23시 10분 간격 cron).
- send: 그날 walk-<날짜>.json 의 talk 후보를 리브 봇 토큰으로 DM 최상위 메시지로 보낸다. context 줄에 출처 링크와 '스레드로 답해 주시면 이어서 얘기합니다'. 하루 1번(state/talks.json), 마지막 답 이후 답 없는 말 걸기 2건이면 쉰다, 3일 무응답이면 unanswered 로 닫는다.
- 대화: Hermes Slack 어댑터(_fetch_thread_context)가 스레드 답장 때 봇이 쓴 부모 메시지도 맥락에 넣는 것을 코드로 확인 — 리브가 무슨 얘기를 꺼냈는지 알고 답한다.
- collect: 스레드 답(없으면 3시간 안의 DM 최상위)을 읽고 마지막 답 후 30분이 지나면 Sonnet(도구 없음, 잠금 동일)이 공개용 요약 1-2문장으로 바꿔 kind=talk 로 노트에 add·render·push. 개인 경험·회사 일화·이름은 빼고 관점만 — 가짜 대화로 요약 시험 시 이름은 빠졌고 회사 일화가 남아 규칙을 조였다.
- 첫 전송: 2026-10-04 12:30 (멱등성 키 얘기, ts=1791084602.747039). 중복 send 거부·답 없을 때 collect 무동작 확인. cron 최소 PATH 에서 claude 호출 확인.
남은 것: AC2 — 관리자님 답이 실제로 노트에 기록되는 것을 확인해야 닫는다.
<!-- SECTION:NOTES:END -->
