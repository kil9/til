---
id: TASK-26
title: 제출 파이프라인 E2E 검증 및 운용 기록
status: Blocked
assignee: []
created_date: '2026-07-17 07:27'
updated_date: '2026-07-17 07:42'
labels:
  - solo
milestone: m-1
dependencies:
  - TASK-23
  - TASK-24
  - TASK-25
priority: medium
ordinal: 26000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
실제 제출 1건으로 전 구간을 왕복 검증한다: 관리자 페이지 폼 제출 → til-inbox 이슈 생성 → 워처 감지·claim → headless /publish-til 게시 → 이슈 클로즈 → Slack #TIL 알림 4종. 운용법(잡 위치·재시작·PAT 재발급·트러블슈팅)을 auto-memory 와 til-inbox README 에 기록한다. til 공개 repo 쪽 문서에는 비밀 슬러그를 남기지 않는다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 실제 제출 1건이 페이지→이슈→워처→게시→클로즈→Slack 까지 완주한다
- [x] #2 운용 런북이 auto-memory 와 til-inbox README 에 기록된다
- [x] #3 til 공개 repo 문서에 비밀 슬러그가 노출되지 않는다
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
결정 필요: 실제 제출 1건 완주(AC #1)는 사용자 액션 대기 — fine-grained PAT 발급(til-inbox 한정, Issues RW) 후 제출 페이지에서 등록하고 실제 URL 1건 제출. 자가 실행분은 완료: 운용 런북(til-inbox README + auto-memory til-submit-watcher), til 공개 문서 슬러그 미노출 검증(task-23 노트에서 슬러그 제거, 디렉터리명은 public tree 노출이 설계 전제·방어선은 PAT). 제출이 오면 cron 워처가 자동 처리하므로 완주 확인 후 이 태스크를 Done 으로.
<!-- SECTION:NOTES:END -->
