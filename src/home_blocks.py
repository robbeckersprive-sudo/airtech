"""Home blocks 2 and 3 (Nov 20, after the Doorstroom hero). Styles assets/css/home-blocks.css, behaviour
assets/js/home-blocks.js.

Block 2 "Processchema" — the heading promises one coherent process, so the section draws it: two lines of one
installation. The product line (Solids processing: Opslaan → Doseren → Pneumatisch transport → Zeven en scheiden) carries
granules; the air line (Industriële luchttechniek: Stofafzuiging → Hoogvacuüm → Filtratie → schone lucht) carries air.
They meet where the transport air goes to the filter. Every station is a link; hovering or focusing one fills the
inspector plate next to the heading (photo, solution title, lead). Phones: two vertical lines with photo rows.

Block 3 "Röntgen" — the eight component groups as catalogue plates. A scan line follows the pointer: left of it the
cross-section, right of it the exterior (renders registered by tools/register_sections.py, the blower section mirrored). Phones: a swipe deck where swiping itself moves the scan line, with a progress line.
Copy comes from solution_data / category_data; no new claims."""
import re
from components import (OPLOSSINGEN, COMPONENTEN, SOL_IMG, sym, pic, icon, link, split_lines, _slug, _v, COMP_SYM)
from solution_data import SOLUTIONS
from category_data import CATEGORIES
from cyclone_category_data import CYCLONES

# ---------------------------------------------------------------- block 2
SOL_BY_NAME = {v['name'] if 'name' in v else k: (k, v) for k, v in SOLUTIONS.items()}
GROUP = {name: grp for grp, items in OPLOSSINGEN for name, _h in items}
HREF = {name: h for _g, items in OPLOSSINGEN for name, h in items}

# station order and column (1-4) per line; the join sits in column 3
PRODUCT_LINE = [('Opslaan', 1), ('Doseren', 2), ('Pneumatisch transport', 3), ('Zeven en scheiden', 4)]
AIR_LINE = [('Stofafzuiging', 1), ('Hoogvacuüm', 2), ('Filtratie', 3)]
DEFAULT = 'Pneumatisch transport'


def _sol(name):
    """(slug, data) of a solution by its display name."""
    for k, v in SOLUTIONS.items():
        if v.get('name') == name or _slug(name) == k or _slug(name).replace('-', '') == k.replace('-', ''):
            return k, v
    raise KeyError(name)


def _first_sentence(text):
    text = re.sub(r'<[^>]+>', '', text)
    m = re.match(r'(.+?[.!?])(\s|$)', text)
    return m.group(1) if m else text


def _station(name, col, code, i):
    _k, s = _sol(name)
    on = ' is-on' if name == DEFAULT else ''
    join = ' sx-st--join' if col == 3 else ''
    return (f'<li class="sx-st{join}" style="--c:{col};--i:{i}"><a class="sx-node{on}" href="{HREF[name]}" data-sx-key="{_slug(name)}">'
            f'<span class="sx-node__dot" aria-hidden="true">{sym(name)}</span>'
            f'<span class="sx-node__txt"><span class="sx-node__code" aria-hidden="true">{code}</span>'
            f'<span class="sx-node__name">{name}</span>'
            f'<span class="sx-node__lead">{_first_sentence(s["lead"])}</span></span>'
            f'<span class="sx-node__thumb" aria-hidden="true">{pic(SOL_IMG[name], "", "72px")}</span>'
            f'{icon("ur")}</a></li>')


def _lane(kind, title, stations, letter, end_label):
    lis = ''.join(_station(n, c, f'{letter}{i + 1}', i) for i, (n, c) in enumerate(stations))
    grains = ''.join(f'<i style="--g:{g}"></i>' for g in range(10))
    return f'''<div class="sx-lane sx-lane--{kind}">
        <h3 class="sx-lane__t"><span class="sx-lane__letter" aria-hidden="true">{letter}</span>{title}</h3>
        <div class="sx-lane__body">
          <span class="sx-track" aria-hidden="true"><span class="sx-track__flow">{grains}</span><span class="sx-track__end">{end_label}</span></span>
          <ol class="sx-list">{lis}</ol>
        </div>
      </div>'''


def _inspector():
    plates = []
    for grp, items in OPLOSSINGEN:
        for name, href in items:
            _k, s = _sol(name)
            on = ' is-on' if name == DEFAULT else ''
            plates.append(f'''<div class="sx-insp__item{on}" data-sx-item="{_slug(name)}">
          <div class="sx-insp__img">{pic(SOL_IMG[name], "", "(min-width: 900px) 30vw, 1px")}</div>
          <div class="sx-insp__txt">
            <p class="sx-insp__grp">{grp}</p>
            <p class="sx-insp__title">{s["title"]}</p>
            <p class="sx-insp__lead">{_first_sentence(s["lead"])}</p>
          </div>
        </div>''')
    reg = ''.join(f'<i class="sx-reg sx-reg--{c}"></i>' for c in ('tl', 'tr', 'bl', 'br'))
    return f'''<aside class="sx-insp" aria-hidden="true">
      <div class="sx-insp__plate">{"".join(plates)}{reg}<span class="sx-insp__tag">Oplossing</span></div>
    </aside>'''


def schema_block():
    product = _lane('product', 'Solids processing', PRODUCT_LINE, 'A', 'naar uw proces')
    air = _lane('air', 'Industriële luchttechniek', AIR_LINE, 'B', 'schone lucht')
    return f'''<section class="section--home sx" id="specialisaties" aria-labelledby="spec-title" data-sx>
  <div class="container">
    <div class="sx-head">
      <div class="sx-intro">
        <h2 id="spec-title" class="h2" data-split>{split_lines("Twee specialisaties.<br><em>Eén samenhangend proces.</em>")}</h2>
        <p class="sx-sub">Productstroom en luchtstroom raken elkaar in elke installatie. Daarom bekijken we ze samen.</p>
        <p class="sx-legend" aria-hidden="true"><span class="sx-key sx-key--product"><i></i>Productstroom</span><span class="sx-key sx-key--air"><i></i>Luchtstroom</span></p>
      </div>
      {_inspector()}
    </div>
    <div class="sx-schema" data-sx-schema>
      {product}
      <div class="sx-join" aria-hidden="true"><span class="sx-join__line"></span><span class="sx-join__label">transportlucht naar het filter</span></div>
      {air}
    </div>
  </div>
</section>'''


# ---------------------------------------------------------------- block 3
SECTION_IMG = {   # group -> (cross-section render, mode); scrub needs a registered render
    'Blowers &amp; ventilatoren': ('14-blower-doorsnede-reg', 'scrub'),
    'Cyclonen': ('13-cycloon-doorsnede-reg', 'scrub'),
    'Filters': ('05-filter-doorsnede', 'scrub'),
    'Doseersluizen': ('15-doseersluis-doorsnede-reg', 'scrub'),
    'Leidingwerk &amp; koppelingen': ('07-leidingwerk-doorsnede', 'scrub'),
    'Big-bag stations': ('08-bigbag-doorsnede', 'scrub'),
    'Afsluiters': ('09-afsluiter-doorsnede', 'scrub'),
    'Zeven': ('10-zeef-doorsnede', 'scrub'),
}


def _items(href):
    if 'cyclonen' in href:
        return [i.name for i in CYCLONES['items']]
    slug = href.replace('componenten-', '').replace('.html', '')
    return [i['name'] for i in CATEGORIES[slug]['items']]


def _card(i, title, href, img):
    sec, mode = SECTION_IMG[title]
    names = _items(href)
    sizes = '(min-width: 1100px) 22vw, (min-width: 900px) 30vw, 78vw'
    chips = ''.join(f'<li>{n}</li>' for n in names)
    reg = ''.join(f'<i class="cx-reg cx-reg--{c}"></i>' for c in ('tl', 'tr', 'bl', 'br'))
    return f'''<li class="cx-card" style="--i:{i}"><a class="cx-link" href="{href}" data-cx-card data-scan="{mode}">
        <span class="cx-plate" aria-hidden="true">
          <span class="cx-img cx-img--ext">{pic(img, "", sizes)}</span>
          <span class="cx-img cx-img--sec">{pic(sec, "", sizes)}</span>
          <i class="cx-scan"><b>Doorsnede</b></i>{reg}
          <span class="cx-no">{i + 1:02d}<small>/{len(COMPONENTEN):02d}</small></span>
          <ul class="cx-chips">{chips}</ul>
        </span>
        <span class="cx-meta">{sym(COMP_SYM[title], "sym cx-sym")}<span class="cx-name" data-eq>{title}</span>
          <span class="cx-count">{len(names)} uitvoeringen</span>{icon("ur")}</span>
      </a></li>'''


def catalog_block():
    cards = ''.join(_card(i, t, h, img) for i, (t, h, img) in enumerate(COMPONENTEN))
    dots = ''.join(f'<button type="button" class="cx-dot" tabindex="-1" data-cx-dot="{i}" aria-label="Naar {t}"><i></i></button>'
                   for i, (t, _h, _img) in enumerate(COMPONENTEN))
    return f'''<section class="section--home band--sage cx" aria-labelledby="comp-title" data-cx>
  <div class="container">
    <div class="cx-head">
      <h2 id="comp-title" class="h2" data-split>{split_lines("Het juiste component.<br><em>Op de juiste plek.</em>")}</h2>
      <p class="cx-hint" aria-hidden="true"><i class="cx-hint__scan"></i><span class="cx-hint__fine">Beweeg over een component en kijk erin</span><span class="cx-hint__touch">Swipe en kijk erin</span></p>
      {link("Alle componenten", "componenten.html")}
    </div>
    <ul class="cx-grid" data-cx-deck>{cards}</ul>
    <div class="cx-progress" aria-hidden="true"><span class="cx-progress__line"><span class="cx-progress__fill" data-cx-fill></span></span>{dots}</div>
  </div>
</section>
<script src="{_v("assets/js/home-blocks.js")}" defer></script>'''
