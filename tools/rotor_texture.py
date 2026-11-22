"""Rotor texture for the Doorstroom hero's dosing sheet (33-hero-doseersluis).

The rotor behind the inspection glass is photographed in perspective (an ellipse rx 81 / ry 100 in 570x380 photo units,
centre 306,184.5). The hero spins a copy of it in "unsquashed" space. That copy must not carry the factory-window glare
that sits on the glass (upper left), or the glare would spin along. This script cuts the rotor ellipse from the 1536px
photo, unsquashes it to a circle, replaces the glare area with the pocket 90 degrees further (the rotor has 8 vanes),
squashes it back and writes images/33-hero-doseersluis-rotor.{webp,avif}. Run: python tools/rotor_texture.py"""
from PIL import Image, ImageDraw, ImageFilter
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'images', '33-hero-doseersluis-1536.webp')
CX, CY, RX, RY = 306, 184.5, 81, 100      # rotor ellipse in photo units (570 x 380)
BOX = (CX - RX, CY - RY, CX + RX, CY + RY)
GLARE = [(258, 117, 30, 26), (243, 150, 12, 22)]   # (cx, cy, rx, ry) glare spots on the glass, photo units


def main():
    im = Image.open(SRC).convert('RGB')
    s = im.width / 570
    crop = im.crop(tuple(round(v * s) for v in BOX))
    w, h = crop.size
    k = RX / RY
    circ = crop.resize((round(w / k), h), Image.LANCZOS)          # unsquashed: the rotor is round here
    cw, ch = circ.size
    donor = circ.rotate(-90, resample=Image.BICUBIC, center=(cw / 2, ch / 2))   # pocket from 90 deg clockwise moves here
    mask = Image.new('L', circ.size, 0)
    d = ImageDraw.Draw(mask)
    for gx, gy, grx, gry in GLARE:
        x = (gx - BOX[0]) * s / k; y = (gy - BOX[1]) * s
        d.ellipse((x - grx * s / k, y - gry * s, x + grx * s / k, y + gry * s), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(14 * s / 2.7))
    clean = Image.composite(donor, circ, mask).resize((w, h), Image.LANCZOS)
    for ext, kw in (('webp', {'quality': 86}), ('avif', {'quality': 62})):
        try:
            clean.save(os.path.join(ROOT, 'images', f'33-hero-doseersluis-rotor.{ext}'), **kw)
        except Exception as e:      # avif needs pillow-avif; webp is the fallback the page uses
            print('skip', ext, e)
    print('rotor texture', clean.size, 'box', BOX)


if __name__ == '__main__':
    main()
