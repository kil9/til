---
id: TASK-141
title: 리브가 산책 때마다 노트 페이지 디자인을 조금씩 고친다
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
관리자 요청(2026-10-24): 산책 노트를 계속 꾸며 나가는 느낌으로, 무언가를 흉내 내지 말고 리브가 바꾸고 싶은 디자인으로 매일 조금씩 바꾼다. 토큰을 약간 더 써도 된다. 리브 몫의 CSS(liv-notes/liv.css)를 산책 출력으로 통째 고치고, 오늘 바꾼 것을 한 줄로 남긴다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 산책 프롬프트가 현재 liv.css·페이지 구조를 주고 고친 CSS 와 바꾼 이유를 받는다
- [x] #2 CSS 는 url(·@import·역슬래시·< 를 거부하고 크기 상한 안에서만 반영된다
- [x] #3 페이지 끝에 날짜별 '바꾼 것' 기록이 보인다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
walk 프롬프트가 현재 liv.css·최근 고친 기록 5건·페이지 클래스 구조를 주고 design.css(전문)·design.note 를 받는다. 흉내 금지·읽기 편함·다크 모드를 조건으로 명시. ok_css 가 8000자·url(·@import·@font-face·역슬래시·<·중괄호 불균형을 거부(적대 입력 확인). 페이지 끝 details.design-log 에 날짜별 기록. 첫 실측 2026-10-24: '그림첩을 나란히, 그림에 점선 테두리, 종류는 둥근 꼬리표' 반영(37ae153). 산책 비용은 넉넉 단계 /usr/bin/zsh.71·26턴으로 기존과 비슷했다.
<!-- SECTION:NOTES:END -->
