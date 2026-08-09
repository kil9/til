---
id: TASK-120
title: 브리핑 출처를 로고 배지로 표시
status: Done
assignee: []
created_date: '2026-08-09 03:05'
updated_date: '2026-08-09 03:20'
labels: []
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
아침 브리핑(p/briefing/)의 항목 출처(GeekNews / Hacker News)를 텍스트 두 글자(`<span class="src">HN</span>`) 대신 브랜드 로고 타일로 보여준다. 지금은 `.foot` 메타 줄 중간에 파묻혀 어느 소스에서 온 글인지 훑을 때 눈에 안 들어온다.

## 할 일
- 인라인 SVG 로고 마크 2종 (외부 리소스 금지, 단일 파일 원칙)
  - GN: 브랜드 남색(#0000AA) 타일 + GeekNews 파비콘의 픽셀 글리프에서 뽑은 흰 'GN'
  - HN: 브랜드 주황(#FF6600) 타일 + 흰 Y
- render.py `foot()` 의 출처 배지·`also` 배지를 로고로 교체 (title/aria-label 로 소스 전체 이름)
- '훑고 넘긴 것' 그리드(item-rest.html)에도 출처 로고 추가 — 지금은 출처 표시가 아예 없다
- template.html 에 `.srcmark` CSS
- DESIGN.md 에 브랜드 로고 색 예외 명시 (One Blue Rule 과 충돌하지 않음을 기록)
- backlog/assets/briefing/README.md 갱신

## 완료 조건
- 템플릿(til repo)과 잡 코드(nuc14 ~/jobs/liv-briefing)를 같은 때에 배포 — assert_filled 가 미치환 토큰을 잡으므로 한쪽만 나가면 발행이 죽는다
- 과거 회차 재렌더로 라이트/다크 양쪽 확인
- site-check.py 통과
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 GN·HN 로고가 인라인 SVG 로 .foot 줄과 rest 그리드에 표시된다
- [ ] #2 라이트/다크 양쪽에서 로고가 식별된다
- [ ] #3 출처 이름이 title/aria-label 로 남아 접근성이 유지된다
- [ ] #4 site-check.py 통과
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
브랜드 타일 2종을 template.html 상단 SVG 스프라이트 <symbol> 로 정의하고 각 자리는 <use> 로 참조한다. 회차당 56회 쓰이므로 SVG 를 되풀이하면 페이지가 배로 불어난다 — 실측 증가분 9KB(110→119KB).

GN 마크의 'GN' 은 GeekNews 파비콘(32x32 픽셀 워드마크 'GeekNews' 2줄)에서 G·N 글리프만 잘라 붙인 것이다. 원본 전체는 배지 크기에서 안 읽힌다. 색 #0000AA 는 그 사이트 apple-touch-icon 실측값.

HN 마크는 원본의 흰 사각 테두리를 뺐다. 17px 표시에서 테두리를 넣으려면 Y 를 줄여야 하고 줄인 Y 는 뭉갠다(세 안을 17px 로 다운스케일해 비교하고 고름).

## 자리를 두 번 옮겼다

처음에는 메타 줄(.foot)의 백분위 앞에 뒀는데 발행하고 보니 두 가지가 어긋났다.

1. 로고 앞뒤로 큰 빈칸이 생겼다. 인라인 <svg> 에 내재 크기가 없는데 CSS 가 `height: 1.15em; width: auto` 만 줘서, width:auto 가 기본 폭(300px 상당)을 잡았다. width 와 height 를 둘 다 주는 것으로 고쳤다.
2. 자리 자체가 늦었다. 항목을 다 읽고 나서야 출처를 알게 되고, 그 줄에서 백분위 문구와 뒤엉켜 보였다. 사용자 지적을 받아 제목 끝(h3·h4)으로 옮기고 크기를 0.85em 으로 줄였다.

메타 줄에는 백분위만 남지만 그 문구가 이미 소스마다 다르므로('추천 상위' = GeekNews, '프런트 상위' = HN) 출처 표시가 사라지지 않는다. 양쪽에 오른 글의 also 는 제목 옆 로고가 가리키지 않는 '다른 쪽' 이라 이름을 글자로 밝힌다.

'훑고 넘긴 것' 그리드에도 출처를 새로 붙였다(원래 표시가 아예 없었고 회차 건수의 대부분이 거기 있다). 머리말·footer 의 '수집 GeekNews' 도 두 소스를 적도록 고쳤다 — task-106 에서 빠진 자리.

DESIGN.md 에 The Foreign Logo Exception 을 추가했다. 남의 브랜드 색은 팔레트·Two-Mode Parity 밖이고 다크에서 opacity 로만 누른다.

잡 코드(nuc14 ~/jobs/liv-briefing/render.py, 비버전)의 srcmark()/foot()/item·rest fill 을 같은 때에 고쳤다. assert_filled 가 미치환 {{SRC}} 를 잡으므로 한쪽만 배포되면 발행이 죽는다.

검증: site-check.py 위반 없음. 브라우저 렌더 확인은 이 머신에서 못 한다 — puppeteer/크롬이 없어 render-check.mjs 가 돌지 않는다. 그래서 첫 배치의 빈칸 결함을 발행 전에 못 잡았다. 미리보기 HTML 을 만들어 사용자에게 보내는 것이 이 저장소에서 실질적인 렌더 확인 수단이다.
<!-- SECTION:NOTES:END -->
