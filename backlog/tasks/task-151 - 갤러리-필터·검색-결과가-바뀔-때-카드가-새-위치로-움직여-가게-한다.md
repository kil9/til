---
id: TASK-151
title: 갤러리 필터·검색 결과가 바뀔 때 카드가 새 위치로 움직여 가게 한다
status: Done
assignee: []
created_date: '2026-11-07T05:22:00Z'
updated_date: '2026-11-07T05:24:00Z'
labels: []
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
사용자 요청(2026-11-07): til.kil9.dev 에 적절한 모션그래픽 도입. kil9-design-style §2-9 기준 — 움직임은 무엇이 어디로 갔는지 좇게 할 때만 쓰고 장식 움직임은 쓰지 않는다. 루트 index.html 의 주제 칩·검색은 지금 카드를 즉시 숨기고 보여 줘 남은 카드가 어디서 왔는지 끊긴다. 같은 문서 View Transitions 로 남는 카드는 새 위치로 미끄러지고 빠지는/새로 들어오는 카드는 짧게 페이드되게 한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 주제 칩·검색어 변경 때 남는 카드가 이전 위치에서 새 위치로 이동하고, 빠지는·들어오는 카드는 페이드된다(250ms 안팎)
- [x] #2 prefers-reduced-motion: reduce 이거나 View Transitions 미지원 브라우저에서는 지금과 똑같이 즉시 바뀐다
- [x] #3 넓은·좁은(390px) 폭 × 라이트·다크 캡처에서 넘침·콘솔 오류가 없고 site-check.py 가 통과한다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
같은 문서 View Transitions 로 구현(index.html). 칩 클릭·검색(160ms 입력 멈춤 뒤)에서 카드에 전환하는 동안만 view-transition-name 을 붙였다 떼고(교차 문서 전환에 끼지 않게), root 는 움직이지 않는다. 남는 카드 240ms 이동, 빠지는 카드 90ms 페이드 후 들어오는 카드 150ms 페이드 — 처음엔 셋 다 240ms 였는데 빠지는 카드와 올라오는 카드 글자가 겹쳐 읽혀 나눴다. 검증: puppeteer 로 1280·390 × 라이트·다크 × reduced-motion 8조합 — 전환 2회 발생/reduce 에선 0회, 끝난 뒤 이름·클래스 정리, 가로 넘침 없음, 콘솔 오류는 로컬 출처의 Cloudflare 분석 CORS 뿐. site-check.py 위반 없음.
<!-- SECTION:NOTES:END -->
