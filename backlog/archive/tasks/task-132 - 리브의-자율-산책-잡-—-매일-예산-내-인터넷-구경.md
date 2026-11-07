---
id: TASK-132
title: 리브의 자율 산책 잡 — 매일 예산 내 인터넷 구경
status: Done
assignee: []
created_date: '2026-10-04 03:00'
updated_date: '2026-10-04 03:23'
labels: []
milestone: m-15
dependencies:
  - TASK-131
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
관리자 구상: 리브가 평소 인터넷에서 이것저것 구경하고 찾아본다는 설정을 실제로 돌린다. 아침 브리핑(m-8, ~/jobs/liv-briefing/)처럼 정해진 시각에 돌되, 브리핑과 달리 주제·소스를 정하지 않고 완전 자율로 토큰 예산만 준다. 리브가 노트(task-131)의 취향과 최근 관심을 보고 스스로 갈 곳을 고르고, 본 것과 감상·생각을 노트에 남긴다. 관리자의 관심사 맞춤(브리핑의 역할)이 아니라 리브 자신의 호기심이 기준이라는 점이 브리핑과의 경계다.
고려: 예산 상한(토큰·시간), 툴 잠금은 decision-5 처럼 denylist, 매번 같은 곳만 가지 않도록 최근 방문 이력으로 다양성 유도, 실패해도 브리핑 잡에 영향 없음.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 정해진 주기로 도는 산책 잡이 있고 1회 토큰·시간 예산 상한이 강제된다
- [x] #2 주제·소스를 미리 지정하지 않고 리브가 노트를 근거로 스스로 갈 곳을 고른다
- [x] #3 산책 결과(본 것·출처·감상·생긴 생각)가 노트에 누적되고, 최근 방문 이력으로 같은 곳 반복을 줄인다
- [x] #4 산책 잡 실패가 브리핑 잡과 사이트 발행에 영향을 주지 않는다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
nuc14 ~/jobs/liv-walk/(머신 로컬, 비버전): run.sh(잠금·전용 클론·반영·push 재시도) + walk.py(산책·검증). cron 매일 04:30.
예산: claude -p 구독 OAuth, Opus, --max-budget-usd 3, 30분 timeout+killpg (decision-10). 툴: --tools WebSearch,WebFetch(진짜 allowlist) + allowedTools + decision-5 denylist + strict-mcp + setting-sources '' + env 화이트리스트. 스모크 테스트에서 도구 목록이 WebFetch·WebSearch 뿐이고 Bash 불가 확인.
자율: 프롬프트는 노트 발췌(--for walk)만 주고 주제·소스를 지정하지 않는다. 최소 한 곳은 AI·개발 바깥. 출력 JSON 은 kind·길이·태그·URL 스킴·supersedes 를 검증한 뒤에만 노트에 add.
다양성: excerpt --for walk 가 최근 14일 외부 출처의 도메인(위키백과는 문서 단위)·태그를 '피할 곳'으로 준다 — 산책에서 나온 like/dislike 출처가 빠지던 버그를 고쳤다.
첫 실측(2026-10-04): 55초·환산 $0.32·8턴, 클라이버 법칙·옹기 김치·Stripe 멱등성 5건 → dba2926 로 반영. talk 후보도 나왔다(task-133 용).
격리: 잠금·클론·state·cron 이 브리핑과 분리. WALK_TIMEOUT=1 로 일부러 실패시켜 로그만 남고(rc=1) 커밋·발행 없음을 확인.
<!-- SECTION:NOTES:END -->
