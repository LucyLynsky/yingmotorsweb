# -*- coding: utf-8 -*-
"""Fix remaining photo regions and tighter video wall-text removal."""
from pathlib import Path
import shutil
import cv2
import numpy as np
from PIL import Image, ImageOps

ROOT = Path(r"E:\codePrj\web\images\product pictures20260830")
PREV = ROOT / "_preview"
BAK = ROOT / "_backup"


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


def inpaint(img, mask, r=8):
    m = (mask > 0).astype(np.uint8) * 255
    if int(m.sum()) == 0:
        return img
    a = cv2.inpaint(img, m, r, cv2.INPAINT_TELEA)
    b = cv2.inpaint(img, m, max(r, 10), cv2.INPAINT_NS)
    return cv2.addWeighted(a, 0.4, b, 0.6, 0)


def color_in_boxes(bgr, boxes, ranges, dilate_k=13):
    h, w = bgr.shape[:2]
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    roi = np.zeros((h, w), np.uint8)
    for x1, y1, x2, y2 in boxes:
        roi[y1:y2, x1:x2] = 255
    hit = np.zeros((h, w), np.uint8)
    for lo, hi in ranges:
        hit = cv2.bitwise_or(hit, cv2.inRange(hsv, np.array(lo), np.array(hi)))
    hit = cv2.bitwise_and(hit, roi)
    hit = cv2.morphologyEx(hit, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    if dilate_k:
        hit = cv2.dilate(hit, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilate_k, dilate_k)))
    return hit, roi


def fix_72():
    dest = ROOT / r"used\HOWO\20260830072651_72_24.jpg"
    shutil.copy2(BAK / "20260830072651_72_24.jpg", dest)
    bgr = load_photo(dest)
    boxes = [
        (1080, 2520, 1680, 2880),  # foreground plate
        (350, 2220, 760, 2460),  # black truck behind
        (850, 2460, 1220, 2680),  # orange second truck
        (80, 2140, 280, 2285),  # far left if any
    ]
    mask, roi = color_in_boxes(
        bgr, boxes, [((80, 25, 25), (145, 255, 255))], dilate_k=14
    )
    # ensure each box that has blue gets covered
    vis = bgr.copy()
    vis[mask > 0] = (0, 0, 255)
    for x1, y1, x2, y2 in boxes:
        cv2.rectangle(vis, (x1, y1), (x2, y2), (0, 255, 255), 4)
    preview(vis, "72_mask.jpg")
    out = inpaint(bgr, mask, r=8)
    preview(out, "72_done.jpg")
    save_photo(out, dest)
    Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB)).crop((1000, 2480, 1750, 2950)).save(
        PREV / "72_done_plate.jpg", quality=92
    )
    Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB)).crop((200, 2100, 1200, 2700)).save(
        PREV / "72_done_bg.jpg", quality=92
    )
    print("72 mask", int(mask.sum() / 255))


def fix_70():
    dest = ROOT / r"used\Mixing tank\20260830072428_70_24.jpg"
    bgr = load_photo(dest)  # already mostly cleaned
    boxes = [
        (2900, 1020, 3950, 1520),  # leftover spec text on drum
        (2320, 980, 2820, 1360),  # tank leftovers
    ]
    mask, _ = color_in_boxes(
        bgr,
        boxes,
        [
            ((0, 0, 0), (180, 220, 110)),  # remaining dark glyphs
            ((0, 50, 40), (18, 255, 255)),
            ((160, 50, 40), (180, 255, 255)),
        ],
        dilate_k=15,
    )
    vis = bgr.copy()
    vis[mask > 0] = (0, 0, 255)
    preview(vis, "70_mask2.jpg")
    out = inpaint(bgr, mask, r=10)
    preview(out, "70_done.jpg")
    save_photo(out, dest)
    Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB)).crop((2100, 400, 4032, 1600)).save(
        PREV / "70_done_brand.jpg", quality=90
    )
    print("70 pass2 mask", int(mask.sum() / 255))


def yellow_mask(bgr):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    y = cv2.inRange(hsv, (8, 40, 45), (48, 255, 255))
    y = cv2.morphologyEx(y, cv2.MORPH_CLOSE, np.ones((21, 21), np.uint8))
    # cover adjacent black grilles, buckets, tracks
    dark = cv2.inRange(hsv, (0, 0, 0), (180, 255, 70))
    near = cv2.dilate(y, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 61)))
    machines = cv2.bitwise_or(y, cv2.bitwise_and(dark, near))
    ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (27, 35))
    return cv2.dilate(machines, ker)


def wall_band_mask(bgr):
    """Corrugated facade rows (vertical texture), not sky and not machines."""
    h, w = bgr.shape[:2]
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    machines = yellow_mask(bgr)
    vert = cv2.absdiff(gray, cv2.blur(gray, (1, 21)))
    row_vert = vert.mean(axis=1)
    ylw = (cv2.inRange(hsv, (8, 40, 45), (48, 255, 255)) > 0).mean(axis=1)
    row_ok = (row_vert > 6.2) & (ylw < 0.22)
    row_ok[: int(h * 0.05)] = False
    row_ok[int(h * 0.40) :] = False
    band = np.zeros((h, w), np.uint8)
    band[row_ok] = 255
    facade = cv2.bitwise_and(band, cv2.bitwise_not(machines))
    # keep pixels that look like siding or letters on siding (not pure sky)
    not_sky = cv2.bitwise_not(cv2.inRange(hsv, (100, 0, 210), (130, 60, 255)))
    facade = cv2.bitwise_and(facade, not_sky)
    return facade, machines


def wall_text_mask(bgr):
    """3D wall letters interrupt vertical siding ribs; detect that residual."""
    facade, machines = wall_band_mask(bgr)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    # blur along the rib (vertical); letters stick out from that average
    rib = cv2.blur(gray, (1, 41))
    diff = cv2.absdiff(gray, rib)
    _, th = cv2.threshold(diff, 11, 255, cv2.THRESH_BINARY)
    letters = cv2.bitwise_and(th, facade)
    letters = cv2.morphologyEx(letters, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    letters = cv2.dilate(letters, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 13)))
    letters = cv2.bitwise_and(letters, facade)
    letters = cv2.bitwise_and(letters, cv2.bitwise_not(machines))
    return letters, machines


def fill_vertical(img, mask):
    """Interpolate along columns so corrugated vertical ribs stay intact."""
    out = img.copy().astype(np.float32)
    h, w = img.shape[:2]
    m = mask > 0
    for x in range(w):
        bad = m[:, x]
        if not np.any(bad):
            continue
        ys_g = np.flatnonzero(~bad)
        ys_b = np.flatnonzero(bad)
        if ys_g.size < 8:
            continue
        for c in range(3):
            out[ys_b, x, c] = np.interp(ys_b, ys_g, img[ys_g, x, c].astype(np.float32))
    return np.clip(out, 0, 255).astype(np.uint8)


def fill_horizontal(img, mask):
    out = img.copy().astype(np.float32)
    h, w = img.shape[:2]
    m = mask > 0
    for y in range(h):
        bad = m[y]
        if not np.any(bad):
            continue
        xs_g = np.flatnonzero(~bad)
        xs_b = np.flatnonzero(bad)
        if xs_g.size < 10:
            continue
        for c in range(3):
            out[y, xs_b, c] = np.interp(xs_b, xs_g, img[y, xs_g, c].astype(np.float32))
    return np.clip(out, 0, 255).astype(np.uint8)


def debug_video_frames():
    for name, idx in [
        ("f095a0e4", 0),
        ("f095a0e4", 151),
        ("f095a0e4", 301),
        ("f26fc6f1", 0),
        ("f26fc6f1", 161),
        ("f26fc6f1", 322),
    ]:
        bgr = cv2.imread(str(PREV / f"{name}_f{idx}.jpg"))
        mask, machines = wall_text_mask(bgr)
        filled = fill_vertical(bgr, mask)
        out = filled
        out[machines > 0] = bgr[machines > 0]
        vis = bgr.copy()
        vis[mask > 0] = (0, 0, 255)
        preview(np.hstack([bgr, vis, out]), f"dbg_{name}_{idx}.jpg", max_w=1400)
        print(name, idx, "mask", int(mask.sum() / 255))


def process_video(src, tag):
    import imageio.v2 as imageio

    # restore original video first
    shutil.copy2(BAK / src.name, src)
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
        filled = fill_vertical(frame, mask)
        out = filled
        out[machines > 0] = frame[machines > 0]
        writer.append_data(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))
        if i in samples:
            vis = frame.copy()
            vis[mask > 0] = (0, 0, 255)
            preview(np.hstack([frame, vis, out]), f"{tag}_f{i}_cmp.jpg", max_w=1080)
            print(" sample", i, "mask", int(mask.sum() / 255))
        i += 1
        if i % 80 == 0:
            print("  ", i, "/", n)
    writer.close()
    cap.release()
    shutil.copy2(tmp, src)
    print("saved", src)


if __name__ == "__main__":
    import sys

    mode = sys.argv[1] if len(sys.argv) > 1 else "photos"
    if mode == "photos":
        fix_72()
        fix_70()
    elif mode == "debugvid":
        debug_video_frames()
    elif mode == "video1":
        process_video(ROOT / r"used\Komatsu\f095a0e4e0e23d12d80e0258a0b63670.mp4", "koma")
    elif mode == "video2":
        process_video(ROOT / r"used\Mining truck\f26fc6f16bda7ccc22a7bf99d93f1312.mp4", "mine")
    else:
        print("unknown", mode)
