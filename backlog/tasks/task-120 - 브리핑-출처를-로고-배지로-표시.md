---
id: TASK-120
title: 브리핑 출처를 로고 배지로 표시
status: Done
assignee: []
created_date: '2026-08-09 03:05'
updated_date: '2026-08-09 03:11'
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
브랜드 타일 2종을 template.html 상단 SVG 스프라이트 <symbol> 로 정의하고 각 자리는 <use> 로 참조한다. 회차당 56회 쓰이므로 SVG 를 되풀이하면 페이지가 배로 불어난다 — 실측 증가분 8KB(110→118KB).

GN 마크의 'GN' 은 GeekNews 파비콘(32x32 픽셀 워드마크 'GeekNews' 2줄)에서 G·N 글리프만 잘라 붙인 것이다. 원본 전체는 배지 크기에서 안 읽힌다. 색 #0000AA 는 그 사이트 apple-touch-icon 실측값.

HN 마크는 원본의 흰 사각 테두리를 뺐다. 17px 표시에서 테두리를 넣으려면 Y 를 줄여야 하고 줄인 Y 는 뭉갠다(세 안을 17px 로 다운스케일해 비교하고 고름).

'훑고 넘긴 것' 그리드에도 출처를 새로 붙였다(원래 표시가 아예 없었고 회차 건수의 대부분이 거기 있다). 머리말·footer 의 '수집 GeekNews' 도 두 소스를 적도록 고쳤다 — task-106 에서 빠진 자리.

DESIGN.md 에 The Foreign Logo Exception 을 추가했다. 남의 브랜드 색은 팔레트·Two-Mode Parity 밖이고 다크에서 opacity 로만 누른다.

잡 코드(nuc14 ~/jobs/liv-briefing/render.py, 비버전)의 srcmark()/foot()/rest fill 을 같은 때에 고쳤다. assert_filled 가 미치환 {{SRC}} 를 잡으므로 한쪽만 배포되면 발행이 죽는다.

검증: site-check.py 위반 없음. 브라우저 렌더 확인은 못 했다 — 이 머신에 puppeteer/크롬이 없어 render-check.mjs 가 돌지 않는다. 로고 자체는 PIL 로 17px 다운스케일해 식별성을 확인했고, 줄 안 배치(vertical-align -0.22em)는 라이브에서 눈으로 볼 것.
<!-- SECTION:NOTES:END -->
