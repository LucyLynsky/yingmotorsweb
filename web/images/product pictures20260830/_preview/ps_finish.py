# -*- coding: utf-8 -*-
"""Clone bright paint from the sides of each target rect — never from ground/sky."""
from pathlib import Path
import shutil
import cv2
import numpy as np
from PIL import Image, ImageOps

ROOT = Path(r"E:\codePrj\web\images\product pictures20260830")
PREV = ROOT / "_preview"
BAK = ROOT / "_backup"
PREV.mkdir(exist_ok=True)


def load_photo(path):
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    return cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)


def save_photo(bgr, path, quality=95):
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    Image.fromarray(rgb).save(path, quality=quality, subsampling=0, optimize=True)


def preview(bgr, name, max_w=1100):
    h, w = bgr.shape[:2]
    small = cv2.resize(bgr, (max_w, int(h * max_w / w)), interpolation=cv2.INTER_AREA)
    cv2.imwrite(str(PREV / name), small, [int(cv2.IMWRITE_JPEG_QUALITY), 90])


def crop_save(bgr, box, name):
    x1, y1, x2, y2 = box
    rgb = cv2.cvtColor(bgr[y1:y2, x1:x2], cv2.COLOR_BGR2RGB)
    Image.fromarray(rgb).save(PREV / name, quality=92)


def draw_boxes(bgr, boxes, color=(0, 255, 255)):
    vis = bgr.copy()
    for x1, y1, x2, y2 in boxes:
        cv2.rectangle(vis, (x1, y1), (x2, y2), color, 4)
    return vis


def blue_plate_rects(bgr, search_boxes, min_area=2500):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    rects = []
    for x1, y1, x2, y2 in search_boxes:
        roi = hsv[y1:y2, x1:x2]
        blue = cv2.inRange(roi, (92, 55, 40), (128, 255, 240))
        blue = cv2.morphologyEx(blue, cv2.MORPH_CLOSE, np.ones((17, 11), np.uint8))
        cnts, _ = cv2.findContours(blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        good = []
        for c in cnts:
            a = cv2.contourArea(c)
            if a < min_area:
                continue
            rx, ry, rw, rh = cv2.boundingRect(c)
            ar = rw / max(rh, 1)
            if rh < 40 or rw < 80 or ar < 1.3 or ar > 5.5:
                continue
            good.append((a, x1 + rx, y1 + ry, rw, rh))
        if good:
            good.sort(reverse=True)
            a, gx, gy, gw, gh = good[0]
            pad = 7
            rects.append((gx - pad, gy - pad, gx + gw + pad, gy + gh + pad))
    return rects


def bright_orange(bgr):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    return cv2.inRange(hsv, (1, 90, 95), (22, 255, 255))


def drum_white(bgr):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    # pale paint, not blue sky
    low_s = hsv[:, :, 1] < 45
    hi_v = hsv[:, :, 2] > 165
    h = hsv[:, :, 0]
    not_sky = (h < 70) | (h > 145)
    return (low_s & hi_v & not_sky).astype(np.uint8) * 255


def side_samples(img, like, y, x1, x2, reach=90):
    h, w = img.shape[:2]
    ls, rs = x1 - reach, x2 + reach
    left = img[y, max(0, ls) : x1][like[y, max(0, ls) : x1] > 0]
    right = img[y, x2 : min(w, rs)][like[y, x2 : min(w, rs)] > 0]
    return left, right


def trim_to_paint(rect, img, like, reach=90, min_n=5):
    x1, y1, x2, y2 = [int(v) for v in rect]
    h = img.shape[0]
    y1 = max(0, y1)
    y2 = min(h, y2)

    def ok(y):
        L, R = side_samples(img, like, y, x1, x2, reach)
        return len(L) + len(R) >= min_n

    while y1 < y2 and not ok(y1):
        y1 += 1
    while y2 > y1 and not ok(y2 - 1):
        y2 -= 1
    return x1, y1, x2, y2


def fill_rect_from_sides(img, rect, like, reach=90):
    x1, y1, x2, y2 = trim_to_paint(rect, img, like, reach)
    if y2 - y1 < 8 or x2 - x1 < 8:
        print("  skip tiny", rect, "->", (x1, y1, x2, y2))
        return img, (x1, y1, x2, y2)
    out = img.copy()
    last = None
    width = x2 - x1
    t = np.linspace(0, 1, width, dtype=np.float32)[:, None]
    for y in range(y1, y2):
        left, right = side_samples(img, like, y, x1, x2, reach)
        if len(left) >= 4:
            lv = np.median(left.astype(np.float32), axis=0)
        else:
            lv = last[0] if last is not None else None
        if len(right) >= 4:
            rv = np.median(right.astype(np.float32), axis=0)
        else:
            rv = last[1] if last is not None else None
        if lv is None and rv is None:
            continue
        if lv is None:
            lv = rv
        if rv is None:
            rv = lv
        last = (lv, rv)
        row = (1.0 - t) * lv + t * rv
        out[y, x1:x2] = np.clip(row, 0, 255).astype(np.uint8)
    # soften only the 4px seam
    mask = np.zeros(img.shape[:2], np.uint8)
    mask[y1:y2, x1:x2] = 255
    ring = cv2.dilate(mask, np.ones((7, 7), np.uint8))
    ring = cv2.subtract(ring, cv2.erode(mask, np.ones((3, 3), np.uint8)))
    blur = cv2.GaussianBlur(out, (5, 5), 0)
    out = np.where(ring[..., None] > 0, blur, out)
    return out, (x1, y1, x2, y2)


def inpaint_rect(img, rect, r=5):
    x1, y1, x2, y2 = [int(v) for v in rect]
    m = np.zeros(img.shape[:2], np.uint8)
    m[y1:y2, x1:x2] = 255
    a = cv2.inpaint(img, m, r, cv2.INPAINT_TELEA)
    b = cv2.inpaint(img, m, r + 2, cv2.INPAINT_NS)
    return cv2.addWeighted(a, 0.5, b, 0.5, 0)


def apply_rects(bgr, rects, like, tag):
    vis = draw_boxes(bgr, rects)
    preview(vis, f"{tag}_rects.jpg")
    out = bgr
    used = []
    for rect in rects:
        out, used_r = fill_rect_from_sides(out, rect, like)
        used.append(used_r)
        print(tag, "fill", rect, "->", used_r)
    return out, used


def fix_71():
    dest = ROOT / r"used\HOWO\20260830072551_71_24.jpg"
    shutil.copy2(BAK / dest.name, dest)
    bgr = load_photo(dest)
    rects = blue_plate_rects(bgr, [(1180, 2980, 1720, 3220)], min_area=8000)
    if not rects:
        rects = [(1210, 3007, 1659, 3176)]
        print("71 fallback rect")
    out, used = apply_rects(bgr, rects, bright_orange(bgr), "71")
    save_photo(out, dest)
    crop_save(out, (1100, 2900, 1750, 3280), "71_done_plate.jpg")
    preview(out, "71_done.jpg")


def fix_72():
    dest = ROOT / r"used\HOWO\20260830072651_72_24.jpg"
    shutil.copy2(BAK / dest.name, dest)
    bgr = load_photo(dest)
    fg = blue_plate_rects(bgr, [(1080, 2520, 1700, 2820)], min_area=8000)
    print("72 fg detected", fg)
    if not fg:
        fg = [(1140, 2555, 1635, 2790)]
    out, _ = apply_rects(bgr, fg, bright_orange(bgr), "72fg")

    rear = blue_plate_rects(
        out,
        [
            (390, 2110, 760, 2350),
            (840, 2460, 1210, 2670),
            (50, 2110, 290, 2290),
        ],
        min_area=1200,
    )
    print("72 rear detected", rear)
    vis = draw_boxes(out, rear, (0, 255, 0))
    preview(vis, "72_rear_rects.jpg")
    for rect in rear:
        # dark trim: inpaint is OK if rect stays on the bumper
        out = inpaint_rect(out, rect, r=4)
        print("72 rear inpaint", rect)
    save_photo(out, dest)
    crop_save(out, (1000, 2480, 1750, 2920), "72_done_fgplate.jpg")
    crop_save(out, (200, 2080, 1250, 2720), "72_done_rear.jpg")
    preview(out, "72_done.jpg")


def fix_70():
    dest = ROOT / r"used\Mixing tank\20260830072428_70_24.jpg"
    shutil.copy2(BAK / dest.name, dest)
    bgr = load_photo(dest)
    # tight boxes from original artwork
    rects = [
        (2320, 900, 2820, 1360),   # tank logo + 亚特重工
        (2720, 760, 3920, 1120),   # YATE + red mark
        (2980, 1100, 3820, 1480),  # spec lines
    ]
    white = drum_white(bgr)
    # keep donors on the vehicle, not flags/sky
    band = np.zeros(white.shape, np.uint8)
    band[680:1580, 2180:4000] = 255
    white = cv2.bitwise_and(white, band)
    out, used = apply_rects(bgr, rects, white, "70")
    save_photo(out, dest)
    crop_save(out, (2200, 680, 4032, 1600), "70_done_drum.jpg")
    crop_save(out, (2260, 840, 2880, 1420), "70_done_tank.jpg")
    preview(out, "70_done.jpg")


if __name__ == "__main__":
    fix_71()
    fix_72()
    fix_70()
    print("done")
