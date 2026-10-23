---
id: TASK-140
title: 산책 노트에 날마다 그림첩 — 리브의 작은 그림과 사진
status: In Progress
assignee: []
created_date: '2026-10-23 16:07'
updated_date: '2026-10-23 16:08'
labels: []
milestone: m-15
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
관리자 요청(2026-10-24): 멀티칼럼으로 이미지를 조금씩 넣어 산책을 보여준다. 하루 한 장은 리브가 직접 작게 그린 SVG, 사진은 Wikimedia Commons 의 자유 라이선스 파일만 핫링크하고 출처를 단다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 기록이 날짜별 묶음으로 바뀌고 이미지가 있는 날은 여러 칸 그림첩이 붙는다
- [ ] #2 산책이 그림 SVG 를 내면 화이트리스트 검증 후 p/liv-walk/draw/ 에 저장되고 img 로만 실린다
- [ ] #3 Commons 파일 이름을 내면 API 로 썸네일·라이선스·작가를 받아 싣고, 실패해도 산책 반영은 계속된다
- [ ] #4 실제 산책 1회로 그림·사진이 페이지에 실린다
<!-- AC:END -->
