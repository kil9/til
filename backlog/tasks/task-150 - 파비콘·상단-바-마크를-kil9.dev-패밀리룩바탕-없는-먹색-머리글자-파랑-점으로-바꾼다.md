---
id: TASK-150
title: 파비콘·상단 바 마크를 kil9.dev 패밀리룩(바탕 없는 먹색 머리글자 + 파랑 점)으로 바꾼다
status: To Do
assignee: []
created_date: '2026-11-07T02:22:00Z'
labels: []
dependencies: []
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
요청 원문: "다른 사이트들도 같은 패밀리룩으로" (접수 2026-11-07, health.kil9.dev 세션에서)

패밀리룩 정의(health·quant 에 반영 완료): 파비콘은 16×16 viewBox 에 바탕 없이(투명) 사이트 머리글자를 먹색(Pretendard Bold 글리프를 path 로)으로, 오른쪽 아래에 파랑 점(.kil9.dev 를 뜻함). 수치는 health 와 같게 — 글자 배율 13.4/1448(0.00925), 가로 중심 6.2, 세로 중심 7.5, 점 x12.2 y10.6 한 변 3.6. 색은 라이트 글자 먹색·점 #2457c5, 다크(SVG 안 prefers-color-scheme) 글자 #eceef0·점 #7ea6ff. 상단 바 워드마크는 '[12px 마크] <사이트>(700) .kil9.dev(400 옅은 먹색)' 이고 마크는 파비콘과 같은 글자+점이다.
정본: ~/work/kil9/health.kil9.dev/web/favicon.svg·mockups/favicon/gen.py(시안 E), ~/work/kil9/quant.kil9.dev/ops/render_favicon.py(글리프 추출·파비콘과 상단 바 마크를 함께 갈아 끼우는 생성기, 마크 색은 CSS 로 칠해 사이트 테마를 따름). 홈 화면 앱 아이콘(apple-touch-icon·icon-192/512, 다섯 사이트 공통 가족 아이콘)은 범위 밖이다.

이 사이트: til.kil9.dev(GitHub Pages, 정적). 지금 파비콘은 페이지마다 <link rel=icon> 에 data:image/webp base64 가 박혀 있다 — 루트에 favicon.svg 하나를 두고 모든 페이지(2026/·pages/·topics/·404 등, 생성 스크립트가 있으면 그 템플릿)가 그것을 참조하게 바꾼다. 머리글자는 t.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 파비콘이 바탕 없는 먹색 머리글자 + 파랑 점이고 health·quant 와 같은 배율·점 위치·색(라이트·다크)을 쓴다
- [ ] #2 상단 바 워드마크가 '[마크] <사이트> 굵게 + .kil9.dev 보통·옅은 먹색' 이고 마크가 파비콘과 같은 글자·점이다(좁은 화면에서 넘치면 .kil9.dev 를 숨긴다)
- [ ] #3 주요 화면을 넓은·좁은(390px) 폭 × 라이트·다크로 캡처해 넘침·콘솔 오류가 없고 그 repo 의 테스트가 통과한다
<!-- AC:END -->
