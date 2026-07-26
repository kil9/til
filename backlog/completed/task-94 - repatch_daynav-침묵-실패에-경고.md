---
id: TASK-94
title: repatch_daynav 침묵 실패에 경고
status: Done
assignee: []
created_date: '2026-07-26 09:45'
updated_date: '2026-07-26 09:46'
labels: []
milestone: m-10
dependencies: []
priority: high
ordinal: 94000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
render.py 의 repatch_daynav() 는 DAYNAV 마커를 못 찾으면 False 만 돌려주고 잡은 정상 종료한다. 템플릿에서 마커 이름이 바뀌거나 사라지면 '어제 페이지에 다음 링크가 영영 안 생김' 이 조용히 발생한다. 직전 회차가 있는데 패치가 되지 않으면 stderr 에 경고를 찍는다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 직전 회차 페이지가 있는데 DAYNAV 마커를 못 찾으면 stderr 에 어느 파일인지 포함한 경고가 나온다
- [x] #2 이미 올바른 내비가 들어 있어 바뀔 것이 없는 정상 경우에는 경고가 나오지 않는다
- [x] #3 마커를 지운 사본으로 실제 재현해 경고를 확인한다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
repatch_daynav() 가 bool 대신 'patched'/'unchanged'/'no-marker'/'missing' 을 돌려주고, main() 이 unchanged·patched 가 아닌 결과를 stderr 경고로 올린다. 검증: 가짜 2026-07-25 회차를 만들어 (A) 정상 재발행에서는 경고가 없고 (B) 그 페이지의 DAYNAV 마커를 지운 뒤 재발행하면 'no-marker' 경고가 파일 경로와 함께 뜨는 것을 확인했다. render.py 는 머신 로컬(~/jobs/liv-briefing/, repo 밖)이라 이 커밋에는 태스크 파일만 들어간다.
<!-- SECTION:NOTES:END -->
