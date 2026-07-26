---
id: TASK-91
title: 주간 리캡
status: Done
assignee: []
created_date: '2026-07-26 07:28'
updated_date: '2026-07-26 08:35'
labels:
  - solo
milestone: m-9
dependencies:
  - TASK-85
priority: low
ordinal: 91000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
일요일에 그 주 브리핑을 훑어 관통하는 흐름 한 편을 쓴다. 일간 브리핑은 그날 안에서만 보므로 며칠에 걸쳐 이어지는 추세를 놓친다(이번 주만 해도 오픈 웨이트 모델의 추격이 여러 날 걸쳐 나왔다).

일간과 다른 점은 형식이다. 항목 나열이 아니라 산문 한 편이고, 잘 나오면 그 자체로 til 페이지가 될 수 있다. 그 경우 브리핑 경로가 아니라 <YYYY>/<slug>/ 로 정식 게시할지 판단하는 단계를 둔다 — 자동으로 갤러리에 올리지는 않는다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 주 1회 그 주 브리핑을 종합한 리캡이 생성된다
- [x] #2 항목 나열이 아니라 흐름을 서술하는 산문 형식이다
- [x] #3 til 정식 게시로 승격할지 판단하는 단계가 있고 자동 게시하지 않는다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
recap.py + recap.sh, cron 20 9 * * 0(일요일, 그날 발행 뒤). 그 주 브리핑이 3회 미만이면 관통할 흐름이 없다고 보고 만들지 않는다.

- 형식: 항목 나열이 아니라 산문 3-6문단이고 소제목을 써도 된다. 프롬프트에 '월요일에는… 화요일에는… 식으로 날짜를 따라가지 마라', '이번 주 재료로 뒷받침되지 않는 일반론을 쓰지 마라' 를 명시했다. 페이지는 til 본문과 같은 720px 셸(backlog/assets/briefing/recap.html)에 마무리 리브 코멘트 하나와 출처(그 주 브리핑 목록)를 단다.
- 경로는 p/briefing/recap/<날짜>/ 이고 noindex, 갤러리 미노출이다. 아카이브 페이지 맨 위에 '주간 리캡' 묶음으로 따로 나온다(일간과 형식이 달라 섞지 않았다).
- 승격은 자동으로 하지 않는다. 모델이 '브리핑을 안 읽은 사람이 읽어도 남는 것이 있는가' 로 판단해 recommend/why/slug 를 내고, Slack 메시지에 판단과 함께 til-inbox submit 프리필 링크를 붙인다. 누르는 것은 관리자다.
- push 재시도 시 모델을 다시 부르지 않는다(state/recap-<날짜>.json 캐시 재사용). Slack 알림은 push 성공 뒤에 --announce 로 따로 보낸다 — 그전에 보내면 링크가 404 다.

검증: 합성 주간(3회분)으로 생성해 산문 품질·승격 판단·페이지 렌더·아카이브 노출·알림 문구까지 확인했다. 실제 첫 리캡은 브리핑이 3회 쌓인 뒤 첫 일요일에 나온다.
<!-- SECTION:NOTES:END -->
