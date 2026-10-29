---
id: TASK-3
title: 설정화 시트 제작
status: Done
assignee: []
created_date: '2026-07-15 04:55'
updated_date: '2026-07-15 09:13'
labels: []
milestone: m-0
dependencies:
  - TASK-2
priority: high
ordinal: 3000
---

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 확정 스타일로 전신 1장, 상반신 1장, 표정 변형 3종 이상을 캐릭터 일관성을 유지하며 생성한다
- [x] #2 각 이미지를 폭 1440px 이하 WebP(q75, 장당 약 70-100KB)로 압축해 임베드 가능한 형태로 준비한다
- [x] #3 결과 시트를 사용자에게 전달해 승인받고, 최종 프롬프트·생성 파라미터를 설정 문서에 기록한다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
T-2 확정본을 참고 이미지로 넣어 전신·상반신·표정 3종(미소/계면쩍음/눈반짝)×원본·치비 = 8컷을 codex 로 생성(캐릭터 일관성 유지 확인). 8건 동시 실행 중 2건 model-at-capacity 실패 → 순차 재시도로 회수. 전 컷 1024x1536, WebP q75 24-67KB 로 backlog/assets/liv/sheet/ 보존. 원본 비율 눈반짝 컷 1회 재생성(하이라이트 강조+설레는 미소) 후 8장 전체 사용자 승인. doc-3 §4-3 에 컷 구성·프롬프트·파라미터·운용 팁 기록. AC 3/3 체크.
<!-- SECTION:NOTES:END -->
