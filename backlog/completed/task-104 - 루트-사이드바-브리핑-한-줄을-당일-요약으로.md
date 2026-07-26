---
id: TASK-104
title: 루트 사이드바 브리핑 한 줄을 당일 요약으로
status: Done
assignee: []
created_date: '2026-07-26 14:18'
updated_date: '2026-07-26 14:31'
labels: []
dependencies:
  - TASK-103
priority: medium
ordinal: 2000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
루트 index.html 사이드바 '오늘의 브리핑' 아래 문구가 '리브가 아침마다 인터넷을 훑어 골라 둔 것들 →' 이라는 고정 안내문이다. 이 사이트는 사실상 관리자 전용이라 첫 방문자용 안내보다 오늘 브리핑에 무엇이 들어 있는지 한 문장이 낫다.

배관: 사이드바는 이미 p/briefing/latest.json 을 fetch 해 안 읽은 회차 배지를 켠다(task-93). 그 JSON 에 요약 한 문장 필드를 추가하고 같은 fetch 에서 .briefing-line 텍스트를 갈아끼우면 루트 index.html 을 매일 커밋할 필요가 없다. 문장은 발행 잡(nuc14 ~/jobs/liv-briefing/compose.py)이 그날 브리핑 전체를 보고 별도로 생성해 render.py 가 latest.json 에 쓴다 — 강추 1건 재활용이 아니라 회차 전체를 대표해야 하고, 사이드바 폭(260px)에 맞는 길이여야 한다. fetch 실패나 필드 없는 구버전 JSON 이면 HTML 에 박힌 현재 안내문구가 그대로 남는다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 p/briefing/latest.json 에 당일 브리핑을 한 문장으로 요약한 필드가 들어가고, 발행 잡이 회차마다 새로 채운다
- [ ] #2 루트 사이드바 '오늘의 브리핑' 아래 줄이 그 문장으로 표시된다 — 기존 latest.json fetch 를 재사용하고 요청을 늘리지 않는다
- [ ] #3 fetch 실패·필드 누락 시 HTML 에 박힌 기존 안내문구가 그대로 보이고 빈 줄이 생기지 않는다
- [ ] #4 backlog/assets/briefing/README.md 에 latest.json 스키마와 이 문장의 생성 주체가 적힌다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
latest.json 에 line 추가(compose 의 sidebar → render_archive). 루트 index.html 은 기존 배지 fetch 하나를 재사용해 .briefing-line 을 갈아끼우고, 실패·필드 누락 시 HTML 의 상설 문구가 그대로 남는다. 2026-07-26 회차는 sidebar 를 손으로 채워 재렌더해 latest.json 을 curl 로 확인. 브라우저 렌더 확인은 연결된 Chrome 이 원격(Windows/macOS)이라 localhost 서버에 닿지 않아 생략했다.
<!-- SECTION:NOTES:END -->
