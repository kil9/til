---
id: TASK-144
title: 브리핑·글쓰기 발췌에서 최근에 쓴 노트 항목 빼기
status: To Do
assignee: []
created_date: '2026-10-23 17:10'
labels: []
milestone: m-15
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
TASK-134 확인 중 발견(2026-10-24): '같은 항목 연속 사용 금지'가 문체 규칙에만 있어 브리핑에서 같은 노트가 이틀 연속 쓰였다(꿀벌 8자 춤 10-09·10-10, 우편 창구 10-20·10-21). 발췌 단계에서 최근 발행분의 리브 문장과 겹치는 노트를 빼면 모델이 고를 수 없게 된다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 liv-notes.py excerpt 가 최근 발행 리브 문장(또는 그 경로)을 받아 겹치는 노트를 발췌에서 뺀다
- [ ] #2 브리핑 compose 가 직전 3회차의 리브 문장을 넘겨, 10-10·10-21 의 실제 입력으로 재현하면 꿀벌·우편 노트가 빠진다
- [ ] #3 퍼블리시 런북(AGENTS.md §2-2)의 발췌 명령도 같은 옵션을 쓴다
<!-- AC:END -->
