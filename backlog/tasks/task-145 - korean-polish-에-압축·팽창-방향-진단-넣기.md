---
id: TASK-145
title: korean-polish 에 압축·팽창 방향 진단 넣기
status: To Do
assignee: []
created_date: '2026-10-25T18:14:00Z'
labels: []
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
배경: eiaserinnys/seosoyoung-revision-skill(MIT)의 0단계 지문 방향 진단을 가볍게 들인다. korean-polish 는 '빼기 우선'과 변경률 50% 가드 때문에 덜어내는 쪽으로만 고친다. 그런데 요약형 글의 AI 티는 주어·접속사가 빠진 압축 지문이라 풀어 써야 사라진다.

작업 위치: ~/work/skills/claude/skills/korean-polish (kil9/skills 저장소에서 커밋).
접근: SKILL.md §0 에 '압축 / 팽창 / 문단별 병행' 진단을 한 단계로 추가하고, 압축으로 판정한 문단에서는 §3 의 빼기 우선과 §4 변경률 가드를 완화한다(주어·목적어·접속사 복원은 주입으로 치지 않는다). 징후 목록은 원 스킬 SKILL.md §4 를 짧게 줄여 담는다. sources.md 에 출처와 MIT 고지를 추가한다.
범위 밖: 3패스 2σ 프로브(우리 코퍼스는 사용자가 직접 쓴 글이라 판정 방향이 뒤집힘), anti-ai-lexicon 전체 병합, 토큰을 많이 쓰는 다중 패스.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 korean-polish SKILL.md 에 압축·팽창 방향 진단 단계가 있고, 진단 결과에 따라 빼기 우선·변경률 가드 적용이 달라진다
- [ ] #2 sources.md 에 seosoyoung-revision-skill 출처와 MIT 고지, 가져온 것과 버린 것이 적혀 있다
- [ ] #3 압축형 문단 하나(drafts/ 의 요약형 문단 등)로 시험해 주어·접속사를 복원한 수정안이 나오는 것을 확인했다
<!-- AC:END -->
