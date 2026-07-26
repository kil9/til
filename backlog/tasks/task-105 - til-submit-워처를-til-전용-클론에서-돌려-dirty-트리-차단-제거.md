---
id: TASK-105
title: til-submit 워처를 til 전용 클론에서 돌려 dirty 트리 차단 제거
status: To Do
assignee: []
created_date: '2026-07-26 14:50'
labels: []
dependencies: []
priority: high
ordinal: 3000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
til-inbox #30(LangGraph 껍데기 값) 접수가 처리되지 않고 failed 로 남았다. 원인은 watcher/run.sh 가 $HOME/work/kil9/til, 즉 사람·에이전트가 쓰는 주 작업 트리에서 직접 /publish-til 을 돌리는 구조라, 09:16 그 시각 다른 세션의 커밋 안 된 변경 때문에 'git pull --rebase' 가 실패하고 dirty-tree 가드에 걸려 중단됐다는 것. 로그: 'error: 리베이스로 풀하기 할 수 없습니다: 스테이징하지 않은 변경 사항이 있습니다.' 바로 다음 접수 #31 은 트리가 깨끗해져 정상 처리됐으므로 재현은 타이밍 의존이다.

접근: liv-briefing 잡(~/jobs/liv-briefing/run.sh:81-95)의 선례대로 전용 클론을 쓴다 — 없으면 clone, 있으면 fetch + reset --hard origin/main 으로 강제 정렬해 주 작업 트리와 완전히 분리한다. 그러면 dirty 가드 자체가 불필요해지고 접수가 로컬 작업 상황에 좌우되지 않는다. push 경합(docs-ai-summary·liv-briefing 이 같은 repo 에 push)은 브리핑 잡의 재시도 루프를 참고한다. 원본은 kil9/til-inbox watcher/run.sh 이며 nuc14 ~/jobs/til-submit/run.sh 는 그 심볼릭 링크라, 수정·커밋은 til-inbox repo 에서 한다.

실패 알림 개선도 같은 태스크에 포함: 현재 실패 notify 는 '❌ til-submit #N 처리 실패 (exit rc)' 뿐이라 Slack 에서 보고도 조치를 못 했다. 이슈 URL 과 '라벨을 pending 으로 되돌리면 재시도' 안내를 메시지에 넣는다(이슈 코멘트에는 이미 있는 문구).

마무리로 #30 라벨을 pending 으로 되돌려 실제 발행까지 확인한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 watcher/run.sh 가 til 주 작업 트리($HOME/work/kil9/til)를 건드리지 않고 전용 클론에서 /publish-til 을 실행한다
- [ ] #2 주 작업 트리가 dirty 한 상태에서도 접수가 정상 처리된다(수동 재현 확인)
- [ ] #3 push 가 non-fast-forward 로 밀릴 때 최신을 받아 재시도한다
- [ ] #4 실패 Slack 알림에 이슈 URL 과 pending 되돌리기 재시도 안내가 포함된다
- [ ] #5 til-inbox #30 을 pending 으로 되돌려 재처리하고, TIL 페이지가 실제로 발행돼 이슈가 done/closed 된다
<!-- AC:END -->
