"""Convert the supplied kiosk renders (PNG) into AVIF + WebP derivatives for the trade-fair kiosk.

Usage:  python tools/kiosk_images.py <folder with the PNGs>

Writes images/kiosk/<name>-<width>.{avif,webp} and images/kiosk/manifest.json. Kept apart from
images/manifest.json (the site library) so the kiosk can be rebuilt without touching site pages.
"""
import json
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'images', 'kiosk')

# name -> widths. Screens are 1080p or 4K; the panorama spans two screens.
SOURCES = {
    '01-proceslijn-panorama': (3840, 7680),
    '02-cycloon': (1920, 3840),
    '03-filter': (1920, 3840),
    '04-doseersluis': (1920, 3840),
    '05-granulaat-textuur': (1920, 3840),
    '06-totem': (1080, 2160),
}


def main(src):
    os.makedirs(OUT, exist_ok=True)
    manifest = {}
    for name, widths in SOURCES.items():
        path = os.path.join(src, name + '.png')
        im = Image.open(path).convert('RGB')
        manifest[name] = {'w': im.width, 'h': im.height, 'widths': list(widths)}
        for w in widths:
            h = round(im.height * w / im.width)
            r = im if w == im.width else im.resize((w, h), Image.LANCZOS)
            r.save(os.path.join(OUT, f'{name}-{w}.webp'), quality=82, method=6)
            r.save(os.path.join(OUT, f'{name}-{w}.avif'), quality=60, speed=6)
            print(f'{name}-{w}: avif {os.path.getsize(os.path.join(OUT, f"{name}-{w}.avif")) // 1024} KB')
    with open(os.path.join(OUT, 'manifest.json'), 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=1)


if __name__ == '__main__':
    main(sys.argv[1])
