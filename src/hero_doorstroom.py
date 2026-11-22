"""Home hero "Doorstroom" (Nov 20): one sheet from the header down into block 2.

- The header overlays the hero (page(..., overlay=True)); rail + bar sit on the photo's quiet wall.
- Five sheets of one process line (HERO_SLIDES). Sheet 1 is the empty glass tube with the live granule canvas
  (assets/js/granule-flow.js) and an instrument to switch the flow regime (dichte / verdunde fase); moving the pointer
  over the tube blows an air pulse into it. Sheets 2-5 keep their SVG grain flows (slide_flow.py).
- The tabs became the "Proceslijn": five stations on one centre line along the bottom of the hero. Granules run along
  it, the active segment is the slide clock, and its start (data-sig-origin) is where the site signature line
  (signature.js) turns down into "Twee specialisaties", so hero and block 2 read as one drawing.
Styles: assets/css/top.css (.ds). Behaviour: assets/js/doorstroom.js."""
import json
from components import pic, icon, btn, link, split_lines, _v
from pages import HERO_SLIDES, TUBE, GRAIN_BOX, HERO_SLIDE_SECONDS
from slide_flow import diverter_flow, hero_traces
from hero_modes import SHEET_MODES, EFFECTS

SIZES = '(min-width: 1040px) 100vw, 100vw'

# Callouts on sheet 1, measured on 01-hero-pijpleiding-leeg (x %, y %, label, text, href, side).
# The tube itself is the instrument's subject (and the pointer's playground), so sheet 1 only calls out the bend.
PIPE_SPOTS = [
    (88, 25, 'Transportbocht', 'Bochten voor schurende producten', 'transportbocht.html', 'l'),
]

def _spots(spots):
    out = []
    for i, (x, y, title, text, href, side) in enumerate(spots):
        out.append(f'<li class="ds-spot ds-spot--{side}" style="--x:{x}%;--y:{y}%;--i:{i}" data-ds-spot>'
                   f'<a href="{href}"><span class="ds-spot__dot" aria-hidden="true"><i></i></span>'
                   f'<span class="ds-spot__card"><span class="ds-spot__no" aria-hidden="true">{chr(65 + i)}</span>'
                   f'<strong>{title}</strong><span class="ds-spot__text">{text}</span>{icon("ur")}</span></a></li>')
    return f'<ul class="ds-spots" aria-label="Wat u op deze foto ziet">{"".join(out)}</ul>'


def _pipe():
    def streamline(k):
        return (f'M -60 {791 - k} L {560 - .35 * k:.0f} {791 - k} C {880 - .6 * k:.0f} {791 - k}, '
                f'{1150 - .75 * k:.0f} {620 - .8 * k:.0f}, {1380 - .85 * k:.0f} {270 - .6 * k:.0f}')
    lines = ''.join(f'<path class="sl-base" pathLength="1000" d="{streamline(k)}"/>'
                    f'<path class="sl" pathLength="1000" style="--d:{i * -1.3 - .4:.1f}s;--dur:{6.2 + i * .9:.1f}s" d="{streamline(k)}"/>'
                    for i, k in enumerate((150, 240, 340, 450)))
    tube = json.dumps([[list(b), list(t)] for b, t in TUBE], separators=(',', ':'))
    return f'''<div class="ds-media">{pic(HERO_SLIDES[0]["image"], HERO_SLIDES[0]["alt"], SIZES, eager=True)}</div>
        <canvas class="hero__granules" aria-hidden="true" data-granules data-mode="dense" data-box="{','.join(map(str, GRAIN_BOX))}" data-tube="{tube}" data-glass="{_v('images/hero-glass.webp')}"></canvas>
        <svg class="hero__flow ds-streams" viewBox="0 0 1536 1024" preserveAspectRatio="none" aria-hidden="true" focusable="false" data-flow-svg>
          <defs>
            <linearGradient id="ds-sl-fade" x1="0" x2="1" y1="0" y2="0"><stop offset=".3" stop-color="#fff" stop-opacity="0"/><stop offset=".55" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity=".85"/></linearGradient>
            <mask id="ds-sl-mask"><rect width="1536" height="1024" fill="url(#ds-sl-fade)"/></mask>
          </defs>
          <g class="hero__lines" mask="url(#ds-sl-mask)">{lines}</g>
        </svg>
        {_spots(PIPE_SPOTS)}'''


def _equipment(s):
    effects = dict(EFFECTS, **{'31-hero-wissel': diverter_flow})   # filter / cyclone / dosing: switchable (hero_modes.py)
    overlay = hero_traces(s['image']) + (effects[s['image']]() if s['image'] in effects else '')
    spots = [(x, y, t, sub, href, 'l') for x, y, t, sub, href, _side in s['spots']]
    return f'<div class="ds-media">{pic(s["image"], s["alt"], SIZES)}</div>{overlay}{_spots(spots)}'


def _off(i):
    return '' if i == 0 else ' aria-hidden="true" inert'


# Mode glyphs: 26 x 16, currentColor strokes, granulate dots.
_G = '<svg class="ds-mode__ico" viewBox="0 0 26 16" aria-hidden="true">{}</svg>'
_DOT = '<circle cx="{}" cy="{}" r="{}" fill="var(--granulate)"/>'
GLYPHS = {
    'a1': _G.format('<rect x="9" y="1" width="8" height="10" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.4"/>'
                    + ''.join(_DOT.format(x, y, 1.3) for x, y in ((6, 14), (13, 14), (20, 14), (8, 6), (18, 6)))),
    'b1': _G.format('<rect x="9" y="1" width="8" height="10" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.4"/>'
                    '<path d="M13 1v4M11 3l2 2 2-2" fill="none" stroke="currentColor" stroke-width="1.3"/>'
                    + ''.join(_DOT.format(x, y, 1.3) for x, y in ((10, 14), (13, 15), (16, 14)))),
    'a3': _G.format(''.join(_DOT.format(x, y, 2.4) for x, y in ((6, 8), (13, 10), (20, 7)))),
    'b3': _G.format(''.join(_DOT.format(x, y, 1) for x, y in ((4, 9), (8, 5), (11, 11), (14, 6), (17, 10), (21, 5), (22, 11)))),
    'a4': _G.format('<circle cx="13" cy="8" r="6.5" fill="none" stroke="currentColor" stroke-width="1.4"/>'
                    '<path d="M13 8V1.5" stroke="currentColor" stroke-width="1.4"/>' + _DOT.format(17, 5, 1.4)),
    'b4': _G.format('<circle cx="13" cy="8" r="6.5" fill="none" stroke="currentColor" stroke-width="1.4"/>'
                    '<path d="M13 1.5v13M6.5 8h13" stroke="currentColor" stroke-width="1.4"/>'
                    + ''.join(_DOT.format(x, y, 1.3) for x, y in ((16.5, 4.5), (9.5, 11.5)))),
}


def _instrument(sheet):
    title, hint, modes = SHEET_MODES[sheet]
    btns = []
    for i, (k, label, _t) in enumerate(modes):
        glyph = GLYPHS.get(f'{k}{sheet}') or (f'<i class="ds-mode__glyph ds-mode__glyph--{k}" aria-hidden="true">'
                                             '<b></b><b></b><b></b><b></b><b></b></i>')
        btns.append(f'<button type="button" class="ds-mode__opt" data-ds-mode="{k}" aria-pressed="{str(i == 0).lower()}">'
                    f'{glyph}{label}</button>')
    notes = ''.join(f'<p class="ds-mode__note{" is-on" if i == 0 else ""}" data-ds-note="{k}">{text}</p>'
                    for i, (k, _l, text) in enumerate(modes))
    h = f'<span class="ds-mode__hint">{icon("ur")}{hint}</span>' if hint else ''
    on = ' is-for' if sheet == 0 else ''
    return f'''<div class="ds-mode{on}" data-ds-instrument data-for="{sheet}">
      <p class="ds-mode__t"><span>{title}</span>{h}</p>
      <div class="ds-mode__seg" role="group" aria-label="{title}: kies wat u ziet" data-on="0">{"".join(btns)}<i class="ds-mode__thumb" aria-hidden="true"></i></div>
      <div class="ds-mode__notes" aria-live="polite">{notes}</div>
    </div>'''


def doorstroom_hero():
    n = len(HERO_SLIDES)
    slides, copies, mores, stations = [], [], [], []
    for i, s in enumerate(HERO_SLIDES):
        inner = _pipe() if i == 0 else _equipment(s)
        mode = f' data-mode="{SHEET_MODES[i][2][0][0]}"' if i in SHEET_MODES else ''
        slides.append(f'<div class="ds-slide{" is-on" if i == 0 else ""}" data-slide="{i}"{mode}{_off(i)}><div class="ds-box">{inner}</div></div>')
        copies.append(f'''<div class="ds-copy{" is-on" if i == 0 else ""}" id="ds-slide-{i}" role="group" aria-roledescription="dia" aria-label="{i + 1} van {n}: {s['discipline']}" data-ds-copy{_off(i)}>
          <p class="ds-statement">{split_lines(s['title'])}</p>
          <p class="ds-lead">{s['sub']}</p>
        </div>''')
        text, href = s['link'] if i else ('Meer over pneumatisch transport', 'oplossingen-pneumatisch-transport.html')
        mores.append(f'<span class="ds-more{" is-on" if i == 0 else ""}" data-ds-more{_off(i)}>{link(text, href, "right", "ds-link")}</span>')
        stations.append(f'<li class="ds-st" style="--i:{i}"><button type="button" class="ds-st__btn" data-ds-tab="{i}" aria-controls="ds-slide-{i}"'
                        f'{" aria-current=" + chr(34) + "true" + chr(34) if i == 0 else ""}>'
                        f'<span class="ds-st__thumb" aria-hidden="true"><img src="images/{s["image"]}-480.webp" alt="" width="480" height="320" loading="lazy" decoding="async"></span>'
                        f'<span class="ds-st__node" aria-hidden="true"><i></i></span>'
                        f'<span class="ds-st__no" aria-hidden="true">{i + 1:02d}</span><span class="ds-st__label">{s["tab"]}</span>'
                        f'<span class="visually-hidden"> (dia {i + 1} van {n})</span></button></li>')
    grains = ''.join(f'<i style="--g:{g}"></i>' for g in range(9))
    return f'''<section class="ds" data-hero data-ds data-sheet="0" data-mode="dense" aria-labelledby="ds-title" aria-roledescription="carrousel" style="--slide-dur:{HERO_SLIDE_SECONDS + 2}s">
  <div class="ds-grid" aria-hidden="true"></div>
  <div class="ds-stage" data-ds-stage>
    {"".join(slides)}
    <i class="ds-scan" aria-hidden="true"></i>
  </div>
  <div class="ds-veil" aria-hidden="true"></div>
  <div class="container ds-in">
    <div class="ds-text">
      <h1 id="ds-title" class="ds-kicker"><span class="ds-kicker__pulse" aria-hidden="true"></span>Industriële luchttechniek &amp; solids processing</h1>
      <div class="ds-copies">{"".join(copies)}</div>
      <div class="ds-actions">{btn("Bespreek uw vraagstuk", "#contact", "lg", "ds-cta")}<span class="ds-mores">{"".join(mores)}</span></div>
    </div>
    {"".join(_instrument(i) for i in sorted(SHEET_MODES))}
  </div>
  <div class="container ds-line-wrap">
    <nav class="ds-line" aria-label="Proceslijn: kies een onderwerp" data-ds-line>
      <span class="ds-line__origin" data-sig-origin aria-hidden="true"><i></i></span>
      <span class="ds-line__track" aria-hidden="true"><span class="ds-line__fill" data-ds-fill></span><span class="ds-line__grains">{grains}</span></span>
      <ol class="ds-line__st">{"".join(stations)}</ol>
      <button class="ds-play" type="button" data-ds-play aria-pressed="false" aria-label="Animatie pauzeren">
        <svg class="ds-play__ring" viewBox="0 0 44 44" aria-hidden="true"><circle cx="22" cy="22" r="20.5"/><circle class="ds-play__clock" cx="22" cy="22" r="20.5" pathLength="100"/></svg>
        {icon("pause", attrs=' data-ds-icon-pause')}{icon("play", attrs=' data-ds-icon-play hidden')}
      </button>
    </nav>
  </div>
</section>
<script src="{_v("assets/js/granule-flow.js")}" defer></script>
<script src="{_v("assets/js/doorstroom.js")}" defer></script>'''
