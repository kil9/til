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
├── backlog/              진행 상황 원본(태스크·draft·docs·decisions, backlog CLI)
├── PLAN.md               (아카이브) backlog 전환 전 진행 상황·완료 이력
├── CLAUDE.md             AGENTS.md 로 향하는 심볼릭 링크
└── <slug>/
    └── index.html        개별 페이지(자체 완결형 HTML)
```

- 페이지 하나당 디렉터리 하나. 디렉터리 이름이 곧 URL 경로다.
- 슬러그는 kebab-case. 시간순 정렬이 필요하면 `2026-` 처럼 연도 접두사를 붙인다(예: `2026-matsuri-wuwa`).
- 슬러그는 URL 에 영구히 박히므로 퍼블리시 전에 사용자에게 확인받는다.

## 퍼블리시 런북 (`/publish-pages`)

> 참고: 이 런북의 자동화 스킬은 `/publish-til`(사외용)이다. `/publish-pages` 는 사내망 감지 자동 분기 디스패처(사내 `/publish-naver` ↔ 사외 `/publish-til`), `/publish-naver` 는 사내 GHE+Naver Pages 용이다. 스킬과 이 런북이 어긋나면 **이 런북이 정본**이다.

### 1. 콘텐츠 확보

- 대상이 claude.ai artifact URL(`https://claude.ai/code/artifact/<uuid>`) 이면 **WebFetch** 로 가져온다. `curl` 은 SPA 셸이나 Cloudflare 403 을 받으므로 쓰지 않는다.
- 반환된 HTML 에는 claude.ai 프레임 런타임이 주입돼 있다. 다음을 **제거**한다.
  - `<script>window.__FRAME_PREAMBLE=...</script>` 및 `<!-- frame-runtime -->` ~ `<!-- /frame-runtime -->` 블록 전체
  - 래퍼가 넣은 최소 리셋(`:root{color-scheme:light}` 등) 중 페이지 자체 스타일과 충돌하는 부분
- 페이지 자체의 `<style>`, `<header>`, `<main>`(본문)만 남긴다.

### 2. 자체 완결형 문서로 재조립

깨끗한 standalone HTML 로 감싼다. artifact 원본이 자체 스타일을 갖고 있으면 그 스타일을 존중하고(기존 matsuri/luna/plan-pipeline 페이지처럼), 스타일이 없거나 페이지를 새로 쓰는 경우에는 아래 **공통 셸**(사이트 디자인, T-23 확정: 극한 미니멀·무채색+차가운 블루 액센트)을 기본으로 쓴다.

```html
<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>페이지 제목</title>
<meta name="description" content="한 줄 설명">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect x='3' y='3.2' width='10' height='1.8' rx='.9' fill='%231A5FC8'/%3E%3Crect x='3' y='7.1' width='10' height='1.8' rx='.9' fill='%238A96A2'/%3E%3Crect x='3' y='11' width='7' height='1.8' rx='.9' fill='%238A96A2'/%3E%3C/svg%3E">
<meta property="og:type" content="article">
<meta property="og:title" content="페이지 제목">
<meta property="og:description" content="한 줄 설명">
<meta property="og:url" content="https://kil9.github.io/til/<slug>/">
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
  ... 본문 ...
  <footer><p><a href="../">← today i learned</a></p></footer>
</main>
<!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "56f2ecb667db487b82dc24020c16d8a2"}'></script><!-- End Cloudflare Web Analytics -->
</body>
</html>
```

- 외부 리소스(CDN 스크립트/폰트/이미지) 의존 없이 단일 파일로 열려야 한다. 필요한 자산은 인라인하거나 `data:` URI 로 임베드한다. 웹폰트는 쓰지 않는다(시스템 폰트 스택만).
- artifact 원본 스타일을 유지하는 페이지라도 **favicon·OG 메타(위 템플릿의 `<link rel="icon">`\~`twitter:card` 블록, 제목·설명·slug 치환)와 beacon 은 반드시 넣는다**(T-24). OG 이미지는 쓰지 않는다.
- **유일한 예외는 Cloudflare Web Analytics beacon**(T-15)이다. 위 템플릿의 `</body>` 직전 beacon `<script>` 를 **모든 신규 페이지에 그대로 넣는다**(token 은 클라이언트 임베드용 공개 값). 쿠키 없는 익명 집계이며, 로드 실패해도 페이지 렌더에는 영향이 없다. 지표는 CF 대시보드(Web Analytics, `kil9.github.io`)에서 본다.
- 라이트/다크 대응은 `@media (prefers-color-scheme: dark)` 로 둔다. claude.ai 의 `data-theme` 토글은 standalone 환경에 없으므로 `prefers-color-scheme` 폴백이 있어야 한다.
- 추적/텔레메트리 성격의 주입 스크립트는 모두 제거한다.

### 2-1. 시각 자료 (T-27)

- 텍스트만으로 전달이 어려운 수치·비교·구조·흐름은 표·차트·인포그래픽으로 보강하는 것이 기본이다. 수치 비교는 표, 추이·비중은 **인라인 SVG 차트**, 개념 구조·루프·타임라인은 인라인 SVG 다이어그램으로 그린다. SVG 의 fill/stroke 에 페이지 CSS 변수(`var(--text)`, `var(--accent)` 등)를 써서 다크모드에 자동 대응시킨다. 외부 차트 라이브러리는 쓰지 않는다. (이미 완성된 artifact 를 그대로 옮기는 경우는 원본을 존중한다.)
- 개념 은유·분위기 환기용 **삽화**는 실제로 도움이 될 때만 페이지당 1-2장. 래스터 삽화 생성은 로컬 이미지 생성 에이전트(codex CLI 의 `image_generation`)에 위임한다(레시피는 `/publish-til` 스킬 §2-2). 결과물은 폭 1440px·WebP(q75, 약 70-100KB)로 압축해 base64 `data:image/webp;base64,` URI 로 임베드한다 — 사이드카 이미지 파일 금지(단일 파일 원칙).
- 마크업: `figure.illust` + 상세 `alt` + `figcaption`(설명 + "삽화: Codex 이미지 생성" 출처 표기), 다크모드에서 `filter: brightness(0.9)`. 예시는 `citrini-2028-gic/index.html`.

### 3. 배치

- `<slug>/index.html` 로 저장한다.

### 4. 목록 갱신

- 루트 `index.html`: 갤러리 카드를 **최신이 위로** 추가하고 `Published · N` 카운트를 증가시킨다.
  - 카드 `<a class="card">` 에 `data-date="YYYY-MM-DDTHH:MM"`(정렬·아카이브용, 퍼블리시 시각까지 넣는다 — `.date` 표시는 JS 가 이 값에서 렌더링하므로 `span.date` 텍스트는 무엇을 넣어도 덮어써진다)와 `data-topic="<주제키>"`(필터 칩용, kebab-case)를 반드시 넣는다. 주제키는 기존 카드 값(`hololive`, `claude-code` 등)을 재사용하고, 새 주제면 새 키를 만든다 — 칩은 `data-topic` 과 `.tag` 텍스트("·" 앞 세그먼트가 칩 라벨)에서 자동 생성된다.
- `README.md`: "퍼블리시된 페이지" 표에 행을 추가한다.

### 5. 반영

- `main` 에 commit / push 한다. 커밋 규칙은 아래 참조.
- Pages 는 push 후 몇십 초 뒤 반영된다. URL: `https://kil9.github.io/til/<slug>/`

## 명령어

빌드 단계는 없다. 정적 파일이 전부다.

```bash
# 로컬 미리보기 (루트에서 실행)
python3 -m http.server 8000
# → http://localhost:8000/ 및 http://localhost:8000/<slug>/

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
