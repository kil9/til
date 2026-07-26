#!/usr/bin/env python3
"""루트 검색이 본문까지 보게 하는 정적 색인 search-index.json 을 굽는다(TASK-107).

루트 index.html 의 검색은 카드 텍스트(제목·설명·태그)와 href 슬러그만 본다. 50건이
넘으면 '그 글 어디 있었지' 가 본문 키워드로 기억되는 쪽이 많아 카드만으로는 못 찾는다.
그래서 각 페이지 본문을 긁어 슬러그 → 평문 한 덩어리로 만들어 두고, 검색창에 첫 글자가
들어올 때 지연 로딩해 매치에 얹는다.

- 대상은 갤러리 카드가 있는 페이지만이다. p/briefing/ 회차는 카드가 없어 자연히 빠진다
  (매일 늘고 noindex 라 색인만 부풀린다) — feed.xml·sitemap.xml 과 같은 기준이다.
- 코드 블록(<pre>/<code>)·script·style·base64 임베드는 제외한다. 검색어로 쓰이지 않는
  데다, 넣으면 색인이 본문보다 수십 배로 불어난다.
- 하단 이전/다음 내비(<nav>)와 footer 도 제외한다. 남의 글 제목이 섞이면 그 글이
  엉뚱한 검색어에 걸린다.
- 시각 함수를 쓰지 않아 재실행이 멱등이다(같은 입력 → 같은 파일).

사용법: repo 루트에서  python3 backlog/assets/search-index.py
"""

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sitelib import ROOT, by_date, gallery_cards  # noqa: E402

OUT = ROOT / "search-index.json"

# 색인은 검색창 첫 입력 때만 받아 가므로 초기 로딩과 무관하고, 한국어 평문이라 전송
# 구간에서 gzip 이 3분의 1 아래로 줄인다(51건 556KB → 210KB). 그래서 상한이 아니라
# 사고 감지용 임계다 — 코드 블록 제외가 깨져 base64 나 <pre> 가 섞여 들어가면 자리수가
# 바뀐다. 본문 증가만으로는 당장 안 걸린다(현재의 약 2배 여유).
SIZE_WARN_BYTES = 1024 * 1024

# 본문에서 통째로 걷어낼 요소. 검색어가 되지 않는 것(코드·스크립트)과 다른 글의
# 텍스트가 섞여 들어오는 것(하단 내비·footer)이다.
DROP_EL_RE = re.compile(
    r"<(script|style|pre|code|nav|footer)\b[^>]*>.*?</\1\s*>", re.S | re.I
)
# 상단 복귀 링크("← today i learned")는 전 페이지 공통이라 색인에서 뺀다.
HOME_TOP_RE = re.compile(r'<p class="home-top"[^>]*>.*?</p>', re.S | re.I)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
TAG_RE = re.compile(r"<[^>]+>", re.S)
MAIN_RE = re.compile(r"<main\b[^>]*>(.*)</main>", re.S | re.I)
BODY_RE = re.compile(r"<body\b[^>]*>(.*)</body>", re.S | re.I)
WS_RE = re.compile(r"\s+")


def body_text(page: Path) -> str:
    """페이지 HTML 에서 색인할 평문을 뽑는다."""
    raw = page.read_text(encoding="utf-8")
    m = MAIN_RE.search(raw) or BODY_RE.search(raw)
    text = m.group(1) if m else raw
    text = COMMENT_RE.sub(" ", text)
    text = HOME_TOP_RE.sub(" ", text)
    text = DROP_EL_RE.sub(" ", text)
    # 태그를 지우면 src="data:image/webp;base64,…" 같은 속성값도 함께 사라진다.
    text = TAG_RE.sub(" ", text)
    return WS_RE.sub(" ", html.unescape(text)).strip()


def main():
    index = {}
    empty = []
    for card in by_date(gallery_cards()):
        page = card.file
        if not page.exists():
            raise SystemExit(f"카드가 가리키는 페이지가 없다: {page}")
        text = body_text(page)
        if not text:
            empty.append(card.slug)
            continue
        index[card.slug] = text

    # 키 순서를 최신순으로 고정한다(카드 순서와 같아 diff 가 읽힌다).
    OUT.write_text(
        json.dumps(index, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    size = OUT.stat().st_size
    chars = sum(len(v) for v in index.values())
    print(f"색인 {len(index)}건 · 본문 {chars:,}자 · {OUT.name} {size / 1024:.1f}KB")
    if size > SIZE_WARN_BYTES:
        print(f"  ⚠ 색인 용량 경고 {size / 1024 / 1024:.2f}MB "
              f"(> {SIZE_WARN_BYTES // 1024 // 1024}MB) — 코드 블록·base64 제외가 "
              "깨졌는지 확인. 경고일 뿐 발행은 막지 않는다", file=sys.stderr)
    if empty:
        print(f"본문을 뽑지 못한 페이지 {len(empty)}건: {', '.join(empty)}",
              file=sys.stderr)


if __name__ == "__main__":
    main()
