#!/usr/bin/env python3
"""til 갤러리 카드에서 관심사 프로필을 뽑는다 (task-79).

리브 아침 브리핑(m-8)의 선별 단계가 "관리자가 무엇에 관심이 있는가"를
프롬프트로 받아야 하는데, 파일럿에서는 그 분포를 손으로 셌다. 글이 쌓일수록
손계산이 낡으므로 루트 index.html 을 진실원본 삼아 매 실행마다 다시 뽑는다.

입력: 루트 index.html 의 <a class="card"> (data-topic, data-date, .tag, h2, p)
출력:
  --format prompt (기본)  선별 프롬프트에 그대로 붙여 넣는 텍스트 블록
  --format json           같은 내용의 구조화 데이터

가중치: 최근 글에 지수 감쇠 가중(반감기 90일)을 준다. 계단식("최근 3개월 2배")도
검토했으나 til 은 발행이 몰아치는 패턴이라 경계 하루 차이로 주제 순위가 튄다.
지수 감쇠는 같은 "최근을 두 배로" 를 매끄럽게 준다(90일 전 글이 정확히 0.5배).
누적 분포도 함께 출력해 선별 모델이 장기 관심사와 최근 관심사를 구분할 수 있게 한다.

사용법: repo 루트에서  python3 backlog/assets/interest-profile.py [--format json]
       참조 시각 고정이 필요하면 --now 2026-07-26T09:00
"""

import argparse
import json
import math
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "index.html"
HALF_LIFE_DAYS = 90.0
RECENT_TITLES = 12   # 프롬프트에 싣는 최근 글 제목 수
KST = timezone(timedelta(hours=9))

CARD_RE = re.compile(
    r'<a class="card"\s+href="(?P<href>[^"]+)"\s+data-date="(?P<date>[^"]+)"'
    r'\s+data-topic="(?P<topic>[^"]+)">(?P<body>.*?)</a>',
    re.S,
)
TAG_RE = re.compile(r'<span class="tag">(.*?)</span>', re.S)
H2_RE = re.compile(r"<h2>(.*?)</h2>", re.S)
P_RE = re.compile(r"<p>(.*?)</p>", re.S)


def text(raw):
    """카드 안의 인라인 마크업·엔티티를 걷어낸 평문."""
    s = re.sub(r"<[^>]+>", "", raw)
    for a, b in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"'), ("&#39;", "'")):
        s = s.replace(a, b)
    return " ".join(s.split())


def parse_cards(html):
    cards = []
    for m in CARD_RE.finditer(html):
        body = m.group("body")
        tag = text(TAG_RE.search(body).group(1)) if TAG_RE.search(body) else ""
        chip, _, detail = tag.partition("·")
        title_m, desc_m = H2_RE.search(body), P_RE.search(body)
        cards.append(
            {
                "slug": m.group("href").rstrip("/").split("/")[-1],
                "url": m.group("href").lstrip("."),
                "date": m.group("date"),
                "topic": m.group("topic"),
                "chip": chip.strip(),
                "detail": detail.strip(),
                "title": text(title_m.group(1)) if title_m else "",
                "summary": text(desc_m.group(1)) if desc_m else "",
            }
        )
    return cards


def weight(date_str, now):
    """반감기 HALF_LIFE_DAYS 의 지수 감쇠. 미래 날짜는 1.0 으로 clamp."""
    try:
        dt = datetime.fromisoformat(date_str).replace(tzinfo=KST)
    except ValueError:
        return 1.0
    age_days = max(0.0, (now - dt).total_seconds() / 86400)
    return 0.5 ** (age_days / HALF_LIFE_DAYS)


def build(cards, now):
    topics = {}
    for c in cards:
        t = topics.setdefault(
            c["topic"], {"topic": c["topic"], "label": c["chip"], "count": 0, "weighted": 0.0, "details": []}
        )
        t["count"] += 1
        t["weighted"] += weight(c["date"], now)
        if c["detail"]:
            t["details"].append(c["detail"])
        if not t["label"]:
            t["label"] = c["chip"]

    total_w = sum(t["weighted"] for t in topics.values()) or 1.0
    for t in topics.values():
        t["weighted"] = round(t["weighted"], 2)
        t["share"] = round(t["weighted"] / total_w, 3)
        # 세부 축은 최근 것이 앞에 오도록 (cards 가 최신순). 같은 세부가
        # 여러 글에 걸치는 경우가 흔하므로(USB 진단 3건 등) 중복은 접는다.
        t["details"] = list(dict.fromkeys(t["details"]))[:8]

    ranked = sorted(topics.values(), key=lambda t: (-t["weighted"], -t["count"], t["topic"]))
    recent = sorted(cards, key=lambda c: c["date"], reverse=True)[:RECENT_TITLES]
    return {
        "generated_at": now.isoformat(timespec="minutes"),
        "half_life_days": HALF_LIFE_DAYS,
        "total_articles": len(cards),
        "topics": ranked,
        "recent": [
            {"date": c["date"][:10], "title": c["title"], "topic": c["topic"], "url": c["url"]} for c in recent
        ],
        # 전체 목록. 브리핑의 'til 연관' 판정처럼 최근 것만으로는 부족한 쪽이 쓴다.
        "articles": [
            {"date": c["date"][:10], "title": c["title"], "topic": c["topic"], "url": c["url"],
             "detail": c["detail"], "summary": c["summary"]}
            for c in sorted(cards, key=lambda c: c["date"], reverse=True)
        ],
    }


def render_prompt(p):
    out = [
        f"# 관리자 관심사 프로필 (til {p['total_articles']}건에서 자동 추출, {p['generated_at'][:10]} 기준)",
        "",
        f"주제 비중은 최근 글에 가중치를 준 값이다(반감기 {p['half_life_days']:.0f}일). "
        "누적 건수와 함께 보고, 둘이 어긋나면 최근 쪽을 우선한다.",
        "",
    ]
    for t in p["topics"]:
        line = f"- {t['label'] or t['topic']} ({t['topic']}): 비중 {t['share'] * 100:.0f}%, 누적 {t['count']}건"
        if t["details"]:
            line += "\n  최근 세부: " + ", ".join(t["details"][:5])
        out.append(line)
    out += ["", "## 최근 글 제목", ""]
    out += [f"- {c['date']} [{c['topic']}] {c['title']}" for c in p["recent"]]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="til 카드에서 관심사 프로필 추출")
    ap.add_argument("--format", choices=("prompt", "json"), default="prompt")
    ap.add_argument("--now", help="참조 시각(ISO, KST). 생략하면 현재 시각")
    ap.add_argument("--index", default=str(INDEX), help="갤러리 index.html 경로")
    args = ap.parse_args()

    now = datetime.fromisoformat(args.now).replace(tzinfo=KST) if args.now else datetime.now(KST)
    cards = parse_cards(Path(args.index).read_text(encoding="utf-8"))
    if not cards:
        print("카드를 하나도 찾지 못했다 — index.html 의 카드 마크업이 바뀌었는지 확인할 것", file=sys.stderr)
        return 1
    profile = build(cards, now)
    if args.format == "json":
        print(json.dumps(profile, ensure_ascii=False, indent=2))
    else:
        print(render_prompt(profile))
    return 0


if __name__ == "__main__":
    sys.exit(main())
