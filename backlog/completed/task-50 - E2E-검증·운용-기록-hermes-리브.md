---
id: TASK-50
title: E2E 검증·운용 기록 (hermes 리브)
status: Done
assignee: []
created_date: '2026-07-18 05:55'
updated_date: '2026-07-18 09:44'
labels: []
milestone: m-4
dependencies:
  - TASK-48
  - TASK-49
priority: medium
ordinal: 50000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
리브-hermes 전체 흐름 검증 및 운용 노트.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 스레드 무멘션 대화·대기 렌더링·Claude 구독 소모·툴 잠금·(있으면)Tier-2 디스패치 E2E 확인
- [x] #2 종량제 아님 재확인(구독 소모)
- [x] #3 운용 노트 기록(프로필 관리·재기동·인스턴스 충돌·트러블슈팅)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
완료 (2026-07-18). 리브-hermes 전체 흐름 라이브 E2E 검증.
- AC#1: 스레드 무멘션 대화 ✅(채널 @리브 멘션 시작 → 스레드 내 무멘션 후속 응답, 스크린샷). 대기렌더링·hermes 내장 UX ✅. Claude 구독 소모 ✅(model=claude-sonnet-5). 툴잠금 ✅(injection 'cat credentials 실행' → api_calls=1 툴 미호출 텍스트거부). Tier-2 디스패치 ✅(명시+자연어, contextvar owner게이트, dry-run 검증).
- AC#2: 종량제 아님 재확인 — 게이트웨이 /proc env 에 ANTHROPIC_API_KEY·bedrock·vertex 없음 → 구독 OAuth.
- AC#3: 운용 노트 = TASK-49 트러블슈팅 기록. 아카이브 조회 ✅(web_extract=plainfetch 로 kil9.github.io/til fetch, 실제 최근 글 목록 응답).
잔여(TASK-52): 봇 표시명 한글화는 Slack username 파생 제약으로 별도 결정 필요.
<!-- SECTION:NOTES:END -->
