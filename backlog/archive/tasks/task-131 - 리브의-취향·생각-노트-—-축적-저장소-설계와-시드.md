---
id: TASK-131
title: 리브의 취향·생각 노트 — 축적 저장소 설계와 시드
status: Done
assignee: []
created_date: '2026-10-04 03:00'
updated_date: '2026-10-04 03:19'
labels: []
milestone: m-15
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
리브가 글에서 끌어 쓸 '할 말'의 원천. 지금 리브의 내면은 doc-3 의 성격 설정뿐이라 코멘트가 아카이브 자기언급으로 수렴한다(task-130). 관리자 구상: 토큰을 좀 써서라도 리브의 취향·생각을 조금씩 쌓아 나가 할 말이 생기게 한다.
설계 범위: 무엇을 담나(좋아하게 된 것·싫은 것·요즘 꽂힌 것·구경하다 본 것과 한 줄 감상·관리자와 나눈 얘기·생각이 바뀐 기록), 어디에 두나(커밋 vs 머신 로컬, 공개 여부), 크기를 어떻게 다스리나(컨텍스트에 통째로 넣지 않고 최근분+요약 발췌로 주입 — task-123 의 경량화 원칙), 성격 설정(doc-3)과의 경계(노트는 설정을 덮어쓰지 않고 그 위에 쌓인다).
착수 시 검토 필요: 노트의 공개 여부는 관리자 결정 사항이다(공개면 '리브의 산책 노트' 같은 페이지 후보, 비공개면 글감 저장소에 그친다).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 노트의 스키마(항목 종류·필드)·위치·공개 여부·크기 관리 방식이 문서로 확정된다
- [x] #2 기존 아카이브 115건과 브리핑에서 리브가 보인 반응을 근거로 초기 취향 시드 항목이 채워진다
- [x] #3 글쓰기 경로가 노트를 읽을 때 쓰는 발췌 방식(최근분·관련분만)이 정의된다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
설계 doc-5(스키마 6종 kind·필드, 위치, 공개, 발췌), 결정 decision-10(관리자 결정: 반 숨김 공개·repo 커밋·산책은 구독 쿼터 새벽 Opus $3/30분·말 걸기 Slack DM 하루 1번·미답 2건 쉼).
도구 backlog/assets/liv-notes.py(add·excerpt --for write|walk·render·check). 발췌는 덮인 항목 제외, 2400자 상한(취향 8건은 유지), walk 모드는 최근 14일 도메인·태그를 피할 목록으로 준다.
시드 20건: 아카이브 코멘트(moshi·space-datacenter·backslash-won-sign·elevator 등)와 9-10월 브리핑 반응에서 like 8·dislike 4·into 3·saw 4, 그리고 '두 번 원칙'을 changed 로 덮어 task-130 집계를 노트에 남겼다.
페이지 p/liv-walk/ 렌더, p/liv-today footer 에 흐린 링크. site-check 위반 없음, 1280/390 스크린샷 확인.
<!-- SECTION:NOTES:END -->
