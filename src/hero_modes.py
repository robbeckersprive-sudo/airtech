"""Switchable flow pictures for the Doorstroom hero sheets (Nov 20).

Each sheet whose process has two telling states gets the same instrument as the tube on sheet 1 ("Stromingsbeeld"):
  1 Filtratie   Filteren / Afreinigen   dust builds a cake on the cartridges / an air pulse knocks it off into the cone
  3 Cyclonen    Grof / Fijn             coarse product spirals down to the outlet / part of the fines follows the air up
                                        the vortex finder (why a filter often follows a cyclone)
  4 Doseren     Laag / Hoog toerental   the photographed rotor really turns (assets/js/doorstroom.js drives the angle);
                                        pockets fill under the inlet and empty at the outlet
Wissels gets none: the flap is fixed in the photo, so a route switch would contradict the picture.
All drawings are in the 570 x 380 units of the 3:2 slide photos. Group .fx-a / .fx-b is shown by the slide's
data-mode (a | b), see top.css. Copy: general process knowledge, no product claims."""
from math import cos, sin, tau, radians
import random
from slide_flow import moving_grains
from components import _v

GOLD = ('<radialGradient id="{n}-gold" cx=".32" cy=".26" r=".77"><stop stop-color="#fff0c8"/>'
        '<stop offset=".5" stop-color="#e9bd60"/><stop offset="1" stop-color="#a66c1f"/></radialGradient>')

# ---------------------------------------------------------------- instrument copy per sheet
SHEET_MODES = {
    0: ('Stromingsbeeld', 'Beweeg over de leiding', [
        ('dense', 'Dichte fase', 'Product schuift langzaam als bed of prop door de leiding. Weinig lucht, weinig slijtage.'),
        ('dilute', 'Verdunde fase', 'Product zweeft snel in de luchtstroom. Veel lucht, eenvoudig en flexibel.')]),
    1: ('Filterbedrijf', None, [
        ('a', 'Filteren', 'Stofbeladen lucht stroomt door de patronen. Het stof blijft als koek op het filtermedium achter.'),
        ('b', 'Afreinigen', 'Een luchtpuls blaast de koek van de patronen. Het product valt terug in de conus.')]),
    3: ('Deeltjesgrootte', None, [
        ('a', 'Grof', 'Grove deeltjes worden tegen de wand geslingerd en zakken via de conus naar de uitlaat.'),
        ('b', 'Fijn', 'De fijnste deeltjes volgen deels de lucht omhoog door de dompelbuis. Daarom volgt vaak een filter.')]),
    4: ('Toerental', None, [
        ('a', 'Laag', 'Elk vak neemt een vast volume mee. Een laag toerental geeft een rustige, kleine stroom.'),
        ('b', 'Hoog', 'Dezelfde vakken, vaker per minuut: de doseercapaciteit stijgt mee met het toerental.')]),
}


def _svg(name, body, defs='', clip=None):
    cp = f'<clipPath id="{name}-window"><path clip-rule="evenodd" d="{clip}"/></clipPath>' if clip else ''
    g = f'<g clip-path="url(#{name}-window)">{body}</g>' if clip else body
    return (f'<svg class="hero__flow ds-fx" data-flow-svg viewBox="0 0 570 380" aria-hidden="true" focusable="false">'
            f'<defs>{GOLD.format(n=name)}{cp}{defs}</defs>{g}</svg>')


def _air(d, dur=1.0, extra=''):
    return (f'<path d="{d}" fill="none" stroke="#bdd9ed" stroke-width="1.25" opacity=".72" stroke-dasharray="4 13"{extra}>'
            f'<animate attributeName="stroke-dashoffset" from="0" to="-17" dur="{dur}s" repeatCount="indefinite"/></path>')


def _grains(name, lanes, fade=True):
    guides, grains = moving_grains(name, lanes)
    if not fade:
        grains = grains.replace('values="0;.95;.95;0"', 'values=".95;.95"').replace('keyTimes="0;.08;.9;1"', 'keyTimes="0;1"')
    return guides, grains


# ---------------------------------------------------------------- 1 Filtratie
CARTRIDGES = ((348, 17), (392, 25), (442, 17))     # centre x, half width; top y 84, bottom y 200 (photo units)


def filter_modes():
    name = 'ffx'
    window = 'M313 91 Q382 72 466 83 L467 267 L313 269 Z'
    # A: dusty air rises from the cone into the cartridges, clean air leaves at the top, the cake grows
    lanes_a, air_a, cake = [], [], []
    for i, (cx, hw) in enumerate(CARTRIDGES):
        for k, dx in enumerate((-hw - 6, -hw * .3, hw * .4, hw + 6)):
            lanes_a.append((f'M{cx + dx * .3:.0f} 266 Q{cx + dx * .8:.0f} 236 {cx + dx:.0f} {196 - (k % 2) * 30}', 9, 2.6 + .2 * k, .7))
        air_a.append(_air(f'M{cx} 190 L{cx} 88', 1.2))
        cake.append(f'<rect class="ffx-cake" x="{cx - hw}" y="86" width="{2 * hw}" height="114" rx="3">'
                    f'<animate attributeName="opacity" values=".02;.34;.34;.02" keyTimes="0;.86;.96;1" dur="9s" repeatCount="indefinite"/></rect>')
    ga, pa = _grains(name + 'a', lanes_a)
    # B: a pulse runs down each cartridge in turn and the cake falls into the cone
    lanes_b, pulses = [], []
    for i, (cx, hw) in enumerate(CARTRIDGES):
        for k, dx in enumerate((-hw - 3, -hw * .5, 0, hw * .5, hw + 3)):
            lanes_b.append((f'M{cx + dx:.0f} {110 + 18 * (k % 3)} Q{cx + dx * 1.1:.0f} 210 {cx + dx * .55:.0f} 268', 6, 1.5 + .12 * k, 1.05))
        begin = f'{-i * .8:.1f}s'
        pulses.append(
            f'<g class="ffx-pulse"><ellipse cx="{cx}" cy="86" rx="{hw}" ry="4" fill="#fff" opacity="0">'
            f'<animate attributeName="opacity" values="0;.9;0;0" keyTimes="0;.06;.3;1" dur="2.4s" begin="{begin}" repeatCount="indefinite"/></ellipse>'
            f'<path d="M{cx} 86 L{cx} 200" stroke="#fff" stroke-width="2.2" stroke-linecap="round" fill="none" stroke-dasharray="26 200" stroke-dashoffset="26" opacity=".9">'
            f'<animate attributeName="stroke-dashoffset" values="26;-114;-114" keyTimes="0;.22;1" dur="2.4s" begin="{begin}" repeatCount="indefinite"/></path></g>')
    gb, pb = _grains(name + 'b', lanes_b)
    body = (f'<g class="fx-a">{"".join(cake)}{"".join(air_a)}{pa}</g>'
            f'<g class="fx-b">{"".join(pulses)}{pb}</g>')
    defs = ga + gb + GOLD.format(n=name + 'a') + GOLD.format(n=name + 'b')
    return _svg(name, body, defs, window)


# ---------------------------------------------------------------- 3 Cyclonen
def _spiral(lane, t0=0., t1=1.):
    pts = []
    for step in range(121):
        t = t0 + (t1 - t0) * step / 120
        r = min(77, 8 + 100 * (1 - t)) - lane * .8
        a = tau * (2.85 * t + .5 + lane * .015)
        pts.append(f'{391 + 6 * t + r * cos(a):.2f},{90 + 243 * t + .14 * r * sin(a) + lane:.2f}')
    return 'M ' + ' L '.join(pts)


def _escape(lane):
    """From the lower cone, a tight inner vortex rises to the vortex finder (dompelbuis, bottom at y ~ 130)."""
    pts = []
    for step in range(81):
        s = step / 80
        r = 26 * (1 - s) + 9
        a = tau * (1.9 * s + lane * .5)
        pts.append(f'{398 + r * cos(a):.2f},{236 - 104 * s + .14 * r * sin(a):.2f}')
    return 'M ' + ' L '.join(pts)


def cyclone_modes():
    name = 'cfx'
    window = ('M316 86 Q382 61 465 75 L465 146 L408 334 L381 334 L316 160 Z '
              'M374 72 L374 126 Q400 141 429 127 L429 69 Z')
    air = ''.join(_air('M396 267 C371 243 414 229 397 208 S382 184 399 167 S408 143 398 126', 1.2, f' transform="translate({o} 0)"')
                  for o in (-3, 3))
    lanes_a = [(_spiral(l), 24, 4.7 + l * .16, 1.25) for l in range(5)]
    lanes_b = [(_spiral(l), 34, 3.4 + l * .12, .62) for l in range(5)]
    lanes_up = [(_escape(l), 12, 2.6 + l * .3, .55) for l in range(2)]
    ga, pa = _grains(name + 'a', lanes_a, fade=False)
    gb, pb = _grains(name + 'b', lanes_b, fade=False)
    gu, pu = _grains(name + 'u', lanes_up)
    defs = ga + gb + gu + ''.join(GOLD.format(n=name + k) for k in 'abu')
    body = f'{air}<g class="fx-a">{pa}</g><g class="fx-b">{pb}{pu}</g>'
    return _svg(name, body, defs, window)


# ---------------------------------------------------------------- 4 Doseren
# Rotor ellipse (perspective) in photo units; the texture comes from tools/rotor_texture.py (glare removed).
ROTOR = dict(cx=306, cy=184.5, rx=79, ry=98, k=.81)
POCKETS = (27, 67, 106, 149, 192, 236, 281, 333)    # pocket centres, degrees clockwise from the top (unsquashed)


def dosing_modes():
    rnd = random.Random(11)
    cx, cy, k = ROTOR['cx'], ROTOR['cy'], ROTOR['k']
    pockets = []
    for th in POCKETS:
        dots = []
        for _ in range(16):
            r = rnd.uniform(50, 90)
            a = radians(th + rnd.uniform(-15, 15) * (60 / r))
            dots.append(f'<circle cx="{r * sin(a):.1f}" cy="{-r * cos(a):.1f}" r="{rnd.uniform(2.1, 3.1):.1f}" fill="url(#dfx-gold)"/>')
        pockets.append(f'<g class="dfx-pocket" data-pocket="{th}" opacity="0">{"".join(dots)}</g>')
    defs = (f'<clipPath id="dfx-clip"><ellipse cx="{cx}" cy="{cy}" rx="{ROTOR["rx"]}" ry="{ROTOR["ry"]}"/></clipPath>'
            '<radialGradient id="dfx-feather" cx=".5" cy=".5" r=".5"><stop offset=".55" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>'
            '<mask id="dfx-glare"><ellipse cx="258" cy="117" rx="34" ry="30" fill="url(#dfx-feather)"/>'
            '<ellipse cx="243" cy="150" rx="14" ry="26" fill="url(#dfx-feather)"/></mask>')
    body = f'''<g clip-path="url(#dfx-clip)"><g transform="translate({cx} {cy}) scale({k} 1)"><g data-rotor-spin>
        <g transform="scale({1 / k:.4f} 1) translate({-cx} {-cy})"><image href="{_v('images/33-hero-doseersluis-rotor.webp')}" x="225" y="84.5" width="162" height="200" preserveAspectRatio="none"/></g>
        {"".join(pockets)}</g></g></g>
      <g mask="url(#dfx-glare)"><image href="images/33-hero-doseersluis-1200.webp" width="570" height="380" opacity=".7"/></g>'''
    return (f'<svg class="hero__flow ds-fx ds-rotor" viewBox="0 0 570 380" aria-hidden="true" focusable="false" data-rotor>'
            f'<defs>{GOLD.format(n="dfx")}{defs}</defs>{body}</svg>')


EFFECTS = {'30-hero-filter': filter_modes, '32-hero-cycloon': cyclone_modes, '33-hero-doseersluis': dosing_modes}
