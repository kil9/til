#!/usr/bin/env python3
"""feed.xml(Atom 1.0)·sitemap.xml·robots.txt 를 루트에 생성한다.

진실원본은 루트 index.html 의 갤러리 카드다. 카드에 없는 것은 사이트 밖으로
나가지 않는다 — 특히 p/briefing/ 은 카드가 없고 noindex, follow 로 나가므로
피드·sitemap 어디에도 실리지 않는다.

- 본문 전문을 싣지 않고 카드 설명을 summary 로 낸다. 페이지가 자체 완결형
  HTML(base64 삽화 포함)이라 본문 추출이 지저분하고 피드 용량도 커진다.
- 발행 시각은 data-date(KST 로컬시각)에 +09:00 을 붙여 쓴다.
- robots.txt 는 전체 허용 + Sitemap 줄. 브리핑을 Disallow 하지 않는다 —
  크롤러가 페이지를 못 읽으면 meta noindex 도 못 읽어 오히려 색인될 수 있다.
- 시각 함수를 쓰지 않으므로 두 번 돌려도 결과가 같다(멱등).

사용법: repo 루트에서  python3 backlog/assets/site-feed.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sitelib import ROOT, SITE, by_date, gallery_cards, xml_escape  # noqa: E402

TITLE = "today i learned"
SUBTITLE = "리브가 조사·정리해 올리는 아카이브."
AUTHOR = "리브"

# 카드가 없지만 사람이 도달해야 하는 공개 페이지. 관리자 제출 도구·브리핑은 뺀다.
EXTRA_SITEMAP_PATHS = ["/", "/p/archive/"]


def atom(cards):
    updated = cards[0].rfc3339
    out = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<feed xmlns="http://www.w3.org/2005/Atom">',
        f"  <title>{xml_escape(TITLE)}</title>",
        f"  <subtitle>{xml_escape(SUBTITLE)}</subtitle>",
        f'  <link rel="self" type="application/atom+xml" href="{SITE}/feed.xml"/>',
        f'  <link rel="alternate" type="text/html" href="{SITE}/"/>',
        f"  <id>{SITE}/</id>",
        f"  <updated>{updated}</updated>",
        f"  <author><name>{xml_escape(AUTHOR)}</name></author>",
    ]
    for c in cards:
        out += [
            "  <entry>",
            f"    <title>{xml_escape(c.title)}</title>",
            f'    <link rel="alternate" type="text/html" href="{c.url}"/>',
            f"    <id>{c.url}</id>",
            f"    <published>{c.rfc3339}</published>",
            f"    <updated>{c.rfc3339}</updated>",
            f'    <category term="{xml_escape(c.topic)}"/>',
            f'    <summary type="text">{xml_escape(c.summary)}</summary>',
            "  </entry>",
        ]
    out += ["</feed>", ""]
    return "\n".join(out)


def sitemap(cards):
    latest = cards[0].rfc3339
    out = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path in EXTRA_SITEMAP_PATHS:
        out += [
            "  <url>",
            f"    <loc>{SITE}{path}</loc>",
            f"    <lastmod>{latest}</lastmod>",
            "  </url>",
        ]
    for c in cards:
        out += [
            "  <url>",
            f"    <loc>{c.url}</loc>",
            f"    <lastmod>{c.rfc3339}</lastmod>",
            "  </url>",
        ]
    out += ["</urlset>", ""]
    return "\n".join(out)


def robots():
    return "\n".join([
        "User-agent: *",
        "Allow: /",
        "",
        f"Sitemap: {SITE}/sitemap.xml",
        "",
    ])


def main():
    cards = by_date(gallery_cards())
    for name, text in (
        ("feed.xml", atom(cards)),
        ("sitemap.xml", sitemap(cards)),
        ("robots.txt", robots()),
    ):
        out = ROOT / name
        before = out.read_text(encoding="utf-8") if out.exists() else None
        out.write_text(text, encoding="utf-8")
        state = "생성" if before is None else ("변경 없음" if before == text else "갱신")
        print(f"  {name:14s} {len(text.encode()) // 1024 or 1:3d}KB  {state}")
    print(f"카드 {len(cards)}건 (아티클 {sum(c.is_article for c in cards)}, "
          f"지원 페이지 {sum(not c.is_article for c in cards)}) · 브리핑 제외")


if __name__ == "__main__":
    main()
