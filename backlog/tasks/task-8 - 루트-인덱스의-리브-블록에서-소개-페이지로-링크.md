---
id: TASK-8
title: 루트 인덱스의 리브 블록에서 소개 페이지로 링크
status: To Do
assignee: []
created_date: '2026-07-15 10:13'
labels: []
dependencies:
  - TASK-7
priority: medium
ordinal: 8000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
루트 index.html 히어로의 .keeper 블록(아바타 + 이름 + 한 줄 소개)을 클릭하면 리브 소개 페이지(/liv-today/)로 이동하게 한다. 지금은 정적 텍스트라 리브가 누구인지 알아볼 경로가 없다.

링크 대상이 새 슬러그이므로 TASK-7 이후에 진행한다. 사이트가 극한 미니멀 톤이므로 카드처럼 박스를 두르지 말고 기존 a.card 의 hover 규칙(제목에 액센트 컬러 + 밑줄)과 같은 결로 처리한다. 아바타·소개 문구를 포함한 블록 전체가 클릭 영역이 되는 편이 자연스럽다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 .keeper 블록이 /liv-today/ 로 링크되고, hover·focus-visible 스타일이 기존 갤러리 카드 규칙과 일관된다
- [ ] #2 로컬 미리보기로 라이트/다크와 키보드 포커스 이동을 확인한다
- [ ] #3 AGENTS.md 런북의 .keeper 설명에 소개 페이지 링크라는 사실을 반영한다
<!-- AC:END -->
