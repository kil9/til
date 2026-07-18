---
id: TASK-54
title: til 글쓰기 기반 구조 (topics/·drafts/ + AGENTS.md 워크플로 섹션)
status: To Do
assignee: []
created_date: '2026-07-18 15:44'
labels: []
milestone: m-5
dependencies: []
priority: high
ordinal: 54000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
til 에 글쓰기 작업 공간을 만든다. topics/(글감)·drafts/(초안+대화 로그) 디렉터리를 만들고 .gitignore 에 등록해 비커밋으로 둔다(public repo 라 게시 전 초안 비공개, 머신 간 비동기화는 감수 — 사용자 결정). AGENTS.md 에 글쓰기 워크플로(topics → drafts → 퍼블리시 런북)와 글쓰기 스타일 규칙(이탤릭·볼드·엠대시 금지, 자문자답 제한, 짧게 아이디어 위주 등 kil9log AGENTS.md 의 규칙 1-5)을 옮겨 적는다. 본인 목소리 모사(스타일 가이드·코퍼스)는 복사하지 않고 ~/work/kil9log/archived/ 로컬 경로 참조로만 명시한다(STYLE_GUIDE.md·GAME_REVIEW_STYLE_GUIDE.md·STYLE_ANALYSIS.md·posts/ 코퍼스). 개인 글 인용이 포함된 내용을 til 에 커밋하지 않는 것이 이 마일스톤의 핵심 제약.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 topics/·drafts/ 가 존재하고 .gitignore 로 git 미추적 상태다(.gitkeep 등 구조 표식 방법은 재량)
- [ ] #2 til AGENTS.md 에 글쓰기 워크플로·스타일 규칙 섹션이 있고, 스타일 진실원본은 kil9log 로컬 경로 참조로만 명시돼 있다
- [ ] #3 개인 글 인용·코퍼스 내용이 til 에 커밋되지 않았다
<!-- AC:END -->
