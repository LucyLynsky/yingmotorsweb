# -*- coding: utf-8 -*-
"""Restore plate windows from backup onto current (YATE-cleaned) photo, then clone/mosaic."""
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageOps

ROOT = Path(r"E:\codePrj\web\images\product pictures20260830")
PREV = ROOT / "_preview"
src = ROOT / r"used\Mixing tank\20260830072428_70_24.jpg"
bak = ROOT / "_backup" / "20260830072428_70_24.jpg"


def load_photo(path):
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    return cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)


def save_photo(bgr, path, quality=95):
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    Image.fromarray(rgb).save(path, quality=quality, subsampling=0, optimize=True)


def crop_save(bgr, box, name):
    x1, y1, x2, y2 = [int(v) for v in box]
    rgb = cv2.cvtColor(bgr[y1:y2, x1:x2], cv2.COLOR_BGR2RGB)
    Image.fromarray(rgb).save(PREV / name, quality=94)


cur = load_photo(src)
orig = load_photo(bak)

# restore only bumper/plate windows so drum YATE edits stay
windows = [
    (580, 1860, 840, 2160),  # main
    (250, 1760, 430, 2020),  # mid
    (0, 1680, 220, 1960),    # far (undo accidental inpaint)
]
for x1, y1, x2, y2 in windows:
    cur[y1:y2, x1:x2] = orig[y1:y2, x1:x2]
save_photo(cur, src)

# gen / inspect crops
crop_save(cur, (560, 1860, 860, 2160), "gen_in_70p1.jpg")
crop_save(cur, (250, 1760, 450, 2020), "gen_in_70p2.jpg")
crop_save(cur, (0, 1680, 220, 1960), "gen_in_70p3.jpg")
print("restored plate windows")
