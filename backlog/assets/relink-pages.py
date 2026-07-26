#!/usr/bin/env python3
"""페이지 공통 요소(하단 이전/다음·주제 역링크, og:image, 절 앵커·목차)를 소급 재생성한다.

페이지가 자체 완결형 HTML 이라 이런 요소를 각 파일에 박아야 한다. 진실원본은 루트
index.html 의 갤러리 카드이고, 이 스크립트가 카드를 읽어 각 페이지의 마커 구간을
다시 쓴다. 마커 밖은 건드리지 않으므로 반복 실행이 멱등이다.

마커는 다섯 구간이다.
    <!-- PAGEOG:START --> … <!-- PAGEOG:END -->              </head> 직전 (전 카드, canonical+og)
    <!-- PAGENAV-CSS:START --> … <!-- PAGENAV-CSS:END -->   </head> 직전 (아티클)
    <!-- PAGENAV:START --> … <!-- PAGENAV:END -->            <footer> 직전 (아티클)
    <!-- PAGETOC-CSS:START --> … <!-- PAGETOC-CSS:END -->    </head> 직전 (아티클)
    <!-- PAGETOC:START --> … <!-- PAGETOC:END -->            첫 <h2> 직전 (아티클, h2 5개 이상)

h2 의 id·앵커 링크(TASK-108)만은 마커 구간이 아니라 h2 태그 자체를 고친다. 대신 우리가
붙인 것에 data-anchor="auto" 를 표시해 두고 매번 그것만 다시 계산하므로 재실행이
멱등이고, 손으로 붙인 기존 id 9건은 표시가 없어 건드리지 않는다(그 값으로 나간 링크가
깨지면 안 된다). id 는 URL 에 박히므로 규칙을 바꾸면 되돌리기 어렵다.

og:image 파일 자체는 backlog/assets/archive-thumbs.py 가 굽는다. 그래서 발행 시
archive-thumbs.py 를 먼저 돌리고 이 스크립트를 나중에 돌린다 — 순서가 뒤집히면
새 글이 공통 폴백 이미지를 가리킨 채로 남는다.

- og:image 는 카드가 있는 페이지 전부에, 이전/다음 내비는 날짜 아티클에만 붙인다.
  p/ 지원 페이지는 발행 흐름 밖이라 순서에 낄 자리가 없고, 카드가 없는 페이지
  (갤러리 미링크)는 아예 대상이 아니다.
- 이전/다음은 발행순(data-date)이다. 이전 = 더 예전 글, 다음 = 더 최근 글.
  최신 글은 '다음'이, 가장 오래된 글은 '이전'이 자연히 빠진다.
- 새 글을 발행하면 직전 글의 '다음' 링크도 바뀌므로, 발행 때마다 이 스크립트를 돌려
  바뀐 파일을 전부 같은 커밋에 담는다.
- 끝에 페이지 용량 폭주 경고를 붙인다(TASK-99). 발행 경로에서 매번 도는 스크립트라
  따로 체커를 만들지 않고 여기에 얹었다.

사용법: repo 루트에서  python3 backlog/assets/relink-pages.py
"""

import html
import posixpath
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sitelib import ROOT, SITE, by_date, gallery_cards, xml_escape  # noqa: E402

CSS_MARK = ("<!-- PAGENAV-CSS:START -->", "<!-- PAGENAV-CSS:END -->")
NAV_MARK = ("<!-- PAGENAV:START -->", "<!-- PAGENAV:END -->")
OG_MARK = ("<!-- PAGEOG:START -->", "<!-- PAGEOG:END -->")
TOC_CSS_MARK = ("<!-- PAGETOC-CSS:START -->", "<!-- PAGETOC-CSS:END -->")
TOC_MARK = ("<!-- PAGETOC:START -->", "<!-- PAGETOC:END -->")

# 목차를 넣을 최소 h2 개수. 짧은 글에서는 목차가 소음이다.
TOC_MIN_HEADINGS = 5

OG_DIR = ROOT / "og"
OG_EXT = "jpg"           # archive-thumbs.py 와 맞춘다(크롤러 호환 때문에 JPEG)
OG_FALLBACK = "default"
OG_W, OG_H = 1200, 630

# 사고 감지용 느슨한 상한(TASK-99). 용량 절약이 목적이 아니다 — 용량 최적화는 하지
# 않기로 결정했고 base64 인라인도 그대로다. 목적은 '실수로 터진 페이지'를 발행 전에
# 알아차리는 것이다: WebP q75 압축을 건너뛴 원본 PNG 를 그대로 임베드했거나, 같은
# 이미지를 루프로 여러 번 박았거나, 삽화를 1440px 이 아닌 원해상도로 넣은 경우.
# 이런 것은 수 MB에서 수십 MB로 튄다. 현재 최대가 1.3MB 라 정상 발행은 절대 안 걸린다.
# 경고만 하고 막지 않는다 — 의도적으로 큰 페이지를 쓸 수 있어야 한다.
# 브리핑의 500KB 상한(TASK-95)과는 무관하다. 그쪽은 매일 자동 발행이라 성격이 다르다.
SIZE_WARN_BYTES = 5 * 1024 * 1024

# 페이지마다 CSS 변수 이름이 다를 수 있다(artifact 원본 스타일 유지 페이지). 공통 셸의
# 변수를 우선 쓰되 없으면 셸과 같은 값으로 폴백하고, 다크모드 폴백도 따로 준다.
PAGENAV_CSS = """<style>
  /* 하단 글 이동(TASK-98). backlog/assets/relink-pages.py 가 생성한다 — 손으로 고치지 말 것. */
  .pagenav {
    --pn-rule: var(--rule, #E3E7EB); --pn-faint: var(--text-faint, #6E7A86);
    --pn-accent: var(--accent, #1A5FC8); --pn-text: var(--text, #1B2027);
    margin: 56px 0 0; padding-top: 20px; border-top: 1px solid var(--pn-rule);
    display: grid; gap: 10px;
  }
  @media (prefers-color-scheme: dark) {
    .pagenav {
      --pn-rule: var(--rule, #2A3037); --pn-faint: var(--text-faint, #7E8994);
      --pn-accent: var(--accent, #82B1F0); --pn-text: var(--text, #E7EAEE);
    }
  }
  .pagenav a { color: var(--pn-text); text-decoration: none; font-size: 0.9375rem; }
  .pagenav a:hover, .pagenav a:focus-visible {
    color: var(--pn-accent); text-decoration: underline; text-underline-offset: 3px;
  }
  .pagenav .pn-label {
    display: inline-block; min-width: 3em; margin-right: 6px;
    color: var(--pn-faint); font-size: 0.75rem; letter-spacing: 0.06em;
  }
  .pagenav .pn-topic { margin: 6px 0 0; font-size: 0.8125rem; }
  .pagenav .pn-topic a { color: var(--pn-faint); font-size: inherit; }
</style>"""


PAGETOC_CSS = """<style>
  /* 절 앵커·목차(TASK-108). backlog/assets/relink-pages.py 가 생성한다 — 손으로 고치지 말 것. */
  .h-anchor {
    margin-left: 0.35em; font-weight: 400; text-decoration: none;
    color: var(--text-faint, #6E7A86); opacity: 0; transition: opacity 0.12s;
  }
  h2:hover > .h-anchor, .h-anchor:focus-visible { opacity: 1; }
  /* 터치 기기는 hover 가 없어 영영 안 보인다 — 옅게라도 늘 띄운다. */
  @media (hover: none) { .h-anchor { opacity: 0.4; } }
  .pagetoc {
    --tc-rule: var(--rule, #E3E7EB); --tc-faint: var(--text-faint, #6E7A86);
    --tc-accent: var(--accent, #1A5FC8); --tc-text: var(--text, #1B2027);
    margin: 28px 0 36px; padding: 14px 0; border-top: 1px solid var(--tc-rule);
    border-bottom: 1px solid var(--tc-rule);
  }
  @media (prefers-color-scheme: dark) {
    .pagetoc {
      --tc-rule: var(--rule, #2A3037); --tc-faint: var(--text-faint, #7E8994);
      --tc-accent: var(--accent, #82B1F0); --tc-text: var(--text, #E7EAEE);
    }
  }
  .pagetoc-label {
    margin: 0 0 8px; color: var(--tc-faint);
    font-size: 0.75rem; letter-spacing: 0.06em;
  }
  .pagetoc ol {
    margin: 0; padding: 0; list-style: none;
    display: grid; gap: 4px;
  }
  .pagetoc a { color: var(--tc-text); text-decoration: none; font-size: 0.875rem; }
  .pagetoc a:hover, .pagetoc a:focus-visible {
    color: var(--tc-accent); text-decoration: underline; text-underline-offset: 3px;
  }
</style>"""

# 본문 범위. h2 를 고칠 때 head·footer·하단 내비에 손대지 않기 위한 울타리다.
MAIN_RE = re.compile(r"(<main\b[^>]*>)(.*)(</main>)", re.S | re.I)
BODY_RE = re.compile(r"(<body\b[^>]*>)(.*)(</body>)", re.S | re.I)
H2_RE = re.compile(r"<h2\b([^>]*)>(.*?)</h2>", re.S | re.I)
H2_ANCHOR_RE = re.compile(r'\s*<a class="h-anchor"[^>]*>.*?</a>', re.S)
ID_ATTR_RE = re.compile(r'\sid="([^"]*)"')
AUTO_ATTR_RE = re.compile(r'\sdata-anchor="auto"')
# 제목 앞머리의 번호는 목차 표시에는 남기고 id 에서만 뺀다. 장식 span 판본과 본문에
# 그냥 적힌 "3. " 판본이 둘 다 있다. 번호를 id 에 넣으면 절을 하나 끼워 넣는 순간 그
# 아래 모든 절의 id 가 밀려 기존 링크가 통째로 깨진다.
NUM_SPAN_RE = re.compile(r'^\s*<span class="n">[^<]*</span>', re.I)
NUM_PREFIX_RE = re.compile(r"^\d+(?:[.-]\d+)*[.)]?\s+")
TAG_RE = re.compile(r"<[^>]+>", re.S)
WS_RE = re.compile(r"\s+")


def relative(from_path, to_path):
    """사이트 절대 경로끼리의 상대 링크. "/2026/a/" → "/2026/b/" = "../b/" """
    rel = posixpath.relpath(to_path, from_path)
    return rel if rel.endswith("/") else rel + "/"


def chip(card):
    """칩 라벨. `.tag` 의 "·" 앞 첫 세그먼트(루트 index.html 의 칩 생성과 같은 규칙)."""
    return card.tag.split("·")[0].strip() or card.topic


def nav_html(card, prev_card, next_card):
    rows = []
    for label, target in (("이전", prev_card), ("다음", next_card)):
        if target is None:
            continue
        href = relative(card.path, target.path)
        rows.append(
            f'  <a href="{href}"><span class="pn-label">{label}</span>'
            f"{xml_escape(target.title)}</a>"
        )
    topic_href = relative(card.path, "/") + f"?topic={card.topic}"
    rows.append(
        f'  <p class="pn-topic"><a href="{topic_href}">'
        f"{xml_escape(chip(card))} 글 더 보기 →</a></p>"
    )
    return '<nav class="pagenav" aria-label="글 이동">\n' + "\n".join(rows) + "\n</nav>"


def head_meta_html(card):
    """크롤러가 보는 절대 URL 메타. canonical 과 og:image 둘 다 상대 경로도 data: URI 도
    못 쓴다. 대표 이미지가 없으면 사이트 공통 폴백을 쓴다.

    canonical 은 구 평면 URL(`/til/<slug>/`)·쿼리 붙은 딥링크(`?topic=…`)가 같은 글의
    다른 주소로 색인되는 것을 막는다(TASK-109). 진실원본은 루트 카드의 href 다."""
    name = card.slug if (OG_DIR / f"{card.slug}.{OG_EXT}").exists() else OG_FALLBACK
    url = f"{SITE}/og/{name}.{OG_EXT}"
    return "\n".join([
        f'<link rel="canonical" href="{card.url}">',
        f'<meta property="og:image" content="{url}">',
        f'<meta property="og:image:width" content="{OG_W}">',
        f'<meta property="og:image:height" content="{OG_H}">',
        f'<meta property="og:image:alt" content="{xml_escape(card.title)}">',
    ])


def upgrade_twitter_card(text):
    """OG 이미지가 생겼으니 카드 종류를 큰 이미지로 올린다(마커 밖이라 직접 치환)."""
    return re.sub(
        r'(<meta name="twitter:card" content=")summary(">)',
        r"\1summary_large_image\2", text, count=1,
    )


def plain(fragment):
    """마크업을 걷어낸 제목 텍스트. 태그 자리는 공백으로 두어 <span>3</span>제목 이
    "3제목" 으로 붙지 않게 한다."""
    return WS_RE.sub(" ", html.unescape(TAG_RE.sub(" ", fragment))).strip()


def slugify(text):
    """한글을 그대로 둔 슬러그. 주소창에서는 퍼센트 인코딩되지만 붙여넣으면 복원되고,
    링크만 봐도 어디로 가는지 읽힌다. h2 순번(sec-N)은 절을 넣고 빼면 기존 링크가
    다른 절을 가리켜 쓰지 않는다."""
    s = re.sub(r"[^\w\s-]", "", text.strip().lower(), flags=re.U)
    return re.sub(r"[\s_-]+", "-", s).strip("-")


def rewrite_headings(text):
    """본문 h2 에 id 와 앵커 링크를 붙이고 목차 항목을 돌려준다.

    - 이미 id 가 있고 우리가 붙인 것(data-anchor="auto")이 아니면 그 id 를 그대로 쓴다.
    - 우리가 붙인 id 는 매번 제목에서 다시 계산한다(제목을 고치면 따라온다).
    - 같은 제목이 둘 이상이면 뒤에 -2, -3 을 붙인다.
    """
    m = MAIN_RE.search(text) or BODY_RE.search(text)
    if not m:
        return text, []
    used, entries = set(), []

    def repl(h2):
        attrs, inner = h2.group(1), h2.group(2)
        inner = H2_ANCHOR_RE.sub("", inner)
        label = plain(inner)
        manual = ID_ATTR_RE.search(attrs)
        if manual and not AUTO_ATTR_RE.search(attrs):
            hid = manual.group(1)
            new_attrs = attrs
        else:
            raw = NUM_PREFIX_RE.sub("", plain(NUM_SPAN_RE.sub("", inner)))
            base = slugify(raw) or f"h2-{len(entries) + 1}"
            hid, n = base, 1
            while hid in used:
                n += 1
                hid = f"{base}-{n}"
            new_attrs = AUTO_ATTR_RE.sub("", ID_ATTR_RE.sub("", attrs))
            new_attrs = f'{new_attrs.rstrip()} id="{hid}" data-anchor="auto"'
        used.add(hid)
        entries.append((hid, label))
        anchor = (f'<a class="h-anchor" href="#{hid}" aria-label="이 절 링크"'
                  ' title="이 절 링크">#</a>')
        return f"<h2{new_attrs}>{inner}{anchor}</h2>"

    body = H2_RE.sub(repl, m.group(2))
    return text[: m.start(2)] + body + text[m.end(2):], entries


def toc_html(entries):
    items = "\n".join(
        f'    <li><a href="#{hid}">{xml_escape(label)}</a></li>'
        for hid, label in entries
    )
    return ('<nav class="pagetoc" aria-label="목차">\n'
            '  <p class="pagetoc-label">목차</p>\n  <ol>\n'
            + items + "\n  </ol>\n</nav>")


def unsplice(text, marks):
    """마커 구간을 통째로 걷어낸다(목차 임계 미달로 내려가는 경우)."""
    start, end = marks
    pattern = re.compile(r"[ \t]*" + re.escape(start) + r".*?" + re.escape(end) + r"\n?",
                         re.S)
    return pattern.sub("", text, count=1)


def splice(text, marks, payload, anchor):
    """마커 구간을 payload 로 갈아끼운다. 구간이 없으면 anchor 정규식 앞에 새로 넣는다."""
    start, end = marks
    block = f"{start}\n{payload}\n{end}"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if pattern.search(text):
        return pattern.sub(lambda _: block, text, count=1)
    m = re.search(anchor, text)
    if not m:
        raise SystemExit(f"삽입 위치({anchor})를 찾지 못했다")
    indent = re.match(r"[ \t]*", text[text.rfind("\n", 0, m.start()) + 1:]).group(0)
    return text[: m.start()] + block + "\n" + indent + text[m.start():]


def size_check_pages():
    """용량 검사 대상: 손으로 발행하는 모든 페이지. 카드 없는 미링크 페이지도 포함한다
    (사고는 갤러리 등재 여부와 무관하다). p/briefing/ 은 자동 발행이고 자기 상한
    500KB 를 잡에서 따로 보므로 뺀다."""
    for page in sorted(ROOT.rglob("index.html")):
        rel = page.relative_to(ROOT).as_posix()
        if rel.startswith(("backlog/", "p/briefing/", "topics/", "drafts/")):
            continue
        yield page


def warn_oversize():
    limit_mb = SIZE_WARN_BYTES // 1024 // 1024
    pages = [(p, p.stat().st_size) for p in size_check_pages()]
    over = [(p, n) for p, n in pages if n > SIZE_WARN_BYTES]
    for page, size in over:
        print(f"  ⚠ 용량 경고 {page.parent.name}: {size / 1024 / 1024:.1f}MB "
              f"(> {limit_mb}MB) — 압축을 건너뛴 임베드나 같은 이미지 중복 임베드가 "
              "없는지 확인. 경고일 뿐 발행은 막지 않는다", file=sys.stderr)
    biggest = max(pages, key=lambda x: x[1])
    print(f"용량 경고 {len(over)}건 / {len(pages)}페이지 (임계 {limit_mb}MB, 최대 "
          f"{biggest[0].parent.name} {biggest[1] / 1024 / 1024:.2f}MB)")


def main():
    cards = by_date(gallery_cards())
    articles = [c for c in cards if c.is_article]
    order = {c.slug: i for i, c in enumerate(articles)}
    changed, fallback_og = [], []
    for card in cards:
        page = card.file
        if not page.exists():
            raise SystemExit(f"카드가 가리키는 페이지가 없다: {page}")
        before = page.read_text(encoding="utf-8")

        # canonical·OG 는 카드가 있는 페이지 전부(아티클 + p/ 지원 페이지)에 붙인다.
        after = splice(before, OG_MARK, head_meta_html(card), r"</head>")
        after = upgrade_twitter_card(after)
        if not (OG_DIR / f"{card.slug}.{OG_EXT}").exists():
            fallback_og.append(card.slug)

        # 이전/다음은 발행 흐름 안에 있는 날짜 아티클만. by_date 가 최신순이라
        # i-1 이 더 최근(다음), i+1 이 더 예전(이전)이다.
        if card.is_article:
            i = order[card.slug]
            nxt = articles[i - 1] if i > 0 else None
            prv = articles[i + 1] if i + 1 < len(articles) else None
            after = splice(after, CSS_MARK, PAGENAV_CSS, r"</head>")
            after = splice(after, NAV_MARK, nav_html(card, prv, nxt), r"<footer\b")

            # 절 앵커·목차(TASK-108). h2 를 먼저 고쳐야 목차가 가리킬 id 가 정해진다.
            after, entries = rewrite_headings(after)
            if entries:
                after = splice(after, TOC_CSS_MARK, PAGETOC_CSS, r"</head>")
            if len(entries) >= TOC_MIN_HEADINGS:
                after = splice(after, TOC_MARK, toc_html(entries), r"<h2[\s>]")
            else:
                after = unsplice(after, TOC_MARK)

        if after != before:
            page.write_text(after, encoding="utf-8")
            changed.append(card.slug)

    print(f"카드 {len(cards)}건(아티클 {len(articles)}) · 갱신 {len(changed)}건"
          + (f": {', '.join(changed)}" if changed else " (변경 없음)"))
    print(f"OG 공통 폴백 사용 {len(fallback_og)}건: {', '.join(fallback_og) or '-'}")
    warn_oversize()


if __name__ == "__main__":
    main()
