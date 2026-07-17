---
id: TASK-25
title: 'Slack #TIL 알림: tdb_bot 토큰으로 접수·시작·완료·실패 전송'
status: To Do
assignee: []
created_date: '2026-07-17 07:27'
labels:
  - solo
milestone: m-1
dependencies:
  - TASK-24
priority: medium
ordinal: 25000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
워처 잡에 Slack 알림을 붙인다. ~/.hermes/.env 의 SLACK_BOT_TOKEN(Infisical 관리)으로 chat.postMessage 를 호출해 #TIL 채널에 접수 감지·처리 시작·완료(결과 URL)·실패(에러 요약) 4시점을 알린다. 토큰은 평문 노출 금지(변수 참조만). #TIL 채널 존재와 tdb_bot 멤버십을 확인하고, 없으면 채널 생성+봇 초대를 사용자 액션으로 안내한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 #TIL 채널 존재·봇 멤버십이 확인된다(필요 시 사용자 액션 안내 후)
- [ ] #2 접수·시작·완료·실패 4시점 알림이 #TIL 에 전송된다
- [ ] #3 토큰이 스크립트·로그·커밋 어디에도 평문 노출되지 않는다
<!-- AC:END -->
