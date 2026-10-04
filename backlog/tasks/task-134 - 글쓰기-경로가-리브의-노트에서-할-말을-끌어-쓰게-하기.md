---
id: TASK-134
title: 글쓰기 경로가 리브의 노트에서 할 말을 끌어 쓰게 하기
status: In Progress
assignee: []
created_date: '2026-10-04 03:00'
updated_date: '2026-10-04 03:26'
labels: []
milestone: m-15
dependencies:
  - TASK-130
  - TASK-131
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
노트(task-131)가 쌓여도 페이지·브리핑 머리말을 쓰는 경로가 읽지 않으면 코멘트는 그대로다. 퍼블리시(/publish-til, AGENTS.md §2-2)·브리핑 INTRO·til-inbox 리서치 경로가 노트 발췌를 받아, 아카이브 구조 대신 리브가 본 것·좋아하는 것에서 비유와 감상을 끌어오게 한다. 반대로 노트를 매번 자랑처럼 끼워 넣지 않도록 '드물수록 효과가 크다'(doc-3 §3-1) 원칙도 함께 건다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 퍼블리시·브리핑·리서치 경로가 노트 발췌를 프롬프트로 받는다
- [ ] #2 새로 발행된 .liv 몇 건에서 아카이브 자기언급 대신 노트 유래의 비유·감상이 쓰인 것을 확인한다
- [x] #3 노트 언급이 페이지마다 반복되지 않도록 빈도 기본값이 문체 규칙에 명시된다
- [x] #4 기존 발행 페이지는 수정하지 않는다 — 노트 반영은 이후 발행분에만 적용된다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
2026-10-04 배선: (1) 퍼블리시 — AGENTS.md §2-2 에 'liv-notes.py excerpt --for write --topic' 단계 추가(/publish-til 은 런북을 정본으로 따른다). (2) 무인 접수 — til-inbox f351cdd 가 요청 원문으로 발췌해 <liv-notes> 로 주입, 도구 없으면 '(발췌 없음)', test-run.sh PASS. (3) 브리핑 — nuc14 ~/jobs/liv-briefing/compose.py 에 liv_notes(오늘 선별 제목으로 발췌) 주입, 화자 규칙에 task-130 자기언급 기본값도 반영('한 자리당' 표현도 교체). 2026-10-04 선별분으로 프롬프트 조립 확인(발췌 2339자). 빈도 기본값: doc-3 §3-1·AGENTS §2-2 에 페이지당 1번 이하·브리핑 회차당 1번 이하·같은 항목 연속 사용 금지.
남은 것: AC2 — 다음 발행분(브리핑 10-05 09:00, 다음 til-inbox 접수)의 .liv·liv 한마디를 확인해야 닫는다.
<!-- SECTION:NOTES:END -->
