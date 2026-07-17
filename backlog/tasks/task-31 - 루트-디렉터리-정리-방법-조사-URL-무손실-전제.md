---
id: TASK-31
title: 루트 디렉터리 정리 방법 조사 (URL 무손실 전제)
status: Done
assignee: []
created_date: '2026-07-17 20:00'
updated_date: '2026-07-17 20:04'
labels: []
dependencies: []
priority: low
ordinal: 31000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
루트에 페이지 디렉터리가 24개 쌓여 시각적으로 번잡하다. 핵심 제약은 '디렉터리 이름 = URL 경로'라 슬러그를 옮기면 기존 링크(kil9.github.io/til/<slug>/)가 깨진다는 점. 이 태스크는 URL을 깨지 않으면서 루트를 정리할 수 있는 방법이 실제로 있는지 실현 가능성과 트레이드오프만 조사한다(구현은 별도 결정). 검토 대상: (1) 페이지를 하위 디렉터리(p/ 등)로 이전 + 옛 경로에 meta-refresh 리다이렉트 스텁 남기기 — 스텁이 오히려 dir을 늘리는 역설 포함; (2) GitHub Pages 설정/커스텀 라우팅으로 우회 가능 여부(정적 서빙 한계 확인); (3) 페이지가 아닌 잡동사니(submit-96a2d1c7e19e8a09 제출 테스트 아티팩트, til-archive 구 아카이브, backlog 전환 완료된 PLAN.md 등)만 정리해도 체감이 개선되는지. 각 방안의 URL 유지 비용 대비 정리 이득을 정리해 보고한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 URL 무손실 전제로 루트를 정리할 수 있는 방법 후보(하위 dir 이전+리다이렉트, Pages 설정 우회, 비페이지 잡동사니 정리 등)를 각각의 실현 가능성과 함께 정리한다
- [x] #2 각 방안의 트레이드오프(URL 유지 비용, 스텁으로 인한 dir 증가 역설, 유지보수 부담)를 비교해 보고한다
- [x] #3 submit-96a2d1c7e19e8a09 / til-archive / PLAN.md 등 현재 루트의 비페이지·잔재 항목을 식별하고 각각 정리 가능 여부를 판단한다
- [x] #4 구현은 하지 않고 조사 결과와 권장안만 사용자에게 보고한다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
조사 전용(구현 없음). 핵심 결론: 루트 24개 페이지 dir 중 실제 잔재는 사실상 없음. 태스크 설명의 잔재 가정이 대부분 틀림 — submit-96a2d1c7e19e8a09 는 TASK-23/28 의 라이브 비밀 제출 페이지(noindex·의도적 미링크, 파이프라인이 의존), til-archive 는 갤러리·README 에 링크된 실제 페이지, PLAN.md 는 AGENTS.md 가 명시한 의도적 아카이브. herdr-pane-tradeoffs-anime 는 갤러리 미링크지만 URL 직행 가능한 실제 페이지. backlog/ 만 유일한 비페이지 dir(CLI 가 루트 고정 요구). URL 무손실 재구성: (1) p/<slug>/ 이전+meta-refresh 스텁 = 스텁이 곧 dir 이라 개수가 오히려 2배로 늘어 자기모순; (2) Pages(legacy, .nojekyll 없음)는 정적 서빙이라 서버 리라이트 불가, Jekyll permalink 로 소스↔URL 분리는 이론상 가능하나 전 페이지 front-matter 추가+Liquid 가 인라인 base64/중괄호 처리할 위험+repo 의 무빌드 원칙 위배로 비용 과다; (3) 잡동사니 정리는 제거 대상이 없어 이득 0. 권장: 구조 변경 없음(no-op). 근거 — 이 번잡함은 방문자에게 안 보이는 워킹트리/ls 미관 문제일 뿐이고, 방문자는 index.html 갤러리만 봄. 오직 유지자만 보는 미관을 고치려 실제 URL·복잡도를 지불하는 건 손해.
<!-- SECTION:NOTES:END -->
