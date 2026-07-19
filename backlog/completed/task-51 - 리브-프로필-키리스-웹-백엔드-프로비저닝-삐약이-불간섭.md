---
id: TASK-51
title: 리브 프로필 키리스 웹 백엔드 프로비저닝 (삐약이 불간섭)
status: Done
assignee: []
created_date: '2026-07-18 06:29'
updated_date: '2026-07-18 07:24'
labels: []
dependencies:
  - TASK-46
priority: medium
ordinal: 51000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
loop-task 자동 추가(TASK-46 발견): 리브 슬랙 툴셋을 [web,vision] 로 잠갔으나(danger 툴 제거·injection 차단 검증), web_search/web_extract 는 백엔드(tavily/exa/brave/searxng/ddgs 등)가 없으면 check_fn(check_web_api_key)이 스키마에서 툴을 숨긴다. 실측: 리브가 'https://kil9.github.io/til 조회'에 '브라우징 도구가 없어 확인 안 됨'으로 답. 기본(삐약이) 프로필도 현재 web 백엔드 없음(_get_backend=firecrawl but check=False). 키리스 유일 옵션은 ddgs(pip) 전역 설치인데, 이는 공유 venv 변경이라 삐약이 프로필의 web 툴도 켜져 '기존 인스턴스 불간섭' 제약과 상충. 대안: (a) ddgs 전역 설치 + 리브 web.backend=ddgs 핀(삐약이도 web 획득 side effect), (b) 리브 .env 에 유료 키(TAVILY/BRAVE/EXA) 주입(격리·비용), (c) 로컬 SEARXNG_URL(인스턴스 필요). 결정 필요.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 리브 프로필에서 web_search/web_extract 가 스키마에 노출되고 kil9.github.io/til 조회가 실동작
- [x] #2 선택한 방식이 삐약이(기본 프로필) 런타임 툴 surface 를 의도치 않게 바꾸지 않음(또는 그 변화를 사용자가 승인)
- [x] #3 리브가 아카이브 URL 을 실제 fetch 해 내용 기반으로 답변함을 실증
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
완료 (2026-07-18, 사용자 결정=ddgs 전역설치). 
- ddgs 9.14.4 를 hermes venv 에 설치(키리스 검색). 삐약이도 web 검색 획득(사용자 승인한 부수효과).
- 발견: ddgs 는 **검색 전용** → web_extract(URL 본문) 불가하고, ddgs 검색이 이 소규모 개인 사이트를 못 찾음(DDG 미인덱싱). 아카이브 조회 실패.
- 해결: 키리스 **plain-fetch extract provider** 신설(til-inbox bot/hermes/web-plainfetch/, httpx+lxml). 리브 프로필 전용 플러그인(삐약이 불간섭). SSRF 는 web_extract_tool 상위 가드 의존 + http/https 스킴 재확인.
- config: web.search_backend=ddgs, web.extract_backend=plainfetch.
- 검증: provider 유닛(til 인덱스 fetch, title 'today i learned', 5522자) + 라이브(liv -z '최근 글' → 'LingBot-Map…' 실제 fetch 기반 정답). 잠금 회귀테스트 여전히 PASS(스키마 {web_search,web_extract,vision_analyze} 유지, plainfetch 는 새 툴 추가 안 함).
- 삐약이 영향: ddgs 전역(검색만), plainfetch 는 liv 전용.
<!-- SECTION:NOTES:END -->
