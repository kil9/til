---
id: DRAFT-7
title: 발행 전 자동 점검 — canonical·링크·용량
status: Draft
assignee: []
created_date: '2026-07-26 10:25'
labels: []
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
페이지가 50건을 넘었는데 발행 시 자동 점검이 하나도 없다. rel=canonical 은 2개 페이지에만 있다. 로컬 체커 하나로 묶는다: (1) 전 페이지 canonical 존재·값 일치, (2) 내부 링크 깨짐, (3) 404.html 리다이렉트 맵에 신규 슬러그 등록 여부, (4) HTML 용량 상한(TASK-99 에서 정한 값), (5) 선택적으로 외부 링크 사망 여부(느리므로 별도 실행). 런북 §5 앞에 붙이거나 pre-push 훅으로.
<!-- SECTION:DESCRIPTION:END -->
