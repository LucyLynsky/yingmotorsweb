# -*- coding: utf-8 -*-
"""Save labeled crops of mixer-truck fronts for plate locating."""
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFont

ROOT = Path(r"E:\codePrj\web\images\product pictures20260830")
PREV = ROOT / "_preview"
src = ROOT / r"used\Mixing tank\20260830072428_70_24.jpg"
im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
bgr = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
h, w = bgr.shape[:2]


def save_rgb(bgr_img, name):
    rgb = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
    Image.fromarray(rgb).save(PREV / name, quality=92)


def labeled_crop(box, name, step=100):
    x1, y1, x2, y2 = box
    crop = bgr[y1:y2, x1:x2].copy()
    vis = crop.copy()
    for x in range(((x1 + step - 1) // step) * step, x2, step):
        cv2.line(vis, (x - x1, 0), (x - x1, y2 - y1), (0, 255, 255), 1)
        cv2.putText(vis, str(x), (x - x1 + 4, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    for y in range(((y1 + step - 1) // step) * step, y2, step):
        cv2.line(vis, (0, y - y1), (x2 - x1, y - y1), (0, 255, 255), 1)
        cv2.putText(vis, str(y), (6, y - y1 + 22), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    save_rgb(crop, name)
    save_rgb(vis, name.replace(".jpg", "_grid.jpg"))


labeled_crop((700, 1650, 2000, 2600), "70_main_front.jpg", 80)
labeled_crop((0, 1450, 950, 2150), "70_left_trucks.jpg", 80)

# HSV blue overlay on main front
hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
blue = cv2.inRange(hsv, (85, 40, 40), (135, 255, 255))
overlay = bgr.copy()
overlay[blue > 0] = (0, 0, 255)
save_rgb(overlay[1650:2600, 700:2000], "70_main_blue.jpg")
save_rgb(overlay[1450:2150, 0:950], "70_left_blue.jpg")
print("wrote crops")
