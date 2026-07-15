---
id: TASK-7
title: 소개 페이지 전면 재작성 후 liv-today 로 재발행
status: To Do
assignee: []
created_date: '2026-07-15 10:13'
labels: []
dependencies:
  - TASK-6
priority: high
ordinal: 7000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
https://kil9.github.io/til/liv-archivist/ 를 전면 재작성해 새 슬러그 liv-today 로 재발행한다. 방향 전환의 핵심은 글의 성격이다. 지금 글은 '제작기'(3인칭 보고서 + 제작 과정 + 설정 테이블)인데, 리브 본인이 스스로를 소개하는 1인칭 글로 바꾼다.

톤·내용 지침:
- 전체를 리브 1인칭 존댓말로 쓴다. 제작 과정 서술이 아니라 자기소개다.
- 핵심 논지: 이 사이트의 보고서는 대부분 Codex 나 Claude 가 작성한다. 그래서 그 사실을 숨기기보다 화자에게 캐릭터를 주어 분명히 분리하는 편이 낫다는 판단으로 이 형태를 제안했다는 취지를 리브의 말로 풀어낸다(문구는 그대로 옮기지 말고 재구성).
- 제작 과정(스타일 3안 비교, 시트 8컷 제작기, 생성 파라미터 등)의 비중을 크게 줄인다.
- 항목별 설정 테이블은 삭제한다. 숨은 설정을 목록으로 노출하는 인상을 주지 않도록, 성격·비주얼 설정은 본문 흐름에 아주 일부만 자연스럽게 녹인다.
- '서고지기'·'서고' 표현을 쓰지 않는다(TASK-6 개정본을 따른다). 풀네임 '리브 투데이'를 소개한다.

슬러그 교체: liv-archivist 디렉터리는 발행 당일이라 외부 유입이 사실상 없으므로 리다이렉트 없이 제거한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 리브 1인칭 존댓말 자기소개로 전면 재작성한다. 제작 과정·설정 테이블 없이, 캐릭터를 분리 장치로 두는 판단의 취지를 리브의 말로 담는다
- [ ] #2 설정화 시트는 대표 2-3컷만 본문 흐름에 맞춰 base64 임베드한다(기존 8컷 전시 제거)
- [ ] #3 liv-today/index.html 로 발행하고 liv-archivist 디렉터리를 제거한다. 루트 갤러리 카드와 README 표를 새 슬러그·제목·설명으로 갱신한다(카드 data-date 는 재발행 시각)
- [ ] #4 https://kil9.github.io/til/liv-today/ 라이브에서 라이트/다크 렌더를 확인하고, repo 내에 liv-archivist 참조가 남지 않았음을 grep 으로 확인한다
<!-- AC:END -->
