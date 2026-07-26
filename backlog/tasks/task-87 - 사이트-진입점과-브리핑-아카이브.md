---
id: TASK-87
title: 사이트 진입점과 브리핑 아카이브
status: Done
assignee: []
created_date: '2026-07-26 07:27'
updated_date: '2026-07-26 08:09'
labels:
  - solo
milestone: m-9
dependencies:
  - TASK-81
priority: medium
ordinal: 87000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
브리핑을 사이트에서 찾아갈 수 있게 한다. 루트 index.html 사이드바에 '오늘의 브리핑' 링크 한 줄을 추가하되(리브 소개 블록 근처), 루트 갤러리 카드에는 넣지 않는다. p/briefing/archive/ 에 날짜별 목록을 두어 과거분을 훑을 수 있게 한다.

정리할 것: 보존 기간(무기한 누적 vs N일 후 정리), sitemap·robots 처리, 404.html 리다이렉트 맵 등록 여부, 그리고 브리핑 페이지가 검색엔진에 til 본문 글보다 많이 잡히지 않게 할지. 매일 1건이라 1년이면 365 디렉터리가 되므로 이 판단을 미루면 나중에 되돌리기 어렵다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 루트 사이드바에서 오늘의 브리핑으로 갈 수 있다
- [x] #2 p/briefing/archive/ 에서 과거 브리핑을 날짜로 찾을 수 있다
- [x] #3 보존 기간과 검색엔진 노출 정책이 정해져 문서에 적혔다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
진입점: 루트 사이드바에 '오늘의 브리핑' 블록(a.briefing)을 리브·kil9 소개 아래, 리브의 코멘트 위에 넣었다. AI-SUMMARY 마커 밖이라 요약 잡이 덮어쓰지 않는다. 갤러리 카드·README 표에는 넣지 않는다.

아카이브: p/briefing/archive/ 를 render.py 가 발행 때마다 다시 만든다. p/briefing/ 아래 날짜 디렉터리가 진실원본이고(디렉터리를 스캔), 각 회차의 meta description 을 한 줄 요약으로 쓴다. 월별로 묶어 최신이 위. 템플릿은 backlog/assets/briefing/archive.html(til 공통 720px 셸).

정책(backlog/assets/briefing/README.md 에 정본):
- 보존은 무기한 누적. 페이지 85KB × 365 = 연 30MB 로 Pages 한도(1GB)에 한참 못 미친다. 클론이 무거워지면 그때 다시 본다.
- 검색엔진은 noindex, follow — 브리핑이 til 본문 글보다 많이 색인되면 사이트의 얼굴이 바뀐다. 링크는 따라가게 둬 원문·til 로 가는 경로는 살린다. 데일리·날짜판·아카이브 세 종류 모두 같다.
- sitemap.xml·robots.txt 는 이 저장소에 없다. 만들 이유가 이번에도 없어 두지 않았다(noindex 는 meta 로 충분하다).
- 404.html 리다이렉트 맵에는 등록하지 않는다.

검증: 날짜 디렉터리 2개(6월·7월)를 두고 렌더해 월 그룹·회차 수·상대경로를 확인했고, 루트 인덱스는 헤드리스 스크린샷으로 사이드바 위치를 확인했다.
<!-- SECTION:NOTES:END -->
