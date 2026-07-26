---
id: TASK-80
title: GeekNews 수집·선별 잡 구성
status: Done
assignee: []
created_date: '2026-07-26 03:55'
updated_date: '2026-07-26 07:59'
labels:
  - solo
milestone: m-8
dependencies:
  - TASK-79
priority: medium
ordinal: 80000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
~/jobs/ 아래 docs-ai-summary 와 같은 구조로 데일리 잡을 만든다. RSS(https://news.hada.io/rss/news)를 받아 이미 처리한 항목을 state 로 걸러내고, 관심사 프로필과 함께 headless claude 에 넘겨 상위 N건 선별 + 항목당 요약 3-4줄 + 제외 사유를 생성한다. 파일럿에서 항목 상세는 news.hada.io/topic?id=NNN 을 개별로 가져와야 밀도가 나왔다 - 선별 후에만 상세를 가져오는 2단 구성으로 호출 수를 줄인다. 신규 항목이 임계 미만이면 LLM 호출 없이 조기 종료(docs-ai-summary 의 패턴).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 cron 으로 매일 아침 1회 도는 run.sh 와 state 가 있다
- [x] #2 RSS 수집 → 1차 선별 → 선별분만 상세 fetch 의 2단 구성으로 동작한다
- [x] #3 신규 없음/실패 시 조용히 종료하고 로그를 남긴다
- [x] #4 선별 결과가 페이지 생성 단계가 소비할 중간 포맷(JSON)으로 떨어진다
- [x] #5 선별·정리 모델은 Claude Opus 5 를 기본으로 쓴다 (fable 아님)
- [x] #6 선별 건수는 7-10건 범위에서 모델이 그날 재료에 맞춰 정한다
- [x] #7 선별은 두 축이다: 관심사 프로필 매칭 + GeekNews 추천수. 추천 상위 2-5건은 관심사와 무관해도 무조건 포함한다
- [x] #8 RSS 만으로는 인기 순위를 알 수 없으므로 첫 페이지(추천수·노출 순서)도 함께 수집한다
- [x] #9 인기 축 컷은 절대 추천수가 아니라 최근 30일 롤링 분포의 백분위(p90)로 잡고, 통과 건수를 2-5건으로 clamp 한다. 데이터가 없는 초기에는 그날 수집분 내부 분위수로 폴백
- [x] #10 수집 범위는 첫 페이지에 그치지 않는다(오늘 실측: 상위 6% 항목이 2페이지에 있었다)
- [x] #11 정렬은 추천 백분위가 1순위이고 관심사는 동률·인접 보정에만 쓴다. 관심사가 맞아도 추천이 낮으면 아래로 내려간다(파일럿 v6 에서 확정)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
~/jobs/liv-briefing/ 에 구성했다(머신 로컬·비버전, docs-ai-summary·til-submit 과 같은 자리).

run.sh   flock + 같은 날 재실행 조기종료 + 단계별 로그. 신규 항목이 MIN_NEW(5) 미만이면 LLM 미호출 종료.
collect.py  /new?page=N 을 빈 페이지까지 훑어(오늘 실측 33건, 2쪽까지) 추천수·순서·요약을 긁고 RSS 요약을 id 로 합친다. state/seen.json 으로 처리분 제외, state/points-30d.jsonl 롤링 분포로 백분위 산출(표본 60 미만이면 그날 수집분 내부 분위수 폴백).
select.py   1차 선별. 인기 축(백분위 p90 통과분 2-5건 clamp)은 무조건 포함하고 나머지를 관심사 프로필(task-79 스크립트 호출)로 채워 7-10건. 정렬은 백분위 1순위이고 관심사 등급은 최대 2.0 포인트 보정으로만 개입한다(인접 항목만 뒤집힌다).
compose.py  선별분만 topic 상세 fetch(본문 + 댓글 5개) 후 2차 정리. 리브 문체로 lede·bullets·리브 한마디·til 연관·조사 방향·머리말·개요를 쓰고 state/briefing-<날짜>.json 으로 떨군다. 한마디 4개·연관 3개 상한은 코드에서 clamp 한다(모델이 매번 넘겼다).
llm.py      claude -p --model opus 공용 호출 + JSON 파싱(코드펜스·잡담 방어, 2회 재시도).
seen.py     그날 훑은 id 를 처리 완료로 찍는다. 지금은 run.sh 끝에서 부르지만 발행(task-85)이 붙으면 push 성공 뒤로 옮겨야 한다.

cron: 40 8 * * * (발행 09:00 앞에 재료를 만들어 두는 배치). docs-ai-summary 가 09:00 에 같은 저장소로 push 하므로 task-85 의 발행 push 는 non-fast-forward 재시도를 넣어야 한다.

실측: 전체 4분(수집 즉시, 1차 선별 40초, 상세+정리 3분 20초), LLM 2회. 오늘 재료로 8-9건이 뽑혔고 정렬·요약 품질은 파일럿 v5 수준이다.

함정: 목록 행 파싱은 한 정규식으로 행 전체를 매칭하면 필드 하나가 없는 행에서 lazy 매칭이 다음 행을 삼켜 그 행이 사라진다(20건 중 1건이 그렇게 빠졌다). 행 단위로 자른 뒤 필드별로 뽑는다.

repo 쪽 변경: interest-profile.py --format json 에 전체 글 목록(articles)을 추가했다(til 연관 판정에 최근 12건으로는 부족).
<!-- SECTION:NOTES:END -->
