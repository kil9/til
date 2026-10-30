---
id: TASK-149
title: 발행 검증에 문서 단위 빈도 검사와 커밋 검증 기록 넣기
status: To Do
assignee: []
created_date: '2026-10-30T08:36:00Z'
labels: []
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
배경: 서소영의 서재(eiaserinnys/seosoyoung-blog) 조사(2026-10-30)에서 사용자가 고른 두 가지.
- 빈도 검사: 그쪽은 지적 1건을 받으면 같은 꼴을 본문 전체에서 센다('…라는 것이다' 1건 지적 → 본문 7건). 문장 단위 검사 셋이 '저자는' 32회를 모두 통과시킨 뒤 문서 단위 주어 빈도 검사를 더했다(글 sentences-i-no-longer-write).
- 검증 기록: 발행 PR 본문에 무엇을 돌려 통과했는지와 함께 확인하지 못한 것('실기기 Safari·Android Chrome, SNS OG 표시는 미확인')을 적는다(PR #377).

현재: TASK-130 의 '이 아카이브' 자기언급 47% 는 손으로 한 번 센 것이고 상시 검사가 없다. til-verify.sh 는 doctype·favicon·og·카드 참조·impeccable detect 만 본다. [publish] 커밋 본문은 갱신한 파일 목록뿐이다.

접근:
1. publish-til 스킬(~/work/skills/claude/skills/publish-til, kil9/skills 저장소에서 커밋)의 til-verify.sh 에 새 페이지 본문 텍스트(스크립트·스타일·data URI 제외)의 빈도를 찍는 advisory 스크립트를 붙인다. 셀 것: 문장 종결 꼴 상위 몇 개, 문두 주어 반복, doc-3 §3-1 의 식상 공식 목록 적중. 임계값을 넘으면 경고만 찍고 exit code 에 넣지 않는다(발행을 막지 않는다 — 무인 접수 til-inbox 경로도 같다).
2. publish-til §6 커밋 템플릿에 '검증:'(돌린 검사와 결과)·'미확인:'(돌리지 못했거나 skip 된 것) 두 줄을 넣고, 이 저장소 AGENTS.md 퍼블리시 런북 §5 와 커밋 규칙에도 반영한다.
범위 밖: 리브다움 확률 프로브, 렌더 화면 검수(이번에 고르지 않았다), 기존 페이지 소급 검사.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 til-verify.sh 가 새 페이지 본문의 종결 꼴·문두 주어·doc-3 §3-1 식상 공식 빈도를 출력하고, 임계값을 넘어도 exit code 는 바뀌지 않는다
- [ ] #2 기존 리브 글 한 편에 돌려 반복 꼴이 실제로 잡히는 것을 확인했다(결과를 notes 에 남긴다)
- [ ] #3 publish-til §6 커밋 템플릿과 til AGENTS.md 퍼블리시 런북에 '검증:'·'미확인:' 줄 규칙이 있다
- [ ] #4 kil9/skills 와 til 에 각각 커밋됐다
<!-- AC:END -->
