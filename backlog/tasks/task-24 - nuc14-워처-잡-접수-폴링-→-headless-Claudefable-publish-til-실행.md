---
id: TASK-24
title: 'nuc14 워처 잡: 접수 폴링 → headless Claude(fable) /publish-til 실행'
status: To Do
assignee: []
created_date: '2026-07-17 07:27'
labels:
  - solo
milestone: m-1
dependencies:
  - TASK-22
priority: medium
ordinal: 24000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
nuc14 머신 로컬 잡(~/jobs/til-submit/)으로 til-inbox 를 폴링해 접수를 처리한다. gh 로 open+pending 이슈를 1-2분 간격 폴링, 발견 시 processing 라벨로 claim 하고 headless Claude Code(모델 fable, --dangerously-skip-permissions, cwd=~/work/kil9/til)로 /publish-til 을 실행한다. 성공 시 결과 URL 을 이슈 코멘트로 남기고 done 라벨+클로즈, 실패 시 failed 라벨+에러 요약 코멘트. lockfile 로 동시 실행 방지. 스크립트 소스는 til-inbox repo 에 버저닝하고 cron(또는 systemd user timer)으로 등록한다. 잡 운용법은 머신 로컬 규칙에 따라 auto-memory 에 기록한다.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 워처가 pending 이슈를 감지해 claim(processing)하고 headless claude 로 /publish-til 을 실행한다
- [ ] #2 성공 시 결과 URL 코멘트+done+클로즈, 실패 시 failed 라벨+에러 코멘트가 남는다
- [ ] #3 lockfile 로 중복 실행이 방지되고 cron/systemd 로 자동 기동된다
- [ ] #4 스크립트가 til-inbox repo 에 버저닝된다
<!-- AC:END -->
