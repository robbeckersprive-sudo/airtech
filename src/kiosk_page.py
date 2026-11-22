"""Beurs Kiosk Modus (Nov 22): owner login "Beheer" + a synchronised trade-fair slideshow on one or two screens.

Usage:  python src/kiosk_page.py        (also called at the end of src/build.py)

Writes NL/EN/DE pages and one service worker in the site root:
  beheer[-en|-de].html   owner login + dashboard (settings, live preview, start), behaviour assets/js/beheer.js
  kiosk[-en|-de].html    the player; every sheet is a <template> with three faces: a (left screen), b (right screen), s (single screen)
  kiosk-sw.js   service worker that pre-caches everything the kiosk shows (trade-fair wifi is unreliable)

Content comes from the site data (categories, cyclones, projects), so a new product or project on the site
appears in the kiosk after a rebuild. Styles assets/css/kiosk.css, player assets/js/kiosk.js. README "Beurs Kiosk Modus".
"""
import hashlib
import json
import os
import re
import sys
import i18n
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from components import ROOT, MANIFEST, PHONE_DISPLAY, EMAIL, ADDRESS, COMPONENTEN, _v  # noqa: E402
from category_data import CATEGORIES  # noqa: E402
from cyclone_category_data import CYCLONES  # noqa: E402
from project_data import PROJECTS  # noqa: E402
from home_practice import _count_attrs, ORDER as PROJECT_ORDER  # noqa: E402

KMAN = json.load(open(os.path.join(ROOT, 'images', 'kiosk', 'manifest.json'), encoding='utf-8'))
DOMAIN = 'airtechnicsolutions.nl'
CACHE = set()          # every URL the kiosk can show -> kiosk-sw.js


# ---------------------------------------------------------------- images
def img(name, cls='', pos=''):
    """Fixed-URL picture (no srcset guessing), so the service worker can pre-cache exactly what is shown.
    Kiosk renders: 1920/3840 (panorama 3840/7680) chosen by screen width; site library: its largest width."""
    style = f' style="object-position:{pos}"' if pos else ''
    c = f' class="{cls}"' if cls else ''
    if name in KMAN:
        small, big = KMAN[name]['widths']
        base = f'images/kiosk/{name}'
        CACHE.update(f'{base}-{w}.{fmt}' for w in (small, big) for fmt in ('avif', 'webp'))
        return (f'<picture><source media="(min-width: 2000px)" type="image/avif" srcset="{base}-{big}.avif">'
                f'<source type="image/avif" srcset="{base}-{small}.avif">'
                f'<img src="{base}-{small}.webp" alt="" decoding="async"{c}{style}></picture>')
    w = MANIFEST[name]['widths'][-1]
    CACHE.update({f'images/{name}-{w}.avif', f'images/{name}-{w}.webp'})
    return (f'<picture><source type="image/avif" srcset="images/{name}-{w}.avif">'
            f'<img src="images/{name}-{w}.webp" alt="" decoding="async"{c}{style}></picture>')


def first_sentence(text):
    return re.split(r'(?<=[.!?])\s', text.strip())[0]


def heading(html):
    """Site headings carry soft hyphens and <br><em> for the flow word; the kiosk keeps the <br><em>."""
    return html.replace('&shy;', '')


# ---------------------------------------------------------------- sheets
# group slug -> hero (kiosk render where supplied), text side on that render, exterior + registered section (Röntgen)
GROUPS = [
    ('blowers-ventilatoren', '18-blower-macro', 'left', '03-blower-vrijstaand', '14-blower-doorsnede-reg'),
    ('cyclonen', '02-cycloon', 'left', '04-cycloon-vrijstaand', '13-cycloon-doorsnede-reg'),
    ('filters', '03-filter', 'right', '05-filter-vrijstaand', '05-filter-doorsnede'),
    ('doseersluizen', '04-doseersluis', 'left', '06-doseersluis-vrijstaand', '15-doseersluis-doorsnede-reg'),
    ('leidingwerk-koppelingen', '01-hero-pijpleiding', 'left', '07-leidingwerk-vrijstaand', '07-leidingwerk-doorsnede'),
    ('bigbag-stations', 'cat-hero-bigbag', 'left', '08-bigbag-vrijstaand', '08-bigbag-doorsnede'),
    ('afsluiters', '31-hero-wissel', 'left', '09-afsluiter-vrijstaand', '09-afsluiter-doorsnede'),
    ('zeven', 'cat-hero-zeven', 'left', '10-zeef-vrijstaand', '10-zeef-doorsnede'),
]
PRODUCT_LINE = ['Opslaan', 'Doseren', 'Pneumatisch transport', 'Zeven en scheiden']
AIR_LINE = ['Stofafzuiging', 'Hoogvacuüm', 'Filtratie']
STEPS = [   # titles and images of the home "Werkwijze" (pages.home); first sentence of each step text
    ('Analyse', '22-proces-analyse', 'We brengen uw proces en de gewenste capaciteit in kaart.'),
    ('Engineering', '23-proces-engineering', 'We ontwerpen een installatie voor uw productieomgeving.'),
    ('Realisatie', '24-proces-realisatie', 'We produceren of leveren de onderdelen volgens het ontwerp en monteren de procesinstallatie op locatie.'),
    ('Inbedrijfstelling', '25-proces-inbedrijfstelling', 'We starten de installatie op, stellen de bedrijfsparameters af en toetsen de werking aan de afgesproken eisen.'),
]
TOTEM_CALLOUTS = [   # (x, y) in % of the totem render, label, function
    (45, 40, 'Silo', 'Opslaan'), (46, 60, 'Cycloon', 'Scheiden'), (50, 77, 'Filter', 'Filtreren'),
    (49, 92, 'Sluis', 'Doseren'),
]


def mono(text, cls=''):
    return f'<p class="ks-mono{(" " + cls) if cls else ""}">{text}</p>'


def face(role, body, cls=''):
    return f'<div class="ks-face ks-face--{role}{(" " + cls) if cls else ""}" data-face="{role}">{body}</div>'


def sheet(sid, kind, dur, title, faces, extra=''):
    return (f'<template data-sheet="{sid}" data-kind="{kind}" data-dur="{dur}" data-title="{escape(title)}"{extra}>'
            f'{"".join(faces)}</template>')


def s_opening():
    pano = img('01-proceslijn-panorama', 'ks-pano__img')
    flow = '<canvas class="ks-flow" data-flow aria-hidden="true"></canvas>'
    a = face('a', f'''<div class="ks-pano ks-pano--a">{pano}</div>{flow}
      <div class="ks-copy ks-copy--top">{mono("Airtechnic Solutions · Beek en Donk", "ks-rise")}
        <h1 class="ks-h ks-h--mega ks-rise" style="--d:.25s">Industriële luchttechniek<br><em>&amp; solids processing.</em></h1></div>''')
    b = face('b', f'''<div class="ks-pano ks-pano--b">{pano}</div>{flow}
      <div class="ks-copy ks-copy--top ks-copy--end">{mono("Van procesanalyse tot werkende installatie", "ks-rise")}
        <p class="ks-h ks-h--mega ks-rise" style="--d:.25s">Grip op<br><em>elke stroom.</em></p></div>''')
    s = face('s', f'''<div class="ks-pano ks-pano--s">{pano}</div>{flow}
      <div class="ks-copy ks-copy--top">{mono("Airtechnic Solutions · Beek en Donk", "ks-rise")}
        <h1 class="ks-h ks-h--mega ks-rise" style="--d:.25s">Industriële luchttechniek<br><em>&amp; solids processing.</em></h1>
        <p class="ks-lead ks-rise" style="--d:.6s">Grip op elke stroom.</p></div>''')
    return sheet('opening', 'flow', 16, 'Airtechnic Solutions', [a, b, s])


def _line(items, start):
    return ''.join(f'<li class="ks-rise" style="--d:{.5 + i * .18:.2f}s"><b>{start + i:02d}</b>{n}</li>' for i, n in enumerate(items))


def s_specialisaties():
    join = ('<svg class="ks-join ks-join--{r}" viewBox="0 0 1000 100" preserveAspectRatio="none" aria-hidden="true">'
            '<path pathLength="100" d="M0 50H1000"/></svg>')
    a_body = f'''<div class="ks-bg ks-bg--grain">{img("05-granulaat-textuur")}</div>
      <div class="ks-copy ks-copy--duo">{mono("Specialisatie A · Productstromen", "ks-rise")}
        <h2 class="ks-h ks-h--xl ks-rise" style="--d:.2s">Poeders en granulaten.<br><em>Gecontroleerd verplaatst.</em></h2>
        <ol class="ks-line">{_line(PRODUCT_LINE, 1)}</ol></div>'''
    b_body = f'''<div class="ks-bg ks-bg--grid"></div>
      <div class="ks-copy ks-copy--duo">{mono("Specialisatie B · Luchtstromen", "ks-rise")}
        <h2 class="ks-h ks-h--xl ks-rise" style="--d:.2s">Lucht en stof.<br><em>Onder controle.</em></h2>
        <ol class="ks-line">{_line(AIR_LINE, 5)}</ol></div>'''
    label = '<p class="ks-join__label">transportlucht naar het filter</p>'
    a = face('a', a_body + join.format(r='a'))
    b = face('b', b_body + join.format(r='b') + label)
    s = face('s', f'''<div class="ks-bg ks-bg--grid"></div><div class="ks-duo">
      <div class="ks-duo__col ks-duo__col--grain"><div class="ks-bg ks-bg--grain">{img("05-granulaat-textuur")}</div>
        {mono("Productstromen", "ks-rise")}<h2 class="ks-h ks-h--l ks-rise" style="--d:.2s">Poeders en granulaten.<br><em>Gecontroleerd verplaatst.</em></h2><ol class="ks-line">{_line(PRODUCT_LINE, 1)}</ol></div>
      <div class="ks-duo__col">{mono("Luchtstromen", "ks-rise")}<h2 class="ks-h ks-h--l ks-rise" style="--d:.2s">Lucht en stof.<br><em>Onder controle.</em></h2><ol class="ks-line">{_line(AIR_LINE, 5)}</ol></div>
    </div>''')
    return sheet('specialisaties', 'duo', 16, 'Twee specialisaties', [a, b, s])


def s_group(n, total, slug, hero, side, ext, sec):
    if slug == 'cyclonen':
        d = CYCLONES
        names = [i.name for i in d['items']]
    else:
        d = CATEGORIES[slug]
        names = [i['name'] for i in d['items']]
    name = d['name']
    head = heading(d['heading'])
    intro = first_sentence(d['intro'])
    no = f'{n:02d} / {total:02d}'
    chips = ''.join(f'<li class="ks-rise" style="--d:{1.2 + i * .15:.2f}s">{x}</li>' for i, x in enumerate(names[:5]))
    hero_html = f'<div class="ks-hero ks-hero--{side}">{img(hero, "ks-kb")}</div>'
    copy = f'''<div class="ks-copy ks-copy--{side} ks-copy--low">{mono(f"Componenten · {no}", "ks-rise")}
        <h2 class="ks-h ks-h--xl ks-rise" style="--d:.2s">{head}</h2><p class="ks-lead ks-rise" style="--d:.45s">{intro}</p></div>'''
    reg = ''.join(f'<i class="ks-reg ks-reg--{c}"></i>' for c in ('tl', 'tr', 'bl', 'br'))
    xray = f'''<div class="ks-xray"><div class="ks-xray__plate">
        <div class="ks-xray__img">{img(ext)}</div><div class="ks-xray__img ks-xray__img--sec">{img(sec)}</div>
        <i class="ks-xray__scan"><b>Doorsnede</b></i>{reg}</div></div>'''
    info = f'''<div class="ks-spec">{mono("Principe", "ks-rise")}
        <p class="ks-h ks-h--m ks-rise" style="--d:.3s">{d["principle"]}</p>
        <p class="ks-text ks-rise" style="--d:.55s">{d["explanation"]}</p>
        {mono(f"{len(names)} uitvoeringen", "ks-rise ks-spec__k")}<ul class="ks-chips">{chips}</ul></div>'''
    a = face('a', hero_html + copy)
    b = face('b', f'<div class="ks-bg ks-bg--grid"></div><div class="ks-split">{xray}{info}</div>')
    s = face('s', f'''<div class="ks-split ks-split--s"><div class="ks-hero ks-hero--panel">{img(hero, "ks-kb")}</div>
      <div class="ks-split__copy">{mono(f"Componenten · {no}", "ks-rise")}<h2 class="ks-h ks-h--l ks-rise" style="--d:.2s">{head}</h2>
        <p class="ks-lead ks-rise" style="--d:.45s">{intro}</p>{mono(f"{len(names)} uitvoeringen", "ks-rise ks-spec__k")}<ul class="ks-chips">{chips}</ul></div></div>''')
    return sheet(f'groep-{slug}', 'group', 13, name, [a, b, s], f' data-group="{slug}"')


def s_project(slug):
    p = PROJECTS[slug]
    facts = ''.join(f'<li class="ks-rise" style="--d:{.6 + i * .2:.2f}s"><b{_count_attrs(v)}>{escape(v)}</b><span>{k}</span></li>'
                    for i, (v, k) in enumerate(p['facts'][:3]))
    a = face('a', f'''<div class="ks-hero ks-hero--left">{img(p["image"], "ks-kb")}</div>
      <div class="ks-copy ks-copy--left ks-copy--low">{mono(f"Projectdossier · {p['sector']}", "ks-rise")}
        <h2 class="ks-h ks-h--xl ks-rise" style="--d:.2s">{p["title"]}</h2></div>''')
    b = face('b', f'''<div class="ks-bg ks-bg--grid"></div><div class="ks-dossier">{mono("Feiten uit dit project", "ks-rise")}
        <p class="ks-lead ks-lead--l ks-rise" style="--d:.3s">{p["lead"]}</p><ul class="ks-facts">{facts}</ul>
        <dl class="ks-meta ks-rise" style="--d:1.4s"><div><dt>Materiaal</dt><dd>{p["material"]}</dd></div><div><dt>Omvang</dt><dd>{p["scope"]}</dd></div></dl></div>''')
    s = face('s', f'''<div class="ks-split ks-split--s"><div class="ks-hero ks-hero--panel">{img(p["image"], "ks-kb")}</div>
      <div class="ks-split__copy">{mono(f"Projectdossier · {p['sector']}", "ks-rise")}<h2 class="ks-h ks-h--l ks-rise" style="--d:.2s">{p["title"]}</h2>
        <ul class="ks-facts ks-facts--s">{facts}</ul></div></div>''')
    return sheet(f'project-{slug}', 'project', 14, p['name'], [a, b, s], ' data-pool="project"')


def s_steps():
    plates = ''.join(f'''<div class="ks-step-plate" style="--d:{i * 6}s">
        <div class="ks-step-plate__dr">{img(f"{im}-tekening")}</div><div class="ks-step-plate__ph">{img(im)}</div>
        <i class="ks-step-plate__scan"></i></div>''' for i, (_n, im, _t) in enumerate(STEPS))
    rail = ''.join(f'<li style="--d:{i * 6}s"><b>{i + 1:02d}</b><span class="ks-rail__n">{n}</span><span class="ks-rail__t">{t}</span></li>'
                   for i, (n, _im, t) in enumerate(STEPS))
    a = face('a', f'''<div class="ks-steps-sheet">{plates}</div>
      <div class="ks-copy ks-copy--top">{mono("Werkwijze", "ks-rise")}<h2 class="ks-h ks-h--xl ks-rise" style="--d:.2s">Van tekening<br><em>tot installatie.</em></h2></div>''')
    b = face('b', f'<div class="ks-bg ks-bg--grid"></div><ol class="ks-rail">{rail}</ol>')
    s = face('s', f'''<div class="ks-split ks-split--s"><div class="ks-steps-sheet ks-steps-sheet--panel">{plates}</div>
      <div class="ks-split__copy">{mono("Werkwijze", "ks-rise")}<h2 class="ks-h ks-h--l ks-rise" style="--d:.2s">Van tekening<br><em>tot installatie.</em></h2><ol class="ks-rail ks-rail--s">{rail}</ol></div></div>''')
    return sheet('werkwijze', 'steps', 24, 'Werkwijze', [a, b, s])


def s_installatie():
    calls = ''.join(f'<li class="ks-call" style="--x:{x}%;--y:{y}%;--d:{.8 + i * .35:.2f}s"><i></i><span><b>{fn}</b>{lab}</span></li>'
                    for i, (x, y, lab, fn) in enumerate(TOTEM_CALLOUTS))
    totem = f'<div class="ks-totem"><div class="ks-totem__img">{img("06-totem")}<ul class="ks-calls">{calls}</ul></div></div>'
    mats = [PROJECTS[k]['material'] for k in PROJECT_ORDER]
    mat_list = ''.join(f'<li class="ks-rise" style="--d:{.6 + i * .2:.2f}s">{m}</li>' for i, m in enumerate(mats))
    a = face('a', f'''<div class="ks-bg ks-bg--grid"></div>{totem}
      <div class="ks-copy ks-copy--left ks-copy--mid ks-copy--narrow">{mono("Componenten in samenhang", "ks-rise")}
        <h2 class="ks-h ks-h--xl ks-rise" style="--d:.2s">Van component<br><em>tot complete installatie.</em></h2></div>''')
    b = face('b', f'''<div class="ks-bg ks-bg--grain ks-bg--dim">{img("05-granulaat-textuur")}</div>
      <div class="ks-copy ks-copy--mid">{mono("Materialen uit onze projecten", "ks-rise")}<ul class="ks-mats">{mat_list}</ul></div>''')
    s = face('s', f'''<div class="ks-bg ks-bg--grid"></div>{totem}
      <div class="ks-copy ks-copy--left ks-copy--mid ks-copy--narrow">{mono("Componenten in samenhang", "ks-rise")}
        <h2 class="ks-h ks-h--l ks-rise" style="--d:.2s">Van component<br><em>tot complete installatie.</em></h2></div>''')
    return sheet('installatie', 'install', 15, 'Installaties', [a, b, s])


def s_contact():
    addr = f'{ADDRESS[0]}, {ADDRESS[1]}'
    a = face('a', f'''<div class="ks-bg ks-bg--grid"></div><i class="ks-sweep"></i>
      <div class="ks-copy ks-copy--mid">{mono("Stel uw procesvraag", "ks-rise")}
        <p class="ks-h ks-h--mega ks-rise" style="--d:.2s">Bespreek uw proces.<br><em>Hier op de stand.</em></p></div>''')
    b = face('b', f'''<div class="ks-bg ks-bg--grid"></div><i class="ks-sweep"></i>
      <div class="ks-copy ks-copy--mid"><dl class="ks-contact">
        <div class="ks-rise" style="--d:.3s"><dt>Web</dt><dd>{DOMAIN}</dd></div>
        <div class="ks-rise" style="--d:.5s"><dt>Telefoon</dt><dd>{PHONE_DISPLAY}</dd></div>
        <div class="ks-rise" style="--d:.7s"><dt>E-mail</dt><dd>{EMAIL}</dd></div>
        <div class="ks-rise" style="--d:.9s"><dt>Adres</dt><dd>{addr}</dd></div></dl></div>''')
    s = face('s', f'''<div class="ks-bg ks-bg--grid"></div><i class="ks-sweep"></i>
      <div class="ks-copy ks-copy--mid">{mono("Stel uw procesvraag", "ks-rise")}
        <p class="ks-h ks-h--xl ks-rise" style="--d:.2s">Bespreek uw proces.<br><em>Hier op de stand.</em></p>
        <dl class="ks-contact ks-contact--s"><div class="ks-rise" style="--d:.6s"><dt>Web</dt><dd>{DOMAIN}</dd></div>
        <div class="ks-rise" style="--d:.8s"><dt>Telefoon</dt><dd>{PHONE_DISPLAY}</dd></div></dl></div>''')
    return sheet('contact', 'contact', 14, 'Contact', [a, b, s])


def sheets():
    CACHE.clear()
    out = [s_opening(), s_specialisaties()]
    out += [s_group(i + 1, len(GROUPS), *g) for i, g in enumerate(GROUPS)]
    out += [s_project(k) for k in PROJECT_ORDER]
    out += [s_steps(), s_installatie(), s_contact()]
    return out


# ---------------------------------------------------------------- pages
HEAD = '''<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#08182A">
<title>{title}</title>
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{fonts}">
<link rel="stylesheet" href="{tokens}">
<link rel="stylesheet" href="{css}">
</head>
'''


def head(title):
    return HEAD.format(title=title, fonts=_v('assets/css/fonts.css'), tokens=_v('assets/css/tokens.css'), css=_v('assets/css/kiosk.css'))


def titleblock():
    """Persistent drawing title block per screen; the red progress line runs across both screens."""
    return '''<footer class="ks-tb" aria-hidden="true"><i class="ks-tb__progress"><i data-progress></i></i>
  <div class="ks-tb__cell ks-tb__cell--logo" data-tb="a s"><img src="assets/img/airtechnic-logo-640.webp" alt="" width="640" height="212"></div>
  <div class="ks-tb__cell ks-tb__cell--wide" data-tb="a s"><span class="ks-tb__k">Onderwerp</span><span data-tb-title>Airtechnic Solutions</span></div>
  <div class="ks-tb__cell" data-tb="a s"><span class="ks-tb__k">Blad</span><span data-tb-sheet>01</span></div>
  <div class="ks-tb__cell ks-tb__cell--wide" data-tb="b"><span class="ks-tb__k">Industriële luchttechniek</span><span>&amp; solids processing</span></div>
  <div class="ks-tb__cell" data-tb="b s"><span class="ks-tb__k">Web</span><span>''' + DOMAIN + '''</span></div>
  <div class="ks-tb__cell" data-tb="b"><span class="ks-tb__k">Telefoon</span><span>''' + PHONE_DISPLAY + '''</span></div>
  <div class="ks-tb__cell" data-tb="a b s"><span class="ks-tb__k">Schaal</span><span>1 : 1</span></div>
</footer>'''


def kiosk_html(all_sheets):
    groups = json.dumps([[g[0], (CYCLONES if g[0] == 'cyclonen' else CATEGORIES[g[0]])['name']] for g in GROUPS], ensure_ascii=False)
    return head('Airtechnic · Kiosk') + f'''<body class="ks-body">
<div class="ks-root" data-kiosk-root>
  <div class="ks-stage" data-stage></div>
  <i class="ks-scan" data-scan aria-hidden="true"></i>
  {titleblock()}
  <div class="ks-gate" data-gate hidden>
    <div class="ks-gate__card"><p class="ks-mono">Airtechnic · Kiosk</p><p class="ks-gate__h" data-gate-title>Kiosk starten</p>
      <p class="ks-gate__t" data-gate-text>Klik om dit scherm volledig te vullen.</p>
      <button type="button" class="ks-btn" data-gate-go>Start dit scherm</button>
      <a class="ks-gate__link" href="beheer.html" data-gate-login hidden>Naar Beheer</a></div>
  </div>
  <div class="ks-exit" data-exit hidden role="dialog" aria-modal="true" aria-labelledby="ks-exit-h">
    <div class="ks-gate__card"><p class="ks-gate__h" id="ks-exit-h">Kiosk stoppen?</p>
      <p class="ks-gate__t">Alle kioskschermen stoppen tegelijk.</p>
      <div class="ks-exit__row"><button type="button" class="ks-btn ks-btn--ghost" data-exit-no>Doorgaan</button><button type="button" class="ks-btn" data-exit-yes>Stoppen</button></div></div>
  </div>
</div>
<div class="ks-sheets" hidden>{"".join(all_sheets)}</div>
<script type="application/json" id="ks-groups">{groups}</script>
<script src="{_v('assets/js/kiosk.js')}"></script>
<script>AtKiosk.boot();</script>
</body>
</html>
'''


def beheer_html():
    groups = ''.join(f'<label class="bh-chip"><input type="checkbox" name="groups" value="{slug}" checked><span>{(CYCLONES if slug == "cyclonen" else CATEGORIES[slug])["name"]}</span></label>'
                     for slug, *_ in GROUPS)
    return head('Beheer · Airtechnic Solutions') + f'''<body class="bh-body">
<a class="bh-skip" href="#bh-main">Direct naar de inhoud</a>
<header class="bh-top">
  <a class="bh-logo" href="index.html" aria-label="Naar de website"><img src="assets/img/airtechnic-logo-640.webp" alt="Airtechnic" width="640" height="212"></a>
  <span class="bh-top__k">Beheer</span><!--i18n:skip--><nav class="bh-languages" aria-label="Taal beheer"><a href="beheer.html" lang="nl">NL</a><a href="beheer-en.html" lang="en">EN</a><a href="beheer-de.html" lang="de">DE</a></nav><!--/i18n:skip-->
  <span class="bh-top__user" data-user hidden><span data-user-mail></span><button type="button" class="bh-link" data-logout>Uitloggen</button></span>
</header>
<main id="bh-main" class="bh-main" tabindex="-1">

  <section class="bh-login" data-view="login" hidden aria-labelledby="bh-login-h">
    <form class="bh-plate" data-login novalidate>
      <p class="ks-mono">Airtechnic Solutions · Beheer</p>
      <h1 id="bh-login-h" class="bh-h">Inloggen</h1>
      <div class="bh-field"><label for="bh-mail">E-mailadres</label><input id="bh-mail" name="email" type="email" autocomplete="username" required></div>
      <div class="bh-field"><label for="bh-pass">Wachtwoord</label><input id="bh-pass" name="password" type="password" autocomplete="current-password" required></div>
      <label class="bh-check"><input type="checkbox" name="remember"><span>Onthoud dit apparaat 30 dagen (de kiosk-pc op de stand)</span></label>
      <p class="bh-error" data-login-error role="alert" hidden></p>
      <button type="submit" class="ks-btn">Inloggen</button>
      <dl class="bh-tb"><div><dt>Blad</dt><dd>Beheer</dd></div><div><dt>Schaal</dt><dd>1 : 1</dd></div><div><dt>Rev.</dt><dd>2026</dd></div></dl>
    </form>
  </section>

  <section class="bh-welcome" data-view="welcome" hidden aria-labelledby="bh-welcome-h">
    <svg class="bh-welcome__draw" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
      <path pathLength="100" class="bh-d1" d="M60 60H1540V840H60Z"/>
      <path pathLength="100" class="bh-d3" d="M-20 792H560C660 792 700 752 800 752H1620"/>
      <path pathLength="100" class="bh-d4" d="M-20 828H560C660 828 700 788 800 788H1620"/>
    </svg>
    <div class="bh-welcome__copy">
      <p class="ks-mono bh-w1">Opgeleverd · <span data-today></span></p>
      <h1 id="bh-welcome-h" class="bh-welcome__h"><span class="bh-w2">Uw beursstand,</span><br><em class="bh-w3">klaar voor gebruik.</em></h1>
      <p class="bh-welcome__t bh-w4">Vanaf hier toont u op één of twee schermen een doorlopende presentatie van uw expertise, componenten en projecten. In de stijl van uw website, en altijd actueel.</p>
      <button type="button" class="ks-btn bh-w5" data-welcome-done>Naar de kioskmodus</button>
    </div>
    <dl class="bh-welcome__tb bh-w4"><div><dt>Opdrachtgever</dt><dd>Airtechnic Solutions</dd></div><div><dt>Blad</dt><dd>Kiosk modus</dd></div><div><dt>Status</dt><dd>Gereed</dd></div></dl>
  </section>

  <section class="bh-dash" data-view="dash" hidden aria-labelledby="bh-dash-h">
    <div class="bh-dash__head">
      <div><p class="ks-mono">Beheer · Beurs</p><h1 id="bh-dash-h" class="bh-h">Kiosk modus</h1>
        <p class="bh-sub">Een doorlopende presentatie voor de beursstand. De inhoud komt rechtstreeks uit de website.</p></div>
      <button type="button" class="bh-link" data-welcome-replay>Welkomst opnieuw afspelen</button>
    </div>
    <div class="bh-grid">
      <form class="bh-settings" data-settings>
        <fieldset class="bh-set"><legend><b>01</b> Opstelling</legend>
          <div class="bh-cards">
            <label class="bh-card"><input type="radio" name="layout" value="1"><span class="bh-card__fig bh-card__fig--one" aria-hidden="true"><i></i></span><span class="bh-card__t">Eén scherm</span><span class="bh-card__s">Laptop of één monitor</span></label>
            <label class="bh-card"><input type="radio" name="layout" value="2" checked><span class="bh-card__fig bh-card__fig--two" aria-hidden="true"><i></i><i></i></span><span class="bh-card__t">Twee schermen</span><span class="bh-card__s">Naast elkaar, één doorlopend beeld</span></label>
          </div>
        </fieldset>
        <fieldset class="bh-set"><legend><b>02</b> Componenten in de presentatie</legend>
          <div class="bh-chips">{groups}</div>
          <div class="bh-toggles"><label class="bh-check"><input type="checkbox" name="projects" checked><span>Projecten (twee per ronde, wisselend)</span></label>
            <label class="bh-check"><input type="checkbox" name="steps" checked><span>Werkwijze</span></label></div>
        </fieldset>
        <fieldset class="bh-set"><legend><b>03</b> Tempo en taal</legend>
          <div class="bh-seg" role="radiogroup" aria-label="Tempo"><label><input type="radio" name="tempo" value="1" checked><span>Normaal</span></label><label><input type="radio" name="tempo" value="1.3"><span>Rustig</span></label></div>
          <div class="bh-seg" role="radiogroup" aria-label="Taal"><label><input type="radio" name="lang" value="nl" checked><span>NL</span></label><label><input type="radio" name="lang" value="en"><span>EN</span></label><label><input type="radio" name="lang" value="de"><span>DE</span></label></div>
          <p class="bh-hint">De gekozen taal geldt voor beide schermen en wordt op dit apparaat bewaard.</p>
        </fieldset>
        <fieldset class="bh-set" data-screens-set><legend><b>04</b> Schermen</legend>
          <p class="bh-hint" data-screens-text>Sluit het tweede scherm aan en laat de browser uw schermen zoeken. Scherm B opent dan vanzelf op het tweede scherm.</p>
          <button type="button" class="ks-btn ks-btn--ghost" data-screens-find>Schermen zoeken</button>
          <ol class="bh-screens" data-screens hidden></ol>
        </fieldset>
      </form>
      <aside class="bh-preview" aria-labelledby="bh-prev-h">
        <div class="bh-preview__head"><h2 id="bh-prev-h" class="ks-mono">Live voorbeeld</h2><p class="bh-preview__meta" data-loop-meta></p></div>
        <p class="bh-offline" data-offline-status role="status">Offline voorbereiden…</p><p class="bh-status" data-save-status role="status" aria-live="polite"></p><div class="bh-preview__screens" data-preview></div>
        <button type="button" class="bh-link bh-preview__pause" data-preview-pause aria-pressed="false">Voorbeeld pauzeren</button><p class="bh-error" data-preview-error role="alert" hidden></p><button type="button" class="ks-btn ks-btn--big" data-start>Start kiosk</button>
        <p class="bh-hint" data-start-hint>Stoppen: druk op Esc, of houd linksboven 3 seconden ingedrukt.</p>
        <details class="bh-more"><summary>Scherm B op een tweede apparaat</summary>
          <p class="bh-hint">Open deze link op het tweede apparaat (ook ingelogd). De schermen lopen gelijk op de klok, ook zonder netwerk.</p>
          <div class="bh-copy"><input type="text" readonly data-b-link aria-label="Link voor scherm B"><button type="button" class="ks-btn ks-btn--ghost" data-b-copy>Kopieer</button></div>
        </details>
      </aside>
    </div>
  </section>
</main>
<div class="bh-host" data-host hidden></div>
<script src="{_v('assets/js/kiosk.js')}"></script>
<script src="{_v('assets/js/beheer.js')}"></script>
</body>
</html>
'''


def service_worker(pages):
    shell = ['kiosk.html', 'beheer.html', 'kiosk-en.html', 'kiosk-de.html', 'beheer-en.html', 'beheer-de.html', 'assets/css/fonts.css', 'assets/css/tokens.css', 'assets/css/kiosk.css',
             'assets/js/kiosk.js', 'assets/js/beheer.js', 'assets/img/favicon.svg', 'assets/img/airtechnic-logo-640.webp']
    fonts = sorted('assets/fonts/' + f for f in os.listdir(os.path.join(ROOT, 'assets', 'fonts'))
                   if f.endswith('.woff2') and ('archivo' in f and '100-900' in f or 'ibm-plex-mono' in f))
    urls = shell + fonts + sorted(CACHE)
    version = hashlib.sha256(('\n'.join(urls) + ''.join(pages)).encode()).hexdigest()[:12]
    return f'''/* Generated by src/kiosk_page.py. Pre-caches the kiosk so it keeps running without network.
   Only the listed kiosk URLs are answered from the cache; every other request goes to the network untouched. */
const CACHE = 'at-kiosk-{version}';
const URLS = {json.dumps(urls, indent=0)};
const KNOWN = new Set(URLS.map(u => new URL(u, self.registration.scope).pathname));
self.addEventListener('install', e => {{
  e.waitUntil(caches.open(CACHE).then(async c => {{
    let cursor = 0;
    async function worker() {{
      while (cursor < URLS.length) {{
        const u = URLS[cursor++];
        await c.add(new Request(u, {{cache: 'reload'}})).catch(() => null);
      }}
    }}
    await Promise.all(Array.from({{length: 4}}, worker));
  }}).then(() => self.skipWaiting()));
}});
self.addEventListener('activate', e => {{
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith('at-kiosk-') && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
}});
self.addEventListener('message', e => {{
  if (!e.data || e.data.type !== 'kiosk-cache-status' || !e.ports[0]) return;
  e.waitUntil(caches.open(CACHE).then(async c => {{
    const present = await Promise.all(URLS.map(u => c.match(u)));
    e.ports[0].postMessage({{ready: present.every(Boolean)}});
  }}));
}});
self.addEventListener('fetch', e => {{
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return;
  if (!KNOWN.has(url.pathname)) {{
    // versioned assets and images (e.g. the bundled page CSS of the Vercel build): keep a copy once seen online
    if (!/^\\/(assets|images)\\//.test(url.pathname)) return;
    e.respondWith(caches.open(CACHE).then(c => c.match(e.request).then(hit => hit || fetch(e.request).then(r => {{ if (r.ok) c.put(e.request, r.clone()); return r; }}))));
    return;
  }}
  const page = url.pathname.endsWith('.html');
  // pages: network first (fresh content when online), cache when offline; assets: cache first
  e.respondWith(page
    ? fetch(new Request(e.request, {{signal: AbortSignal.timeout(5000)}})).then(r => {{ if (r.ok) caches.open(CACHE).then(c => c.put(url.pathname, r.clone())); return r; }}).catch(() => caches.match(url.pathname))
    : caches.match(url.pathname).then(hit => hit || fetch(e.request)));
}});
'''


def main():
    all_sheets = sheets()
    kiosk, beheer = kiosk_html(all_sheets), beheer_html()
    files = {}
    extra = json.load(open(os.path.join(ROOT, 'src', 'kiosk_strings.json'), encoding='utf-8'))
    for code in i18n.LANGS:
        suffix = '' if code == 'nl' else '-' + code
        if code != 'nl':
            i18n.catalog(code).update({i18n.norm(k): v[0 if code == 'en' else 1] for k, v in extra.items()})
        payload = {k: (k if code == 'nl' else v[0 if code == 'en' else 1]) for k, v in extra.items()}
        script = '<script>window.KI=' + json.dumps(payload, ensure_ascii=False).replace('</', '<\\/') + ';</script>'
        for kind, source in [('kiosk', kiosk), ('beheer', beheer)]:
            html = i18n.localize_html(source, code).replace('<html lang="nl">', f'<html lang="{code}">')
            if code != 'nl':
                html = html.replace('href="beheer.html" data-gate-login', f'href="beheer{suffix}.html" data-gate-login')
            if code != 'nl':
                html = re.sub(r'data-suf="([^"]*)"', lambda m: 'data-suf="' + m.group(1).replace('/u', '/h') + '"', html)
            html = html.replace('<script src=', script + '<script src=', 1)
            files[f'{kind}{suffix}.html'] = html
    files['kiosk-sw.js'] = service_worker(list(files.values()))
    for name, text in files.items():
        with open(os.path.join(ROOT, name), 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
        print(f'{name:40s} {len(text) // 1024} KB')


if __name__ == '__main__':
    main()
