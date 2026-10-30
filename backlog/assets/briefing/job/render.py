#!/usr/bin/env python3
"""브리핑 JSON → 페이지 HTML (task-85).

템플릿과 자산은 til 저장소(전용 클론)에서 읽는다.
  backlog/assets/briefing/{template,item,item-rest}.html
  backlog/assets/liv/stickers-pastel/*-256.webp, avatar-expression-*-72.webp
  index.html 의 파비콘 base64

같은 내용을 두 곳에 쓴다.
  p/briefing/index.html            항상 최신 1건 (루트까지 ../../)
  p/briefing/<YYYY-MM-DD>/index.html  날짜별 누적 (루트까지 ../../../)

사용법: python3 render.py <til-repo> [YYYY-MM-DD]
"""

import base64
import html
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
STATE = BASE / "state"
KST = timezone(timedelta(hours=9))

# 아침 브리핑에 어울리는 컷만 추린다. 날짜로 돌려 매일 같은 그림이 되지 않게 한다.
HERO_STICKERS = ["mug-sip", "paper-pile", "chin-rest", "point-side", "magnify", "carry-stack", "box-hug"]
AVATARS = ["base", "curious", "troubled", "satisfied", "awkward", "yawn"]
# 이보다 크면 경고. 실측은 100KB 안팎(본문이 대부분, 자산 29KB)이라 구 상한 100KB 는
# 매 회차 걸려 경고가 일상이 됐다 — 매일 뜨는 경고는 곧 안 보게 된다. 여유를 5배로 잡아
# '뜨면 진짜 이상한 것' 으로 되돌린다. 연 365회차라도 500KB × 365 = 178MB 로 Pages 한도
# (1GB) 안이다. 용량을 실제로 줄이려면 상한이 아니라 싣는 항목 수를 손봐야 한다 (task-95).
MAX_BYTES = 500_000


def b64(path):
    return base64.b64encode(path.read_bytes()).decode()


def esc(s):
    return html.escape(str(s or ""), quote=True)


def fill(tpl, mapping):
    for k, v in mapping.items():
        tpl = tpl.replace("{{%s}}" % k, v)
    return tpl


LEFTOVER_RE = re.compile(r"\{\{[A-Z][A-Z0-9_]*\}\}")


def assert_filled(page, where):
    """미치환 토큰이 남았으면 죽는다 (task-106).

    템플릿은 repo 에 있고 잡 코드는 머신 로컬이라 둘의 버전이 어긋난 상태가 실제로 존재할
    수 있다 — 전용 클론이 매 시도 origin/main 으로 reset 하므로 템플릿만 먼저 배포되는
    경로가 있다. fill() 은 모르는 토큰을 조용히 남기므로 그때 라이브 페이지에 리터럴
    {{TOKEN}} 이 그대로 노출된다. 발행이 실패하고 Slack 으로 알림이 가는 편이 낫다.
    """
    left = sorted(set(LEFTOVER_RE.findall(page)))
    if left:
        raise RuntimeError(f"{where}: 치환되지 않은 토큰 {left} — 템플릿과 잡 코드 버전이 어긋났다")


def favicon(repo):
    m = re.search(r'rel="icon" type="image/webp" href="data:image/webp;base64,([A-Za-z0-9+/=]+)"',
                  (repo / "index.html").read_text(encoding="utf-8"))
    if not m:
        raise RuntimeError("루트 index.html 에서 파비콘을 못 찾았다")
    return m.group(1)


DAYNAV_RE = re.compile(r"(<!-- DAYNAV:START -->).*?(<!-- DAYNAV:END -->)", re.S)
DATE_DIR_RE = re.compile(r"\d{4}-\d{2}-\d{2}")

# 항목 참조를 번호가 아니라 제목으로 (task-103). 규칙은 compose 프롬프트에 있고
# 여기는 그 규칙이 안 지켜진 출력과 규칙 이전 회차를 위한 그물이다.
NUMLINK_RE = re.compile(r'<a href="#(i\d+)">\s*(\d{1,2})\s*</a>')
PICK_NUM_RE = re.compile(r"^\s*\d{1,2}\s*[—–-]\s*")
PARTICLES = {"은": "는", "는": "은", "이": "가", "가": "이", "을": "를", "를": "을",
             "과": "와", "와": "과", "으로": "로", "로": "으로"}


def has_final(ch):
    """한글 음절의 받침 유무. 숫자·영문은 한국어 관행대로 읽었을 때로 근사한다."""
    if "가" <= ch <= "힣":
        return (ord(ch) - 0xAC00) % 28 != 0
    return ch in "0136780lmnLMN"  # 영/일/삼/육/칠/팔/공 등 받침으로 끝나는 읽기


def fix_particle(text, replaced):
    """번호를 제목으로 갈아끼운 뒤 바로 뒤 조사를 새 끝음절에 맞춘다.

    '01은' 이 '「지식 팩토리…」은' 으로 남으면 눈에 걸린다. 조사 짝이 아닌 글자면 손대지 않는다.
    """
    if not text or text[0] not in PARTICLES:
        return text
    # '으로/로' 는 두 글자라 먼저 본다.
    for p in ("으로", "로"):
        if text.startswith(p):
            want = "으로" if has_final(replaced[-1]) else "로"
            return want + text[len(p):]
    p = text[0]
    pair = (p, PARTICLES[p])
    first_has_final = {"은": True, "는": False, "이": True, "가": False,
                       "을": True, "를": False, "과": True, "와": False}
    if p not in first_has_final:
        return text
    want = p if first_has_final[p] == has_final(replaced[-1]) else PARTICLES[p]
    return want + text[1:]


def label_by_anchor(data):
    """앵커 → 짧은 라벨. 목차 라벨이 제목보다 짧아 문장에 넣기 좋다."""
    out = {it["anchor"]: it["title"] for it in data.get("items", [])}
    out.update({t["anchor"]: t["label"] for t in data.get("toc", []) if t.get("label")})
    return out


def titles_to_links(text, labels, skip=None):
    """이미 escape 된 본문에서 「제목」 을 그 항목 앵커 링크로 만든다 (task-103).

    liv 한마디는 통째로 escape 되므로 모델이 링크를 쓸 수 없다. 대신 제목을 「」 로
    감싸게 하고 여기서 링크를 건다 — escape 뒤에 치환하므로 주입 위험이 없다.
    """
    for anchor, label in labels.items():
        if anchor == skip:
            continue
        needle = "「" + esc(label) + "」"
        if needle in text:
            text = text.replace(needle, f'<a href="#{anchor}">{needle}</a>')
    return text


def numbers_to_titles(html_text, labels, where):
    """<a href="#i01">01</a> 처럼 링크 글자가 번호뿐인 참조를 제목으로 되돌린다."""
    def sub(m):
        anchor, num = m.group(1), m.group(2)
        label = labels.get(anchor)
        if not label:
            return m.group(0)
        print(f"  번호 참조를 제목으로 고쳤다 ({where}): {num} → {label}", file=sys.stderr)
        return f'<a href="#{anchor}">「{esc(label)}」</a>\x00{anchor}\x00'

    out = NUMLINK_RE.sub(sub, html_text)
    # 치환 자리 바로 뒤 조사를 새 끝음절에 맞춘다.
    while "\x00" in out:
        i = out.index("\x00")
        j = out.index("\x00", i + 1)
        anchor = out[i + 1:j]
        rest = fix_particle(out[j + 1:], labels[anchor])
        out = out[:i] + rest
    return out


def briefing_dates(repo):
    """발행된 회차 날짜(오름차순). 날짜 디렉터리가 진실원본이다."""
    root = repo / "p/briefing"
    if not root.is_dir():
        return []
    return sorted(d.name for d in root.iterdir()
                  if d.is_dir() and DATE_DIR_RE.fullmatch(d.name) and (d / "index.html").exists())


def daynav(dates, date, prefix):
    """이전/다음 회차 이동 (task-92).

    브리핑은 휘발성이 커서 목록으로 되돌아가 고르기보다 옆으로 한 칸씩 넘기는 쪽이 맞다.
    prefix 는 날짜 디렉터리까지의 상대경로 — 날짜판은 '../', 최신판은 './' 다.
    """
    i = dates.index(date) if date in dates else len(dates)
    prev = dates[i - 1] if i > 0 else None
    nxt = dates[i + 1] if i + 1 < len(dates) else None
    short = lambda d: "%d-%d" % (int(d[5:7]), int(d[8:10]))
    d = datetime.fromisoformat(date)
    return ('<nav class="daynav" aria-label="회차 이동">\n'
            + (f'  <a class="prv" href="{prefix}{prev}/">← {short(prev)}</a>\n' if prev
               else '  <span class="prv off">← 이전 회차 없음</span>\n')
            + f'  <span class="cur">{esc(date)} ({"월화수목금토일"[d.weekday()]})</span>\n'
            + (f'  <a class="nxt" href="{prefix}{nxt}/">{short(nxt)} →</a>\n' if nxt
               else '  <span class="nxt off">다음 회차 없음</span>\n')
            + '</nav>')


def repatch_daynav(repo, dates, date, prefix="../"):
    """이미 발행된 날짜 페이지의 이동 내비만 다시 채운다.

    새 회차가 나오면 직전 회차의 '다음' 링크가 비어 있으므로 그것만 갈아끼운다.
    과거 회차를 나중에 채워 넣는 경우까지 감안해 양옆을 모두 손본다.

    결과를 문자열로 돌려준다 — 'patched' / 'unchanged' / 'no-marker' / 'missing'.
    마커를 못 찾는 것은 조용히 넘길 실패가 아니다(task-94). 템플릿에서 마커 이름이
    바뀌거나 사라지면 '어제 페이지에 다음 링크가 영영 안 생김' 이 아무 신호 없이 굳는다.
    """
    page = repo / "p/briefing" / date / "index.html"
    if not page.exists():
        return "missing"
    text = page.read_text(encoding="utf-8")
    if not DAYNAV_RE.search(text):
        return "no-marker"
    new = DAYNAV_RE.sub(lambda m: f"{m.group(1)}\n{daynav(dates, date, prefix)}\n{m.group(2)}", text)
    if new == text:
        return "unchanged"
    page.write_text(new, encoding="utf-8")
    return "patched"


# 배지가 이미 소스를 말하므로 라벨에 소스 이름을 되풀이하지 않는다. 다만 백분위의 뜻은
# 소스마다 다르다 — GeekNews 는 30일 롤링 추천 분포, HN 은 프런트페이지 30건 안의 순위다.
SOURCE_LABEL = {"gn": "추천 상위", "hn": "프런트 상위"}
SOURCE_NAME = {"gn": "GeekNews", "hn": "Hacker News"}


def srcmark(src):
    """출처 로고 (task-120). 실체는 template.html 상단 스프라이트의 <symbol> 이다.

    구 두 글자 텍스트 라벨을 갈아치웠다. 소스가 둘뿐이라 브랜드 타일의 색·형태가 곧
    이름이고, 글자보다 훑을 때 먼저 걸린다. 자리는 제목 끝이다 — 메타 줄에 두면 항목을
    다 읽은 뒤에야 출처를 알게 되고, 실제로 그 자리에서는 백분위 문구와 뒤엉켜 보였다.
    이름은 title·aria-label 로 남는다 — 로고를 못 읽는 독자에게 'HN' 두 글자보다
    오히려 친절하다.

    모르는 소스는 아무것도 내지 않는다. 소스가 늘어도 발행은 나가고, 그때 빠지는 것은
    제목 옆 아이콘 하나뿐이다 — 백분위 문구가 여전히 소스를 구분해 준다.
    """
    name = SOURCE_NAME.get(src)
    if not name:
        return ""
    return (f'<svg class="srcmark" role="img" aria-label="{esc(name)}">'
            f'<title>{esc(name)}</title><use href="#src-{esc(src)}"/></svg>')


def subtitle(it):
    """원제 병기 (task-106). 제목을 옮긴 항목에만 붙는다."""
    if not it.get("title_orig"):
        return ""
    return f'\n    <p class="orig">{esc(it["title_orig"])}</p>'


def foot(it):
    """항목 메타 한 줄. 출처 배지 + 그 소스 기준 백분위 + 반응 온도 배지.

    백분위 문구를 소스별로 다르게 쓰는 이유는 모집단이 다르기 때문이다. HN 쪽 수는
    이미 큐레이션된 프런트페이지 30건 안의 순위라 GeekNews 의 30일 롤링 백분위와 같은
    말이 아니다. 같은 '추천 상위' 로 찍으면 둘을 견주게 된다.
    """
    src = it.get("source", "gn")
    # 로고는 제목 끝으로 갔다. 이 줄에는 백분위만 남는데, 그 문구가 이미 소스마다
    # 다르므로('추천 상위' = GeekNews, '프런트 상위' = HN) 출처 표시가 사라지지 않는다.
    parts = [esc(it["domain"]), esc(it["interest"]),
             f'{SOURCE_LABEL.get(src, "추천 상위")} {esc(it["percentile"])}%']
    also = it.get("also")
    if also:      # 양쪽에 오른 글 — 링크는 GeekNews 쪽만 남기고 점수는 둘 다 보인다.
        # 여기는 제목 옆 로고가 가리키지 않는 '다른 쪽' 이라 이름을 글자로 밝힌다.
        parts.append(f'{esc(SOURCE_NAME.get(also["source"], str(also["source"]).upper()))} '
                     f'{esc(also.get("percentile", ""))}% ({esc(also["points"])}표)')
    if it.get("heat"):
        parts.append(f'<span class="heat">{esc(it["heat"])}</span>')
    return " · ".join(parts)


def render(data, repo, root_rel, dates=(), nav_prefix="../"):
    tdir = repo / "backlog/assets/briefing"
    liv_dir = repo / "backlog/assets/liv"
    day = datetime.fromisoformat(data["date"]).toordinal()
    hero = liv_dir / "stickers-pastel" / f"{HERO_STICKERS[day % len(HERO_STICKERS)]}-256.webp"

    labels = label_by_anchor(data)
    intro = [numbers_to_titles(p, labels, "머리말") for p in data.get("intro", [])]
    if intro:
        sticker = (f'<img class="sticker-hero" src="data:image/webp;base64,{b64(hero)}" '
                   f'alt="{esc(hero.stem.replace("-256", ""))} 포즈의 리브 스티커">')
        intro[0] = intro[0].replace("<p>", "<p>" + sticker, 1)

    items_html, avatar_i = [], 0
    for it in data["items"]:
        tie = ""
        if it.get("tie"):
            t = it["tie"]
            tie = ('    <div class="tiebox"><span class="lbl">til 연관</span>'
                   f'<a href="{esc(root_rel + t["url"].lstrip("./"))}">{esc(t["title"])}</a> {esc(t["text"])}</div>\n')
        liv = ""
        if it.get("liv"):
            av = liv_dir / f"avatar-expression-{AVATARS[avatar_i % len(AVATARS)]}-72.webp"
            avatar_i += 1
            liv = ('    <div class="liv">'
                   f'<img src="data:image/webp;base64,{b64(av)}" alt="리브" width="72" height="72">'
                   f'<p>{titles_to_links(esc(it["liv"]), labels, skip=it["anchor"])}</p></div>\n')
        items_html.append(fill(tdir.joinpath("item.html").read_text(encoding="utf-8"), {
            "ANCHOR": esc(it["anchor"]), "RANK": esc(it["rank"]), "URL": esc(it["url"]),
            "TITLE": esc(it["title"]), "LEDE": esc(it["lede"]),
            "BULLETS": "\n".join(f"      <li>{esc(b)}</li>" for b in it["bullets"]),
            "SRC": srcmark(it.get("source", "gn")),
            "SUBTITLE": subtitle(it), "FOOT": foot(it),
            "TIEBOX": tie, "LIV": liv,
            "ACTION_TOPIC": esc(it["action_topic"]), "ACTION_URL": esc(it["source_url"]),
            "ACTION_ANGLE": esc(it["angle"]),
        }))

    # 넘긴 것 그리드에는 원래 출처 표시가 없었다 (task-120). 본문 항목만 배지를 달면
    # 아래로 내려올수록 어디서 온 글인지 모르게 되고, 그 그리드가 회차 건수의 대부분이다.
    rest_html = [fill(tdir.joinpath("item-rest.html").read_text(encoding="utf-8"), {
        "SRC": srcmark(r.get("source", "gn")),
        "URL": esc(r["url"]), "TITLE": esc(r["title"]), "SUMMARY": esc(r["summary"]),
        "ACTION_TOPIC": esc(r["action_topic"]), "ACTION_URL": esc(r["source_url"]),
        "ACTION_ANGLE": esc(r["angle"]),
    }) for r in data["rest"]]

    toc = "\n".join(f'      <li><a href="#{esc(t["anchor"])}">{esc(t["label"])}</a></li>'
                    for t in data.get("toc", []))
    for h in items_html:
        assert_filled(h, "item.html")
    followup = render_followup(data.get("followup") or {})
    pick = data.get("pick") or {}
    pick_anchor = pick.get("anchor") or (data["items"][0]["anchor"] if data["items"] else "i01")
    # 이유 한 줄에서 '06 — ' 같은 번호 머리를 떼고 제목을 그 자리에 세운다 (task-103).
    pick_line = PICK_NUM_RE.sub("", pick.get("line", ""))
    page = fill(tdir.joinpath("template.html").read_text(encoding="utf-8"), {
        "DATE": esc(data["date"]), "DATE_KO": esc(data["date_ko"]),
        "DESCRIPTION": esc(data["description"]), "FAVICON_B64": favicon(repo),
        "ROOT_REL": root_rel, "ARCHIVE_REL": root_rel + "p/briefing/archive/",
        "SCANNED": esc(data["scanned"]), "PICKED": esc(data["picked"]),
        "INTRO": "\n".join("    " + p for p in intro),
        "PICK_ANCHOR": esc(pick_anchor),
        "PICK_TITLE": esc(labels.get(pick_anchor, "오늘 하나만 고른다면")),
        "PICK_LINE": esc(pick_line),
        "TOC_ITEMS": toc, "ITEMS": "\n".join(items_html), "REST_ITEMS": "\n".join(rest_html),
        "FOLLOWUP": followup,
        "DAYNAV": daynav(dates, data["date"], nav_prefix),
    })
    assert_filled(page, "template.html")
    return page


def render_followup(fu):
    """어제 이후 패널 (task-88). 접수 상태 행 + 지난 항목의 후속 한두 줄.

    빈 날에는 빈 문자열을 돌려준다 — 매일 '없음' 이 찍히면 그 자리가 죽는다.
    """
    rows, notes = fu.get("rows") or [], fu.get("notes") or []
    if not rows and not notes:
        return ""
    lis = []
    for r in rows[:4]:
        cls = " done" if r["state"] == "완성" else ""
        title = esc(r["title"])
        link = f'<a href="{esc(r["page"])}">{title}</a>' if r.get("page") else title
        lis.append(f'      <li><span class="st{cls}">{esc(r["state"])}</span>{link}</li>')
    lis += [f'      <li class="note">{esc(n)}</li>' for n in notes[:2]]
    return ('  <div class="followup">\n    <h2>어제 이후</h2>\n    <ul>\n'
            + "\n".join(lis) + "\n    </ul>\n  </div>")


PROFILE_RE = re.compile(r"(<!-- PROFILE:START -->).*?(<!-- PROFILE:END -->)", re.S)


def update_profile(repo):
    """브리핑 소개 페이지(p/liv-briefing/)의 관심사 프로필 구간을 다시 채운다 (task-84).

    프로필은 til 카드에서 자동으로 뽑히므로 손으로 적어 두면 금방 낡는다.
    """
    page = repo / "p/liv-briefing/index.html"
    script = repo / "backlog/assets/interest-profile.py"
    if not page.exists() or not script.exists():
        return
    p = subprocess.run([sys.executable, str(script), "--format", "json", "--index", str(repo / "index.html")],
                       capture_output=True, text=True, timeout=120)
    if p.returncode != 0:
        print(f"  관심사 프로필 추출 실패 — 소개 페이지는 그대로 둔다: {p.stderr.strip()[:200]}", file=sys.stderr)
        return
    prof = json.loads(p.stdout)
    rows = []
    for t in prof["topics"]:
        detail = ", ".join(t["details"][:4])
        rows.append(f'      <li><b>{esc(t["label"] or t["topic"])}</b> {t["share"] * 100:.0f}%'
                    + (f' — {esc(detail)}' if detail else "") + "</li>")
    block = ('  <div class="profile">\n    <ul>\n' + "\n".join(rows) + "\n    </ul>\n"
             f'    <p class="stamp">til {prof["total_articles"]}건에서 자동 추출 · {prof["generated_at"][:10]} 기준 · '
             f'최근 글에 가중치(반감기 {prof["half_life_days"]:.0f}일)</p>\n  </div>')
    text = PROFILE_RE.sub(lambda m: f"{m.group(1)}\n{block}\n  {m.group(2)}", page.read_text(encoding="utf-8"))
    page.write_text(text, encoding="utf-8")
    print(f"  p/liv-briefing/ 관심사 프로필 갱신 ({len(rows)}개 주제)")


def render_archive(repo, data=None):
    """날짜별 회차 목록. 발행 때마다 다시 만든다 — 디렉터리가 진실원본이다.

    끝에 루트 사이드바용 latest.json 도 함께 쓴다. data 는 이번에 렌더한 회차다.
    """
    root = repo / "p/briefing"
    dates = sorted((d.name for d in root.iterdir()
                    if d.is_dir() and re.fullmatch(r"\d{4}-\d{2}-\d{2}", d.name)
                    and (d / "index.html").exists()), reverse=True)
    rows, month = [], None
    for date in dates:
        page = (root / date / "index.html").read_text(encoding="utf-8")
        m = re.search(r'<meta name="description" content="([^"]*)"', page)
        desc = m.group(1) if m else ""
        desc = desc.split("—", 1)[-1].strip() if "—" in desc else desc
        if date[:7] != month:
            month = date[:7]
            rows.append(f'  <h2>{month}</h2>\n  <div class="rows">' if not rows else
                        f'  </div>\n  <h2>{month}</h2>\n  <div class="rows">')
        d = datetime.fromisoformat(date)
        rows.append(f'    <a class="row" data-date="{date}" href="../{date}/"><span class="d">{date[5:]} '
                    f'({"월화수목금토일"[d.weekday()]})</span><span class="t">{esc(desc)}</span></a>')
    if rows:
        rows.append("  </div>")

    # 주간 리캡(task-91)은 일간과 형식이 달라 위쪽에 따로 묶는다.
    recaps = sorted((d.name for d in (root / "recap").iterdir()
                     if d.is_dir() and (d / "index.html").exists()), reverse=True) \
        if (root / "recap").is_dir() else []
    if recaps:
        head = ['  <h2>주간 리캡</h2>', '  <div class="rows">']
        for date in recaps:
            page = (root / "recap" / date / "index.html").read_text(encoding="utf-8")
            m = re.search(r"<title>(.*?) · 주간 리캡</title>", page, re.S)
            head.append(f'    <a class="row" href="../recap/{date}/"><span class="d">{date[5:]}</span>'
                        f'<span class="t">{esc(m.group(1) if m else date)}</span></a>')
        rows = head + ["  </div>"] + rows

    out = repo / "p/briefing/archive/index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    page = fill((repo / "backlog/assets/briefing/archive.html").read_text(encoding="utf-8"),
                {"FAVICON_B64": favicon(repo), "COUNT": str(len(dates)), "ROWS": "\n".join(rows)})
    out.write_text(page, encoding="utf-8")
    print(f"  p/briefing/archive/index.html ({len(dates)}회차)")

    # 루트 사이드바가 '안 읽은 회차가 있는지'(task-93) 와 '오늘 브리핑이 무슨 내용인지'
    # 한 줄(task-104)을 여기서 읽는다. 루트 index.html 을 매일 고쳐 쓰면 AI 요약 잡과
    # 같은 파일을 다투게 되므로 파일로 뺀다.
    latest = dates[0] if dates else None
    out = repo / "p/briefing/latest.json"
    prev = {}
    if out.exists():
        try:
            prev = json.loads(out.read_text(encoding="utf-8"))
        except ValueError:
            prev = {}
    if data and data.get("date") == latest:
        line = (data.get("sidebar") or "").strip()
    else:
        # 과거 회차를 다시 렌더하는 중이면 최신 회차의 한 줄을 덮어쓰지 않는다.
        line = prev.get("line", "") if prev.get("latest") == latest else ""
    out.write_text(
        json.dumps({"latest": latest, "count": len(dates), "line": line},
                   ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    repo = Path(sys.argv[1]).resolve()
    date = (sys.argv[2] if len(sys.argv) > 2 else
            os.environ.get("BRIEFING_DATE") or datetime.now(KST).date().isoformat())
    src = STATE / f"briefing-{date}.json"
    if not src.exists():
        print(f"브리핑 재료가 없다: {src}", file=sys.stderr)
        return 2
    data = json.loads(src.read_text(encoding="utf-8"))

    # 이번 회차를 포함한 날짜 목록으로 이동 내비를 짠다(디렉터리가 아직 없을 수 있다).
    dates = sorted(set(briefing_dates(repo)) | {date})
    for rel, root_rel, prefix in ((Path("p/briefing"), "../../", "./"),
                                  (Path("p/briefing") / date, "../../../", "../")):
        out = repo / rel / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        page = render(data, repo, root_rel, dates, prefix)
        out.write_text(page, encoding="utf-8")
        size = len(page.encode())
        flag = f"  ← 상한 {MAX_BYTES // 1000}KB 초과" if size > MAX_BYTES else ""
        print(f"  {rel}/index.html {size // 1024}KB{flag}")

    # 양옆 회차의 내비만 갈아끼운다(직전 회차의 '다음' 링크가 지금 생긴다).
    i = dates.index(date)
    for nb in [d for d in (dates[i - 1] if i else None,
                           dates[i + 1] if i + 1 < len(dates) else None) if d]:
        st = repatch_daynav(repo, dates, nb)
        if st == "patched":
            print(f"  p/briefing/{nb}/index.html 이동 내비 갱신")
        elif st != "unchanged":
            print(f"  경고: p/briefing/{nb}/index.html 의 이동 내비를 갱신하지 못했다 ({st}) — "
                  f"DAYNAV 마커가 사라졌는지 template.html 을 확인할 것", file=sys.stderr)
    render_archive(repo, data)
    update_profile(repo)
    return 0


if __name__ == "__main__":
    sys.exit(main())
