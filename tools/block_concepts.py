"""Generate three variants of homepage block 2 ("Twee specialisaties") as review pages.

    python tools/block_concepts.py

Reads the built index.html, replaces the #specialisaties section and adds assets/css/block-concepts.css +
assets/js/block-concepts.js. The hero/header are the live ones, so the scroll hand-off can be judged for real.
    block-a.html  A  "Processchema"  a process line drops from the hero plate's edge, splits at a T into the two
                                     disciplines; P&ID symbols per item; a granule rides the drawn tip
    block-b.html  B  "Aanzichten"    one plate splits along a dash-dot centre line into view A and view B
    block-c.html  C  "Stuklijst"     a parts list beside a sticky plate in the hero plate's position; the row in the
                                     middle of the screen drives the figure and the title block
Copy is the site's own; nothing new is claimed. The live index.html is not touched.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from components import icon, pic, SOL_IMG, _slug  # noqa: E402

DISC = [
    ('A', 'Industriële luchttechniek', 'Schone, veilige en efficiënte luchtoplossingen voor uw proces.',
     ['Stofafzuiging', 'Filtratie', 'Hoogvacuüm']),
    ('B', 'Solids processing', 'Betrouwbaar en gecontroleerd omgaan met poeders en granulaten.',
     ['Pneumatisch transport', 'Doseren', 'Zeven en scheiden', 'Opslaan']),
]
CUTOUT = {'26-multicycloon', '15-doseersluis-doorsnede', '10-zeef-vrijstaand', '08-bigbag-vrijstaand'}

# Simplified process-flow symbols (after ISO 10628), drawn on a 24px grid, 1.5px stroke.
SYM = {
    'Stofafzuiging': '<path d="M7 4h10v5l-3.5 8h-3L7 9z"/><path d="M10.5 17v3h3v-3M17 6.5h4"/>',
    'Filtratie': '<rect x="5" y="4" width="14" height="16" rx="1"/><path d="M5.5 19.5 18.5 4.5" stroke-dasharray="2 2"/>',
    'Hoogvacuüm': '<circle cx="12" cy="12" r="7.5"/><path d="M8.5 6.8 19.3 12 8.5 17.2"/>',
    'Pneumatisch transport': '<path d="M3 12h15M15 8.5l3.5 3.5-3.5 3.5"/><circle cx="6.5" cy="9" r="1.1"/><circle cx="10" cy="15" r="1.1"/><circle cx="12.5" cy="9.5" r="1.1"/>',
    'Doseren': '<circle cx="12" cy="12" r="7.5"/><path d="M12 4.5v15M4.5 12h15M6.7 6.7l10.6 10.6M17.3 6.7 6.7 17.3"/>',
    'Zeven en scheiden': '<rect x="4" y="6" width="16" height="12" rx="1"/><path d="M4.5 12h15" stroke-dasharray="2 2"/><path d="M9 18v2.5M15 18v2.5"/>',
    'Opslaan': '<path d="M6 3h12v11l-4 5.5h-4L6 14z"/><path d="M6 14h12M10 19.5v1.5h4v-1.5"/>',
    'A': '<circle cx="12" cy="12" r="7.5"/><path d="M12 12 9 5.6M12 12l6.6 2.4M12 12l-3.6 6.3"/>',
    'B': '<path d="M6 3h12v11l-4 5.5h-4L6 14z"/><path d="M6 14h12"/>',
}


def sym(name, cls='sym'):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" '
            f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{SYM[name]}</svg>')


def figs(items, sizes):
    out = []
    for i, n in enumerate(items):
        img = SOL_IMG[n]
        cut = ' fig__img--cut' if img in CUTOUT else ''
        out.append(f'<div class="fig__img{cut}{" is-on" if i == 0 else ""}" data-fig-img="{_slug(n)}" data-cap="{n}">{pic(img, "", sizes)}</div>')
    return ''.join(out)


REG = ''.join(f'<i class="reg reg--{c}" aria-hidden="true"></i>' for c in ('tl', 'tr', 'bl', 'br'))


def item_link(n, extra=''):
    return f'<a href="#" data-fig="{_slug(n)}"{extra}>{sym(n)}<span>{n}</span>{icon("ur")}</a>'


# ================================================================= A  Processchema
def variant_a(h2):
    cols = []
    for key, title, text, items in DISC:
        lis = ''.join(f'<li>{item_link(n)}</li>' for n in items)
        cols.append(f'''<article class="blkA-disc" data-disc>
        <div class="blkA-disc__top"><span class="blkA-node" data-blk-node>{sym(key, "sym sym--node")}</span>
          <div><h3 class="h3">{title}</h3><p>{text}</p></div></div>
        <figure class="fig blkA-fig" data-fig-frame>{figs(items, "(min-width: 960px) 34vw, 92vw")}{REG}
          <figcaption><span data-fig-cap>{items[0]}</span><span>{title}</span></figcaption></figure>
        <ul class="blkA-list">{lis}</ul>
      </article>''')
    return f'''<section class="section--home section--ruled blk blk--a" id="specialisaties" aria-labelledby="spec-title" data-blk="a">
  <svg class="blkA-line" aria-hidden="true" focusable="false" data-blk-line>
    <path class="blkA-line__base" data-line-base="0"/><path class="blkA-line__base" data-line-base="1"/>
    <path class="blkA-line__flow" data-line-flow="0"/><path class="blkA-line__flow" data-line-flow="1"/>
    <circle class="blkA-line__granule" r="4.5" data-line-granule="0"/><circle class="blkA-line__granule" r="4.5" data-line-granule="1"/>
  </svg>
  <div class="container blkA">
    <div class="blkA__head">{h2}</div>
    <div class="blkA__cols">{"".join(cols)}</div>
  </div>
</section>'''


# ================================================================= B  Aanzichten
def variant_b(h2):
    views = []
    for key, title, text, items in DISC:
        lis = ''.join(f'<li>{item_link(n)}</li>' for n in items)
        views.append(f'''<article class="blkB-view" data-disc>
        <figure class="fig blkB-fig" data-fig-frame>{figs(items, "(min-width: 960px) 44vw, 92vw")}{REG}
          <i class="blkB-ruler" aria-hidden="true"></i>
          <figcaption><span>Aanzicht {key}</span><span data-fig-cap>{items[0]}</span></figcaption></figure>
        <h3 class="h3">{title}</h3><p>{text}</p>
        <ul class="blkB-list">{lis}</ul>
      </article>''')
    return f'''<section class="section--home section--ruled blk blk--b" id="specialisaties" aria-labelledby="spec-title" data-blk="b">
  <div class="container blkB">
    <div class="blkB__head">{h2}</div>
    <div class="blkB__views" data-blk-split>
      <div class="blkB-merge" aria-hidden="true">{pic("02-pijpleiding-contact", "", "(min-width: 960px) 90vw, 100vw")}</div>
      <i class="blkB-center" aria-hidden="true"></i>
      {"".join(views)}
    </div>
  </div>
</section>'''


# ================================================================= C  Stuklijst
def variant_c(h2):
    groups, all_items = [], []
    for key, title, text, items in DISC:
        grp = f' data-pos="{key}"'
        rows = ''.join(f'<li class="blkC-row" data-row><span class="blkC-pos">{key}{i + 1}</span>{item_link(n, grp)}</li>'
                       for i, n in enumerate(items))
        groups.append(f'''<div class="blkC-group">
        <div class="blkC-group__head">{sym(key, "sym sym--node")}<div><h3 class="h3">{title}</h3><p>{text}</p></div></div>
        <ol class="blkC-rows">{rows}</ol>
      </div>''')
        all_items += items
    return f'''<section class="section--home section--ruled blk blk--c" id="specialisaties" aria-labelledby="spec-title" data-blk="c">
  <div class="container blkC">
    <div class="blkC__list">
      {h2}
      <div class="blkC-legend" aria-hidden="true"><span>Pos.</span><span>Onderdeel</span></div>
      {"".join(groups)}
    </div>
    <div class="blkC__aside">
      <figure class="fig blkC-fig" data-fig-frame>{figs(all_items, "(min-width: 960px) 40vw, 1px")}{REG}
        <i class="blkC-ruler blkC-ruler--x" aria-hidden="true"></i><i class="blkC-ruler blkC-ruler--y" aria-hidden="true"></i>
        <dl class="blkC-title" aria-hidden="true">
          <div><dt>Pos.</dt><dd data-fig-pos>A1</dd></div>
          <div><dt>Onderdeel</dt><dd data-fig-cap>{all_items[0]}</dd></div>
          <div><dt>Blad</dt><dd>02</dd></div>
        </dl>
      </figure>
    </div>
  </div>
</section>'''


VARIANTS = {'a': ('Processchema', variant_a), 'b': ('Aanzichten', variant_b), 'c': ('Stuklijst', variant_c)}


def switcher(cur):
    opts = ''.join(f'<a href="block-{k}.html"{" aria-current=page" if k == cur else ""}><b>{k.upper()}</b><span>{n}</span></a>'
                   for k, (n, _) in VARIANTS.items())
    return (f'<div class="hx-review" role="navigation" aria-label="Blokvarianten (review)"><span class="hx-review__t">Blok 2</span>'
            f'{opts}<span class="hx-review__sep"></span><a href="index.html#specialisaties">Huidig</a></div>')


def main():
    if 'data-process' in open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read():
        sys.exit('index.html already has the Processchema block; these variants were built from the earlier block.')
    v = lambda p: int(os.path.getmtime(os.path.join(ROOT, p)))  # noqa: E731
    html = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    m = re.search(r'<section class="section--home section--ruled" id="specialisaties".*?</section>', html, re.S)
    h2 = re.search(r'<h2 id="spec-title".*?</h2>', m.group(0), re.S).group(0)
    for k, (_n, fn) in VARIANTS.items():
        out = html[:m.start()] + fn(h2) + html[m.end():]
        out = out.replace('<html lang="nl"', f'<html lang="nl" data-block-variant="{k}"', 1)
        out = re.sub(r'(<link rel="stylesheet" href="assets/css/site\.css[^"]*">)',
                     rf'\1\n<link rel="stylesheet" href="assets/css/block-concepts.css?v={v("assets/css/block-concepts.css")}">', out, count=1)
        out = re.sub(r'(<script src="assets/js/site\.js[^"]*" defer></script>)',
                     rf'\1\n<script src="assets/js/block-concepts.js?v={v("assets/js/block-concepts.js")}" defer></script>', out, count=1)
        out = out.replace('</head>', '<meta name="robots" content="noindex">\n</head>', 1)
        out = out.replace('</body>', switcher(k) + '\n</body>', 1)
        with open(os.path.join(ROOT, f'block-{k}.html'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(out)
        print('wrote', f'block-{k}.html')


if __name__ == '__main__':
    main()
