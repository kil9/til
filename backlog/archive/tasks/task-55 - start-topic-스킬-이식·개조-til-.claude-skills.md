---
id: TASK-55
title: start-topic 스킬 이식·개조 (til/.claude/skills)
status: Done
assignee: []
created_date: '2026-07-18 15:45'
updated_date: '2026-07-19 11:06'
labels: []
milestone: m-5
dependencies:
  - TASK-54
priority: high
ordinal: 55000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
kil9log 의 프로젝트 스킬 start-topic(~/work/kil9log/.claude/skills/start-topic/SKILL.md)을 til/.claude/skills/start-topic 으로 이식하고 til 환경에 맞게 개조한다. 개조 포인트: (1) 맥락 복원을 PLAN.md 기반 → til backlog 기반으로 교체, (2) 퍼블리시 출구를 네이버 붙여넣기 → /publish-til 런북(AGENTS.md 정본)으로 교체, (3) topics/·drafts/ 가 gitignore 비커밋임을 반영(커밋 단계 제외), (4) 문체 참조를 ~/work/kil9log/archived/ 로컬 경로로 명시, (5) 보조 에이전트 역할(반론·비판 1순위, 사실 검증, 관점 확장, 문장 다듬기)과 결과를 drafts 대화 로그로 취합하는 절차를 스킬 본문에 정립한다(kil9log 미완료 TASK-2·TASK-3 흡수). 스킬은 public repo 에 커밋되므로 공개 가능한 내용만 담는다(사용자 결정).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 til/.claude/skills/start-topic/SKILL.md 가 존재하고 backlog·/publish-til·gitignore 초안 정책 기준으로 동작하도록 기술돼 있다
- [x] #2 보조 에이전트 역할 지정·취합 절차가 스킬에 포함돼 kil9log TASK-2·3 을 대체한다
- [x] #3 스킬 본문에 개인 글 인용 등 비공개 내용이 없고, 문체 참조는 kil9log 로컬 경로다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
til/.claude/skills/start-topic/SKILL.md 신설. 개조: 맥락복원을 PLAN.md→backlog(--plain), 출구를 네이버 붙여넣기→/publish-til(런북 정본), topics/drafts gitignore 반영(커밋 단계 제거·backlog 태스크로 추적), 문체 참조는 ~/work/kil9log/archived/ 로컬 경로, 서브에이전트 이름 liv-<model>. kil9log SUBAGENTS.md 의 역할표·역할 프롬프트 4종·결과 취합 절차(판정 태그·요약 통계·기록 형식)를 본문에 편입해 kil9log TASK-2·3 대체. 화자는 decision-6(본인 목소리) 명시. 개인 글 인용 없음 — 경로 참조 2곳뿐.
<!-- SECTION:NOTES:END -->
