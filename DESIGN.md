---
name: today i learned
description: 무채색 위 단 하나의 차가운 블루, 그림자 없이 1px 실선으로만 층을 나누는 자체 완결형 아카이브
colors:
  bg: "#FFFFFF"
  text: "#1B2027"
  text-muted: "#4E5A66"
  text-faint: "#6E7A86"
  rule: "#E3E7EB"
  box: "#F4F6F8"
  accent: "#1A5FC8"
  accent-strong: "#12459A"
  bg-dark: "#14171B"
  text-dark: "#E7EAEE"
  text-muted-dark: "#A9B3BD"
  text-faint-dark: "#7E8994"
  rule-dark: "#2A3037"
  box-dark: "#1C2127"
  accent-dark: "#82B1F0"
  accent-strong-dark: "#A9CBF7"
typography:
  display:
    fontFamily: "Pretendard, -apple-system, BlinkMacSystemFont, Apple SD Gothic Neo, Noto Sans KR, Malgun Gothic, system-ui, sans-serif"
    fontSize: "1.5rem"
    fontWeight: 700
    lineHeight: 1.6
    letterSpacing: "-0.01em"
  title:
    fontFamily: "Pretendard, -apple-system, BlinkMacSystemFont, Apple SD Gothic Neo, Noto Sans KR, Malgun Gothic, system-ui, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 600
    lineHeight: 1.5
    letterSpacing: "-0.005em"
  body:
    fontFamily: "Pretendard, -apple-system, BlinkMacSystemFont, Apple SD Gothic Neo, Noto Sans KR, Malgun Gothic, system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: "normal"
  secondary:
    fontFamily: "Pretendard, -apple-system, BlinkMacSystemFont, Apple SD Gothic Neo, Noto Sans KR, Malgun Gothic, system-ui, sans-serif"
    fontSize: "0.9375rem"
    fontWeight: 400
    lineHeight: 1.6
  caption:
    fontFamily: "Pretendard, -apple-system, BlinkMacSystemFont, Apple SD Gothic Neo, Noto Sans KR, Malgun Gothic, system-ui, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 500
    lineHeight: 1.6
  label:
    fontFamily: "Pretendard, -apple-system, BlinkMacSystemFont, Apple SD Gothic Neo, Noto Sans KR, Malgun Gothic, system-ui, sans-serif"
    fontSize: "0.75rem"
    fontWeight: 600
    lineHeight: 1.6
    letterSpacing: "0.08em"
  mono:
    fontFamily: "ui-monospace, SF Mono, monospace"
    fontSize: "0.8125rem"
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: "0.02em"
rounded:
  none: "0"
  md: "8px"
  full: "50%"
spacing:
  xs: "4px"
  sm: "8px"
  md: "12px"
  lg: "16px"
  xl: "24px"
  2xl: "32px"
  3xl: "48px"
  4xl: "64px"
  5xl: "80px"
components:
  card:
    textColor: "{colors.text}"
    typography: "{typography.title}"
    rounded: "{rounded.none}"
    width: "100%"
  card-hover:
    textColor: "{colors.accent}"
  card-date:
    textColor: "{colors.text-faint}"
    typography: "{typography.mono}"
  chip:
    backgroundColor: "transparent"
    textColor: "{colors.text-muted}"
    typography: "{typography.caption}"
    rounded: "{rounded.none}"
    padding: "2px 0"
  chip-active:
    backgroundColor: "transparent"
    textColor: "{colors.accent}"
  search-input:
    backgroundColor: "transparent"
    textColor: "{colors.text}"
    typography: "{typography.caption}"
    rounded: "{rounded.none}"
    padding: "4px 0"
    width: "320px"
  liv-note:
    backgroundColor: "{colors.box}"
    textColor: "{colors.text}"
    typography: "{typography.secondary}"
    rounded: "{rounded.md}"
    padding: "14px 16px"
  liv-avatar:
    backgroundColor: "{colors.bg}"
    rounded: "{rounded.full}"
    size: "28px"
  code-block:
    backgroundColor: "{colors.box}"
    textColor: "{colors.text}"
    typography: "{typography.mono}"
    rounded: "{rounded.md}"
    padding: "14px 16px"
  section-label:
    textColor: "{colors.text-faint}"
    typography: "{typography.label}"
---

# Design System: today i learned

## Overview

**Creative North Star: "The Hairline Archive"**

실선 한 겹으로 지은 아카이브다. 이 사이트에는 카드 테두리도, 그림자도, 배경 블록도 거의 없다. 무엇과
무엇이 다른 층인지는 오직 `1px` 헤어라인과 여백이 말한다. 종이 위에 인쇄된 목록에 가깝고, 화면에서
떠오르거나 눌리는 물체는 하나도 없다.

색은 사실상 무채색 한 벌뿐이고, 유채색은 차가운 블루 하나다. 그 블루는 장식이 아니라 **상태의 언어**다.
누를 수 있는 것, 지금 켜져 있는 것, 방금 검색어에 걸린 것에만 나타난다. 페이지 어디를 봐도 파란색이
보이지 않는다면 그 화면에는 상호작용할 것이 없다는 뜻이고, 그것이 의도한 결과다.

밀도는 편집물의 밀도다. 갤러리는 날짜·주제를 왼쪽 좁은 열에 monospace 로 세워 두고 제목을 오른쪽에
흘려 훑기 좋게 만들고, 아티클은 `720px` 한 단으로 좁혀 읽기에만 집중시킨다. 유일하게 톤이 풀어지는
자리가 리브의 코멘트 블록과 삽화·스티커인데, 이것들이 눈에 띄는 이유는 그 자체가 화려해서가 아니라
나머지가 전부 조용해서다.

**Key Characteristics:**

- 그림자 0개. 깊이는 `1px` 실선과 미묘한 톤 블록(`--box`)으로만 만든다.
- 액센트 블루는 링크·hover·focus·활성 상태 전용. 배경으로 칠하지 않는다.
- 웹폰트 없음. 시스템 스택과 `ui-monospace` 둘로만 위계를 낸다.
- 라이트/다크는 `prefers-color-scheme` 자동 전환뿐. 테마 토글 UI 가 없다.
- 각 페이지는 자체 완결형 단일 파일이라 이 토큰이 페이지마다 `:root` 에 복제된다.

## Colors

무채색은 살짝 푸른 기운이 도는 회색 계열로 통일돼 있고(순수 `#000`·순수 회색이 아니다), 유채색은
블루 하나뿐이다.

### Primary

- **Signal Blue** (`#1A5FC8` / 다크 `#82B1F0`): 이 시스템의 유일한 유채색. 본문 링크, 카드·목차·푸터
  링크의 hover, `:focus-visible` 아웃라인, 활성 주제 칩의 밑줄, 검색 하이라이트(`mark`), 브리핑
  미열람 표시 점. 면을 칠하는 데는 절대 쓰지 않는다.
- **Deep Signal Blue** (`#12459A` / 다크 `#A9CBF7`): 액센트의 강조 단계. 라이트에서는 더 진하게,
  다크에서는 더 밝게 간다 — 두 모드에서 방향이 반대라는 점이 중요하다.

### Neutral

- **Paper White** (`#FFFFFF` / 다크 **Ink Slate** `#14171B`): 페이지 바탕. 다크는 순흑이 아니라
  살짝 푸른 기가 도는 짙은 회색이다.
- **Ink** (`#1B2027` / 다크 `#E7EAEE`): 본문 텍스트와 제목.
- **Muted Ink** (`#4E5A66` / 다크 `#A9B3BD`): 부연 텍스트 — 카드 요약, lede, 사이트 소개, 표 헤더,
  기본 상태의 칩.
- **Faint Ink** (`#6E7A86` / 다크 `#7E8994`): 3차 텍스트 — 날짜, 태그, 대문자 섹션 라벨, figcaption,
  footer, 표 각주. 읽히되 먼저 읽히지 않아야 하는 것 전부.
- **Hairline** (`#E3E7EB` / 다크 `#2A3037`): 모든 구분선. `border-top`·`border-bottom`·`border-left`
  로만 쓰이고 사각 테두리를 두르는 데는 쓰지 않는다.
- **Quiet Box** (`#F4F6F8` / 다크 `#1C2127`): 바탕에서 아주 살짝 들린 면. 코드 블록과 리브 코멘트
  블록, 두 군데뿐이다.

### Named Rules

**The One Blue Rule.** 액센트는 화면의 10% 를 넘지 않고, 텍스트·선·아웃라인으로만 나타난다. 파란 배경
버튼이나 파란 배지를 만들지 않는다. 상호작용의 표시로만 쓰기 때문에 흔해지면 신호가 죽는다.

**The Cool Gray Rule.** 무채색에 따뜻한 기를 섞지 않는다. 모든 회색은 파란 쪽으로 살짝 기울어 있고,
새 회색이 필요하면 기존 6단(`bg`/`text`/`text-muted`/`text-faint`/`rule`/`box`) 중에서 고른다.
7번째 회색을 만들 이유는 거의 없다.

**The Two-Mode Parity Rule.** 새 색을 추가하면 라이트·다크 값을 같은 커밋에서 함께 정한다. 다크 값이
없는 색은 이 시스템에 존재할 수 없다 — 페이지에 테마 토글이 없어 사용자가 피해 갈 방법도 없다.

**The Foreign Logo Exception.** 남의 브랜드 로고는 그 브랜드의 색을 그대로 쓴다. 위 팔레트 규칙과
Two-Mode Parity 의 적용 대상이 아니다 — 로고의 색은 이 사이트가 정하는 값이 아니라 인용하는 값이고,
바꾸면 식별이라는 유일한 존재 이유가 사라진다. 지금 이 예외로 존재하는 색은 아침 브리핑 출처 배지
두 개뿐이다: GeekNews `#0000AA`, Hacker News `#FF6600`. One Blue Rule 과 충돌하지 않는다 — 그 규칙은
액센트 블루를 상호작용 표시로 묶는 것이고, 이 남색은 액센트가 아니라 인용된 상표다. 다크 모드에서는
색을 갈지 않고 `opacity` 로만 눌러 그 자리에서 튀지 않게 한다. 로고를 새로 들일 때는 원본을 그대로
쓰거나(파비콘의 픽셀 글리프처럼) 원본에 최대한 가깝게 그리고, 사이트 톤에 맞추려고 재색칠하지 않는다.

## Typography

**Body Font:** Pretendard (폴백 `-apple-system` → `BlinkMacSystemFont` → `Apple SD Gothic Neo` →
`Noto Sans KR` → `Malgun Gothic` → `system-ui` → `sans-serif`)
**Label/Mono Font:** `ui-monospace`, `SF Mono`, `monospace`

**Character:** 웹폰트를 한 벌도 싣지 않는다. Pretendard 가 설치돼 있으면 그것으로, 없으면 각 OS 의
한글 시스템 서체로 떨어진다 — 어느 쪽이든 무난하게 읽히는 것이 목표이고, 서체로 개성을 내려 하지
않는다. 개성은 monospace 를 쓰는 자리를 엄격히 제한하는 데서 나온다.

### Hierarchy

- **Display** (700, `1.5rem`, `-0.01em`): 페이지 제목과 사이트 제목. 페이지당 하나.
- **Title** (600, `1.0625rem`, line-height `1.5`, `-0.005em`): 아티클 `h2` 절 제목과 갤러리 카드 제목.
  본문(`16px`)과 크게 차이 나지 않는 것이 의도다 — 절 제목이 본문을 압도하지 않는다.
- **Body** (400, `16px`, line-height `1.6`): 본문. 아티클은 `720px` 한 단이라 한 줄이 대략 40-45 한글
  글자에서 끊긴다.
- **Secondary** (400, `0.9375rem`): 카드 요약, lede, 표 셀, 리브 코멘트, 사이트 소개. 본문보다 한 단계
  작고 대개 `text-muted` 와 함께 쓴다.
- **Caption** (500, `0.875rem`): 조작 요소와 보조 항목 — 주제 칩, 검색 입력, 목차 링크, 사이드바
  코멘트 본문. 누를 수 있는 작은 것들이 대체로 이 크기다.
- **Label** (600, `0.75rem`, `letter-spacing: 0.08em`, uppercase, `text-faint`): 사이드바 섹션 머리말
  (AI 코멘트, 브리핑, 월별 목차). 사이트에서 대문자를 쓰는 유일한 자리다.
- **Mono** (400, `0.8125rem`, `tabular-nums`): 날짜, 월별 목차 행, 코드, 인라인 `code`.

### Named Rules

**The Mono-For-Facts Rule.** monospace 는 **세로로 자리를 맞춰야 하는 값**에만 쓴다 — 날짜, 건수,
코드. 그 외 텍스트를 monospace 로 강조하지 않는다. 목차와 카드 날짜가 열을 이루는 인상이 이 규칙 하나에
전부 걸려 있고, `font-variant-numeric: tabular-nums` 가 그 짝이다.

**The Uppercase-Is-A-Label Rule.** 대문자 + `0.08em` 자간 + `0.75rem` + `text-faint` 는 통째로 하나의
의미다: "이 아래가 한 덩어리다". 이 조합을 강조나 제목에 전용하지 않는다.

**The Quiet Bold Rule.** 본문 안에서 굵게 강조하지 않는다. 위계는 크기·색·여백으로 이미 다 났다.

## Layout

컨테이너는 두 폭뿐이다. **아티클은 `max-width: 720px` 한 단**(`padding: 48px 24px 80px`), **갤러리·
아카이브는 `max-width: 1000px` 2단**(본문 `1fr` + 사이드바 `260px`, `column-gap: 40px`). 그 사이의
중간 폭을 새로 만들지 않는다.

세로 리듬은 4의 배수로 움직인다: 문단 사이 `12px`, 표·그림 `16-24px`, 절(`h2`) 위 `40px`, 큰 구분
`32px` 룰, footer 위 `64px`. 값이 헷갈리면 위아래로 가장 가까운 기존 값을 고르는 편이 새 값을 만드는
것보다 항상 낫다.

갤러리 카드는 `grid-template-columns: 8.75rem 1fr` 로 왼쪽에 날짜(1행)·태그(2행), 오른쪽에 제목(1행)·
요약(2행)을 놓는다. 카드끼리의 간격은 `28px` 이고 카드 사이에 선을 긋지 않는다 — 여백만으로 나눈다.

반응형 분기는 넷이다. **1200px 이상**: 아티클 목차가 본문 왼쪽 여백으로 빠져 sticky 레일이 된다
(본문 폭·위치는 그대로). **920px**: 갤러리가 1단이 되고 사이드바가 `order: -1` 로 목록 위에
올라가며, `border-left` 가 `border-bottom` 으로 바뀐다. **560px**: 카드가 블록이 되어 날짜·태그가
제목 위에 가로로 붙는다. **520px**: 스티커의 `float` 이 풀려 가운데 정렬 블록이 된다.

**The Two Widths Rule.** 읽는 화면은 720, 훑는 화면은 1000. 새 페이지를 만들 때 먼저 정할 것은
색이 아니라 이 페이지가 읽는 화면인지 훑는 화면인지다.

## Elevation & Depth

**그림자가 없다.** 사이트 전체(57페이지)에서 `box-shadow` 를 쓰는 곳은 자체 스타일을 가진 채로
이관된 초기 아티클 3개뿐이고, 공통 셸에는 한 줄도 없다. 깊이는 두 가지로만 낸다.

1. **헤어라인**(`1px solid var(--rule)`): 히어로 하단, 사이드바 좌측, 각 사이드바 섹션 상단, 표 행,
   footer 상단, 목차 상하, 하단 내비 상단. 항상 한 방향의 선이지 사각 테두리가 아니다.
2. **톤 블록**(`--box`): 바탕에서 한 단계만 들린 면. 코드 블록과 리브 코멘트 두 곳에만 허용된다.

### Named Rules

**The Flat Rule.** `box-shadow` 를 새로 도입하지 않는다. 어떤 요소를 띄우고 싶다면 그 자리에 필요한 건
그림자가 아니라 여백이거나 선이다.

**The Single Line Rule.** 구분은 한 방향 선 하나로 끝낸다. 위아래를 동시에 두르는 경우는 목차
(`.pagetoc`) 하나뿐이고, 그건 그 블록이 본문 흐름을 잠시 끊는다는 표시라서 예외다.

## Shapes

각진 것이 기본이다. 카드·칩·검색 입력·표에는 `border-radius` 가 없다(`0`). 곡률이 붙는 것은 셋뿐이다:
**`8px`** — 코드 블록, 리브 코멘트, 삽화 이미지. **`50%`** — 아바타(리브 28px·36px, 관리자 36px).
그 밖의 반경 값(`4px`·`10px`·`12px`)은 자체 스타일을 유지한 채 이관된 개별 아티클에만 남아 있고,
공통 셸에서는 쓰지 않는다.

테두리는 사각으로 두르지 않는다. `border` 는 언제나 한 변(`-top`/`-bottom`/`-left`)이다. 검색 입력이
그 태도를 가장 잘 보여 준다 — 상자가 아니라 밑줄 하나이고, 포커스되면 그 밑줄만 액센트로 바뀐다.

**The 8-or-Circle Rule.** 새 반경이 필요하면 `8px` 이거나 `50%` 다. 세 번째 값을 만들지 않는다.

## Components

### Cards (갤러리 항목)

- **성격:** 상자가 아니라 인쇄된 목록의 한 줄. 테두리·배경·그림자가 전부 없다.
- **Shape:** 반경 `0`, 테두리 없음. `grid` 2열(`8.75rem 1fr`), `column-gap: 20px`, 카드 간 `28px`.
- **Color:** 제목 `text`, 요약 `text-muted`, 날짜·태그 `text-faint`.
- **Hover:** 제목만 액센트로 바뀌고 `text-underline-offset: 3px` 밑줄이 붙는다. 카드 전체의 배경은
  변하지 않는다.
- **Focus:** `outline: 2px solid var(--accent); outline-offset: 4px` — 카드 전체를 감싼다.
- **검색 스니펫:** 3행에 `0.8125rem`/`text-faint` 로 붙고, 매치 어절은 `mark` 로 감싸되 배경을 없애고
  액센트 + `600` 으로만 표시한다(형광펜을 쓰지 않는다).

### Chips (주제 필터)

- **Style:** `<button>` 이지만 버튼처럼 보이지 않는다. 배경·테두리·반경 없음, `padding: 2px 0`,
  기본 `text-muted`.
- **State:** 활성이면 액센트 색 + `text-underline-offset: 6px`, `text-decoration-thickness: 2px` 밑줄.
  칩 사이 간격은 `4px 20px`(행 간격은 좁고 열 간격은 넓다).
- **제약:** 칩 라벨은 한 단어여야 한다 — 카드 `.tag` 를 `·` 로 잘라 첫 조각으로 자동 생성되기 때문이다.

### Inputs (검색)

- **Style:** 밑줄 하나(`border-bottom: 1px solid var(--rule)`). 배경·반경·좌우 패딩 없음,
  `max-width: 320px`, placeholder 는 `text-faint`.
- **Focus:** `outline: none` 을 주는 대신 밑줄 색을 액센트로 바꾼다 — 이 시스템에서 아웃라인을 지우는
  것이 허용되는 유일한 자리이고, 대체 표시가 명확하기 때문에 성립한다.

### Navigation (하단 이전/다음)

- **Style:** 상단 헤어라인 아래 `grid`, `gap: 10px`. 링크는 기본 `text` 색에 밑줄 없음.
- **Label:** `이전`/`다음` 라벨이 `min-width: 3em`, `0.75rem`, `letter-spacing: 0.06em`, `text-faint`
  로 앞에 붙어 열을 맞춘다.
- **Hover/Focus:** 액센트 + 밑줄. 그 아래 주제 역링크(`.pn-topic`)는 한 단계 더 옅다.
- **생성물이다.** `backlog/assets/relink-pages.py` 가 마커 구간에 써 넣으므로 손으로 고치지 않는다.

### 리브 코멘트 (`.liv`) — 시그니처 컴포넌트

이 시스템에서 유일하게 면을 가진 대화 블록이다. 화자(리브)의 목소리를 본문에서 분리한다.

- **Shape/Color:** `--box` 배경, 반경 `8px`, `padding: 14px 16px`, 세로 여백 `24px`, `0.9375rem`.
- **Layout:** 반드시 `grid; grid-template-columns: auto 1fr; gap: 10px; align-items: start`.
  **flex 로 짜면 문단이 둘 이상일 때 가로로 나열돼 2칼럼처럼 깨진다** — 실제로 그렇게 발행된 사고가 있다.
- **Avatar:** 28x28, `border-radius: 50%`, 배경 흰색(다크에서 원형 경계가 깨지지 않게), `margin-top: 2px`.
  표정 6종 중 그 문단의 정서에 맞는 것을 고르고 한 페이지에서 같은 표정을 반복하지 않는다.
- **금지:** 이름 라벨(`리브 —`)을 텍스트로 붙이지 않는다. 아바타가 화자를 나타낸다.

### 스티커 (`.sticker-inline`)

- **Style:** 문단 첫머리에 흘려 넣는 `float: right`, `shape-outside: margin-box`,
  `margin: 0 0 12px 20px`.
- **크기는 반드시 `height: 132px`** 로 잡는다(`width` 아님). 스티커마다 종횡비가 달라 `width` 로 주면
  높이가 제멋대로 치솟는다.
- **다크모드 필터를 걸지 않는다.** 흰 다이컷 링은 장식이 아니라 어두운 배경에서 캐릭터를 떼어내는
  기능이다. `brightness(0.9)` 를 걸면 링이 회색으로 떠서 오히려 눈에 걸린다.
- 520px 이하에서 `float` 을 풀고 가운데 블록으로 전환한다. 페이지당 1-2개.

### 삽화 (`figure.illust`)

- 폭 100%, 반경 `8px`, `figcaption` 은 `0.8125rem`/`text-faint`.
- 다크모드에서만 `filter: brightness(0.9)`(스티커와 반대다 — 삽화는 배경이 있는 그림이라 눌러 준다).

### 표 / 코드 블록

- **표:** `width: 100%`, `border-collapse: collapse`, 셀 `padding: 8px 10px`, 행마다 헤어라인
  `border-bottom`. 헤더는 `0.8125rem`/`600`/`text-muted`. 세로선을 긋지 않고 얼룩 배경(zebra)도 없다.
  수치 열은 `.num` 으로 우측 정렬 + `tabular-nums`.
- **코드:** `--box` 배경, 반경 `8px`, `padding: 14px 16px`, `0.8125rem`, `overflow-x: auto`.
  구문 강조(syntax highlighting)를 넣지 않는다.

### 목차 (`.pagetoc`) — 시그니처 컴포넌트

한 마크업이 폭에 따라 두 모습이 된다. **1200px 미만**: 첫 `h2` 앞 인라인 블록. 위아래 헤어라인을
두르는 시스템 내 유일한 요소이고(본문 흐름을 잠시 끊는다는 표시), 링크는 본문 색이다.
**1200px 이상**: 본문 왼쪽 여백으로 빠져 폭 `192px`·간격 `32px` 의 sticky 레일이 된다. 헤어라인과
"목차" 라벨이 사라지고 링크가 `0.8125rem`/`text-muted` 로 내려앉으며, 현재 읽는 절만 액센트가 된다.

- **`position: fixed` 를 쓰지 않는다.** `main` 을 좌표 기준으로 삼는 `absolute` 박스를 본문 높이만큼
  늘리고 그 안을 `sticky`(`top: 48px`)로 붙인다. fixed 는 본문이 끝난 뒤 footer·하단 내비 구간까지
  레일을 끌고 온다.
- **셀렉터는 `main > .pagetoc` 으로 한정한다.** `<main>` 이 없는 자체 스타일 페이지에서 `absolute`
  를 걸면 기준이 `body` 로 올라가 레일이 엉뚱한 자리에 뜬다. 그런 페이지는 인라인 목차로 남는다.
- **레일 링크에 `text-faint` 를 쓰지 않는다.** `0.8125rem` 에서 라이트 대비가 4.38:1 로 AA 에 못
  미친다. `text-muted`(7.05:1)가 조용한 톤을 유지하면서 기준을 넘는 최소 단계다.
- 생성물이다 — `backlog/assets/relink-pages.py` 의 `PAGETOC` 마커 구간을 손으로 고치지 않는다.

### 차트 (`figure.chart`)

인라인 SVG 로만 그린다. `fill`/`stroke` 에 페이지 CSS 변수(`var(--text)`, `var(--accent)`,
`var(--text-faint)`)를 써서 다크모드에 자동 대응시킨다. 외부 차트 라이브러리를 쓰지 않는다.

## Do's and Don'ts

### Do:

- **Do** 새 페이지의 `:root` 에 위 토큰을 라이트·다크 한 쌍으로 그대로 복제한다. 각 페이지가 자체
  완결형 단일 파일이라 공유 스타일시트가 없고, 복제가 이 시스템의 배포 방식이다.
- **Do** 상호작용 가능한 모든 요소에 `:focus-visible { outline: 2px solid var(--accent) }` 를 준다
  (`outline-offset` 은 카드·keeper 4px, 칩 2px, 아이콘 3px).
- **Do** 깊이가 필요하면 헤어라인이나 여백을 먼저 쓴다.
- **Do** 날짜·건수에 `font-variant-numeric: tabular-nums` 를 붙인다.
- **Do** 인라인 SVG 차트의 색을 CSS 변수로 묶어 다크모드에서 저절로 따라가게 한다.
- **Do** 삽화·스티커·아바타를 base64 `data:image/webp` 로 임베드하고 서술형 `alt` 를 단다.

### Don't:

- **Don't** `box-shadow` 를 새로 도입한다. 공통 셸에는 하나도 없고, 남아 있는 3개는 이관된 초기 페이지의
  잔재이지 따라야 할 선례가 아니다.
- **Don't** 액센트 블루로 면을 칠하거나(파란 버튼·파란 배지) 배경 하이라이트를 만든다. 액센트는 텍스트·
  선·아웃라인 전용이다.
- **Don't** `8px`·`50%` 외의 `border-radius` 를 새로 만든다.
- **Don't** 사각 테두리를 두른다. `border` 는 한 변만 쓴다.
- **Don't** 웹폰트를 링크하거나 `@font-face` 를 추가한다. CDN 스크립트·외부 이미지·외부 스타일시트도
  마찬가지다 — 허용된 외부 요청은 Cloudflare Web Analytics beacon 하나뿐이다.
- **Don't** 테마 토글 UI 를 만든다. `prefers-color-scheme` 이 유일한 신호이며, `data-theme` 속성에
  의존하는 스타일은 standalone 환경에서 죽는다.
- **Don't** `.liv` 를 flex 로 짠다(문단 둘 이상에서 레이아웃이 깨진다).
- **Don't** 스티커에 다크모드 필터를 걸거나 `width` 로 크기를 잡는다.
- **Don't** 스크립트가 소유한 마커 구간(`PAGEOG`·`PAGENAV`·`PAGETOC`)을 손으로 고친다.
