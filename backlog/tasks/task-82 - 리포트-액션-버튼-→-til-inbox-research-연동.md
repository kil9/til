---
id: TASK-82
title: 리포트 액션 버튼 → til 자동 생성 연동
status: To Do
assignee: []
created_date: '2026-07-26 03:55'
updated_date: '2026-07-26 05:05'
labels:
  - solo
milestone: m-8
dependencies:
  - TASK-81
priority: medium
ordinal: 82000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
리포트 각 항목의 '더 파보기'·'방향 지시' 버튼이 til-inbox 에 KIND: research 이슈를 만들도록 연결한다. 파일럿은 요청문을 클립보드에 복사만 한다. 이슈 생성에는 PAT 가 필요한데 리포트가 공개 경로에 있으면 곤란하므로, 관리자 제출 페이지(p/submit-<비밀 슬러그>/)처럼 리포트도 비밀 슬러그에 두거나, 공개 리포트에서는 버튼을 감추고 관리자 페이지 사본에서만 노출하는 안을 비교한다. 요청 본문 규약은 til-inbox README 의 SOURCE/KIND/REQUEST 형식을 그대로 쓴다(SOURCE: daily-report).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 PAT 노출 없이 버튼이 동작하는 방식이 결정·구현됐다
- [ ] #2 생성된 이슈가 기존 워처의 research 상태 기계를 그대로 탄다
- [ ] #3 방향 지시 텍스트가 REQUEST 본문에 함께 실린다
- [ ] #4 버튼은 항목당 하나다: 1회 누르면 방향 지시 입력칸이 열리고, 2회 누르면 그대로 접수된다
- [ ] #5 지시 없이 눌러도 리브가 알아서 조사 방향을 정해 진행한다
- [ ] #6 요청은 조사만(research)이 아니라 til 페이지 생성(submit)까지 간다
<!-- AC:END -->
