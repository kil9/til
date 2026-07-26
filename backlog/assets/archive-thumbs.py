#!/usr/bin/env python3
"""/p/archive/ 격자 커버 썸네일과 공유 미리보기(og:image) 생성.

루트 index.html 의 갤러리 카드를 돌며 각 페이지에 임베드된 가장 큰
이미지(대개 본문 삽화)를 대표 이미지로 뽑아, 같은 추출 결과에서 두 판본을 굽는다.

    p/archive/thumbs/<slug>.webp   480x172  격자 커버
    og/<slug>.jpg                  1200x630 공유 미리보기(TASK-100)

그리고 p/archive/index.html 의 THUMBS 매니페스트(마커 구간)를 갱신한다.

- 큰 이미지가 없는 페이지(파비콘뿐)는 건너뛴다 → 격자에서 주제 타일 폴백, OG 는
  사이트 공통 1장(og/default.jpg)을 공유한다. 글마다 만들지 않는다.
- 대표 이미지가 부적절하면 backlog/assets/page-image-override/<slug>.<확장자> 로
  갈아끼운다(썸네일·OG 공통 훅).
- 알파가 큰 이미지(스티커류)는 흰 배경에 contain, 그 외는 위쪽 바이어스 crop.
- 재실행은 멱등. 카드에서 사라진 슬러그의 생성물은 지운다.
- 페이지 head 의 og:image 메타를 박는 것은 backlog/assets/relink-pages.py 몫이라,
  발행 시 이 스크립트를 먼저 돌리고 그 다음에 relink-pages.py 를 돌린다.

사용법: repo 루트에서  python3 backlog/assets/archive-thumbs.py
"""

import base64
import io
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "p" / "archive" / "index.html"
THUMB_DIR = ROOT / "p" / "archive" / "thumbs"
OG_DIR = ROOT / "og"                       # 공유 미리보기 이미지(TASK-100)
OVERRIDE_DIR = ROOT / "backlog" / "assets" / "page-image-override"
W, H = 480, 172          # 커버 실표시(최대 ~320px 폭)의 1.5배쯤, object-fit 과 동일 비율
OG_W, OG_H = 1200, 630   # og:image 표준 비율(1.91:1)
OG_QUALITY = 82          # OG 는 JPEG 다 — 아래 OG_EXT 주석 참조
MIN_SRC_BYTES = 8_000    # 이보다 작으면 파비콘/아바타로 보고 썸네일 없음 처리
QUALITY = 72
OG_FALLBACK = "default"  # 대표 이미지가 없는 글이 공유할 사이트 공통 1장
# OG 이미지만 JPEG 로 굽는다. 사이트의 다른 이미지는 전부 WebP 지만, og:image 는
# 우리가 아니라 남의 크롤러(카카오톡·X·Slack)가 읽는다. Slack·Facebook 은 WebP 를
# 읽지만 카카오톡·X 는 지원이 불확실해, 미리보기가 통째로 사라지는 위험보다
# 몇십 KB 를 지불하는 쪽이 낫다. 단일 파일 원칙(§2-1)은 페이지 안의 자산 이야기라
# 사이드카인 OG 이미지에는 애초에 적용되지 않는다.
OG_EXT = "jpg"


def gallery_cards():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    for href in re.findall(r'<a class="card"\s+href="([^"]+)"', html):
        slug = href.rstrip("/").split("/")[-1]
        yield slug, ROOT / href.lstrip("./") / "index.html"


def override_src(slug):
    """수동 오버라이드 훅. backlog/assets/page-image-override/<slug>.<확장자> 가 있으면
    본문에서 뽑은 삽화 대신 그 파일을 대표 이미지로 쓴다(썸네일·OG 공통).
    대표 이미지가 부적절하거나 본문에 삽화가 없는 글에 쓴다."""
    if not OVERRIDE_DIR.is_dir():
        return None
    for path in sorted(OVERRIDE_DIR.glob(f"{slug}.*")):
        if path.suffix.lower() in (".webp", ".png", ".jpg", ".jpeg"):
            return path.read_bytes()
    return None


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


def fit(raw, w, h, pad):
    """대표 이미지를 w x h 로 맞춘다. 알파가 큰 스티커류는 흰 배경에 contain,
    그 외 삽화류는 채워서 자르되 위쪽 바이어스(인물이 대개 상단 중앙에 있다)."""
    img = Image.open(io.BytesIO(raw))
    if alpha_ratio(img) > 0.15:
        # 스티커류: crop 하면 머리/발이 잘린다
        canvas = Image.new("RGB", (w, h), "#FFFFFF")
        img = img.convert("RGBA")
        scale = min((h - pad) / img.height, (w - pad) / img.width)
        small = img.resize((max(1, round(img.width * scale)), max(1, round(img.height * scale))), Image.LANCZOS)
        canvas.paste(small, ((w - small.width) // 2, (h - small.height) // 2), small)
        return canvas, "contain"
    img = img.convert("RGB")
    scale = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    left = (img.width - w) // 2
    top = round((img.height - h) * 0.42)
    return img.crop((left, top, left + w, top + h)), "crop"


def make_thumb(raw):
    return fit(raw, W, H, 16)


def make_og(raw):
    return fit(raw, OG_W, OG_H, 40)


def make_og_fallback():
    """대표 이미지가 없는 글이 공유하는 사이트 공통 1장. 리브 아바타 + 사이트 이름.
    글마다 만들지 않는다. 입력이 고정이라 재실행해도 같은 바이트가 나온다."""
    canvas = Image.new("RGB", (OG_W, OG_H), "#FFFFFF")
    liv = Image.open(backlog_asset("liv/liv-final-chibi.webp")).convert("RGB")
    height = 520
    liv = liv.resize((round(liv.width * height / liv.height), height), Image.LANCZOS)
    canvas.paste(liv, (130, (OG_H - height) // 2))

    draw = ImageDraw.Draw(canvas)
    x = 130 + liv.width + 90
    draw.text((x, 268), "today i learned", font=_font(76), fill="#1B2027")
    draw.text((x, 366), "til.kil9.dev", font=_font(38), fill="#6E7A86")
    return canvas


def save_og(img, path):
    img.save(path, "JPEG", quality=OG_QUALITY, optimize=True, progressive=True)


def _font(size):
    for path in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def backlog_asset(rel):
    return ROOT / "backlog" / "assets" / rel


def main():
    THUMB_DIR.mkdir(parents=True, exist_ok=True)
    OG_DIR.mkdir(parents=True, exist_ok=True)
    done, skipped, og_done = [], [], []
    for slug, page in gallery_cards():
        raw = override_src(slug) or largest_image(page.read_text(encoding="utf-8"))
        if raw is None:
            skipped.append(slug)
            continue
        thumb, mode = make_thumb(raw)
        out = THUMB_DIR / f"{slug}.webp"
        thumb.save(out, "WEBP", quality=QUALITY)
        og_out = OG_DIR / f"{slug}.{OG_EXT}"
        save_og(make_og(raw)[0], og_out)
        done.append(slug)
        og_done.append(slug)
        print(f"  {slug:36s} {len(raw)//1024:4d}KB → 썸네일 {out.stat().st_size//1024:3d}KB"
              f" · OG {og_out.stat().st_size//1024:3d}KB ({mode})")

    fallback = OG_DIR / f"{OG_FALLBACK}.{OG_EXT}"
    save_og(make_og_fallback(), fallback)

    # 대상에서 빠진 슬러그(카드가 사라졌거나 대표 이미지가 없어진 경우)의 생성물은
    # 남겨 두면 아무도 안 가리키는 유령 파일이 된다.
    keep = set(done)
    for stale in sorted(set(p.stem for p in OG_DIR.glob(f"*.{OG_EXT}")) - keep - {OG_FALLBACK}):
        (OG_DIR / f"{stale}.{OG_EXT}").unlink()
        print(f"  삭제(대상 아님) og/{stale}.{OG_EXT}")
    for stale in sorted(set(p.stem for p in THUMB_DIR.glob("*.webp")) - keep):
        (THUMB_DIR / f"{stale}.webp").unlink()
        print(f"  삭제(대상 아님) thumbs/{stale}.webp")

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
    print(f"OG 이미지 {len(og_done)}건 + 공통 폴백 1건({fallback.stat().st_size // 1024}KB) → og/")
    print("  ↳ 페이지 head 의 og:image 반영은 backlog/assets/relink-pages.py 가 한다")


if __name__ == "__main__":
    main()
