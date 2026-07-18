---
id: TASK-49
title: 별도 게이트웨이 systemd + 기존 리브 데몬 전환
status: Blocked
assignee: []
created_date: '2026-07-18 05:55'
updated_date: '2026-07-18 06:59'
labels: []
milestone: m-4
dependencies:
  - TASK-45
  - TASK-46
  - TASK-47
priority: medium
ordinal: 49000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
리브 프로필 게이트웨이를 상시 구동하고 기존 standalone liv-bot.service 를 은퇴시킨다. 워크스페이스에 hermes 인스턴스 난입·중복 알림 이력(todolbi task-6)이 있어 인스턴스 충돌에 유의.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 hermes-liv-gateway.service(리브 프로필) systemd user 유닛 신설·enable·상시구동
- [ ] #2 기존 liv-bot.service disable/stop 은퇴, 두 인스턴스 동시 수신 방지
- [ ] #3 워크스페이스 인스턴스 충돌(중복 알림 등) 없음 확인, 재부팅 후 자동기동
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
TASK-47(Blocked, 사용자 조치)에 의존하는 라이브 커토버 — 구동 중 liv-bot.service 를 은퇴시키는 되돌리기 어려운 outward 작업이라 사용자 오버사이트로 수행. TASK-47 재설치와 한 세션에서 이어감.

현황(2026-07-18 확인): 실행 게이트웨이는 삐약이 기본 프로필(HERMES_HOME=~/.hermes, PID 1205885, 5일째)뿐. stray liv 게이트웨이 없음(TASK-44 브리지 테스트 프로세스 정리됨). 기존 standalone liv-bot.service active. 이중 Slack 수신 없음.
주의: 'hermes gateway status' 는 프로세스 매칭이 프로필 구분을 안 해(둘 다 'gateway run') liv/default 를 헷갈릴 수 있음 — 커토버 검증은 systemd 유닛 + Slack 앱 active connections 로 확인.

## 커토버 절차 (TASK-47 재설치·새 xoxb 반영 후)
1. liv gateway install --no-start-now --start-on-login  → hermes-liv-gateway systemd user 유닛 신설(부팅 자동기동 enable, 아직 미기동). (AC#1)
2. systemctl --user stop liv-bot.service && systemctl --user disable liv-bot.service  → 기존 봇 은퇴. (AC#2)
3. systemctl --user start <hermes-liv-gateway 유닛>  → 신규 기동. (두 인스턴스 동시 수신 방지: 반드시 2 다음 3)
4. 검증(AC#3): liv Slack 앱 스레드에 멘션 없이 메시지 → 리브가 1회만 응답(중복 없음). journalctl 로 게이트웨이 로그 확인. 리부트 후 자동기동 확인.
5. TASK-42 하드닝(systemd 샌드박싱 등)은 이 신규 유닛에 적용 검토.

의존: TASK-45(SOUL)·TASK-46(툴잠금) Done, TASK-47(스코프) 선행 필요.

[Fable advisor MUST-FIX #1, 크리티컬] 툴 스키마는 **게이트웨이 프로세스의 HERMES_HOME** 에서 빌드된다(source.profile 아님; gateway/run.py:16781 _load_gateway_config). 따라서 리브 슬랙 게이트웨이는 반드시 **전용 프로세스 HERMES_HOME=~/.hermes/profiles/liv** 로 떠야 TASK-46 잠금이 문다. 현재 라이브 게이트웨이 둘 다 글로벌(~/.hermes)이며, 리브가 글로벌 멀티플렉서로 서빙되면 잠금이 **무효**가 되고 글로벌 config(platform_toolsets.slack:[hermes-slack]=풀툴) + 글로벌 MCP(hass-mcp HA작동·grafana)가 임의 Slack 입력에 노출된다.
커토버 검증 필수: (1) 'liv gateway install' 이 만든 systemd 유닛의 Environment 에 HERMES_HOME=~/.hermes/profiles/liv 확인, (2) 기동 후 실제 프로세스 env(/proc/PID/environ)로 HERMES_HOME 재확인, (3) 리브 앱에 셸/파일 injection 시도해 차단 실증, (4) test_toolset_lockdown.py 를 그 HERMES_HOME 으로 재실행.
<!-- SECTION:NOTES:END -->
