#!/usr/bin/env python3
"""흰 배경 생성물 -> 투명 배경 + 흰 다이컷 테두리 WebP.

numpy 없이 PIL 만으로 동작한다.
  1) 네 모서리에서 flood fill 로 '바깥 흰 영역'만 투명화 (내부 흰색은 보존)
  2) 알파를 dilate 해 실루엣 바깥으로 흰 띠를 두른다
  3) 콘텐츠 바운딩박스로 crop 후 정사각 캔버스에 여백 두고 배치
"""
import sys
from PIL import Image, ImageFilter, ImageDraw


def outer_mask(img, tol=18):
    """바깥 배경(흰색)을 1, 캐릭터를 0 으로 하는 마스크."""
    w, h = img.size
    # 흰색 근사 픽셀만 seed 대상으로: L 채널 임계
    gray = img.convert("L")
    # 임계 이상(밝은) 픽셀 = 잠재 배경
    bg_cand = gray.point(lambda v: 255 if v >= 255 - tol else 0, mode="L")
    # flood fill: 모서리에서 시작해 연결된 밝은 영역만 채운다
    mask = Image.new("L", (w + 2, h + 2), 0)
    filled = bg_cand.copy()
    for seed in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        if filled.getpixel(seed) == 255:
            ImageDraw.floodfill(filled, seed, 128, thresh=0)
    # 128 로 칠해진 곳만 바깥 배경
    return filled.point(lambda v: 255 if v == 128 else 0, mode="L")


def diecut(src, dst, size=512, border=10, pad=8, quality=80):
    img = Image.open(src).convert("RGB")
    bg = outer_mask(img)
    alpha = bg.point(lambda v: 0 if v else 255, mode="L")

    # 잔 노이즈 제거 후 테두리용 dilate
    alpha = alpha.filter(ImageFilter.MedianFilter(3))
    ring = alpha.filter(ImageFilter.MaxFilter(2 * border + 1))

    rgba = img.convert("RGBA")
    # 테두리 영역은 흰색으로 칠하고, 그 위에 원본을 알파 합성
    plate = Image.new("RGBA", img.size, (255, 255, 255, 0))
    plate.putalpha(ring)
    plate.paste(rgba, (0, 0), alpha)

    box = plate.getbbox()
    plate = plate.crop(box)
    # 정사각 캔버스
    side = max(plate.size)
    canvas = Image.new("RGBA", (side, side), (255, 255, 255, 0))
    canvas.paste(plate, ((side - plate.width) // 2, (side - plate.height) // 2))
    inner = size - 2 * pad
    canvas = canvas.resize((inner, inner), Image.LANCZOS)
    out = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    out.paste(canvas, (pad, pad))
    out.save(dst, "WEBP", quality=quality, method=6)
    return out


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    size = int(sys.argv[3]) if len(sys.argv) > 3 else 512
    border = int(sys.argv[4]) if len(sys.argv) > 4 else 10
    diecut(src, dst, size=size, border=border)
    import os
    print(f"{dst}  {os.path.getsize(dst)/1024:.1f}KB")
