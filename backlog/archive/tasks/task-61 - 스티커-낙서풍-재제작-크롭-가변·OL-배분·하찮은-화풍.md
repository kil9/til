---
id: TASK-61
title: 스티커 낙서풍 재제작 (크롭 가변·OL 배분·하찮은 화풍)
status: Done
assignee: []
created_date: '2026-07-19 12:36'
updated_date: '2026-07-19 12:37'
labels:
  - sticker
dependencies: []
ordinal: 61000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
구 18종은 전신 스탠딩 일변도라 128px 표시에서 정보 없는 하반신이 세로 절반을 먹었다. 크롭을 포즈별로 가변화(상반신 13·허벅지 3·전신 2)하고, 화풍을 하찮은 낙서풍으로 바꾸며, 복장을 포즈마다 OL/후디로 배분한 18종을 stickers-doodle/ 에 신규 제작한다. 구 세트는 보존.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 18종 전부 생성·다이컷 후처리 완료(512/256 양판본)
- [ ] #2 md5 전수 상이(재탕 없음)
- [ ] #3 실제 표시 132px 라이트·다크에서 동작이 읽힘
- [ ] #4 캐릭터 식별 요소(파란 눈·헤어핀 1개·로우 번) 유지
- [ ] #5 doc-3 §4-7·AGENTS.md §2-3 반영
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
18종 stickers-doodle/ 신규 제작 완료. 파일럿 2컷(cross-no·tablet-run)으로 하찮은 강도를 사용자 확정한 뒤 5·5·3·3 배치로 나머지 16컷 생성. md5 전수 상이. 핵심 발견: (1) 상반신 크롭을 프레임 하단에서 자르면 다이컷 flood fill 이 새므로 몸통 밑동을 곡선으로 닫아야 한다, (2) 기준본을 참고로 넣으면 매끈한 화풍까지 복사되므로 '참고 이미지의 화풍을 따르지 말 것'을 명시해야 한다, (3) 거친 선을 요구하면 선에 틈이 생겨 flood fill 구멍이 되므로 '떨리되 끊기지 않는다'를 함께 넣어야 한다. 구 세트 stickers/ 는 보존.
<!-- SECTION:NOTES:END -->
