---
id: TASK-137
title: '접수 창구: 받은 내용과 조사 요청을 두 칸으로 나눈다'
status: Done
assignee: []
created_date: '2026-10-17 01:21'
updated_date: '2026-10-17 01:47'
labels: []
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
p/submit-96a2d1c7e19e8a09/index.html 의 입력이 textarea(#request) 하나뿐이다. 공유 시트로 들어오면 prefillFromShare() 가 title·text·url 을 그 칸에 몰아 넣어서, 조사 방향을 덧붙이려면 스크롤해 맨 위나 맨 아래로 가야 한다(모바일에서 특히 불편).

접근: 위 칸은 받은 내용, 아래 칸은 빈 textarea 로 '이런 식으로 조사해 줘' 같은 요청을 쓴다.
- 공유 진입: 받은 title·text·url 은 편집칸이 아니라 고정 카드(제목·도메인·URL 이 보기 좋게 정리된 형태)로 보여 준다. 잘못 들어왔을 때 비우거나 고칠 수단은 둔다.
- 직접 진입: 위 칸은 URL·주제를 넣는 입력칸이다.
- 제출: 두 값을 별도 필드로 나란히 이슈 본문에 싣는다. 워처(til-inbox/watcher/run.sh:164)는 'REQUEST:' 줄 아래 전부를 자유 텍스트로 받으므로, REQUEST 블록 안에 '받은 내용' / '조사 요청' 소제목으로 나눠 담으면 워처 변경 없이 호환된다. 이슈 제목은 받은 내용 첫 줄(제목)에서 만드는 현행 규칙을 유지한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 공유 시트로 진입하면 받은 title·text·url 이 고정 카드로 표시되고, 그 아래 빈 textarea 에 커서가 놓인다
- [x] #2 직접 진입하면 위 칸에 URL·주제를, 아래 칸에 조사 요청을 따로 쓸 수 있다
- [x] #3 제출된 이슈 본문의 REQUEST 블록에 받은 내용과 조사 요청이 구분돼 담기고, 조사 요청이 비어 있어도 접수된다
- [x] #4 워처 run.sh 의 REQUEST 파싱이 수정 없이 새 본문을 처리한다(test-run.sh 류로 확인)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
입력을 '받은 내용'(#source)과 '조사 방향'(#note) 두 칸으로 나눴다. 공유 진입이면 #source 를 숨기고 title·text·url 을 왼쪽 헤어라인 카드로 보여 준다(본문 3줄 clamp·눌러서 펼치기, URL 은 도메인+경로 mono, 고치기·비우기). 접수 값의 진실원본은 언제나 #source.
본문: REQUEST 블록에 받은 내용을 라벨 없이 먼저, 그 뒤에 '관리자가 원하는 조사 방향:' 라벨로 note. 워처 Slack 스니펫이 REQUEST 첫 줄이라 라벨을 앞에 두지 않았다. 한쪽만 있으면 라벨 없이 그 값만.
Fable 자문 반영: 성공 시 카드·공유 쿼리까지 한 함수(resetForm)로 정리, focus 는 접수 패널이 보일 때만(토큰 등록 직후 재시도), 빈 제출은 err 메시지, displayUrl 은 new URL try/catch.
검증: 헤드리스 chromium(360px)에서 공유 진입→카드 표시·#note focus, 접수 POST 본문 캡처, 리셋 후 카드 제거·쿼리 삭제, 직접 진입 note 만 접수, 빈 제출 메시지, 비우기, 토큰 없음+공유 시 focus 이동 없음. run.sh 160-180행의 sed/python 을 같은 본문으로 돌려 req 전체 보존·스니펫=제목 확인(워처 수정 없음).
<!-- SECTION:NOTES:END -->
