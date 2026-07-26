---
id: TASK-106
title: Hacker News 를 두 번째 소스로 추가
status: Blocked
assignee: []
created_date: '2026-07-26 06:01'
updated_date: '2026-07-26 15:36'
labels:
  - solo
milestone: m-8
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
현재 브리핑 소스는 GeekNews(news.hada.io) 하나다. https://news.ycombinator.com/ 을 두 번째 소스로 붙여 한 브리핑에 함께 싣는다.

검토할 것:
- 수집: HN 은 공식 Firebase API(hacker-news.firebaseio.com)와 Algolia 검색 API 가 있어 RSS 보다 점수·댓글수를 정확히 얻기 쉽다. GeekNews 는 첫 페이지 스크레이핑이 필요했던 것과 대비된다.
- 인기 축 정규화: GeekNews 추천수(오늘 실측 중앙값 7, 최대 56)와 HN points(수백 단위)는 스케일이 다르다. 절대값을 섞지 말고 각 소스 내부의 백분위로 환산해 비교해야 한다. task-80 의 롤링 백분위 컷을 소스별로 따로 유지하는 형태.
- 중복 제거: 같은 원문이 양쪽에 오르는 일이 잦다(오늘도 오픈 웨이트·Opus 5 관련 글이 겹쳤다). 원문 URL 정규화로 합치고 양쪽 점수를 함께 표시할지 결정한다.
- 지면 배분: 소스별 섹션으로 나눌지, 한 목록에 섞고 출처만 표기할지. 리브의 개요 패널(오늘의 강추·미니 목차)은 소스와 무관하게 하나로 유지하는 편이 읽기 흐름에 맞다.
- 언어: HN 은 영문이라 요약 부담이 커진다. 정리 모델은 동일하게 Opus 5.

파일럿 평가(task-78) 통과 후, GeekNews 단일 소스가 안정된 다음에 착수한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 collect.py 가 GeekNews 와 함께 HN Algolia front_page 엔드포인트에서 항목을 수집하고, 각 항목에 source(gn|hn) 필드를 남긴다
- [ ] #2 추천 백분위를 소스별로 따로 매긴다 — points-30d.jsonl 의 롤링 표본을 소스별로 분리해 GN 추천수(중앙값 한 자리)와 HN points(수백 단위)를 절대값으로 섞지 않는다
- [ ] #3 원문 URL 정규화로 양쪽에 오른 같은 글을 한 항목으로 합치고, 링크는 GeekNews 쪽 논의 페이지만 남긴다(HN 링크는 버린다)
- [ ] #4 브리핑 본문은 소스 섹션을 나누지 않고 백분위 상위를 한 목록에 섞어 싣되, 각 항목에 출처 배지(GN/HN)와 그 소스 기준 점수·백분위를 표기한다. 중복 항목은 양쪽 점수를 함께 보인다
- [ ] #5 HN 항목의 제목은 Opus 5 가 한글로 옮기고 원문 제목을 작게 병기한다
- [ ] #6 리브의 개요 패널(오늘의 강추·미니 목차)은 소스와 무관하게 하나로 유지된다
- [ ] #7 HN 수집·정규화 실패가 GeekNews 단독 발행을 막지 않는다(한쪽 소스가 죽어도 브리핑이 나간다)
- [ ] #8 실제 발행 회차 1건 이상에서 HN 항목이 섞여 나오고 페이지 용량이 500KB 상한 안에 있다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
보류 — 사용자 지시로 착수 보류(2026-07-27). 원 draft 의 전제(GeekNews 단일 소스가 안정된 뒤 착수)도 아직 유효하다. 재개하려면 상태를 To Do 로 되돌린다.

확정 사항(2026-07-27 승격 인터뷰):
- 지면: 소스 섹션을 나누지 않고 한 목록에 섞는다. 항목마다 출처 배지 + 그 소스 기준 점수·백분위.
- 중복: 원문 URL 정규화로 합치고 링크는 GeekNews 쪽만 남긴다(백분위와 무관하게 GN 우선).
- 수집: HN Algolia front_page 엔드포인트(호출 1회로 톱페이지 전원의 점수·댓글수·URL). Firebase 는 아이템당 요청이라 30회+ 필요해 배제.
- 언어: 제목은 Opus 5 로 한글 번역 + 원문 병기.

작업 대상 코드는 nuc14 ~/jobs/liv-briefing/ 의 collect.py·compose.py 이며 이 디렉터리는 git 저장소가 아니다(머신 로컬 비버전). 따라서 이 태스크에는 커밋할 코드 변경이 없고, repo 쪽 변경은 템플릿(backlog/assets/briefing/)에 손이 갈 때만 생긴다.

기존 배관 참고점: 백분위는 collect.py 의 points_history()/percentile_rank() 가 state/points-30d.jsonl 30일 롤링 표본으로 매기고, compose.py 의 build_prompt() 가 '추천 상위 N%' 문구로 모델에 넘긴다. 소스별 표본 분리는 이 두 자리를 함께 고쳐야 한다.
<!-- SECTION:NOTES:END -->
