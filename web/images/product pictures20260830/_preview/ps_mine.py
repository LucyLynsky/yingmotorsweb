# -*- coding: utf-8 -*-
"""Wipe the factory wall behind the mining trucks; keep machines and ground."""
from pathlib import Path
import shutil
import cv2
import numpy as np

ROOT = Path(r"E:\codePrj\web\images\product pictures20260830")
PREV = ROOT / "_preview"
BAK = ROOT / "_backup"
SRC = ROOT / r"used\Mining truck\f26fc6f16bda7ccc22a7bf99d93f1312.mp4"


def preview(bgr, name, max_w=1100):
    h, w = bgr.shape[:2]
    small = cv2.resize(bgr, (max_w, int(h * max_w / w)), interpolation=cv2.INTER_AREA)
    cv2.imwrite(str(PREV / name), small, [int(cv2.IMWRITE_JPEG_QUALITY), 90])


def keep_mask(bgr):
    """Yellow machines + green trees only. Do not treat dark wall letters as machines."""
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    yellow = cv2.inRange(hsv, (8, 35, 40), (42, 255, 255))
    yellow = cv2.morphologyEx(yellow, cv2.MORPH_CLOSE, np.ones((17, 17), np.uint8))
    green = cv2.inRange(hsv, (35, 40, 40), (90, 255, 255))
    keep = cv2.bitwise_or(yellow, green)
    return cv2.dilate(keep, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 11)))


def wall_mask(bgr):
    """Wipe facade from roof down to each column's machine top (or a deep default)."""
    h, w = bgr.shape[:2]
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    keep = keep_mask(bgr)

    blue = cv2.inRange(hsv, (95, 45, 50), (135, 255, 220)) > 0
    roof = np.where(blue.sum(axis=0) >= 3, blue.argmax(axis=0), h).astype(np.int32)
    roof = cv2.blur(roof.reshape(1, -1).astype(np.float32), (1, 41)).astype(np.int32).ravel()
    valid = roof[(roof > 8) & (roof < int(h * 0.7))]
    y_roof = int(np.percentile(valid, 5)) if valid.size else int(h * 0.10)

    keep_b = keep > 0
    below = keep_b[y_roof:, :]
    has = below.any(axis=0)
    first = np.argmax(below, axis=0)
    default_stop = int(h * 0.58)
    stops = np.where(has, y_roof + first + 28, default_stop)
    stops = np.clip(stops, y_roof + 12, h).astype(np.int32)
    y_stop = int(stops.max())

    yy = np.arange(h, dtype=np.int32)[:, None]
    wall = ((yy >= y_roof) & (yy < stops[None, :])).astype(np.uint8) * 255
    wall[keep_b] = 0
    wall[: max(0, y_roof - 1)] = 0
    return wall, keep, y_roof, y_stop


def fill_wall_with_sky(img, wall, y_roof):
    """Paint the wall with a smooth overcast strip taken from the real sky."""
    h, w = img.shape[:2]
    out = img.copy()
    sky_h = max(8, min(int(y_roof), 90))
    sky = img[:sky_h].astype(np.float32)
    avg = sky.mean(axis=(0, 1))
    col = sky[-min(12, sky_h) :].mean(axis=0)
    col = 0.18 * col + 0.82 * avg
    col = cv2.GaussianBlur(col.reshape(1, w, 3), (0, 0), 25)[0]
    ys, xs = np.where(wall > 0)
    if ys.size == 0:
        return out
    out[ys, xs] = np.clip(col[xs], 0, 255).astype(np.uint8)
    return out


def erase_frame(bgr):
    wall, keep, y_roof, y_stop = wall_mask(bgr)
    out = fill_wall_with_sky(bgr, wall, y_roof)
    out[keep > 0] = bgr[keep > 0]
    return out, wall, keep, y_roof, y_stop


def debug():
    for idx in (0, 80, 161, 242, 322):
        bgr = cv2.imread(str(PREV / f"f26fc6f1_f{idx}.jpg"))
        out, wall, machines, yt, yb = erase_frame(bgr)
        vis = bgr.copy()
        vis[wall > 0] = (0, 0, 255)
        h = bgr.shape[0]
        y2 = min(h, int(h * 0.55))
        preview(np.hstack([bgr[:y2], vis[:y2], out[:y2]]), f"mine_wipe_{idx}.jpg", max_w=1500)
        preview(out, f"mine_wipe_full_{idx}.jpg", max_w=720)
        print("frame", idx, "wall", int(wall.sum() / 255), "roof", yt, "stop", yb)


def process():
    import imageio.v2 as imageio

    shutil.copy2(BAK / SRC.name, SRC)
    cap = cv2.VideoCapture(str(SRC))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"mine video {n} frames @{fps:.2f}")
    tmp = PREV / "mine_out.mp4"
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
        out, wall, _, _, _ = erase_frame(frame)
        writer.append_data(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))
        if i in samples:
            vis = frame.copy()
            vis[wall > 0] = (0, 0, 255)
            preview(np.hstack([frame, vis, out]), f"mine_run_{i}.jpg", max_w=1200)
            preview(out, f"mine_run_full_{i}.jpg", max_w=720)
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
