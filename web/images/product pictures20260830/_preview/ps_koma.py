# -*- coding: utf-8 -*-
"""Cover Chinese wall letters on the Komatsu yard video; keep excavators."""
from pathlib import Path
import shutil
import cv2
import numpy as np

ROOT = Path(r"E:\codePrj\web\images\product pictures20260830")
PREV = ROOT / "_preview"
BAK = ROOT / "_backup"
SRC = ROOT / r"used\Komatsu\f095a0e4e0e23d12d80e0258a0b63670.mp4"


def preview(bgr, name, max_w=1100):
    h, w = bgr.shape[:2]
    if w > max_w:
        small = cv2.resize(bgr, (max_w, int(h * max_w / w)), interpolation=cv2.INTER_AREA)
    else:
        small = bgr
    cv2.imwrite(str(PREV / name), small, [int(cv2.IMWRITE_JPEG_QUALITY), 90])


def machine_mask(bgr):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    yellow = cv2.inRange(hsv, (8, 38, 45), (42, 255, 255))
    yellow = cv2.morphologyEx(yellow, cv2.MORPH_CLOSE, np.ones((17, 15), np.uint8))
    dark = cv2.inRange(hsv, (0, 0, 0), (180, 255, 75))
    near = cv2.dilate(yellow, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 41)))
    keep = cv2.bitwise_or(yellow, cv2.bitwise_and(dark, near))
    # grey cab / hydraulics next to yellow
    grey = cv2.inRange(hsv, (0, 0, 35), (180, 55, 210))
    keep = cv2.bitwise_or(keep, cv2.bitwise_and(grey, near))
    return cv2.dilate(keep, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 13)))


def roof_and_sky(bgr):
    """Sky = bright pixels hanging from the top; roof = first building row per column."""
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    h, w = bgr.shape[:2]
    val = hsv[:, :, 2]
    sat = hsv[:, :, 1]
    skyish = ((val >= 175) & (sat <= 70)).astype(np.uint8) * 255
    skyish[:4, :] = 255
    skyish[int(h * 0.72) :, :] = 0
    # keep only components touching the top
    n, lab, stats, _ = cv2.connectedComponentsWithStats(skyish, 8)
    sky = np.zeros((h, w), np.uint8)
    for i in range(1, n):
        x, y, bw, bh, area = stats[i]
        if y <= 2 and area > 80:
            sky[lab == i] = 255
    roof = np.full(w, h, np.int32)
    sky_b = sky > 0
    for x in range(w):
        col = sky_b[:, x]
        if col.any():
            y = int(np.flatnonzero(col)[-1]) + 1
        else:
            # fallback: first darker / more saturated pixel
            ys = np.flatnonzero((val[:, x] < 170) | (sat[:, x] > 72))
            y = int(ys[0]) if ys.size else 0
        roof[x] = np.clip(y, 0, h - 1)
    roof = cv2.blur(roof.reshape(1, -1).astype(np.float32), (1, 31)).ravel().astype(np.int32)
    return sky, roof


def wall_mask(bgr):
    """Facade from roof down to the first machine (or a deep default)."""
    h, w = bgr.shape[:2]
    keep = machine_mask(bgr)
    sky, roof = roof_and_sky(bgr)
    keep_b = keep > 0
    yy = np.arange(h, dtype=np.int32)[:, None]
    default_stop = int(h * 0.58)
    stops = np.empty(w, np.int32)
    for x in range(w):
        y0 = int(roof[x])
        below = keep_b[y0:, x]
        if below.any():
            y1 = y0 + int(np.argmax(below))
        else:
            y1 = default_stop
        # include a little of the wall just above the boom so letter feet go too
        stops[x] = np.clip(y1 + 6, y0 + 8, h)
    stops = cv2.blur(stops.reshape(1, -1).astype(np.float32), (1, 21)).ravel().astype(np.int32)
    wall = ((yy >= roof[None, :]) & (yy < stops[None, :])).astype(np.uint8) * 255
    wall[keep_b] = 0
    wall[sky > 0] = 0
    return wall, keep, sky, roof, stops


def fill_wall(bgr, wall, keep):
    """Paint the letter band with robust per-row siding color (no letter residual)."""
    h, w = bgr.shape[:2]
    region = (wall > 0) & (keep == 0)
    base = bgr.copy().astype(np.float32)
    for y in range(h):
        xs = np.flatnonzero(region[y])
        if xs.size < 10:
            continue
        pix = bgr[y, xs].astype(np.float32)
        med = np.median(pix, axis=0)
        dist = np.linalg.norm(pix - med, axis=1)
        cut = np.percentile(dist, 50)
        good = xs[dist <= max(10.0, cut)]
        if good.size >= 6:
            med = np.median(bgr[y, good], axis=0)
        base[y, xs] = med
    # do not blur across machines: only the painted band is written back
    filled = np.clip(base, 0, 255).astype(np.uint8)
    xs_all = np.arange(w, dtype=np.float32)
    rib = (3.5 * np.sin(2 * np.pi * xs_all / 7.0)).astype(np.float32)
    filled = np.clip(filled.astype(np.float32) + rib[None, :, None], 0, 255).astype(np.uint8)
    out = bgr.copy()
    out[region] = filled[region]
    out[keep > 0] = bgr[keep > 0]
    return out


def erase_frame(bgr):
    wall, keep, sky, roof, stops = wall_mask(bgr)
    out = fill_wall(bgr, wall, keep)
    return out, wall, keep, sky


def debug():
    for idx in (0, 75, 151, 226, 301):
        bgr = cv2.imread(str(PREV / f"koma_f{idx}.jpg"))
        out, wall, keep, sky = erase_frame(bgr)
        vis = bgr.copy()
        vis[wall > 0] = (0, 0, 255)
        y2 = min(bgr.shape[0], 720)
        preview(np.hstack([bgr[:y2], vis[:y2], out[:y2]]), f"koma_wipe_{idx}.jpg", max_w=1500)
        preview(out, f"koma_wipe_full_{idx}.jpg", max_w=720)
        print(
            "frame",
            idx,
            "wall",
            int(wall.sum() / 255),
            "keep",
            int(keep.sum() / 255),
        )


def process():
    import imageio.v2 as imageio

    shutil.copy2(BAK / SRC.name, SRC)
    cap = cv2.VideoCapture(str(SRC))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"koma video {n} frames @{fps:.2f}")
    tmp = PREV / "koma_out.mp4"
    writer = imageio.get_writer(
        str(tmp),
        fps=float(fps),
        codec="libx264",
        quality=7,
        pixelformat="yuv420p",
        macro_block_size=1,
    )
    samples = {0, n // 4, n // 2, 3 * n // 4, max(n - 2, 0)}
    i = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        out, wall, _, _ = erase_frame(frame)
        writer.append_data(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))
        if i in samples:
            vis = frame.copy()
            vis[wall > 0] = (0, 0, 255)
            preview(np.hstack([frame, vis, out]), f"koma_run_{i}.jpg", max_w=1200)
            preview(out, f"koma_run_full_{i}.jpg", max_w=720)
            print(" sample", i, "wall", int(wall.sum() / 255))
        i += 1
        if i % 80 == 0:
            print("  ", i, "/", n)
    writer.close()
    cap.release()
    shutil.copy2(tmp, SRC)
    print("saved", SRC, "frames", i)


if __name__ == "__main__":
    import sys

    mode = sys.argv[1] if len(sys.argv) > 1 else "debug"
    if mode == "debug":
        debug()
    elif mode == "run":
        process()
    else:
        print("unknown", mode)
