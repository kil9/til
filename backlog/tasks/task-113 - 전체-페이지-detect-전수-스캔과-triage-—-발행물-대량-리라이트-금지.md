---
id: TASK-113
title: 전체 페이지 detect 전수 스캔과 triage — 발행물 대량 리라이트 금지
status: Done
assignee: []
created_date: '2026-07-28 16:25'
updated_date: '2026-07-28 18:01'
labels: []
milestone: m-12
dependencies:
  - TASK-112
priority: medium
ordinal: 7000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
index.html(갤러리)·404.html 과 2026/ 전체(53페이지)를 npx impeccable detect 로 전수 스캔한다. 자체 완결형 페이지가 많아 수 분 이상 걸리니 백그라운드로 돌린다. 규칙별로 집계한 뒤 (1) 갤러리·공용 자산은 수정, (2) 이미 발행된 개별 글은 가독성·명도 대비처럼 실해가 있는 것만 고치고 나머지는 inline ignore 로 waive 하거나 방치한다 — 발행물 대량 리라이트 작업을 만들지 않는다. 집계와 처리 방침은 backlog doc 으로 남긴다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 전수 스캔의 규칙별 집계와 처리 방침이 backlog doc 으로 남는다
- [x] #2 갤러리(index.html)와 공용 자산이 detect 를 통과한다
- [x] #3 기존 글 수정은 가독성·대비 등 실해가 있는 것으로 한정된다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
전수 스캔(77파일, 약 9분) 총 485건. 집계·처리 방침 정본은 doc-4.
수정(실해만): low-contrast 10파일 — p/til-archive 다크 --text-faint #647178(3.4:1) → #828F98(4.7-5.6:1), plan-pipeline 9파일 --ink-3 #767d8c(4.42:1) → #7d8493(4.87:1). tiny-text — til-archive 0.72rem → 0.8125rem. broken-image — submit 페이지의 src="" 를 1x1 투명 GIF placeholder 로(속성을 빼면 규칙이 다시 걸린다). p/archive 격자 커버 radius 10px → 8px(공용 자산이라 이관 잔재 취급 안 함).
waive(.impeccable/config.json, 커밋됨): single-font·flat-type-hierarchy 전역(웹폰트 미사용·압축 타입 스케일이 확정 정책), index.html 0.5rem 글리프, 2026/**의 tiny-text(전부 인라인 SVG 차트 라벨이라 오탐), opus5-skill-rework all-caps-body(Label 역할).
design-system-* 4종 241건은 전역 waive 하지 않았다 — 끄면 TASK-114 게이트가 신규 페이지 램프 이탈도 못 잡아 도입 목적이 사라진다. 기존 페이지는 게이트가 안 보므로 끌 이유도 없다.
em-dash-overuse 27건은 waive 하지 않고 남겼다. 규칙상 위반이 맞지만 고치려면 본문 27편 재작성이라 금지 범위이고, advisory 라 발행을 막지 않는다. 알려진 부채로 doc-4 §5 에 기록.
검증: npx impeccable detect index.html 404.html p/archive/ → 0 findings, exit 0.
전체 재스캔은 사용자 판단으로 생략했다(개별 확인은 완료).
<!-- SECTION:NOTES:END -->
