---
id: TASK-100
title: 'og:image 도입 — archive-thumbs.py 확장'
status: To Do
assignee: []
created_date: '2026-07-26 10:24'
labels: []
milestone: m-11
dependencies: []
priority: medium
ordinal: 100000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
지금 공유 미리보기가 텍스트뿐이다(Slack·카카오톡·X 에서 회색 블록). T-24(2026-07-12)에서 'OG 이미지는 제외' 로 결정했지만 근거가 어디에도 기록돼 있지 않다. 정황상 이유는 og:image 가 data: URI 를 못 쓴다는 것 — 크롤러가 읽을 실제 URL 이 필요해 당시의 무예외 단일 파일 원칙과 정면 충돌했다. 그 충돌은 p/archive/thumbs/ 사이드카 예외로 이미 해소됐다.

- backlog/assets/archive-thumbs.py 가 이미 각 페이지의 최대 임베드 삽화를 뽑아 480x172 로 굽는다. 같은 추출 결과에서 1200x630 판본을 og/<slug>.webp 로 하나 더 굽는다.
- 삽화 없는 글(현재 49건 중 12건)은 사이트 공통 폴백 1장. 리브 아바타 + 사이트 이름 정도의 정적 이미지로, 페이지마다 만들지 않는다.
- 대표 이미지가 부적절한 글을 위해 카드 data-thumb 처럼 수동 오버라이드 훅을 둔다.
- 각 페이지 head 의 og:image·og:image:width·og:image:height 와 twitter:card 를 summary_large_image 로 올린다. 소급은 TASK-98 과 같은 후처리 스크립트에 얹는다.
- 절대 URL 이어야 한다(https://til.kil9.dev/og/<slug>.webp). 상대 경로는 크롤러가 못 읽는다.
- WebP 를 못 읽는 크롤러가 남아 있는지 확인하고, 문제가 있으면 JPEG 로 굽는다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 삽화 있는 글은 자기 삽화, 없는 글은 공통 폴백으로 og:image 가 붙고 URL 이 절대 경로다
- [ ] #2 archive-thumbs.py 한 번 실행으로 썸네일과 OG 이미지가 함께 생성되고 멱등이다
- [ ] #3 수동 오버라이드 훅이 동작한다
- [ ] #4 실제 공유 미리보기가 Slack 과 카카오톡에서 이미지 카드로 뜬다(라이브 확인)
- [ ] #5 OG 이미지를 쓰기로 바꾼 근거와 T-24 결정 번복이 AGENTS.md 에 반영됐다
<!-- AC:END -->
