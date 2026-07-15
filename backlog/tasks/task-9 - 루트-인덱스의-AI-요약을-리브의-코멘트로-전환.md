---
id: TASK-9
title: 루트 인덱스의 'AI 요약'을 '리브의 코멘트'로 전환
status: In Progress
assignee: []
created_date: '2026-07-15 10:14'
updated_date: '2026-07-15 10:46'
labels: []
dependencies:
  - TASK-6
priority: medium
ordinal: 9000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
루트 index.html 히어로의 'AI 요약' 섹션을 '리브의 코멘트'로 바꾼다. 라벨만이 아니라 요약문 자체의 문체도 리브 1인칭 존댓말로 바꾼다. 라벨만 바꾸면 리브의 코멘트라면서 건조한 3인칭 요약이 나와 어긋난다.

주의: 이 섹션은 repo 밖 머신 로컬 잡(~/jobs/docs-ai-summary/)이 index.html 의 <!-- AI-SUMMARY:START -->~<!-- AI-SUMMARY:END --> 마커 사이를 통째로 덮어쓴다. 따라서 index.html 만 고치면 다음 갱신 때 되돌아간다. 실제 변경 지점은 세 곳이다.
- ~/jobs/docs-ai-summary/inject.py: 섹션 라벨·aria-label 문자열
- ~/jobs/docs-ai-summary/run.sh: 요약 생성 프롬프트를 리브 1인칭 존댓말로. 문체 규칙은 doc-3(TASK-6 개정본)을 따르되 프롬프트에 필요한 만큼만 옮긴다
- repo 의 index.html: 현재 주입돼 있는 섹션 마크업

마커 이름 자체(AI-SUMMARY)를 바꾸려면 inject.py 의 정규식과 index.html 을 동시에 바꿔야 하고, 어긋나면 잡이 'AI-SUMMARY 마커가 없음'으로 죽는다. 굳이 바꿀 이유가 없으면 마커는 유지하고 표시 문자열만 바꾼다.

잡은 머신 로컬이라 이 repo 커밋에 포함되지 않는다(잡 디렉터리는 자체 git repo 인지 확인 후 그쪽 규칙을 따른다).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 inject.py 의 라벨·aria-label 이 '리브의 코멘트'로 바뀌고, run.sh 의 요약 프롬프트가 리브 1인칭 존댓말 문체를 지시한다(doc-3 문체 규칙 준수: 절제·과장 금지·느낌표 1회 이하)
- [ ] #2 repo 의 index.html 에 현재 주입된 섹션도 새 라벨·리브 문체로 갱신하고, 라이트/다크 미리보기를 확인한다
- [ ] #3 잡을 1회 실행해 주입 결과가 새 라벨과 리브 문체로 나오고 마커가 유실되지 않음을 확인한다(신규 페이지가 없어 조기 종료하면 강제 실행 경로로 검증)
<!-- AC:END -->
