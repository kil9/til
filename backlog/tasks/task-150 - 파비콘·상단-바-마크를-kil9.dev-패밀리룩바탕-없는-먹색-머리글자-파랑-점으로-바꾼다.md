---
id: TASK-150
title: 파비콘·상단 바 마크·설치 아이콘을 kil9.dev 패밀리 아이콘(리브)으로 바꾼다
status: Done
assignee: []
created_date: '2026-11-07T02:22:00Z'
updated_date: '2026-11-07T05:57:00Z'
labels: []
dependencies: []
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
kil9.dev 패밀리 아이콘(liv TASK-7, 2026-11-07 확정)으로 파비콘·상단 바 마크·홈 화면 설치 아이콘을 바꾼다.

정본: ~/work/kil9/liv/design/family-icons/ — README.md 에 기조·수치·파일 용도, out/til/ 에 favicon.svg·mark.svg·app-icon.svg·apple-touch-icon.png(180)·icon-192.png·icon-512.png·icon-maskable-512.png, out/index.html 에 여섯 사이트를 한눈에 보는 페이지. 파일은 이 repo 로 복사해 쓰고, 도형을 고칠 일이 생기면 liv 생성기(gen.py·render.py)에서 고친다.

기조: 바탕 없는 먹색 채움 도형 + 오른쪽 아래 파랑 점(.kil9.dev). 파비콘과 상단 바 마크가 같은 그림이다. 상단 바 워드마크는 '[12px 마크] <사이트>(700) .kil9.dev(400 옅은 먹색)'. 설치 아이콘은 미색(#f1efe9) 바탕에 같은 마크이고, 지금의 공통 가족 앱 아이콘(미색·먹색 선·주황 강조)을 대신한다.

이 사이트는 예외다: 마크는 리브 아바타 그대로이고 파랑 점을 달지 않는다(가족 표시 밖, 사용자 결정). out/til/ 의 favicon.svg·mark.svg 는 리브를 원으로 자른 그림이다.

이 사이트: til.kil9.dev(GitHub Pages, 정적). 지금 파비콘은 페이지마다 <link rel=icon> 에 리브 data:image/webp base64 가 박혀 있다 — 루트에 favicon.svg 하나를 두고 모든 페이지(2026/·pages/·topics/·404 등, 생성 스크립트가 있으면 그 템플릿)가 그것을 참조하게 바꾼다. 설치 아이콘은 루트의 apple-touch-icon.png·icon-192/512.png(책 그림)를 미색 바탕 리브로 바꾼다. 상단(header.hero)에 사이트 이름 줄을 둘지는 착수 때 DESIGN.md 와 맞춰 판단한다 — 두면 워드마크 형식을 따른다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 모든 페이지의 파비콘이 루트 favicon.svg(liv design/family-icons/out/til/favicon.svg, 리브·점 없음) 하나를 참조하고 페이지마다 박힌 data: URI 가 없다
- [x] #2 apple-touch-icon(180)·manifest icon-192/512 를 out/til/ 의 PNG(미색 바탕 리브)로 바꾸고 manifest 에 icon-maskable-512.png 를 purpose maskable 로 따로 적으며, 참조 URL 의 ?v= 를 올린다
- [x] #3 상단에 사이트 이름 줄을 두면 '[12px 리브] til(700) .kil9.dev(400 옅은 먹색)' 형식이고, 두지 않으면 그 판단을 notes 에 남긴다
- [x] #4 주요 화면을 넓은·좁은(390px) 폭 × 라이트·다크로 캡처해 넘침·콘솔 오류가 없고 그 repo 의 테스트가 통과한다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
루트 favicon.svg(liv design/family-icons/out/til, 리브 원형·점 없음)를 두고 페이지에 박혀 있던 리브 WebP data URI 링크 271파일(2026/·p/·404·브리핑 템플릿 3·liv-notes.py 템플릿, 과거 브리핑 회차 포함)을 <link rel=icon type=image/svg+xml href=/favicon.svg?v=1> 로 바꿨다. 생성기 3곳(briefing render.py·recap.py, liv-notes.py)이 루트 index.html 에서 base64 를 정규식으로 뽑던 favicon() 을 없앴다 — 남겨 두면 루트가 바뀐 지금 발행이 예외로 멈춘다. 예외: p/submit-<토큰>(📮)·p/namhae-<토큰>(🌊)은 자기 아이콘(접수 창구는 apple-touch 사이드카까지)을 가진 별도 도구라 그대로 두었고, pages/engram/ 은 engram 발행물이라 손대지 않았다. 설치 아이콘: apple-touch-icon(180)·icon-192/512 를 미색 바탕 리브로 교체, manifest 에 icon-maskable-512 를 purpose maskable 로 분리(기존 'any maskable' 은 any 로), ?v=3·manifest ?v=4. display 는 browser 그대로(AGENTS.md 의 WebAPK 함정). AC3 상단 사이트 이름 줄은 두지 않았다 — 루트는 h1 'today i learned' 가, 글은 '← today i learned' 링크가 이미 사이트 이름을 보이고, til 은 패밀리 표시(파랑 점) 밖이라 '[리브] til .kil9.dev' 줄은 같은 이름을 한 번 더 쓰는 셈이다. AGENTS.md 런북의 공통 셸·파비콘 규칙 갱신. 검증: liv-notes.py render 결과가 일괄 치환과 같음(아이콘 줄 외 diff 없음), 브리핑 render.py 를 임시 사본에 돌려 새 링크·남은 토큰 없음, puppeteer 로 루트·글·archive·briefing·liv-walk·404 를 1280·390 × 라이트·다크 24조합 — 파비콘 200 image/svg+xml, pageerror 없음, 넘침은 go-encoding-json-v2 의 390px 하나인데 6d17391 에도 같아 기존 결함(TASK-153 등록). site-check.py·render-check.mjs 위반 없음.
<!-- SECTION:NOTES:END -->
