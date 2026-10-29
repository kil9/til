---
id: TASK-28
title: 제출 페이지 토큰 재설정을 우상단 톱니바퀴 메뉴로 이동
status: Done
assignee: []
created_date: '2026-07-17 09:06'
updated_date: '2026-07-17 09:07'
labels:
  - solo
milestone: m-1
dependencies: []
priority: medium
ordinal: 28000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
사용자 피드백: 폼 아래 상시 노출된 '토큰 재설정' 버튼은 실수로 누르기 쉽다. 우상단 톱니바퀴(설정) 버튼을 추가하고, 누르면 열리는 메뉴 안에서만 토큰 재설정이 가능하도록 옮긴다. 메뉴 밖 클릭 시 닫힘, aria-expanded 등 접근성 유지.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 폼 하단 상시 노출 재설정 버튼이 제거된다
- [x] #2 우상단 톱니바퀴 클릭 → 메뉴의 '토큰 재설정' 클릭 2단계로만 재설정된다
- [x] #3 메뉴 밖 클릭으로 닫히고 라이트/다크 모두 자연스럽다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
폼 하단 상시 재설정 버튼 제거. 우상단 톱니(octicon gear, currentColor·hover 액센트) + 드롭다운 메뉴(토큰 재설정 1항목), 밖 클릭 닫힘, aria-expanded/haspopup. 재설정 시 메뉴 닫고 '토큰을 지웠습니다' 안내 후 등록 패널로 전환. 헤드리스 렌더로 기본·열림 상태 확인.
<!-- SECTION:NOTES:END -->
