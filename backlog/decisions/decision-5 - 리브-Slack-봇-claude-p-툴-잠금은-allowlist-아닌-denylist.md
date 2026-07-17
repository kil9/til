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

리브 대화 데몬의 `claude -p` 호출은 **allowlist + denylist 를 함께** 주고, 프롬프트는 stdin 으로 넘긴다. 둘의 역할이 다르다:

- `--allowedTools WebFetch WebSearch`: 아카이브 조회 툴을 **pre-approve**. 이게 없으면 헤드리스에서 WebFetch 가 "사용자 승인이 필요"로 **막힌다**(default permission-mode 라도 WebFetch 는 도메인 승인이 필요해 자동 실행되지 않는다 — Bash 와 다르다). additive 라 잠금 효과는 없고 승인 효과만 있다.
- `--disallowedTools <denylist>`: 위험 툴을 세션에서 **제거**. deny 가 allow 를 이기므로, allowlist 를 함께 줘도 denylist 의 툴은 여전히 제거된다(최종 조합에서 Bash 강제 시도 → "Bash 도구가 없다" 재확인).

denylist(제거 대상): `Bash Edit Write NotebookEdit Read Glob Grep Agent Task Skill Workflow ToolSearch ScheduleWakeup TodoWrite` (실행·파일변경·파일읽기·서브에이전트 스폰·MCP 로딩 계열 전부).

추가 방어:
- 종량제 차단: subprocess env 에서 `ANTHROPIC_API_KEY` unset(`env -u`) + systemd `UnsetEnvironment=ANTHROPIC_API_KEY`. 있으면 구독 OAuth 를 덮어 종량제로 넘어간다.
- cwd 는 민감 파일 없는 전용 빈 디렉터리(`~/.liv/workdir`, 700).
- 프롬프트 인젝션 완화: 사용자 입력을 명확한 구분자로 감싸 시스템 지시와 섞이지 않게 한다. 대화 감지 마커(PUBLISH_REQUEST)는 **응답 마지막 줄만** 파싱하고, 프롬프트에 넣는 외부 텍스트의 마커 토큰은 escape 한다.
- `--dangerously-skip-permissions` 는 절대 쓰지 않는다(til-submit 무인 배치와 달리 이건 임의 입력 대화 봇이다).

### 추가 하드닝 (Fable advisor 점검 + 실측, 2026-07-18 반영)

denylist 만으로 안 막히는 상속 벡터 3개를 실측으로 확인해 플래그로 닫았다:

- **MCP 상속**: `claude -p` 는 사용자 `~/.claude.json` 의 MCP 서버(실측: `ccs-websearch`·`ccs-image-analysis`)를 그대로 로드한다. MCP 툴은 이름(`mcp__…`)이 달라 denylist 로 안 잡힌다 → **`--strict-mcp-config --mcp-config '{"mcpServers":{}}'`** 로 전면 차단.
- **유저 메모리·settings 상속**: `claude -p` 는 사용자 글로벌 `~/.claude/CLAUDE.md`(실측: liv 가 "herdr" 등 내부 규칙을 그대로 노출)와 `settings.json` 의 `permissions.allow` 를 상속한다(HOME·CLAUDE_CONFIG_DIR 오버라이드로는 안 막힘 — 메모리는 getpwuid 홈에서 읽는다). → **`--setting-sources ''`**(user/project/local 전부 미로드)로 메모리 유출 + settings.allow 상속을 함께 차단. 인증·모델은 그대로 적용돼 구독 OAuth 는 유지된다.
- **종량제·엔드포인트 우회 env**: `ANTHROPIC_API_KEY` 외에 `ANTHROPIC_AUTH_TOKEN`·`ANTHROPIC_BASE_URL`·`CLAUDE_CODE_USE_BEDROCK/VERTEX` 도 같은 계열이라, 블록리스트 대신 **env 화이트리스트**({HOME,PATH,LANG,LC_*,USER,LOGNAME})로 새로 조립한다.
- **`--permission-mode dontAsk` 는 fail-open**(실측: allowlist 밖 Bash 가 그대로 실행됨). 그래서 dontAsk 로 화이트리스트화하는 길은 없고 denylist 가 유일 경계로 남는다. 신규 툴 구멍 위험은 유효하므로 CLI 버전 업 시 툴 목록 재점검이 곧 보안 통제다.
- 프로세스 정리: `claude` 가 node 자식을 낳아 timeout 시 단일 kill 로는 잔존이 남으므로 `start_new_session=True` + timeout 시 `killpg`.

## Consequences

- allowlist 방식으로 오해해 `--allowedTools "WebFetch WebSearch"` 만 주면 **Bash 가 열린 채로 배포되는 치명적 오배포**가 된다. 반드시 denylist 다.
- denylist 는 열거식이라 향후 claude 버전이 새 실행/변경 툴을 추가하면 목록에 없을 위험이 있다. 버전 업 시 `claude --help` 의 툴 목록을 재점검한다. (잔여 inert 툴 TaskCreate·SendMessage·ReportFindings 는 헤드리스 단일 세션에서 외부 효과가 없어 남겨도 무해.)
- 리브가 아카이브 질문에 실제 사이트를 조회해 답할 수 있다(WebFetch/WebSearch 유지). persona 의 "확인 후 답, 추측 금지" 규약과 합치.
