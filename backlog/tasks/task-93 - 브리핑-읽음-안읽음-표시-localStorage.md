---
id: TASK-93
title: 브리핑 읽음/안읽음 표시 (localStorage)
status: Done
assignee: []
created_date: '2026-07-26 09:27'
updated_date: '2026-07-26 09:34'
labels: []
dependencies: []
ordinal: 93000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
독자가 사실상 관리자 1명이므로 인증 없이 브라우저 localStorage 에 방문한 회차 날짜를 기록해 읽음/안읽음을 구분한다. 페이지를 열면 읽음. 표시는 루트 사이드바(안 읽은 회차가 있을 때 점)와 p/briefing/archive/ 목록(읽은 행 흐리게).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 브리핑 회차 페이지를 열면 그 날짜가 localStorage 에 읽음으로 기록된다
- [x] #2 p/briefing/archive/ 목록에서 읽은 회차와 안 읽은 회차가 시각적으로 구분된다
- [x] #3 루트 사이드바 '오늘의 브리핑' 블록에 안 읽은 회차가 있을 때만 표시가 붙는다
- [x] #4 JS 가 없거나 저장소가 막힌 브라우저에서도 레이아웃이 깨지지 않는다(표시만 생략)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
localStorage 키 liv-briefing-read 에 방문 회차 날짜를 배열로 쌓는다(회차 페이지 로드 즉시). 표시는 두 곳: 루트 사이드바 배지(.briefing-new, p/briefing/latest.json 의 최신 회차를 안 읽었을 때만)와 아카이브 목록 행 구분(.row.read 흐리게 / .row.unread 앞점). 루트 index.html 에 최신 날짜를 박지 않고 latest.json 을 따로 둔 것은 AI 요약 잡이 같은 파일을 매일 덮어쓰기 때문이다. 검증: 브라우저가 다른 머신이라 페이지에 실제로 박힌 스크립트 조각을 떼어 스텁 DOM(node)에서 돌렸다 — 방문 기록 append, 아카이브 unread/read 분류, 배지 hidden=false/true 가 기대대로 나왔다. 관련 JS 는 모두 try/catch(또는 promise catch) 안이라 저장소가 막혀도 표시만 빠진다. 눈으로 보는 확인은 사용자 브라우저 몫.
<!-- SECTION:NOTES:END -->
