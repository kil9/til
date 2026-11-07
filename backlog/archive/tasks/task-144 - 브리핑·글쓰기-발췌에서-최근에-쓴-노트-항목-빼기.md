---
id: TASK-144
title: 브리핑·글쓰기 발췌에서 최근에 쓴 노트 항목 빼기
status: Done
assignee: []
created_date: '2026-10-23 17:10'
updated_date: '2026-10-23 17:16'
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
- [x] #1 liv-notes.py excerpt 가 최근 발행 리브 문장(또는 그 경로)을 받아 겹치는 노트를 발췌에서 뺀다
- [x] #2 브리핑 compose 가 직전 3회차의 리브 문장을 넘겨, 10-10·10-21 의 실제 입력으로 재현하면 꿀벌·우편 노트가 빠진다
- [x] #3 퍼블리시 런북(AGENTS.md §2-2)의 발췌 명령도 같은 옵션을 쓴다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
excerpt --avoid-recent N: 최근 브리핑 N회·루트 카드 순 아티클 N편의 .liv 코멘트를 읽어, 코멘트마다 노트와의 겹침을 IDF 가중 합(어간은 3자 이상이면 끝 글자를 뗀다)으로 재고 최대값이 26 이상인 노트를 발췌에서 뺀다. 이어 붙여 재면 길이만큼 잡음이 커져(64건 제외) 코멘트별 최대로 바꿨다. 임계 근거: 10월 브리핑 실측에서 실제 재사용 28-53, 우연한 겹침 25 이하. 재현(--avoid-before): 10-10 기준 n-0046(꿀벌)·n-0049(꿀 시럽), 10-21 기준 n-0113(우편)·n-0096 이 빠진다. 배선: 브리핑 compose.py(nuc14, 백업 compose.py.bak-avoid)·til-inbox watcher/run.sh(1954e60, test-run PASS)·AGENTS.md §2-2 런북 명령.
<!-- SECTION:NOTES:END -->
