---
id: TASK-81
title: 데일리 리포트 페이지 경로·노출 정책 확정
status: Done
assignee: []
created_date: '2026-07-26 03:55'
updated_date: '2026-07-26 07:39'
labels:
  - solo
milestone: m-8
dependencies:
  - TASK-78
priority: medium
ordinal: 81000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
리포트를 사이트 어디에 둘지 정한다. 후보: (a) p/daily/ 상설 페이지에 최신만 덮어쓰기 (b) p/daily/<YYYY-MM-DD>/ 로 누적 + p/daily/ 인덱스. 매일 1건이 갤러리 카드로 쏟아지면 til 본문 글이 묻히므로 루트 갤러리에는 노출하지 않는 것이 기본이다(사이드바에 '오늘의 브리핑' 링크 한 줄 정도). 보존 기간(예: 30일 후 정리)과 sitemap/robots 처리도 함께 정한다. 페이지 셸은 파일럿 HTML 을 기준으로 한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 경로 구조(a/b)와 근거가 결정됐다
- [x] #2 루트 갤러리·README·아카이브에 노출할지 여부가 결정됐다
- [x] #3 보존 기간 정책이 정해졌다
- [x] #4 파일럿 HTML 을 정리한 페이지 템플릿이 저장소에 있다
- [x] #5 레이아웃은 2칼럼(본문 항목 + 우측 부가 정보)이고 til 본문 페이지보다 넓다(약 1160px)
- [x] #6 선별 제외분도 접지 않고 우측에 한 줄 요약 형태로 노출한다
- [x] #7 til 정합성은 고정 섹션이 아니라 요약 불릿 하나로 녹이고 [til 연관] 레이블 + 해당 글 링크를 붙인다. 연관이 약하면 생략한다
- [x] #8 레이아웃은 위에서 아래로 한 번만 읽히게 한다: 항목마다 좌(본문)+우(메타·버튼)로 완결, 선별 제외분은 맨 아래 그리드에 짧은 요약으로
- [x] #9 데일리 페이지에는 그날 생성된 정보만 싣는다. 관심사 프로필·선정 기준 등 매일 같은 정보는 상설 소개 페이지로 빼고 footer 링크 한 줄만 남긴다
- [x] #10 최상단 우측은 오늘의 개요(강추 1건 + 전체 미니 목차, 본문 앵커)로 채운다
- [x] #11 항목 요약은 '~라는 글이다' 식 3인칭 설명이 아니라 저자가 직접 말하는 어투로 쓴다(가능하면 원문 화자의 결에 맞춰)
- [x] #12 확정: p/briefing/ 이 항상 최신 1건, p/briefing/<YYYY-MM-DD>/ 로 과거분 누적, 루트 갤러리 카드에는 노출하지 않는다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
템플릿을 backlog/assets/briefing/ 에 넣었다: template.html(셸·CSS·머리말·footer·액션 JS) + item.html + item-rest.html, 치환은 {{TOKEN}}. 같은 디렉터리 README.md 가 토큰 계약·레이아웃 원칙·경로/노출 정책의 정본이다. 더미 데이터로 스모크 렌더해 미치환 토큰 0·태그 균형을 확인했다.

정책 결정:
- 경로: p/briefing/ 최신 1건 + p/briefing/<YYYY-MM-DD>/ 누적(AC12 확정분). 최신판과 날짜판은 내용이 같고 상대경로 깊이만 다르다({{ROOT_REL}}).
- 노출: 루트 갤러리 카드·README 표·p/archive/ 모두 미노출. 진입은 루트 사이드바 링크 한 줄 + p/briefing/archive/(task-87) 둘.
- 검색엔진: noindex, follow. 매일 1건이 til 본문 글보다 많이 색인되면 사이트의 얼굴이 바뀐다. 링크는 따라가게 둬 원문·til 로 가는 경로는 살린다.
- 보존: 날짜판 무기한 누적. 대신 페이지당 40KB 상한(임베드는 hero 스티커 1 + 아바타 2-3)을 둔다 - 파일럿이 76KB 였고 그대로면 1년에 30MB 다. 40KB 면 연 15MB 라 정리 잡이 필요 없다. 상한이 무너지면 그때 보존 기간을 다시 본다.
- 404.html 리다이렉트 맵에는 등록하지 않는다(구 평면 URL 시절에 없던 경로).
- 폭은 AC5 대로 1160px(파일럿은 1120px).

AGENTS.md 저장소 구조와 규칙에 p/briefing/ 를 추가했다.
<!-- SECTION:NOTES:END -->
