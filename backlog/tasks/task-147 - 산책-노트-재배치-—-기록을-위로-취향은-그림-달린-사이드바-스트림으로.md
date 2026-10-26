---
id: TASK-147
title: 산책 노트 재배치 — 기록을 위로, 취향은 그림 달린 사이드바 스트림으로
status: Done
assignee: []
created_date: '2026-10-26T13:05:00Z'
updated_date: '2026-10-26T13:33:00Z'
labels: []
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
관리자 요청(2026-10-26): https://til.kil9.dev/p/liv-walk/ 에서 기록을 맨 위로 올리고 오래된 날은 접는다. 좋아/별로/꽂힌 것은 종류별로 묶지 말고 사이드바에 날짜순으로 한 개씩 섞어 짧게 보인다. 많은 항목에 codex 로 만든 그림을 원본 비율로 달고, 그림을 누르면 기록 속 그 노트로 이동하고 다시 누르면 출처 원문으로 간다. 결정: 그림은 사이드바 취향 항목에만(기록의 리브 SVG·사진 그림첩은 유지), 원문은 출처 기사.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 기록이 페이지 맨 위에 오고 최근 며칠만 펼치며 그 아래 날은 접혀 있다
- [x] #2 좋아/별로/꽂힌 것이 종류별 묶음 없이 날짜순 한 항목씩 사이드바(좁은 화면은 기록 아래)에 짧은 문장으로 나온다
- [x] #3 사이드바 항목 다수에 codex 로 만든 그림이 잘리지 않은 원본 비율로 붙는다
- [x] #4 그림을 누르면 기록 속 그 노트로 이동(접힌 날이면 펼침)하고, 같은 그림을 다시 누르면 출처 원문으로 간다
- [x] #5 산책 잡이 앞으로 새 취향 노트에도 짧은 문장과 그림을 만든다(walk 프롬프트·run.sh 반영)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
무엇을: p/liv-walk 를 기록 위·취향 사이드바로 재배치. 기록은 최근 3일 펼침(OPEN_DAYS 7→3), 그 뒤 30일 접힘. 취향(좋아·별로·꽂힘)은 종류 묶음 없이 최근 것부터 한 항목씩 사이드바(960px 이상은 오른쪽 sticky 칸, 좁으면 기록 아래)에 짧은 문장(decor short, 48자 이하)으로, 12개 뒤는 '더 보기'. 취향 67건 전부에 codex 그림(liv-notes.py pics, 720px WebP, 비율 그대로·높이만 240px 상한, 합계 908KB). 그림 클릭은 기록 속 노트로 이동(접힌 날 펼침·하이라이트), 같은 그림 재클릭은 출처 원문(인라인 스크립트, a.pic.armed 에 '원문 ↗' 표시). 본 페이지 밖 날의 노트는 달별 아카이브 앵커로 건다. 기본 CSS 의 4:3 강제 크롭과 liv.css 사진 크롭도 걷어냈다. 문장 속 링크 구절(anchor)은 더 쓰지 않는다.
산책 잡(nuc14 ~/jobs/liv-walk, 비버전): walk.py 프롬프트가 link 대신 short 를 내고 페이지 구조 설명을 새 클래스로 갱신, run.sh 가 apply-walk 뒤 pics --limit 4 --jobs 2 --render 를 부른다(실패해도 발행 진행, 원본 PNG 는 ~/.cache/liv-pics 에 캐시). 백업 *.bak-sidebar.
왜: 2026-10-26 관리자 요청. 결정 — 그림은 사이드바 취향 항목에만, '원문'은 출처 기사.
검증: render·check ok, site-check 위반 없음, puppeteer 로 데스크톱·다크·모바일 캡처 확인, 접힌 날 노트(n-0138) 그림 첫 클릭 → details 펼침·hit·뷰포트 안·armed, 두 번째 클릭 → 출처 URL 로 이동 일치. cron 과 같은 최소 환경에서 codex 로그인 확인.
<!-- SECTION:NOTES:END -->
