---
id: TASK-82
title: 리포트 액션 버튼 → til 자동 생성 연동
status: Done
assignee: []
created_date: '2026-07-26 03:55'
updated_date: '2026-07-26 08:14'
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
- [x] #1 PAT 노출 없이 버튼이 동작하는 방식이 결정·구현됐다
- [x] #2 생성된 이슈가 기존 워처의 research 상태 기계를 그대로 탄다
- [x] #3 방향 지시 텍스트가 REQUEST 본문에 함께 실린다
- [x] #4 버튼은 항목당 하나다: 1회 누르면 방향 지시 입력칸이 열리고, 2회 누르면 그대로 접수된다
- [x] #5 지시 없이 눌러도 리브가 알아서 조사 방향을 정해 진행한다
- [x] #6 요청은 조사만(research)이 아니라 til 페이지 생성(submit)까지 간다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
til-inbox 이슈 작성 화면을 쿼리스트링으로 미리 채워 새 탭으로 여는 방식으로 정했다(decision-9). 비밀 슬러그·관리자 사본 두 안은 토큰이 정적 파일에 박히는 문제를 옮기기만 해서 버렸다.

til-inbox 가 비공개 저장소라는 점이 인증을 대신한다 - 관리자가 아니면 그 URL 이 404 이고, 워처는 pending 라벨이 붙은 이슈만 집는데 라벨은 쓰기 권한이 있어야 붙는다. 페이지에는 토큰이 없다.

버튼 동작: 1회 클릭 → 방향 지시 textarea, 2회 클릭 → 이슈 URL 을 새 탭으로 연다(팝업 차단 대비 본문은 클립보드에도 복사). 본문은 SOURCE: briefing (<날짜>) / REQUEST: <제목> — <원문 URL> / 조사 방향 / 관리자 지시 순이고 KIND 는 비운다 — 워처의 기본 경로가 submit(원문을 읽고 til 페이지 생성)이다. 지시를 비워 두면 compose 단계에서 모델이 미리 써 둔 조사 방향(angle)이 그대로 실린다.

URL 길이는 실측 2.5KB 로 브라우저 한도에 여유가 있다(가장 긴 angle 기준).

Cloudflare Tunnel + Access 로 접수 엔드포인트를 노출하면 클릭 하나가 줄지만 서비스·CORS·Access 정책·서버측 토큰이 새로 생긴다. 접수 빈도가 높아지면 그때 window.open 을 fetch 로 바꾼다(본문 규약은 그대로).
<!-- SECTION:NOTES:END -->
