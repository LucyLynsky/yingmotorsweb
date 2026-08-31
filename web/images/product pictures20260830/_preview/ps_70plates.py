# -*- coding: utf-8 -*-
"""PS out dealer plates on Mixing tank photo 70. Do not restore backup."""
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
    x1, y1, x2, y2 = [int(v) for v in box]
    rgb = cv2.cvtColor(bgr[y1:y2, x1:x2], cv2.COLOR_BGR2RGB)
    Image.fromarray(rgb).save(PREV / name, quality=92)


def preview(bgr, name, max_w=1100):
    h, w = bgr.shape[:2]
    small = cv2.resize(bgr, (max_w, int(h * max_w / w)), interpolation=cv2.INTER_AREA)
    cv2.imwrite(str(PREV / name), small, [int(cv2.IMWRITE_JPEG_QUALITY), 90])


def blue_plate_mask(bgr, box, pad=6):
    x1, y1, x2, y2 = box
    hsv = cv2.cvtColor(bgr[y1:y2, x1:x2], cv2.COLOR_BGR2HSV)
    blue = cv2.inRange(hsv, (88, 45, 40), (135, 255, 255))
    blue = cv2.morphologyEx(blue, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    blue = cv2.dilate(blue, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (pad, pad)))
    mask = np.zeros(bgr.shape[:2], np.uint8)
    mask[y1:y2, x1:x2] = blue
    return mask


def inpaint(img, mask, r=6):
    m = (mask > 0).astype(np.uint8) * 255
    if int(m.sum()) == 0:
        return img
    a = cv2.inpaint(img, m, r, cv2.INPAINT_TELEA)
    b = cv2.inpaint(img, m, r + 2, cv2.INPAINT_NS)
    return cv2.addWeighted(a, 0.45, b, 0.55, 0)


def fill_from_sides(img, mask, like, reach=70):
    """Lerp from matching paint left/right of each mask run."""
    out = img.copy()
    h, w = img.shape[:2]
    ys, xs = np.where(mask > 0)
    if ys.size == 0:
        return out
    for y in range(int(ys.min()), int(ys.max()) + 1):
        row = mask[y] > 0
        if not np.any(row):
            continue
        xs_b = np.flatnonzero(row)
        x1, x2 = int(xs_b[0]), int(xs_b[-1]) + 1
        L = img[y, max(0, x1 - reach) : x1][like[y, max(0, x1 - reach) : x1] > 0]
        R = img[y, x2 : min(w, x2 + reach)][like[y, x2 : min(w, x2 + reach)] > 0]
        if len(L) < 3 and len(R) < 3:
            continue
        lv = np.median(L.astype(np.float32), axis=0) if len(L) >= 3 else None
        rv = np.median(R.astype(np.float32), axis=0) if len(R) >= 3 else None
        if lv is None:
            lv = rv
        if rv is None:
            rv = lv
        t = np.linspace(0, 1, x2 - x1, dtype=np.float32)[:, None]
        out[y, x1:x2] = np.clip((1 - t) * lv + t * rv, 0, 255).astype(np.uint8)
    return out


def mosaic(img, mask, block=8):
    out = img.copy()
    ys, xs = np.where(mask > 0)
    if ys.size == 0:
        return out
    y1, y2 = int(ys.min()), int(ys.max()) + 1
    x1, x2 = int(xs.min()), int(xs.max()) + 1
    roi = out[y1:y2, x1:x2]
    mh, mw = roi.shape[:2]
    small = cv2.resize(
        roi, (max(1, mw // block), max(1, mh // block)), interpolation=cv2.INTER_AREA
    )
    pix = cv2.resize(small, (mw, mh), interpolation=cv2.INTER_NEAREST)
    local = mask[y1:y2, x1:x2] > 0
    roi[local] = pix[local]
    out[y1:y2, x1:x2] = roi
    return out


def main():
    bgr = load_photo(src)
    windows = {
        "main": (610, 1900, 800, 2130),
        "mid": (290, 1840, 400, 1990),
        "far": (0, 1760, 160, 1940),
    }
    masks = {k: blue_plate_mask(bgr, box, pad=8) for k, box in windows.items()}
    vis = bgr.copy()
    vis[masks["main"] > 0] = (0, 0, 255)
    vis[masks["mid"] > 0] = (0, 255, 0)
    vis[masks["far"] > 0] = (0, 255, 255)
    crop_save(vis, (0, 1700, 900, 2200), "70_plates_mask.jpg")
    for k, m in masks.items():
        print(k, "px", int(m.sum() / 255))

    out = bgr.copy()

    # main plate sits on dark grille
    out = inpaint(out, masks["main"], r=7)
    # second pass on leftover blue
    m2 = blue_plate_mask(out, windows["main"], pad=6)
    if m2.sum() > 400 * 255:
        out = inpaint(out, m2, r=5)
        print("main pass2", int(m2.sum() / 255))

    # mid plate sits on white bumper
    hsv = cv2.cvtColor(out, cv2.COLOR_BGR2HSV)
    white = cv2.inRange(hsv, (0, 0, 150), (180, 55, 255))
    filled = fill_from_sides(out, masks["mid"], white, reach=55)
    # keep fill only on mask; inpaint any leftover
    out = np.where(masks["mid"][..., None] > 0, filled, out)
    leftover = blue_plate_mask(out, windows["mid"], pad=5)
    if leftover.sum() > 200 * 255:
        out = inpaint(out, leftover, r=4)
        print("mid leftover", int(leftover.sum() / 255))

    # far plate if any
    if masks["far"].sum() > 200 * 255:
        out = inpaint(out, masks["far"], r=4)
        print("far inpainted")
    else:
        print("far: no plate")

    save_photo(out, src)
    crop_save(out, (600, 1880, 820, 2140), "70_p1_done.jpg")
    crop_save(out, (270, 1800, 430, 2000), "70_p2_done.jpg")
    crop_save(out, (0, 1700, 280, 1960), "70_p3_done.jpg")
    crop_save(out, (0, 1650, 900, 2200), "70_plates_done.jpg")
    preview(out, "70_done.jpg")
    print("saved", src)


if __name__ == "__main__":
    main()
