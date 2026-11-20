"""Generate three variants of homepage block 3 ("Het juiste component.") as review pages.

    python tools/comp_concepts.py

Reads the built index.html, replaces the components carousel section and adds assets/css/comp-concepts.css +
assets/js/comp-concepts.js. Hero, header and block 2 are the live ones, so the hand-off can be judged for real.
    comp-a.html  A  "Proceslijn"       the process axis (hero plate edge, block 2 line) continues and bends into a
                                       horizontal rail; the eight components are stations with their own symbol
    comp-b.html  B  "Catalogusbladen"  all eight at once as framed plates; registration marks open out on entry,
                                       dimension lines (no numbers) draw around the product on hover
    comp-c.html  C  "Doorsnede A-A"    one large plate; a section line A-A sweeps across as it scrolls past and cuts
                                       the exterior open where a cross-section exists (blower, cyclone, rotary valve)
Copy is the site's own; nothing new is claimed. The live index.html is not touched.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
import components as C  # noqa: E402
from components import COMPONENTEN, icon, pic, sym, _slug  # noqa: E402

# extra process-flow symbols for component groups (after ISO 10628), added to the shared set at build time
C.SYM.update({
    'pipe': '<path d="M5 20v-7a8 8 0 0 1 8-8h6"/><path d="M3 20h4M19 3v4"/>',
    'bag': '<path d="M7 7h10l2 9-3 4H8l-3-4z"/><path d="M9 7V4.5M15 7V4.5"/>',
    'valve': '<path d="M4 7v10l16-10v10z"/><path d="M12 12V5M9.5 5h5"/>',
})
COMP_SYM = {
    'Blowers &amp; ventilatoren': 'Hoogvacuüm', 'Cyclonen': 'Stofafzuiging', 'Filters': 'Filtratie',
    'Doseersluizen': 'Doseren', 'Leidingwerk &amp; koppelingen': 'pipe', 'Big-bag stations': 'bag',
    'Afsluiters': 'valve', 'Zeven': 'Zeven en scheiden',
}
SECTION = {'Blowers &amp; ventilatoren': '14-blower-doorsnede', 'Cyclonen': '13-cycloon-doorsnede',
           'Doseersluizen': '15-doseersluis-doorsnede'}
FLIP_EXT = {'Blowers &amp; ventilatoren'}   # exterior render faces the other way than its section; mirror it to register
REG = ''.join(f'<i class="cx-reg cx-reg--{c}" aria-hidden="true"></i>' for c in ('tl', 'tr', 'bl', 'br'))


def head(h2, extra=''):
    return f'<div class="cx-head">{h2}{extra}</div>'


ALL_LINK = C.link('Alle componenten', '#', cls='cx-all')


# ================================================================= A  Proceslijn
def variant_a(h2):
    slides = ''.join(
        f'''<li class="carousel__slide cxA-st" data-slide style="--i:{i}">
        <span class="cxA-st__node" aria-hidden="true">{sym(COMP_SYM[t], "sym sym--node")}</span>
        <a class="cxA-st__card" href="{h}"><span class="cxA-st__img">{pic(img, "", "(min-width: 960px) 20vw, 60vw")}</span>
          <span class="cxA-st__label"><span>{t}</span>{icon("ur")}</span></a></li>'''
        for i, (t, h, img) in enumerate(COMPONENTEN))
    return f'''<section class="section--home band--sage cx cx--a" aria-labelledby="comp-title" data-cx="a">
  <svg class="cxA-entry" aria-hidden="true" focusable="false" data-cx-entry><path class="cxA-entry__base"/><path class="cxA-entry__flow"/></svg>
  <div class="container" data-carousel>
    {head(h2)}
    <div class="carousel cxA-rail">
      <button class="carousel__btn carousel__btn--prev" type="button" data-prev aria-label="Vorige componenten">{icon("left")}</button>
      <ul class="carousel__track cxA-track" data-track tabindex="0" role="list" aria-label="Componenten (gebruik de pijltjestoetsen om te bladeren)">{slides}</ul>
      <button class="carousel__btn carousel__btn--next" type="button" data-next aria-label="Volgende componenten">{icon("right")}</button>
    </div>
    <div class="carousel__footer">
      <div class="carousel__pager">
        <button class="text-btn" type="button" data-prev>{icon("left")}Vorige</button>
        <span class="carousel__count" data-count aria-live="polite">1 – 4 van 8</span>
        <button class="text-btn" type="button" data-next>Volgende{icon("right")}</button>
      </div>
      {ALL_LINK}
    </div>
  </div>
</section>'''


# ================================================================= B  Catalogusbladen
def variant_b(h2):
    cells = ''.join(
        f'''<li class="cxB-cell" style="--i:{i}"><a class="cxB-card" href="{h}">
        <span class="cxB-plate">{pic(img, "", "(min-width: 960px) 22vw, 45vw")}{REG}
          <i class="cxB-dim cxB-dim--x" aria-hidden="true"></i><i class="cxB-dim cxB-dim--y" aria-hidden="true"></i></span>
        <span class="cxB-label">{sym(COMP_SYM[t])}<span>{t}</span>{icon("ur")}</span></a></li>'''
        for i, (t, h, img) in enumerate(COMPONENTEN))
    return f'''<section class="section--home band--sage cx cx--b" aria-labelledby="comp-title" data-cx="b">
  <div class="container">
    {head(h2, ALL_LINK)}
    <ul class="cxB-grid" data-cx-grid>{cells}</ul>
  </div>
</section>'''


# ================================================================= C  Doorsnede A-A
def variant_c(h2):
    layers = []
    for i, (t, h, img) in enumerate(COMPONENTEN):
        sec = SECTION.get(t)
        sec_html = f'<span class="cxC-sec">{pic(sec, "", "(min-width: 960px) 46vw, 92vw")}</span>' if sec else ''
        layers.append(f'<div class="cxC-layer{" is-on" if i == 1 else ""}{" has-sec" if sec else ""}" data-pick-layer="{_slug(t)}">'
                      f'<span class="cxC-ext{" cxC-ext--flip" if t in FLIP_EXT else ""}">{pic(img, "", "(min-width: 960px) 46vw, 92vw")}</span>{sec_html}</div>')
    picks = ''.join(
        f'''<li><button class="cxC-pick{" is-on" if i == 1 else ""}" type="button" data-pick="{_slug(t)}" data-href="{h}" data-name="{t}"
          aria-pressed="{"true" if i == 1 else "false"}">{sym(COMP_SYM[t])}<span>{t}</span>{'<span class="cxC-tag">A–A</span>' if t in SECTION else ''}</button></li>'''
        for i, (t, h, img) in enumerate(COMPONENTEN))
    return f'''<section class="section--home band--sage cx cx--c" aria-labelledby="comp-title" data-cx="c">
  <div class="container cxC">
    <figure class="cxC-plate" data-cx-plate>
      {"".join(layers)}
      <span class="cxC-cut" aria-hidden="true"><b>A</b><b>A</b></span>
      {REG}
      <figcaption><span data-cx-name>Cyclonen</span><span data-cx-view>Doorsnede A–A</span></figcaption>
    </figure>
    <div class="cxC-side">
      {head(h2)}
      <ul class="cxC-picks" aria-label="Kies een component">{picks}</ul>
      <div class="cxC-actions"><a class="link" href="componenten-cyclonen.html" data-cx-go>Bekijk <span data-cx-goname>Cyclonen</span>{icon("ur")}</a>{ALL_LINK}</div>
    </div>
  </div>
</section>'''


VARIANTS = {'a': ('Proceslijn', variant_a), 'b': ('Catalogusbladen', variant_b), 'c': ('Doorsnede A–A', variant_c)}


def switcher(cur):
    opts = ''.join(f'<a href="comp-{k}.html"{" aria-current=page" if k == cur else ""}><b>{k.upper()}</b><span>{n}</span></a>'
                   for k, (n, _) in VARIANTS.items())
    return (f'<div class="hx-review" role="navigation" aria-label="Blokvarianten (review)"><span class="hx-review__t">Blok 3</span>'
            f'{opts}<span class="hx-review__sep"></span><a href="index.html">Huidig</a></div>')


def main():
    v = lambda p: int(os.path.getmtime(os.path.join(ROOT, p)))  # noqa: E731
    html = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    m = re.search(r'<section class="section--home band--sage carousel-section".*?</section>', html, re.S)
    if not m:
        sys.exit('index.html has no components carousel any more; these variants were built from it.')
    h2 = re.search(r'<h2 id="comp-title".*?</h2>', m.group(0), re.S).group(0)
    for k, (_n, fn) in VARIANTS.items():
        out = html[:m.start()] + fn(h2) + html[m.end():]
        out = out.replace('<html lang="nl"', f'<html lang="nl" data-comp-variant="{k}"', 1)
        out = re.sub(r'(<link rel="stylesheet" href="assets/css/site\.css[^"]*">)',
                     rf'\1\n<link rel="stylesheet" href="assets/css/comp-concepts.css?v={v("assets/css/comp-concepts.css")}">', out, count=1)
        out = re.sub(r'(<script src="assets/js/site\.js[^"]*" defer></script>)',
                     rf'\1\n<script src="assets/js/comp-concepts.js?v={v("assets/js/comp-concepts.js")}" defer></script>', out, count=1)
        out = out.replace('</head>', '<meta name="robots" content="noindex">\n</head>', 1)
        out = out.replace('</body>', switcher(k) + '\n</body>', 1)
        with open(os.path.join(ROOT, f'comp-{k}.html'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(out)
        print('wrote', f'comp-{k}.html')


if __name__ == '__main__':
    main()
