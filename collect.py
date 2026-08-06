#!/usr/bin/env python3
"""GeekNews 수집 — 새 소식 목록 + RSS 요약을 합쳐 후보를 만든다 (task-80).

- 목록(/new?page=N)은 추천수(points)와 노출 순서를 주고, RSS 는 항목 요약을 준다.
  RSS 만으로는 인기 순위를 알 수 없어 둘을 id 로 합친다.
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
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
STATE = BASE / "state"
LIST_URL = "https://news.hada.io/new?page={}"
RSS_URL = "https://news.hada.io/rss/news"
MAX_PAGES = 4
HISTORY_DAYS = 30
MIN_HISTORY = 60          # 이보다 적으면 롤링 분포를 믿지 않는다
MIN_NEW = int(os.environ.get("MIN_NEW", "5"))   # 신규가 이보다 적으면 목록 전체로 backfill
UA = "Mozilla/5.0 (X11; Linux x86_64) liv-briefing/1.0 (+https://til.kil9.dev/)"
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


def list_pages():
    """목록 페이지에서 추천수·순서를 긁는다. 빈 페이지를 만나면 멈춘다."""
    items = {}
    for page in range(1, MAX_PAGES + 1):
        html = fetch(LIST_URL.format(page))
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
            items[tid] = {
                "id": tid,
                "title": strip_tags(title.group(1)),
                "source_url": link.group(1) if link else f"https://news.hada.io/topic?id={tid}",
                "domain": domain.group(1) if domain else "news.hada.io",
                "desc": strip_tags(desc.group(1)) if desc else "",
                "points": int(points.group(1)),
                "comments": int(comments.group(1)) if comments else 0,
                "published": datetime.fromtimestamp(int(ts.group(1)), KST).isoformat(timespec="minutes"),
                "topic_url": f"https://news.hada.io/topic?id={tid}",
                "list_page": page,
            }
        print(f"  목록 {page}쪽: {len(marks)}건")
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
    """최근 HISTORY_DAYS 일치 추천수 표본. 항목당 마지막 관측값만 쓴다."""
    path = STATE / "points-30d.jsonl"
    cutoff = (now - timedelta(days=HISTORY_DAYS)).date().isoformat()
    latest, keep = {}, []
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
            latest[rec["id"]] = rec["points"]
    return latest, keep, path


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
    items = list_pages()
    if not items:
        print("목록에서 한 건도 못 긁었다 — 마크업이 바뀌었는지 확인할 것", file=sys.stderr)
        return 2
    summaries = rss_summaries()
    for tid, it in items.items():
        it["summary"] = summaries.get(tid, "")

    seen = set(load_json(STATE / "seen.json", {"ids": []})["ids"])
    fresh = [it for it in items.values() if it["id"] not in seen]
    print(f"  훑은 {len(items)}건 중 신규 {len(fresh)}건")

    # 신규가 얇은 날엔 목록 전체로 되돌린다. 발행이 끊기는 것보다 회차 간 중복이 낫다.
    backfilled = len(fresh) < MIN_NEW
    if backfilled:
        fresh = list(items.values())
        print(f"  신규 {MIN_NEW}건 미만 — 목록 전체 {len(fresh)}건으로 backfill (중복 허용)")

    # 추천 이력 갱신(오늘 관측치를 기록)한 뒤 백분위를 매긴다.
    latest, keep, hist_path = points_history(now)
    for it in items.values():
        latest[it["id"]] = max(latest.get(it["id"], 0), it["points"])
        keep.append(json.dumps({"date": today, "id": it["id"], "points": it["points"]}, ensure_ascii=False))
    hist_path.write_text("\n".join(keep) + "\n", encoding="utf-8")

    sample = list(latest.values())
    basis = "rolling-30d"
    if len(sample) < MIN_HISTORY:
        sample = [it["points"] for it in items.values()]
        basis = "today-only"
        print(f"  이력 {len(latest)}건뿐 — 그날 수집분 내부 분위수로 폴백")
    for it in fresh:
        it["percentile"] = percentile_rank(it["points"], sample)

    fresh.sort(key=lambda it: (it["percentile"], -it["points"]))
    out = {
        "date": today,
        "collected_at": now.isoformat(timespec="minutes"),
        "scanned": len(items),
        "percentile_basis": basis,
        "sample_size": len(sample),
        "backfilled": backfilled,
        "items": fresh,
    }
    path = STATE / f"collected-{today}.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    mark = " · backfill" if backfilled else ""
    print(f"  → {path.name} ({len(fresh)}건, 백분위 기준 {basis}/{len(sample)}표본{mark})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
