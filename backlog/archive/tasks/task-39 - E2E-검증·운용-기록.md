---
id: TASK-39
title: E2E 검증·운용 기록
status: Blocked
assignee: []
created_date: '2026-07-17 20:30'
updated_date: '2026-07-17 22:13'
labels: []
milestone: m-2
dependencies:
  - TASK-37
  - TASK-38
priority: medium
ordinal: 39000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
전체 흐름 검증 및 운용 노트.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 멘션/DM → Sonnet 응답, 글쓰기 요청 → Fable 잡 → 공개 TIL 게시까지 E2E 확인
- [x] #2 두 티어 모두 구독 소모(종량제 아님) 확인
- [x] #3 재시작·재부팅 후 지속 구동 확인, 운용 노트 기록
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
검증 완료: AC#2 두 티어 구독소모(Tier-1 데몬 /proc environ 에 ANTHROPIC_API_KEY 부재, Tier-2 워처 claude -p --model fable-5 API키 미설정·cron/rc export 없음·최근 실게시 성공). AC#3 재시작→즉시 재연결 확인, 재부팅은 enabled(default.target.wants)+Linger=yes 로 자동기동 보장, 운용노트 README 기록(til-inbox e5c4029). AC#1 일부: 멘션→Sonnet 라이브 응답 확인, 글쓰기 요청→디스패치→pending 이슈(포맷 워처 소비형과 일치) 확인.

결정 필요(Blocked 사유): AC#1 마지막 링크 = liv 디스패치 → 기존 워처 → **공개 사이트 실제 게시**. 이건 사용자 공개 사이트에 외부노출 산출물을 남기는 비가역 행위라 자는 사용자 대신 자율 게시하지 않았다. 워처 파이프라인 자체는 TASK-26 에서 실게시 E2E 검증됨 + liv 이슈 포맷이 동일하므로 by-construction 로는 동작한다. 사용자가 깨어나면 liv 에게 (멘션+)`!til <주제>` 를 보내 직접 최종 실게시를 트리거하거나, 승인하면 내가 던진다.
<!-- SECTION:NOTES:END -->
