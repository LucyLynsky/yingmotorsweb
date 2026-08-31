# -*- coding: utf-8 -*-
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageOps

ROOT = Path(r"E:\codePrj\web\images\product pictures20260830")
PREV = ROOT / "_preview"
src = ROOT / r"used\Mixing tank\20260830072428_70_24.jpg"
im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
bgr = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
h, w = bgr.shape[:2]


def save(box, name):
    x1, y1, x2, y2 = box
    rgb = cv2.cvtColor(bgr[y1:y2, x1:x2], cv2.COLOR_BGR2RGB)
    Image.fromarray(rgb).save(PREV / name, quality=95)
    print(name, rgb.shape)


save((620, 1860, 860, 2120), "70_p1.jpg")
save((280, 1780, 450, 1980), "70_p2.jpg")
save((0, 1700, 280, 1950), "70_p3.jpg")

# precise blue blobs in these windows
hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
windows = [
    (600, 1850, 860, 2140, "main"),
    (250, 1760, 450, 2000, "mid"),
    (0, 1680, 280, 1960, "far"),
]
for x1, y1, x2, y2, tag in windows:
    roi = hsv[y1:y2, x1:x2]
    blue = cv2.inRange(roi, (90, 50, 50), (130, 255, 255))
    blue = cv2.morphologyEx(blue, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    cnts, _ = cv2.findContours(blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print("---", tag)
    for c in cnts:
        a = cv2.contourArea(c)
        if a < 80:
            continue
        rx, ry, rw, rh = cv2.boundingRect(c)
        print(f"  area={int(a)} orig=({x1+rx},{y1+ry},{x1+rx+rw},{y1+ry+rh}) {rw}x{rh} ar={rw/max(rh,1):.2f}")
