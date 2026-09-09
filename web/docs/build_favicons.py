# -*- coding: utf-8 -*-
"""Build square favicons and OG image from the YING MOTORS Y mark. Google Search needs a 1:1 icon >48px."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"E:\codePrj\web")
ASSETS = ROOT / "assets"
INK = (33, 14, 6, 255)
GOLD = (228, 148, 2, 255)

# Wordmark Y from logo-mark.svg, closed path.
Y_PATH = [
    (130.56740027510318, 21.0),
    (88.47386519944979, 108.82599724896836),
    (88.47386519944979, 164.0),
    (61.5261348005502, 164.0),
    (61.5261348005502, 108.82599724896836),
    (19.432599724896832, 21.0),
    (47.65887207702888, 21.0),
    (75.0, 82.56671251719395),
    (102.34112792297111, 21.0),
]


def y_polygon(size: int, pad_ratio: float = 0.18) -> list[tuple[float, float]]:
    xs = [p[0] for p in Y_PATH]
    ys = [p[1] for p in Y_PATH]
    ox, oy = min(xs), min(ys)
    ow, oh = max(xs) - ox, max(ys) - oy
    pad = size * pad_ratio
    avail = size - 2 * pad
    scale = avail / oh
    tw = ow * scale
    tx = (size - tw) / 2
    ty = pad
    return [((x - ox) * scale + tx, (y - oy) * scale + ty) for x, y in Y_PATH]


def make_mark(size: int) -> Image.Image:
    im = Image.new("RGBA", (size, size), INK)
    draw = ImageDraw.Draw(im)
    draw.polygon(y_polygon(size), fill=GOLD)
    return im


def save_png(im: Image.Image, path: Path, size: int) -> None:
    out = im.resize((size, size), Image.Resampling.LANCZOS)
    out.convert("RGBA").save(path, "PNG", optimize=True)


def write_svg() -> None:
    pts = " ".join(f"{x:.3f},{y:.3f}" for x, y in y_polygon(512, 0.18))
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" role="img" aria-label="YING MOTORS">
  <rect width="512" height="512" fill="#210E06"/>
  <polygon fill="#E49402" points="{pts}"/>
</svg>
"""
    (ASSETS / "favicon.svg").write_text(svg, encoding="utf-8")


def load_font(size: int) -> ImageFont.ImageFont:
    for name in ("segoeuib.ttf", "arialbd.ttf", "calibrib.ttf", "segoeui.ttf", "arial.ttf"):
        path = Path(r"C:\Windows\Fonts") / name
        if path.is_file():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def make_og() -> None:
    w, h = 1200, 630
    im = Image.new("RGB", (w, h), INK[:3])
    mark = make_mark(220).convert("RGBA")
    im.paste(mark, (80, (h - 220) // 2), mark)
    draw = ImageDraw.Draw(im)
    title = load_font(64)
    sub = load_font(28)
    draw.text((340, 230), "YING MOTORS", font=title, fill=GOLD[:3])
    draw.text((340, 320), "Trucks & machines for export", font=sub, fill=(246, 241, 234))
    draw.text((340, 365), "Liangshan, Shandong, China", font=sub, fill=(180, 160, 140))
    im.save(ASSETS / "og-image.jpg", "JPEG", quality=88, optimize=True)


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    write_svg()
    master = make_mark(512)
    save_png(master, ASSETS / "favicon-32.png", 32)
    save_png(master, ASSETS / "favicon-48.png", 48)
    save_png(master, ASSETS / "favicon-96.png", 96)
    save_png(master, ASSETS / "favicon-192.png", 192)
    save_png(master, ASSETS / "favicon-512.png", 512)
    save_png(master, ASSETS / "apple-touch-icon.png", 180)
    ico = master.convert("RGBA")
    ico.save(
        ASSETS / "favicon.ico",
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48)],
    )
    (ROOT / "favicon.ico").write_bytes((ASSETS / "favicon.ico").read_bytes())
    make_og()
    print("Wrote favicon.ico, PNG sizes, apple-touch-icon.png, og-image.jpg")


if __name__ == "__main__":
    main()
