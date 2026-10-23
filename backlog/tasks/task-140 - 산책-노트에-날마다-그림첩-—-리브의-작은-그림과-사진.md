---
id: TASK-140
title: 산책 노트에 날마다 그림첩 — 리브의 작은 그림과 사진
status: Done
assignee: []
created_date: '2026-10-23 16:07'
updated_date: '2026-10-23 16:21'
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
- [x] #1 기록이 날짜별 묶음으로 바뀌고 이미지가 있는 날은 여러 칸 그림첩이 붙는다
- [x] #2 산책이 그림 SVG 를 내면 화이트리스트 검증 후 p/liv-walk/draw/ 에 저장되고 img 로만 실린다
- [x] #3 Commons 파일 이름을 내면 API 로 썸네일·라이선스·작가를 받아 싣고, 실패해도 산책 반영은 계속된다
- [x] #4 실제 산책 1회로 그림·사진이 페이지에 실린다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
기록을 달→날 묶음으로 바꾸고 날마다 .album 그리드(모바일 2칸) 그림첩. SVG 는 ElementTree 로 파싱해 허용 요소·속성만 다시 쓰고(script·a·style·on* 제거를 적대 입력으로 확인) p/liv-walk/draw/<날짜>.svg 에 저장, <img> 로만 싣는다. 사진은 모델이 Commons 파일 이름을 내면 walk.py 가 API 로 썸네일(utm 꼬리 제거)·작가·라이선스를 받고, 없는 파일은 건너뛴다. 실측 2026-10-24: 동굴 진주 그림 1장 + Carlsbad 동굴 진주 사진(Public domain, 200 image/jpeg) 게재(37ae153). nuc14 ~/jobs/liv-walk 의 walk.py·run.sh 도 고쳤다(비버전, 백업 state/*.bak-decor).
<!-- SECTION:NOTES:END -->
