---
id: TASK-13
title: '루트 인덱스 사이드바 순서 변경: 리브 소개 · kil9 · 리브의 코멘트'
status: Done
assignee: []
created_date: '2026-07-16 19:24'
updated_date: '2026-07-16 19:39'
labels:
  - solo
dependencies: []
priority: medium
ordinal: 13000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
현재 루트 index.html 의 aside.side 는 리브의 코멘트(AI-SUMMARY 마커 구간) → 리브 소개(a.keeper) → kil9(.human) 순이다. 저자 소개가 먼저 오고 코멘트가 뒤따르도록 리브 소개 → kil9 → 리브의 코멘트 순으로 재배치한다.

접근: aside.side 안의 마크업 블록 순서를 바꾸고, 지금 a.keeper 가 갖고 있는 border-top 구분선을 .ai-summary 쪽으로 옮긴다(소개 두 블록은 붙이고 코멘트 앞에만 구분선). a.keeper 는 사이드바 최상단이 되므로 margin-top/padding-top 도 함께 정리한다.

주의: AI-SUMMARY 마커 구간은 머신 로컬 잡(~/jobs/docs-ai-summary/inject.py)이 통째로 덮어쓴다. inject.py 는 '<!-- AI-SUMMARY:START -->.*?<!-- AI-SUMMARY:END -->' 를 re.subn 으로 치환하는 마커 기반이라 위치 이동 자체는 안전하지만, 마커 주석 쌍은 그대로 유지해야 하고 마커 안의 마크업은 손대지 않는다. 구분선은 마커 바깥(.ai-summary CSS)에서 준다.

AGENTS.md 의 사이드바 구조 설명(§2-2 마지막 문단, '사이드바 위쪽이 리브의 코멘트, 그 아래가 a.keeper …')도 새 순서에 맞게 고친다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 루트 index.html 의 aside.side 가 리브 소개(a.keeper) → kil9(.human) → 리브의 코멘트(.ai-summary) 순으로 렌더링된다
- [x] #2 AI-SUMMARY:START/END 마커 쌍이 그대로 유지되고, 마커 안 마크업은 변경되지 않는다
- [x] #3 구분선(border-top)이 .ai-summary 앞에만 있고, 리브 소개와 kil9 블록 사이에는 여백만 있다
- [x] #4 a.keeper 가 최상단이 되면서 어색해진 margin-top/padding-top 이 정리돼 있다
- [x] #5 920px 이하 반응형(사이드바가 order:-1 로 목록 위)에서도 세 블록 순서·여백이 깨지지 않는다
- [x] #6 AGENTS.md 의 사이드바 구조 설명이 새 순서와 일치한다
<!-- AC:END -->
