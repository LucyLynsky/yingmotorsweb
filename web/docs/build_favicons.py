# -*- coding: utf-8 -*-
"""Build favicons: opaque brown square, gold letter Y. Google crops the square into a circle."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"E:\codePrj\web")
ASSETS = ROOT / "assets"
INK = (33, 14, 6, 255)  # #210E06
GOLD = (228, 148, 2, 255)


def load_font(size: int) -> ImageFont.ImageFont:
    fonts = Path(r"C:\Windows\Fonts")
    for name in ("ariblk.ttf", "arialbd.ttf", "segoeuib.ttf", "calibrib.ttf", "arial.ttf"):
        path = fonts / name
        if path.is_file():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def make_mark(size: int) -> Image.Image:
    """Opaque brown square + gold Y. No transparency — Google may ignore transparent icons."""
    im = Image.new("RGBA", (size, size), INK)
    draw = ImageDraw.Draw(im)
    font = load_font(max(12, int(size * 0.58)))
    bbox = draw.textbbox((0, 0), "Y", font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - tw) / 2 - bbox[0]
    y = (size - th) / 2 - bbox[1]
    draw.text((x, y), "Y", font=font, fill=GOLD)
    return im


def save_png(im: Image.Image, path: Path, size: int) -> None:
    out = im.resize((size, size), Image.Resampling.LANCZOS)
    out.convert("RGBA").save(path, "PNG", optimize=True)


def write_svg() -> None:
    svg = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" role="img" aria-label="YING MOTORS">
  <rect width="512" height="512" fill="#210E06"/>
  <text x="256" y="368" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="700" font-size="300" fill="#E49402">Y</text>
</svg>
"""
    (ASSETS / "favicon.svg").write_text(svg, encoding="utf-8")


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
