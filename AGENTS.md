# AGENTS.md

이 저장소에서 AI 에이전트가 작업하기 위한 지침이다. 사람용 개요는 [README.md](README.md), 진행 상황은 backlog(`backlog/`, 조회는 `/next-task`)를 본다. 구 [PLAN.md](PLAN.md) 는 2026-07-13 backlog 로 전환되어 완료 이력 아카이브로만 남아 있다.

## 이 저장소는 무엇인가

`kil9/til` 은 정적 HTML 페이지를 GitHub Pages 로 호스팅하는 퍼블리시 저장소다. 사용자가 `/publish-pages` 로 특정 콘텐츠(주로 claude.ai artifact)를 넘기면, 그 콘텐츠를 자체 완결형 HTML 로 만들어 새 디렉터리에 담고 목록을 갱신한 뒤 `main` 에 push 한다.

- 라이브: <https://kil9.github.io/til/>
- 호스팅: GitHub Pages, `main` 브랜치 루트에서 직접 서빙(Deploy from a branch, 빌드 없음)
- 공개 범위: **public** 저장소(무료 Pages 조건). 여기에 올리는 모든 것은 즉시 공개된다.

## 저장소 구조

```
til/
├── index.html            루트 갤러리 랜딩 페이지(퍼블리시된 페이지 목록)
├── README.md             사람용 개요 + 퍼블리시된 페이지 표
├── AGENTS.md             (이 파일) 에이전트 지침 + 퍼블리시 런북
├── 404.html              커스텀 404 + 구 URL → 신 경로 리다이렉트 맵
├── backlog/              진행 상황 원본(태스크·draft·docs·decisions, backlog CLI)
├── PLAN.md               (아카이브) backlog 전환 전 진행 상황·완료 이력
├── CLAUDE.md             AGENTS.md 로 향하는 심볼릭 링크
├── <YYYY>/                날짜 아티클(til). 연도가 최상위 버킷 (예: 2026/)
│   └── <slug>/
│       └── index.html   개별 페이지(자체 완결형 HTML)
└── p/                    비-날짜 지원 페이지(pages). 소개·아카이브·제출 도구 등
    └── <slug>/
        └── index.html
```

- 루트를 평평하게 두지 않는다(TASK-32, TASK-40 에서 `t/` 래퍼 제거). 날짜 아티클은 `<연도>/<slug>/`, 비-날짜 상설 페이지(리브 소개·아카이브·관리자 제출 도구 등)는 `p/<slug>/` 아래에 둔다. 루트에는 `<연도>/`·`p/`·`backlog/` 와 루트 파일만 남긴다.
- 연도(`<YYYY>`)는 갤러리 카드 `data-date` 의 연도를 쓴다(현재는 전부 `2026`).
- 슬러그는 kebab-case. `<연도>/` 로 이미 시간 분리되므로 슬러그에 `2026-` 연도 접두사를 새로 붙일 필요는 없다(기존 `2026-07-plan-pipeline` 등은 그대로 둔다).
- 슬러그·경로는 URL 에 영구히 박히므로 퍼블리시 전에 사용자에게 확인받는다. 구 평면 URL(`/til/<slug>/`)은 `404.html` 리다이렉트 맵이 새 경로로 넘겨준다.

## 퍼블리시 런북 (`/publish-pages`)

> 참고: 이 런북의 자동화 스킬은 `/publish-til`(사외용)이다. `/publish-pages` 는 사내망 감지 자동 분기 디스패처(사내 `/publish-naver` ↔ 사외 `/publish-til`), `/publish-naver` 는 사내 GHE+Naver Pages 용이다. 스킬과 이 런북이 어긋나면 **이 런북이 정본**이다.

### 1. 콘텐츠 확보

- 대상이 claude.ai artifact URL(`https://claude.ai/code/artifact/<uuid>`) 이면 **WebFetch** 로 가져온다. `curl` 은 SPA 셸이나 Cloudflare 403 을 받으므로 쓰지 않는다.
- 반환된 HTML 에는 claude.ai 프레임 런타임이 주입돼 있다. 다음을 **제거**한다.
  - `<script>window.__FRAME_PREAMBLE=...</script>` 및 `<!-- frame-runtime -->` ~ `<!-- /frame-runtime -->` 블록 전체
  - 래퍼가 넣은 최소 리셋(`:root{color-scheme:light}` 등) 중 페이지 자체 스타일과 충돌하는 부분
- 페이지 자체의 `<style>`, `<header>`, `<main>`(본문)만 남긴다.

### 2. 자체 완결형 문서로 재조립

깨끗한 standalone HTML 로 감싼다. artifact 원본이 자체 스타일을 갖고 있으면 그 스타일을 존중하고(기존 plan-pipeline 페이지처럼), 스타일이 없거나 페이지를 새로 쓰는 경우에는 아래 **공통 셸**(사이트 디자인, T-23 확정: 극한 미니멀·무채색+차가운 블루 액센트)을 기본으로 쓴다.

```html
<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>페이지 제목</title>
<meta name="description" content="한 줄 설명">
<link rel="icon" type="image/webp" href="data:image/webp;base64,(리브 파비콘 — 루트 index.html 의 것을 그대로 복사)">
<meta property="og:type" content="article">
<meta property="og:title" content="페이지 제목">
<meta property="og:description" content="한 줄 설명">
<meta property="og:url" content="https://kil9.github.io/til/<YYYY>/<slug>/">
<meta property="og:site_name" content="today i learned">
<meta property="og:locale" content="ko_KR">
<meta name="twitter:card" content="summary">
<style>
  :root {
    --bg: #FFFFFF;
    --text: #1B2027;
    --text-muted: #4E5A66;
    --text-faint: #6E7A86;
    --rule: #E3E7EB;
    --accent: #1A5FC8;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #14171B;
      --text: #E7EAEE;
      --text-muted: #A9B3BD;
      --text-faint: #7E8994;
      --rule: #2A3037;
      --accent: #82B1F0;
    }
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; background: var(--bg); color: var(--text);
    font-family: "Pretendard", -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo",
      "Noto Sans KR", "Malgun Gothic", system-ui, sans-serif;
    font-size: 16px; line-height: 1.6; -webkit-font-smoothing: antialiased;
  }
  main { max-width: 720px; margin: 0 auto; padding: 48px 24px 80px; }
  h1 { margin: 0 0 8px; font-size: 1.5rem; font-weight: 700; letter-spacing: -0.01em; }
  h2 { margin: 40px 0 12px; font-size: 1.0625rem; font-weight: 600; }
  p { margin: 0 0 12px; }
  a { color: var(--accent); text-decoration: underline; text-underline-offset: 3px; }
  code { font-family: ui-monospace, "SF Mono", monospace; font-size: 0.9em; }
  hr { border: 0; border-top: 1px solid var(--rule); margin: 32px 0; }
  footer {
    margin-top: 64px; padding-top: 16px; border-top: 1px solid var(--rule);
    font-size: 0.8125rem; color: var(--text-faint);
  }
</style>
</head>
<body>
<main>
  <p class="home-top" style="margin:0 0 28px;font-size:0.8125rem"><a href="../../">← today i learned</a></p>
  ... 본문 ...
  <footer><p><a href="../../">← today i learned</a></p></footer>
</main>
<!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "56f2ecb667db487b82dc24020c16d8a2"}'></script><!-- End Cloudflare Web Analytics -->
</body>
</html>
```

- 외부 리소스(CDN 스크립트/폰트/이미지) 의존 없이 단일 파일로 열려야 한다. 필요한 자산은 인라인하거나 `data:` URI 로 임베드한다. 웹폰트는 쓰지 않는다(시스템 폰트 스택만).
- artifact 원본 스타일을 유지하는 페이지라도 **favicon·OG 메타(위 템플릿의 `<link rel="icon">`\~`twitter:card` 블록, 제목·설명·slug 치환)와 beacon 은 반드시 넣는다**(T-24). OG 이미지는 쓰지 않는다. 파비콘은 전 페이지 공통 **리브 원형 아이콘**(64px WebP, 얼굴 크롭 + 원형 마스크)이며 페이지별 커스텀 파비콘을 만들지 않는다 — base64 데이터는 루트 `index.html` 의 것을 복사한다.
- **인덱스로 돌아가는 링크(`← today i learned`)를 상단(본문 첫 요소)과 하단(footer) 양쪽에 넣는다.** 자체 스타일 페이지도 동일 — 상단은 히어로/본문 컨테이너의 첫 요소로, 하단은 기존 footer 안에 넣는다. 위 템플릿의 `../../` 은 아티클 뎁스(`<YYYY>/<slug>/`, 루트가 2단계 위) 기준이며, 지원 페이지(`p/<slug>/`)도 같은 2단계라 동일하게 `../../` 다.
- **유일한 예외는 Cloudflare Web Analytics beacon**(T-15)이다. 위 템플릿의 `</body>` 직전 beacon `<script>` 를 **모든 신규 페이지에 그대로 넣는다**(token 은 클라이언트 임베드용 공개 값). 쿠키 없는 익명 집계이며, 로드 실패해도 페이지 렌더에는 영향이 없다. 지표는 CF 대시보드(Web Analytics, `kil9.github.io`)에서 본다.
- 라이트/다크 대응은 `@media (prefers-color-scheme: dark)` 로 둔다. claude.ai 의 `data-theme` 토글은 standalone 환경에 없으므로 `prefers-color-scheme` 폴백이 있어야 한다.
- 추적/텔레메트리 성격의 주입 스크립트는 모두 제거한다.

### 2-1. 시각 자료 (T-27)

- 텍스트만으로 전달이 어려운 수치·비교·구조·흐름은 표·차트·인포그래픽으로 보강하는 것이 기본이다. 수치 비교는 표, 추이·비중은 **인라인 SVG 차트**, 개념 구조·루프·타임라인은 인라인 SVG 다이어그램으로 그린다. SVG 의 fill/stroke 에 페이지 CSS 변수(`var(--text)`, `var(--accent)` 등)를 써서 다크모드에 자동 대응시킨다. 외부 차트 라이브러리는 쓰지 않는다. (이미 완성된 artifact 를 그대로 옮기는 경우는 원본을 존중한다.)
- 개념 은유·분위기 환기용 **삽화**는 실제로 도움이 될 때만 페이지당 1-2장. 래스터 삽화 생성은 로컬 이미지 생성 에이전트(codex CLI 의 `image_generation`)에 위임한다(레시피는 `/publish-til` 스킬 §2-2). 결과물은 폭 1440px·WebP(q75, 약 70-100KB)로 압축해 base64 `data:image/webp;base64,` URI 로 임베드한다 — 사이드카 이미지 파일 금지(단일 파일 원칙).
- 마크업: `figure.illust` + 상세 `alt` + `figcaption`(설명 + "삽화: Codex 이미지 생성" 출처 표기), 다크모드에서 `filter: brightness(0.9)`. 예시는 `citrini-2028-gic/index.html`.

### 2-2. 화자 — 리브 투데이 (T-4, TASK-6·TASK-11 개정)

이 사이트의 페이지에는 전속 AI 지식 큐레이터 캐릭터 **리브 투데이**(평소 호칭 "리브")라는 화자 자아가 있다. 설정 진실원본은 `backlog/docs/doc-3 - 리브-투데이-캐릭터-설정.md`(성격·문체 규칙·예문·비주얼 스펙·설정화 시트)이며, 아래는 퍼블리시 시 지켜야 할 요약이다.

- **적용 범위**: T-4 이후 **신규 페이지부터**. 기존 페이지는 일괄 소급하지 않되, 사용자가 특정 페이지를 지정하면 예외로 개고한다(`notosanskr-nfc-fixed` 가 그 사례). 소급 시 본문 보고서체는 유지하고 리브 문장·삽화만 얹는다.
- **본문은 기존과 동일한 건조한 보고서체**가 기본이다. 정보 전달이 주, 자아는 양념.
- **위치 제한 없음**: 도입부(작성 경위), 본문 중간(곁가지 감상·실수 고백), 마무리(소감·다음 안내) 중 자연스러운 자리에 넣는다.
- **성격(TASK-11 개정)**: 핵심 축은 **일은 정확하게 하는데 두 번 하기 싫어서 최소 동선을 찾는 사람**이다. 텐션이 낮고 시큰둥하되, 무기력·번아웃과는 다르다 — 지쳐 쓰러질 것 같은 인상은 이 캐릭터가 아니다. 곁가지를 못 버리고 쌓아 두는 호더 기질은 유지된다.
- **드물수록 효과가 크다(TASK-11)**: 한 자리당 1-2문장, 페이지 전체로도 몇 자리면 충분하다. 한 가지 캐릭터성(특히 귀찮음·나른함)을 문단마다 반복하면 금방 질린다. 삽화가 이미 나른함을 보여주므로 글에서 되풀이할 필요가 없다. 애매하면 뺀다.
- **톤**: 존댓말, 사이트 주인 호칭은 "사용자님". 나른하되 담백하게. 과장·이모지·느낌표를 남발하지 않는다(느낌표는 페이지당 1회 이하가 기본).
- **호칭(TASK-20)**: 풀네임 "리브 투데이"는 소개 페이지(`/p/liv-today/`)의 자기소개부(인사말·이름 유래)와 공개 설정화 페이지(`/p/liv-today/sheet/`)에서만 노출한다. 그 외 모든 자리(본문·바이라인·meta description·삽화 alt·루트 인덱스)는 "리브"로 쓴다. 저장소 문서(README·AGENTS.md·doc-3)는 캐릭터를 정의하는 자리라 풀네임을 유지한다.
- **어휘**: AI 툴·데이터·파이프라인을 다루는 현대적 어휘로 쓴다 — 쌓이는 곳은 "아카이브", 결과물은 "보고서"·"페이지". 구 "서고지기" 컨셉의 도서관 어휘("서고"·"서가"·"장서"·"사서"·"열람")는 TASK-6 에서 폐기됐으므로 되살리지 않는다.
- **위 문체·비주얼 항목은 기본값이지 금지 목록이 아니다.** 페이지의 목적에 맞으면 벗어나도 된다. 특정 페이지·컷을 위한 일회성 조정은 그것에만 적용하고 설정(doc-3)으로 편입하지 않는다 — 그렇게 굳히면 캐릭터가 쓸 수 있는 표현이 계속 줄어든다.
- **캐릭터 이미지(TASK-11 개정)**: 삽화로 쓸 때는 SD(넨드로이드 치비)가 메인이고, 설정화 시트 8컷이 `backlog/assets/liv/sheet/` 에, 공개 설정화 페이지가 `/p/liv-today/sheet/` 에 있다(갤러리 미노출, 소개 페이지 링크로만 진입 — 공개 페이지는 SD 6컷과 코멘트 아바타 표정 6종을 게시하고 사람 비율 2컷은 내렸다). 화풍은 **굵은 아웃라인의 플랫 마스코트 풍**, 헤어는 **뒤에서 낮게 묶어 목덜미가 드러나는 로우 번**(TASK-57, 2026-07-19 채택 — 구 풀어헤친 보브는 legacy), 기본 복장은 **그레이 후디 + 네이비 와이드 팬츠**(OL 룩은 외출용, 소매 걷은 셔츠+블루 카디건 변형은 외출·바쁜 작업일 배리에이션)이며, 앞머리 한 갈래에 **파란 통신 헤어핀**(그릴 슬릿 + 청록 LED, 2026-07-17 추가·잠정)이 있다 — 공개 노출 컷(소개 페이지·공개 설정화 SD 6컷·아바타)은 모두 핀 판본이고, 내부 참고용 사람 비율 2컷만 핀 없는 구 판본이다(doc-3 §4). 사람 비율 컷은 공개 페이지에 쓰지 않는다(내부 참고용, `backlog/assets/liv/` 에만 둔다). 신규 생성이 필요하면 doc-3 §4-2\~§4-5 의 확정 프롬프트·일관성 규칙을 따른다 — 특히 `codex exec -i ref.png -- "프롬프트"` 의 `--` 를 빠뜨리면 프롬프트가 통째로 삼켜진다. 임베드 규칙은 §2-1 과 동일(base64 `data:` URI, 사이드카 파일 금지). **base64 치환 시 placeholder 이름이 서로의 접두사가 되지 않게 하고**(`IMG_OL` 이 `IMG_OLC` 를 깨뜨린 사고가 있었다), 임베드 후 각 URI 를 디코드해 WebP 헤더(RIFF/WEBP)까지 검증한다.
- **리브 코멘트 블록(`.liv`)에는 아바타 아이콘을 넣는다.** 마크업은 `<div class="liv"><img src="data:image/webp;base64,…" alt="리브" width="72" height="72"><p>본문</p></div>`, CSS 는 `.liv { display: grid; grid-template-columns: auto 1fr; gap: 10px; align-items: start; }` + `.liv img { grid-column: 1; grid-row: 1; width: 28px; height: 28px; margin-top: 2px; border-radius: 50%; background: #FFFFFF; }` + `.liv p { grid-column: 2; }` 다. **flex 로 짜지 말 것** — `.liv` 안에 `<p>` 가 둘 이상이면 flex 는 문단을 가로로 나열해 2칼럼처럼 보인다(kb16 마지막 블록이 그렇게 깨져 게시됐다). grid 는 `<p>` 가 몇 개든 2열에 행으로 쌓아 준다. 아바타가 화자를 나타내므로 `"리브 —"` 같은 텍스트 라벨은 넣지 않는다(구 `.liv .who` 패턴은 2026-07-17 폐기). **원본은 헤어핀 판본을 72x72 WebP q85(약 2KB)로 줄여 쓴다** — 표시가 28px 이라 256px 원본은 과하고, 한 페이지에 코멘트가 서너 개면 그만큼 반복 임베드돼 용량이 불어난다(agent-workflow 가 256px 3회 반복으로 352KB 였다가 320KB 로 줄었다). TASK-15의 6종은 `backlog/assets/liv/avatar-expression-<표정>-72.webp` 에 있고, 코멘트의 정서에 맞춰 고른다. 한 페이지에서 같은 표정을 반복하지 않으며, 애매하면 기본 시큰둥(`base`)을 쓴다. 테두리 배경을 흰색으로 두는 이유는 원본 배경이 흰색이라 다크모드에서 원형 경계가 깨지지 않게 하기 위함이다.
- 루트 `index.html` 은 본문(`.feed`, 카드 목록)과 우측 사이드바(`aside.side`, 260px) 2칼럼이다. 사이드바 위쪽이 리브의 상설 노출 자리인 `a.keeper` 블록(아바타·이름·한 줄 소개 전체가 `/p/liv-today/` 로 가는 링크), 그 아래가 사람 관리자 `.human` 블록(kil9, 링크 없음 — 아바타·이름·한 줄 소개 스타일은 `.keeper` 와 공유한다)이며, 그 아래가 '리브의 코멘트'(`<!-- AI-SUMMARY:START -->`\~`END`)다(TASK-13 에서 소개가 먼저 오도록 재배치). 구분선(`border-top`)은 `.ai-summary` 앞에만 두고 소개 두 블록 사이는 여백만 준다 — `a.keeper` 는 사이드바 최상단이라 `margin-top`·`padding-top`·`border-top` 이 없다. `.human` 아바타는 24px 도트 원본이라 `image-rendering: pixelated` 로 확대 보간을 끈다. 히어로는 제목 + 사이트 소개(`.site-intro`)만 두고, 인덱스에서 리브의 표기는 "리브"(풀네임 아님)다. 사이드바는 sticky 가 아니며(스크롤을 따라가지 않는다), 920px 이하에서는 `order: -1` 로 목록 위에 올라간다. `a.keeper` 의 hover·focus 스타일은 `a.card` 규칙(제목에 액센트 + 밑줄)과 같은 결로 맞춘다(TASK-8). 마커 구간은 머신 로컬 잡(`~/jobs/docs-ai-summary/`, repo 밖)이 통째로 덮어쓰므로 그 안에 손으로 마크업을 넣지 않는다 — 라벨·문체를 바꾸려면 잡의 `inject.py`·`run.sh` 를 함께 고쳐야 한다(TASK-9). 마커 이름 `AI-SUMMARY` 는 `inject.py` 의 정규식과 짝이라 유지한다.

### 3. 배치

- 날짜 아티클은 `<현재연도>/<slug>/index.html`, 비-날짜 상설 페이지는 `p/<slug>/index.html` 로 저장한다. `<현재연도>` dir 이 없으면 만든다.
- 새 페이지의 인덱스 복귀 링크·상대 자산 경로가 새 뎁스에 맞는지 확인한다. `<YYYY>/<slug>/`·`p/<slug>/` 둘 다 루트가 2단계 위(`../../`)다.
- 구 URL 안전망을 위해 `404.html` 의 리다이렉트 맵(`map` 객체)에 `"<slug>":"<새 경로>"` 항목을 추가한다. 새 슬러그가 옛 평면 경로와 겹칠 일은 없지만, 리다이렉트 맵은 구 슬러그의 진실원본이므로 신규도 함께 등록해 둔다.

### 4. 목록 갱신

- 루트 `index.html`: 갤러리 카드를 **최신이 위로** 추가하고 `Published · N` 카운트를 증가시킨다.
  - 카드 `<a class="card">` 의 `href` 는 새 경로(`./<YYYY>/<slug>/` 또는 `./p/<slug>/`)로 넣는다.
  - 카드 `<a class="card">` 에 `data-date="YYYY-MM-DDTHH:MM"`(정렬·아카이브용, 퍼블리시 시각까지 넣는다 — `.date` 표시는 JS 가 이 값에서 렌더링하므로 `span.date` 텍스트는 무엇을 넣어도 덮어써진다)와 `data-topic="<주제키>"`(필터 칩용, 영문 kebab-case)를 반드시 넣는다. 기존 키는 `index.html` 을 grep 해 확인하고, 새 주제면 새 키를 만든다.
  - `.tag` 는 `<칩 라벨> · <세부 주제>` 형식이고 **한국어로 쓴다**. 제품명·고유명사·정착된 약어(`Claude Code`, `SRE` 등)만 원형을 유지한다.
  - **칩 라벨은 한 단어여야 한다.** 칩은 `.tag` 를 `"·"` 로 split 한 첫 세그먼트에서 자동 생성되므로(`index.html` 의 `topics[key] = ...split("·")[0].trim()`), 칩 이름 자체에 `·` 를 넣으면 앞부분만 잘려 칩이 된다.
- `README.md`: "퍼블리시된 페이지" 표 **맨 위**에 행을 추가한다. 표는 갤러리와 같은 **최신이 위** 정렬이다(갤러리는 JS 가 `data-date` 로 런타임 정렬하지만 README 는 정적이라 손으로 순서를 지켜야 한다 — 과거에 오래된 것이 위인 채로 어긋나 있었다). 표에는 주제 열이 없으므로 재분류는 README 를 건드리지 않는다.

### 4-1. 주제 분류는 유동적이다

칩 분류에 하위 호환은 없다. 글이 쌓여 균형이 깨지면 기존 카드의 `data-topic`·`.tag` 를 자유롭게 재조정한다 — 한 주제가 비대해지면 쪼개고, 잘게 남은 것들은 합친다. `data-topic` 은 슬러그와 달리 URL 에 박히지 않아 되돌리기 쉽다(딥링크 `?topic=<키>` 가 깨지는 정도이고, 그건 감수한다).

기준값:

- 칩 개수는 총 건수에서 도출한다. 대략 **칩 하나당 3-4건**, 최소 4개·최대 9개 — 17건이면 4-6칩, 27건이면 7-9칩. 글이 늘면 칩도 같이 는다.
- 상한이 9인 근거는 폭이다. 칩 라벨이 한국어 두세 글자라 짧아서 한 줄에 그 정도가 들어간다(2026-07-16 실측: 5칩 + "전체" 가 컨테이너 폭의 절반도 못 채웠다). **라벨이 길어지거나 영문으로 돌아가면 상한도 같이 내린다.** `.chips` 는 `flex-wrap: wrap` 이라 넘쳐도 두 줄로 감싸질 뿐 레이아웃이 깨지지는 않으므로, 이 상한은 렌더링 제약이 아니라 한눈에 훑을 수 있는 개수의 문제다.
- 각 칩은 **2건 이상**. 1건짜리 칩은 인접 칩에 흡수시킨다.
- **분할 트리거는 비중이다.** 한 칩이 전체의 40% 를 넘으면 분할을 검토한다. 절대 건수(예: 8건 이상)로 트리거를 잡지 않는다 — 총량이 커지면 그런 숫자는 의미를 잃는다.
- 분할이 칩 상한을 넘길 때는 가장 작은 칩들 중 의미상 묶이는 짝을 병합해 자리를 만든다. **자연스러운 짝이 없으면 분할을 보류한다 — 억지 분류보다 불균형이 낫다.**

**위 수치는 방향을 주기 위한 기준값이지 지켜야 할 계약이 아니다.** 상황에 맞지 않으면 규칙 자체를 유동적으로 바꿔도 된다. 수치를 맞추려고 주제가 안 맞는 글을 한 칩에 몰아넣는 것이 수치를 어기는 것보다 나쁘다.

기존 카드의 분류 변경은 칩 신설·병합까지 포함해 **사용자 확인 없이 수행하고 결과만 보고한다**.

### 5. 반영

- `main` 에 commit / push 한다. 커밋 규칙은 아래 참조.
- Pages 는 push 후 몇십 초 뒤 반영된다. URL: 아티클 `https://kil9.github.io/til/<YYYY>/<slug>/`, 지원 페이지 `https://kil9.github.io/til/p/<slug>/`

## 명령어

빌드 단계는 없다. 정적 파일이 전부다.

```bash
# 로컬 미리보기 (루트에서 실행)
python3 -m http.server 8000
# → http://localhost:8000/ 및 http://localhost:8000/<YYYY>/<slug>/ (또는 /p/<slug>/)

# HTML 문법 눈검사 이외 별도 린트/테스트 없음.
# 배포 상태 확인
gh api repos/kil9/til/pages --jq '.status, .html_url'
```

## 환경 / 전제

- git remote `origin` = `https://github.com/kil9/til` (public)
- `gh` 는 github.com 계정 `kil9` 로 인증돼 있어야 한다(`repo` scope 필요).
- 필수 환경변수 없음. 외부 DB/API/MCP 의존 없음.
- GitHub Pages 설정: source = branch `main`, path = `/`(root).

## 보안 주의사항

- **저장소가 public 이다.** 시크릿·토큰·비공개 정보·개인 식별정보를 절대 커밋하지 않는다. push 하는 순간 공개되며 되돌려도 히스토리에 남는다.
- 외부 artifact 를 옮길 때 주입된 스크립트(프레임 런타임, 트래킹 등)를 제거해 순수 콘텐츠만 남긴다.
- 저작권·초상권이 걸린 콘텐츠를 공개 퍼블리시하기 전에 사용자에게 확인받는다.

## 커밋 규칙

- 커밋 전 `README.md`, `AGENTS.md`, backlog(진행 상황) 를 검토하고, 변경이 필요하면 **같은 커밋에 포함**한다. 특히 페이지를 추가하면 README 표·루트 갤러리·backlog 진행 상황이 함께 갱신돼야 한다.
- 커밋 단위는 논리적으로 분리한다(페이지 추가 1건 = 커밋 1건이 기본).
- 커밋/푸시는 사용자가 요청하거나 퍼블리시 런북을 실행할 때 수행한다.
