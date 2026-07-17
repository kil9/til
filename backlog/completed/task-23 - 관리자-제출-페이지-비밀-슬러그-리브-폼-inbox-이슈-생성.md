---
id: TASK-23
title: '관리자 제출 페이지: 비밀 슬러그 + 리브 폼 + inbox 이슈 생성'
status: Done
assignee: []
created_date: '2026-07-17 07:27'
updated_date: '2026-07-17 07:42'
labels:
  - solo
milestone: m-1
dependencies:
  - TASK-22
priority: medium
ordinal: 23000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
til repo 에 비밀 랜덤 슬러그 디렉터리로 관리자 전용 제출 페이지를 만든다. 갤러리·README 에 등록하지 않고 noindex 를 단다(liv-today/sheet 미노출 전례). 상단에서 리브가 아바타와 함께 맞아주고, URL(필수)+메모(선택) 폼을 둔다. 제출 JS 는 localStorage 의 fine-grained PAT(최초 1회 입력 UI, kil9/til-inbox Issues RW 한정)로 api.github.com 을 직접 호출해 til-inbox 에 접수 이슈를 만든다(CORS 실측 확인, TASK-21). PAT 미설정·인증 실패·성공 각각의 피드백을 리브의 말투로 표시한다. 공통 셸 디자인, 다크모드, 외부 리소스 금지.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 비밀 슬러그 페이지가 생성되고 갤러리·README·sitemap 어디에도 노출되지 않으며 noindex 메타가 있다
- [x] #2 PAT 최초 1회 입력·localStorage 보관·재설정 UI 가 동작한다
- [x] #3 URL 제출 시 til-inbox 에 규약(TASK-22) 포맷의 이슈가 생성되고 성공/실패 피드백이 표시된다
- [x] #4 리브 인사·아바타가 있고 공통 셸 디자인과 다크모드를 따른다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
슬러그는 미노출 원칙에 따라 여기 기록하지 않음(디렉터리는 repo 트리에서 보이지만 문서·갤러리·README 에 링크하지 않는다 — 방어선은 PAT). PAT 패널(localStorage til-inbox-pat, 등록 시 GET /repos 검증)·제출 폼·리브 인사(base 표정 아바타 72px WebP, RIFF 헤더 검증) 구현. 이슈 페이로드는 gh 토큰 curl 로 실측(201, pending 라벨, 본문 규약 일치 — 테스트 이슈 #1 은 done 클로즈). 의도적 이탈: OG 메타·CF beacon 생략 — 미노출 관리자 페이지라 슬러그를 소셜 캐시·애널리틱스 경로에 남기지 않기 위함. PAT 실토큰 브라우저 플로는 TASK-26 E2E 에서 검증.
<!-- SECTION:NOTES:END -->
