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
  python3 backlog/assets/liv-notes.py apply-walk <state/walk-D.json>   # 산책 잡(run.sh)이 부른다

페이지 꾸밈(취향 문장 속 링크 구절·이모지, 날마다의 그림·사진, 리브가 고쳐 가는 CSS)은 원본이
아니라 사이드카 liv-notes/decor.json·liv.css 에 둔다 — 원본은 덧붙이기 전용이고 꾸밈은 뒤에
얼마든지 다시 칠할 수 있어야 해서다(task-139·140·141).

--notes·--out 으로 경로를 바꿀 수 있다(테스트·전용 클론용).
"""

import argparse
import html
import json
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
NOTES = ROOT / "backlog" / "assets" / "liv-notes" / "notes.jsonl"
PAGE = ROOT / "p" / "liv-walk" / "index.html"
DECOR = ROOT / "backlog" / "assets" / "liv-notes" / "decor.json"
LIV_CSS = ROOT / "backlog" / "assets" / "liv-notes" / "liv.css"
DRAW = PAGE.parent / "draw"
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


# ── 꾸밈 ────────────────────────────────────────────────────────────────
# decor.json = {"notes": {id: {anchor, emoji, emoji_pos}},
#               "days": {date: {"drawing": {file, caption}, "photos": [{src, page, caption, credit, license}]}},
#               "design": [{date, note}]}
# 전부 산책 모델의 출력에서 오므로 공개 페이지에 싣기 전에 여기서 틀을 엄격히 본다.

MAX_CSS = 16000   # 주간 개편(task-142)에서 크게 다시 쓴 CSS 도 다음 날 조금씩 고칠 때 그대로 통과해야 한다
MAX_SVG = 12000
CSS_BANNED = re.compile(r"url\s*\(|@import|@font-face|expression|javascript|behavior|[<\\]", re.I)
SVG_NS = "{http://www.w3.org/2000/svg}"
SVG_ELEMS = set("""svg g path circle ellipse rect line polyline polygon text tspan title desc defs
    linearGradient radialGradient stop clipPath""".split())
SVG_ATTRS = set("""viewBox width height d cx cy r rx ry x y x1 y1 x2 y2 dx dy points fill stroke
    stroke-width stroke-linecap stroke-linejoin stroke-dasharray stroke-opacity fill-opacity fill-rule
    opacity transform font-size font-family font-weight font-style text-anchor letter-spacing id offset
    stop-color stop-opacity gradientUnits gradientTransform fx fy clip-path preserveAspectRatio""".split())
SVG_VALUE = re.compile(r"^(url\(#[A-Za-z][\w-]*\)|[^():;<>&\\]*)$")
PHOTO_SRC = re.compile(r"^https://(upload|thumb)\.wikimedia\.org/wikipedia/commons/[\w%./()~+,!'-]+$")
PHOTO_PAGE = re.compile(r"^https://commons\.wikimedia\.org/wiki/File:[^\s\"<>]+$")


def load_decor():
    d = json.loads(DECOR.read_text(encoding="utf-8")) if DECOR.exists() else {}
    return {"notes": d.get("notes", {}), "days": d.get("days", {}), "design": d.get("design", [])}


def save_decor(d):
    DECOR.write_text(json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def clean(s, limit):
    s = " ".join(str(s or "").split())
    return s if 0 < len(s) <= limit else ""


def ok_emoji(s):
    s = str(s or "").strip()
    if not 1 <= len(s) <= 8:
        return ""
    cats = [unicodedata.category(c) for c in s]
    if "So" not in cats or any(c not in ("So", "Sk", "Mn", "Me", "Cf") for c in cats):
        return ""
    return s


def note_decor(n, text):
    """산책 출력의 노트 하나에서 링크 구절·이모지를 꺼낸다. 구절은 원문에 그대로 있어야 한다."""
    out = {}
    anchor = clean(n.get("link"), 40)
    if len(anchor) >= 2 and anchor in text:
        out["anchor"] = anchor
    emoji = ok_emoji(n.get("emoji"))
    if emoji:
        out["emoji"] = emoji
        out["emoji_pos"] = "front" if n.get("emoji_pos") == "front" else "back"
    return out


def sanitize_svg(src):
    """허용 요소·속성만 남겨 새로 쓴다. 실패하면 ''. 페이지에는 <img> 로만 실어 스크립트가 돌 길이 없지만,
    파일을 직접 열 수도 있으니 파일 자체도 깨끗해야 한다."""
    src = str(src or "").strip()
    src = re.sub(r"^<\?xml[^>]*\?>", "", src).strip()
    if not src or len(src.encode()) > MAX_SVG or "<!" in src or "<?" in src:
        return ""
    try:
        root = ET.fromstring(src)
    except ET.ParseError:
        return ""
    count = 0

    def tag(el):
        t = el.tag
        if t.startswith(SVG_NS):
            t = t[len(SVG_NS):]
        return t if t in SVG_ELEMS and "}" not in t else None

    def emit(el):
        nonlocal count
        count += 1
        if count > 600:
            raise ValueError
        t = tag(el)
        if t is None:  # 허용 밖 요소(script·a·foreignObject 등)는 하위째 버린다
            return ""
        attrs = []
        for k, v in el.attrib.items():
            if k not in SVG_ATTRS or not SVG_VALUE.match(v):
                continue
            attrs.append(f' {k}="{html.escape(v, quote=True)}"')
        if t == "svg":
            attrs.insert(0, ' xmlns="http://www.w3.org/2000/svg"')
        body = html.escape(el.text or "", quote=False) if t in ("text", "tspan", "title", "desc") else ""
        for c in el:
            body += emit(c)
            if t in ("text", "tspan"):
                body += html.escape(c.tail or "", quote=False)
        return f"<{t}{''.join(attrs)}>{body}</{t}>"

    if tag(root) != "svg" or "viewBox" not in root.attrib:
        return ""
    try:
        return emit(root)
    except (ValueError, RecursionError):
        return ""


def ok_photo(ph):
    src, page = str(ph.get("src") or ""), str(ph.get("page") or "")
    if not PHOTO_SRC.match(src) or not PHOTO_PAGE.match(page):
        return None
    return {"src": src, "page": page, "caption": clean(ph.get("caption"), 80),
            "credit": clean(ph.get("credit"), 120), "license": clean(ph.get("license"), 40)}


def ok_css(css):
    css = str(css or "").strip()
    if not css or len(css) > MAX_CSS or CSS_BANNED.search(css) or css.count("{") != css.count("}"):
        return ""
    return css + "\n"


def cmd_apply_walk(a):
    """산책 결과 하나를 노트·꾸밈에 반영하고 페이지를 굽는다. 한 부분이 거부돼도 나머지는 남긴다."""
    walk = json.loads(a.walk.read_text(encoding="utf-8"))
    day = a.date or walk.get("date") or today()
    decor = load_decor()
    for n in walk.get("notes") or []:
        notes = load(a.notes)
        note = {"id": next_id(notes), "date": day, "kind": n["kind"], "text": n["text"].strip(),
                "tags": [t.strip().lower() for t in n["tags"] if t.strip()], "origin": "walk",
                "source": {"title": n["source"]["title"], "url": n["source"].get("url") or ""}}
        if n.get("supersedes"):
            note["supersedes"] = n["supersedes"]
        errs = validate(notes + [note])
        if errs:
            print("노트 거부: " + "; ".join(errs))
            continue
        with a.notes.open("a", encoding="utf-8") as f:
            f.write(json.dumps(note, ensure_ascii=False) + "\n")
        extra = note_decor(n, note["text"])
        if extra:
            decor["notes"][note["id"]] = extra
        print(note["id"])

    today_decor = {}
    dr = walk.get("drawing") or {}
    svg = sanitize_svg(dr.get("svg"))
    if svg:
        DRAW.mkdir(parents=True, exist_ok=True)
        (DRAW / f"{day}.svg").write_text(svg + "\n", encoding="utf-8")
        today_decor["drawing"] = {"file": f"draw/{day}.svg", "caption": clean(dr.get("caption"), 80)}
    elif dr:
        print("그림 거부 — 허용 틀 밖")
    photos = [p for p in (ok_photo(p) for p in (walk.get("photos") or [])[:3]) if p]
    if photos:
        today_decor["photos"] = photos
    if today_decor:
        decor["days"][day] = today_decor

    design = walk.get("design") or {}
    css = ok_css(design.get("css"))
    if css:
        LIV_CSS.write_text(css, encoding="utf-8")
        decor["design"] = [d for d in decor["design"] if d.get("date") != day]
        entry = {"date": day, "note": clean(design.get("note"), 400 if design.get("redesign") else 160)
                 or "조금 고쳤습니다."}
        if design.get("redesign") is True:
            entry["redesign"] = True
        decor["design"].append(entry)
    elif design:
        print("디자인 거부 — CSS 가 허용 틀 밖")
    save_decor(decor)
    cmd_render(a)


# ── 렌더 ────────────────────────────────────────────────────────────────

def favicon():
    m = re.search(r'rel="icon" type="image/webp" href="data:image/webp;base64,([A-Za-z0-9+/=]+)"',
                  (ROOT / "index.html").read_text(encoding="utf-8"))
    if not m:
        raise SystemExit("루트 index.html 에서 파비콘을 못 찾았다")
    return m.group(1)


def esc(s):
    return html.escape(s, quote=True)


def with_emoji(body, d):
    e = d.get("emoji")
    if not e:
        return body
    mark = f'<span class="emoji" aria-hidden="true">{esc(e)}</span>'
    return f"{mark} {body}" if d.get("emoji_pos") == "front" else f"{body} {mark}"


def taste_text(n, d):
    """취향 문장에 출처 링크를 문장 속 구절 하나로 단다 — 출처 표기를 따로 붙이지 않는다."""
    text, url = n["text"], (n.get("source") or {}).get("url") or ""
    anchor = d.get("anchor") or ""
    if url and anchor and anchor in text:
        i = text.index(anchor)
        body = f'{esc(text[:i])}<a href="{esc(url)}">{esc(anchor)}</a>{esc(text[i + len(anchor):])}'
    else:
        body = esc(text)
    return with_emoji(body, d)


def item_html(n, by_id, d):
    src = ""
    if n.get("source"):
        t, u = esc(n["source"]["title"]), n["source"].get("url") or ""
        # 내부 경로는 상대 링크로 남겨 사이트 점검의 링크 검사를 받게 한다.
        src = f' <span class="src">— <a href="{esc(u)}">{t}</a></span>' if u else f' <span class="src">— {t}</span>'
    before = ""
    if n.get("supersedes") and n["supersedes"] in by_id:
        before = f'<p class="before">전에는: {esc(by_id[n["supersedes"]]["text"])}</p>'
    return (f'<span class="kind">{KINDS[n["kind"]]}</span>'
            f'<p>{with_emoji(esc(n["text"]), d)}{src}</p>{before}')


def album_html(day, up=""):
    figs = []
    dr = day.get("drawing")
    if dr:
        cap = esc(dr.get("caption") or "")
        figs.append(f'<figure class="drawing"><img src="{up}{esc(dr["file"])}" alt="{cap or "리브의 그림"}" '
                    f'loading="lazy" width="240" height="180"><figcaption>{cap}</figcaption></figure>')
    for ph in day.get("photos") or []:
        cap = esc(ph.get("caption") or "")
        credit = " · ".join(esc(x) for x in (ph.get("credit"), ph.get("license")) if x)
        figs.append(f'<figure class="photo"><a href="{esc(ph["page"])}"><img src="{esc(ph["src"])}" '
                    f'alt="{cap}" loading="lazy"></a><figcaption>{cap}'
                    f'{f"<small>{credit}</small>" if credit else ""}</figcaption></figure>')
    return f'<div class="album">{"".join(figs)}</div>' if figs else ""


TASTE_SHOWN = {"like": 8, "dislike": 4, "into": 4}   # 취향 목록에서 펼쳐 두는 최근 항목 수
OPEN_DAYS = 7      # 본 페이지에서 펼쳐 두는 최근 날 수
FOLD_DAYS = 30     # 그 뒤로 접어서 본 페이지에 남기는 날 수. 더 오래된 날은 달별 아카이브에만 있다


EMOJI_SPAN = '<span class="emoji" aria-hidden="true">{}</span> '


def day_html(day, xs, by_id, decor, up="", folded=False):
    nd = decor["notes"]
    stamp = f'<time datetime="{day}">{day[5:].replace("-", ".")}</time>'
    body = (album_html(decor["days"].get(day, {}), up) + '<ul class="log">'
            + "".join(f'<li>{item_html(n, by_id, nd.get(n["id"], {}))}</li>' for n in xs) + "</ul>")
    if not folded:
        return f'<section class="day">{stamp}{body}</section>'
    # 접힌 날의 머리에는 그날 붙은 이모지와 첫 노트 첫머리를 보여 무엇을 봤는지 짐작하게 한다.
    marks = "".join(esc(nd[n["id"]]["emoji"]) for n in xs if nd.get(n["id"], {}).get("emoji"))
    lead = esc(xs[0]["text"][:48].rstrip()) + "…"
    return (f'<details class="day folded"><summary>{stamp}<span class="peek">'
            f'{EMOJI_SPAN.format(marks) if marks else ""}{lead}'
            f'</span><span class="count">{len(xs)}건</span></summary>{body}</details>')


def by_day(notes):
    days = {}
    for n in sorted(notes, key=lambda n: (n["date"], n["id"]), reverse=True):
        days.setdefault(n["date"], []).append(n)
    return days


def month_label(month):
    y, m = month.split("-")
    return f"{y}년 {int(m)}월"


def page(body_title, meta, main, canonical, up, decor):
    liv_css = LIV_CSS.read_text(encoding="utf-8") if LIV_CSS.exists() else ""
    if liv_css and not ok_css(liv_css):
        raise SystemExit(f"{LIV_CSS} 가 허용 틀 밖이다")
    return TEMPLATE.replace("{{FAVICON_B64}}", favicon()) \
        .replace("{{LIV_CSS}}", liv_css) \
        .replace("{{TITLE}}", body_title) \
        .replace("{{CANONICAL}}", canonical) \
        .replace("{{META}}", meta) \
        .replace("{{MAIN}}", main) \
        .replace("{{UP}}", up)


def render(notes, decor=None):
    """본 페이지 HTML 과 달별 아카이브 {YYYY-MM: HTML} 을 돌려준다."""
    decor = decor or load_decor()
    nd = decor["notes"]
    by_id = {n["id"]: n for n in notes}
    gone = superseded(notes)
    live = [n for n in notes if n["id"] not in gone]
    taste = [n for n in sorted(live, key=lambda n: (n["date"], n["id"]), reverse=True)
             if n["kind"] in ("like", "dislike", "into")]
    days = by_day(notes)
    order = list(days)
    months = sorted({d[:7] for d in order}, reverse=True)

    groups = []
    for kind in ("like", "dislike", "into"):
        xs = [n for n in taste if n["kind"] == kind]
        if xs:
            lis = [f"<li>{taste_text(n, nd.get(n['id'], {}))}</li>" for n in xs]
            keep = TASTE_SHOWN[kind]
            more = (f'<details class="more"><summary>더 보기 ({len(lis) - keep})</summary><ul class="taste">'
                    + "\n".join(lis[keep:]) + "</ul></details>") if len(lis) > keep else ""
            groups.append(f'<section class="taste-group taste-{kind}"><h2>{KINDS[kind]}</h2>\n<ul class="taste">\n'
                          + "\n".join(lis[:keep]) + "\n</ul>" + more + "</section>")

    # 기록: 최근 OPEN_DAYS 일은 펼치고, 그 뒤 FOLD_DAYS 일은 접어 두고, 더 오래된 날은 달별 아카이브로.
    log, month = [], None
    for i, day in enumerate(order[:OPEN_DAYS + FOLD_DAYS]):
        if day[:7] != month:
            month = day[:7]
            log.append(f'<h3>{month_label(month)}</h3>')
        log.append(day_html(day, days[day], by_id, decor, folded=i >= OPEN_DAYS))
    archive_nav = ('<nav class="archive"><h2>지난 달</h2><ul>'
                   + "".join(f'<li><a href="{m}/">{month_label(m)}</a>'
                             f'<span class="count">{sum(len(days[d]) for d in order if d[:7] == m)}건</span></li>'
                             for m in months) + "</ul></nav>")

    design = sorted(decor["design"], key=lambda d: d["date"], reverse=True)
    design_html = ""
    if design:
        design_html = ('<details class="design-log"><summary>리브가 이 페이지를 고친 기록</summary><ul>'
                       + "".join(f'<li><time datetime="{esc(d["date"])}">{esc(d["date"][5:].replace("-", "."))}</time>'
                                 f'<p>{"<span class=\"redesign\">개편</span> " if d.get("redesign") else ""}{esc(d["note"])}</p></li>'
                                 for d in design)
                       + "</ul></details>")
    updated = max((n["date"] for n in notes), default=today())
    main = ('<div class="tastes">' + "\n".join(groups) + '</div>\n<h2 class="log-title">기록</h2>\n'
            + "\n".join(log) + "\n" + archive_nav + "\n" + design_html)
    index = page("산책 노트", f"{len(notes)}건 · 마지막 기록 {updated}", main,
                 "https://til.kil9.dev/p/liv-walk/", "", decor)

    archives = {}
    for m in months:
        ds = [d for d in order if d[:7] == m]
        body = (f'<p class="back"><a href="../">← 산책 노트</a></p>\n'
                + "\n".join(day_html(d, days[d], by_id, decor, up="../") for d in ds))
        archives[m] = page(f"산책 노트 · {month_label(m)}",
                           f"{sum(len(days[d]) for d in ds)}건 · {len(ds)}일", body,
                           f"https://til.kil9.dev/p/liv-walk/{m}/", "../", decor)
    return index, archives


def cmd_render(a):
    notes = load(a.notes)
    errs = validate(notes)
    if errs:
        raise SystemExit("렌더 거부 — 원본 위반:\n  " + "\n  ".join(errs))
    index, archives = render(notes)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(index, encoding="utf-8")
    for m, body in archives.items():
        (a.out.parent / m).mkdir(exist_ok=True)
        (a.out.parent / m / "index.html").write_text(body, encoding="utf-8")
    print(f"{a.out} ({len(notes)}건, 달별 아카이브 {len(archives)}개)")


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
<title>{{TITLE}} · today i learned</title>
<meta name="description" content="리브가 구경하다 본 것과 좋아하게 된 것">
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="{{CANONICAL}}">
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
  main { max-width: 760px; margin: 0 auto; padding: 48px 24px 80px; }
  h1 { margin: 0 0 8px; font-size: 1.5rem; font-weight: 700; letter-spacing: -0.01em; }
  h2 { margin: 40px 0 12px; font-size: 1.0625rem; font-weight: 600; }
  p { margin: 0; }
  a { color: var(--accent); text-decoration: underline; text-underline-offset: 3px; }
  .meta { color: var(--text-faint); font-size: 0.8125rem; margin-bottom: 32px; }
  ul { list-style: none; margin: 0; padding: 0; }
  li { padding: 12px 0; border-top: 1px solid var(--rule); }
  .taste li { padding: 8px 0; }
  h3 { margin: 32px 0 4px; font-size: 0.9375rem; font-weight: 600; color: var(--text-muted); }
  .log-title { margin-top: 56px; }
  .taste a { color: inherit; text-decoration-color: var(--accent); text-decoration-thickness: 1px; }
  .taste a:hover { color: var(--accent); }
  .emoji { font-style: normal; }
  .day { display: grid; grid-template-columns: 3.5em 1fr; column-gap: 12px; padding-top: 16px; }
  .day > time { grid-row: 1 / span 2; padding-top: 14px; }
  .day > .album, .day > .log { grid-column: 2; }
  .album {
    display: grid; grid-template-columns: repeat(auto-fill, minmax(min(150px, 42%), 1fr));
    gap: 12px; margin: 12px 0 4px;
  }
  figure { margin: 0; }
  figure img {
    display: block; width: 100%; height: auto; aspect-ratio: 4 / 3; object-fit: cover;
    border-radius: 6px; background: var(--rule);
  }
  .drawing img { object-fit: contain; background: transparent; border: 1px solid var(--rule); }
  figcaption { margin-top: 6px; font-size: 0.8125rem; color: var(--text-muted); line-height: 1.45; }
  figcaption small { display: block; color: var(--text-faint); font-size: 0.75rem; }
  .log li { padding: 12px 0; }
  .kind { display: block; color: var(--text-faint); font-size: 0.8125rem; }
  time { color: var(--text-faint); font-size: 0.8125rem; font-variant-numeric: tabular-nums; }
  .src { color: var(--text-muted); }
  .before { color: var(--text-faint); font-size: 0.875rem; margin-top: 4px; }
  .design-log { margin-top: 48px; font-size: 0.875rem; color: var(--text-muted); }
  .design-log summary { cursor: pointer; color: var(--text-faint); }
  .design-log li { display: grid; grid-template-columns: 3.5em 1fr; gap: 12px; padding: 8px 0; }
  .day.folded { display: block; border-top: 1px solid var(--rule); }
  .day.folded > summary {
    display: grid; grid-template-columns: 3.5em 1fr auto; gap: 12px; align-items: baseline;
    padding: 10px 0; cursor: pointer; list-style: none;
  }
  .day.folded > summary::-webkit-details-marker { display: none; }
  .day.folded .peek { color: var(--text-muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .day.folded[open] .peek { visibility: hidden; }
  .count { color: var(--text-faint); font-size: 0.8125rem; font-variant-numeric: tabular-nums; }
  .day.folded > .album, .day.folded > .log { margin-left: calc(3.5em + 12px); }
  .archive ul { display: flex; flex-wrap: wrap; gap: 8px 20px; }
  .archive li { border: 0; padding: 0; display: flex; gap: 6px; align-items: baseline; }
  .back { margin-bottom: 24px; font-size: 0.875rem; }
  .redesign { font-size: 0.75rem; color: var(--accent); border: 1px solid currentColor; border-radius: 4px; padding: 0 4px; }
  .taste li { break-inside: avoid; }
  .more > summary { cursor: pointer; color: var(--text-faint); font-size: 0.875rem; padding: 8px 0; }
  /* 넓은 화면은 칸을 나눠 한 화면에 더 많이 보이게 한다 */
  @media (min-width: 1100px) {
    main { max-width: 1120px; }
    .tastes { display: grid; grid-template-columns: 2fr 1fr; column-gap: 40px; align-items: start; }
    .tastes .taste-like { grid-row: span 2; }
    .tastes .taste-like .taste { columns: 2; column-gap: 32px; }
    .log { display: grid; grid-template-columns: 1fr 1fr; column-gap: 32px; }
  }
  footer {
    margin-top: 64px; padding-top: 16px; border-top: 1px solid var(--rule);
    font-size: 0.8125rem; color: var(--text-faint);
  }
  /* ── 여기서부터 리브의 몫(backlog/assets/liv-notes/liv.css) — 산책 때마다 조금씩 고친다 ── */
{{LIV_CSS}}</style>
</head>
<body>
<main>
<h1>{{TITLE}}</h1>
<p class="meta">{{META}}</p>
{{MAIN}}
<footer><a href="{{UP}}../liv-today/">리브</a> · <a href="{{UP}}../../">today i learned</a></footer>
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

    s = sub.add_parser("apply-walk")
    s.add_argument("walk", type=Path)
    s.add_argument("--date")
    s.add_argument("--out", type=Path, default=PAGE)
    s.set_defaults(fn=cmd_apply_walk)

    s = sub.add_parser("check")
    s.set_defaults(fn=cmd_check)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
