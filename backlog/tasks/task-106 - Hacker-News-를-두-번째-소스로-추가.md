---
id: TASK-106
title: Hacker News 를 두 번째 소스로 추가
status: In Progress
assignee: []
created_date: '2026-07-26 06:01'
updated_date: '2026-08-06 08:05'
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
- [x] #1 collect.py 가 GeekNews 와 함께 HN Algolia front_page 엔드포인트에서 항목을 수집하고, 각 항목에 source(gn|hn) 필드를 남긴다
- [x] #2 추천 백분위를 소스별로 따로 매긴다 — points-30d.jsonl 의 롤링 표본을 소스별로 분리해 GN 추천수(중앙값 한 자리)와 HN points(수백 단위)를 절대값으로 섞지 않는다
- [x] #3 원문 URL 정규화로 양쪽에 오른 같은 글을 한 항목으로 합치고, 링크는 GeekNews 쪽 논의 페이지만 남긴다(HN 링크는 버린다)
- [x] #4 브리핑 본문은 소스 섹션을 나누지 않고 백분위 상위를 한 목록에 섞어 싣되, 각 항목에 출처 배지(GN/HN)와 그 소스 기준 점수·백분위를 표기한다. 중복 항목은 양쪽 점수를 함께 보인다
- [x] #5 HN 항목의 제목은 Opus 5 가 한글로 옮기고 원문 제목을 작게 병기한다
- [x] #6 리브의 개요 패널(오늘의 강추·미니 목차)은 소스와 무관하게 하나로 유지된다
- [x] #7 HN 수집·정규화 실패가 GeekNews 단독 발행을 막지 않는다(한쪽 소스가 죽어도 브리핑이 나간다)
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

재개(2026-08-06, 사용자 지시). 원 전제였던 'GeekNews 단일 소스 안정' 은 충족됐다.

구현: collect.py(HN Algolia front_page 1회 호출·hn: 접두·소스별 백분위와 backfill·URL 정규화 병합·BRIEFING_HN 킬스위치), select.py(재등장 판정에 URL 축 추가·인기 축 소스별 상한·CANDIDATE_LIMIT 40→55·소스 구성 로그), compose.py(HN 상세는 Algolia items 의 본문+최상위 댓글 5개·title_ko·소스별 배지 하한·상세 수집 per-item 격리), render.py(출처 배지와 소스별 백분위 문구·원제 병기·미치환 토큰 가드). repo 쪽은 item.html·template.html(.src/.orig)·README.

설계 판단:
- id 를 양쪽 다 접두하지 않고 HN 만 hn: 을 붙였다. '맨 id = GeekNews' 규약이면 seen.json·points-30d.jsonl·과거 selected-*.json 마이그레이션이 통째로 사라진다. 그 마이그레이션의 실패는 조용하다(seen 필터 무효화 → 어제 글 재등장, 에러 없음)이라 경로 자체를 없애는 편이 폴백을 잘 짜는 것보다 안전하다.
- HN 원문 페이지를 긁지 않는다. 임의 웹사이트라 불안정하고, 태그를 벗기면 내비·쿠키 배너가 6000자 본문 자리를 차지해 요약이 오히려 나빠진다. GN 쪽 '본문' 도 원문이 아니라 GN+ 요약이라 격차가 크지 않다. 원문 fetch 강화는 별도 draft 로 뺐다.
- 선별 총량은 7-10 그대로 뒀다. 제약은 재료 공급이 아니라 읽는 사람의 아침 읽기량이다.

착수 전에 못 본 상호작용 하나를 자문에서 잡았다: task-118 의 반응 온도 배지가 comments 원값으로 자르는데 HN 은 댓글이 수백 개(당일 실측 중앙값 60, 최대 671)라 HN 이 배지를 독점하고 GN 기준 하한 10개가 무의미해진다. 하한을 소스별(gn 10 / hn 250)로 바꾸고 후보를 소스당 1건으로 두어 회차당 최대 2건을 유지했다. HN 250 은 그날 프런트페이지 상위 5건 컷(247)에서 온 잠정값이다.

또 하나: compose 의 상세 수집에 per-item try/except 가 없어 항목 하나의 fetch 실패가 회차 전체를 죽이는 결함이 HN 이전에도 잠재해 있었다. 이번에 격리했다.

검증(실 state 를 건드리지 않게 잡 디렉터리를 스크래치로 clone 하고 state 사본과 함께 돌렸다):
- url_key 정규화 8케이스, 빈 키끼리 병합 금지, 재등장 URL 판정, 인기 축 소스별 clamp, 소스별 배지 임계 경계값, 미치환 토큰 가드(오탐 없음을 발행된 실페이지로 확인) 전부 통과.
- 킬스위치 off 로 돌려 기존 GN 단독 경로가 그대로임을 확인.
- 실수집→선별→정리→렌더 전 구간 1회. 56건(GN 26 + HN 30) 수집, 한글 제목 9건에 원제 병기, 출처 배지 10건, 반응 배지 1건(671댓글=화제), 114KB, 리터럴 토큰 잔존 0.

관찰 필요: 그 스크래치 회차가 10건 중 9건 HN 이었다. 오후 실행이라 GeekNews 신규가 2건뿐이고 나머지가 재등장 강등을 먹은 조건 탓이 크다(실제 09:00 회차는 GN 3건 선별). 확정 슬롯 clamp 는 정상 동작했고(HN 2건) 나머지는 관심사 축이 채운 결과다. 소스 균형을 강제하지 않는 것이 확정 사항이라 상한을 새로 걸지 않고 선별 로그에 소스 구성을 남겼다. 일주일 굴려 보고 GN 좋은 글이 실제로 밀려나면 그때 다시 본다.

AC#8(실제 발행 회차에 HN 이 섞여 나오고 500KB 이내)만 남았다. 내일 09:00 정기 발행이 검증 창이다.
<!-- SECTION:NOTES:END -->
