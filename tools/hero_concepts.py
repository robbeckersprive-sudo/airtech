"""Generate three hero + transition concepts as review pages next to the live homepage.

    python tools/hero_concepts.py

Reads the built index.html, keeps the hero markup (photo stage, granule canvas, hotspots) intact and wraps or extends
it per concept, then adds assets/css/hero-concepts.css + assets/js/hero-concepts.js. Output:
    hero-a.html   A  "Inzoomen"   pinned camera dolly into the stream; the content rises over it as a sheet
    hero-b.html   B  "Tekenblad"  the full-bleed photo folds into a framed drawing plate; the hero becomes a split layout
    hero-c.html   C  "Stroomlijn" no pin: a forest band whose curved edge follows the pipe, disciplines run along it
The live index.html is not touched.

SUPERSEDED (Nov 20): concept B is now the live hero (see README "Hero Tekenblad"); running this on the current
build would wrap the hero twice. Kept for reference.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from components import OPLOSSINGEN  # noqa: E402

DISCIPLINES = [n for _, items in OPLOSSINGEN for n, _h in items]

CONCEPTS = {'a': 'Inzoomen', 'b': 'Tekenblad', 'c': 'Stroomlijn'}


def concept_a(hero, specs):
    hero = hero.replace('<section class="hero"', '<section class="hero hcA-hero"', 1)
    specs = specs.replace('<section class="section--home"', '<section class="section--home hc-sheet"', 1)
    return f'<div class="hcA" data-hc-track>\n{hero}\n</div>', specs


def concept_b(hero, specs):
    plate = '''<div class="hcB-plate" aria-hidden="true">
    <i class="hcB-ruler hcB-ruler--x"></i><i class="hcB-ruler hcB-ruler--y"></i>
    <i class="hcB-reg hcB-reg--tl"></i><i class="hcB-reg hcB-reg--tr"></i><i class="hcB-reg hcB-reg--bl"></i><i class="hcB-reg hcB-reg--br"></i>
    <dl class="hcB-title">
      <div><dt>Project</dt><dd>Proceslijn</dd></div>
      <div><dt>Discipline</dt><dd>Pneumatisch transport</dd></div>
      <div><dt>Blad</dt><dd>01</dd></div>
    </dl>
  </div>'''
    hero = hero.replace('<section class="hero"', '<section class="hero hcB-hero"', 1)
    hero = hero.replace('<div class="hero__veil"', plate + '\n  <div class="hero__veil"', 1)
    specs = specs.replace('<section class="section--home"', '<section class="section--home hcB-next"', 1)
    return f'<div class="hcB" data-hc-track>\n{hero}\n</div>', specs


def concept_c(hero, specs):
    words = ''.join(f'<tspan>{d}</tspan><tspan class="hcC-dot"> • </tspan>' for d in DISCIPLINES)
    edge = f'''<div class="hcC-edge" aria-hidden="true" data-hc-curve>
    <svg class="hcC-svg" xmlns="http://www.w3.org/2000/svg">
      <path class="hcC-fill" data-hc-fill/>
      <path class="hcC-line" id="hcC-path" data-hc-line/>
      <text class="hcC-text" dy="26"><textPath href="#hcC-path" data-hc-text>{words * 3}</textPath></text>
    </svg>
  </div>'''
    hero = hero.replace('<section class="hero"', '<section class="hero hcC-hero"', 1)
    specs = specs.replace('<section class="section--home"', '<section class="section--home hcC-next" data-theme="forest"', 1)
    specs = specs.replace('<div class="container specs">', edge + '\n  <div class="container specs">', 1)
    specs = specs.replace('<article class="spec">', '<article class="spec" data-theme="light">')  # light cards keep their own ink on the band
    return hero, specs


BUILDERS = {'a': concept_a, 'b': concept_b, 'c': concept_c}


def switcher(cur):
    opts = ''.join(f'<a href="hero-{k}.html"{" aria-current=page" if k == cur else ""}><b>{k.upper()}</b><span>{n}</span></a>'
                   for k, n in CONCEPTS.items())
    return (f'<div class="hx-review" role="navigation" aria-label="Heroconcepten (review)"><span class="hx-review__t">Hero</span>'
            f'{opts}<span class="hx-review__sep"></span><a href="index.html">Huidig</a></div>')


def main():
    if 'data-hero-track' in open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read():
        sys.exit('index.html already has the Tekenblad hero; these concepts were built from the earlier hero.')
    v = lambda p: int(os.path.getmtime(os.path.join(ROOT, p)))  # noqa: E731
    html = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    hm = re.search(r'<section class="hero".*?</section>', html, re.S)
    sm = re.search(r'<section class="section--home" id="specialisaties".*?</section>', html, re.S)
    assert hm and sm and hm.end() < sm.start()
    gap = html[hm.end():sm.start()]
    for k, fn in BUILDERS.items():
        # the transition surface must be solid from the first frame: no section-level fade (headings keep their reveal)
        hero, specs = fn(hm.group(0), sm.group(0).replace(' data-reveal>', '>', 1))
        out = html[:hm.start()] + hero + gap + specs + html[sm.end():]
        out = out.replace('<html lang="nl"', f'<html lang="nl" data-hero-concept="{k}"', 1)
        out = re.sub(r'(<link rel="stylesheet" href="assets/css/site\.css[^"]*">)',
                     rf'\1\n<link rel="stylesheet" href="assets/css/hero-concepts.css?v={v("assets/css/hero-concepts.css")}">', out, count=1)
        out = re.sub(r'(<script src="assets/js/site\.js[^"]*" defer></script>)',
                     rf'\1\n<script src="assets/js/hero-concepts.js?v={v("assets/js/hero-concepts.js")}" defer></script>', out, count=1)
        out = out.replace('</head>', '<meta name="robots" content="noindex">\n</head>', 1)
        out = out.replace('</body>', switcher(k) + '\n</body>', 1)
        with open(os.path.join(ROOT, f'hero-{k}.html'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(out)
        print('wrote', f'hero-{k}.html')


if __name__ == '__main__':
    main()
