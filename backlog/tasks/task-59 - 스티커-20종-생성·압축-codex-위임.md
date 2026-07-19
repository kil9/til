---
id: TASK-59
title: 스티커 20종 생성·압축 (codex 위임)
status: To Do
assignee: []
created_date: '2026-07-19 06:23'
labels: []
milestone: m-6
dependencies:
  - TASK-58
priority: medium
ordinal: 59000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
TASK-58 에서 확정한 스펙·포즈 목록대로 codex 이미지 생성(image_generation)에 위임해 스티커를 만든다. 기존 SD 컷(로우 번·헤어핀 판본)을 ref 로 넣어 doc-3 §4 일관성 규칙을 따른다(codex exec -i ref.png -- "프롬프트" 의 -- 누락 주의). 투명 배경 + 흰 다이컷 테두리 처리 후 원본·소형 판본을 WebP 로 압축해 backlog/assets/liv/stickers/ 에 저장한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 확정 포즈 전 종이 생성되어 backlog/assets/liv/stickers/ 에 원본·소형 판본으로 저장된다
- [ ] #2 전 파일이 투명 배경(알파)·흰 테두리·규격 크기·용량 목표를 충족하고 WebP 헤더(RIFF/WEBP) 검증을 통과한다
- [ ] #3 화풍·헤어(로우 번)·헤어핀이 기존 SD 컷과 일관된다
<!-- AC:END -->
