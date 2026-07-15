---
id: TASK-6
title: '리브 설정 개정: ''서고지기'' 폐기, AI 지식 큐레이터 · 풀네임 리브 투데이'
status: To Do
assignee: []
created_date: '2026-07-15 10:13'
labels: []
dependencies: []
priority: high
ordinal: 6000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
사용자 피드백으로 캐릭터 컨셉을 재조정한다. '서고지기'라는 직함과 '서고' 비유를 사이트 전반에서 걷어내고, 실제 역할 그대로 'AI 지식 큐레이터'로 정리한다. 풀네임은 '리브 투데이'(로마자 Liv Today)로 확정한다.

진실원본 doc-3 를 먼저 고치고 런북·공개물이 그것을 따르게 한다. 개정 범위는 진실원본(doc-3)·런북(AGENTS.md §2-2)·공개물(README, 루트 index.html)까지다. 완료 이력(doc-2 프로젝트 계획, 마일스톤 m-0, 완료 태스크 파일·notes, 아카이브 PLAN.md)은 그때의 판단 기록이므로 소급하지 않는다. 공개 페이지 liv-archivist 는 TASK-7 에서 통째로 대체되므로 여기서 손대지 않는다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 doc-3 를 개정한다: 직함·정체성을 'AI 지식 큐레이터'로, 풀네임 '리브 투데이'(로마자 Liv Today)를 명시하고, 문체 규칙의 '서고' 시그니처 표현과 도서관 비유 잔재를 삭제해 대체 어휘를 규정한다. 예문도 새 어휘로 고친다
- [ ] #2 AGENTS.md §2-2 의 제목·본문에서 '서고지기'·'서고' 표현을 제거하고 doc-3 개정본과 일치시킨다
- [ ] #3 README 개요 한 줄과 루트 index.html 의 .keeper 소개 문안(이름·한 줄 소개)을 새 명칭으로 갱신하고, 로컬 미리보기로 라이트/다크를 확인한다
- [ ] #4 doc-3·AGENTS.md·README·index.html 에 '서고지기'·'서고' 잔존이 없음을 grep 으로 확인한다(완료 이력 문서와 liv-archivist 는 제외)
<!-- AC:END -->
