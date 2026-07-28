---
id: TASK-114
title: 발행 전 점검에 impeccable detect 게이트 추가
status: Done
assignee: []
created_date: '2026-07-28 16:25'
updated_date: '2026-07-28 18:01'
labels: []
milestone: m-12
dependencies:
  - TASK-112
priority: medium
ordinal: 8000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
발행 전 자동 점검(TASK-109 로 완료된 canonical·링크·용량 점검)에 새 페이지 디렉터리 대상 npx impeccable detect 를 게이트로 추가해 신규 페이지부터 0 failures 를 기본으로 한다. advisory(em-dash 등)는 발행을 막지 않는다 — advisory 는 exit code 에 반영되지 않으므로 failures 만 기준으로 삼으면 된다. 점검 스크립트가 til repo 쪽에 있으면 여기서, /publish-til 스킬 쪽 변경이 필요하면 skills repo(~/work/skills)에서 커밋한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 발행 플로에 detect 게이트가 들어가 신규 페이지가 0 failures 여야 발행된다
- [x] #2 advisory 는 발행을 막지 않는다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
게이트는 skills repo 의 publish-til/til-verify.sh 에 넣었다(커밋 531d7be, codex 쪽은 심볼릭 링크라 자동 반영). site-check.py 가 아니라 여기인 이유는 site-check 가 사이트 전체를 보는 자리라 기존 발행물 잔재로 새 글이 막히기 때문 — 게이트는 새 페이지 디렉터리 하나만 본다.
detect 는 failures 가 있을 때만 exit 2 로 끝나고 advisory 는 exit code 에 안 들어가므로, exit code 만 보면 AC #2 가 저절로 충족된다. exit != 0,2 (미설치·네트워크 실패)는 skip 을 찍고 넘어간다 — 품질 게이트라 발행을 막지 않되 조용히 통과시키지도 않는다. 하드 게이트는 site-check.py 가 계속 맡는다.
실측 검증 3종: 2026/codex-code-mode-batching(정상) → verify ok exit 0 / p/til-archive(failures) → FAIL exit 1 / index.html·404.html·p/archive(advisory 만) → 0 findings exit 0.
문서 반영: skills repo SKILL.md §5, til repo AGENTS.md 퍼블리시 런북 §5.
<!-- SECTION:NOTES:END -->
