---
id: decision-5
title: 리브 Slack 봇 claude -p 툴 잠금은 allowlist 아닌 denylist
date: '2026-07-17 21:27'
status: accepted
---
## Context

리브 Slack 봇(TASK-35/36)은 채널의 **임의 사용자** 텍스트를 `claude -p` 프롬프트로 넘긴다. 봇이 도는 nuc14 에는 사용자 OAuth 자격증명(`~/.claude/.credentials.json`)·Slack 토큰(`~/.liv/.env`)이 있어, 프롬프트 인젝션으로 Bash(RCE)·파일 읽기(토큰 유출)·서브에이전트 escape 가 가능하면 치명적이다. 헤드리스 `claude -p` 의 실제 권한 semantics 를 실측해 안전한 호출을 확정했다(2026-07-18, claude 2.1.212, Sonnet 5).

실측 결과:

- **헤드리스 `-p` 기본 permission-mode 는 모든 툴을 프롬프트 없이 실행한다.** `hostname`·`date` 를 Bash 로 시켜보면 그대로 실행돼 출력을 돌려준다(글로벌 `permissions.allow` 가 비어 있어도 그렇다). 즉 `-p` 는 기본적으로 무방비다.
- **`--allowedTools` 는 additive(비제한적)다.** `--allowedTools WebSearch` 만 줘도 Bash 는 여전히 실행된다. allowlist 로는 잠글 수 없다.
- **`--disallowedTools <tools...>` 만이 툴을 세션에서 실제로 제거한다.** 제거하면 모델이 "그 도구가 없다"고 답하고 우회로가 없다. 우회 3종(직접 Bash / Agent 서브에이전트 escape / Read 로 `~/.liv/.env` 유출)을 모두 시도해 전부 차단 확인.
- **함정: `--allowedTools`/`--disallowedTools` 는 variadic 이라 바로 뒤 프롬프트 인자를 삼킨다.** 프롬프트는 반드시 **stdin** 으로 넘긴다(안 그러면 "Input must be provided…" 에러).

## Decision

리브 대화 데몬의 `claude -p` 호출은 **denylist 로 위험 툴을 전부 제거**하고, 프롬프트는 stdin 으로 넘긴다. 남기는 툴은 아카이브 조회용 `WebFetch`·`WebSearch` 뿐(기본 제공이라 별도 allow 불필요).

denylist(제거 대상): `Bash Edit Write NotebookEdit Read Glob Grep Agent Task Skill Workflow ToolSearch ScheduleWakeup TodoWrite` (실행·파일변경·파일읽기·서브에이전트 스폰·MCP 로딩 계열 전부).

추가 방어:
- 종량제 차단: subprocess env 에서 `ANTHROPIC_API_KEY` unset(`env -u`) + systemd `UnsetEnvironment=ANTHROPIC_API_KEY`. 있으면 구독 OAuth 를 덮어 종량제로 넘어간다.
- cwd 는 민감 파일 없는 전용 빈 디렉터리(`~/.liv/workdir`, 700).
- 프롬프트 인젝션 완화: 사용자 입력을 명확한 구분자로 감싸 시스템 지시와 섞이지 않게 한다.
- `--dangerously-skip-permissions` 는 절대 쓰지 않는다(til-submit 무인 배치와 달리 이건 임의 입력 대화 봇이다).

## Consequences

- allowlist 방식으로 오해해 `--allowedTools "WebFetch WebSearch"` 만 주면 **Bash 가 열린 채로 배포되는 치명적 오배포**가 된다. 반드시 denylist 다.
- denylist 는 열거식이라 향후 claude 버전이 새 실행/변경 툴을 추가하면 목록에 없을 위험이 있다. 버전 업 시 `claude --help` 의 툴 목록을 재점검한다. (잔여 inert 툴 TaskCreate·SendMessage·ReportFindings 는 헤드리스 단일 세션에서 외부 효과가 없어 남겨도 무해.)
- 리브가 아카이브 질문에 실제 사이트를 조회해 답할 수 있다(WebFetch/WebSearch 유지). persona 의 "확인 후 답, 추측 금지" 규약과 합치.
