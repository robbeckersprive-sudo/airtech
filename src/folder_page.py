"""Productfolder: a 4-page A4 print document per product, rendered to PDF by tools/render_folders.py.

Same source as the product pages (PRODUCTS) and the same tokens (tokens.css), so a folder never
drifts from the site. Only verified content is used: nothing here is written for the folder alone
except the section labels.

Brand: BRANDS holds the per-brand values (name, logo, accent tokens). A second brand or a dealer
co-brand is one more entry; the template reads only from the brand dict.

Layer 2 (personalised folder) hooks in through `recipient`: a dict with company / application that
is printed on the cover. Not used by the static build.
"""
import glob
import os
from datetime import date
from html import escape

from components import ROOT, SITE, ORG, PHONE_DISPLAY, ADDRESS, EMAIL, contact_url, COMPONENTEN
from product_data import PRODUCTS
from product_routes import PRODUCT_ROUTES
from project_data import PROJECTS

OUT_DIR = os.path.join(ROOT, 'folders')
BRANDS = {
    'airtechnic': dict(name=ORG, logo='airtechnic-logo-transparent.png',
                       tokens={'--brand-ink': 'var(--steel-900)', '--brand-accent': 'var(--red)',
                               '--brand-band': 'var(--steel-950)'}),
}
# Verified project cases that show the product in use (project_data.py holds the facts).
PRACTICE = {'cycloonafscheider': 'driessen-food-extrusion'}
MONTHS = ['januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli', 'augustus', 'september',
          'oktober', 'november', 'december']


IMG_DIR = os.path.join(OUT_DIR, 'img')
FONT_DIR = os.path.join(OUT_DIR, 'fonts')
# key: (family, style, source woff2, wdth, wght). Static Archivo instances: Chromium writes variable fonts into a PDF as Type3 glyphs (not real,
# embedded fonts), so the folder uses fixed instances cut from the site's variable woff2.
FONT_INSTANCES = {  # family: (source, wdth, wght)
    'archivo-folder-400': ('Archivo Folder', 'normal', 'archivo-normal-100-900-latin.woff2', 100, 400),
    'archivo-folder-700': ('Archivo Folder', 'normal', 'archivo-normal-100-900-latin.woff2', 100, 700),
    'archivo-folder-head': ('Archivo Folder Head', 'normal', 'archivo-normal-100-900-latin.woff2', 78, 800),
    'archivo-folder-display': ('Archivo Folder Display', 'normal', 'archivo-normal-100-900-latin.woff2', 72, 850),
    'archivo-folder-wide': ('Archivo Folder Wide', 'italic', 'archivo-italic-100-900-latin.woff2', 125, 300),
}


def _fresh(out, src):
    return os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(src)


def build_fonts():
    from fontTools.ttLib import TTFont
    from fontTools.varLib.instancer import instantiateVariableFont
    os.makedirs(FONT_DIR, exist_ok=True)
    css = []
    for key, (family, style, src, wdth, wght) in FONT_INSTANCES.items():
        src_path = os.path.join(ROOT, 'assets', 'fonts', src)
        file = key + '.ttf'
        out = os.path.join(FONT_DIR, file)
        if not _fresh(out, src_path):
            font = instantiateVariableFont(TTFont(src_path), {'wdth': wdth, 'wght': wght})
            font.flavor = None
            names = font['name']
            ps = family.replace(' ', '') + '-' + str(wght) + ('Italic' if style == 'italic' else '')
            for nid, val in ((1, family), (2, 'Italic' if style == 'italic' else 'Regular'),
                             (4, f'{family} {wght}'), (6, ps), (16, family), (17, str(wght))):
                names.setName(val, nid, 3, 1, 0x409)
            font.save(out)
        css.append(f"@font-face{{font-family:'{family}';font-style:{style};font-weight:{wght};"
                   f"src:url(fonts/{file}) format('truetype');}}")
    for w in (400, 500):  # IBM Plex Mono is static already: the site's files are used as they are
        css.append(f"@font-face{{font-family:'IBM Plex Mono';font-weight:{w};"
                   f"src:url(../assets/fonts/ibm-plex-mono-normal-{w}-latin.woff2) format('woff2');}}")
    return '\n'.join(css)


def _img(name, px, folder='images', jpeg=False, matte=None, palette=False):
    """Print-sized copy of a site image (about 250 dpi at its placed size) in folders/img/.

    The site's webp sets are screen-sized and would make a 8 MB PDF; Chromium re-encodes every
    transparent image as lossless PNG, so the pixel count is what decides the file size. A cut-out
    that sits on a flat colour gets `matte` (that colour) and becomes a JPEG; one on a gradient
    gets `palette` (256 colours, dithered: invisible at print size, a fifth of the bytes)."""
    from PIL import Image
    if folder == 'images':
        files = glob.glob(os.path.join(ROOT, 'images', name + '-*.webp'))
        sizes = {int(f.rsplit('-', 1)[1].split('.')[0]): f for f in files
                 if f.rsplit('-', 1)[1].split('.')[0].isdigit()}
        src = sizes[min((s for s in sizes if s >= px), default=max(sizes))]
    else:
        src = os.path.join(ROOT, folder, name)
    base = os.path.splitext(os.path.basename(name))[0]
    jpeg = jpeg or bool(matte)
    out = os.path.join(IMG_DIR, f'{base}-{px}' + ('-p' if palette else '') + '.' + ('jpg' if jpeg else 'png'))
    if not _fresh(out, src):
        os.makedirs(IMG_DIR, exist_ok=True)
        im = Image.open(src)
        im.thumbnail((px, px * 4), Image.LANCZOS)
        if matte:
            flat = Image.new('RGBA', im.size, matte)
            flat.alpha_composite(im.convert('RGBA'))
            im = flat
        if jpeg:
            im.convert('RGB').save(out, quality=80, optimize=True, progressive=True)
        elif palette:
            im.convert('RGBA').quantize(256, method=Image.Quantize.FASTOCTREE,
                                        dither=Image.Dither.FLOYDSTEINBERG).save(out, optimize=True)
        else:
            im.save(out, optimize=True)
    return 'img/' + os.path.basename(out)


def _kicker(d):
    hrefs = [h for _t, h, _i in COMPONENTEN]
    url = 'componenten-' + d['category'] + '.html'
    family = list(PRODUCT_ROUTES.get(d['category'], {}).values())
    g = hrefs.index(url) + 1 if url in hrefs else 0
    k = family.index(d['slug']) + 1 if d['slug'] in family else 0
    return escape(d['family_name']) + (f' · {g}.{k}' if g and k else '')


def _title_block(d, sheet, total, brand, today):
    return f'''<footer class="tb">
    <div class="tb__brand"><img src="{_img(brand['logo'], 600, 'assets/img')}" alt="{escape(brand['name'])}"></div>
    <div><small>Document</small>Productfolder · {escape(d['name'])}</div>
    <div><small>Uitgave</small>{today}</div>
    <div><small>Online</small><a href="{SITE}/{d['slug']}.html">{SITE.split('//')[1]}/{d['slug']}.html</a></div>
    <div class="tb__sheet"><small>Blad</small>{sheet}/{total}</div>
  </footer>'''


def folder_html(slug, brand_key='airtechnic', recipient=None):
    d = PRODUCTS[slug]
    brand = BRANDS[brand_key]
    t = date.today()
    today = f'{t.day} {MONTHS[t.month - 1]} {t.year}'
    name = escape(d['name'])
    views = {label: image for label, image, *_ in d['views']}
    hero = d['image']
    cutaway = d['cutaway']
    total = 4
    tb = lambda n: _title_block(d, n, total, brand, today)  # noqa: E731
    fonts = build_fonts()
    brand_style = ';'.join(f'{k}:{v}' for k, v in brand['tokens'].items())

    facts = ''.join(f'<div><dt>{escape(k)}</dt><dd>{escape(v)}</dd></div>' for k, v in d['facts'])
    for_line = ''
    if recipient:
        for_line = (f'<p class="cv__for"><small>Opgesteld voor</small>{escape(recipient.get("company", ""))}'
                    + (f'<span>{escape(recipient["application"])}</span>' if recipient.get('application') else '')
                    + '</p>')
    cover = f'''<section class="sheet cv">
  <header class="cv__top">
    <img class="cv__logo" src="{_img(brand['logo'], 600, 'assets/img')}" alt="{escape(brand['name'])}">
    <p class="mono">Productfolder<br><span>{_kicker(d)}</span></p>
  </header>
  <div class="cv__band">
    <div class="cv__copy">
      <p class="mono cv__eyebrow">Componenten · {escape(d['family_name'])}</p>
      <h1>{name}</h1>
      <p class="cv__lead">{escape(d['lead'])}</p>
      <dl class="cv__facts">{facts}</dl>
      {for_line}
    </div>
    <figure class="cv__plate"><img src="{_img(hero, 900, palette=True)}" alt="{escape(d['views'][0][2])}"></figure>
    <span class="cv__axis" aria-hidden="true"></span>
  </div>
  {tb(1)}
</section>'''

    markers = ''.join(f'<span class="hs" style="left:{x}%;top:{y}%">{i}</span>'
                      for i, (_t, _x, x, y) in enumerate(d['steps'], 1))
    steps = ''.join(f'<li><span class="n">{i:02d}</span><div><h3>{escape(title)}</h3><p>{escape(text)}</p></div></li>'
                    for i, (title, text, *_xy) in enumerate(d['steps'], 1))
    werking = f'''<section class="sheet">
  <header class="sh"><p class="mono">01 · Werking</p><h2>{d['principle_title']}</h2><p>{escape(d['principle_intro'])}</p></header>
  <div class="wk">
    <figure class="wk__plate"><div class="wk__img"><img src="{_img(cutaway, 900, matte='#E3E8ED')}" alt="{name} · schematische doorsnede">{markers}</div>
      <figcaption>{name} · schematische doorsnede van het werkingsprincipe</figcaption></figure>
    <div class="wk__steps"><h3 class="mono">{escape(d['step_heading'])}</h3><ol>{steps}</ol>
      <p class="note">{escape(d['note'])}</p></div>
  </div>
  {tb(2)}
</section>'''

    uses = ''.join(f'<div><dt>{escape(title)}</dt><dd>{escape(text)}</dd></div>' for title, text in d['applications'])
    rows = ''.join(f'<tr><th scope="row">{k}</th><td>{escape(v)}</td></tr>' for k, v in d['spec_rows'])
    side = [(lab, img) for lab, img in views.items() if lab not in ('Doorsnede',)][1:3]
    side_figs = ''.join(f'<figure><img src="{_img(img, 420, palette=True)}" alt="{name} · {escape(lab.lower())}"><figcaption>{escape(lab)}</figcaption></figure>'
                        for lab, img in side)
    sector_label = 'Sectoren' if slug == 'cycloonafscheider' else 'Toepasbaarheid'
    selectie = f'''<section class="sheet">
  <header class="sh"><p class="mono">02 · Toepassing</p><h2>{d['context_title']}</h2><p>{escape(d['context_intro'])}</p></header>
  <dl class="uses">{uses}</dl>
  <p class="sectors"><strong class="mono">{sector_label}</strong> {escape(d['sectors'])}</p>
  <div class="sel">
    <div class="sel__copy"><p class="mono">03 · Selectie</p><h2>Afgestemd op<br><em>uw proces</em></h2>
      <p>{escape(d['selection_intro'])}</p>
      <div class="sel__views">{side_figs}</div></div>
    <table class="specs"><thead><tr><th scope="col">Criterium</th><th scope="col">Waar we op letten</th></tr></thead><tbody>{rows}</tbody></table>
  </div>
  {tb(3)}
</section>'''

    practice = ''
    pkey = PRACTICE.get(slug)
    if pkey:
        p = PROJECTS[pkey]
        photo = p['photos'][0]
        pfacts = ''.join(f'<div><dt>{escape(v.replace("≈ ", "ca. "))}</dt><dd>{escape(k)}</dd></div>' for v, k in p['facts'])
        practice = f'''<article class="pr">
    <figure><img src="{_img(photo[0], 820, 'images/project-originals', jpeg=True)}" alt="{escape(photo[1])}"><figcaption>{escape(photo[1])}</figcaption></figure>
    <div><p class="mono">04 · In de praktijk · {escape(p['sector'])}</p><h2>{escape(p['name'])}</h2>
      <p>{escape(p['lead'])}</p><dl class="pr__facts">{pfacts}</dl><p>{escape(p['solution'])}</p>
      <a href="{SITE}/project-{pkey}.html">Lees het project online</a></div>
  </article>'''
    first = lambda text: text.split('. ')[0].rstrip('.') + '.'  # noqa: E731  (a whole sentence, never a cut-off)
    rel = ''.join(f'<li><img src="{_img(image, 240, palette=True)}" alt=""><div><h3>{escape(label)}</h3><p>{escape(first(text))}</p><a href="{SITE}/{href}">Bekijk online</a></div></li>'
                  for label, image, text, href in d['related'][:3])
    ask = d['faq_items'][-1][1]
    doc_url = f"{SITE}/{slug}.html{contact_url(d['documentation_topic'])}"
    contact = f'''<section class="sheet">
  {practice}
  <section class="rel"><p class="mono">05 · {d['related_title'].replace('<em>', '').replace('</em>', '')}</p><ul>{rel}</ul></section>
  <section class="ct">
    <div><h2>{escape(d['contact_title'])}</h2><p>{escape(d['contact_intro'])}</p>
      <p class="ct__ask"><strong>Voor een gericht voorstel.</strong> {escape(ask)}</p></div>
    <ul class="ct__lines mono">
      <li><small>Bellen</small>{PHONE_DISPLAY}</li>
      <li><small>Mailen</small><a href="mailto:{EMAIL}">{EMAIL}</a></li>
      <li><small>Bezoeken</small>{ADDRESS[0]}, 5741 TX {ADDRESS[1]}</li>
      <li class="ct__cta"><a href="{doc_url}">Vraag documentatie aan</a></li>
    </ul>
  </section>
  {tb(4)}
</section>'''

    return f'''<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<title>{name} · Productfolder · {escape(brand['name'])}</title>
<meta name="author" content="{escape(brand['name'])}">
<meta name="description" content="{escape(d['lead'])}">
<style>{fonts}</style>
<link rel="stylesheet" href="../assets/css/tokens.css">
<link rel="stylesheet" href="../assets/css/folder-print.css">
</head>
<body data-brand="{brand_key}" style="{brand_style}">
<main>
{cover}
{werking}
{selectie}
{contact}
</main>
</body>
</html>
'''


FOLDER_SLUGS = ['cycloonafscheider']  # POC: one product; the template works for every PRODUCTS slug.


def build_folders(slugs=FOLDER_SLUGS):
    os.makedirs(OUT_DIR, exist_ok=True)
    paths = []
    for slug in slugs:
        path = os.path.join(OUT_DIR, slug + '.print.html')
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(folder_html(slug))
        paths.append(path)
    return paths


if __name__ == '__main__':
    for p in build_folders():
        print(p)
