# kil9 / til

`/publish-pages` 로 요청한 정적 페이지를 GitHub Pages 로 퍼블리시하는 저장소.

- 라이브 사이트: <https://kil9.github.io/til/>
- 각 페이지는 자체 완결형(self-contained) HTML 이며, 한 페이지당 디렉터리 하나를 차지한다.
- 루트 `index.html` 은 퍼블리시된 페이지 전체를 나열하는 갤러리 랜딩 페이지다.

## URL 구조

```
https://kil9.github.io/til/                     루트 갤러리
https://kil9.github.io/til/<디렉터리>/           개별 페이지 (예: 2026-matsuri-wuwa)
```

GitHub Pages 는 `main` 브랜치 루트를 그대로 서빙한다(별도 빌드 없음). `main` 에 push 하면 몇십 초 뒤 반영된다.

## 페이지 추가하기

1. 퍼블리시할 콘텐츠(자체 완결형 HTML)를 준비한다.
2. `<slug>/index.html` 로 새 디렉터리에 저장한다.
3. 루트 `index.html` 의 갤러리 목록과 이 README 의 "퍼블리시된 페이지" 목록을 갱신한다.
4. `main` 에 commit / push 한다.

에이전트가 수행할 때의 상세 절차와 규칙은 [AGENTS.md](AGENTS.md) 의 퍼블리시 런북을 따른다.

## 주요 기능

- 정적 HTML 페이지를 디렉터리 단위로 호스팅
- 퍼블리시된 페이지를 한눈에 보는 갤러리 랜딩 페이지
- 라이트/다크 테마 자동 대응(각 페이지가 `prefers-color-scheme` 지원)
- 외부 의존성 없는 단일 파일 페이지(오프라인에서도 열림)

## 퍼블리시된 페이지

| 날짜 | 페이지 | 경로 |
| --- | --- | --- |
| 2026-07-11 | TIL 아카이브 — Today I Learned | [/til-archive/](https://kil9.github.io/til/til-archive/) |
| 2026-07-11 | 姫森ルーナ ✕ 鳴潮 — 루나의 명조 방송 항해일지 | [/2026-luna-wuwa/](https://kil9.github.io/til/2026-luna-wuwa/) |
| 2026-07-11 | 夏色まつり ✕ 鳴潮 — 마츠리의 명조 방송 전기록 | [/2026-matsuri-wuwa/](https://kil9.github.io/til/2026-matsuri-wuwa/) |
| 2026-07-11 | 두 세션 플랜 파이프라인 — Claude Code 를 생산자·소비자로 나눠 쓰기 | [/2026-07-plan-pipeline/](https://kil9.github.io/til/2026-07-plan-pipeline/) |
| 2026-07-12 | 알파벳 축소·애플 확대 — AI capex 헷지 가설 재검증 | [/ai-capex-hedge/](https://kil9.github.io/til/ai-capex-hedge/) |
| 2026-07-12 | Claude Fable 5 vs GPT-5.6 — computer use 벤치마크·가격 비교 | [/claude-vs-gpt56-computer-use/](https://kil9.github.io/til/claude-vs-gpt56-computer-use/) |
| 2026-07-12 | 시트리니 리포트 — 「2028 글로벌 지능 위기」 해설 | [/citrini-2028-gic/](https://kil9.github.io/til/citrini-2028-gic/) |
| 2026-07-13 | 미첼 하시모토 인터뷰 해설 — 터미널·Zig·오픈소스 | [/hashimoto-oss-philosophy/](https://kil9.github.io/til/hashimoto-oss-philosophy/) |
