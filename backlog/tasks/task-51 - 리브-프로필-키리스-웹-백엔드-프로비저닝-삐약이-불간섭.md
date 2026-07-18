---
id: TASK-51
title: 리브 프로필 키리스 웹 백엔드 프로비저닝 (삐약이 불간섭)
status: Blocked
assignee: []
created_date: '2026-07-18 06:29'
updated_date: '2026-07-18 06:29'
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
- [ ] #1 리브 프로필에서 web_search/web_extract 가 스키마에 노출되고 kil9.github.io/til 조회가 실동작
- [ ] #2 선택한 방식이 삐약이(기본 프로필) 런타임 툴 surface 를 의도치 않게 바꾸지 않음(또는 그 변화를 사용자가 승인)
- [ ] #3 리브가 아카이브 URL 을 실제 fetch 해 내용 기반으로 답변함을 실증
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
결정 필요: 리브 웹 백엔드를 (a) ddgs 전역설치+핀(삐약이도 web 켜짐) / (b) 유료키 격리주입 / (c) 로컬 searxng 중 무엇으로 할지. 삐약이 툴 surface 변화 허용 여부가 핵심.
<!-- SECTION:NOTES:END -->
