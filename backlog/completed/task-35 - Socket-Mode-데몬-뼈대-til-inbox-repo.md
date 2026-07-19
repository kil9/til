---
id: TASK-35
title: Socket Mode 데몬 뼈대 (til-inbox repo)
status: Done
assignee: []
created_date: '2026-07-17 20:30'
updated_date: '2026-07-17 21:39'
labels: []
milestone: m-2
dependencies:
  - TASK-33
priority: high
ordinal: 35000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
til-inbox repo 에 slack_bolt Socket Mode 데몬을 얹는다. 멘션·DM 수신 → 에코까지 되는 최소 골격.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 til-inbox repo 에 리브 봇 데몬 스캐폴딩
- [x] #2 slack_bolt Socket Mode 로 app_mention·DM 수신 확인(에코 응답)
- [x] #3 토큰은 ~/.hermes/.env 런타임 참조, 평문 커밋 금지
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
til-inbox bot/liv_daemon.py (커밋 55585fb). slack_bolt 1.30.0 Socket Mode 데몬. 멘션→스레드 에코, DM→flat 에코. 토큰 ~/.liv/.env 런타임 참조(평문 커밋 없음). 봇↔봇 루프 방지+신뢰봇 allowlist(LIV_ALLOW_BOT_IDS), _dedup 재전송 중복방지, 수신 로그. 검증: #til 멘션→'(echo) …' 스레드 왕복 E2E 확인(테스트 메시지 삭제 정리). 부수 처리: liv 를 #til 에 tdb_bot 토큰 conversations.invite 로 초대(비멤버였음). 실 바이너리 ~/.local/bin/claude, venv ~/.liv/venv. DM 경로는 봇끼리 cannot_dm_bot 라 헤드리스 자동검증 불가하나 코드는 채널과 대칭.
<!-- SECTION:NOTES:END -->
