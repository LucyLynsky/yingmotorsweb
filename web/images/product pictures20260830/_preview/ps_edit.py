# -*- coding: utf-8 -*-
"""Remove plates / brand lettering from product photos and wall text from videos."""
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


def roi_mask(h, w, boxes):
    m = np.zeros((h, w), np.uint8)
    for x1, y1, x2, y2 in boxes:
        cv2.rectangle(m, (int(x1), int(y1)), (int(x2), int(y2)), 255, -1)
    return m


def color_in_roi(bgr, boxes, ranges, dilate_k=11):
    """HSV inRange inside ROIs, then dilate."""
    h, w = bgr.shape[:2]
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    hit = np.zeros((h, w), np.uint8)
    for lo, hi in ranges:
        hit = cv2.bitwise_or(hit, cv2.inRange(hsv, lo, hi))
    hit = cv2.bitwise_and(hit, roi_mask(h, w, boxes))
    hit = cv2.morphologyEx(hit, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    if dilate_k > 0:
        hit = cv2.dilate(hit, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilate_k, dilate_k)))
    return hit


def inpaint(img, mask, r=9):
    m = (mask > 0).astype(np.uint8) * 255
    if int(m.sum()) == 0:
        return img
    a = cv2.inpaint(img, m, r, cv2.INPAINT_TELEA)
    b = cv2.inpaint(img, m, max(r, 11), cv2.INPAINT_NS)
    return cv2.addWeighted(a, 0.4, b, 0.6, 0)


def restore(name, dest):
    shutil.copy2(BAK / name, dest)


def run_photos():
    # --- 71 license plate ---
    p71 = ROOT / r"used\HOWO\20260830072551_71_24.jpg"
    restore("20260830072551_71_24.jpg", p71)
    bgr = load_photo(p71)
    boxes = [(1195, 2988, 1680, 3195)]
    mask = color_in_roi(
        bgr,
        boxes,
        [((85, 40, 30), (140, 255, 255))],
        dilate_k=15,
    )
    # if color miss, fall back to full box
    if mask.sum() < 2000:
        mask = roi_mask(*bgr.shape[:2], boxes)
        mask = cv2.dilate(mask, np.ones((9, 9), np.uint8))
    vis = bgr.copy()
    vis[mask > 0] = (0, 0, 255)
    preview(vis, "71_mask.jpg")
    out = inpaint(bgr, mask, r=8)
    preview(out, "71_done.jpg")
    save_photo(out, p71)
    print("71 mask px", int(mask.sum() / 255))

    # --- 72 license plates (fg + two behind) ---
    p72 = ROOT / r"used\HOWO\20260830072651_72_24.jpg"
    restore("20260830072651_72_24.jpg", p72)
    bgr = load_photo(p72)
    boxes = [
        (1160, 2810, 1645, 3095),  # foreground
        (500, 2435, 980, 2635),  # second truck
        (210, 2285, 560, 2415),  # third truck
        (80, 2180, 280, 2280),  # far if present
    ]
    mask = color_in_roi(
        bgr,
        boxes,
        [((85, 40, 30), (140, 255, 255))],
        dilate_k=13,
    )
    vis = bgr.copy()
    vis[mask > 0] = (0, 0, 255)
    preview(vis, "72_mask.jpg")
    out = inpaint(bgr, mask, r=8)
    preview(out, "72_done.jpg")
    save_photo(out, p72)
    print("72 mask px", int(mask.sum() / 255))

    # --- 89 TRUCKLORD ---
    p89 = ROOT / r"used\HOWO\20260830072933_89_24.jpg"
    restore("20260830072933_89_24.jpg", p89)
    bgr = load_photo(p89)
    # front words + side badge
    boxes = [
        (180, 1620, 980, 1920),  # left truck word
        (1100, 1600, 2150, 1950),  # right truck word
        (2480, 1780, 3010, 2380),  # side TRUCK LORD badge
    ]
    # black lettering
    mask = color_in_roi(
        bgr,
        boxes,
        [((0, 0, 0), (180, 255, 95))],
        dilate_k=15,
    )
    vis = bgr.copy()
    vis[mask > 0] = (0, 0, 255)
    preview(vis, "89_mask.jpg")
    out = inpaint(bgr, mask, r=7)
    # second pass leftovers
    mask2 = color_in_roi(out, boxes, [((0, 0, 0), (180, 255, 90))], dilate_k=11)
    if mask2.sum() > 500:
        out = inpaint(out, mask2, r=6)
    preview(out, "89_done.jpg")
    save_photo(out, p89)
    print("89 mask px", int(mask.sum() / 255))

    # --- 70 YATE / 亚特重工 ---
    p70 = ROOT / r"used\Mixing tank\20260830072428_70_24.jpg"
    restore("20260830072428_70_24.jpg", p70)
    bgr = load_photo(p70)
    boxes = [
        (2320, 900, 2820, 1360),  # small tank logo + 亚特重工
        (2720, 740, 3980, 1480),  # drum YATE block + specs
    ]
    mask = color_in_roi(
        bgr,
        boxes,
        [
            ((0, 70, 50), (15, 255, 255)),  # red logo
            ((160, 70, 50), (180, 255, 255)),
            ((0, 0, 0), (180, 220, 90)),  # black text
        ],
        dilate_k=19,
    )
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((21, 31), np.uint8))
    vis = bgr.copy()
    vis[mask > 0] = (0, 0, 255)
    preview(vis, "70_mask.jpg")
    out = inpaint(bgr, mask, r=12)
    mask2 = color_in_roi(
        out,
        boxes,
        [
            ((0, 60, 40), (15, 255, 255)),
            ((160, 60, 40), (180, 255, 255)),
            ((0, 0, 0), (180, 200, 95)),
        ],
        dilate_k=13,
    )
    if mask2.sum() > 400:
        out = inpaint(out, mask2, r=9)
    preview(out, "70_done.jpg")
    save_photo(out, p70)
    print("70 mask px", int(mask.sum() / 255))


def yellow_machine_mask(bgr):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    y1 = cv2.inRange(hsv, (10, 55, 60), (45, 255, 255))
    y2 = cv2.inRange(hsv, (0, 70, 60), (12, 255, 255))
    m = cv2.bitwise_or(y1, y2)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    m = cv2.dilate(m, np.ones((13, 13), np.uint8))
    return m


def wall_text_mask(bgr):
    """Characters on corrugated facade via horizontal residual; keep machines intact."""
    h, w = bgr.shape[:2]
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    machines = yellow_machine_mask(bgr)

    # horizontal corrugation residual: letters stick out
    horiz = cv2.blur(gray, (71, 1))
    diff = cv2.absdiff(gray, horiz)
    diff = cv2.GaussianBlur(diff, (5, 5), 0)
    _, th = cv2.threshold(diff, 16, 255, cv2.THRESH_BINARY)

    band = np.zeros((h, w), np.uint8)
    band[int(h * 0.07) : int(h * 0.46), :] = 255
    th = cv2.bitwise_and(th, band)
    th = cv2.bitwise_and(th, cv2.bitwise_not(machines))

    # drop long horizontal window strips
    horiz_lines = cv2.morphologyEx(
        th, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (45, 1))
    )
    th = cv2.subtract(th, horiz_lines)
    th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, np.ones((11, 11), np.uint8))
    th = cv2.dilate(th, np.ones((7, 7), np.uint8))

    cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros((h, w), np.uint8)
    for c in cnts:
        x, y, bw, bh = cv2.boundingRect(c)
        area = cv2.contourArea(c)
        if area < 180:
            continue
        if bh < 16 or bw < 12:
            continue
        ar = bw / max(bh, 1)
        if ar < 0.18 and bh > 70:  # pole
            continue
        if ar > 7 and bh < 22:  # window row
            continue
        if y > int(h * 0.48):
            continue
        cv2.drawContours(mask, [c], -1, 255, -1)

    mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
    mask = cv2.bitwise_and(mask, cv2.bitwise_not(machines))
    return mask, machines


def fill_horizontal(img, mask):
    out = img.copy().astype(np.float32)
    h, w = img.shape[:2]
    m = mask > 0
    for y in range(h):
        bad = m[y]
        if not np.any(bad):
            continue
        good = ~bad
        xs_g = np.flatnonzero(good)
        xs_b = np.flatnonzero(bad)
        if xs_g.size < 8:
            continue
        for c in range(3):
            out[y, xs_b, c] = np.interp(xs_b, xs_g, img[y, xs_g, c].astype(np.float32))
    return np.clip(out, 0, 255).astype(np.uint8)


def debug_video_frames():
    for name, idx in [("f095a0e4", 0), ("f095a0e4", 151), ("f095a0e4", 301),
                      ("f26fc6f1", 0), ("f26fc6f1", 161), ("f26fc6f1", 322)]:
        bgr = cv2.imread(str(PREV / f"{name}_f{idx}.jpg"))
        mask, machines = wall_text_mask(bgr)
        filled = fill_horizontal(bgr, mask)
        out = inpaint(filled, mask, r=4)
        out[machines > 0] = bgr[machines > 0]
        vis = bgr.copy()
        vis[mask > 0] = (0, 0, 255)
        preview(np.hstack([bgr, vis, out]), f"dbg_{name}_{idx}.jpg", max_w=1400)
        print(name, idx, "mask", int(mask.sum() / 255))


def process_video(src, tag):
    import imageio.v2 as imageio

    cap = cv2.VideoCapture(str(src))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"video {tag} {n} frames @{fps}")
    tmp = PREV / f"{tag}_out.mp4"
    writer = imageio.get_writer(
        str(tmp),
        fps=float(fps),
        codec="libx264",
        quality=7,
        pixelformat="yuv420p",
        macro_block_size=1,
    )
    i = 0
    samples = {0, n // 4, n // 2, 3 * n // 4, max(n - 2, 0)}
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        mask, machines = wall_text_mask(frame)
        filled = fill_horizontal(frame, mask)
        out = inpaint(filled, mask, r=4)
        out[machines > 0] = frame[machines > 0]
        writer.append_data(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))
        if i in samples:
            vis = out.copy()
            vis[mask > 0] = (0, 0, 255)
            preview(np.hstack([frame, vis, out]), f"{tag}_f{i}_cmp.jpg", max_w=1080)
            print(" sample", i, "mask", int(mask.sum() / 255))
        i += 1
        if i % 60 == 0:
            print("  ", i, "/", n)
    writer.close()
    cap.release()
    shutil.copy2(tmp, src)
    print("saved", src)


if __name__ == "__main__":
    import sys

    mode = sys.argv[1] if len(sys.argv) > 1 else "photos"
    if mode == "photos":
        run_photos()
    elif mode == "debugvid":
        debug_video_frames()
    elif mode == "video1":
        process_video(ROOT / r"used\Komatsu\f095a0e4e0e23d12d80e0258a0b63670.mp4", "koma")
    elif mode == "video2":
        process_video(ROOT / r"used\Mining truck\f26fc6f16bda7ccc22a7bf99d93f1312.mp4", "mine")
    else:
        print("unknown", mode)
