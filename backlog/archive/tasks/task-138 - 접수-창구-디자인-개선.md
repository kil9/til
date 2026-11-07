---
id: TASK-138
title: 접수 창구 디자인 개선
status: Done
assignee: []
created_date: '2026-10-17 01:21'
updated_date: '2026-10-17 01:49'
labels: []
dependencies:
  - TASK-137
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
p/submit-96a2d1c7e19e8a09/index.html(리브의 접수 창구, PWA·공유 시트 진입) 의 화면을 다듬는다. TASK-137 로 받은 내용 카드 + 조사 요청 칸 구조가 생긴 뒤, 그 구조를 기준으로 시각 위계·간격·타이포·카드 표현·상태 메시지(접수 중·완료·실패)·모바일 공유 시트 진입 화면을 개선한다. 사이트 전반 톤은 DESIGN.md 를 따른다.

범위 밖: 리브 캐릭터 그림체 재작업(2026-10-01 중단 결정). 기존 스티커·비주얼은 그대로 쓴다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 모바일 폭(360px)에서 공유 시트로 진입했을 때 받은 내용 카드와 조사 요청 칸, 접수 버튼이 스크롤 없이 한 화면에 들어온다
- [x] #2 접수 중·완료·실패 상태가 시각적으로 구분된다
- [x] #3 DESIGN.md 의 색·타이포 토큰과 어긋나지 않고 라이트·다크 모두에서 확인했다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
DESIGN.md(Hairline Archive) 위반을 걷어냈다: .panel 사각 테두리 → border-top 헤어라인, 파란 면 버튼 → --box 면 + 액센트 글자(높이 44px, 520px 이하 꽉 채움), 입력칸 사각 테두리 → --box 면. 여러 줄 입력에 밑줄 하나는 모바일에서 경계가 사라진다는 Fable 자문을 받아들여, --box 를 접수 폼에 한해 세 번째 용도로 쓰는 예외를 DESIGN.md '폼' 절에 적었다(카드 --box 안은 기각, 왼쪽 헤어라인 인용 블록 유지).
상태 메시지: 진행 중 text-faint, 성공 ✓, 실패 ! 글리프로 색 외 구분, 메시지가 뜨면 scrollIntoView. 공유 진입+토큰 있음일 때만 body.share-entry 로 스티커를 숨기고 제목·인트로 여백을 줄인다(토큰 등록 화면은 안내 유지). 520px 이하 main 패딩 축소.
검증: 헤드리스 chromium 360x640·360x740 라이트·다크에서 공유 진입 시 접수 버튼 하단 624px(한 화면 안, 키보드 닫힌 상태), 성공·실패 상태 화면, 데스크톱 토큰 등록·직접 진입 화면을 눈으로 확인. TASK-137 동작 검증 스크립트 재실행 통과.
<!-- SECTION:NOTES:END -->
