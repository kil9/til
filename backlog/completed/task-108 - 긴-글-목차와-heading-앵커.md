---
id: TASK-108
title: 긴 글 목차와 heading 앵커
status: Done
assignee: []
created_date: '2026-07-26 10:25'
updated_date: '2026-07-26 16:06'
labels:
  - solo
milestone: m-11
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
아티클 49건 중 h2 에 id 가 있는 것이 9건뿐이다. 5천 자 넘는 페이지가 여럿인데 목차가 없고, 특정 절을 링크로 가리킬 수도 없다. h2 에 슬러그 id 를 자동 부여하고 앵커 링크를 붙이고, h2 가 일정 개수 넘는 글에만 상단 목차를 넣는다. TASK-98·TASK-100 과 같은 소급 후처리 스크립트에 얹는 것이 자연스럽다(draft-1 도 같은 배관). id 는 URL 에 박히므로 한글 heading 의 슬러그 규칙을 먼저 정해야 한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 후처리 스크립트가 아티클 h2 에 한글 슬러그 id 를 자동 부여한다(공백은 하이픈, 문장부호 제거, 한글은 그대로 둔다)
- [x] #2 각 h2 에 그 절을 가리키는 앵커 링크가 붙어 클릭·복사로 URL 을 얻을 수 있다
- [x] #3 h2 가 5개 이상인 글에만 상단 목차 블록을 넣는다
- [x] #4 이미 id 가 있는 h2 9건의 기존 id 는 바뀌지 않는다(그 값으로 나간 링크가 깨지지 않는다)
- [x] #5 같은 제목의 h2 가 둘 이상이면 뒤에 -2, -3 을 붙여 id 충돌을 막는다
- [x] #6 마커 구간 방식이라 재실행이 멱등이고, 전 아티클에 소급 적용된다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
확정 사항(2026-07-27 승격 인터뷰):
- id 규칙: 한글을 그대로 쓴 슬러그(예: id="그래프가-값을-내는-조건"). 주소창에서는 퍼센트 인코딩되지만 붙여넣으면 복원되고, 링크만 봐도 어디로 가는지 읽힌다. h2 순번(sec-N)은 절을 넣고 빼면 기존 링크가 다른 절을 가리켜 배제했다.
- 목차 임계: h2 5개 이상. 짧은 글에서는 목차가 소음이다.

배관은 TASK-98·TASK-100 과 같은 소급 후처리(backlog/assets/relink-pages.py 계열, 마커 구간 덮어쓰기)에 얹는다. id 는 URL 에 박히므로 규칙 변경은 이후 되돌리기 어렵다.

TASK-109 와 같은 스크립트를 건드릴 가능성이 높아 둘 다 solo 로 둔다.

완료(2026-07-27):
- relink-pages.py 에 rewrite_headings()/toc_html()/unsplice() 추가. 아티클 49건에 소급 적용.
- id 규칙: 한글 그대로 슬러그(소문자화·문장부호 제거·공백→하이픈). 앞머리 번호는 뺀다 — '3. ' 판본과 <span class="n">3</span> 판본 둘 다. 번호를 넣으면 절을 하나 끼워 넣을 때 아래 id 가 전부 밀려 링크가 통째로 깨진다(태스크가 sec-N 을 배제한 것과 같은 이유).
- 기존 수동 id 9건 보존: 우리가 붙인 id 에만 data-anchor="auto" 를 달고 그것만 매번 재계산한다. 표시가 없는 id 는 손대지 않는다.
- 목차는 h2 5개 이상일 때만 <!-- PAGETOC:START --> 구간으로 첫 h2 앞에, CSS 는 <!-- PAGETOC-CSS:START --> 구간에. 임계 미달 페이지에 남아 있으면 걷어낸다.
- 목차 라벨은 번호가 붙은 원문 제목을 그대로 쓴다. CSS counter 로 번호를 매기면 '1. 1. 제목' 이 되어 뺐다.
- h2 범위는 <main>(없으면 <body>) 안으로 제한 — footer·하단 내비의 h2 를 건드리지 않는다.
- 검증: 아티클 전수 스캔(id 누락 0·중복 0·앵커 수=h2 수·목차 임계와 링크 대상 일치), 유닛 테스트(동일 제목 3개 → -2/-3, 수동 id 유지, footer 미변경, 2회 실행 멱등), 스크립트 2회 연속 실행 diff 동일, 헤드리스 Firefox 로 목차 링크 5개 전부 h2 로 해석되고 퍼센트 인코딩된 한글 프래그먼트로 해당 절에 정확히 착지(top=0).
- 갤러리 카드가 없는 herdr-pane-tradeoffs-anime 는 기존 og:image·하단 내비와 같은 기준으로 대상 밖이다.
- 곁가지: search-index.py 가 앵커의 '#' 를 색인에서 빼도록 보강(목차는 <nav> 라 이미 제외).
<!-- SECTION:NOTES:END -->
