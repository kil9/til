---
id: TASK-109
title: 발행 전 자동 점검 — canonical·링크·용량
status: Done
assignee: []
created_date: '2026-07-26 10:25'
updated_date: '2026-07-26 16:12'
labels:
  - solo
milestone: m-11
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
페이지가 50건을 넘었는데 발행 시 자동 점검이 하나도 없다. rel=canonical 은 2개 페이지에만 있다. 로컬 체커 하나로 묶는다: (1) 전 페이지 canonical 존재·값 일치, (2) 내부 링크 깨짐, (3) 404.html 리다이렉트 맵에 신규 슬러그 등록 여부, (4) HTML 용량 상한(TASK-99 에서 정한 값), (5) 선택적으로 외부 링크 사망 여부(느리므로 별도 실행). 런북 §5 앞에 붙이거나 pre-push 훅으로.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 backlog/assets/ 의 사이트 전체 점검 스크립트 하나로 묶이고, 발행 런북 §5(재생성 뒤·커밋 전) 단계로 들어간다
- [x] #2 relink-pages.py 가 마커 구간 방식으로 전 페이지에 rel=canonical 을 소급 주입한다(현재 2건 → 전 페이지)
- [x] #3 점검기가 canonical 존재와 값 일치(루트 카드의 경로와 같은지)를 확인한다
- [x] #4 내부 링크 깨짐(존재하지 않는 경로를 가리키는 상대·절대 링크)을 검출한다
- [x] #5 루트 카드에 있는 슬러그가 404.html 리다이렉트 맵에 등록됐는지 확인한다
- [x] #6 HTML 용량 상한(TASK-99 의 5MB)을 넘는 페이지를 보고한다
- [x] #7 외부 링크 생존 확인은 기본 실행에서 빠지고 별도 플래그로만 돈다(느려서 발행을 막으면 안 된다)
- [x] #8 위반이 있으면 비영 종료코드로 끝나 무인 워처 발행에서도 걸린다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
확정 사항(2026-07-27 승격 인터뷰):
- 배치: repo 안 스크립트 + 런북 §5 단계. 스킬(~/.claude/skills/publish-til)은 repo 밖이라 버전 관리가 따로 놀고 다른 머신에 안 퍼지며, pre-push 훅은 훅 미설치 머신에서 조용히 빠진다. 런북에 넣으면 무인 워처도 같은 절차를 따르므로 자동으로 걸린다.
- canonical: 점검만 하지 않고 relink-pages.py 가 전 페이지에 소급 주입한다. og:image·하단 내비를 마커 구간에 박는 기존 배관의 확장이라 자리가 이미 있다.
- 외부 링크: 기본 제외, 별도 플래그.

기존 점검과의 경계: 스킬의 til-preflight.sh(경로·브랜치·clean·슬러그 충돌)와 til-verify.sh(새 페이지의 doctype·favicon·og:title·beacon·카드/README 참조)는 둘 다 그 페이지 하나만 본다. 이 태스크는 사이트 전체를 보는 자리라 중복이 아니다.

완료(2026-07-27):
- backlog/assets/site-check.py 신설. canonical(존재·카드 URL 일치) / 내부 링크 + 앵커 대상 / 404 리다이렉트 맵 등록·경로 일치 / 용량 5MB. 위반 있으면 exit 1. 런북 §5(재생성 뒤·커밋 전)에 단계로 넣고 README 절차도 5→6 으로 갱신.
- canonical 은 relink-pages.py 의 PAGEOG 마커 구간에 og:image 와 함께 소급 주입(og_html → head_meta_html). 카드 있는 51건 전부. p/briefing/ 의 기존 canonical 2건은 카드가 없어 대상 밖이라 충돌하지 않는다.
- 앵커 검사는 TASK-108 로 절 id 가 생기면서 실효가 생겨 같이 넣었다(같은 페이지 #id + 다른 페이지 #id 둘 다).
- 실행 결과 위반 0건 / 페이지 69·카드 51·내부 링크 414개, 1초 미만.
- 오탐 2종을 잡아 예외 처리: JS 가 런타임에 조립하는 href(작은따옴표·줄바꿈·템플릿 리터럴이 보이면 리터럴 링크가 아니다), '#top'(요소가 없어도 문서 맨 위로 가는 HTML 표준 프래그먼트).
- 음성 테스트로 각 검사가 실제로 발화하는지 확인: canonical 제거·값 변조, 없는 경로/없는 앵커/다른 페이지의 없는 앵커, 404 맵 항목 삭제·경로 변조, 6MB 더미 페이지 → 각각 정확히 걸리고 exit 1.
- --external 실측: 외부 URL 232개 순차 확인 7분, 응답 없음 8건(404·타임아웃·연결 끊김). 경고로만 세고 종료코드에 반영하지 않는다 — 남의 서버 사정으로 발행이 막히면 안 된다. 봇 차단·HEAD 미지원(403·405·429)은 죽은 것으로 세지 않는다.
<!-- SECTION:NOTES:END -->

2026-07-26 범위 축소: (4) HTML 용량 상한은 TASK-99 에서 5MB 경고로 확정돼 `relink-pages.py` 끝에 들어갔다 — 이 draft 에서 뺀다. 남은 범위는 (1) canonical, (2) 내부 링크 깨짐, (3) 404 맵 등록 여부, (5) 외부 링크 사망 여부다. 삽입 배관이 필요하면 `relink-pages.py` 의 마커 방식을 그대로 쓴다.
