---
id: TASK-44
title: 리브 전용 hermes 프로필 생성·구성
status: Done
assignee: []
created_date: '2026-07-18 05:54'
updated_date: '2026-07-18 06:15'
labels: []
milestone: m-4
dependencies:
  - TASK-43
priority: high
ordinal: 44000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
hermes profile create 로 리브 독립 인스턴스를 만든다(별도 HERMES_HOME). 삐약이 기본 프로필 불간섭.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 hermes profile create 로 리브 전용 프로필(독립 HERMES_HOME) 생성
- [x] #2 config.yaml 에 provider=Claude 구독·모델 설정
- [x] #3 .env 에 리브 Slack 봇/앱 토큰(~/.liv/.env 재사용) 주입, 게이트웨이가 리브 앱으로 Socket Mode 연결 확인
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
완료 (2026-07-18). 리브 전용 hermes 프로필 생성·구성.
- 프로필: 'liv' at ~/.hermes/profiles/liv (독립 HERMES_HOME), wrapper ~/.local/bin/liv, 72 bundled skills. 삐약이 기본 프로필(~/.hermes)·bland-ai 불간섭.
- config.yaml: model.default=claude-sonnet-5, model.provider=anthropic, model.base_url=https://api.anthropic.com. 구독 OAuth 는 전역 ~/.claude/.credentials.json 자동 발견(프로필 .env 에 종량제 키 없음). 스모크: 'liv -z' → LIV_PROFILE_OK (구독 서빙).
- .env: ~/.liv/.env 의 SLACK_APP_TOKEN(xapp-)·SLACK_BOT_TOKEN(xoxb-) 재사용 주입, chmod 600. hermes 도 동일 var 명 사용.
- Socket Mode 연결 실증: (a) Slack API 비파괴 검증 — auth.test ok(team=todolbi, user=liv, bot_id=B0BJ5JW0BEW), apps.connections.open ok(wss URL 발급). (b) 기존 liv-bot 잠시 stop → 'liv gateway run' 기동 → workspace todolbi(team T0B512YJWCD) 인증 성공, 인증된 API 호출 도달, auth 실패 0 → gateway kill → liv-bot restart(active, Bolt 재연결). 이중 Socket Mode 회피 위해 브리지.
발견(→TASK-47): 현 liv 앱 스코프 app_mentions:read,chat:write,im:write,im:history,im:read 뿐이라 channel_directory 가 users.conversations 에서 missing_scope(needed: channels:read), 그룹DM 은 mpim:history/message.mpim 누락 경고. hermes 스레드 무멘션엔 channels:history/read + message.channels(+mpim) 필요 — TASK-47 대상.
<!-- SECTION:NOTES:END -->
