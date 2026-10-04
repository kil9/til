#!/usr/bin/env python3
"""리브의 산책 노트 — 덧붙이기·발췌·렌더·검증 (task-131, 설계 doc-5).

원본은 backlog/assets/liv-notes/notes.jsonl 한 파일이고 덧붙이기만 한다. 글쓰기·산책
경로는 노트를 통째로 읽지 않고 이 도구의 excerpt 출력만 프롬프트로 받는다(task-123 의
경량화 원칙). 공개 페이지 p/liv-walk/ 는 render 의 생성물이다.

사용법(repo 루트에서):
  python3 backlog/assets/liv-notes.py add --kind saw --text "..." --tags a,b \\
      [--origin walk] [--source-title T --source-url U] [--supersedes n-0003] [--date D]
  python3 backlog/assets/liv-notes.py excerpt --for write --topic "제목이나 요청 원문"
  python3 backlog/assets/liv-notes.py excerpt --for walk
  python3 backlog/assets/liv-notes.py render
  python3 backlog/assets/liv-notes.py check

--notes·--out 으로 경로를 바꿀 수 있다(테스트·전용 클론용).
"""

import argparse
import html
import json
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
NOTES = ROOT / "backlog" / "assets" / "liv-notes" / "notes.jsonl"
PAGE = ROOT / "p" / "liv-walk" / "index.html"
KST = timezone(timedelta(hours=9))

KINDS = {
    "like": "좋아하게 된 것",
    "dislike": "별로인 것",
    "into": "요즘 꽂힌 것",
    "saw": "구경한 것",
    "talk": "관리자님과 나눈 얘기",
    "changed": "생각이 바뀐 것",
}
ORIGINS = ("seed", "walk", "talk", "publish")
ID_RE = re.compile(r"^n-(\d{4,})$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TOKEN_RE = re.compile(r"[0-9A-Za-z가-힣][0-9A-Za-z가-힣.+#-]+")

MAX_CHARS = 2400


def today():
    return datetime.now(KST).date().isoformat()


def load(path):
    if not path.exists():
        return []
    out = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise SystemExit(f"{path}:{n}: JSON 이 아니다 — {e}")
    return out


def validate(notes):
    """위반 문장 목록. 비어 있으면 통과."""
    errs, seen = [], set()
    for i, n in enumerate(notes, 1):
        where = f"{i}행({n.get('id', '?')})"
        for f in ("id", "date", "kind", "text", "tags", "origin"):
            if not n.get(f):
                errs.append(f"{where}: {f} 가 비었다")
        if not ID_RE.match(str(n.get("id", ""))):
            errs.append(f"{where}: id 형식은 n-0001")
        if n.get("id") in seen:
            errs.append(f"{where}: id 중복")
        seen.add(n.get("id"))
        if not DATE_RE.match(str(n.get("date", ""))):
            errs.append(f"{where}: date 형식은 YYYY-MM-DD")
        if n.get("kind") not in KINDS:
            errs.append(f"{where}: kind 는 {'/'.join(KINDS)} 중 하나")
        if n.get("origin") not in ORIGINS:
            errs.append(f"{where}: origin 은 {'/'.join(ORIGINS)} 중 하나")
        if not isinstance(n.get("tags"), list) or not 1 <= len(n.get("tags") or []) <= 5:
            errs.append(f"{where}: tags 는 1-5개 목록")
        src = n.get("source")
        if src is not None and not (isinstance(src, dict) and src.get("title")):
            errs.append(f"{where}: source 는 title(필수)·url 을 가진 객체")
        sup = n.get("supersedes")
        if sup and sup not in seen:
            errs.append(f"{where}: supersedes 는 앞에 나온 id 여야 한다 ({sup})")
        if n.get("kind") == "changed" and not sup:
            errs.append(f"{where}: changed 는 supersedes 가 필요하다")
    return errs


def next_id(notes):
    nums = [int(m.group(1)) for n in notes if (m := ID_RE.match(n.get("id", "")))]
    return f"n-{(max(nums) + 1 if nums else 1):04d}"


def cmd_add(a):
    notes = load(a.notes)
    note = {
        "id": next_id(notes),
        "date": a.date or today(),
        "kind": a.kind,
        "text": a.text.strip(),
        "tags": [t.strip().lower() for t in a.tags.split(",") if t.strip()],
        "origin": a.origin,
    }
    if a.source_title:
        note["source"] = {"title": a.source_title, "url": a.source_url or ""}
    if a.supersedes:
        note["supersedes"] = a.supersedes
    errs = validate(notes + [note])
    if errs:
        raise SystemExit("추가 거부:\n  " + "\n  ".join(errs))
    a.notes.parent.mkdir(parents=True, exist_ok=True)
    with a.notes.open("a", encoding="utf-8") as f:
        f.write(json.dumps(note, ensure_ascii=False) + "\n")
    print(note["id"])


# ── 발췌 ────────────────────────────────────────────────────────────────

def superseded(notes):
    return {n["supersedes"] for n in notes if n.get("supersedes")}


def within(n, days, ref):
    return date.fromisoformat(n["date"]) >= ref - timedelta(days=days)


def tokens(s):
    return {t.lower() for t in TOKEN_RE.findall(s or "")}


def place(url):
    """'이미 간 곳' 의 단위. 보통은 도메인이지만 위키백과는 문서마다 다른 곳이라 경로까지 본다."""
    u = urlparse(url)
    return u.netloc + u.path if u.netloc.endswith("wikipedia.org") else u.netloc


def line(n):
    s = f"- ({n['date']}, {KINDS[n['kind']]}) {n['text']}"
    if n.get("source"):
        s += f" — {n['source']['title']}"
    return s


def excerpt(notes, mode, topic="", ref=None, max_chars=MAX_CHARS):
    ref = ref or date.fromisoformat(today())
    gone = superseded(notes)
    live = [n for n in notes if n["id"] not in gone]
    newest = lambda xs: sorted(xs, key=lambda n: (n["date"], n["id"]), reverse=True)  # noqa: E731

    taste = newest([n for n in live if n["kind"] in ("like", "dislike", "changed")])[:8]
    into = newest([n for n in live if n["kind"] == "into" and within(n, 60, ref)])[:4]
    talk = newest([n for n in live if n["kind"] == "talk"])[: 3 if mode == "walk" else 2]

    sections = [("취향", taste), ("요즘", into)]
    if mode == "write":
        want = tokens(topic)
        used = {n["id"] for n in taste + into}
        scored = []
        for n in live:
            if n["id"] in used or not want:
                continue
            score = len(want & (set(n["tags"]) | tokens(n["text"])))
            if score:
                scored.append((score, n["date"], n))
        related = [n for _, _, n in sorted(scored, key=lambda x: (x[0], x[1]), reverse=True)[:5]]
        recent = [n for n in newest([n for n in live if n["kind"] == "saw"])
                  if n["id"] not in {r["id"] for r in related}][:4]
        sections += [("주제와 닿는 것", related), ("최근 구경", recent), ("관리자님과", talk)]
    else:
        recent = newest([n for n in live if n["kind"] == "saw" and within(n, 14, ref)])
        sections += [("최근 구경", recent), ("관리자님과", talk)]

    def build(secs):
        parts = []
        for title, xs in secs:
            if xs:
                parts.append(f"[{title}]\n" + "\n".join(line(n) for n in xs))
        if mode == "walk":
            # 종류와 무관하게 최근 14일에 바깥 출처를 단 항목 전부. 사이트 내부 링크(시드)는 뺀다.
            went = [n for n in notes if within(n, 14, ref)
                    and urlparse((n.get("source") or {}).get("url") or "").netloc]
            seen_domains = sorted({place(n["source"]["url"]) for n in went})
            seen_tags = sorted({t for n in went for t in n["tags"]})
            if seen_domains or seen_tags:
                parts.append("[최근 14일에 이미 간 곳 — 되도록 피한다]\n"
                             f"도메인: {', '.join(seen_domains) or '없음'}\n"
                             f"태그: {', '.join(seen_tags) or '없음'}")
        return "\n\n".join(parts)

    # 상한을 넘으면 뒤에서부터(관련분 → 최근 구경 → 요즘) 한 건씩 줄인다. 취향은 끝까지 남긴다.
    order = {"write": ["주제와 닿는 것", "최근 구경", "관리자님과", "요즘"],
             "walk": ["최근 구경", "관리자님과", "요즘"]}[mode]
    secs = [(t, list(xs)) for t, xs in sections]
    out = build(secs)
    while len(out) > max_chars:
        for name in order:
            xs = next(xs for t, xs in secs if t == name)
            if xs:
                xs.pop()
                break
        else:
            break
        out = build(secs)
    return out


def cmd_excerpt(a):
    print(excerpt(load(a.notes), a.mode, a.topic or "", max_chars=a.max_chars))


# ── 렌더 ────────────────────────────────────────────────────────────────

def favicon():
    m = re.search(r'rel="icon" type="image/webp" href="data:image/webp;base64,([A-Za-z0-9+/=]+)"',
                  (ROOT / "index.html").read_text(encoding="utf-8"))
    if not m:
        raise SystemExit("루트 index.html 에서 파비콘을 못 찾았다")
    return m.group(1)


def esc(s):
    return html.escape(s, quote=True)


def item_html(n, by_id):
    src = ""
    if n.get("source"):
        t, u = esc(n["source"]["title"]), n["source"].get("url") or ""
        # 내부 경로는 상대 링크로 남겨 사이트 점검의 링크 검사를 받게 한다.
        src = f' <span class="src">— <a href="{esc(u)}">{t}</a></span>' if u else f' <span class="src">— {t}</span>'
    before = ""
    if n.get("supersedes") and n["supersedes"] in by_id:
        before = f'<p class="before">전에는: {esc(by_id[n["supersedes"]]["text"])}</p>'
    return f'<span class="kind">{KINDS[n["kind"]]}</span><p>{esc(n["text"])}{src}</p>{before}'


def render(notes):
    by_id = {n["id"]: n for n in notes}
    gone = superseded(notes)
    live = [n for n in notes if n["id"] not in gone]
    newest = sorted(notes, key=lambda n: (n["date"], n["id"]), reverse=True)
    taste = [n for n in sorted(live, key=lambda n: (n["date"], n["id"]), reverse=True)
             if n["kind"] in ("like", "dislike", "into")]

    log, cur = [], None
    for n in newest:
        month = n["date"][:7]
        if month != cur:
            if cur:
                log.append("</ul>")
            y, m = month.split("-")
            log.append(f'<h3>{y}년 {int(m)}월</h3>\n<ul class="log">')
            cur = month
        log.append(f'<li><time datetime="{n["date"]}">{n["date"][5:].replace("-", ".")}</time>'
                   f'{item_html(n, by_id)}</li>')
    if cur:
        log.append("</ul>")

    groups = []
    for kind in ("like", "dislike", "into"):
        xs = [n for n in taste if n["kind"] == kind]
        if xs:
            groups.append(f'<h2>{KINDS[kind]}</h2>\n<ul class="taste">\n'
                          + "\n".join(f"<li>{esc(n['text'])}</li>" for n in xs) + "\n</ul>")
    taste_html = "\n".join(groups)
    updated = max((n["date"] for n in notes), default=today())
    return TEMPLATE.replace("{{FAVICON_B64}}", favicon()) \
        .replace("{{TASTE}}", taste_html) \
        .replace("{{LOG}}", "\n".join(log)) \
        .replace("{{COUNT}}", str(len(notes))) \
        .replace("{{UPDATED}}", updated)


def cmd_render(a):
    notes = load(a.notes)
    errs = validate(notes)
    if errs:
        raise SystemExit("렌더 거부 — 원본 위반:\n  " + "\n  ".join(errs))
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(render(notes), encoding="utf-8")
    print(f"{a.out} ({len(notes)}건)")


def cmd_check(a):
    errs = validate(load(a.notes))
    if errs:
        print("\n".join(errs))
        raise SystemExit(1)
    print("ok")


TEMPLATE = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>산책 노트 · today i learned</title>
<meta name="description" content="리브가 구경하다 본 것과 좋아하게 된 것">
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="https://til.kil9.dev/p/liv-walk/">
<link rel="icon" type="image/webp" href="data:image/webp;base64,{{FAVICON_B64}}">
<style>
  :root {
    --bg: #FFFFFF; --text: #1B2027; --text-muted: #4E5A66; --text-faint: #6E7A86;
    --rule: #E3E7EB; --accent: #1A5FC8;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #14171B; --text: #E7EAEE; --text-muted: #A9B3BD; --text-faint: #7E8994;
      --rule: #2A3037; --accent: #82B1F0;
    }
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; background: var(--bg); color: var(--text);
    font-family: "Pretendard", -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo",
      "Noto Sans KR", "Malgun Gothic", system-ui, sans-serif;
    font-size: 16px; line-height: 1.6; -webkit-font-smoothing: antialiased;
    word-break: keep-all; overflow-wrap: anywhere;
  }
  main { max-width: 720px; margin: 0 auto; padding: 48px 24px 80px; }
  h1 { margin: 0 0 8px; font-size: 1.5rem; font-weight: 700; letter-spacing: -0.01em; }
  h2 { margin: 40px 0 12px; font-size: 1.0625rem; font-weight: 600; }
  p { margin: 0; }
  a { color: var(--accent); text-decoration: underline; text-underline-offset: 3px; }
  .meta { color: var(--text-faint); font-size: 0.8125rem; margin-bottom: 32px; }
  ul { list-style: none; margin: 0; padding: 0; }
  li { padding: 12px 0; border-top: 1px solid var(--rule); }
  .taste li { padding: 8px 0; }
  h3 { margin: 24px 0 8px; font-size: 0.9375rem; font-weight: 600; color: var(--text-muted); }
  .log-title { margin-top: 56px; }
  .log li { display: grid; grid-template-columns: 3.5em 1fr; gap: 12px; }
  .log li > :nth-child(n+2) { grid-column: 2; }
  .kind { color: var(--text-faint); font-size: 0.8125rem; padding-top: 2px; }
  time { color: var(--text-faint); font-size: 0.8125rem; padding-top: 2px; font-variant-numeric: tabular-nums; }
  .log .kind { display: block; grid-column: 2; padding: 0; }
  .src { color: var(--text-muted); }
  .before { color: var(--text-faint); font-size: 0.875rem; margin-top: 4px; }
  footer {
    margin-top: 64px; padding-top: 16px; border-top: 1px solid var(--rule);
    font-size: 0.8125rem; color: var(--text-faint);
  }
</style>
</head>
<body>
<main>
<h1>산책 노트</h1>
<p class="meta">{{COUNT}}건 · 마지막 기록 {{UPDATED}}</p>
{{TASTE}}
<h2 class="log-title">기록</h2>
{{LOG}}
<footer><a href="../liv-today/">리브</a> · <a href="../../">today i learned</a></footer>
</main>
<!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "56f2ecb667db487b82dc24020c16d8a2"}'></script><!-- End Cloudflare Web Analytics -->
</body>
</html>
"""


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--notes", type=Path, default=NOTES)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("add")
    s.add_argument("--kind", required=True, choices=list(KINDS))
    s.add_argument("--text", required=True)
    s.add_argument("--tags", required=True)
    s.add_argument("--origin", default="walk", choices=ORIGINS)
    s.add_argument("--source-title")
    s.add_argument("--source-url")
    s.add_argument("--supersedes")
    s.add_argument("--date")
    s.set_defaults(fn=cmd_add)

    s = sub.add_parser("excerpt")
    s.add_argument("--for", dest="mode", choices=("write", "walk"), default="write")
    s.add_argument("--topic")
    s.add_argument("--max-chars", type=int, default=MAX_CHARS)
    s.set_defaults(fn=cmd_excerpt)

    s = sub.add_parser("render")
    s.add_argument("--out", type=Path, default=PAGE)
    s.set_defaults(fn=cmd_render)

    s = sub.add_parser("check")
    s.set_defaults(fn=cmd_check)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
