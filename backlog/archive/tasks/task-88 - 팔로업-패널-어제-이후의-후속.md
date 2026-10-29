---
id: TASK-88
title: 팔로업 패널 (어제 이후의 후속)
status: Done
assignee: []
created_date: '2026-07-26 07:27'
updated_date: '2026-07-26 08:27'
labels:
  - solo
milestone: m-9
dependencies:
  - TASK-85
  - TASK-82
priority: medium
ordinal: 88000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
브리핑을 1회성에서 연속물로 만든다. 오늘의 개요 패널 아래에 2-3행으로 (1) 어제 이후 TIL 만들기로 접수된 건의 처리 상태와 완성된 페이지 링크, (2) 지난 브리핑에 실었던 항목의 후속 소식(그 프로젝트가 v2 를 냈다, 그 주장이 반박됐다 등)을 보여 준다.

데이터 출처는 til-inbox 이슈 상태와 이전 브리핑의 state 파일이다. 파일럿 때는 데이터가 없어 보류했던 항목이며(Fable 자문 C안), 발행이 며칠 쌓인 뒤에 착수한다. 빈 날에는 패널 자체를 렌더링하지 않는다 — 매일 '없음'이 찍히면 그 자리가 죽는다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 전날 이후 접수된 TIL 요청의 상태가 브리핑에 보인다
- [x] #2 완성된 til 페이지로 바로 갈 수 있다
- [x] #3 보여 줄 것이 없는 날에는 패널이 아예 렌더링되지 않는다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
개요 패널 아래 '어제 이후' 블록으로 넣었다(.followup, 우측 칼럼).

- followup.py 가 til-inbox 이슈를 직전 브리핑 시각 이후로 훑어 상태(접수됨·작업 중·완성·실패)와 완성 페이지 링크를 모은다. 링크는 워처가 done 시 남기는 '게시 완료: <URL>' 코멘트에서 뽑는다. 최대 6건, 완성분이 위로.
- 지난 브리핑 항목의 후속은 compose 단계에서 처리한다: 직전 briefing-*.json 의 항목 목록을 프롬프트에 넣고, 오늘 재료에 그 후속이 실제로 있을 때만 followup_notes 에 0-2문장을 쓰게 했다. 억지로 채우지 말라고 명시했다.
- rows 와 notes 가 모두 비면 render_followup 이 빈 문자열을 돌려주고 패널 자체가 안 그려진다. 실측으로 두 경우를 다 확인했다(빈 날 렌더에 followup 마크업 없음).

접수 건이 브리핑 버튼에서 온 것인지(from_briefing)도 같이 기록해 둔다 — 지금 패널에는 안 쓰지만 나중에 '브리핑에서 나온 것' 만 추릴 때 필요하다.

오늘 실측: 접수 27번(SAD 광치료)이 완성 상태로 잡혀 페이지 링크까지 붙었다.
<!-- SECTION:NOTES:END -->
