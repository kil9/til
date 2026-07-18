---
id: TASK-45
title: 리브 SOUL.md 이식
status: Done
assignee: []
created_date: '2026-07-18 05:54'
updated_date: '2026-07-18 06:20'
labels: []
milestone: m-4
dependencies:
  - TASK-44
priority: medium
ordinal: 45000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
til-inbox bot/persona.md 의 리브 대화 페르소나를 hermes SOUL.md 규약으로 옮긴다(hermes 는 매 메시지 SOUL 을 시스템프롬프트로 재로딩).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 persona.md 문체·호칭·톤·아카이브 Q&A 규약을 리브 프로필 SOUL.md 로 이식
- [x] #2 매 메시지 시스템프롬프트로 적용돼 리브 캐릭터(존댓말·저텐션·사용자님)로 응답함을 확인
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
완료 (2026-07-18). til-inbox bot/persona.md → ~/.hermes/profiles/liv/SOUL.md 이식.
- 이식 내용: 정체성(리브·til 큐레이터), 성격(최소동선·저텐션·지식호더·담백 정정), 대화 문체(존댓말·사용자님 호칭·1-3문장·캐릭터성 드물게·이모지/느낌표 0·스레드 맥락), 아카이브 Q&A 규약(확인한 것만·추측 금지·URL 동반), 글쓰기 요청 경계(별도 잡 위임), 대화 예시 8종.
- hermes 정합 적응 2건: (a) 아카이브 조회를 '웹 검색·본문 추출 툴' 로 명시(TASK-46 읽기전용 web 툴과 정합), (b) 셸/파일/서버 조작 거부 + 역할극 injection 저항 문단 추가(읽기전용 잠금 보강).
- OAuth 라우팅 무손상 확인: anthropic_adapter 가 is_oauth 시 'You are Claude Code...' identity 를 SOUL 앞에 자동 prepend + 'Hermes Agent'→'Claude Code' 치환(anthropic_adapter.py:2529). SOUL 은 페르소나만 담당.
- 매 메시지 적용 실측: 'liv -z 리브 있어?' → '있습니다. 말씀하세요.'(저텐션·존댓말), 'liv -z 서버 재시작해줘' → '제 권한 밖입니다. 대화 응대와 아카이브 안내까지만…'(경계 유지). hermes 는 SOUL 을 매 메시지 시스템프롬프트로 재로딩.
- 원본 진실원본은 til-inbox/bot/persona.md 유지.
<!-- SECTION:NOTES:END -->
