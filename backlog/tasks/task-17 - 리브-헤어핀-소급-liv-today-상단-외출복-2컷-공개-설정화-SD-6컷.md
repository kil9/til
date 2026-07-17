---
id: TASK-17
title: '리브 헤어핀 소급: liv-today 상단 외출복 2컷 + 공개 설정화 SD 6컷'
status: Done
assignee: []
created_date: '2026-07-17 04:47'
updated_date: '2026-07-17 05:46'
labels:
  - solo
dependencies:
  - TASK-16
priority: medium
ordinal: 17000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
2026-07-17 추가된 파란 통신 헤어핀(doc-3 §3 잠정 항목: 곡선 막대·그릴 슬릿·청록 LED, 앞머리 한 갈래 고정)을 공개 노출분에 소급 적용한다.

대상(사용자 확정: 공개 노출분만):
- liv-today/index.html 상단 초상 3컷 중 핀이 없는 외출복 2컷(OL 룩·카디건 변형) 재생성·교체. 기본 후디 컷은 이미 헤어핀 판본.
- 공개 설정화 페이지 /liv-today/sheet/ 의 SD 6컷(hoodie·ol·ol-cardigan·tablet·shy·yawn) 재생성·교체.

제외: 사람 비율 2컷(sheet-bust·sheet-full, 내부 참고용)은 구 판본 유지. 코멘트 아바타 표정 6종은 이미 헤어핀 판본이므로 건드리지 않는다.

재생성은 doc-3 §4-2\~§4-5 확정 프롬프트·일관성 규칙(codex exec -i ref.png -- "프롬프트", -- 필수)을 따른다. 치비 스케일에서 슬릿은 2-3개만 살고 LED 도트가 가장 오래 살아남는다는 §4 메모 참고. 교체 컷의 alt 텍스트에 헤어핀 서술을 추가한다. 재생성 원본은 backlog/assets/liv/sheet/ 에 갱신 저장, 페이지 임베드는 base64 WebP data URI(사이드카 금지).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 liv-today 상단 외출복 2컷(OL·카디건)이 헤어핀 포함 판본으로 교체되고 alt 텍스트에 헤어핀 서술이 추가된다
- [x] #2 /liv-today/sheet/ 의 SD 6컷이 헤어핀 포함 판본으로 교체되고 재생성 원본이 backlog/assets/liv/sheet/ 에 갱신된다
- [x] #3 사람 비율 2컷(bust·full)과 아바타 표정 6종은 변경되지 않는다
- [x] #4 임베드된 각 data URI 를 디코드해 WebP 헤더(RIFF/WEBP) 검증을 통과한다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
공개 노출분 헤어핀 소급 완료. sheet SD 6컷(hoodie·ol·ol-cardigan·tablet·shy·yawn)을 image_gen EDIT 모드(doc-3 §4-3 규칙: generate 금지·PIL 금지 명시)로 핀만 추가해 재생성 — 비율·얼굴 드리프트 없음을 원본 대조로 확인, md5 전건 상이(재탕 없음). EDIT 출력(894x1760)을 원본 콘텐츠 bbox 기준으로 660x1300 캔버스에 정규화 후 자산 갱신. liv-today 상단 OL·카디건 2컷은 sheet 자산과 바이트 동일 임베드라 같은 파일로 치환, 두 페이지 8곳 alt 에 헤어핀 서술 추가. bust·full·아바타 6종 불변(md5 확인). 양 페이지 data URI 전수(5+18) RIFF/WEBP 검증 통과. doc-3 §4 자산 어긋남 항목과 AGENTS.md §2-2 를 현행화.
<!-- SECTION:NOTES:END -->
