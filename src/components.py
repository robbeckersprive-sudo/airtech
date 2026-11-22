"""Shared component library for the Airtechnic "Flow" templates.

Every function returns an HTML string. Pages (see pages.py) only compose these.
"""
import json
import hashlib
import os
import random
import re
from functools import lru_cache
from html import escape

from contact_delivery import CONTACT_PATH, CONTACT_TOPICS, FIELD_LIMITS, RECIPIENT as EMAIL

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = json.load(open(os.path.join(ROOT, 'images', 'manifest.json'), encoding='utf-8'))

SITE = os.environ.get('SITE_URL', 'https://airtechnology.vercel.app').rstrip('/')
ORG = 'Airtechnic Solutions'
PHONE_DISPLAY = '+31 (0)85 0660 243'
PHONE_TEL = '+31850660243'
PRIVACY_URL = 'https://airtechnicsolutions.nl/airtechnicsolutions.nl/wp-content/uploads/2018/10/Privacyverklaring-klant-en-leveranciersadministratie.pdf'
ADDRESS = ('Scherpenbeemd 3', 'Beek en Donk')
MAPS_ROUTE = 'https://www.google.com/maps/dir/?api=1&amp;destination=Scherpenbeemd%203%2C%20Beek%20en%20Donk%2C%20Nederland'

PAGES = {
    'home': 'index.html',
    'artikel': 'kennis-druk-of-vacuumtransport.html',
    'categorie': 'componenten-cyclonen.html',
    'product': 'cycloonafscheider.html',
}

# ---------------------------------------------------------------- icons
_ICONS = {
    'ur': '<path d="M7 17 17 7M8.5 7H17v8.5"/>',
    'down': '<path d="M12 5v14M6.5 13.5 12 19l5.5-5.5"/>',
    'left': '<path d="M19 12H5M10.5 6.5 5 12l5.5 5.5"/>',
    'right': '<path d="M5 12h14M13.5 6.5 19 12l-5.5 5.5"/>',
    'chev-right': '<path d="m9.5 6 6 6-6 6"/>',
    'chev-down': '<path d="m6 9.5 6 6 6-6"/>',
    'check': '<path d="m4.5 12.5 5 5L19.5 7"/>',
    'phone': '<path d="M5.2 3.8h3.5l1.8 4.6-2.3 1.4a11 11 0 0 0 6 6l1.4-2.3 4.6 1.8v3.5a1.8 1.8 0 0 1-1.9 1.8A16.5 16.5 0 0 1 3.4 5.7a1.8 1.8 0 0 1 1.8-1.9z"/>',
    'mail': '<rect x="3" y="5.5" width="18" height="13" rx="1.5"/><path d="m3.5 7 8.5 6 8.5-6"/>',
    'pin': '<path d="M12 21s-6.5-5.9-6.5-11.2a6.5 6.5 0 0 1 13 0C18.5 15.1 12 21 12 21z"/><circle cx="12" cy="9.8" r="2.3"/>',
    'search': '<circle cx="10.8" cy="10.8" r="6.3"/><path d="m15.5 15.5 4.5 4.5"/>',
    'zoom': '<circle cx="10.8" cy="10.8" r="6.3"/><path d="m15.5 15.5 4.5 4.5M10.8 8v5.6M8 10.8h5.6"/>',
    'share': '<circle cx="6.5" cy="12" r="2.3"/><circle cx="17.5" cy="6" r="2.3"/><circle cx="17.5" cy="18" r="2.3"/><path d="m8.6 10.9 6.8-3.7M8.6 13.1l6.8 3.7"/>',
    'pause': '<path d="M9 6.5v11M15 6.5v11" stroke-width="2.2"/>',
    'close': '<path d="M6 6l12 12M18 6 6 18"/>',
    'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
    'alert': '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.8v5.2M12 16.2v.2"/>',
}
_FILLED = {
    'play': '<path d="M8 5.5v13l10.5-6.5z"/>',
    'linkedin': '<path d="M4.5 3h15A1.5 1.5 0 0 1 21 4.5v15a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 3 19.5v-15A1.5 1.5 0 0 1 4.5 3zm2.1 6.8V18h2.6V9.8zM7.9 5.6a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3zM10.8 9.8V18h2.6v-4.3c0-1.2.4-2.2 1.7-2.2s1.5 1.1 1.5 2.3V18h2.6v-4.8c0-2.4-.7-3.6-2.9-3.6-1.3 0-2.2.6-2.8 1.5V9.8z"/>',
}


def icon(name, cls='', attrs=''):
    extra = f' {cls}' if cls else ''
    if name in _FILLED:
        return f'<svg class="i i--fill i--{name}{extra}" viewBox="0 0 24 24" aria-hidden="true" focusable="false"{attrs}>{_FILLED[name]}</svg>'
    return f'<svg class="i i--{name}{extra}" viewBox="0 0 24 24" aria-hidden="true" focusable="false"{attrs}>{_ICONS[name]}</svg>'


LOGO_MARK = ('<svg viewBox="0 0 30 34" aria-hidden="true" focusable="false">'
             '<path fill="#D21F26" d="M2.5 33.5C9.8 27.6 16.4 16.5 21.3.5h7.2C24 17.8 15 29.4 5.4 33.9z"/></svg>')


def logo(href='index.html'):
    return (f'<a class="logo logo--airtechnic" href="{href}" aria-label="{ORG}, naar de homepage">'
            '<span class="logo__art" aria-hidden="true">'
            '<img src="assets/img/airtechnic-logo-320.webp" srcset="assets/img/airtechnic-logo-320.webp 320w, assets/img/airtechnic-logo-640.webp 640w" sizes="(max-width: 719px) 180px, 240px" width="2176" height="722" alt="" decoding="async">'
            '</span><svg class="logo__flow" viewBox="0 0 180 8" fill="none" aria-hidden="true" focusable="false">'
            '<path pathLength="100" d="M1 6H110C133 6 146 2 179 2"/>'
            '</svg></a>')


def tbd(label='TBD'):
    return f'<span class="tbd">[{label}]</span>'


# ---------------------------------------------------------------- media
def pic(name, alt='', sizes='100vw', eager=False, img_cls='', style=''):
    """Responsive <picture> with AVIF + WebP, explicit dimensions, lazy by default."""
    m = MANIFEST[name]
    ws = m['widths']

    def srcset(ext):
        return ', '.join(f'images/{name}-{w}.{ext} {w}w' for w in ws)

    fallback = next((w for w in ws if w >= 800), ws[-1])
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    cls = f' class="{img_cls}"' if img_cls else ''
    st = f' style="{style}"' if style else ''
    return (f'<picture><source type="image/avif" srcset="{srcset("avif")}" sizes="{sizes}">'
            f'<source type="image/webp" srcset="{srcset("webp")}" sizes="{sizes}">'
            f'<img src="images/{name}-{fallback}.webp" width="{m["w"]}" height="{m["h"]}" alt="{escape(alt)}" {load} decoding="async"{cls}{st}></picture>')


def preload(name, sizes='100vw'):
    m = MANIFEST[name]
    ss = ', '.join(f'images/{name}-{w}.avif {w}w' for w in m['widths'])
    return f'<link rel="preload" as="image" type="image/avif" imagesrcset="{ss}" imagesizes="{sizes}" fetchpriority="high">'


def media(name, alt='', ratio='ar-16-10', contain=False, sizes='(min-width: 960px) 33vw, 100vw', style='', extra_cls=''):
    cls = 'media' + (' media--contain' if contain else '') + (f' {ratio}' if ratio else '') + (f' {extra_cls}' if extra_cls else '')
    return f'<div class="{cls}">{pic(name, alt, sizes, style=style)}</div>'


# ---------------------------------------------------------------- links & buttons
def btn_icon(name='ur'):
    """Two stacked arrows: on hover the first exits, the second slides in (direction-aware)."""
    return f'<span class="btn__icon" aria-hidden="true">{icon(name)}{icon(name, "btn__icon-2")}</span>'


def btn(text, href, size='', cls='', icon_name='ur'):
    s = f' btn--{size}' if size else ''
    c = f' {cls}' if cls else ''
    return f'<a class="btn{s}{c}" href="{href}" data-magnetic><span class="btn__label">{text}</span>{btn_icon(icon_name)}</a>'


def link(text, href, arrow='ur', cls='', extra='', attrs=''):
    c = f' {cls}' if cls else ''
    return f'<a class="link{c}" href="{href}"{attrs}>{text}{extra}{icon(arrow)}</a>'


# ---------------------------------------------------------------- headings
# Discretionary breaks follow Dutch compound boundaries and only appear when needed.
_HEADING_COMPOUNDS = {
    "acceptatiecriteria": "acceptatie|criteria",
    "buiskoppeling": "buis|koppeling",
    "doorblaassluis": "doorblaas|sluis",
    "doseersluizen": "doseer|sluizen",
    "doseerstation": "doseer|station",
    "druktransport": "druk|transport",
    "filterelement": "filter|element",
    "filterselectie": "filter|selectie",
    "filtersysteem": "filter|systeem",
    "fractioneerzeef": "fractioneer|zeef",
    "leidingwissel": "leiding|wissel",
    "luchttechniek": "lucht|techniek",
    "manchetafsluiter": "manchet|afsluiter",
    "ontluchtingsfilter": "ontluchtings|filter",
    "patroonfilter": "patroon|filter",
    "procesanalyse": "proces|analyse",
    "productieproces": "productie|proces",
    "scheidingstechnieken": "scheidings|technieken",
    "schuifafsluiter": "schuif|afsluiter",
    "selectievragen": "selectie|vragen",
    "slijtagebeeld": "slijtage|beeld",
    "stofafzuiging": "stof|afzuiging",
    "transportbocht": "transport|bocht",
    "transportleiding": "transport|leiding",
    "transportlijn": "transport|lijn",
    "ventilatorunit": "ventilator|unit",
    "voorafscheider": "voor|afscheider",
    "werkingsprincipe": "werkings|principe",
    "zijkanaalblower": "zijkanaal|blower",
    "luchtstroom": "lucht|stroom",
    "proceslucht": "proces|lucht",
    "projectaanpak": "project|aanpak",
    "centrifugaalventilator": "centrifugaal|ventilator",
    "cycloonafscheider": "cycloon|afscheider",
    "transportafscheider": "transport|afscheider",
    "draaizuigerblower": "draai|zuiger|blower",
    "vacuümtransport": "vacuüm|transport",
    "productstroom": "product|stroom",
    "procesinstallatie": "proces|installatie",
    "inbedrijfstelling": "inbedrijf|stelling",
}
_HEADING_WORD = re.compile("|".join(_HEADING_COMPOUNDS), re.IGNORECASE)


def heading_breaks(match):
    def compound(word):
        text = word.group()
        chunks = _HEADING_COMPOUNDS[text.lower()].split("|")
        start = 0
        parts = []
        for chunk in chunks:
            parts.append(text[start:start + len(chunk)])
            start += len(chunk)
        return "&shy;".join(parts)

    # Preserve markup, including ids and links, inside headings.
    return "".join(part if part.startswith("<") else _HEADING_WORD.sub(compound, part)
                   for part in re.split(r"(<[^>]+>)", match.group()))


def split_lines(html):
    """Wrap each <br>-separated line in a mask so it can slide up on reveal (no JS needed for layout)."""
    parts = re.split(r'<br\s*/?>', html)
    return ' '.join(f'<span class="ln"><span class="ln__in" style="--ln:{i}">{p}</span></span>' for i, p in enumerate(parts))


def eyebrow(text, aside=None, tag='p'):
    # Staal & Signaal: labels above headings are retired; the heading carries itself.
    return ''
    a = f' <span class="eyebrow__aside">{aside}</span>' if aside else ''
    return f'<{tag} class="eyebrow">{text}{a}</{tag}>'


def section_head(title, hid, eyebrow_text=None, sub=None, level=2, plain=False):
    e = eyebrow(eyebrow_text) if eyebrow_text else ''
    s = f'<p class="sub">{sub}</p>' if sub else ''
    p = ' h2--plain' if plain else ''
    return f'<div class="section-head">{e}<h{level} id="{hid}" class="h2{p}" data-split>{split_lines(title)}</h{level}>{s}</div>'


# ---------------------------------------------------------------- navigation data
OPLOSSINGEN = [
    ('Industriële luchttechniek', [('Stofafzuiging', 'oplossingen-stofafzuiging.html'), ('Filtratie', 'oplossingen-filtratie.html'), ('Hoogvacuüm', 'oplossingen-hoogvacuum.html')]),
    ('Solids processing', [('Pneumatisch transport', 'oplossingen-pneumatisch-transport.html'), ('Doseren', 'oplossingen-doseren.html'), ('Zeven en scheiden', 'oplossingen-zeven-en-scheiden.html'), ('Opslaan', 'oplossingen-opslaan.html')]),
]
COMPONENTEN = [
    ('Blowers &amp; ventilatoren', 'componenten-blowers-ventilatoren.html', '03-blower-vrijstaand'),
    ('Cyclonen', PAGES['categorie'], '04-cycloon-vrijstaand'),
    ('Filters', 'componenten-filters.html', '05-filter-vrijstaand'),
    ('Doseersluizen', 'componenten-doseersluizen.html', '06-doseersluis-vrijstaand'),
    ('Leidingwerk &amp; koppelingen', 'componenten-leidingwerk-koppelingen.html', '07-leidingwerk-vrijstaand'),
    ('Big-bag stations', 'componenten-bigbag-stations.html', '08-bigbag-vrijstaand'),
    ('Afsluiters', 'componenten-afsluiters.html', '09-afsluiter-vrijstaand'),
    ('Zeven', 'componenten-zeven.html', '10-zeef-vrijstaand'),
]


# Header "Doorsnede" (concept B, rolled out 2026-11-20): a contact rail that scrolls away, a sticky bar with a ruler
# (scroll gauge + hover marker) and full-width drawers that swap a figure per item. Mobile: sheet with <details name>.
SOL_IMG = {
    'Stofafzuiging': '26-multicycloon',
    'Filtratie': '05-filter-vrijstaand',
    'Hoogvacuüm': '03-blower-vrijstaand',
    'Pneumatisch transport': '07-leidingwerk-vrijstaand',
    'Doseren': '15-doseersluis-doorsnede',
    'Zeven en scheiden': '10-zeef-vrijstaand',
    'Opslaan': '08-bigbag-vrijstaand',
}
SOLUTIONS_HREF = PAGES['home'] + '#specialisaties'


def _slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower().replace('&amp;', 'en').replace('ü', 'u')).strip('-')


def _header_sheet(current=None):
    """Mobile menu "Tekenblad" (mobile.css / mobile.js): a full-screen steel sheet that is drawn down behind a red scan
    line. Numbered index; Oplossingen and Componenten drill in to their own pane (photo plates), contact in thumb reach.
    The id / data-hx-sheet hooks are the ones the header always used."""
    comp_names = {t for t, _h, _i in COMPONENTEN}
    cur_attr = lambda on: ' aria-current="page"' if on else ''
    opl = ''.join(
        f'<div class="mnav__group"><p class="mnav__group-t">{group}</p><ul>'
        + ''.join(f'<li><a class="mnav__row" href="{href}"><span class="mnav__thumb">{pic(SOL_IMG[label], "", "64px")}</span>'
                  f'<span>{label}</span>{icon("ur")}</a></li>' for label, href in items)
        + '</ul></div>' for group, items in OPLOSSINGEN)
    tiles = ''.join(f'<li style="--i:{i}"><a class="mnav__tile" href="{h}"{cur_attr(t == current)}>'
                    f'<span class="mnav__tile-img">{pic(img, "", "45vw")}</span><span class="mnav__tile-t">{t}</span></a></li>'
                    for i, (t, h, img) in enumerate(COMPONENTEN))
    root = [
        ('button', 'opl', 'Oplossingen', False),
        ('button', 'comp', 'Componenten', current in comp_names),
        ('projecten.html', None, 'Projecten', current == 'Projecten'),
        ('index.html#steps-title', None, 'Werkwijze', False),
        ('over-ons.html', None, 'Over ons', current == 'Over ons'),
        ('kennisbank.html', None, 'Kennisbank', current == 'Kennisbank'),
    ]
    items = []
    for i, (kind, key, label, on) in enumerate(root):
        inner = (f'<span class="mnav__no">{i + 1:02d}</span><span class="mnav__label"><span>{label}</span></span>'
                 f'{icon("chev-right" if kind == "button" else "ur")}')
        dot = ' is-current' if on else ''
        if kind == 'button':
            items.append(f'<li style="--i:{i}"><button class="mnav__item{dot}" type="button" data-mnav-open="{key}" '
                         f'aria-expanded="false" aria-controls="mnav-{key}">{inner}</button></li>')
        else:
            items.append(f'<li style="--i:{i}"><a class="mnav__item{dot}" href="{kind}"{cur_attr(on)}>{inner}</a></li>')
    back = f'<button class="mnav__back" type="button" data-mnav-back>{icon("left")}<span>Menu</span></button>'
    return f'''<div class="mnav" id="hx-sheet" data-hx-sheet data-theme="steel" role="dialog" aria-modal="true" aria-label="Menu" hidden>
    <i class="mnav__scan" aria-hidden="true"></i>
    <div class="mnav__body">
      <nav class="mnav__panes" aria-label="Mobiele navigatie">
        <div class="mnav__pane mnav__pane--root" data-mnav-pane="root">
          <ol class="mnav__list">{"".join(items)}</ol>
        </div>
        <div class="mnav__pane mnav__pane--sub" id="mnav-opl" data-mnav-pane="opl" hidden>
          {back}<p class="mnav__kicker"><span>01</span>Oplossingen</p>
          {opl}
          <a class="mnav__all" href="{SOLUTIONS_HREF}">Verken onze oplossingen{icon("ur")}</a>
        </div>
        <div class="mnav__pane mnav__pane--sub" id="mnav-comp" data-mnav-pane="comp" hidden>
          {back}<p class="mnav__kicker"><span>02</span>Componenten</p>
          <ul class="mnav__tiles">{tiles}</ul>
          <a class="mnav__all" href="componenten.html">Alle componenten{icon("ur")}</a>
        </div>
      </nav>
    </div>
    <div class="mnav__foot">
      <a class="btn btn--block mnav__cta" href="index.html#contact"><span class="btn__label">Bespreek uw vraagstuk</span>{btn_icon()}</a>
      <div class="mnav__quick">
        <a href="tel:{PHONE_TEL}">{icon("phone")}<span>Bel ons</span></a>
        <a href="mailto:{EMAIL}">{icon("mail")}<span>Mail ons</span></a>
      </div>
      <a class="mnav__location" href="https://www.google.com/maps/dir/?api=1&amp;destination=Scherpenbeemd%203%2C%20Beek%20en%20Donk%2C%20Nederland" target="_blank" rel="noopener noreferrer" aria-label="Route naar Airtechnic, Scherpenbeemd 3, Beek en Donk in Google Maps">{icon("pin")}<span class="mnav__location-address">{ADDRESS[0]}<span>{ADDRESS[1]}</span></span><span class="mnav__location-action">Route{icon("ur")}</span></a>
    </div>
  </div>'''


def header(overlay=False, current=None):
    """current: label of the active component group (e.g. 'Cyclonen') to mark in the Componenten drawer."""
    first = OPLOSSINGEN[0][1][0][0]
    groups = ''.join(
        f'<div class="hxb-group"><p class="hxb-group__t">{t}</p><ul>'
        + ''.join(f'<li><a href="{h}" data-fig="{_slug(n)}"><span>{n}</span>{icon("ur")}</a></li>' for n, h in items)
        + '</ul></div>' for t, items in OPLOSSINGEN)
    figs = ''.join(f'<div class="hxb-fig__img hxb-fig__img--cut{" is-on" if n == first else ""}" data-fig-img="{_slug(n)}" data-cap="{n}" data-grp="{g}">'
                   f'{pic(SOL_IMG[n], "", "(min-width: 1040px) 40vw, 1px")}</div>'
                   for g, items in OPLOSSINGEN for n, _h in items)
    marks = ''.join(f'<i class="hxb-reg hxb-reg--{c}"></i>' for c in ('tl', 'tr', 'bl', 'br'))
    clist = ''.join(f'<li><a href="{h}" data-fig="{_slug(t)}"{" aria-current=page" if t == current else ""}>'
                    f'<span class="hxb-thumb">{pic(img, "", "56px")}</span><span>{t}</span>{icon("ur")}</a></li>'
                    for t, h, img in COMPONENTEN)
    cfigs = ''.join(f'<div class="hxb-fig__img hxb-fig__img--cut{" is-on" if i == 0 else ""}" data-fig-img="{_slug(t)}" '
                    f'data-cap="{t}" data-grp="Componenten">{pic(img, "", "(min-width: 1040px) 30vw, 1px")}</div>'
                    for i, (t, _h, img) in enumerate(COMPONENTEN))
    comp_on = ' is-current' if current in {item[0] for item in COMPONENTEN} else ''
    ov = ' hx--overlay' if overlay else ''
    return f'''<header class="hx hx--b{ov}" data-site-header>
  <div class="hxb-rail">
    <div class="container hxb-rail__in">
      <nav class="hxb-rail__links" aria-label="Service"><a href="kennisbank.html">Kennisbank</a><a href="index.html#contact">Contact</a></nav>
      <ul>
        <li><a href="{MAPS_ROUTE}" target="_blank" rel="noopener noreferrer" aria-label="{ADDRESS[0]}, {ADDRESS[1]}: route naar Airtechnic in Google Maps">{icon("pin")}<span>{ADDRESS[0]}, {ADDRESS[1]}</span></a></li>
        <li><a href="tel:{PHONE_TEL}">{icon("phone")}<span>{PHONE_DISPLAY}</span></a></li>
        <li><a href="mailto:{EMAIL}">{icon("mail")}<span>{EMAIL}</span></a></li>
      </ul>
    </div>
  </div>
  <div class="hxb-bar">
    <div class="container hxb-bar__in">
      {logo()}
      <nav class="hxb-nav" aria-label="Hoofdnavigatie">
        <ul>
          <li><button class="hxb-link" type="button" data-hx-tab="opl" aria-expanded="false" aria-controls="hxb-opl">Oplossingen{icon("chev-down")}</button></li>
          <li><button class="hxb-link{comp_on}" type="button" data-hx-tab="comp" aria-expanded="false" aria-controls="hxb-comp">Componenten{icon("chev-down")}</button></li>
          <li><a class="hxb-link{' is-current' if current == 'Projecten' else ''}" href="projecten.html"{' aria-current="true"' if current == 'Projecten' else ''}>Projecten</a></li>
          <li><a class="hxb-link" href="index.html#steps-title">Werkwijze</a></li>
          <li><a class="hxb-link{' is-current' if current == 'Over ons' else ''}" href="over-ons.html"{' aria-current="page"' if current == 'Over ons' else ''}>Over ons</a></li>
        </ul>
      </nav>
      <a class="btn btn--sm hxb-cta" href="index.html#contact" data-magnetic><span class="btn__label">Bespreek uw vraagstuk</span>{btn_icon()}</a>
      <button class="hx-burger" type="button" data-hx-burger aria-expanded="false" aria-controls="hx-sheet" aria-label="Menu openen"><span></span><span></span></button>
    </div>
    <div class="hxb-ruler" aria-hidden="true"><span class="hxb-ruler__progress" data-scroll-progress></span><span class="hxb-ruler__marker"></span></div>
  </div>
  <div class="hxb-drawer" id="hxb-opl" data-hx-panel="opl" role="region" aria-label="Oplossingen" inert>
    <div class="container hxb-drawer__in">
      <div class="hxb-drawer__nav">{groups}
        <a class="link hxb-drawer__all" href="{SOLUTIONS_HREF}">Verken onze oplossingen{icon("ur")}</a>
      </div>
      <figure class="hxb-fig hxb-fig--cut" data-fig-frame>{figs}{marks}
        <figcaption><span data-fig-cap>{first}</span><span data-fig-grp>{OPLOSSINGEN[0][0]}</span></figcaption>
      </figure>
    </div>
  </div>
  <div class="hxb-drawer" id="hxb-comp" data-hx-panel="comp" role="region" aria-label="Componenten" inert>
    <div class="container hxb-drawer__in hxb-drawer__in--comp">
      <div class="hxb-drawer__nav"><ul class="hxb-clist">{clist}</ul>
        <a class="link hxb-drawer__all" href="componenten.html">Alle componenten{icon("ur")}</a>
      </div>
      <figure class="hxb-fig hxb-fig--cut" data-fig-frame>{cfigs}{marks}
        <figcaption><span data-fig-cap>{COMPONENTEN[0][0]}</span><span data-fig-grp>Componenten</span></figcaption>
      </figure>
    </div>
  </div>
  {_header_sheet(current)}
</header>'''


def breadcrumb(items):
    """items: list of (label, href); last item is the current page."""
    lis = []
    for i, (label, href) in enumerate(items):
        if i == len(items) - 1:
            lis.append(f'<li aria-current="page">{label}</li>')
        else:
            lis.append(f'<li><a href="{href}">{label}</a></li>')
    return f'<nav aria-label="Kruimelpad"><ol class="breadcrumb">{"".join(lis)}</ol></nav>'


def breadcrumb_jsonld(items, current_url):
    els = []
    for i, (label, href) in enumerate(items):
        url = current_url if i == len(items) - 1 else (SITE + '/' + (href if href not in ('#', 'index.html') else ''))
        els.append({'@type': 'ListItem', 'position': i + 1, 'name': label.replace('&amp;', '&'), 'item': url})
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': els}


# ---------------------------------------------------------------- cards & tiles
def card(title, link_text, href, img, alt='', ratio='ar-4-3', contain=False, text=None, title_cls='card__title h3',
         sizes='(min-width: 960px) 30vw, (min-width: 640px) 50vw, 100vw', style='', attrs='', tag='h3'):
    t = f'<p class="card__text">{text}</p>' if text else ''
    hidden_ctx = f'<span class="visually-hidden">: {title}</span>'
    return (f'<article class="card" data-spotlight{attrs}>{media(img, alt, ratio, contain, sizes, style)}'
            f'<{tag} class="{title_cls}">{title}</{tag}>{t}'
            f'{link(link_text, href, extra=hidden_ctx, cls="card__link")}</article>')


def product_tile(label, href, img, active=False):
    a = ' is-active' if active else ''
    return (f'<a class="product-tile{a}" href="{href}" data-spotlight><span class="product-tile__img">'
            f'{pic(img, "", "(min-width: 960px) 22vw, (min-width: 640px) 45vw, 70vw")}</span>'
            f'<span class="product-tile__label">{label}</span><span class="product-tile__go" aria-hidden="true">{icon("ur")}</span></a>')


def checklist(items):
    return '<ul class="checklist">' + ''.join(f'<li>{icon("check")}<span>{i}</span></li>' for i in items) + '</ul>'


# ---------------------------------------------------------------- FAQ
def faq(items, open_first=False):
    out = []
    for i, (q, a) in enumerate(items):
        o = ' open' if (open_first and i == 0) else ''
        body = f'<p>{a}</p>' if a else f'<p>{tbd()}</p>'
        out.append(f'<details class="faq__item"{o}><summary><span>{q}</span><span class="faq__icon" aria-hidden="true"></span></summary>'
                   f'<div class="faq__answer">{body}</div></details>')
    return f'<div class="faq">{"".join(out)}</div>'


def faq_jsonld(items):
    answered = [(q, a) for q, a in items if a]
    if not answered:
        return None  # nothing publishable yet: all answers are [TBD]
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in answered]}


def faq_section(title, items, hid, open_first=False):
    return f'''<section class="section" aria-labelledby="{hid}" data-reveal>
  <div class="container">
    {section_head(title, hid)}
    {faq(items, open_first)}
  </div>
</section>'''


# ---------------------------------------------------------------- contact block
def _field(name, label, kind='text', required=False, autocomplete=None, textarea=False, hint=None):
    fid = f'f-{name}'
    req = ' <span class="req" aria-hidden="true">*</span>' if required else ''
    ac = f' autocomplete="{autocomplete}"' if autocomplete else ''
    r = (' required' if required else '') + f' maxlength="{FIELD_LIMITS[name]}"'
    descriptions = ([f'{fid}-hint'] if hint else []) + ([f'{fid}-err'] if required else [])
    desc = f' aria-describedby="{" ".join(descriptions)}"' if descriptions else ''
    help_text = f'<p class="field__hint" id="{fid}-hint" data-contact-hint aria-live="polite">{escape(hint)}</p>' if hint else ''
    ctrl = (f'<textarea id="{fid}" name="{name}" rows="4"{r}{desc}></textarea>' if textarea else
            f'<input id="{fid}" name="{name}" type="{kind}"{ac}{r}{desc}>')
    err = (f'<p class="field__error" id="{fid}-err" hidden>{icon("alert")}<span data-msg></span></p>' if required else '')
    dv = ' data-validate' if required else ''
    return f'<div class="field"{dv}><label for="{fid}">{label}{req}</label>{help_text}{ctrl}{err}</div>'


def contact_url(topic):
    return f'?aanvraag={topic}#contact'


def contact(title, intro, deco=False, topic='algemeen', topics=()):
    """Contact block (Nov 21 restyle, styles in top.css "CONTACT", behaviour assets/js/contact-plus.js).
    The real form logic stays in site.js: it needs #contact, .contact__lines a[href^=mailto], [data-contact-topic]
    (the <select>, still the source of truth) and the [data-validate] fields. The topic chips only drive the select;
    the progress line (Vraag, Naam, E-mail) shows which required field is still open."""
    naam = _field('naam', 'Naam', required=True, autocomplete='name')
    mail = _field('email', 'E-mailadres', 'email', True, 'email')
    bedrijf = _field('bedrijf', 'Bedrijf (optioneel)', autocomplete='organization')
    telefoon = _field('telefoon', 'Telefoon (optioneel)', 'tel', autocomplete='tel')
    vraag = _field('vraagstuk', 'Uw bericht', required=True, textarea=True, hint=CONTACT_TOPICS[topic][1])
    # at most two page-specific topics, then the same four intent shortcuts on every page, 'Algemene vraag' last
    intents = ('installatieontwerp', 'bestaande-installatie', 'onderdelen', 'terugbellen')
    own = [k for k in dict.fromkeys((topic, *topics)) if k != 'algemeen'][:2]
    keys = list(dict.fromkeys((*own, *intents))) + ['algemeen']
    options = ''.join(
        f'<option value="{key}" data-hint="{escape(CONTACT_TOPICS[key][1])}"'
        f'{" selected" if key == topic else ""}>{escape(CONTACT_TOPICS[key][0])}</option>' for key in keys)
    chips = ''.join(
        f'<button type="button" class="ct-chip" role="radio" aria-checked="{str(key == topic).lower()}" tabindex="{0 if key == topic else -1}" '
        f'data-ct-topic="{key}">{escape(CONTACT_TOPICS[key][0].split(" · ")[-1])}</button>' for key in keys)
    deco_html = (f'<div class="contact__deco" aria-hidden="true">{pic("02-pijpleiding-contact", "", "45vw")}</div>' if deco else '')
    tips = ('Welk product u verwerkt', 'De gewenste capaciteit', 'Afstand en hoogteverschil van het transport',
            'Foto&rsquo;s of tekeningen van de huidige situatie')
    helpers = ''.join(f'<button type="button" class="ct-helper" data-ct-add="{t}: ">+ {t}</button>'
                      for t in ('Product', 'Capaciteit', 'Afstand', 'Huidige situatie'))
    tip_items = ''.join(f'<li>{icon("check")}<span>{t}</span></li>' for t in tips)
    steps = ''.join(f'<li data-ct-step="{k}"><i></i><span>{t}</span></li>' for k, t in (('vraagstuk', 'Vraag'), ('naam', 'Naam'), ('email', 'E-mail')))
    deco_cls = ' contact--deco' if deco else ''
    return f'''<section data-theme="forest" class="contact ct{deco_cls}" id="contact" aria-labelledby="contact-title" data-reveal>
  <div class="ct-grid-bg" aria-hidden="true"></div>
  {deco_html}
  <div class="container ct-in">
    <div class="ct-intro">
      <p class="ct-kicker"><span class="ct-kicker__dot" aria-hidden="true"></span>Contact</p>
      <h2 id="contact-title" class="h2" data-split>{split_lines(title)}</h2>
      <p class="ct-lead">{intro}</p>
      <div class="ct-tips"><p class="ct-tips__t">Handig om te noemen</p><ul>{tip_items}</ul></div>
      <ul class="contact__lines ct-lines">
        <li><a href="tel:{PHONE_TEL}"><span class="ct-lines__ico">{icon("phone")}</span><span class="ct-lines__txt"><small>Bellen</small>{PHONE_DISPLAY}</span>{icon("ur")}</a></li>
        <li><a href="mailto:{EMAIL}"><span class="ct-lines__ico">{icon("mail")}</span><span class="ct-lines__txt"><small>Mailen</small><span class="ct-lines__value">{escape(EMAIL).replace('@', '@<wbr>')}</span></span>{icon("ur")}</a></li>
      </ul>
      <a class="ct-addr address-route" href="{MAPS_ROUTE}" target="_blank" rel="noopener noreferrer" aria-label="{ADDRESS[0]}, {ADDRESS[1]}: route naar Airtechnic in Google Maps">{icon("pin")}<span>{ADDRESS[0]}, {ADDRESS[1]}</span>{icon("ur")}</a>
    </div>
    <div class="ct-card-wrap">
      <div class="contact__card ct-card" data-theme="light">
        <ol class="ct-progress" aria-hidden="true" data-ct-progress><span class="ct-progress__line"><b data-ct-fill></b></span>{steps}</ol>
        <form class="form" action="{CONTACT_PATH}" method="post" novalidate data-form aria-labelledby="contact-form-title">
          <div class="form__heading">
            <h3 class="h3" id="contact-form-title" tabindex="-1">Stel uw vraag</h3>
            <p class="form__note">Velden met * zijn verplicht.</p>
          </div>
          <div class="field ct-topic">
            <label for="f-onderwerp" id="f-onderwerp-label">Onderwerp</label>
            <div class="ct-chips" role="radiogroup" aria-labelledby="f-onderwerp-label" data-ct-chips hidden>{chips}</div>
            <select id="f-onderwerp" name="onderwerp" data-contact-topic>{options}</select>
          </div>
          {vraag}
          <div class="ct-helpers" data-ct-helpers hidden><span class="ct-helpers__t">Snel aanvullen</span>{helpers}</div>
          <div class="form__row form__row--2">{naam}{mail}</div>
          <div class="form__row form__row--2">{bedrijf}{telefoon}</div>
          <div class="form__actions ct-actions">
            <button class="btn btn--lg" type="submit" disabled><span class="btn__label">Verstuur uw aanvraag</span>{btn_icon()}</button>
            <p class="form__privacy"><span class="ct-reassure">{icon("check")}Vrijblijvend</span><a href="{PRIVACY_URL}">Privacyverklaring</a></p>
          </div>
          <p class="form__feedback" role="status" tabindex="-1" data-contact-feedback></p>
          <noscript><p class="form__note">Mail rechtstreeks naar <a href="mailto:{EMAIL}">{EMAIL}</a> of bel ons.</p></noscript>
        </form>
      </div>
    </div>
  </div>
</section>
<script src="{_v("assets/js/contact-plus.js")}" defer></script>'''


# ---------------------------------------------------------------- footer
def _sheet_name(title):
    """Page name for the footer title block: the <title> before ' | ', tags and entities resolved."""
    from html import unescape
    return escape(unescape(re.sub(r'<[^>]+>', '', title)).split(' | ')[0])


def footer(variant="stone", sheet=''):
    """Footer "Titelblok" (Nov 21, styles in top.css "FOOTER"): the site's drawing sheet ends in a title block, a
    framed grid of cells (brand, motto, links, contact) with the current page as "Blad". `variant` kept for callers."""
    sheet = sheet or 'Airtechnic Solutions'
    tech = ('<nav aria-label="Techniek"><h2 class="ft-h">Techniek</h2>'
            '<a href="index.html#specialisaties">Onze specialisaties</a><a href="componenten.html">Componenten</a>'
            f'<a href="{PAGES["categorie"]}">Cyclonen &amp; afscheiders</a><a href="kennisbank.html">Kennisbank</a></nav>')
    org = ('<nav aria-label="Airtechnic"><h2 class="ft-h">Airtechnic</h2>'
           '<a href="over-ons.html">Over ons</a><a href="index.html#steps-title">Onze werkwijze</a>'
           '<a href="projecten.html">Projecten</a><a href="index.html#contact">Stel uw vraag</a></nav>')
    direct = (f'<div><h2 class="ft-h">Direct contact</h2><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>'
              f'<a href="mailto:{EMAIL}">{EMAIL}</a><address><a class="address-route" href="{MAPS_ROUTE}" target="_blank" rel="noopener noreferrer" aria-label="{ADDRESS[0]}, 5741 TX {ADDRESS[1]}: route naar Airtechnic in Google Maps"><span>{ADDRESS[0]}<br>5741 TX {ADDRESS[1]}</span>{icon("ur")}</a></address></div>')
    return f'''<footer class="af ft af--{variant}" id="footer">
  <div class="container">
    <div class="ft-block">
      <div class="ft-cell ft-cell--brand">{logo()}<p class="ft-k ft-k--mute">Industriële luchttechniek &amp; solids processing</p></div>
      <div class="ft-cell ft-cell--motto"><p class="ft-motto">Grip op <em>elke stroom.</em></p></div>
      <div class="ft-cell"><p class="ft-k">01</p>{tech}</div>
      <div class="ft-cell"><p class="ft-k">02</p>{org}</div>
      <div class="ft-cell ft-cell--contact"><p class="ft-k">03</p>{direct}</div>
      <div class="ft-cell ft-cell--sheet">
        <dl class="ft-meta"><div><dt>Blad</dt><dd>{sheet}</dd></div><div><dt>Schaal</dt><dd>1 : 1</dd></div><div><dt>Rev.</dt><dd>2026</dd></div></dl>
        <a class="ft-top" href="#main">{icon("ur")}<span>Naar boven</span></a>
      </div>
    </div>
    <div class="ft-base"><span>&copy; Airtechnic Solutions BV</span>
      <span class="ft-base__links"><a href="{PRIVACY_URL}">Privacyverklaring</a><a href="https://nl.linkedin.com/company/airtechnic-solutions">LinkedIn {icon("ur")}</a></span>
    </div>
  </div>
</footer>'''


# ---------------------------------------------------------------- page shell
FAVICON = 'assets/img/favicon.svg'
@lru_cache(maxsize=None)
def _v(rel):
    """Stable content version: builds do not depend on checkout timestamps."""
    with open(os.path.join(ROOT, rel), 'rb') as asset:
        version = hashlib.sha256(asset.read()).hexdigest()[:12]
    return f'{rel}?v={version}'


# Site signature "Hartlijn" (signature.js): short station labels per section heading id
SIG_LABELS = {
    'spec-title': 'Specialisaties', 'comp-title': 'Componenten', 'steps-title': 'Werkwijze', 'kennis-title': 'Kennis',
    'faq-title': 'Vragen', 'contact-title': 'Contact', 'werking-title': 'Werking', 'uitv-title': 'Uitvoering',
    'toep-title': 'Toepassingen', 'relc-title': 'Verwant', 'advies-title': 'Advies', 'principe-title': 'Principe',
    'rel-title': 'Verwant', 'meer-title': 'Verder lezen', 'vergelijking': 'Vergelijking', 'cat-grid-title': 'Overzicht',
}


def sig_labels(body):
    for k, lab in SIG_LABELS.items():
        body = body.replace(f'aria-labelledby="{k}"', f'aria-labelledby="{k}" data-sig-label="{lab}"', 1)
    return body


def page(filename, title, description, og_image, body, jsonld=(), overlay=False, preload_img=None, html_cls='', footer_variant="stone", nav_current=None, preview=False, stylesheet=None):
    url = SITE + '/' + ('' if filename == 'index.html' else filename)
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(d, ensure_ascii=False)}</script>\n' for d in jsonld if d)
    hc = f' class="{html_cls}"' if html_cls else ''
    pre = preload(*preload_img) if preload_img else ''
    robots = '<meta name="robots" content="noindex">\n' if preview else ''
    extra_style = f'<link rel="stylesheet" href="{_v(stylesheet)}">\n' if stylesheet else ''
    body = re.sub(r"<h([1-6])\b[^>]*>.*?</h\1>", heading_breaks, sig_labels(body), flags=re.S)
    return f'''<!doctype html>
<html lang="nl" data-sig="a" data-sig-start="origin"{hc}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.classList.add('js')</script>
<title>{title}</title>
<meta name="description" content="{escape(description)}">
{robots}<link rel="canonical" href="{url}">
<meta name="theme-color" content="#F3F1EC">
<meta property="og:type" content="{'article' if filename.startswith('kennis-') else 'website'}">
<meta property="og:site_name" content="{ORG}">
<meta property="og:locale" content="nl_NL">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/images/{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{FAVICON}" type="image/svg+xml">
<link rel="preload" as="font" type="font/woff2" href="assets/fonts/archivo-normal-site.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="assets/fonts/archivo-italic-300-112-site.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="assets/fonts/archivo-italic-300-100-site.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="assets/fonts/ibm-plex-mono-normal-400-latin.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="assets/fonts/ibm-plex-mono-normal-500-latin.woff2" crossorigin>
<link rel="stylesheet" href="{_v('assets/css/fonts.css')}">
{pre}
<link rel="stylesheet" href="{_v('assets/css/tokens.css')}">
<link rel="stylesheet" href="{_v('assets/css/site.css')}">
<link rel="stylesheet" href="{_v('assets/css/signature.css')}">
<link rel="stylesheet" href="{_v('assets/css/airtechnic-footer.css')}">
<link rel="stylesheet" href="{_v('assets/css/top.css')}">
{extra_style}<link rel="stylesheet" href="{_v('assets/css/mobile.css')}">
<link rel="stylesheet" href="{_v('assets/css/brand.css')}">
<script src="{_v('assets/js/page-transitions.js')}"></script>
<script src="{_v('assets/js/site.js')}" defer></script>
<script src="{_v('assets/js/signature.js')}" defer></script>
<script src="{_v('assets/js/mobile.js')}" defer></script>
<script src="{_v('assets/js/equalize.js')}" defer></script>
{ld}</head>
<body>
<a class="skip-link" href="#main">Direct naar de inhoud</a>
{header(overlay, nav_current)}
<main id="main" tabindex="-1">
{body}
</main>
{footer(footer_variant, _sheet_name(title))}
</body>
</html>
'''


def org_jsonld():
    return {'@context': 'https://schema.org', '@type': 'Organization', 'name': ORG, 'url': SITE + '/',
            'logo': SITE + '/assets/img/airtechnic-logo-transparent.png', 'email': EMAIL, 'telephone': PHONE_TEL,
            'address': {'@type': 'PostalAddress', 'streetAddress': ADDRESS[0], 'addressLocality': ADDRESS[1], 'addressCountry': 'NL'}}


# ---------------------------------------------------------------- illustrations
def pipe_svg(kind):
    """Inline illustration for the druk/vacuüm comparison. kind: 'druk' | 'vacuum'."""
    rnd = random.Random(7 if kind == 'druk' else 11)
    g = f'steel-{kind}'
    gv = f'steelv-{kind}'
    dots = []
    golds = ['#D9A441', '#C38E2E', '#E7BE6A', '#B98227']
    n = 150 if kind == 'druk' else 95
    for _ in range(n):
        x = rnd.uniform(74, 246)
        if kind == 'druk':
            y = 113 - abs(rnd.gauss(0, 9)) - rnd.uniform(0, 2)
        else:
            y = rnd.uniform(87, 112)
        y = max(86, min(112.5, y))
        r = rnd.uniform(1.6, 2.8)
        dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{rnd.choice(golds)}"/>')
    if kind == 'druk':
        right = f'<rect x="262" y="80" width="98" height="36" fill="url(#{g})"/>'
        air = '<path d="M14 98h26M30 91l8 7-8 7" fill="none" stroke="#56606B" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" opacity=".7"/>'
    else:
        right = (f'<rect x="262" y="80" width="25" height="36" fill="url(#{g})"/>'
                 f'<path d="M286 80A36 36 0 0 0 322 44V0h36v44a72 72 0 0 1-72 72z" fill="url(#{gv})"/>')
        air = '<path d="M340 30V6M333 14l7-8 7 8" fill="none" stroke="#56606B" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" opacity=".7"/>'
    arrows = ''.join(f'<path d="M{x} 98h20M{x + 13} 91l7 7-7 7" fill="none" stroke="#D21F26" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
                     for x in (138, 176))
    title = 'Druktransport: product wordt met perslucht door de leiding geduwd' if kind == 'druk' else 'Vacuümtransport: product wordt door onderdruk in de leiding aangezogen'
    return f'''<svg viewBox="0 0 360 150" role="img" aria-label="{title}">
  <defs>
    <linearGradient id="{g}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EEF1F4"/><stop offset=".35" stop-color="#C6CFD8"/><stop offset=".7" stop-color="#97A3B0"/><stop offset="1" stop-color="#D3DAE1"/></linearGradient>
    <linearGradient id="{gv}" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#D3DAE1"/><stop offset=".35" stop-color="#97A3B0"/><stop offset=".7" stop-color="#C6CFD8"/><stop offset="1" stop-color="#EEF1F4"/></linearGradient>
  </defs>
  <rect x="0" y="80" width="62" height="36" fill="url(#{g})"/>
  {right}
  <rect x="68" y="81" width="184" height="34" fill="#F3F5F8" opacity=".75"/>
  {''.join(dots)}
  <rect x="68" y="81" width="184" height="34" fill="none" stroke="#97A3B0" stroke-width="1"/>
  <path d="M74 86h170" stroke="#fff" stroke-width="2" opacity=".7"/>
  <rect x="56" y="72" width="13" height="52" rx="2" fill="url(#{g})" stroke="#8A949F" stroke-width=".8"/>
  <rect x="251" y="72" width="13" height="52" rx="2" fill="url(#{g})" stroke="#8A949F" stroke-width=".8"/>
  {arrows}
  {air}
</svg>'''


# ---------------------------------------------------------------- process-flow symbols + plate figure
# Simplified process-flow symbols (after ISO 10628) on a 24px grid, 1.5px stroke: the site's icon set for disciplines.
SYM = {
    'Stofafzuiging': '<path d="M7 4h10v5l-3.5 8h-3L7 9z"/><path d="M10.5 17v3h3v-3M17 6.5h4"/>',
    'Filtratie': '<rect x="5" y="4" width="14" height="16" rx="1"/><path d="M5.5 19.5 18.5 4.5" stroke-dasharray="2 2"/>',
    'Hoogvacuüm': '<circle cx="12" cy="12" r="7.5"/><path d="M8.5 6.8 19.3 12 8.5 17.2"/>',
    'Pneumatisch transport': '<path d="M3 12h15M15 8.5l3.5 3.5-3.5 3.5"/><circle cx="6.5" cy="9" r="1.1"/><circle cx="10" cy="15" r="1.1"/><circle cx="12.5" cy="9.5" r="1.1"/>',
    'Doseren': '<circle cx="12" cy="12" r="7.5"/><path d="M12 4.5v15M4.5 12h15M6.7 6.7l10.6 10.6M17.3 6.7 6.7 17.3"/>',
    'Zeven en scheiden': '<rect x="4" y="6" width="16" height="12" rx="1"/><path d="M4.5 12h15" stroke-dasharray="2 2"/><path d="M9 18v2.5M15 18v2.5"/>',
    'Opslaan': '<path d="M6 3h12v11l-4 5.5h-4L6 14z"/><path d="M6 14h12M10 19.5v1.5h4v-1.5"/>',
    'Industriële luchttechniek': '<circle cx="12" cy="12" r="7.5"/><path d="M12 12 9 5.6M12 12l6.6 2.4M12 12l-3.6 6.3"/>',
    'Solids processing': '<path d="M6 3h12v11l-4 5.5h-4L6 14z"/><path d="M6 14h12"/>',
}



def sym(name, cls='sym'):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" '
            f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{SYM[name]}</svg>')


def plate_figure(items, caption, sizes, cls=''):
    """Framed plate with a consistent transparent product render per item."""
    imgs = ''.join(
        f'<div class="pfig__img pfig__img--cut{" is-on" if i == 0 else ""}" '
        f'data-fig-img="{_slug(n)}" data-cap="{n}">{pic(SOL_IMG[n], "", sizes)}</div>' for i, n in enumerate(items))
    reg = ''.join(f'<i class="pfig__reg pfig__reg--{c}" aria-hidden="true"></i>' for c in ('tl', 'tr', 'bl', 'br'))
    c = f' {cls}' if cls else ''
    return (f'<figure class="pfig{c}" data-fig-frame>{imgs}{reg}'
            f'<figcaption><span data-fig-cap>{items[0]}</span><span>{caption}</span></figcaption></figure>')


# component groups: symbol per group, cross-section render where one exists (block 3 "Catalogusbladen")
SYM.update({
    'pipe': '<path d="M5 20v-7a8 8 0 0 1 8-8h6"/><path d="M3 20h4M19 3v4"/>',
    'bag': '<path d="M7 7h10l2 9-3 4H8l-3-4z"/><path d="M9 7V4.5M15 7V4.5"/>',
    'valve': '<path d="M4 7v10l16-10v10z"/><path d="M12 12V5M9.5 5h5"/>',
})
COMP_SYM = {
    'Blowers &amp; ventilatoren': 'Hoogvacuüm', 'Cyclonen': 'Stofafzuiging', 'Filters': 'Filtratie',
    'Doseersluizen': 'Doseren', 'Leidingwerk &amp; koppelingen': 'pipe', 'Big-bag stations': 'bag',
    'Afsluiters': 'valve', 'Zeven': 'Zeven en scheiden',
}
COMP_SECTION = {
    'Blowers &amp; ventilatoren': ('14-blower-doorsnede', True),
    'Cyclonen': ('13-cycloon-doorsnede', False),
    'Filters': ('05-filter-doorsnede', False),
    'Doseersluizen': ('15-doseersluis-doorsnede', False),
    'Leidingwerk &amp; koppelingen': ('07-leidingwerk-doorsnede', False),
    'Big-bag stations': ('08-bigbag-doorsnede', False),
    'Afsluiters': ('09-afsluiter-doorsnede', False),
    'Zeven': ('10-zeef-doorsnede', False),
}


def catalog_sheet(title, href, img, i):
    sec = COMP_SECTION.get(title)
    sizes = '(min-width: 960px) 22vw, 45vw'
    sec_html = ''
    if sec:
        flip = ' sheet__img--flip' if sec[1] else ''
        sec_html = (f'<span class="sheet__img sheet__img--sec{flip}">{pic(sec[0], "", sizes)}</span>'
                    f'<i class="sheet__cut" aria-hidden="true"></i>')
    reg = ''.join(f'<i class="sheet__reg sheet__reg--{c}" aria-hidden="true"></i>' for c in ('tl', 'tr', 'bl', 'br'))
    hint = '<span class="visually-hidden"> (met doorsnede)</span>' if sec else ''
    return (f'<li class="catalog__cell" style="--i:{i}"><a class="sheet" href="{href}">'
            f'<span class="sheet__plate{" has-sec" if sec else ""}"><span class="sheet__img sheet__img--ext">{pic(img, "", sizes)}</span>'
            f'{sec_html}{reg}<i class="sheet__dim sheet__dim--x" aria-hidden="true"></i><i class="sheet__dim sheet__dim--y" aria-hidden="true"></i></span>'
            f'<span class="sheet__label">{sym(COMP_SYM[title])}<span>{title}{hint}</span>{icon("ur")}</span></a>'
            f'<button class="sheet__toggle" type="button" aria-pressed="false" aria-label="Doorsnede van {title}">Doorsnede</button></li>')
