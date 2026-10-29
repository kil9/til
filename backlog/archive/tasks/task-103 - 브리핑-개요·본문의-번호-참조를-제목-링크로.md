---
id: TASK-103
title: 브리핑 개요·본문의 번호 참조를 제목 링크로
status: Done
assignee: []
created_date: '2026-07-26 14:17'
updated_date: '2026-07-26 14:28'
labels: []
dependencies: []
priority: medium
ordinal: 1000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
브리핑 페이지에서 항목을 '06' 같은 두 자리 번호로 가리키는 자리가 여럿이다(개요 박스의 '오늘 하나만 고른다면' 한 줄, 리브 머리말·한마디의 상호 참조). 번호만 봐서는 무슨 글인지 알 수 없고 앵커를 눌러 본 뒤에도 되돌아와야 이해가 된다. 참조 자리를 전부 글 제목으로 바꾸고 그 제목 자체가 해당 항목 앵커로 가는 링크가 되게 한다.

배관: 템플릿은 backlog/assets/briefing/(template.html·item.html), 발행 잡은 nuc14 머신 로컬 ~/jobs/liv-briefing/(compose.py·render.py, repo 밖·비버전). 현재 PICK_LINE 은 잡이 '06 — …' 형태의 평문을 만들어 넣는다. 참조 대상 제목·앵커를 함께 넘기도록 토큰을 늘리고(예: PICK_TITLE), 본문 중 상호 참조는 compose 프롬프트가 번호 대신 제목을 쓰도록 규칙을 고친다. 본문 h3 의 01/02 rank 뱃지는 위치 표시라 그대로 둔다. 템플릿·README 변경은 repo 커밋, 잡 변경은 머신 로컬.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 개요 박스의 '오늘 하나만 고른다면' 이 번호 대신 글 제목을 노출하고, 그 제목을 누르면 해당 항목 앵커로 이동한다
- [ ] #2 리브 머리말·한마디 등 본문 안에서 다른 항목을 가리킬 때 번호가 아니라 제목(앵커 링크)으로 나온다 — compose 프롬프트/렌더 규칙에 반영
- [ ] #3 backlog/assets/briefing/README.md 의 토큰 표가 실제 템플릿과 일치한다
- [ ] #4 다음 회차(또는 재렌더한 기존 회차)에서 번호만 있는 참조가 남아 있지 않음을 실물로 확인
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
템플릿에 PICK_TITLE 추가(pick 라벨은 <p>, 제목이 앵커 링크). 잡(~/jobs/liv-briefing, 머신 로컬): compose 프롬프트에 '참조는 번호 대신 제목' 규칙 3곳, render 에 numbers_to_titles(조사 자동 교정)·titles_to_links(liv 의 「제목」 자동 링크)·pick line 번호 머리 제거. 2026-07-26 회차를 재렌더해 번호 링크 0건 확인.
<!-- SECTION:NOTES:END -->
