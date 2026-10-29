---
id: TASK-34
title: 리브 페르소나 시스템 프롬프트 구성
status: Done
assignee: []
created_date: '2026-07-17 20:30'
updated_date: '2026-07-17 20:55'
labels: []
milestone: m-2
dependencies: []
priority: medium
ordinal: 34000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
doc-3(리브 캐릭터 설정)을 헤드리스 주입용 시스템 프롬프트로 요약. 대화 응대용(간결·나른·존댓말·관리자님 호칭)과 TIL 근거 Q&A 규약 포함.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 doc-3 기반 리브 대화 페르소나 프롬프트 작성(문체·호칭·톤·드묾 규칙)
- [x] #2 --append-system-prompt 로 claude -p 에 주입 가능한 형태로 파일화
- [x] #3 TIL 저장소 공개 페이지를 근거로 답하는 Q&A 참조 규약 포함
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
산출물: til-inbox repo bot/persona.md (커밋 155d139). doc-3 캐릭터 설정을 헤드리스 claude -p --append-system-prompt 주입용 리브 대화 페르소나로 요약.

대화 레지스터는 Fable advisor(chihaya) 자문 반영 — TIL 페이지 보고서체와 구분되는 실시간 Slack 대화체: 바로 본론·1-3문장 기본·캐릭터성 4-5턴당 1회 이하·호칭 관리자님은 사이트 주인 한정·한숨/말줄임표 연기 및 설정 낭독 금지. 안티패턴(나른함 과잉·설정 낭독·보고서체 유입·이모지 남발·과잉 사과·도서관 어휘 회귀)도 프롬프트에 명시.

AC#2 실증: claude -p --model claude-sonnet-5 --append-system-prompt "$(cat bot/persona.md)" 실주입 검증 — 담백한 자기소개(설정 낭독 없음)·권한 밖 요청 담백 거절·없는 숫자 지어내지 않고 확인 제안 확인. 구독 OAuth 로 동작(ANTHROPIC_API_KEY 미설정).

AC#3 TIL Q&A 규약: 헤드리스 claude -p 가 WebFetch/WebSearch 보유 확인 → '가능하면 사이트 조회 후 답, 실패 시 확인 안 됨 명시, 추측 금지' 조회-도구-있음 버전으로 작성. TASK-36 데몬에서 도구 허용 정책(WebFetch 권한모드) 확정 시 규약 문구 재검토 여지.
<!-- SECTION:NOTES:END -->
