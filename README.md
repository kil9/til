# kil9 / til

`/publish-pages` 로 요청한 정적 페이지를 GitHub Pages 로 퍼블리시하는 저장소.

- 라이브 사이트: <https://kil9.github.io/til/>
- 각 페이지는 자체 완결형(self-contained) HTML 이며, 한 페이지당 디렉터리 하나를 차지한다.
- 루트 `index.html` 은 퍼블리시된 페이지 전체를 나열하는 갤러리 랜딩 페이지다.
- 이 아카이브의 화자는 전속 AI 지식 큐레이터 캐릭터 **리브 투데이**다. 신규 페이지부터 적용되며, 설정·문체 규칙은 `backlog/docs/doc-3 - 리브-투데이-캐릭터-설정.md` 와 [AGENTS.md](AGENTS.md) §2-2 에 있다. 소개는 [/p/liv-today/](https://kil9.github.io/til/p/liv-today/), 설정화 시트는 [/p/liv-today/sheet/](https://kil9.github.io/til/p/liv-today/sheet/)(갤러리 미노출, 소개 페이지 링크로 진입).

## URL 구조

```
https://kil9.github.io/til/                     루트 갤러리
https://kil9.github.io/til/<디렉터리>/           개별 페이지 (예: til-archive)
```

GitHub Pages 는 `main` 브랜치 루트를 그대로 서빙한다(별도 빌드 없음). `main` 에 push 하면 몇십 초 뒤 반영된다.

## 페이지 추가하기

1. 퍼블리시할 콘텐츠(자체 완결형 HTML)를 준비한다.
2. `<slug>/index.html` 로 새 디렉터리에 저장한다.
3. 루트 `index.html` 의 갤러리 목록과 이 README 의 "퍼블리시된 페이지" 목록을 갱신한다.
4. `main` 에 commit / push 한다.

에이전트가 수행할 때의 상세 절차와 규칙은 [AGENTS.md](AGENTS.md) 의 퍼블리시 런북을 따른다.

## 글 쓰기

이미 완성된 콘텐츠를 옮기는 것이 아니라 글을 처음부터 쓸 때는 `topics/`(글감) → `drafts/`(초안·대화 로그) → 퍼블리시 순으로 진행한다. 두 디렉터리는 게시 전 원고가 public 저장소로 새지 않도록 `.gitignore` 로 비커밋이며, 템플릿만 추적한다. 워크플로·스타일 규칙은 [AGENTS.md](AGENTS.md) 의 "글쓰기 워크플로" 섹션에 있다.

## 주요 기능

- 정적 HTML 페이지를 디렉터리 단위로 호스팅
- 퍼블리시된 페이지를 한눈에 보는 갤러리 랜딩 페이지
- 라이트/다크 테마 자동 대응(각 페이지가 `prefers-color-scheme` 지원)
- 외부 의존성 없는 단일 파일 페이지(오프라인에서도 열림)

## 퍼블리시된 페이지

| 날짜 | 페이지 | 경로 |
| --- | --- | --- |
| 2026-07-20 | 키 밀림 사건 종결 보고 | [/2026/key-repeat-case-closed/](https://kil9.github.io/til/2026/key-repeat-case-closed/) |
| 2026-07-19 | 키보드를 살렸더니 마이크가 죽었다 | [/2026/keyboard-fixed-mic-dead/](https://kil9.github.io/til/2026/keyboard-fixed-mic-dead/) |
| 2026-07-19 | 같은 80%인데 색이 다른 이유 | [/2026/pace-not-percent/](https://kil9.github.io/til/2026/pace-not-percent/) |
| 2026-07-19 | 키보드 글자 폭발 조사기 | [/2026/key-repeat-explosion/](https://kil9.github.io/til/2026/key-repeat-explosion/) |
| 2026-07-18 | 노동 이후의 자본주의와 기본소득 | [/2026/post-labor-capitalism/](https://kil9.github.io/til/2026/post-labor-capitalism/) |
| 2026-07-18 | LingBot-Map — 폰으로 찍고, 4080 으로 돌린다 | [/2026/lingbot-map-local/](https://kil9.github.io/til/2026/lingbot-map-local/) |
| 2026-07-17 | QMK 레이어는 왜 아래를 못 보나 | [/2026/kb16-qmk-layer-stack/](https://kil9.github.io/til/2026/kb16-qmk-layer-stack/) |
| 2026-07-17 | 범인은 전원도, 허브도 아니었다 — 매크로패드 부트루프 3차 수사 | [/2026/kb16-bootloop-usb-power/](https://kil9.github.io/til/2026/kb16-bootloop-usb-power/) |
| 2026-07-17 | 프롬프트를 입으로 친다면 얼마일까 | [/2026/voice-prompting-cost/](https://kil9.github.io/til/2026/voice-prompting-cost/) |
| 2026-07-17 | Moshi, 한국어 화자에게 쓸만한가 | [/2026/moshi-voice-ai/](https://kil9.github.io/til/2026/moshi-voice-ai/) |
| 2026-07-17 | 리브가 읽은 kil9conf | [/2026/kil9conf-14-years/](https://kil9.github.io/til/2026/kil9conf-14-years/) |
| 2026-07-16 | 기획과 실행을 분리하는 법 | [/2026/2026-07-agent-workflow/](https://kil9.github.io/til/2026/2026-07-agent-workflow/) |
| 2026-07-16 | herdr 에서 orca 로 옮길까 | [/2026/herdr-vs-orca/](https://kil9.github.io/til/2026/herdr-vs-orca/) |
| 2026-07-15 | 안녕하세요, 리브입니다 | [/p/liv-today/](https://kil9.github.io/til/p/liv-today/) |
| 2026-07-15 | Claude 스킬 만들기: Anthropic 공식 가이드 정리 | [/2026/claude-skills-guide/](https://kil9.github.io/til/2026/claude-skills-guide/) |
| 2026-07-15 | 글자가 겹치면 폰트를 고치면 된다: NotoSansKR NFC Fixed 삽질기 | [/2026/notosanskr-nfc-fixed/](https://kil9.github.io/til/2026/notosanskr-nfc-fixed/) |
| 2026-07-15 | 내 셸에선 되는데: systemd PATH 와 fail-closed 가드가 겹친 자리 | [/2026/systemd-path-fail-closed/](https://kil9.github.io/til/2026/systemd-path-fail-closed/) |
| 2026-07-14 | 닌텐도의 Actions Runner 운용 | [/2026/nintendo-actions-runner/](https://kil9.github.io/til/2026/nintendo-actions-runner/) |
| 2026-07-14 | 에이전트를 지켜보는 비용 — herdr pane 오케스트레이션 재평가 | [/2026/herdr-pane-tradeoffs/](https://kil9.github.io/til/2026/herdr-pane-tradeoffs/) |
| 2026-07-13 | Backlog.md 도입 검토 | [/2026/backlog-md-vs-plan-md/](https://kil9.github.io/til/2026/backlog-md-vs-plan-md/) |
| 2026-07-13 | Ghostty vs Windows Terminal | [/2026/ghostty-vs-windows-terminal/](https://kil9.github.io/til/2026/ghostty-vs-windows-terminal/) |
| 2026-07-13 | 미첼 하시모토 인터뷰 해설 — 터미널·Zig·오픈소스 | [/2026/hashimoto-oss-philosophy/](https://kil9.github.io/til/2026/hashimoto-oss-philosophy/) |
| 2026-07-12 | 시트리니 리포트 — 「2028 글로벌 지능 위기」 해설 | [/2026/citrini-2028-gic/](https://kil9.github.io/til/2026/citrini-2028-gic/) |
| 2026-07-12 | Claude Fable 5 vs GPT-5.6 — computer use 벤치마크·가격 비교 | [/2026/claude-vs-gpt56-computer-use/](https://kil9.github.io/til/2026/claude-vs-gpt56-computer-use/) |
| 2026-07-12 | 알파벳 축소·애플 확대 — AI capex 헷지 가설 재검증 | [/2026/ai-capex-hedge/](https://kil9.github.io/til/2026/ai-capex-hedge/) |
| 2026-07-11 | 두 세션 플랜 파이프라인 — Claude Code 를 생산자·소비자로 나눠 쓰기 | [/2026/2026-07-plan-pipeline/](https://kil9.github.io/til/2026/2026-07-plan-pipeline/) |
| 2026-07-11 | TIL 아카이브 — Today I Learned | [/p/til-archive/](https://kil9.github.io/til/p/til-archive/) |
