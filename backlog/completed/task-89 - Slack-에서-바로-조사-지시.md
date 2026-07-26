---
id: TASK-89
title: Slack 에서 바로 조사 지시
status: Done
assignee: []
created_date: '2026-07-26 07:28'
updated_date: '2026-07-26 08:24'
labels:
  - solo
milestone: m-9
dependencies:
  - TASK-86
  - TASK-82
priority: medium
ordinal: 89000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
폰으로 Slack 브리핑을 읽다가 바로 조사를 시킬 수 있게 한다. 발행 메시지의 스레드에 답글을 달면 그것이 til-inbox 이슈(KIND: submit)가 되고, 리브가 회신한다. 항목을 특정할 수 있게 메시지에 항목 번호를 넣거나 Block Kit 버튼을 단다.

기존 자산이 절반쯤 있다: til-inbox 워처가 SOURCE/KIND/REQUEST 규약으로 이슈를 소비하고, 리브 봇(hermes-gateway-liv)이 이미 Slack 대화를 받는다. 새로 필요한 것은 발행 메시지 스레드를 브리핑 항목과 묶는 매핑과, 어느 항목을 가리키는지 모호할 때 리브가 되묻는 경로다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 발행 메시지 스레드에 답글을 달면 til-inbox 이슈가 생성된다
- [x] #2 어느 항목에 대한 지시인지 항목 번호나 버튼으로 특정된다
- [x] #3 모호하면 리브가 스레드에서 되묻고, 확정되면 진행한다
- [x] #4 페이지 버튼(task-82)과 같은 요청 규약을 쓴다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
hermes 봇을 건드리지 않고 브리핑 잡 안에서 닫았다. 리브 봇(hermes-gateway-liv)의 자연어 마커 경로와 별개로, 스레드 답글은 폴링으로 읽는다 - 돌고 있는 서비스를 고치지 않아도 되고 단독 테스트가 된다.

배관:
- announce.py 가 발행 메시지에 항목 번호(01\~08)를 넣고, state/threads/<날짜>.json 에 메시지 ts ↔ 항목(번호·제목·URL·조사 방향) 매핑과 처리한 답글 ts 목록을 남긴다.
- thread-watch.py(cron */5 7-23시)가 최근 3일치 스레드의 conversations.replies 를 읽어 관리자(U0B54E64FNW)의 새 답글만 처리한다. 봇 자신의 답글은 무시한다.
- 항목 특정: 'N번' → 그 항목, 숫자 하나만 있어도 그 항목, 제목 일부가 하나만 걸려도 그 항목. 숫자가 여럿이거나 아무것도 안 걸리면 스레드에서 되묻고 그 답글은 처리 완료로 찍는다(다음 답글에서 확정된다).
- 접수 본문은 페이지 버튼(task-82)과 같은 규약이고 SOURCE 만 briefing-slack 이다. KIND 를 비워 워처 기본 경로(submit)로 간다. 답글 문장 전체가 '관리자 지시' 로 실린다.
- 접수하면 스레드에 'NN번 「제목」 으로 접수했습니다' 로 회신한다.

검증: 항목 특정을 7개 문장으로 확인했다('3번 파봐'→03, '3번이랑 5번'→되묻기, 'Mindwalk 좀 봐줘'→05, '뭔가 좋네'→되묻기, '5'→05, 'LangGraph 건 자세히'→07). 실제 스레드(오늘 발행 메시지)에 대해 폴링 경로가 도는 것도 확인했다. 답글 → 이슈 생성은 관리자 계정으로 답글이 달려야 나오므로 실사용에서 처음 확인된다.

pick_item 함정: len(nums)==1 확인 후 제너레이터 안에서 nums.pop() 을 쓰면 비교마다 pop 이 돌아 두 번째 비교에서 빈 set 이 된다. 밖에서 한 번 꺼내 쓴다.
<!-- SECTION:NOTES:END -->
