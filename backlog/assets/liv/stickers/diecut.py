#!/usr/bin/env python3
"""흰 배경 생성물 -> 투명 배경 + 흰 다이컷 테두리 WebP.

numpy 없이 PIL 만으로 동작한다.
  1) 네 모서리에서 flood fill 로 '바깥 흰 영역'만 투명화 (내부 흰색은 보존)
  2) 알파를 dilate 해 실루엣 바깥으로 흰 띠를 두른다
  3) 콘텐츠 bbox 로 crop 후 **긴 변을 목표 크기로 정규화**(종횡비 유지, 정사각 강제 없음)

정사각 캔버스로 패딩하지 않는 이유: 보이지 않는 투명 여백이 본문 인라인 배치에서
텍스트 간격을 어긋나게 한다. 설정화 페이지 그리드는 object-fit: contain 으로 흡수한다.

QA: bbox 내부의 투명 픽셀 비율을 함께 출력한다. 순백 소품에 flood fill 이 새어
구멍이 뚫리면 이 값이 튀므로 육안 검수 전에 기계적으로 걸러낼 수 있다.
"""
import os
import sys
from PIL import Image, ImageFilter, ImageDraw

# 출력 긴 변 기준 링 두께 (512 -> 10px, 256 -> 5px 로 같은 비율)
RING_RATIO = 10 / 512


def outer_mask(img, tol=18):
    """바깥 배경(흰색)을 255, 캐릭터를 0 으로 하는 마스크."""
    w, h = img.size
    gray = img.convert("L")
    bg_cand = gray.point(lambda v: 255 if v >= 255 - tol else 0, mode="L")
    filled = bg_cand.copy()
    for seed in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        if filled.getpixel(seed) == 255:
            ImageDraw.floodfill(filled, seed, 128, thresh=0)
    return filled.point(lambda v: 255 if v == 128 else 0, mode="L")


def hole_ratio(alpha):
    """실루엣 bbox 안에서 투명한 픽셀의 비율. 내부 구멍 탐지용."""
    box = alpha.getbbox()
    if not box:
        return 1.0
    crop = alpha.crop(box)
    hist = crop.histogram()
    total = crop.width * crop.height
    return sum(hist[:128]) / total


def diecut(src, dst, long_side=512, quality=80):
    img = Image.open(src).convert("RGB")
    bg = outer_mask(img)
    alpha = bg.point(lambda v: 0 if v else 255, mode="L")
    alpha = alpha.filter(ImageFilter.MedianFilter(3))

    # 캐릭터만 먼저 오려 bbox 로 자르고 출력 크기로 줄인 뒤, 그 해상도에서 링을 두른다.
    # 원본 해상도에서 dilate 하면 MaxFilter 커널이 60px 대라 컷당 수십 초가 걸린다
    # (PIL 은 numpy 없이 O(n·k²) 로 돈다). 줄인 뒤 두르면 결과는 사실상 같고 훨씬 빠르다.
    cut = Image.new("RGBA", img.size, (255, 255, 255, 0))
    cut.paste(img.convert("RGBA"), (0, 0), alpha)
    cut = cut.crop(cut.getbbox())

    ring_out = max(2, round(long_side * RING_RATIO))
    inner = long_side - 2 * ring_out  # 링 두께만큼 안쪽으로 넣어야 캔버스 밖으로 안 넘친다
    w, h = cut.size
    if w >= h:
        size = (inner, max(1, round(h * inner / w)))
    else:
        size = (max(1, round(w * inner / h)), inner)
    cut = cut.resize(size, Image.LANCZOS)

    canvas = Image.new("RGBA", (size[0] + 2 * ring_out, size[1] + 2 * ring_out), (255, 255, 255, 0))
    canvas.paste(cut, (ring_out, ring_out))

    a = canvas.getchannel("A")
    ring = a.filter(ImageFilter.MaxFilter(2 * ring_out + 1))
    plate = Image.new("RGBA", canvas.size, (255, 255, 255, 0))
    plate.putalpha(ring)
    plate.paste(canvas, (0, 0), a)
    plate.save(dst, "WEBP", quality=quality, method=6)
    return plate, hole_ratio(alpha)


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    long_side = int(sys.argv[3]) if len(sys.argv) > 3 else 512
    quality = int(sys.argv[4]) if len(sys.argv) > 4 else 80
    out, holes = diecut(src, dst, long_side=long_side, quality=quality)
    print(
        f"{os.path.basename(dst):28s} {out.width}x{out.height}  "
        f"{os.path.getsize(dst)/1024:5.1f}KB  hole={holes:.3f}"
    )
