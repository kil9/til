---
id: TASK-148
title: '''자리·손잡이'' 규칙을 낱말 대체표에서 판정 기준 한 문장으로 바꾸기'
status: To Do
assignee: []
created_date: '2026-10-30T08:36:00Z'
labels: []
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
배경: 서소영의 서재(eiaserinnys/seosoyoung-blog) 글 sentences-i-no-longer-write(2026-09-22). 물리 동사 10개를 금지하자 엿새 뒤 원고에서 표에 없는 15개가 같은 일을 했다. 대안 단어 열이 있으면 관계를 정하지 않고 낱말만 바꿔 끼울 수 있어서, 규칙을 '만질 수 없는 것(점수·범위·책임)을 주어·목적어로 두고 물리적 위치·동작·속성 서술어로 그 관계를 설명하는 문장은 관계를 명명하는 말로 바꾼다'는 판정 기준으로 바꿨다. 2026-10-30 조사에서 사용자가 도입을 골랐다.

현재: korean-polish 는 references/ai-tells.md T24(추상 개념 + 물리 서술어)로 이미 이 기준을 들였다(2026-10-27). 남은 곳은 낱말 대체표 둘이다.
- 글로벌 CLAUDE.md '사용자 커뮤니케이션 규칙'의 '손잡이·자리 를 덜 쓴다(§17)' 항목. 원본 ~/kil9conf/claude/CLAUDE.global.md, 근거 ~/kil9conf/backlog/docs/doc-29 §17('손잡이 → 버튼·명령…', '자리 → 위치·줄·함수…' 대체표). kil9conf 저장소에서 커밋한다.
- 이 저장소 AGENTS.md §2-2 의 '"~한 자리" 금지' 항목과 그 정본 backlog/docs/doc-3 §3-1('곳·문단·번으로 바꾼다').

접근: 두 곳의 본문을 T24 판정 기준 한 문장으로 다시 쓰고, 대체 낱말은 '예: …' 로만 남긴다. doc-29 §17 의 진단('추상적이어서 읽는 쪽이 한 번 더 추론한다')은 서소영 쪽 관찰과 같으므로 유지하고, 대체표가 실패하는 이유(새 낱말로 옮겨 간다)와 출처를 덧붙인다. 유지할 것: §17 의 '금지가 아니라 빈도를 줄인다' 취지, 비유가 실제로 맞을 때 남기는 예외, '자리를 맞추다'·'그 자리에서' 같은 관용 표현 예외. '손잡이' 도 추상 개념의 물리 비유라 같은 기준에 들어간다.
범위 밖: 기존 문서·페이지에서 두 낱말 일괄 치환, korean-polish 수정(이미 T24 가 있다).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 글로벌 CLAUDE.md(kil9conf claude/CLAUDE.global.md) §17 항목이 낱말 대체표가 아니라 판정 기준 한 문장으로 적혀 있고, '빈도를 줄인다' 취지와 관용 표현·실제로 맞는 비유 예외가 남아 있다
- [ ] #2 doc-29 §17 에 대체표가 실패하는 이유와 서소영 sentences-i-no-longer-write 출처, korean-polish T24 참조가 추가돼 있다
- [ ] #3 til AGENTS.md §2-2 와 doc-3 §3-1 의 '자리' 항목이 같은 판정 기준으로 바뀌고 대체 낱말은 예시로만 남아 있다
- [ ] #4 kil9conf 와 til 에 각각 커밋됐다
<!-- AC:END -->
