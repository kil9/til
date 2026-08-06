---
id: DRAFT-5
title: 리캡 Slack 재공지 가드
status: Draft
assignee: []
created_date: '2026-08-06 06:15'
labels: []
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
loop-backlog 자동 추가(2026-08-06, task-117 작업 중 발견).

recap.sh 는 state/recap-published-<날짜> 마커로 재발행은 막지만, 마지막 줄의 'python3 recap.py $REPO $TODAY --announce' 에는 가드가 없다. 스크립트를 다시 돌리면(수동 재실행, cron 중복 등) 이미 공지한 리캡의 Slack 알림이 또 나간다. 데일리 쪽은 state/announced-<날짜> 마커가 있어 이 문제가 없다.

완료 조건: 리캡도 데일리와 같은 방식으로 공지 마커를 두고, 마커가 있으면 --announce 를 건너뛴다. 발행 자체가 실패한 회차는 다음 실행에서 정상적으로 공지된다.

지금 당장 아프지 않은 이유: 리캡은 주 1회이고 재실행 경로가 사실상 수동뿐이다. task-117 의 완료 조건에도 들어 있지 않다.
<!-- SECTION:DESCRIPTION:END -->
