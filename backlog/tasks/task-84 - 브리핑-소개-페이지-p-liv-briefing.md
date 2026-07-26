---
id: TASK-84
title: 브리핑 소개 페이지 (p/liv-briefing/)
status: Done
assignee: []
created_date: '2026-07-26 05:49'
updated_date: '2026-07-26 08:11'
labels:
  - solo
milestone: m-8
dependencies:
  - TASK-81
priority: low
ordinal: 84000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
데일리 브리핑에서 빼낸 상설 정보를 담는 페이지. 선정 기준(관심사 축 + 추천 백분위 축, 2-5건 clamp), 현재 관심사 프로필, 수집 범위와 정리 모델, 액션 버튼이 무엇을 하는지. 브리핑 footer 에서 한 줄로 링크한다. 매일 같은 정보를 데일리 페이지에서 반복하지 않기 위한 자리다(Fable 자문 결론).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 p/liv-briefing/ 페이지가 있고 선정 기준·관심사 프로필·수집 범위가 서술돼 있다
- [x] #2 관심사 프로필은 자동 추출 결과(task-79)를 반영해 갱신된다
- [x] #3 데일리 브리핑 footer 에서 이 페이지로 링크한다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
p/liv-briefing/ 페이지를 만들었다. 브리핑에서 매일 반복될 상설 정보를 전부 이쪽으로 뺐다: 무엇을 하는가(08:40 재료·09:00 발행·Slack 알림), 어떻게 고르는가(추천 축 p90 2-5건 · 관심사 축 · 정렬은 백분위 1순위), 지금의 관심사 프로필, 수집 범위와 정리 모델(Opus 5), 버튼이 하는 일.

프로필 구간은 <!-- PROFILE:START -->\~END 마커이고 render.py 의 update_profile 이 발행 때마다 interest-profile.py 결과로 덮어쓴다(주제별 비중·세부 축·표본 수·기준일). 손으로 적어 두면 글이 쌓일수록 낡는다. 루트 index.html 의 AI-SUMMARY 마커와 같은 방식이다.

브리핑 footer 는 이미 이 페이지로 링크하고 있었고(template.html), 이 페이지에서도 오늘의 브리핑·지난 브리핑·리브 소개로 돌아가는 링크를 둔다. 갤러리 카드로는 내보내지 않는다 - 브리핑과 같은 이유(상설 지원 페이지)다.
<!-- SECTION:NOTES:END -->
