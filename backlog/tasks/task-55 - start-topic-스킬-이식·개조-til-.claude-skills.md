---
id: TASK-55
title: start-topic 스킬 이식·개조 (til/.claude/skills)
status: To Do
assignee: []
created_date: '2026-07-18 15:45'
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
- [ ] #1 til/.claude/skills/start-topic/SKILL.md 가 존재하고 backlog·/publish-til·gitignore 초안 정책 기준으로 동작하도록 기술돼 있다
- [ ] #2 보조 에이전트 역할 지정·취합 절차가 스킬에 포함돼 kil9log TASK-2·3 을 대체한다
- [ ] #3 스킬 본문에 개인 글 인용 등 비공개 내용이 없고, 문체 참조는 kil9log 로컬 경로다
<!-- AC:END -->
