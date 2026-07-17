---
id: TASK-20
title: 리브 풀네임 노출 축소 및 '성인 투데이는' 문장 개고
status: Done
assignee: []
created_date: '2026-07-17 06:23'
updated_date: '2026-07-17 06:44'
labels:
  - solo
dependencies: []
ordinal: 20000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
풀네임 '리브 투데이'는 소개 페이지(/liv-today/)의 자기소개부(인사말·이름 유래)와 공개 설정화 페이지(/liv-today/sheet/)에만 유지하고, 그 외 모든 자리(liv-today meta description 2곳, 루트 index.html 아바타 alt, liv-today 내 삽화 alt 등)는 '리브'로 통일한다. 아울러 liv-today/index.html:88 의 이름 유래 문장 '성인 투데이는…' 이 '성인(adult)'으로 오독될 수 있으므로 표현을 다듬는다(예: 성(姓) 표기를 풀어 쓰는 방식 등, 자연스러운 문장으로). 호칭 운용 규칙(풀네임은 소개·설정화 페이지에서만)을 진실원본 doc-3 과 AGENTS.md §2-2 에 반영한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 풀네임 텍스트 노출이 /liv-today/ 자기소개부와 /liv-today/sheet/ 로 한정되고 나머지(메타·alt 포함)는 '리브'로 통일된다
- [x] #2 '성인 투데이는' 문장이 오독 없이 자연스럽게 개고된다
- [x] #3 doc-3 과 AGENTS.md §2-2 에 풀네임 호칭 운용 규칙이 기록된다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
퍼블리시 페이지의 풀네임 노출을 /liv-today/ 인사말과 /liv-today/sheet/ 로 한정. 개정: liv-today 메타 2곳·삽화 alt 3곳, 루트 인덱스 카드 설명·아바타 alt, moshi·voice·kil9conf 바이라인, kb16-bootloop·notosanskr 인사 문장. '성인 투데이는' → '제 성(姓)인 투데이는' 으로 개고. 운용 규칙을 doc-3 §1 과 AGENTS.md §2-2 에 기록. 결정: README·AGENTS·doc-3 등 저장소 문서는 캐릭터를 정의하는 자리라 풀네임 유지, backlog/assets legacy 보존본도 불변.
<!-- SECTION:NOTES:END -->
