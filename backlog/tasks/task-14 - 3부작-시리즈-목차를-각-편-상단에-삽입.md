---
id: TASK-14
title: 3부작 시리즈 목차를 각 편 상단에 삽입
status: In Progress
assignee: []
created_date: '2026-07-16 19:31'
updated_date: '2026-07-16 19:39'
labels:
  - solo
dependencies: []
priority: medium
ordinal: 14000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
plan-pipeline(2026-07-11) · backlog-md-vs-plan-md(2026-07-13) · agent-workflow(2026-07-16) 세 편은 같은 주제(topic=workflow)를 잇는 시리즈인데 서로 가는 길이 없다. 세 페이지 모두 상단에 시리즈 목차를 넣어 서로 오갈 수 있게 한다.

시리즈명은 '기획과 실행을 분리하기'. 순서는 시간순 1) 두 세션 플랜 파이프라인 2) Backlog.md 도입 검토 3) 기획과 실행을 분리하는 법.

목차 형태는 시리즈명 라벨 + 번호 붙인 세로 목록이고, 현재 보고 있는 편은 링크 없이 강조하고 '지금 보는 글' 로 표시한다. 나머지 두 편은 상대 경로 링크(../<slug>/).

위치는 홈 링크(← today i learned) 바로 아래, 제목 위. 다만 페이지 셸이 갈린다:
- backlog-md-vs-plan-md, 2026-07-agent-workflow: 공통 셸. main 안 p.home-top 바로 다음에 넣는다.
- 2026-07-plan-pipeline: 자체 스타일. header.hero 안 홈 링크 p 다음, div.kicker 앞에 넣는다. 히어로가 자체 색·타이포를 쓰므로 목차 스타일을 그 페이지 팔레트에 맞춘다.

스타일은 페이지 CSS 변수(var(--text-faint), var(--accent), var(--rule) 등)를 써서 다크모드에 자동 대응시킨다. 세 페이지가 변수명을 공유하는지 각각 확인할 것. 외부 리소스 없이 인라인 CSS 로만.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 세 페이지 모두 상단(홈 링크 바로 아래, 제목 위)에 시리즈 목차가 있다
- [ ] #2 목차는 '시리즈 · 기획과 실행을 분리하기' 라벨 + 1·2·3 번호가 붙은 세로 목록이다
- [ ] #3 현재 보고 있는 편은 링크가 아니라 강조 표시되고 '지금 보는 글' 임이 드러난다
- [ ] #4 나머지 두 편 링크가 상대 경로로 실제 동작한다(로컬 http.server 로 세 페이지 왕복 확인)
- [ ] #5 2026-07-plan-pipeline 은 header.hero 안에 자체 팔레트와 어울리게 들어가 히어로가 깨지지 않는다
- [ ] #6 라이트/다크 양쪽에서 목차 색이 페이지 CSS 변수를 따라간다
- [ ] #7 외부 리소스 의존 없이 각 파일이 단일 파일로 열린다
<!-- AC:END -->
