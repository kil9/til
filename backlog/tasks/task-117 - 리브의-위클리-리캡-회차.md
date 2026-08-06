---
id: TASK-117
title: 리브의 위클리 리캡 회차
status: To Do
assignee: []
created_date: '2026-08-06 05:51'
labels:
  - solo
milestone: m-13
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
AIwitness 위클리(https://aiwitness.kr/weekly)를 참고한 주 1회 리캡 회차. 데일리 브리핑이 항목 나열이라면, 위클리는 그 주 회차들을 재료로 흐름을 서사로 엮는 판단 메모다.

참고한 형식(7월 5주차 회차 실측):
- 캐치한 두 줄 헤드라인("1점 차이, 80% 인하 — 이번 주 경쟁은 벤치마크가 아니라 가격표에서 벌어졌다")
- 요일별 타임라인(월~일, 사건 한 줄씩)
- '이번 주 이야기' 2-3편 — 개별 항목을 맥락으로 엮은 서사, 모든 주장에 인라인 출처 링크

검토할 것:
- 경로: p/briefing/weekly/<식별자>/ 형태가 자연스럽다. 데일리와 같은 noindex·갤러리 미노출 정책을 따를지, 아카이브(p/briefing/archive/)에 어떻게 섞을지 결정.
- 재료: 그 주 데일리 회차의 수집·선별 데이터(nuc14 ~/jobs/liv-briefing/ 산출물)를 재사용한다. 원문 재수집 없이 compose 만 주간 단위로 한 번 더 돈다.
- 발행 요일: AIwitness 는 화요일. 브리핑 리듬(매일 09:00)에 맞춰 정한다.
- 리브 화자: 데일리보다 서사가 길어지므로 캐릭터 규칙(드물수록 효과가 크다)을 지키면서 판단 메모 어투를 잡는다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 위클리 경로·노출·발행 요일 정책이 backlog/assets/briefing/README.md 에 문서화된다
- [ ] #2 위클리 템플릿이 backlog/assets/briefing/ 에 추가되고 렌더가 값을 채운다(데일리 템플릿과 셸 공유 여부는 재량)
- [ ] #3 재료는 그 주 데일리 회차의 수집·선별 데이터를 재사용하고 원문을 재수집하지 않는다
- [ ] #4 회차 구성에 헤드라인·요일 타임라인·이야기 2편 이상이 있고, 이야기의 근거 항목은 해당 데일리 회차 앵커로 링크된다
- [ ] #5 위클리 발행 실패가 데일리 발행을 막지 않고 그 역도 성립한다
- [ ] #6 실제 발행 회차 1건 이상이 나온다
<!-- AC:END -->
