---
id: TASK-16
title: 'liv-today 하단 개편: 설정화 컷 제거, 리브 일상 신규 삽화 2컷'
status: Done
assignee: []
created_date: '2026-07-17 04:46'
updated_date: '2026-07-17 05:31'
labels:
  - solo
dependencies: []
priority: medium
ordinal: 16000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
https://kil9.github.io/til/liv-today/ 하단(본문 중간 이후)에 흩어진 설정화 시트 유래 SD 컷 3개(태블릿·머쓱·하품)는 시선을 분산시키므로 제거한다 — 설정화 페이지(/liv-today/sheet/)에서 볼 수 있으면 충분하다. 대신 리브의 일상·업무 신규 삽화 2컷을 그려 넣는다: ① 집에서 평소처럼 릴랙스하는 모습, ② 바쁘게 일하는 모습(지루하다는 표정을 지으려 하지만 내심 새로운 지식을 얻는 것이 즐거운 기색이 새어 나오는).

창의성 방침(사용자 확정): SD 치비 비율과 핵심 포인트(헤어핀·후디 등)는 유지하되, 배경·소품·구도·연출은 기존 설정화 틀(흰 바탕 정면 입상)에서 벗어나 자유롭게 그린다. 기존 컷과 너무 똑같이 나오지 않도록 일관성이 조금 깨지는 것은 감수한다.

생성 레시피는 doc-3 §4-2\~§4-5(codex exec -i ref.png -- "프롬프트", -- 필수)를 따르되 프롬프트는 장면에 맞게 변주. 신규 컷이므로 헤어핀 판본으로 생성한다. 원본은 backlog/assets/liv/ 에 보관하고 페이지에는 base64 WebP(q75, 폭 1440px 이하 적정) data URI 로 임베드(사이드카 금지).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 liv-today/index.html 본문에서 설정화 시트 유래 SD 컷 3개(태블릿·머쓱·하품 figure)가 제거된다
- [x] #2 신규 일상 삽화 2컷(집 릴랙스 1, 바쁘게 일하지만 내심 즐거운 1)이 SD 치비 + 파란 통신 헤어핀 포함으로 생성되어 본문에 임베드되고, 원본이 backlog/assets/liv/ 에 저장된다
- [x] #3 새 컷은 배경·소품·구도에서 기존 설정화 컷과 뚜렷이 구분된다(흰 바탕 정면 입상 반복 아님)
- [x] #4 임베드된 각 data URI 를 디코드해 WebP 헤더(RIFF/WEBP) 검증을 통과하고, 페이지는 외부 리소스 없는 단일 파일로 유지된다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
liv-today 본문에서 설정화 유래 SD 3컷(태블릿·계면쩍음·하품) 제거. 신규 일상 삽화 2컷을 codex generate(기준본 liv-final-chibi 참고)로 생성해 교체 임베드: '하는 일' 섹션에 바쁜 작업 컷(카디건 작업복, 시큰둥하려는데 즐거움이 새는 표정), '그럼' 섹션에 집 릴랙스 컷(후디, 소파+쿠션+벗어둔 슬리퍼). 릴랙스 컷은 1차 생성이 3등신으로 드리프트해 비율 부정형 강화로 1회 재생성해 채택. 원본은 backlog/assets/liv/illust-home-relax.webp·illust-work-busy.webp(1536x1024 q90), 임베드는 1440px WebP q75(각 60-65KB). 검증: 페이지 data URI 5건 전부 RIFF/WEBP 헤더 OK, 외부 리소스는 CF beacon 뿐, md5 로 재탕 아님 확인.
<!-- SECTION:NOTES:END -->
