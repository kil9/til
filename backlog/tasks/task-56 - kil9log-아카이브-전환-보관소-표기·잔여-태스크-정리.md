---
id: TASK-56
title: kil9log 아카이브 전환 (보관소 표기·잔여 태스크 정리)
status: To Do
assignee: []
created_date: '2026-07-18 15:45'
labels: []
milestone: m-5
dependencies:
  - TASK-55
priority: medium
ordinal: 56000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
대상 repo 는 ~/work/kil9log(private)다. til 쪽 기반(TASK-54·55)이 갖춰진 뒤 kil9log 를 자료 보관소로 전환한다. (1) README.md·AGENTS.md 상단에 아카이브 안내를 단다: 신규 글쓰기·퍼블리시는 til(~/work/kil9/til)에서 진행하고, 이 repo 는 문체 진실원본(archived/ 스타일 가이드 3종 + 페북·텀블러·티스토리 코퍼스)과 과거 글(topics/drafts/published) 보관소다. (2) kil9log backlog 잔여 태스크를 정리한다: TASK-2·3 은 til TASK-55 로 흡수, TASK-4·5·6 은 til draft(네이버 크로스포스트 보류)로 이관, TASK-1 은 폐기(codex 는 이미 til 연동, gemini 는 필요시 재등록) — 각각 이관·폐기 사유를 태스크에 남기고 닫는다. (3) kil9log 의 자동 커밋 규칙에 따라 kil9log 쪽 변경은 kil9log 에 커밋한다(푸시는 하지 않음).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 kil9log README·AGENTS.md 상단에 아카이브 안내와 til 포인터가 있다
- [ ] #2 kil9log 잔여 태스크 6개가 모두 이관·폐기 사유와 함께 정리돼 To Do 가 비어 있다
- [ ] #3 kil9log 쪽 변경이 kil9log 저장소에 커밋돼 있다
<!-- AC:END -->
