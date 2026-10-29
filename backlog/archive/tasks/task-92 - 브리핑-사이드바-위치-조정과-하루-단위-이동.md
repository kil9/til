---
id: TASK-92
title: 브리핑 사이드바 위치 조정과 하루 단위 이동
status: Done
assignee: []
created_date: '2026-07-26 09:21'
updated_date: '2026-07-26 09:27'
labels: []
dependencies: []
ordinal: 92000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
루트 사이드바의 '오늘의 브리핑' 블록을 리브의 코멘트 아래로 내리고, 브리핑 페이지에 이전/다음 날 이동 내비를 발행 시점 정적 생성으로 넣는다. 아카이브 인덱스(p/briefing/archive/)는 그대로 유지한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 루트 index.html 사이드바에서 .briefing 블록이 .ai-summary 아래에 온다(AI-SUMMARY 마커 구간은 건드리지 않는다)
- [x] #2 브리핑 날짜 페이지에 이전/다음 날 링크가 정적 HTML 로 들어간다
- [x] #3 새 회차를 발행하면 직전 날짜 페이지의 '다음' 링크가 마커 구간 교체로 채워진다
- [x] #4 최신판(p/briefing/index.html)에도 이동 내비가 있고 상대경로가 날짜판과 어긋나지 않는다
- [x] #5 render.py 로 기존 회차를 재렌더해 링크가 실제로 열린다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
사이드바의 '오늘의 브리핑' 블록을 리브의 코멘트 아래(월별 목차 위)로 이동하고, 문구에서 GeekNews 를 빼 '인터넷을 훑어'로 바꿨다(소스가 늘어날 예정). 브리핑 페이지 하단에 하루 단위 이동 내비를 넣었다 — template.html 의 {{DAYNAV}} + DAYNAV 마커, render.py 의 daynav()/repatch_daynav() 가 발행 시점에 정적 생성하고 새 회차가 나오면 직전 회차의 '다음' 링크만 갈아끼운다. run.sh 는 그 패치가 커밋에서 빠지지 않게 p/briefing 을 통째로 add 한다. 검증: 가짜 2026-07-25 회차를 만들어 재렌더해 양방향 링크(../2026-07-26/, ../2026-07-25/)와 최신판의 ./2026-07-25/ 경로를 확인한 뒤 정리했다. 아카이브 인덱스는 사용자 결정으로 유지.
<!-- SECTION:NOTES:END -->
