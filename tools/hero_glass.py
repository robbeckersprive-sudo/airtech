"""Front-glass layer for the granule canvas: the empty tube's reflections and walls, with alpha, so granules
drawn underneath read as being inside the glass. Output covers the canvas box BX (photo px)."""
import os, json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys; sys.path.insert(0, os.path.join(ROOT, 'src'))
from pages import TUBE as SEC, GRAIN_BOX as BX   # single source for the tube geometry and canvas box
D = ROOT


def cr(pts, n=24):
    out = []; p = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(p) - 2):
        for k in range(n):
            t = k / n; t2 = t * t; t3 = t2 * t
            out.append(tuple(.5 * ((2 * p[i][j]) + (-p[i - 1][j] + p[i + 1][j]) * t + (2 * p[i - 1][j] - 5 * p[i][j] + 4 * p[i + 1][j] - p[i + 2][j]) * t2
                                   + (-p[i - 1][j] + 3 * p[i][j] - 3 * p[i + 1][j] + p[i + 2][j]) * t3) for j in (0, 1)))
    out.append(tuple(pts[-1])); return out


im = Image.open(os.path.join(ROOT, 'images', '01-hero-pijpleiding-leeg-1536.webp')).convert('RGB')
x0, y0, x1, y1 = BX
crop = im.crop(BX)
arr = np.asarray(crop).astype(np.float32)
W, H = crop.size
bot = [(x - x0, y - y0) for x, y in cr([s[0] for s in SEC])]
top = [(x - x0, y - y0) for x, y in cr([s[1] for s in SEC])]

tube = Image.new('L', (W, H), 0); ImageDraw.Draw(tube).polygon(bot + top[::-1], fill=255)
tube = np.asarray(tube) > 0
tube_d = ndimage.binary_dilation(tube, iterations=6)
# distance from the tube outline (inside), to build the wall band
dist_in = ndimage.distance_transform_edt(tube)

L = arr @ np.array([.299, .587, .114])
Lb = ndimage.gaussian_filter(L, 10)
hp = L - Lb
hl = np.clip((hp - 4) / 18, 0, 1)                 # bright detail: reflections AND background seen through
# keep only long, thin streaks (reflections on the glass); blobs are background behind the tube
lab, n = ndimage.label(hl > .25)
keep = np.zeros(n + 1, bool)
for i, sl in enumerate(ndimage.find_objects(lab), 1):
    ys, xs = np.nonzero(lab[sl] == i)
    if len(xs) < 25: continue
    c = np.cov(np.vstack([xs, ys]).astype(float))
    ev = np.sort(np.linalg.eigvalsh(c))[::-1]
    length, width = 4 * np.sqrt(max(ev[0], 1e-6)), 4 * np.sqrt(max(ev[1], 1e-6))
    keep[i] = length > 70 and length / max(width, 1) > 5
hl = hl * ndimage.binary_dilation(keep[lab], iterations=2)
wall = np.clip(1 - (dist_in - 4) / 9, 0, 1) * tube  # 4..13 px band just inside the wall
alpha = np.maximum(hl * .9, wall * .7)
alpha = np.maximum(alpha, .06 * tube)              # faint glass veil over everything inside
alpha *= tube_d
alpha = ndimage.gaussian_filter(alpha, .8)
rgba = np.dstack([arr, np.clip(alpha * 255, 0, 255)]).astype(np.uint8)
OUT = os.path.join(ROOT, 'images', 'hero-glass.webp')
Image.fromarray(rgba, 'RGBA').save(OUT, quality=86, method=6)
print('glass', os.path.getsize(OUT), 'bytes', W, H)
