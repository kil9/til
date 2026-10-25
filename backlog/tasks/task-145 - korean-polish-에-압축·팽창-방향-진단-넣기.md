---
id: TASK-145
title: korean-polish 에 압축·팽창 방향 진단 넣기
status: Done
assignee: []
created_date: '2026-10-25T18:14:00Z'
updated_date: '2026-10-25T18:22:00Z'
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
- [x] #1 korean-polish SKILL.md 에 압축·팽창 방향 진단 단계가 있고, 진단 결과에 따라 빼기 우선·변경률 가드 적용이 달라진다
- [x] #2 sources.md 에 seosoyoung-revision-skill 출처와 MIT 고지, 가져온 것과 버린 것이 적혀 있다
- [x] #3 압축형 문단 하나(drafts/ 의 요약형 문단 등)로 시험해 주어·접속사를 복원한 수정안이 나오는 것을 확인했다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
무엇을: korean-polish SKILL.md §0 에 '방향' 단계(압축/팽창/문단별)를 넣고, 압축 문단에서는 §3 철칙 3(빼기 우선)에 복원 예외, §4 변경률에서 보탠 어절 제외(대신 1.5배 상한)·주입 점검 완화를 걸었다. §5 진단 요약에 방향 표시. sources.md 에 seosoyoung-revision-skill(68db489) 출처·MIT 고지·버린 것(2σ 프로브, 2패스·lexicon·다중 패스, 장르별 비율·SNS 게이트)과 이유를 적었다. 커밋은 kil9/skills ca7b29e·d40d8f0.
왜: 빼기 우선과 50% 가드 때문에 요약형 글의 압축 지문을 덜어내는 쪽으로만 고쳤다. 압축 판정은 징후가 한 문단에 셋 이상 겹칠 때만 하게 해 일반 글이 늘어지지 않게 했다.
검증: 맥락 없는 Sonnet 서브에이전트에 고친 SKILL.md 만 읽혀 압축형 다이제스트 문단(2026-10-25 브리핑의 Docker 글을 다이제스트 투로 줄인 시험용 문단. drafts/ 의 글은 사용자 문장이 대부분이라 압축 징후가 약해 쓰지 않았다)을 고치게 했다. 방향을 '전 문단 압축'으로 판정하고 주어('컨테이너는')·접속사('그래서')·조사·서술어를 복원했다. 길이 1.16배, 변경률 41%(보탠 어절 제외), 의미 보존 6/6.
참고: 첫 커밋 ca7b29e 는 이 세션 편집을 옆 세션(session_01SzfTQKyLbRSL5te41dvqED)이 skills 저장소에서 커밋한 것이다. 내용은 동일해 되돌리지 않았다.
<!-- SECTION:NOTES:END -->
