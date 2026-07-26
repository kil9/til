#!/usr/bin/env python3
"""발행 전 사이트 전체 점검(TASK-109). 위반이 있으면 비영 종료코드로 끝난다.

페이지가 50건을 넘도록 발행 시 자동 점검이 하나도 없었다. 스킬의 til-preflight.sh·
til-verify.sh 는 둘 다 '지금 올리는 그 페이지 하나' 만 보므로, 사이트 전체를 보는
자리가 비어 있다 — 새 글이 직전 글의 링크를 바꾸고, 카드 하나가 404 맵에서 빠지고,
페이지가 조용히 비대해지는 것은 전부 전체를 봐야 잡힌다.

점검 항목:
  1. canonical  카드가 있는 페이지마다 rel=canonical 이 있고 값이 카드 경로와 같은가
  2. 링크       내부 링크(상대·루트절대)가 실제 파일을 가리키는가, 같은 페이지 앵커(#id)가 있는가
  3. 404 맵     루트 카드의 슬러그가 404.html 리다이렉트 맵에 등록됐는가
  4. 용량       HTML 이 상한(relink-pages.py 와 같은 5MB)을 넘는가
  5. 외부 링크  (선택) http(s) 링크가 살아 있는가 — 느려서 기본 실행에서는 뺀다

사용법:
    python3 backlog/assets/site-check.py             # 1~4 (1초 미만, 발행 경로용)
    python3 backlog/assets/site-check.py --external  # 외부 링크 생존까지(수 분)

1~4 는 파일만 읽어 1초 안에 끝난다. 5 는 외부 URL 230여 개를 순차로 두드려 7분쯤
걸리고(2026-07-27 실측) 남의 서버 사정에 흔들리므로 플래그로 분리했고, 결과도 위반이
아니라 경고다 — 실측에서 8건이 404·타임아웃이었는데 그걸로 발행이 막히면 곤란하다.
"""

import html
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sitelib import ROOT, SITE, gallery_cards  # noqa: E402

# relink-pages.py 의 SIZE_WARN_BYTES 와 같은 값(TASK-99). 그쪽은 발행 흐름에서 경고만
# 하고, 여기서는 같은 임계를 위반으로 세어 무인 발행도 걸리게 한다.
SIZE_LIMIT_BYTES = 5 * 1024 * 1024

# 스캔에서 뺄 경로. 사이트로 서빙되지 않거나(backlog·작업 공간), 자동 발행이라 자기
# 상한·검증을 따로 갖는 것(p/briefing/)이다.
SKIP_PREFIXES = ("backlog/", "topics/", "drafts/", "og/", ".git/")

CANONICAL_RE = re.compile(r'<link rel="canonical" href="([^"]*)"', re.I)
LINK_RE = re.compile(r'(?:href|src)="([^"]*)"', re.I)
ID_RE = re.compile(r'\sid="([^"]*)"')
MAP_ENTRY_RE = re.compile(r'"([^"]+)"\s*:\s*"([^"]*)"')
# 파일을 가리키지 않는 스킴. 프래그먼트("#…")는 아래에서 따로 본다.
NON_FILE_SCHEMES = ("mailto:", "tel:", "javascript:", "data:")
# 스크립트가 런타임에 조립하는 href("… <a href=\"' + SUBMIT_PAGE + '\">…")는 정적으로
# 판정할 수 없다. 작은따옴표·줄바꿈·템플릿 리터럴이 보이면 리터럴 링크가 아니다.
JS_EXPR_RE = re.compile(r"['\n]|\$\{")


def pages():
    """사이트로 서빙되는 HTML 페이지. 갤러리에 안 걸린 페이지도 포함한다."""
    for page in sorted(ROOT.rglob("*.html")):
        rel = page.relative_to(ROOT).as_posix()
        if rel.startswith(SKIP_PREFIXES):
            continue
        yield page


def check_canonical(cards, problems):
    for card in cards:
        page = card.file
        if not page.exists():
            problems.append(f"카드가 가리키는 페이지가 없다: {card.path}")
            continue
        found = CANONICAL_RE.search(page.read_text(encoding="utf-8"))
        if not found:
            problems.append(f"canonical 없음: {card.path}")
        elif found.group(1) != card.url:
            problems.append(
                f"canonical 불일치: {card.path} — 페이지 {found.group(1)} ≠ 카드 {card.url}"
            )


def resolve(page, target):
    """링크가 가리키는 파일 경로. 디렉터리면 index.html 로 내린다."""
    if target.startswith("/"):
        path = ROOT / target.lstrip("/")
    else:
        path = page.parent / target
    if target.endswith("/") or path.is_dir():
        path = path / "index.html"
    return path


def check_links(problems):
    """내부 링크와 같은 페이지 앵커. 외부·data:·mailto: 는 여기서 보지 않는다."""
    checked = 0
    for page in pages():
        text = page.read_text(encoding="utf-8")
        ids = set(ID_RE.findall(text))
        rel_page = page.relative_to(ROOT).as_posix()
        for raw in LINK_RE.findall(text):
            target = html.unescape(raw).strip()
            if not target or target.startswith(("http://", "https://", "//")) \
                    or target.startswith(NON_FILE_SCHEMES) \
                    or JS_EXPR_RE.search(target):
                continue
            if target.startswith("#"):
                anchor = urllib.parse.unquote(target[1:])
                # "#top" 은 요소가 없어도 문서 맨 위로 가는 HTML 표준 프래그먼트다.
                if anchor and anchor.lower() != "top" and anchor not in ids:
                    problems.append(f"페이지 안 앵커 대상 없음: {rel_page} → {target}")
                continue
            path_part = urllib.parse.unquote(target.split("#")[0].split("?")[0])
            if not path_part:
                continue
            checked += 1
            path = resolve(page, path_part)
            if not path.exists():
                problems.append(f"내부 링크 깨짐: {rel_page} → {target}")
            elif "#" in target:
                # 다른 페이지의 앵커까지 본다. 절 id 는 소급 생성물이라 틀어지기 쉽다.
                anchor = urllib.parse.unquote(target.split("#", 1)[1])
                if anchor and anchor.lower() != "top" and anchor not in set(
                        ID_RE.findall(path.read_text(encoding="utf-8"))):
                    problems.append(f"다른 페이지 앵커 대상 없음: {rel_page} → {target}")
    return checked


def check_404_map(cards, problems):
    """404.html 의 리다이렉트 맵은 구 평면 URL(/til/<slug>/)의 진실원본이다.
    신규 슬러그도 함께 등록해 두기로 했으므로(런북 §3) 누락을 여기서 잡는다."""
    text = (ROOT / "404.html").read_text(encoding="utf-8")
    mapped = dict(MAP_ENTRY_RE.findall(text))
    for card in cards:
        if card.slug not in mapped:
            problems.append(f"404 리다이렉트 맵에 없음: {card.slug}")
            continue
        want = card.path.strip("/")
        if mapped[card.slug].strip("/") != want:
            problems.append(
                f"404 맵 경로 불일치: {card.slug} — 맵 {mapped[card.slug]} ≠ 카드 {want}"
            )


def check_size(problems):
    biggest = (None, 0)
    for page in pages():
        size = page.stat().st_size
        if size > biggest[1]:
            biggest = (page, size)
        if size > SIZE_LIMIT_BYTES:
            problems.append(
                f"용량 초과: {page.relative_to(ROOT).as_posix()} "
                f"{size / 1024 / 1024:.1f}MB > {SIZE_LIMIT_BYTES // 1024 // 1024}MB"
            )
    return biggest


def probe(url, method, ua):
    """살아 있으면 None, 아니면 사유 문자열."""
    req = urllib.request.Request(url, method=method, headers={"User-Agent": ua})
    try:
        urllib.request.urlopen(req, timeout=15)
        return None
    except urllib.error.HTTPError as e:
        # 봇 차단·요청 제한은 페이지가 죽은 것이 아니다.
        return None if e.code in (403, 429) else str(e.code)
    except Exception as e:                      # noqa: BLE001 — 원인 이름만 쓴다
        return type(e).__name__


def check_external():
    """외부 링크 생존. 느린 데다 상대 서버 사정으로 흔들려서 기본 실행에서 뺐고,
    결과도 위반이 아니라 경고로 센다 — 남의 서버 때문에 내 발행이 막히면 안 된다."""
    urls = {}
    for page in pages():
        text = page.read_text(encoding="utf-8")
        for raw in LINK_RE.findall(text):
            target = html.unescape(raw).strip()
            if target.startswith(("http://", "https://")) and not target.startswith(SITE):
                urls.setdefault(target, page.relative_to(ROOT).as_posix())
    # 브라우저 UA 를 쓴다. 기본 urllib UA 는 문전에서 막혀 살아 있는 페이지가
    # 죽은 것으로 잡힌다.
    ua = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
          "Chrome/126.0 Safari/537.36")
    dead = []
    for url, where in sorted(urls.items()):
        why = probe(url, "HEAD", ua)
        # HEAD 를 제대로 처리하지 않는 서버가 흔하다(실측에서 aitimes·UBC 가 HEAD 에는
        # 404 를 주고 GET 에는 200 을 줬다). HEAD 가 실패하면 GET 으로 한 번 더 본다.
        if why:
            why = probe(url, "GET", ua)
        if why:
            dead.append((url, where, why))
    print(f"외부 링크 {len(urls)}개 확인 · 응답 없음 {len(dead)}건")
    for url, where, why in dead:
        print(f"  ⚠ {why}  {url}  ({where})", file=sys.stderr)


def main():
    cards = gallery_cards()
    problems = []
    check_canonical(cards, problems)
    links = check_links(problems)
    check_404_map(cards, problems)
    biggest = check_size(problems)

    page_count = sum(1 for _ in pages())
    print(f"페이지 {page_count} · 카드 {len(cards)} · 내부 링크 {links}개 확인 · "
          f"최대 {biggest[0].relative_to(ROOT).as_posix()} "
          f"{biggest[1] / 1024 / 1024:.2f}MB")

    if "--external" in sys.argv:
        check_external()

    if problems:
        print(f"\n위반 {len(problems)}건:", file=sys.stderr)
        for p in problems:
            print(f"  ✗ {p}", file=sys.stderr)
        return 1
    print("위반 없음")
    return 0


if __name__ == "__main__":
    sys.exit(main())
