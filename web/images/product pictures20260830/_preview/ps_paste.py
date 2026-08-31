# -*- coding: utf-8 -*-
"""Paste GenerateImage crops back onto originals with aspect match + feather."""
from pathlib import Path
import shutil
import cv2
import numpy as np
from PIL import Image, ImageOps

ROOT = Path(r"E:\codePrj\web\images\product pictures20260830")
PREV = ROOT / "_preview"
BAK = ROOT / "_backup"
ASSETS = Path(r"C:\Users\chatx\.cursor\projects\e-codePrj-web\assets")


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


def load_gen(name):
    im = Image.open(ASSETS / name).convert("RGB")
    return cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)


def match_aspect(gen, tw, th, y_bias=0.0):
    """Crop gen to target aspect, then resize. y_bias: -1 top, 0 center, 1 bottom."""
    gh, gw = gen.shape[:2]
    target_ar = tw / th
    src_ar = gw / gh
    if src_ar > target_ar + 0.01:
        nw = max(1, int(round(gh * target_ar)))
        x0 = (gw - nw) // 2
        gen = gen[:, x0 : x0 + nw]
    elif src_ar < target_ar - 0.01:
        nh = max(1, int(round(gw / target_ar)))
        extra = gh - nh
        y0 = int(np.clip((extra / 2) + y_bias * extra / 2, 0, extra))
        gen = gen[y0 : y0 + nh]
    return cv2.resize(gen, (tw, th), interpolation=cv2.INTER_LANCZOS4)


def inner_alpha(th, tw, inner_xy, feather):
    """Alpha is exactly 1.0 in the core; only a thin border is feathered."""
    ix1, iy1, ix2, iy2 = inner_xy
    m = np.zeros((th, tw), np.uint8)
    m[max(0, iy1) : max(0, iy2), max(0, ix1) : max(0, ix2)] = 255
    k = max(3, int(feather) | 1)
    eroded = cv2.erode(m, np.ones((k, k), np.uint8))
    alpha = cv2.GaussianBlur(m, (0, 0), max(feather * 0.35, 1.0)).astype(np.float32) / 255.0
    alpha[eroded > 0] = 1.0
    return np.clip(alpha, 0, 1)


def paste_feather(dst, gen, box, feather=18, y_bias=0.0, inner=None):
    """Replace inner region at full opacity; feather only the inner border."""
    x1, y1, x2, y2 = box
    tw, th = x2 - x1, y2 - y1
    src = match_aspect(gen, tw, th, y_bias=y_bias)
    if inner is None:
        alpha = inner_alpha(th, tw, (0, 0, tw, th), feather)
    else:
        ix1, iy1, ix2, iy2 = inner
        alpha = inner_alpha(
            th, tw, (ix1 - x1, iy1 - y1, ix2 - x1, iy2 - y1), feather
        )
    roi = dst[y1:y2, x1:x2].astype(np.float32)
    mixed = src.astype(np.float32) * alpha[..., None] + roi * (1.0 - alpha[..., None])
    dst[y1:y2, x1:x2] = np.clip(mixed, 0, 255).astype(np.uint8)
    return dst


def inpaint_rect(img, rect, r=5):
    x1, y1, x2, y2 = rect
    m = np.zeros(img.shape[:2], np.uint8)
    m[y1:y2, x1:x2] = 255
    m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
    a = cv2.inpaint(img, m, r, cv2.INPAINT_TELEA)
    b = cv2.inpaint(img, m, r + 2, cv2.INPAINT_NS)
    return cv2.addWeighted(a, 0.5, b, 0.5, 0)


def fill_plate_on_paint(img, rect, hsv_lo, hsv_hi, reach=70):
    """Lerp from matching paint on left/right, rows that have donors."""
    x1, y1, x2, y2 = rect
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    like = cv2.inRange(hsv, np.array(hsv_lo), np.array(hsv_hi))
    out = img.copy()
    h, w = img.shape[:2]
    last = None
    width = x2 - x1
    t = np.linspace(0, 1, width, dtype=np.float32)[:, None]
    for y in range(y1, y2):
        L = img[y, max(0, x1 - reach) : x1][like[y, max(0, x1 - reach) : x1] > 0]
        R = img[y, x2 : min(w, x2 + reach)][like[y, x2 : min(w, x2 + reach)] > 0]
        if len(L) >= 5:
            lv = np.median(L.astype(np.float32), axis=0)
        else:
            lv = last[0] if last else None
        if len(R) >= 5:
            rv = np.median(R.astype(np.float32), axis=0)
        else:
            rv = last[1] if last else None
        if lv is None and rv is None:
            continue
        if lv is None:
            lv = rv
        if rv is None:
            rv = lv
        last = (lv, rv)
        # prefer brighter donor for orange bumpers
        out[y, x1:x2] = np.clip((1 - t) * lv + t * rv, 0, 255).astype(np.uint8)
    return out


def main():
    # --- 71 ---
    p71 = ROOT / r"used\HOWO\20260830072551_71_24.jpg"
    shutil.copy2(BAK / p71.name, p71)
    b71 = load_photo(p71)
    g71 = load_gen("gen_out_71.png")
    crop_save(match_aspect(g71, 620, 300, y_bias=-0.55), (0, 0, 620, 300), "71_gen_aligned.jpg")
    # gen has extra black below; bias toward top of gen
    b71 = paste_feather(
        b71, g71, (1140, 2940, 1760, 3240), feather=12, y_bias=-0.55,
        inner=(1195, 2995, 1680, 3195),
    )
    save_photo(b71, p71)
    crop_save(b71, (1100, 2900, 1750, 3280), "71_done_plate.jpg")
    preview(b71, "71_done.jpg")
    print("71 pasted")

    # --- 72 ---
    p72 = ROOT / r"used\HOWO\20260830072651_72_24.jpg"
    shutil.copy2(BAK / p72.name, p72)
    b72 = load_photo(p72)
    g72 = load_gen("gen_out_72.png")
    b72 = paste_feather(
        b72, g72, (1080, 2500, 1780, 2860), feather=12, y_bias=-0.15,
        inner=(1125, 2550, 1655, 2810),
    )
    g72r = load_gen("gen_out_72rear.png")
    b72 = paste_feather(
        b72, g72r, (360, 2080, 800, 2380), feather=10, y_bias=0.0,
        inner=(410, 2135, 740, 2325),
    )
    # remaining distant plates: tight blue bbox then inpaint (dark/small)
    hsv = cv2.cvtColor(b72, cv2.COLOR_BGR2HSV)
    blue = cv2.inRange(hsv, (92, 70, 50), (128, 255, 235))
    for box in [(840, 2470, 1200, 2660), (50, 2115, 280, 2280)]:
        x1, y1, x2, y2 = box
        roi = blue[y1:y2, x1:x2]
        if int(roi.sum()) < 500 * 255:
            continue
        ys, xs = np.where(roi > 0)
        rx1, rx2 = x1 + int(xs.min()) - 4, x1 + int(xs.max()) + 4
        ry1, ry2 = y1 + int(ys.min()) - 4, y1 + int(ys.max()) + 4
        b72 = inpaint_rect(b72, (rx1, ry1, rx2, ry2), r=4)
        print("72 extra plate", (rx1, ry1, rx2, ry2))
    save_photo(b72, p72)
    crop_save(b72, (1000, 2480, 1750, 2920), "72_done_fgplate.jpg")
    crop_save(b72, (200, 2080, 1250, 2720), "72_done_rear.jpg")
    preview(b72, "72_done.jpg")
    print("72 pasted")

    # --- 70 ---
    p70 = ROOT / r"used\Mixing tank\20260830072428_70_24.jpg"
    shutil.copy2(BAK / p70.name, p70)
    b70 = load_photo(p70)
    gdrum = load_gen("gen_out_70drum.png")
    b70 = paste_feather(
        b70, gdrum, (2680, 700, 4000, 1520), feather=14, y_bias=0.05,
        inner=(2710, 730, 3970, 1505),
    )
    gtank = load_gen("gen_out_70tank.png")
    b70 = paste_feather(
        b70, gtank, (2260, 820, 2920, 1420), feather=12, y_bias=0.1,
        inner=(2360, 880, 2860, 1370),
    )
    save_photo(b70, p70)
    crop_save(b70, (2200, 680, 4032, 1600), "70_done_drum.jpg")
    crop_save(b70, (2260, 840, 2880, 1420), "70_done_tank.jpg")
    preview(b70, "70_done.jpg")
    print("70 pasted")

    # leftover spec text: copy white from just above each dark glyph
    hsv = cv2.cvtColor(b70, cv2.COLOR_BGR2HSV)
    x1, y1, x2, y2 = 2900, 1050, 3950, 1520
    gray = cv2.cvtColor(b70[y1:y2, x1:x2], cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY_INV)
    th = cv2.morphologyEx(th, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    th = cv2.dilate(th, np.ones((5, 5), np.uint8))
    cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    nfix = 0
    for c in cnts:
        a = cv2.contourArea(c)
        if a < 40 or a > 8000:
            continue
        rx, ry, rw, rh = cv2.boundingRect(c)
        if rh > 90 or rw > 420:
            continue
        gx1, gy1 = x1 + rx - 3, y1 + ry - 3
        gx2, gy2 = x1 + rx + rw + 3, y1 + ry + rh + 3
        src_y1 = max(700, gy1 - rh - 25)
        src_y2 = src_y1 + (gy2 - gy1)
        if src_y2 > gy1:
            src_y2 = gy1
            src_y1 = src_y2 - (gy2 - gy1)
        patch = b70[src_y1:src_y2, gx1:gx2]
        if patch.shape[0] == gy2 - gy1 and patch.shape[1] == gx2 - gx1:
            b70[gy1:gy2, gx1:gx2] = patch
            nfix += 1
    print("70 spec clones", nfix)
    save_photo(b70, p70)
    crop_save(b70, (2200, 680, 4032, 1600), "70_done_drum.jpg")
    crop_save(b70, (2900, 1050, 3950, 1550), "70_done_specs.jpg")


if __name__ == "__main__":
    main()
