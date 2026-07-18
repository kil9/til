---
id: TASK-44
title: 리브 전용 hermes 프로필 생성·구성
status: To Do
assignee: []
created_date: '2026-07-18 05:54'
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
- [ ] #1 hermes profile create 로 리브 전용 프로필(독립 HERMES_HOME) 생성
- [ ] #2 config.yaml 에 provider=Claude 구독·모델 설정
- [ ] #3 .env 에 리브 Slack 봇/앱 토큰(~/.liv/.env 재사용) 주입, 게이트웨이가 리브 앱으로 Socket Mode 연결 확인
<!-- AC:END -->
