---
id: TASK-60
title: 스티커 사용 규칙 문서화 + 공개 게시·시범 적용
status: Done
assignee: []
created_date: '2026-07-19 06:23'
updated_date: '2026-07-19 08:00'
labels: []
milestone: m-6
dependencies:
  - TASK-59
priority: medium
ordinal: 60000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
AGENTS.md 퍼블리시 런북에 스티커 사용 규칙(용처, 페이지당 1-2개 노출 원칙, base64 data: URI 임베드, 마크업 패턴)을 추가한다. 공개 설정화 페이지(/p/liv-today/sheet/)에 스티커 섹션을 추가해 전 종을 게시하고, 기존 또는 신규 페이지 1곳에 시범 적용해 라이트/다크 렌더링을 확인한다. 페이지 추가·수정분은 런북 규칙대로 README·갤러리 갱신과 함께 커밋한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 AGENTS.md 에 스티커 사용 규칙 절이 추가된다
- [x] #2 /p/liv-today/sheet/ 에 스티커 섹션이 게시된다
- [x] #3 1개 페이지에 시범 적용되어 라이트/다크 모두에서 테두리·렌더링이 확인된다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
AGENTS.md §2-3 '리브 스티커' 절 추가(용처·페이지당 1-2개·소형 판본 base64·float 마크업·다크모드 무보정). /p/liv-today/sheet/ 에 스티커 18종 섹션 게시(600KB). 시범 적용은 2026/moshi-voice-ai — §2 '결격' 판정에 cross-no, §5 비용 역전 문단에 weigh-both 를 float 로. 브라우저로 라이트/다크 양쪽 렌더링 확인 완료(다크에서 흰 링이 캐릭터를 배경에서 분리해 주고 튀지 않아 brightness 보정 불필요 확인). 배치 중 실측 두 건을 규칙에 반영: (1) 크기는 width 가 아니라 height 로 잡아야 한다(종횡비가 1:2.5 라 width 104px 면 높이가 256px 로 치솟음), (2) float 스티커를 표 바로 앞 문단에 두면 표 폭을 좁히므로 흐르는 본문 옆에 둔다.
<!-- SECTION:NOTES:END -->
