---
id: DRAFT-7
title: 브리핑 본문의 em-dash 정리
status: Draft
assignee: []
created_date: '2026-08-06 08:05'
labels: []
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
loop-backlog 자동 추가(2026-08-06, task-106 작업 중 발견).

저장소 규약은 외부로 나가는 글에서 em-dash 를 금지하는데, 데일리 브리핑 회차에는 회차당 7-19개가 들어 있다(2026-08-04 7개 / 08-05 19개 / 08-06 16개 실측). compose 프롬프트에 금지 규칙이 없어서다. 주간 리캡은 task-117 에서 프롬프트에 금지를 넣었다.

이 태스크에서 손대지 않은 이유: HN 도입과 무관한 선행 조건이고, 프롬프트 한 줄이지만 모든 회차의 문장 리듬이 바뀌는 변경이라 별건으로 보는 것이 맞다.

완료 조건: compose 프롬프트가 em-dash 를 금지하고, 발행 회차 1건에서 0개임을 확인한다. 기존 발행분은 소급하지 않는다(리브 캐릭터 규칙의 소급 정책과 같다).
<!-- SECTION:DESCRIPTION:END -->
