---
id: TASK-30
title: 'liv-today 바쁜 날 삽화 수정: 모니터 뒷면이 보이도록 재생성'
status: Done
assignee: []
created_date: '2026-07-17 09:17'
updated_date: '2026-07-17 09:22'
labels: []
dependencies: []
ordinal: 30000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
liv-today/index.html 의 '바쁜 날의 저입니다' 삽화(원본 backlog/assets/liv/illust-work-busy.webp)에서 리브가 시청자를 향해 앉아 모니터를 보는 구도인데, 모니터 화면 콘텐츠가 시청자 쪽으로 보여 공간적으로 어색하다. 모니터 뒷면이 시청자에게 보이도록 이미지를 수정(재생성)한다. doc-3 §4 의 codex 이미지 편집 레시피(-i ref -- 프롬프트)를 따른다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 수정된 삽화에서 모니터 뒷면이 시청자에게 보이고 화면 콘텐츠가 보이지 않는다
- [x] #2 리브의 외형(복장·헤어핀·표정)과 화풍이 원본과 일관된다
- [x] #3 liv-today/index.html 의 base64 임베드가 새 이미지로 교체되고 WebP 헤더(RIFF/WEBP) 디코드 검증을 통과한다
- [x] #4 원본 자산 backlog/assets/liv/illust-work-busy.webp 도 새 판본으로 갱신된다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
codex image_gen EDIT 모드로 illust-work-busy 를 수정 — 시청자 쪽으로 보이던 모니터 화면 콘텐츠(파란 UI 블록)를 제거하고 진회색 백패널+스탠드(뒷면)로 교체, 캐릭터·책상·키보드·종이·창문·화풍은 원본 유지. md5 대조로 재탕 아님 확인, 결과 눈검사 통과. liv-today/index.html 임베드를 1440px WebP q75(56KB, 기존 61KB 에서 감소)로 교체하고 페이지 내 전 data URI 6건 RIFF/WEBP 헤더 검증 통과. 원본 자산 backlog/assets/liv/illust-work-busy.webp 도 신판(q90, 110KB)으로 갱신.
<!-- SECTION:NOTES:END -->
