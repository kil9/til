---
id: TASK-59
title: 스티커 20종 생성·압축 (codex 위임)
status: Done
assignee: []
created_date: '2026-07-19 06:23'
updated_date: '2026-07-19 07:51'
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
- [x] #1 확정 포즈 전 종이 생성되어 backlog/assets/liv/stickers/ 에 원본·소형 판본으로 저장된다
- [x] #2 전 파일이 투명 배경(알파)·흰 테두리·규격 크기·용량 목표를 충족하고 WebP 헤더(RIFF/WEBP) 검증을 통과한다
- [x] #3 화풍·헤어(로우 번)·헤어핀이 기존 SD 컷과 일관된다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
18종 생성 완료(backlog/assets/liv/stickers/, 원본 512px 386KB + 소형 256px 184KB). 5건 이하 배치 5회로 나눠 돌렸고 유사 포즈(O/X, 박스/종이더미)는 서로 다른 배치에 배치했다. md5 전수 상이로 재탕 없음, WebP RIFF 헤더·RGBA 알파(0-255) 전수 검증 통과, 화풍·로우 번·헤어핀 일관성 유지. 재생성 4컷(circle-ok 팔이 머리에 붙어 O 막힘, cross-no X가 팔짱으로 읽힘, toss-paper 휴지통이 분리돼 bbox 벌어짐, chin-rest 헤어핀 2개) — 넷 다 1024px 원본에선 멀쩡했고 128px 로 줄여서야 드러났다. 실패 사례·회피책은 doc-3 §4-6 '18종 실측'에 기록. diecut.py 는 리사이즈 후 링을 두르도록 고쳐 컷당 40초에서 5초로 줄였다.
<!-- SECTION:NOTES:END -->
