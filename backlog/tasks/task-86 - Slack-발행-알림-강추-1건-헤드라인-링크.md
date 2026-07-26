---
id: TASK-86
title: Slack 발행 알림 (강추 1건 + 헤드라인 + 링크)
status: Done
assignee: []
created_date: '2026-07-26 07:27'
updated_date: '2026-07-26 08:07'
labels:
  - solo
milestone: m-9
dependencies:
  - TASK-85
priority: high
ordinal: 86000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
브리핑이 push 되면 Slack #til 로 리브가 알린다. 형식은 강추 1건(제목 + 왜 권하는지 한 줄) + 나머지 항목 제목을 한 줄로 압축 + 페이지 링크. 전문을 싣지 않는 이유는 알림 피로를 만들지 않고 실제로 페이지를 열게 하기 위함이다.

기존 자산: til-submit 워처가 이미 Slack #til 로 접수·완료를 알리고 있고, 리브 봇(hermes-gateway-liv, 표시명 '리브')이 있다. 같은 앱·같은 말투로 보낸다. 발행 실패 시에도 같은 채널로 알린다(task-85 의 실패 통지).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 발행 성공 시 강추 1건 + 헤드라인 + 링크가 #til 로 간다
- [x] #2 리브 봇 계정·말투로 나가며 기존 접수 알림과 톤이 일관된다
- [x] #3 발행 실패 시 원인 요약이 같은 채널로 간다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
announce.py 를 추가하고 run.sh 가 push 성공 뒤에 부른다(파일이 없으면 건너뛰도록 가드가 있어 순서 의존이 없다).

형식: 굵게 처리한 날짜 헤더 + 훑은/실은 건수 → 강추 1건(제목 + pick.line 의 이유 한 줄) → 나머지 헤드라인을 ' · ' 로 이어 한 줄(부제를 떼고 26자에서 자른다. 폰 알림에서 읽는 글이다) → 페이지 링크. 전문은 싣지 않는다.

발신은 til-submit 과 같은 배관이다: ~/.hermes/profiles/liv/.env 의 SLACK_BOT_TOKEN 우선, ~/.hermes/.env 폴백, 채널 C0BJUAH0Y7J(#til).

실패 통지는 run.sh 쪽이다. ERR 트랩이 죽은 줄 번호를, push 3회 실패는 별도 문구를 같은 채널로 보낸다.

검증: auth.test 로 봇 신원(livtoday, team todolbi)과 conversations.info 로 #til 참여를 확인했고 메시지 본문은 --dry-run 으로 확인했다. 실제 발신은 하지 않았다 — 페이지가 아직 안 올라간 상태에서 '올려 두었습니다' 라고 보내면 링크가 404 다. 첫 실제 메시지는 첫 발행과 함께 나간다.
<!-- SECTION:NOTES:END -->
