# -*- coding: utf-8 -*-
"""Cover Mixing-tank dealer plates with a solid black mark."""
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageOps

ROOT = Path(r"E:\codePrj\web\images\product pictures20260830")
PREV = ROOT / "_preview"
src = ROOT / r"used\Mixing tank\20260830072428_70_24.jpg"


def load_photo(path):
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    return cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)


def save_photo(bgr, path, quality=95):
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    Image.fromarray(rgb).save(path, quality=quality, subsampling=0, optimize=True)


def crop_save(bgr, box, name):
    x1, y1, x2, y2 = box
    rgb = cv2.cvtColor(bgr[y1:y2, x1:x2], cv2.COLOR_BGR2RGB)
    Image.fromarray(rgb).save(PREV / name, quality=92)


def preview(bgr, name, max_w=1100):
    h, w = bgr.shape[:2]
    small = cv2.resize(bgr, (max_w, int(h * max_w / w)), interpolation=cv2.INTER_AREA)
    cv2.imwrite(str(PREV / name), small, [int(cv2.IMWRITE_JPEG_QUALITY), 90])


def plate_poly(bgr, box):
    x1, y1, x2, y2 = box
    hsv = cv2.cvtColor(bgr[y1:y2, x1:x2], cv2.COLOR_BGR2HSV)
    blue = cv2.inRange(hsv, (88, 45, 40), (135, 255, 255))
    blue = cv2.morphologyEx(blue, cv2.MORPH_CLOSE, np.ones((11, 9), np.uint8))
    cnts, _ = cv2.findContours(blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cnts:
        return None
    c = max(cnts, key=cv2.contourArea)
    if cv2.contourArea(c) < 200:
        return None
    c = c + np.array([x1, y1])
    rect = cv2.minAreaRect(c)
    box_pts = cv2.boxPoints(rect)
    # expand slightly so the mark fully covers the plate edge
    cx, cy = rect[0]
    w, h = rect[1]
    ang = rect[2]
    w, h = w + 10, h + 10
    return cv2.boxPoints(((cx, cy), (w, h), ang)).astype(np.int32)


def main():
    bgr = load_photo(src)
    windows = [
        (610, 1900, 800, 2130),
        (290, 1840, 400, 1990),
    ]
    mark = bgr.copy()
    for box in windows:
        poly = plate_poly(bgr, box)
        if poly is None:
            print("no plate in", box)
            continue
        cv2.fillConvexPoly(mark, poly, (18, 18, 18))
        print("marked", poly.tolist())

    save_photo(mark, src)
    crop_save(mark, (580, 1860, 860, 2160), "70_p1_mark.jpg")
    crop_save(mark, (250, 1760, 430, 2020), "70_p2_mark.jpg")
    crop_save(mark, (0, 1650, 900, 2200), "70_plates_mark.jpg")
    preview(mark, "70_done.jpg")
    print("saved", src)


if __name__ == "__main__":
    main()
