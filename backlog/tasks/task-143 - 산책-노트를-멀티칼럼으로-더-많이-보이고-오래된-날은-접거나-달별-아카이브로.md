---
id: TASK-143
title: 산책 노트를 멀티칼럼으로 더 많이 보이고 오래된 날은 접거나 달별 아카이브로
status: To Do
assignee: []
created_date: '2026-10-23 16:35'
labels: []
milestone: m-15
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
관리자 요청(2026-10-24, 당장은 아님): 한 화면에 내용이 더 많이 보이게 멀티칼럼 배치를 쓰고, 오래된 기록은 접어 두거나 아카이브한다. 노트가 하루 5-6건씩 늘어 한 페이지가 계속 길어지는 문제다. 후보: 최근 7-14일만 펼치고 그 전은 날짜별 details 로 접기, 지난달은 p/liv-walk/<YYYY-MM>/ 아카이브 페이지로 굽기(noindex 유지, site-check 링크 검사 통과), 넓은 화면에서 날 묶음을 2-3칸 그리드나 masonry 로. 구조(HTML)는 renderer 몫이고 리브의 CSS(task-141)가 그 위에서 계속 꾸밀 수 있어야 하므로 클래스 구조를 walk 프롬프트의 구조 설명과 함께 갱신한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 넓은 화면에서 기록이 여러 칸으로 놓여 한 화면에 보이는 날 묶음이 지금보다 많다
- [ ] #2 최근 기간 밖의 날은 접히거나 달별 아카이브 페이지로 옮겨지고 본 페이지에서 링크된다
- [ ] #3 walk 프롬프트의 페이지 구조 설명이 새 구조와 맞고, 리브의 기존 liv.css 가 깨지지 않는지 렌더로 확인한다
<!-- AC:END -->
