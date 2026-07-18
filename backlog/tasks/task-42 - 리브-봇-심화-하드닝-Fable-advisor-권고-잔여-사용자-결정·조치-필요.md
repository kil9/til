---
id: TASK-42
title: '리브 봇 심화 하드닝 (Fable advisor 권고 잔여, 사용자 결정·조치 필요)'
status: Blocked
assignee: []
created_date: '2026-07-17 22:29'
updated_date: '2026-07-18 11:33'
labels: []
dependencies: []
priority: medium
ordinal: 42000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
loop-task 세션(2026-07-18)에서 Fable advisor(anya) 점검으로 나온 권고 중, 사용자 결정·조치가 필요하거나 라이브 서비스에 리스크가 있어 자율 반영하지 않은 잔여 항목. 치명 상속 벡터(MCP·CLAUDE.md·env)는 이미 반영됨(decision-5). 여기는 defense-in-depth·운영 견고성.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 전용 리눅스 사용자 분리 검토(자격증명 격리+systemd ProtectHome; --setting-sources 로 메모리/settings 누출은 이미 차단돼 긴급도는 낮아짐)
- [ ] #2 til-inbox 전용 fine-grained PAT 로 디스패치(현재 gh 는 kil9 전체 권한; til-inbox issues RW 단일 repo PAT 로 좁혀 EnvironmentFile 600 주입)
- [ ] #3 Tier-2 디스패치에 owner 확정 단계 추가 검토(마커 감지 → '접수할까요?' → owner 확정 답글/리액션 → 게시; 오추출·오발동 차단. 현재는 owner 즉시 디스패치)
- [ ] #4 구독 쿼터 rate limit(전역+사용자별; 쿼터는 사용자 본인 사용과 공유)
- [ ] #5 OAuth 만료 감지 알림(연속 실패 N회 → owner DM; 만료 시 전 호출이 조용히 실패)
- [ ] #6 systemd 샌드박싱(NoNewPrivileges·PrivateTmp·MemoryMax·ProtectSystem=strict+ReadWritePaths[~/.claude,workdir]; 라이브 서비스라 claude 토큰갱신 쓰기 안 깨지게 테스트 후 적용)
- [ ] #7 claude CLI 버전 핀 또는 업데이트 시 툴 목록 diff 점검(denylist 는 신규 툴에 구멍 — 버전관리가 보안 통제)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
사용자 지시로 보류(2026-07-18). 착수 시점은 사용자가 다시 결정. hermes 커토버(TASK-44\~53) 이후 전제가 달라진 항목(#7 CLI 버전 핀 등)이 있어 재개 시 AC 재평가 필요.
<!-- SECTION:NOTES:END -->
