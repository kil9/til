#!/usr/bin/env python3
"""루트 index.html 갤러리 카드 파서 — 사이트 메타데이터의 단일 진실원본.

feed/sitemap 생성(site-feed.py)과 아티클 후처리(relink-pages.py)가 같은 카드를
읽어야 하므로 파싱을 여기 한 곳에 둔다. 카드 마크업이 바뀌면 이 파일만 고친다.

카드 형태:
    <a class="card" href="./2026/<slug>/" data-date="YYYY-MM-DDTHH:MM" data-topic="<키>">
      <div class="meta">
        <span class="date">...</span>
        <span class="tag">칩 · 세부</span>
      </div>
      <h2>제목</h2>
      <p>설명</p>
      <div class="path">/<slug>/</div>
    </a>
"""

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = "https://til.kil9.dev"
KST = "+09:00"

# 속성 순서·개수를 고정하지 않는다. 고정하면 카드에 속성이 하나만 늘어도(문서화된
# data-thumb 훅 등) 그 글이 피드·sitemap·내비·og:image 에서 통째로, 그것도 무증상으로
# 빠진다. 여는 태그를 통으로 잡고 속성은 따로 뽑은 뒤, 아래 gallery_cards 에서
# 여는 태그 개수와 파싱 건수를 대조해 조용한 누락을 막는다.
CARD_OPEN_RE = re.compile(r'<a class="card"\s([^>]*)>(.*?)</a>', re.S)
CARD_TAG_RE = re.compile(r'<a class="card"[\s>]')
ATTR_RE = re.compile(r'([a-zA-Z][\w-]*)="([^"]*)"')
REQUIRED_ATTRS = ("href", "data-date", "data-topic")


class Card:
    __slots__ = ("href", "date", "topic", "title", "summary", "tag")

    def __init__(self, href, date, topic, title, summary, tag):
        self.href = href          # "./2026/<slug>/"
        self.date = date          # "YYYY-MM-DDTHH:MM"
        self.topic = topic        # "ai"
        self.title = title
        self.summary = summary
        self.tag = tag            # "AI · Human-in-the-Loop"

    @property
    def path(self):
        """사이트 루트 기준 절대 경로. "/2026/<slug>/" """
        return "/" + self.href.lstrip("./")

    @property
    def slug(self):
        return self.href.rstrip("/").split("/")[-1]

    @property
    def url(self):
        return SITE + self.path

    @property
    def file(self):
        return ROOT / self.href.lstrip("./") / "index.html"

    @property
    def rfc3339(self):
        """data-date(분 단위, KST 로컬시각)를 RFC3339 로. Atom·sitemap 공용."""
        return f"{self.date}:00{KST}"

    @property
    def is_article(self):
        """날짜 아티클(<YYYY>/<slug>/)인지. 아니면 p/ 지원 페이지."""
        return not self.path.startswith("/p/")


def gallery_cards(index_html=None):
    """루트 index.html 의 카드를 마크업 등장 순서대로 돌려준다(정렬하지 않는다)."""
    text = (index_html or (ROOT / "index.html")).read_text(encoding="utf-8") \
        if not isinstance(index_html, str) else index_html
    cards = []
    for attrs_src, body in CARD_OPEN_RE.findall(text):
        attrs = dict(ATTR_RE.findall(attrs_src))
        missing = [a for a in REQUIRED_ATTRS if not attrs.get(a)]
        if missing:
            raise SystemExit(
                f"갤러리 카드에 필수 속성이 없다({', '.join(missing)}): <a class=\"card\" {attrs_src}>"
            )
        title = _text(body, r"<h2>(.*?)</h2>")
        summary = _text(body, r"<p>(.*?)</p>")
        tag = _text(body, r'<span class="tag">(.*?)</span>')
        cards.append(Card(attrs["href"], attrs["data-date"], attrs["data-topic"],
                          title, summary, tag))
    # 여는 태그 수와 대조해 조용한 누락을 잡는다. 여기서 죽는 편이 생성물에서
    # 글 하나가 아무 말 없이 빠지는 것보다 낫다.
    seen = len(CARD_TAG_RE.findall(text))
    if len(cards) != seen:
        raise SystemExit(
            f"갤러리 카드 파싱 누락: 여는 태그 {seen}개 중 {len(cards)}개만 읽었다. "
            "카드 마크업이 바뀌었는지 확인하라(backlog/assets/sitelib.py)"
        )
    if not cards:
        raise SystemExit("루트 index.html 에서 갤러리 카드를 하나도 찾지 못했다")
    return cards


def by_date(cards):
    """발행 최신순(내림차순). 동일 시각은 마크업 순서를 유지한다."""
    return sorted(cards, key=lambda c: c.date, reverse=True)


def _text(body, pattern):
    m = re.search(pattern, body, re.S)
    if not m:
        return ""
    return html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()


def xml_escape(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))
