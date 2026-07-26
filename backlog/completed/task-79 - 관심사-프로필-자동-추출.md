---
id: TASK-79
title: 관심사 프로필 자동 추출
status: Done
assignee: []
created_date: '2026-07-26 03:55'
updated_date: '2026-07-26 07:36'
labels:
  - solo
milestone: m-8
dependencies:
  - TASK-78
priority: medium
ordinal: 79000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
루트 index.html 의 카드 data-topic·.tag·제목에서 관심사 프로필을 뽑는 스크립트를 만든다. 파일럿에서는 손으로 뽑았다(AI 15·워크플로 10·하드웨어 7·터미널 5·시스템 3·경제 3·사이트 2·읽을거리 2 + 세부 축). 자동화하면 글이 쌓일수록 프로필이 따라 움직인다. 최근 글에 가중치를 주는 방식(예: 최근 3개월 2배)을 검토한다. 출력은 선별 프롬프트에 그대로 끼울 수 있는 텍스트/JSON.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 til 카드에서 주제 분포와 세부 축을 뽑는 스크립트가 있다
- [x] #2 최근 글 가중 여부를 결정하고 근거를 남겼다
- [x] #3 출력이 선별 단계 프롬프트에 그대로 들어가는 형태다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
backlog/assets/interest-profile.py 추가. 루트 index.html 카드(data-topic·data-date·.tag·h2·p)를 파싱해 주제 비중·세부 축·최근 글 제목을 뽑는다. --format prompt(기본, 선별 프롬프트에 그대로 붙임) / --format json 두 출력.

가중치 결정: 지수 감쇠(반감기 90일)를 채택하고 누적 건수를 함께 출력한다. 계단식('최근 3개월 2배')은 til 발행이 몰아치는 패턴이라 경계 하루 차이로 주제 순위가 튀어서 버렸다. 47건 기준 가중 비중은 AI 32%·워크플로 22%·하드웨어 15%·터미널 10%·시스템/경제 6%·읽을거리 4%·사이트 3% 로, 파일럿에서 손으로 센 분포와 순위가 일치한다(발행이 최근 한 달에 몰려 있어 아직 감쇠 효과가 작다).

세부 축은 .tag 의 '·' 뒤 세그먼트를 주제별로 모아 중복을 접고 최근순 8개까지.
<!-- SECTION:NOTES:END -->
