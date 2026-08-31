# -*- coding: utf-8 -*-
"""Locate blue license plates on Mixing tank photo 70."""
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
print("size", w, h)

hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
blue = cv2.inRange(hsv, (92, 55, 40), (130, 255, 240))
# ignore sky: keep lower 55% of image
blue[: int(h * 0.42), :] = 0
blue = cv2.morphologyEx(blue, cv2.MORPH_CLOSE, np.ones((11, 11), np.uint8))

cnts, _ = cv2.findContours(blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
found = []
vis = bgr.copy()
for c in cnts:
    a = cv2.contourArea(c)
    if a < 400:
        continue
    x, y, rw, rh = cv2.boundingRect(c)
    ar = rw / max(rh, 1)
    print(f"blob area={int(a)} rect=({x},{y},{x+rw},{y+rh}) size={rw}x{rh} ar={ar:.2f}")
    if rh < 12 or rw < 30 or ar < 1.1 or ar > 6.5:
        continue
    found.append((x, y, x + rw, y + rh, a))
    cv2.rectangle(vis, (x, y), (x + rw, y + rh), (0, 0, 255), 4)

print("kept", found)

# also dump lower-front crop for manual look
front = bgr[int(h * 0.45) : h, 0 : int(w * 0.72)]
rgb = cv2.cvtColor(front, cv2.COLOR_BGR2RGB)
Image.fromarray(rgb).save(PREV / "70_front_bumpers.jpg", quality=90)
small = cv2.resize(vis, (1100, int(h * 1100 / w)))
cv2.imwrite(str(PREV / "70_plate_detect.jpg"), small, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

# crops of each kept blob with padding
for i, (x1, y1, x2, y2, a) in enumerate(found):
    pad = 40
    c1, cy1 = max(0, x1 - pad), max(0, y1 - pad)
    c2, cy2 = min(w, x2 + pad), min(h, y2 + pad)
    rgb = cv2.cvtColor(bgr[cy1:cy2, c1:c2], cv2.COLOR_BGR2RGB)
    Image.fromarray(rgb).save(PREV / f"70_plate_c{i}.jpg", quality=92)
    print("crop", i, (c1, cy1, c2, cy2))
