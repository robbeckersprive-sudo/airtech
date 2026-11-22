"""Blueprint line drawings of the werkwijze photos (home block 5 "Van tekening tot installatie").

Each step first shows its photo as a technical drawing (pale lines on a steel drawing sheet with a 24px grid); scrolling
plots the real photo over it behind the red scan line. Lines come from a difference of Gaussians on the photo, so the
drawing matches the photo pixel for pixel. Designer drawings win: a file tools/drawing-src/<name>.{webp,png,jpg} (same
1672 x 941 framing as the photo, registered to it) is used instead of the generated one.
Writes images/<name>-tekening-<w>.{webp,avif} + manifest entries.
Run: python tools/drawing_versions.py"""
import json, os
from PIL import Image, ImageFilter, ImageOps, ImageChops, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, 'images')
NAMES = ['22-proces-analyse', '23-proces-engineering', '24-proces-realisatie', '25-proces-inbedrijfstelling']
SHEET, MINOR, MAJOR, INK = (14, 42, 71), (22, 58, 94), (30, 70, 110), (214, 228, 242)


def drawing(im):
    g = im.convert('L')
    s = g.width / 800                                    # keep the line weight constant across sizes
    a = g.filter(ImageFilter.GaussianBlur(1.2 * s)); b = g.filter(ImageFilter.GaussianBlur(3.2 * s))
    lines = ImageOps.autocontrast(ImageChops.subtract(b, a), cutoff=1.5)
    lines = lines.point(lambda v: 0 if v < 38 else min(255, int((v - 38) * 2.2)))
    W, H = g.size
    sheet = Image.new('RGB', (W, H), SHEET)
    d = ImageDraw.Draw(sheet)
    step = max(12, round(24 * s))
    for x in range(0, W, step):
        d.line([(x, 0), (x, H)], fill=MAJOR if (x // step) % 4 == 0 else MINOR)
    for y in range(0, H, step):
        d.line([(0, y), (W, y)], fill=MAJOR if (y // step) % 4 == 0 else MINOR)
    return Image.composite(Image.new('RGB', (W, H), INK), sheet, lines)


SRC = os.path.join(ROOT, 'tools', 'drawing-src')


def designer(n):
    for ext in ('webp', 'png', 'jpg'):
        f = os.path.join(SRC, f'{n}.{ext}')
        if os.path.exists(f):
            return Image.open(f).convert('RGB')
    return None


def main():
    man = json.load(open(os.path.join(IMG, 'manifest.json'), encoding='utf-8'))
    for n in NAMES:
        m = man[n]
        widths = [w for w in m['widths'] if w <= 1200]
        given = designer(n)
        for w in widths:
            if given is not None:
                out = given.resize((w, round(given.height * w / given.width)), Image.LANCZOS)
            else:
                out = drawing(Image.open(os.path.join(IMG, f'{n}-{w}.webp')))
            out.save(os.path.join(IMG, f'{n}-tekening-{w}.webp'), quality=82)
            try:
                out.save(os.path.join(IMG, f'{n}-tekening-{w}.avif'), quality=58)
            except Exception as e:
                print('avif skipped', e)
        h = round(m['h'] * widths[-1] / m['w'])
        man[n + '-tekening'] = {'w': widths[-1], 'h': h, 'widths': widths, 'alpha': False}
        print(n, widths, 'designer' if given is not None else 'generated')
    json.dump(man, open(os.path.join(IMG, 'manifest.json'), 'w', encoding='utf-8'), indent=2, ensure_ascii=False)


if __name__ == '__main__':
    main()
