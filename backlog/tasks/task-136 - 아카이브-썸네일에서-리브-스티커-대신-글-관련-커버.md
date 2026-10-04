---
id: TASK-136
title: 아카이브 썸네일에서 리브 스티커 대신 글 관련 커버
status: Done
assignee: []
created_date: '2026-10-04 07:04'
updated_date: '2026-10-04 07:08'
labels: []
dependencies:
  - TASK-135
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
/p/archive/ 격자 커버가 리브 스티커 위주라는 사용자 요청(2026-10-04). archive-thumbs.py 가 '가장 큰 임베드 이미지'를 고르다 보니 삽화 없는 글은 리브 스티커가 커버가 된다. 기존 페이지 재생성 없이, 스티커(알파 큰 이미지)는 커버 후보에서 빼고 남는 글은 그 글의 data-icon 을 크게 얹은 주제 타일로 대신한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 archive-thumbs.py 가 알파가 큰 스티커류를 격자 썸네일 후보에서 제외하고, OG 이미지는 종전대로 굽는다
- [x] #2 썸네일 없는 글의 커버가 주제 색 타일 위 그 글의 data-icon(이모지·로고)으로 그려진다
- [x] #3 재생성 후 격자 커버에 리브 단독 스티커가 남지 않는다(삽화 속 리브 장면은 유지)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
archive-thumbs.py 가 격자 썸네일 후보에서 알파 비율 0.15 초과(리브 스티커·아바타류)를 뺀다(largest_image allow_sticker=False). OG 는 종전대로 스티커 포함. 재생성 결과 썸네일 81→55건, 빠진 26건은 전부 리브 단독 스티커였고 남은 썸네일·OG 81장은 바이트 변화 없음(리브 장면 삽화 유지). /p/archive/ coverFor 가 썸네일 없는 글에 카드 data-icon(TASK-135)을 46px 원형 배지로 주제 색 타일 위에 얹는다. 검증: 1280px 라이트·다크 스크린샷 육안 확인, site-check·render-check 위반 없음. 기존 페이지 삽화 재생성은 하지 않았다(사용자 요청).
<!-- SECTION:NOTES:END -->
