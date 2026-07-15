---
id: TASK-4
title: 런북·루트 인덱스에 서고지기 반영
status: Done
assignee: []
created_date: '2026-07-15 04:56'
updated_date: '2026-07-15 09:39'
labels: []
milestone: m-0
dependencies:
  - TASK-1
  - TASK-3
priority: medium
ordinal: 4000
---

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 AGENTS.md 런북에 신규 페이지의 서고지기 자아 표출 규칙 요약(적용 위치·빈도·톤 + 설정 문서 포인터)을 추가한다. 기존 페이지 소급 없음을 명시한다
- [x] #2 루트 index.html 에 서고지기 소개(이름·한 줄 소개, 이미지 사용 여부는 설정 문서를 따름)를 반영하고 라이트/다크 모드 모두 로컬 미리보기로 확인한다
- [x] #3 README.md 에 반영이 필요한지 검토하고 필요 시 같은 커밋에 포함한다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
AGENTS.md §2-2 '화자 — 서고지기 리브' 신설: 적용 범위(신규 페이지부터, 소급 없음)·자아 표출 위치(제한 없음)·빈도(자리당 1-2문장)·톤(존댓말/사용자님/느낌표 1회 이하)·캐릭터 이미지 운용(SD 메인, 시트 경로, base64 임베드) + doc-3 포인터. 루트 index.html 히어로에 .keeper 소개 블록 추가 — sheet-chibi-smile 에서 얼굴 원형 크롭 48px 아바타(WebP 15.6KB, base64 임베드)+이름+한 줄 소개. AI-SUMMARY 마커 바깥에 배치(로컬 잡 inject.py 가 마커 사이를 덮어쓰므로). 아바타 원본은 backlog/assets/liv/avatar-chibi.webp 보존. 검증: 로컬 http.server + 헤드리스 Firefox 로 라이트/다크 렌더 확인(다크는 media query 스왑 사본으로 캡처). README 개요에 리브 한 줄 추가. AC 3/3 체크.
<!-- SECTION:NOTES:END -->
