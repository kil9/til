---
id: TASK-146
title: start-topic 문장 다듬기 역할을 무맥락 낭독 검수로 바꾸기
status: To Do
assignee: []
created_date: '2026-10-25T18:15:00Z'
labels: []
dependencies:
  - TASK-145
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
배경: seosoyoung-revision-skill 의 2패스(맥락 없는 새 서브에이전트가 한국 교양 프로그램 아나운서처럼 원고를 소리 내어 읽는 기준으로 검수)를 가볍게 들인다. 지금 start-topic 4단계 역할 4(문장·표현 다듬기)는 스타일 규칙 위반을 찾는 교열이라, 소리 내어 읽을 때 걸리는 어순·긴 관계절·같은 종결 반복은 잘 못 잡는다.

작업 위치: til 저장소 .claude/skills/start-topic/SKILL.md 의 '4. 보조 에이전트' 역할 4 프롬프트.
접근: 역할 4 프롬프트를 낭독 검수로 고친다. 담을 것: 읽기 전용, 0단계에서 진단한 방향(풀어 쓰기 / 덜어내기, task-145 의 korean-polish 진단 결과), 점검 항목(걸리는 어순·조사, 한 호흡에 버거운 긴 문장, 부자연스러운 명사형, 숫자·고유명사 읽기 모호함, 종결 어미 반복), 문체·1인칭·수치 유지, 사용자가 직접 쓴 문장 제외, 보고는 '원문 → 수정안 (이유)' 30개 이내. 기존 스타일 규칙(이탤릭 금지, 엠대시 금지 등) 점검은 유지한다. 서브에이전트는 반론·검증 에이전트와 다른 새 에이전트로 띄운다.
범위 밖: 3패스 프로브, 자동 발행분(liv-walk·liv-briefing)에 적용.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 start-topic SKILL.md 역할 4 프롬프트가 무맥락 낭독 기준과 방향 진단 전달, 사용자 문장 제외를 담고 있다
- [ ] #2 반론·검증 에이전트와 별도의 새 서브에이전트로 띄운다는 규칙이 적혀 있다
- [ ] #3 drafts/ 의 초안 한 편으로 시험 실행해 보고 형식대로 수정 목록이 나오는 것을 확인했다
<!-- AC:END -->
