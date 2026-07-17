---
id: TASK-27
title: 제출 폼을 단일 자유 텍스트로 개편 (URL 필드 제거)
status: Done
assignee: []
created_date: '2026-07-17 08:14'
updated_date: '2026-07-17 08:17'
labels:
  - solo
milestone: m-1
dependencies: []
priority: medium
ordinal: 27000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
사용자 피드백: 항상 URL 을 제출하는 게 아니라 주제만 던질 때도 있으므로 URL 필드가 따로 있는 것이 어색하다. 제출 페이지를 요청 자유 텍스트 하나로 바꾸고(URL 은 텍스트 안에 자연스럽게 포함), 이슈 본문 규약을 SOURCE + REQUEST 블록으로 개정, 워처 파싱·프롬프트·Slack 스니펫을 맞춘다. til-inbox README 규약도 갱신.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 제출 페이지가 요청 텍스트 하나(필수)만 받고 이슈 제목은 요청 첫 줄 요약이 된다
- [x] #2 워처가 REQUEST 블록을 파싱해 프롬프트에 넘기고 mock 으로 성공 경로가 재검증된다
- [x] #3 til-inbox README 의 접수 규약이 갱신된다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
페이지: URL 인풋 제거, 요청 textarea 단일 필드(필수), 제목은 첫 줄 60자 요약, 본문 SOURCE+REQUEST 블록. 워처: REQUEST 블록 파싱(REQUEST: 다음 줄부터 전부), 빈 요청 가드, Slack 스니펫은 python3 로 60자 절단(멀티바이트 안전). mock 실측: 여러 줄 주제형 요청 #5 가 프롬프트에 원문 그대로 전달돼 done+클로즈 완주. 부수 확인: 테스트 중 dirty 가드가 미추적 task 파일에도 걸림 — 정상 동작(porcelain 이 ?? 포함). localStorage 키 불변이라 기등록 토큰 유지.
<!-- SECTION:NOTES:END -->
