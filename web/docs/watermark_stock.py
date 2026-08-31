# -*- coding: utf-8 -*-
"""Apply Yingmotors watermark + filename label to stock photos and videos."""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = Path(r"E:\codePrj\web")
STOCK = ROOT / "images" / "stock"
FONT_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")
MARK_TEXT = "Yingmotors"
ORIG_DIRNAME = "_orig"


def _ffmpeg() -> str:
    import imageio_ffmpeg

    return imageio_ffmpeg.get_ffmpeg_exe()


def make_overlay(w: int, h: int, label: str) -> Image.Image:
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    font_mark = ImageFont.truetype(str(FONT_BOLD), size=max(16, min(w, h) // 18))
    font_label = ImageFont.truetype(str(FONT_BOLD), size=max(13, w // 26))

    probe = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    bbox = ImageDraw.Draw(probe).textbbox((0, 0), MARK_TEXT, font=font_mark)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad = max(8, w // 70)
    tile_size = (tw + pad * 2, th + pad * 2)

    mask = Image.new("L", tile_size, 0)
    ImageDraw.Draw(mask).text((pad, pad), MARK_TEXT, font=font_mark, fill=255)
    k = max(3, int(round(w / 110.0)))
    if k % 2 == 0:
        k += 1
    stroke_mask = ImageChops.subtract(mask.filter(ImageFilter.MaxFilter(k)), mask)

    stroke = Image.new("RGBA", tile_size, (0, 0, 0, 0))
    stroke.paste((0, 0, 0, 220), mask=stroke_mask)
    fill = Image.new("RGBA", tile_size, (0, 0, 0, 0))
    fill.paste((255, 255, 255, 255), mask=mask)
    glyph = Image.alpha_composite(stroke, fill)
    r, g, b, a = glyph.split()
    a = a.point(lambda p: int(p * 0.78))
    tile = Image.merge("RGBA", (r, g, b, a))
    rotated = tile.rotate(-32, expand=True, resample=Image.Resampling.BICUBIC)

    rw, rh = rotated.size
    cx, cy = w / 2.0, h / 2.0
    # Four marks around the image center: up, down, left, right.
    # Keep a gap so they do not merge into one block.
    ox = max(int(w * 0.28), int(rw * 0.62))
    oy = max(int(h * 0.28), int(rh * 0.62))
    max_ox = max(0, (w - rw) // 2)
    max_oy = max(0, (h - rh) // 2)
    ox = min(ox, max_ox) if max_ox else ox
    oy = min(oy, max_oy) if max_oy else oy
    for px, py in (
        (cx, cy - oy),
        (cx, cy + oy),
        (cx - ox, cy),
        (cx + ox, cy),
    ):
        x = int(round(px - rw / 2.0))
        y = int(round(py - rh / 2.0))
        overlay.paste(rotated, (x, y), rotated)

    ld = ImageDraw.Draw(overlay)
    lbbox = ld.textbbox((0, 0), label, font=font_label)
    lw, lh = lbbox[2] - lbbox[0], lbbox[3] - lbbox[1]
    pad_x, pad_y = max(8, w // 90), max(5, h // 90)
    margin_right = max(10, w // 80)
    # Detail gallery / thumbs use object-fit:cover and clip ~16–24% of
    # portrait frames. Lift the tag into the visible lower-right band.
    if h > w * 1.1:
        margin_bottom = int(h * 0.26)
    else:
        margin_bottom = max(10, w // 80)
    bx2, by2 = w - margin_right, h - margin_bottom
    bx1 = bx2 - lw - pad_x * 2
    by1 = by2 - lh - pad_y * 2
    ld.rounded_rectangle([bx1, by1, bx2, by2], radius=max(4, w // 180), fill=(0, 0, 0, 168))
    ld.text((bx1 + pad_x, by1 + pad_y - 1), label, font=font_label, fill=(255, 255, 255, 235))
    return overlay


def watermark_image(src: Path, dst: Path) -> None:
    img = Image.open(src).convert("RGBA")
    overlay = make_overlay(img.width, img.height, src.stem)
    out = Image.alpha_composite(img, overlay).convert("RGB")
    dst.parent.mkdir(parents=True, exist_ok=True)
    out.save(dst, "JPEG", quality=92, optimize=True)


def video_size(path: Path) -> tuple[int, int]:
    import cv2

    cap = cv2.VideoCapture(str(path))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    if w <= 0 or h <= 0:
        raise RuntimeError(f"cannot read video size: {path}")
    return w, h


def watermark_video(src: Path, dst: Path) -> None:
    w, h = video_size(src)
    overlay = make_overlay(w, h, src.stem)
    with tempfile.TemporaryDirectory() as tmp:
        png = Path(tmp) / "wm.png"
        mp4 = Path(tmp) / "out.mp4"
        overlay.save(png, "PNG")
        cmd = [
            _ffmpeg(),
            "-y",
            "-i",
            str(src),
            "-i",
            str(png),
            "-filter_complex",
            "[1:v]format=rgba[wm];[0:v][wm]overlay=0:0:format=auto",
            "-c:v",
            "libx264",
            "-crf",
            "20",
            "-preset",
            "veryfast",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "copy",
            "-movflags",
            "+faststart",
            str(mp4),
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            cmd = [
                _ffmpeg(),
                "-y",
                "-i",
                str(src),
                "-i",
                str(png),
                "-filter_complex",
                "[1:v]format=rgba[wm];[0:v][wm]overlay=0:0:format=auto",
                "-c:v",
                "libx264",
                "-crf",
                "20",
                "-preset",
                "veryfast",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                "-b:a",
                "128k",
                "-movflags",
                "+faststart",
                str(mp4),
            ]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            if proc.returncode != 0:
                raise RuntimeError(proc.stderr[-2000:])
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(mp4, dst)


def backup_originals(folder: Path) -> Path:
    orig = folder / ORIG_DIRNAME
    orig.mkdir(exist_ok=True)
    for src in list(folder.glob("*.jpg")) + list(folder.glob("*.mp4")):
        if src.name.endswith("_wm.jpg"):
            continue
        dest = orig / src.name
        if not dest.exists():
            shutil.copy2(src, dest)
    thumbs = folder / "thumbs"
    if thumbs.is_dir():
        (orig / "thumbs").mkdir(exist_ok=True)
        for src in thumbs.glob("*.jpg"):
            dest = orig / "thumbs" / src.name
            if not dest.exists():
                shutil.copy2(src, dest)
    return orig


def process_folder(folder: Path) -> None:
    if not folder.is_dir():
        raise FileNotFoundError(folder)
    orig = backup_originals(folder)
    images = sorted(p for p in orig.glob("*.jpg") if not p.name.endswith("_wm.jpg"))
    thumbs = sorted((orig / "thumbs").glob("*.jpg")) if (orig / "thumbs").is_dir() else []
    videos = sorted(orig.glob("*.mp4"))

    for src in images:
        dst = folder / src.name
        print(f"image {src.name}", flush=True)
        watermark_image(src, dst)
    for src in thumbs:
        dst = folder / "thumbs" / src.name
        print(f"thumb {src.name}", flush=True)
        watermark_image(src, dst)
    for src in videos:
        dst = folder / src.name
        print(f"video {src.name}", flush=True)
        watermark_video(src, dst)


def product_folders() -> list[Path]:
    skip = {ORIG_DIRNAME, "_inspect"}
    return sorted(
        p for p in STOCK.iterdir()
        if p.is_dir() and p.name not in skip and not p.name.startswith("_")
    )


def main() -> None:
    names = sys.argv[1:]
    folders = [STOCK / n for n in names] if names else product_folders()
    for folder in folders:
        print(f"=== {folder.name}", flush=True)
        process_folder(folder)
    print("done", flush=True)


if __name__ == "__main__":
    main()
