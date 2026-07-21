---
id: TASK-64
title: 리브 스티커 세트 C (파스텔) 18종 제작
status: Done
assignee: []
created_date: '2026-07-19 15:32'
updated_date: '2026-07-19 15:33'
labels:
  - sticker
dependencies: []
ordinal: 64000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
낙서풍(세트 B) 말고 공식 화풍 기반의 상반신 위주 귀여운 세트를 만든다. 낙서풍과 용도로 병용한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 18종 생성·다이컷(512/256), md5 전수 상이
- [ ] #2 16종 상반신 + 2종 예외, OL 7/후디 11
- [ ] #3 파스텔 룩을 doc-3 공식 복장 배리에이션으로 승격
- [ ] #4 공개 설정화 페이지에 두 세트 섹션 분리 게시
- [ ] #5 구 세트 A 를 legacy/stickers-standing 으로 이관
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
파일럿 3회 끝에 기준 확정. 1차는 '귀엽게' 지시가 화풍을 광택 애니풍으로 끌고 가 2등신이 3등신으로 늘어나고 기호가 멀리 떠 bbox 를 넓혔다. 2차에서 비율·화풍·기호를 부정형으로 눌러 잡았고, 3차에서 사용자 피드백(머리카락 광택 허용, 눈은 크게)을 반영해 확정. 최대 함정은 생성이 아니라 배관이었다 — codex exec 를 & 로 띄운 뒤 부모 셸이 타임아웃으로 죽으면 자식이 stdin 을 잃고 무한 대기에 빠진다(< /dev/null 필수, 20분 소모). 공개 페이지는 두 섹션 분리 + 192px 재임베드로 828KB.
<!-- SECTION:NOTES:END -->
