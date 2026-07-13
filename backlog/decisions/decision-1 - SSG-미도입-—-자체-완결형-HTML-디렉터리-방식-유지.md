---
id: decision-1
title: SSG 미도입 — 자체 완결형 HTML 디렉터리 방식 유지
date: '2026-07-13 14:08'
status: accepted
---
## Context

블로그/정적 사이트 프레임워크(SSG) 도입을 검토(구 PLAN T-16, 2026-07 결정). 페이지가 늘면서 공통 룩·메타 삽입을 빌드 타임에 처리할지가 쟁점이었다.

## Decision

**현행 "artifact 당 자체 완결형 HTML 디렉터리" 방식 유지(SSG 미도입).**

근거:
1. claude.ai artifact 는 이미 완성된 standalone HTML 이라, SSG(본문+템플릿→HTML 생성 모델)에 넣으려면 프론트매터+콘텐츠로 역분해가 필요해 워크플로가 오히려 한 단계 늘어난다.
2. 정렬·아카이브·필터 칩 등 동적 기능은 클라이언트 JS 로 이미 구현돼(구 T-10/T-11/T-14) 빌드 타임 렌더링 이점이 상쇄된다.
3. Jekyll 외 SSG(Astro/Hugo/Eleventy)는 GitHub Actions 빌드 필수(새 CI 실패 지점)이고, 어떤 SSG 든 루트 index.html 이 빌드 산출물이 되어 nuc14 AI요약 직접 주입(구 T-12)과 소스/산출물 이중화가 충돌한다.
4. 남은 "전 페이지 공통 삽입" 수요(OG 메타·분석 beacon)는 SSG 없이 런북 템플릿 강화로 충분하다.

## Consequences

- 공통 룩 변경은 각 페이지 수동 유지보수. 소급 공통 삽입용 경량 후처리 스크립트는 별도 draft 로 보류.
- **재평가 트리거**: 페이지가 수십 건 이상으로 늘고 공통 룩 변경이 수동 유지보수 병목이 되면 Jekyll(유일한 무빌드·네이티브 서빙 SSG)에 한해 재검토.
