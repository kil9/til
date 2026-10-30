#!/usr/bin/env python3
"""수집 — GeekNews 와 Hacker News 에서 후보를 만든다 (task-80, HN 은 task-106).

- GeekNews 메인 피드와 신규 목록(/new?page=N)을 합쳐 후보를 만든다. 메인 피드는 이미
  한번 걸러진 글을, 신규 목록은 막 올라온 글을 보완한다. RSS 는 항목 요약을 준다.
- HN 은 Algolia front_page 엔드포인트 호출 1회로 톱페이지 전원의 점수·댓글수·URL 을
  받는다(실측: 실제 프런트페이지와 29/30 일치). Firebase 는 아이템당 요청이라 배제했다.
- **id 는 GeekNews 만 맨 값이고 HN 은 `hn:` 을 붙인다.** 맨 id = GeekNews 라는 규약이라
  seen.json·points-30d.jsonl·과거 selected-*.json 을 마이그레이션하지 않아도 된다.
  양쪽을 다 접두하면 그 세 곳의 기존 데이터가 전부 미아가 되고, 그 사고는 조용하다
  (seen 필터가 무효화돼 어제 실은 글이 다시 실릴 뿐 에러가 안 난다).
- **추천 백분위는 소스별로 따로 매긴다.** GeekNews 추천수는 한 자리에서 56 수준이고
  HN points 는 13-708 이라 절대값을 섞으면 GeekNews 가 전멸한다.
- 한 소스 수집이 통째로 실패해도 다른 소스로 진행한다. 둘 다 비었을 때만 중단한다.
  BRIEFING_HN=0 이면 HN 은 아예 끈다.
- 첫 페이지에서 끊지 않는다. 빈 페이지가 나올 때까지(또는 MAX_PAGES) 훑는다 —
  파일럿에서 추천 상위 6% 항목이 2페이지에 있었다.
- 이미 처리한 id 는 state/seen.json 으로 거른다. 다만 그렇게 걸러 남은 신규가
  MIN_NEW 미만이면 그날 훑은 목록 전체로 되돌린다(backfill). 매일 발행되는 것이
  중복 회피보다 우선이라는 결정이다 — 새벽에 올라온 글이 적은 날 브리핑이 통째로
  빠지는 것을 막는다. 회차 간 중복은 감수한다.
- 추천 백분위는 state/points-30d.jsonl 의 최근 30일 롤링 분포로 매긴다. 이력이
  얇으면(MIN_HISTORY 미만) 그날 수집분 내부 분위수로 폴백한다.

출력: state/collected-<날짜>.json
"""

import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
STATE = BASE / "state"
NEW_LIST_URL = "https://news.hada.io/new?page={}"
MAIN_LIST_URL = "https://news.hada.io/?page={}"
RSS_URL = "https://news.hada.io/rss/news"
HN_URL = "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage={}"
HN_ITEM_URL = "https://news.ycombinator.com/item?id={}"
HN_LIMIT = 30             # 프런트페이지 한 장
MAX_PAGES = 4
HISTORY_DAYS = 30
MIN_HISTORY = 60          # 이보다 적으면 롤링 분포를 믿지 않는다. 소스별로 따로 본다
MIN_NEW = int(os.environ.get("MIN_NEW", "5"))   # 신규가 이보다 적으면 목록 전체로 backfill
# GeekNews 는 HN 프런트페이지보다 천천히 갈린다. 미선정 글도 seen 에 들어가므로
# 신규가 한 자릿수인 날에는 지난 후보를 다시 열어 두어야 한 번의 판정 누락으로 사라지지 않는다.
MIN_NEW_BY_SOURCE = {"gn": int(os.environ.get("MIN_NEW_GN", "10")), "hn": MIN_NEW}
# 킬 스위치. 아침에 HN 쪽이 이상하면 코드를 되돌리지 않고 이 값만 0 으로 두면
# 그날부터 GeekNews 단독 발행으로 즉시 복귀한다.
HN_ENABLED = os.environ.get("BRIEFING_HN", "1") == "1"
# GeekNews CloudFront 는 2026-08-19 부터 UA 에 liv-briefing 토큰이 있으면 403 을
# 돌려준다. 브라우저 호환 UA 로 요청하되 연락처 토큰은 붙이지 않는다.
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36")
KST = timezone(timedelta(hours=9))

# 행 단위로 잘라 놓고 필드별로 뽑는다. 한 정규식으로 행 전체를 매칭하면 어느
# 행에 필드 하나가 없을 때 lazy 매칭이 다음 행까지 삼켜 그 행이 통째로 사라진다.
ROW_SPLIT_RE = re.compile(r"<div class='topic_row' data-topic-state-id='(\d+)'")
F_TITLE_RE = re.compile(r"<h2 class='topic-title-heading'>(.*?)</h2>", re.S)
F_LINK_RE = re.compile(r"<div class=topictitle>.*?<a href='([^']+)'", re.S)
F_DOMAIN_RE = re.compile(r"<span class=topicurl>\(([^)]*)\)</span>")
F_DESC_RE = re.compile(r"<div class='topicdesc'>.*?class='c99 breakall'>(.*?)</a>", re.S)
F_POINTS_RE = re.compile(r"<span id='tp\d+'>(\d+)</span>")
F_TS_RE = re.compile(r'data-timestamp="(\d+)"')
F_COMMENTS_RE = re.compile(r"data-topic-comment-count='(\d+)'")
ENTRY_RE = re.compile(r"<entry>(.*?)</entry>", re.S)


def fetch(url, retries=3):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=25) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:  # 네트워크는 흔들린다. 마지막 시도에서만 올린다
            if i == retries - 1:
                raise
            print(f"  재시도 {i + 1}/{retries}: {url} ({e})", file=sys.stderr)
            time.sleep(2 * (i + 1))


def strip_tags(s):
    # 엔티티 해제는 html.unescape 에 맡긴다. 손수 만든 치환표는 수치 참조의 제로
    # 패딩 변형(&#039;)을 몰라 그대로 남겼고, 렌더에서 & 가 다시 escape 돼
    # 화면에 "&#039;" 가 노출됐다. 표 순서 탓에 &amp;lt; 가 < 로 이중 디코드되던
    # 문제도 같이 사라진다(unescape 는 한 번만 푼다).
    s = re.sub(r"<[^>]+>", "", s)
    return " ".join(html.unescape(s).split())


# 추적 파라미터. 같은 글이 소스마다 다른 꼬리표를 달고 와서 병합을 방해한다.
TRACKING_RE = re.compile(r"^(utm_\w*|fbclid|gclid|mc_(cid|eid)|ref|source|s|igshid)$", re.I)


def url_key(u):
    """원문 URL 정규화 키. 못 만들면 빈 문자열이고, 그 항목은 병합 대상에서 빠진다.

    Ask HN/Show HN 처럼 외부 링크가 없는 항목이 빈 키를 공유하면 서로 다른 글이
    한 항목으로 합쳐지므로, 빈 키끼리는 절대 묶지 않는다.
    """
    if not u:
        return ""
    try:
        p = urllib.parse.urlsplit(u)
    except ValueError:
        return ""
    if p.scheme not in ("http", "https") or not p.netloc:
        return ""
    host = p.netloc.lower().split("@")[-1]
    for port in (":80", ":443"):
        if host.endswith(port):
            host = host[: -len(port)]
    host = host.removeprefix("www.").rstrip(".")
    path = re.sub(r"/+$", "", p.path) or "/"
    query = sorted((k, v) for k, v in urllib.parse.parse_qsl(p.query, keep_blank_values=True)
                   if not TRACKING_RE.match(k))
    return urllib.parse.urlunsplit(("https", host, path, urllib.parse.urlencode(query), ""))


def hn_front_page():
    """HN 프런트페이지. 호출 1회로 점수·댓글수·URL 을 받는다."""
    data = json.loads(fetch(HN_URL.format(HN_LIMIT)))
    items = {}
    for h in data.get("hits", []):
        oid = str(h.get("objectID") or "")
        title = (h.get("title") or "").strip()
        if not oid or not title:
            continue
        discussion = HN_ITEM_URL.format(oid)
        # Ask/Show HN 은 외부 링크가 없다. 그 경우 원문 자리에 토론 페이지를 세운다.
        source_url = h.get("url") or discussion
        items[f"hn:{oid}"] = {
            "id": f"hn:{oid}",
            "source": "hn",
            "title": title,
            "source_url": source_url,
            "domain": urllib.parse.urlsplit(source_url).netloc.lower().removeprefix("www.")
                      or "news.ycombinator.com",
            "desc": (h.get("story_text") or "")[:600],
            "points": int(h.get("points") or 0),
            "comments": int(h.get("num_comments") or 0),
            "published": (h.get("created_at") or "")[:16],
            "topic_url": discussion,
            "list_page": 1,
            "url_key": url_key(h.get("url")),
        }
    print(f"  HN 프런트페이지 {len(items)}건")
    return items


def list_pages(url_template=NEW_LIST_URL, max_pages=MAX_PAGES, label="신규 목록"):
    """목록 페이지에서 추천수·순서를 긁는다. 빈 페이지를 만나면 멈춘다."""
    items = {}
    for page in range(1, max_pages + 1):
        html = fetch(url_template.format(page))
        marks = list(ROW_SPLIT_RE.finditer(html))
        if not marks:
            break
        for i, m in enumerate(marks):
            tid = m.group(1)
            chunk = html[m.end(): marks[i + 1].start() if i + 1 < len(marks) else len(html)]
            title, points, ts = F_TITLE_RE.search(chunk), F_POINTS_RE.search(chunk), F_TS_RE.search(chunk)
            if not (title and points and ts) or tid in items:
                continue
            link, domain = F_LINK_RE.search(chunk), F_DOMAIN_RE.search(chunk)
            desc, comments = F_DESC_RE.search(chunk), F_COMMENTS_RE.search(chunk)
            source_url = link.group(1) if link else f"https://news.hada.io/topic?id={tid}"
            items[tid] = {
                # GeekNews 는 맨 id 다. 접두하면 기존 seen·백분위 이력이 통째로 미아가 된다.
                "id": tid,
                "source": "gn",
                "title": strip_tags(title.group(1)),
                "source_url": source_url,
                "url_key": url_key(link.group(1)) if link else "",
                "domain": domain.group(1) if domain else "news.hada.io",
                "desc": strip_tags(desc.group(1)) if desc else "",
                "points": int(points.group(1)),
                "comments": int(comments.group(1)) if comments else 0,
                "published": datetime.fromtimestamp(int(ts.group(1)), KST).isoformat(timespec="minutes"),
                "topic_url": f"https://news.hada.io/topic?id={tid}",
                "list_page": page,
                "list_kind": label,
            }
        print(f"  {label} {page}쪽: {len(marks)}건")
    return items


def rss_summaries():
    xml = fetch(RSS_URL)
    out = {}
    for body in ENTRY_RE.findall(xml):
        m = re.search(r"topic\?id=(\d+)", body)
        if not m:
            continue
        c = re.search(r"<content[^>]*><!\[CDATA\[(.*?)\]\]></content>", body, re.S)
        out[m.group(1)] = strip_tags(c.group(1))[:600] if c else ""
    return out


def load_json(path, default):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print(f"  {path.name} 파손 — 기본값으로 진행", file=sys.stderr)
    return default


def points_history(now):
    """최근 HISTORY_DAYS 일치 추천수 표본을 소스별로. 항목당 마지막 관측값만 쓴다.

    source 필드가 없는 옛 레코드는 GeekNews 다(HN 이전에 쌓인 것뿐이다).
    """
    path = STATE / "points-30d.jsonl"
    cutoff = (now - timedelta(days=HISTORY_DAYS)).date().isoformat()
    latest, keep = {"gn": {}, "hn": {}}, []
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("date", "") < cutoff:
                continue
            keep.append(line)
            latest.setdefault(rec.get("source", "gn"), {})[rec["id"]] = rec["points"]
    return latest, keep, path


def merge_duplicates(gn_items, hn_items):
    """같은 원문이 양쪽에 오른 것을 한 항목으로 합친다. 남는 쪽은 언제나 GeekNews 다.

    링크는 GeekNews 논의 페이지만 남기고 HN 쪽 점수는 `also` 로 달아 함께 보인다.
    """
    by_key = {it["url_key"]: it for it in gn_items if it.get("url_key")}
    out, merged = list(gn_items), 0
    for it in hn_items:
        gn = by_key.get(it["url_key"]) if it.get("url_key") else None
        if gn is None:
            out.append(it)
            continue
        gn["also"] = {"source": "hn", "points": it["points"], "comments": it["comments"],
                      "percentile": it.get("percentile"), "url": it["topic_url"]}
        merged += 1
    return out, merged


def percentile_rank(points, sample):
    """상위 몇 %인가. 낮을수록 인기가 높다. 동점은 절반만 앞선 것으로 센다."""
    if not sample:
        return 100.0
    higher = sum(1 for p in sample if p > points)
    ties = sum(1 for p in sample if p == points)
    return round(100.0 * (higher + ties / 2) / len(sample), 1)


def main():
    now = datetime.now(KST)
    today = now.date().isoformat()
    STATE.mkdir(exist_ok=True)

    print("GeekNews 수집")
    items = {}
    try:
        groups = []
        for label, url, pages in (("신규 목록", NEW_LIST_URL, MAX_PAGES),
                                  ("메인 피드", MAIN_LIST_URL, 1)):
            try:
                groups.append(list_pages(url, pages, label))
            except Exception as e:
                print(f"  GeekNews {label} 실패 — 다른 목록으로 계속: {e}", file=sys.stderr)
        for group in groups:
            items.update(group)
        if not items:
            raise RuntimeError("두 목록에서 한 건도 못 긁었다 — 마크업이 바뀌었는지 확인할 것")
        print(f"  GeekNews 중복 제거 후 {len(items)}건")
        try:
            summaries = rss_summaries()
        except Exception as e:
            # 목록의 설명만으로도 선별은 가능하다. RSS 보강 하나 때문에 그날 회차를
            # 버리지 않는다.
            print(f"  GeekNews RSS 수집 실패 — 목록 설명으로 진행: {e}", file=sys.stderr)
            summaries = {}
        for tid, it in items.items():
            it["summary"] = summaries.get(tid, "")
    except Exception as e:
        print(f"  GeekNews 수집 실패 — HN 으로 계속: {e}", file=sys.stderr)

    # 어느 한쪽도 필수 소스가 아니다. 한쪽이 막혀도 다른 쪽으로 그날 회차를 만든다.
    hn = {}
    if not HN_ENABLED:
        print("  BRIEFING_HN=0 — HN 수집을 건너뛴다")
    else:
        try:
            hn = hn_front_page()
        except Exception as e:
            print(f"  HN 수집 실패 — GeekNews 단독으로 진행: {e}", file=sys.stderr)
    if not items and not hn:
        print("두 소스에서 한 건도 못 모았다 — 발행 중단", file=sys.stderr)
        return 2
    by_source = {"gn": items, "hn": hn}

    # 추천 이력 갱신(오늘 관측치를 기록)한 뒤 소스별로 백분위를 매긴다. 소스를 섞으면
    # HN points(수백)가 GeekNews 추천수(한 자리)를 통째로 덮어 GeekNews 가 전멸한다.
    latest, keep, hist_path = points_history(now)
    for src, group in by_source.items():
        for it in group.values():
            seen_pts = latest.setdefault(src, {})
            seen_pts[it["id"]] = max(seen_pts.get(it["id"], 0), it["points"])
            keep.append(json.dumps({"date": today, "id": it["id"], "source": src,
                                    "points": it["points"]}, ensure_ascii=False))
    hist_path.write_text("\n".join(keep) + "\n", encoding="utf-8")

    basis, sizes = {}, {}
    for src, group in by_source.items():
        if not group:
            continue
        sample = list(latest.get(src, {}).values())
        basis[src] = "rolling-30d"
        if len(sample) < MIN_HISTORY:
            sample = [it["points"] for it in group.values()]
            basis[src] = "today-only"
            print(f"  {src} 이력 {len(latest.get(src, {}))}건뿐 — 그날 수집분 내부 분위수로 폴백")
        sizes[src] = len(sample)
        for it in group.values():
            it["percentile"] = percentile_rank(it["points"], sample)

    # 신규 판정과 backfill 은 소스별이다. 합산하면 HN 30건 때문에 GeekNews 가 얇은 날에도
    # backfill 이 안 돌아 그날 회차가 통째로 HN 이 된다.
    seen = set(load_json(STATE / "seen.json", {"ids": []})["ids"])
    backfilled = []
    fresh_by_source = {}
    for src, group in by_source.items():
        if not group:
            fresh_by_source[src] = []
            continue
        fresh = [it for it in group.values() if it["id"] not in seen]
        print(f"  {src}: 훑은 {len(group)}건 중 신규 {len(fresh)}건")
        # 신규가 얇은 날엔 목록 전체로 되돌린다. 발행이 끊기는 것보다 회차 간 중복이 낫다.
        min_new = MIN_NEW_BY_SOURCE.get(src, MIN_NEW)
        if len(fresh) < min_new:
            fresh = list(group.values())
            backfilled.append(src)
            print(f"  {src}: 신규 {min_new}건 미만 — 전체 {len(fresh)}건으로 backfill (중복 허용)")
        fresh_by_source[src] = fresh

    merged_items, merged = merge_duplicates(fresh_by_source["gn"], fresh_by_source["hn"])
    if merged:
        print(f"  같은 원문 {merged}건을 GeekNews 쪽으로 합쳤다")

    merged_items.sort(key=lambda it: (it["percentile"], -it["points"]))
    out = {
        "date": today,
        "collected_at": now.isoformat(timespec="minutes"),
        "scanned": sum(len(g) for g in by_source.values()),
        "scanned_by_source": {s: len(g) for s, g in by_source.items()},
        "percentile_basis": basis,
        "sample_size": sizes,
        "backfilled": backfilled,
        "merged": merged,
        "items": merged_items,
    }
    path = STATE / f"collected-{today}.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    counts = {s: sum(1 for it in merged_items if it["source"] == s) for s in ("gn", "hn")}
    mark = f" · backfill {'/'.join(backfilled)}" if backfilled else ""
    print(f"  → {path.name} ({len(merged_items)}건 = GN {counts['gn']} + HN {counts['hn']}, "
          f"백분위 기준 {basis}{mark})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
