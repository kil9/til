---
id: TASK-8
title: 루트 인덱스의 리브 블록에서 소개 페이지로 링크
status: Done
assignee: []
created_date: '2026-07-15 10:13'
updated_date: '2026-07-15 10:46'
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
- [x] #1 .keeper 블록이 /liv-today/ 로 링크되고, hover·focus-visible 스타일이 기존 갤러리 카드 규칙과 일관된다
- [x] #2 로컬 미리보기로 라이트/다크와 키보드 포커스 이동을 확인한다
- [x] #3 AGENTS.md 런북의 .keeper 설명에 소개 페이지 링크라는 사실을 반영한다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
히어로의 .keeper 를 <section> 에서 <a class="keeper" href="./liv-today/"> 로 바꿔 아바타·이름·소개문을 감싼 블록 전체를 클릭 영역으로 만들었다. 사이트 톤대로 박스를 두르지 않고 a.card 규칙을 그대로 따랐다 — hover 시 .keeper-name 에 액센트 컬러 + 밑줄(a.card:hover h2 와 동일), focus-visible 은 2px 액센트 아웃라인 + offset 4px(a.card 와 동일). aria-label 은 '지식 큐레이터 소개' → '리브 투데이 소개 페이지로 이동' 으로 링크임이 드러나게 고쳤다.

검증(로컬 미리보기 + Chrome): 라이트/다크 모두 hover 시 이름이 액센트+밑줄로 전환됨을 확인. 페이지 첫 Tab 으로 블록 전체에 액센트 아웃라인이 잡히고, Enter 로 /liv-today/ 이동됨을 확인.

AGENTS.md §2-2 의 .keeper 설명에 링크라는 사실과 hover 규칙 근거를 반영.
<!-- SECTION:NOTES:END -->
