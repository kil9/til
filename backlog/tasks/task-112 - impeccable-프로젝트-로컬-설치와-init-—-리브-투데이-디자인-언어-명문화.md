---
id: TASK-112
title: impeccable 프로젝트 로컬 설치와 init — 리브 투데이 디자인 언어 명문화
status: To Do
assignee: []
created_date: '2026-07-28 16:25'
labels: []
milestone: m-12
dependencies: []
priority: medium
ordinal: 6000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
npx impeccable install --scope=project 로 .claude/ 에 스킬·훅을 설치하고 /impeccable init 으로 PRODUCT.md·DESIGN.md 를 만든다. DESIGN.md 는 AGENTS.md §2-2 와 doc-3(리브 투데이 캐릭터 설정)의 문체·디자인 규칙을 흡수해 사이트 디자인 언어를 명문화한다 — 기존 규칙과 모순을 만들지 않는다. main 루트가 GitHub Pages 로 공개 서빙되므로 .impeccable/(리뷰 보고서·라이브 상태)은 반드시 gitignore 에 넣는다. 훅은 .claude/settings.local.json(gitignore)에 등록되므로 머신별 1회 재등록이 필요하다 — 이 사실을 AGENTS.md 에 남긴다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 install --scope=project 와 init 이 완료되고 /impeccable 커맨드가 동작한다
- [ ] #2 DESIGN.md 가 AGENTS.md §2-2·doc-3 과 모순 없이 사이트 디자인 언어를 명문화한다
- [ ] #3 .impeccable/ 이 gitignore 에 있다
- [ ] #4 HTML 편집 시 훅(hook.mjs)이 발동하는 것을 확인했다
<!-- AC:END -->
