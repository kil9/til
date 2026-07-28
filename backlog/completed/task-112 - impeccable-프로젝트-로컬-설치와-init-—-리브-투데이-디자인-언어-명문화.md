---
id: TASK-112
title: impeccable 프로젝트 로컬 설치와 init — 리브 투데이 디자인 언어 명문화
status: Done
assignee: []
created_date: '2026-07-28 16:25'
updated_date: '2026-07-28 16:45'
labels: []
milestone: m-12
dependencies: []
priority: medium
ordinal: 6000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
npx impeccable install --scope=project 로 .claude/ 에 스킬·훅을 설치하고 /impeccable init 으로 PRODUCT.md·DESIGN.md 를 만든다. DESIGN.md 는 AGENTS.md §2-2 와 doc-3(리브 투데이 캐릭터 설정)의 문체·디자인 규칙을 흡수해 사이트 디자인 언어를 명문화한다 — 기존 규칙과 모순을 만들지 않는다. main 루트가 GitHub Pages 로 공개 서빙되므로 .impeccable/(리뷰 보고서·라이브 상태)은 반드시 gitignore 에 넣는다. 훅은 .claude/settings.local.json(gitignore)에 등록되므로 머신별 1회 재등록이 필요하다 — 이 사실을 AGENTS.md 에 남긴다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 install --scope=project 와 init 이 완료되고 /impeccable 커맨드가 동작한다
- [x] #2 DESIGN.md 가 AGENTS.md §2-2·doc-3 과 모순 없이 사이트 디자인 언어를 명문화한다
- [x] #3 .impeccable/ 이 gitignore 에 있다
- [x] #4 HTML 편집 시 훅(hook.mjs)이 발동하는 것을 확인했다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
npx impeccable install(project) 로 .claude/skills/impeccable/ + settings.local.json 훅 등록 완료. init 은 PRODUCT.md 만 쓰고 DESIGN.md 는 document 플로 소관이라(reference/init.md L3) 둘로 나눠 수행했다 — PRODUCT.md 는 init 절차, DESIGN.md 는 document scan mode 로 실제 CSS 토큰을 추출해 작성. 인터뷰 라운드는 열지 않고 AGENTS.md·README.md·doc-3 에서 도출했으며 그 사실을 PRODUCT.md 머리말에 명시했다(자율 드레인 중).
DESIGN.md: 라이트/다크 16색 + 타이포 7단(display/title/body/secondary/caption/label/mono) + rounded 3단 + 컴포넌트 12종, 명명 규칙 10개(One Blue / Cool Gray / Two-Mode Parity / Mono-For-Facts / Uppercase-Is-A-Label / Quiet Bold / Two Widths / Flat / Single Line / 8-or-Circle). 사이트 전체에서 box-shadow 는 이관된 초기 페이지 3곳뿐이라 Flat 을 불변조건으로 적었다. detect 가 램프 이탈로 잡은 0.875rem 은 실사용 96회+ 라 caption 단계로 정식 편입했다(규칙에 맞춘 게 아니라 누락을 메운 것).
gitignore: .impeccable/* + !.impeccable/config.json — config.json 만 예외로 둔 이유는 규칙 waive 목록이 머신마다 다르면 발행 게이트가 사람마다 다르게 통과하기 때문. 스킬 본체 .claude/skills/impeccable/(130여 파일)도 벤더링하지 않는다(훅 재등록이 어차피 머신별 1회라 install 한 번이 둘을 같이 가져온다).
훅 검증: 합성 PostToolUse 이벤트를 hook.mjs 에 넣어 p/archive/index.html 의 design-system-radius(10px) 를 잡아내는 것을 확인. DESIGN.md 를 물고 도는 것도 같이 확인됐다.
남은 detect 소견(single-font / flat-type-hierarchy / archive 10px / index.html 0.5rem 장식 글리프)은 TASK-113 triage 소관이라 여기서 건드리지 않았다.
<!-- SECTION:NOTES:END -->
