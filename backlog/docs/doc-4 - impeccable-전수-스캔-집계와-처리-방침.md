---
id: doc-4
title: impeccable 전수 스캔 집계와 처리 방침
type: other
created_date: '2026-07-28 17:59'
---
# impeccable 전수 스캔 집계와 처리 방침

TASK-113 산출물. `npx impeccable detect` 로 `index.html`·`404.html`·`2026/`·`p/` 를 전수 스캔한
결과와, 각 규칙을 어떻게 처리하기로 했는지의 진실원본이다. 시각 규칙 자체의 정본은 루트
`DESIGN.md`(TASK-112), waive 목록의 정본은 `.impeccable/config.json`(커밋됨)이다.

## 1. 스캔 조건

- 대상 77 파일(카드 있는 페이지 + 브리핑 회차 + 갤러리 미링크 페이지 포함), 소요 약 9분.
- 실행 시점: 2026-07-28, DESIGN.md 작성 직후 waive 를 하나도 걸지 않은 상태.
- **아래 집계는 그 최초 스캔의 숫자다.** §3 의 수정·waive 를 반영한 재스캔은 돌리다 중단했으므로,
  전체 재집계가 필요하면 `npx impeccable detect --json index.html 404.html 2026/ p/` 를 다시 돌린다.
  개별 확인은 이미 했다 — 갤러리·공용 자산은 0건으로 통과한다(§4).

## 2. 규칙별 집계 (최초 스캔, 총 485건 / 77파일)

| 규칙 | 건수 | 파일 | 판정 |
|---|---:|---:|---|
| `design-system-radius` | 134 | 67 | 방치(이관 잔재) |
| `design-system-color` | 54 | 22 | 방치(이관 잔재) |
| `design-system-font-size` | 52 | 30 | 방치 + 갤러리 1건만 waive |
| `single-font` | 50 | 50 | 전역 waive(시스템 불변조건) |
| `gpt-thin-border-wide-shadow` | 41 | 10 | 방치(이관 잔재) |
| `low-contrast` | 37 | 10 | **수정** |
| `side-tab` | 35 | 16 | 방치(이관 잔재) |
| `tiny-text` | 28 | 6 | **수정 1파일** + 나머지 waive(SVG 라벨) |
| `em-dash-overuse` | 27 | 27 | 방치(advisory, §5) |
| `flat-type-hierarchy` | 15 | 15 | 전역 waive(시스템 불변조건) |
| `skipped-heading` | 9 | 9 | 방치 |
| `design-system-font` | 1 | 1 | 방치 |
| `all-caps-body` | 1 | 1 | waive(Label 역할) |
| `broken-image` | 1 | 1 | **수정** |

`design-system-*` 4종(총 241건, 전체의 절반)은 전부 DESIGN.md 램프 이탈이다. 이 사이트는 페이지마다
자체 완결형 HTML 이고 초기 글 상당수가 artifact 스타일을 그대로 가져왔으므로, 램프 이탈이 많은 것은
설계 결과이지 결함이 아니다. **이것이 발행물을 대량 리라이트하지 않기로 한 근거**다 — 대신 TASK-114
게이트가 신규 페이지 디렉터리만 보게 해서 새 글부터 DESIGN.md 를 따르게 한다.

## 3. 처리 방침 세 갈래

### 3-1. 수정 — 실해가 있는 것만

읽는 사람이 실제로 손해를 보는 것만 고쳤다. 그 외에는 손대지 않았다.

- **`low-contrast` 37건 / 10파일.**
  - `p/til-archive/index.html`: 다크 `--text-faint: #647178` 이 surface `#141D22` 위에서 3.4:1
    (WCAG AA 4.5:1 미달). `#828F98` 로 올려 세 배경(`#0D1316`/`#141D22`/`#1A252B`)에서 각각
    5.64 / 5.15 / 4.71:1 확보.
  - `2026/2026-07-plan-pipeline/*.html` 9파일: `--ink-3: #767d8c` 가 `#12151b` 위에서 4.42:1 로
    간발의 미달. `#7d8493`(4.87:1)로 올렸다. 한 값 치환이라 비용이 없다.
- **`tiny-text` 11.52px / `p/til-archive/index.html`.** `font-size: 0.72rem` 2곳을 `0.8125rem`(13px)
  으로. 같은 파일의 대비 수정과 함께 이 페이지만 실질 개선했다.
- **`broken-image` / `p/submit-96a2d1c7e19e8a09/index.html`.** `<img id="liv-sticker" src="">` 는
  JS 가 나중에 채우는 자리인데, 빈 `src` 는 브라우저가 문서 URL 로 요청을 보내 실패한다. 1x1 투명
  GIF data URI 를 placeholder 로 넣었다. **`src` 속성을 아예 빼면 규칙이 다시 걸린다**(빈 src 와
  누락 src 를 같이 잡는다) — 처음에 그렇게 고쳤다가 되돌렸다.
- **`design-system-radius` / `p/archive/index.html`.** 격자 커버 `10px` → `8px`. 갤러리 계열
  공용 자산이라 이관 잔재 취급하지 않고 DESIGN.md 스케일에 맞췄다.

### 3-2. waive — `.impeccable/config.json` (커밋됨)

waive 는 전부 이 한 파일에 모았다. 인라인 주석을 쓰지 않은 이유는 한 곳에서 검토 가능하게 두기
위해서다(발행물이 저장소를 떠나는 형태가 아니라 인라인의 이점이 없다).

| 항목 | 범위 | 이유 |
|---|---|---|
| `ignoreRules: single-font` | 전역 | 웹폰트를 싣지 않는 것이 확정 정책이다(DESIGN.md Don't). 50파일 전부에서 뜨는데 전부 의도다. |
| `ignoreRules: flat-type-hierarchy` | 전역 | 압축된 타입 스케일이 의도다 — 절 제목이 본문을 압도하지 않게 한 것(DESIGN.md Typography). |
| `design-system-font-size: 0.5rem` | `index.html` | 브리핑 미열람 표시 `●` 글리프 크기. 텍스트가 아니라 장식 기호다. |
| `tiny-text: *` | `2026/**/index.html` | 걸린 11px 이 전부 인라인 SVG 차트의 축·주석 라벨이다. 본문이 아니라 도표 안 글자라 오탐이다. |
| `all-caps-body: *` | `2026/opus5-skill-rework/index.html` | `.lbl`(0.6875rem uppercase)은 DESIGN.md 가 인정하는 Label 역할이다. |

**`design-system-*` 를 전역 waive 하지 않은 것이 중요하다.** 전역으로 끄면 TASK-114 게이트가
신규 페이지의 램프 이탈도 못 잡아 도입 목적이 사라진다. 기존 페이지는 게이트가 애초에 보지 않으므로
끌 이유도 없다.

### 3-3. 방치

`design-system-radius`·`design-system-color`·`design-system-font-size`(갤러리 1건 제외)·
`gpt-thin-border-wide-shadow`·`side-tab`·`skipped-heading`·`design-system-font`. 전부 개별 발행물의
이관 당시 스타일이고, 고치려면 페이지를 다시 쓰는 수준이 된다. 게이트가 신규 페이지만 보므로
발행을 막지 않는다. **다시 스캔하면 계속 뜨는 것이 정상이다.**

## 4. 갤러리·공용 자산 상태 (AC #2)

`npx impeccable detect index.html 404.html p/archive/` → **0 findings, exit 0.**

최초 스캔에서 이 셋에 있던 것은 넷뿐이었다: `index.html` 의 `0.5rem` 글리프(waive),
`404.html` 의 `flat-type-hierarchy`(전역 waive), `p/archive/` 의 `10px` radius(수정) 와
`single-font`/`flat-type-hierarchy`(전역 waive). 공용 자산은 애초에 거의 깨끗했다.

## 5. 남겨 둔 것 — em-dash

`em-dash-overuse` 가 27 페이지에서 뜬다. 이 저장소의 글쓰기 규칙은 **사외로 나가는 글에 em-dash 를
쓰지 않는 것**이므로 이 27건은 규칙 위반이 맞다. 그런데 고치려면 본문 산문을 27편 다시 쓰는 일이고,
그건 TASK-113 이 명시적으로 금지한 발행물 대량 리라이트다. advisory 라 exit code 에 안 들어가
발행도 막지 않는다.

그래서 **waive 하지 않고 그대로 뜨게 뒀다.** 규칙을 끄면 앞으로 쓰는 글에서도 안 뜨는데, 신규 글은
규칙을 지켜야 하므로 신호를 살려 두는 편이 낫다. 기존 27건은 알려진 부채로 여기 적어 둔다.

## 6. 재현

```bash
npx impeccable detect --json index.html 404.html 2026/ p/ > /tmp/scan.json   # 약 9분
npx impeccable detect index.html 404.html p/archive/                          # 공용 자산만, 수 초
npx impeccable ignores list                                                   # 현재 waive 목록
```
