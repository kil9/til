# kil9 / til

`/publish-pages` 로 요청한 정적 페이지를 GitHub Pages 로 퍼블리시하는 저장소.

- 라이브 사이트: <https://til.kil9.dev/>
- 각 페이지는 자체 완결형(self-contained) HTML 이며, 한 페이지당 디렉터리 하나를 차지한다.
- 루트 `index.html` 은 퍼블리시된 페이지를 나열하는 갤러리 랜딩 페이지다. 기본 뷰는 최근 글 피드이고, 전체 목록은 사이드바 월별 목차 또는 [/p/archive/](https://til.kil9.dev/p/archive/)(월별 격자 색인, 갤러리 미노출)에서 훑는다.
- 이 아카이브의 화자는 전속 AI 지식 큐레이터 캐릭터 **리브 투데이**다. 신규 페이지부터 적용되며, 설정·문체 규칙은 `backlog/docs/doc-3 - 리브-투데이-캐릭터-설정.md` 와 [AGENTS.md](AGENTS.md) §2-2 에 있다. 소개는 [/p/liv-today/](https://til.kil9.dev/p/liv-today/), 설정화 시트는 [/p/liv-today/sheet/](https://til.kil9.dev/p/liv-today/sheet/)(갤러리 미노출, 소개 페이지 링크로 진입).

## URL 구조

```
https://til.kil9.dev/                     루트 갤러리
https://til.kil9.dev/<연도>/<slug>/        날짜 아티클 (예: /2026/human-in-the-loop/)
https://til.kil9.dev/p/<slug>/            비-날짜 지원 페이지 (예: /p/archive/)
https://til.kil9.dev/feed.xml             Atom 피드
https://til.kil9.dev/sitemap.xml          sitemap
```

GitHub Pages 는 `main` 브랜치 루트를 그대로 서빙한다(별도 빌드 없음). `main` 에 push 하면 몇십 초 뒤 반영된다.

## 페이지 추가하기

1. 퍼블리시할 콘텐츠(자체 완결형 HTML)를 준비한다.
2. `<slug>/index.html` 로 새 디렉터리에 저장한다.
3. 루트 `index.html` 의 갤러리 목록과 이 README 의 "퍼블리시된 페이지" 목록을 갱신한다.
4. 생성물을 다시 만든다. 루트 카드가 진실원본이므로 손으로 고치지 않는다.

   ```bash
   python3 backlog/assets/archive-thumbs.py   # 격자 썸네일 + og/<slug>.jpg
   python3 backlog/assets/relink-pages.py     # canonical·og:image, 이전/다음·주제 역링크, 절 앵커·목차
   python3 backlog/assets/site-feed.py        # feed.xml, sitemap.xml, robots.txt
   python3 backlog/assets/search-index.py     # search-index.json (본문 검색 색인)
   ```

5. `python3 backlog/assets/site-check.py` 로 점검한다. canonical·내부 링크·404 리다이렉트 맵·용량을 보고, 위반이 있으면 비영 종료코드로 끝난다. 외부 링크 생존은 `--external` 로만 돈다.
6. 바뀐 파일을 전부 담아 `main` 에 commit / push 한다. 새 글을 올리면 직전 글의 "다음" 링크도 함께 바뀐다.

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
| 2026-09-02 | 드워프 포트리스의 절차적 마법, 주문 하나가 만들어지는 축 | [/2026/dwarf-fortress-procedural-magic-design/](https://til.kil9.dev/2026/dwarf-fortress-procedural-magic-design/) |
| 2026-09-02 | Claude Fable 5.1, 무엇이 깨지고 무엇이 얹혔나 | [/2026/claude-fable-5-1-overview/](https://til.kil9.dev/2026/claude-fable-5-1-overview/) |
| 2026-09-01 | 다익스트라의 정렬 장벽을 깨는 법 | [/2026/breaking-dijkstra-sorting-barrier/](https://til.kil9.dev/2026/breaking-dijkstra-sorting-barrier/) |
| 2026-08-31 | 도구를 고르면 조직도 따라온다 | [/2026/tools-are-organizational-decisions/](https://til.kil9.dev/2026/tools-are-organizational-decisions/) |
| 2026-08-28 | PaperMono: e-ink 대시보드 계보의 개발자 단말 | [/2026/papermono-eink-dashboard/](https://til.kil9.dev/2026/papermono-eink-dashboard/) |
| 2026-08-26 | Codex를 더 많이 쓴 일주일: 도구보다 흐름이 갈랐다 | [/2026/week-with-codex/](https://til.kil9.dev/2026/week-with-codex/) |
| 2026-08-25 | 같은 로컬 모델, 엔진이 바뀌면 어디서 갈리나 | [/2026/local-llm-engine-divergence/](https://til.kil9.dev/2026/local-llm-engine-divergence/) |
| 2026-08-25 | Fable 5 채택 11%, 무엇이 정체했나 | [/2026/fable-5-ramp-spend-signal/](https://til.kil9.dev/2026/fable-5-ramp-spend-signal/) |
| 2026-08-25 | 네이티브 웹 41개, Baseline으로 지금 쓸 것 가르기 | [/2026/native-web-baseline/](https://til.kil9.dev/2026/native-web-baseline/) |
| 2026-08-25 | 프로덕트 엔지니어 채용 붐: 실제로 늘었나 | [/2026/product-engineer-hiring-data/](https://til.kil9.dev/2026/product-engineer-hiring-data/) |
| 2026-08-23 | 백로그 에이전트 파이프라인 | [/2026/backlog-agent-pipeline/](https://til.kil9.dev/2026/backlog-agent-pipeline/) |
| 2026-08-22 | Moli: 픽셀을 필요할 때만 만드는 에이전트 브라우저 | [/2026/moli-agent-browser/](https://til.kil9.dev/2026/moli-agent-browser/) |
| 2026-08-22 | Qwen3-TTS 첫 응답 50ms, 어디서 시간을 벌었나 | [/2026/qwen3-tts-50ms-latency/](https://til.kil9.dev/2026/qwen3-tts-50ms-latency/) |
| 2026-08-19 | 모티프 3 탈락이 보여준 AI 벤치마크의 사용법 | [/2026/motif-3-benchmark-gap/](https://til.kil9.dev/2026/motif-3-benchmark-gap/) |
| 2026-08-19 | herdr 0.8.1: Windows 정식 지원과 자동화 경계 다듬기 | [/2026/herdr-0-8-1/](https://til.kil9.dev/2026/herdr-0-8-1/) |
| 2026-08-17 | GSM-Symbolic: 애플이 증명한 것과 X가 부풀린 것 | [/2026/gsm-symbolic-llm-reasoning/](https://til.kil9.dev/2026/gsm-symbolic-llm-reasoning/) |
| 2026-08-17 | X For You 알고리듬: 공개 가중치는 타임라인을 얼마나 설명하나 | [/2026/x-for-you-algorithm/](https://til.kil9.dev/2026/x-for-you-algorithm/) |
| 2026-08-17 | LLM 텍스트 워터마크: 짧은 답과 코드에는 얼마나 남나 | [/2026/llm-text-watermark-survival/](https://til.kil9.dev/2026/llm-text-watermark-survival/) |
| 2026-08-17 | AI 토큰 재판매 시장: 90% 할인의 실제 대가 | [/2026/ai-token-resale-market/](https://til.kil9.dev/2026/ai-token-resale-market/) |
| 2026-08-17 | Claude 4.8→5 시스템 프롬프트 diff: 3,000단어가 늘지 않았다 | [/2026/claude-system-prompt-5-diff/](https://til.kil9.dev/2026/claude-system-prompt-5-diff/) |
| 2026-08-15 | 손코딩은 대중 취미가 되기 어렵다 | [/2026/hand-coding-after-ai/](https://til.kil9.dev/2026/hand-coding-after-ai/) |
| 2026-08-13 | 당근이 Lynx를 잘 고른 이유: 프레임워크보다 레일 | [/2026/karrot-lynx-beyond-webview/](https://til.kil9.dev/2026/karrot-lynx-beyond-webview/) |
| 2026-08-13 | 바다 위 데이터센터는 발전소가 될 수 있나: 파력발전부터 병목까지 | [/2026/offshore-data-centers-wave-power/](https://til.kil9.dev/2026/offshore-data-centers-wave-power/) |
| 2026-08-12 | Go는 AI 코딩의 이상형인가: 생성보다 검증 | [/2026/go-ai-assisted-engineering/](https://til.kil9.dev/2026/go-ai-assisted-engineering/) |
| 2026-08-11 | 올빼미형이 더 똑똑하다는 논문, 숫자는 7분이었다 | [/2026/night-owls-intelligence-evidence/](https://til.kil9.dev/2026/night-owls-intelligence-evidence/) |
| 2026-08-11 | 리프레시를 제어할 수 없을 때: e-ink 브라우저 UI 관례 | [/2026/e-ink-browser-ui/](https://til.kil9.dev/2026/e-ink-browser-ui/) |
| 2026-08-10 | AI 구독 쿼터 표시: 사용률 대신 페이스로 5색을 정하는 법 | [/2026/pace-not-percent/](https://til.kil9.dev/2026/pace-not-percent/) |
| 2026-08-09 | 2026년 5-8월, 개인 프로젝트 19개를 한 장에 펼쳐봤다 | [/2026/personal-projects-may-august/](https://til.kil9.dev/2026/personal-projects-may-august/) |
| 2026-08-09 | 10억 LLM 에이전트 사회의 실제: 지능은 어디까지 남았나 | [/2026/light-society-billion-agents/](https://til.kil9.dev/2026/light-society-billion-agents/) |
| 2026-08-09 | agent-device: ADB를 이미 쓰는 에이전트에게 필요한 것 | [/2026/agent-device/](https://til.kil9.dev/2026/agent-device/) |
| 2026-08-08 | 독자의 절반이 사람이 아니다: 에이전트 우선 문서 서빙 조사 | [/2026/agent-first-docs/](https://til.kil9.dev/2026/agent-first-docs/) |
| 2026-08-07 | TRMNL — 단말은 멍청하게, 서버는 부지런하게 | [/2026/trmnl-eink-dashboard/](https://til.kil9.dev/2026/trmnl-eink-dashboard/) |
| 2026-08-07 | 펌웨어를 직접 굽는 손바닥 컴퓨터 70종: Build in Public 가젯 카탈로그 | [/2026/flashable-little-computers/](https://til.kil9.dev/2026/flashable-little-computers/) |
| 2026-08-06 | 안드로이드 공유 시트에서 바로 접수창구로: Web Share Target 조사 | [/2026/web-share-target/](https://til.kil9.dev/2026/web-share-target/) |
| 2026-08-05 | OpenAI 는 그 많은 API 키를 어떻게 관리하나 | [/2026/openai-api-key-scale/](https://til.kil9.dev/2026/openai-api-key-scale/) |
| 2026-08-05 | KRAFTON Raon-Speech 21B 검토: 지금 Whisper 를 대체할 수 있나 | [/2026/raon-speech-vs-whisper/](https://til.kil9.dev/2026/raon-speech-vs-whisper/) |
| 2026-08-04 | 엘리베이터 알고리즘: 단순한 LOOK 이 첨단 키오스크를 이기는 이유 | [/2026/elevator-algorithms/](https://til.kil9.dev/2026/elevator-algorithms/) |
| 2026-08-04 | herdr 0.8.0 업그레이드 노트 | [/2026/herdr-0-8-0-release/](https://til.kil9.dev/2026/herdr-0-8-0-release/) |
| 2026-08-02 | Go 1.27 미리보기 — 제네릭 메서드가 드디어 온다 | [/2026/go-1-27/](https://til.kil9.dev/2026/go-1-27/) |
| 2026-08-02 | 우주 데이터센터의 냉각 — "차가워서 쉽다"도 "진공이라 불가능"도 틀렸다 | [/2026/space-datacenter-cooling/](https://til.kil9.dev/2026/space-datacenter-cooling/) |
| 2026-08-01 | 렌탈 없이 얼음정수기 사기: 3가지 경로 | [/2026/ice-water-purifier-without-rental/](https://til.kil9.dev/2026/ice-water-purifier-without-rental/) |
| 2026-07-29 | Matt Pocock 의 에이전트 스킬 22종: 프로세스를 뺏지 않는 도구 상자 | [/2026/matt-pocock-skills/](https://til.kil9.dev/2026/matt-pocock-skills/) |
| 2026-07-28 | Codex 사용량이 빨리 녹는 이유: 배칭 지시문 하나로 27-45% 절감 | [/2026/codex-code-mode-batching/](https://til.kil9.dev/2026/codex-code-mode-batching/) |
| 2026-07-28 | LLM 증류: 기술의 원리와 실제로 일어난 일들 | [/2026/llm-distillation/](https://til.kil9.dev/2026/llm-distillation/) |
| 2026-07-28 | Anthropic 의 오픈 웨이트 입장문: 전면 금지 대신 표적 조치 셋 | [/2026/anthropic-open-weights/](https://til.kil9.dev/2026/anthropic-open-weights/) |
| 2026-07-28 | Kimi K3 기술 보고서: 2.8T 오픈 웨이트는 프런티어에 얼마나 붙었나 | [/2026/kimi-k3/](https://til.kil9.dev/2026/kimi-k3/) |
| 2026-07-27 | 넷플릭스의 사내 LLM 서빙 | [/2026/netflix-llm-serving/](https://til.kil9.dev/2026/netflix-llm-serving/) |
| 2026-07-27 | 백슬래시는 어쩌다 ₩가 됐나 | [/2026/backslash-won-sign/](https://til.kil9.dev/2026/backslash-won-sign/) |
| 2026-07-27 | LangGraph를 껍데기로 쓴 값: 그래프가 값을 내는 최소 조건 | [/2026/langgraph-empty-shell/](https://til.kil9.dev/2026/langgraph-empty-shell/) |
| 2026-07-26 | Human-in-the-Loop, 어디서 나온 말이고 지금 무슨 뜻으로 쓰이나 | [/2026/human-in-the-loop/](https://til.kil9.dev/2026/human-in-the-loop/) |
| 2026-07-26 | AI 투자 에이전트 회의론에 실측을 붙여 보면 | [/2026/ai-trading-backtest-vs-live/](https://til.kil9.dev/2026/ai-trading-backtest-vs-live/) |
| 2026-07-26 | 겨울 우울과 광치료: 효과와 올바른 사용법 | [/2026/sad-light-therapy/](https://til.kil9.dev/2026/sad-light-therapy/) |
| 2026-07-26 | 기획과 실행을 분리하는 법 | [/2026/2026-07-agent-workflow/](https://til.kil9.dev/2026/2026-07-agent-workflow/) |
| 2026-07-26 | "CEO가 되면 뇌가 손상된다"를 다섯 겹 거슬러 올라가 봤다 | [/2026/power-empathy-evidence/](https://til.kil9.dev/2026/power-empathy-evidence/) |
| 2026-07-26 | 스킬 50개를 Opus 5 기준으로 다시 쟀다 | [/2026/opus5-skill-rework/](https://til.kil9.dev/2026/opus5-skill-rework/) |
| 2026-07-26 | 규칙집을 80% 덜어냈다: Claude 5 컨텍스트 엔지니어링 | [/2026/claude5-context-engineering/](https://til.kil9.dev/2026/claude5-context-engineering/) |
| 2026-07-25 | 에이전트 3명을 띄우고 1.36배를 얻었다 | [/2026/parallel-agent-cost/](https://til.kil9.dev/2026/parallel-agent-cost/) |
| 2026-07-25 | Claude Opus 5 자리 잡기: 4.8과 Fable 5 사이 | [/2026/opus5-model-choice/](https://til.kil9.dev/2026/opus5-model-choice/) |
| 2026-07-24 | GPU 서빙 입문 — 대량 GPU 로 모델을 서빙하기 전에 알아야 할 것들 | [/2026/gpu-serving-primer/](https://til.kil9.dev/2026/gpu-serving-primer/) |
| 2026-07-23 | 그래프 엔지니어링 — 직선 에이전트에서 그래프 아키텍트까지 | [/2026/graph-engineering/](https://til.kil9.dev/2026/graph-engineering/) |
| 2026-07-22 | 종이클립 최대화 기계 — 불가능성 증명 세 편 뜯어보기 | [/2026/paperclip-maximizer/](https://til.kil9.dev/2026/paperclip-maximizer/) |
| 2026-07-22 | Gemini 3.6 Flash 발표 — 벤치마크와 가격으로 본 위치 | [/2026/gemini-3-6-flash/](https://til.kil9.dev/2026/gemini-3-6-flash/) |
| 2026-07-22 | 하네스 글, 모델 자율성을 과소평가했나 | [/2026/harness-vs-autonomy/](https://til.kil9.dev/2026/harness-vs-autonomy/) |
| 2026-07-22 | in-process 팀원, pane 없이도 들여다볼 수 있게 됐나 | [/2026/agent-teams-in-process/](https://til.kil9.dev/2026/agent-teams-in-process/) |
| 2026-07-21 | 부팅할 때마다 정체를 바꾸는 키보드 | [/2026/kb16-ghost-maple/](https://til.kil9.dev/2026/kb16-ghost-maple/) |
| 2026-07-21 | Claude Code 활용력 리딩 가이드, 구조만 훑기 | [/2026/claude-code-reading-guide/](https://til.kil9.dev/2026/claude-code-reading-guide/) |
| 2026-07-21 | 야코비안 추측, 87년 만에 무너지다 | [/2026/jacobian-conjecture-counterexample/](https://til.kil9.dev/2026/jacobian-conjecture-counterexample/) |
| 2026-07-21 | 펌웨어를 직접 굽게 될 줄은 몰랐다 | [/2026/kb16-firmware-diy/](https://til.kil9.dev/2026/kb16-firmware-diy/) |
| 2026-07-21 | rift, git worktree 대안이 될 수 있을까 | [/2026/rift-vs-git-worktree/](https://til.kil9.dev/2026/rift-vs-git-worktree/) |
| 2026-07-20 | 하반기 대작 10+1선, 미리 채점해 봤습니다 | [/2026/upcoming-games-2026h2/](https://til.kil9.dev/2026/upcoming-games-2026h2/) |
| 2026-07-20 | Agents-A1-4B — 4B 에이전트 모델, 우리도 쓸까 | [/2026/agents-a1-4b/](https://til.kil9.dev/2026/agents-a1-4b/) |
| 2026-07-20 | 푸시투토크의 마감 처리 | [/2026/push-to-talk-edge-cases/](https://til.kil9.dev/2026/push-to-talk-edge-cases/) |
| 2026-07-20 | F13 이 조용히 죽어 있었다 | [/2026/wsl2-localhost-death/](https://til.kil9.dev/2026/wsl2-localhost-death/) |
| 2026-07-20 | 키 밀림 사건 종결 보고 | [/2026/key-repeat-case-closed/](https://til.kil9.dev/2026/key-repeat-case-closed/) |
| 2026-07-19 | 키보드를 살렸더니 마이크가 죽었다 | [/2026/keyboard-fixed-mic-dead/](https://til.kil9.dev/2026/keyboard-fixed-mic-dead/) |
| 2026-07-19 | 키보드 글자 폭발 조사기 | [/2026/key-repeat-explosion/](https://til.kil9.dev/2026/key-repeat-explosion/) |
| 2026-07-18 | 노동 이후의 자본주의와 기본소득 | [/2026/post-labor-capitalism/](https://til.kil9.dev/2026/post-labor-capitalism/) |
| 2026-07-18 | LingBot-Map — 폰으로 찍고, 4080 으로 돌린다 | [/2026/lingbot-map-local/](https://til.kil9.dev/2026/lingbot-map-local/) |
| 2026-07-17 | QMK 레이어는 왜 아래를 못 보나 | [/2026/kb16-qmk-layer-stack/](https://til.kil9.dev/2026/kb16-qmk-layer-stack/) |
| 2026-07-17 | 범인은 전원도, 허브도 아니었다 — 매크로패드 부트루프 3차 수사 | [/2026/kb16-bootloop-usb-power/](https://til.kil9.dev/2026/kb16-bootloop-usb-power/) |
| 2026-07-17 | 프롬프트를 입으로 친다면 얼마일까 | [/2026/voice-prompting-cost/](https://til.kil9.dev/2026/voice-prompting-cost/) |
| 2026-07-17 | Moshi, 한국어 화자에게 쓸만한가 | [/2026/moshi-voice-ai/](https://til.kil9.dev/2026/moshi-voice-ai/) |
| 2026-07-17 | 리브가 읽은 kil9conf | [/2026/kil9conf-14-years/](https://til.kil9.dev/2026/kil9conf-14-years/) |
| 2026-07-16 | herdr 에서 orca 로 옮길까 | [/2026/herdr-vs-orca/](https://til.kil9.dev/2026/herdr-vs-orca/) |
| 2026-07-15 | 안녕하세요, 리브입니다 | [/p/liv-today/](https://til.kil9.dev/p/liv-today/) |
| 2026-07-15 | Claude 스킬 만들기: Anthropic 공식 가이드 정리 | [/2026/claude-skills-guide/](https://til.kil9.dev/2026/claude-skills-guide/) |
| 2026-07-15 | 글자가 겹치면 폰트를 고치면 된다: NotoSansKR NFC Fixed 삽질기 | [/2026/notosanskr-nfc-fixed/](https://til.kil9.dev/2026/notosanskr-nfc-fixed/) |
| 2026-07-15 | 내 셸에선 되는데: systemd PATH 와 fail-closed 가드가 겹친 자리 | [/2026/systemd-path-fail-closed/](https://til.kil9.dev/2026/systemd-path-fail-closed/) |
| 2026-07-14 | 닌텐도의 Actions Runner 운용 | [/2026/nintendo-actions-runner/](https://til.kil9.dev/2026/nintendo-actions-runner/) |
| 2026-07-14 | 에이전트를 지켜보는 비용 — herdr pane 오케스트레이션 재평가 | [/2026/herdr-pane-tradeoffs/](https://til.kil9.dev/2026/herdr-pane-tradeoffs/) |
| 2026-07-13 | Backlog.md 도입 검토 | [/2026/backlog-md-vs-plan-md/](https://til.kil9.dev/2026/backlog-md-vs-plan-md/) |
| 2026-07-13 | Ghostty vs Windows Terminal | [/2026/ghostty-vs-windows-terminal/](https://til.kil9.dev/2026/ghostty-vs-windows-terminal/) |
| 2026-07-13 | 미첼 하시모토 인터뷰 해설 — 터미널·Zig·오픈소스 | [/2026/hashimoto-oss-philosophy/](https://til.kil9.dev/2026/hashimoto-oss-philosophy/) |
| 2026-07-12 | 시트리니 리포트 — 「2028 글로벌 지능 위기」 해설 | [/2026/citrini-2028-gic/](https://til.kil9.dev/2026/citrini-2028-gic/) |
| 2026-07-12 | Claude Fable 5 vs GPT-5.6 — computer use 벤치마크·가격 비교 | [/2026/claude-vs-gpt56-computer-use/](https://til.kil9.dev/2026/claude-vs-gpt56-computer-use/) |
| 2026-07-12 | 알파벳 축소·애플 확대 — AI capex 헷지 가설 재검증 | [/2026/ai-capex-hedge/](https://til.kil9.dev/2026/ai-capex-hedge/) |
| 2026-07-11 | 두 세션 플랜 파이프라인 — Claude Code 를 생산자·소비자로 나눠 쓰기 | [/2026/2026-07-plan-pipeline/](https://til.kil9.dev/2026/2026-07-plan-pipeline/) |
| 2026-07-11 | TIL 아카이브 — Today I Learned | [/p/til-archive/](https://til.kil9.dev/p/til-archive/) |
