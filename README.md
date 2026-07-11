# kil9 / docs

`/publish-pages` 로 요청한 정적 페이지를 GitHub Pages 로 퍼블리시하는 저장소.

- 라이브 사이트: <https://kil9.github.io/docs/>
- 각 페이지는 자체 완결형(self-contained) HTML 이며, 한 페이지당 디렉터리 하나를 차지한다.
- 루트 `index.html` 은 퍼블리시된 페이지 전체를 나열하는 갤러리 랜딩 페이지다.

## URL 구조

```
https://kil9.github.io/docs/                     루트 갤러리
https://kil9.github.io/docs/<디렉터리>/           개별 페이지 (예: 2026-matsuri-wuwa)
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
| 2026-07-11 | 姫森ルーナ ✕ 鳴潮 — 루나의 명조 방송 항해일지 | [/2026-luna-wuwa/](https://kil9.github.io/docs/2026-luna-wuwa/) |
| 2026-07-11 | 夏色まつり ✕ 鳴潮 — 마츠리의 명조 방송 전기록 | [/2026-matsuri-wuwa/](https://kil9.github.io/docs/2026-matsuri-wuwa/) |
| 2026-07-11 | 두 세션 플랜 파이프라인 — Claude Code 를 생산자·소비자로 나눠 쓰기 | [/2026-07-plan-pipeline/](https://kil9.github.io/docs/2026-07-plan-pipeline/) |
