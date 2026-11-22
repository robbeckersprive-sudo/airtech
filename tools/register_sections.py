"""Register cross-section renders onto their exterior renders (home block 3 "Röntgen" catalogue).

The X-ray scan line follows the pointer, so section and exterior must sit on the same pixels. Filter, leidingwerk,
big-bag, afsluiter and zeef were rendered registered. Cycloon and doseersluis differ a few percent in scale: this script
fits the section's alpha bounding box onto the exterior's and writes `<section>-reg` in the exterior's sizes
(webp + avif) plus a manifest entry. The blower section faces the other way: it is mirrored first.
Run: python tools/register_sections.py"""
import json, os
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, 'images')
PAIRS = {'04-cycloon-vrijstaand': '13-cycloon-doorsnede', '06-doseersluis-vrijstaand': '15-doseersluis-doorsnede',
         '03-blower-vrijstaand': '14-blower-doorsnede'}
MIRROR = {'14-blower-doorsnede'}   # rendered facing the other way


def load(name, w):
    return Image.open(os.path.join(IMG, f'{name}-{w}.webp')).convert('RGBA')


def bbox(im):
    return im.getchannel('A').point(lambda a: 255 if a > 40 else 0).getbbox()


def main():
    man = json.load(open(os.path.join(IMG, 'manifest.json'), encoding='utf-8'))
    for ext, sec in PAIRS.items():
        m = man[ext]
        A = load(ext, m['widths'][-1])
        B = load(sec, man[sec]['widths'][-1])
        if sec in MIRROR:
            B = ImageOps.mirror(B)
        B = B.resize((A.width, round(B.height * A.width / B.width)), Image.LANCZOS)
        ba, bb = bbox(A), bbox(B)
        R = Image.new('RGBA', A.size, (0, 0, 0, 0))
        R.paste(B.crop(bb).resize((ba[2] - ba[0], ba[3] - ba[1]), Image.LANCZOS), ba[:2])
        name = sec + '-reg'
        for w in m['widths']:
            im = R if w == A.width else R.resize((w, round(A.height * w / A.width)), Image.LANCZOS)
            im.save(os.path.join(IMG, f'{name}-{w}.webp'), quality=86)
            try:
                im.save(os.path.join(IMG, f'{name}-{w}.avif'), quality=62)
            except Exception as e:
                print('avif skipped', e)
        man[name] = {'w': A.width, 'h': A.height, 'widths': m['widths'], 'alpha': True}
        print(name, A.size)
    json.dump(man, open(os.path.join(IMG, 'manifest.json'), 'w', encoding='utf-8'), indent=2, ensure_ascii=False)


if __name__ == '__main__':
    main()
