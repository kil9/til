#!/usr/bin/env python3
"""/p/archive/ 격자 커버용 실제 썸네일 생성.

루트 index.html 의 갤러리 카드를 돌며 각 페이지에 임베드된 가장 큰
이미지(대개 본문 삽화)를 추출해 480x172 WebP 로 p/archive/thumbs/<slug>.webp
에 저장하고, p/archive/index.html 의 THUMBS 매니페스트(마커 구간)를 갱신한다.

- 큰 이미지가 없는 페이지(파비콘뿐)는 건너뛴다 → 격자에서 주제 타일 폴백.
- 알파가 큰 이미지(스티커류)는 흰 배경에 contain, 그 외는 위쪽 바이어스 crop.
- 재실행은 멱등. 새 페이지 추가 후 썸네일을 붙이려면 이 스크립트만 다시 돌린다.

사용법: repo 루트에서  python3 backlog/assets/archive-thumbs.py
"""

import base64
import io
import re
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "p" / "archive" / "index.html"
THUMB_DIR = ROOT / "p" / "archive" / "thumbs"
W, H = 480, 172          # 커버 실표시(최대 ~320px 폭)의 1.5배쯤, object-fit 과 동일 비율
MIN_SRC_BYTES = 8_000    # 이보다 작으면 파비콘/아바타로 보고 썸네일 없음 처리
QUALITY = 72


def gallery_cards():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    for href in re.findall(r'<a class="card"\s+href="([^"]+)"', html):
        slug = href.rstrip("/").split("/")[-1]
        yield slug, ROOT / href.lstrip("./") / "index.html"


def largest_image(page_html):
    best = None
    for m in re.finditer(r"data:image/(?:webp|png|jpeg);base64,([A-Za-z0-9+/=]+)", page_html):
        raw = base64.b64decode(m.group(1))
        if best is None or len(raw) > len(best):
            best = raw
    return best if best and len(best) >= MIN_SRC_BYTES else None


def alpha_ratio(img):
    if img.mode not in ("RGBA", "LA", "PA"):
        return 0.0
    alpha = img.convert("RGBA").getchannel("A").resize((64, 64))
    px = list(alpha.getdata())
    return sum(1 for v in px if v < 32) / len(px)


def make_thumb(raw):
    img = Image.open(io.BytesIO(raw))
    if alpha_ratio(img) > 0.15:
        # 스티커류: 흰 배경에 contain (crop 하면 머리/발이 잘린다)
        canvas = Image.new("RGB", (W, H), "#FFFFFF")
        img = img.convert("RGBA")
        scale = min((H - 16) / img.height, (W - 16) / img.width)
        fit = img.resize((max(1, round(img.width * scale)), max(1, round(img.height * scale))), Image.LANCZOS)
        canvas.paste(fit, ((W - fit.width) // 2, (H - fit.height) // 2), fit)
        return canvas, "contain"
    # 삽화류: 채워서 자르되 위쪽 바이어스(인물이 대개 상단 중앙에 있다)
    img = img.convert("RGB")
    scale = max(W / img.width, H / img.height)
    img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    left = (img.width - W) // 2
    top = round((img.height - H) * 0.42)
    return img.crop((left, top, left + W, top + H)), "crop"


def main():
    THUMB_DIR.mkdir(parents=True, exist_ok=True)
    done, skipped = [], []
    for slug, page in gallery_cards():
        raw = largest_image(page.read_text(encoding="utf-8"))
        if raw is None:
            skipped.append(slug)
            continue
        thumb, mode = make_thumb(raw)
        out = THUMB_DIR / f"{slug}.webp"
        thumb.save(out, "WEBP", quality=QUALITY)
        done.append(slug)
        print(f"  {slug:36s} {len(raw)//1024:4d}KB → {out.stat().st_size//1024:3d}KB ({mode})")

    manifest = "var THUMBS = {" + ",".join(f'"{s}":1' for s in sorted(done)) + "};"
    html = ARCHIVE.read_text(encoding="utf-8")
    new_html, n = re.subn(
        r"(// THUMBS:START\n)[^\n]*(\n\s*// THUMBS:END)",
        lambda m: m.group(1) + "    " + manifest + m.group(2),
        html,
    )
    if n != 1:
        sys.exit("THUMBS 마커를 p/archive/index.html 에서 찾지 못했다")
    ARCHIVE.write_text(new_html, encoding="utf-8")
    print(f"썸네일 {len(done)}건, 타일 폴백 {len(skipped)}건: {', '.join(skipped) or '-'}")


if __name__ == "__main__":
    main()
