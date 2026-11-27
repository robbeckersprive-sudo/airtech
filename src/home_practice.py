"""Home blocks 4 and 5 (Nov 21). Styles appended to assets/css/home-blocks.css ("BLOCK 4" / "BLOCK 5"),
behaviour assets/js/home-practice.js.

Block 4 "Projectdossier" (#projecten) — all five real projects (project_data.PROJECTS, facts from the original
airtechnicsolutions.nl cases) instead of two tabs with a title. The illustration fills the steel band and fades into it;
a project changes behind the red scan line; its hard facts are set as large readings that count up. A dossier index with
thumbnails picks the project (tabs, arrow keys); phones swipe the picture.

Block 5 "Van tekening tot installatie" (#steps-title) — the four steps are all readable (no hidden tab panels). A sticky
sheet shows the step under the reading line: first as a blueprint drawing of its photo (tools/drawing_versions.py),
then scrolling plots the real photo over it behind the scan line. A rail with four nodes fills as you read.
Phones: each step carries its own sheet, plotted by its own scroll position."""
import re
from components import pic, icon, link, checklist, contact_url, split_lines, _v
from project_data import PROJECTS

# ---------------------------------------------------------------- block 4
ORDER = ['pet-recycling', 'driessen-food-extrusion', 'centraal-stofzuigsysteem', 'dierenvoeding', 'eischaalverwerking']


def _count_attrs(value):
    """'≈ 1,1 t/u' -> data-count="1.1" data-dec="1" data-pre="≈ " data-suf=" t/u"; non-numbers are not counted."""
    m = re.fullmatch(r'(≈\s*)?(\d{1,3}(?:\.\d{3})*|\d+)(?:,(\d+))?(\s.*)?', value)
    if not m or '×' in value:
        return ''
    whole = m.group(2).replace('.', '')
    dec = m.group(3) or ''
    num = whole + ('.' + dec if dec else '')
    return (f' data-count="{num}" data-dec="{len(dec)}" data-pre="{m.group(1) or ""}" data-suf="{m.group(4) or ""}"')


def _value(value):
    """Big number, smaller unit: '18.000 m³/u' -> 18.000<small> m³/u</small>."""
    m = re.fullmatch(r'(≈\s*)?([\d.,]+)(\s.*)?', value)
    if not m or '×' in value:
        return f'<span class="pd-fact__word{" pd-fact__word--num" if "×" in value else ""}">{value}</span>'
    pre = f'<small class="pd-fact__pre">{m.group(1).strip()}</small>' if m.group(1) else ''
    suf = f'<small>{m.group(3)}</small>' if m.group(3) else ''
    return f'{pre}<span data-pd-num>{m.group(2)}</span>{suf}'


def _sector_chip(sector):
    """Sector label links to its sector page (Nov 27) when one exists; same chip markup otherwise."""
    from sector_data import SECTORS, sector_file
    slug = next((k for k, v in SECTORS.items() if v['project_sector'] == sector), None)
    return f'<a class="pd-sector__link" href="{sector_file(slug)}"><span>{sector}</span></a>' if slug else f'<span>{sector}</span>'


def dossier_block():
    n = len(ORDER)
    imgs, copies, tabs = [], [], []
    for i, slug in enumerate(ORDER):
        p = PROJECTS[slug]
        on = i == 0
        off = '' if on else ' aria-hidden="true" inert'
        imgs.append(f'<div class="pd-img{" is-on" if on else ""}" data-pd-img>{pic(p["image"], "", "(min-width: 900px) 64vw, 100vw", eager=False)}</div>')
        facts = ''.join(f'<div class="pd-fact"><dt>{label}</dt><dd{_count_attrs(val)}>{_value(val)}</dd></div>' for val, label in p['facts'][:4])
        copies.append(f'''<div class="pd-copy{" is-on" if on else ""}" id="pd-{slug}" role="tabpanel" aria-labelledby="pd-tab-{i}" data-pd-copy{off}>
          <p class="pd-sector">{_sector_chip(p["sector"])}{p["category"]}</p>
          <h3 class="pd-title">{split_lines(p["title"])}</h3>
          <p class="pd-lead">{p["lead"]}</p>
          <dl class="pd-facts" style="--n:{len(p["facts"][:4])}">{facts}</dl>
          <dl class="pd-meta"><div><dt>Opdrachtgever</dt><dd>{p["client"]}</dd></div><div><dt>Materiaal</dt><dd>{p["material"]}</dd></div><div><dt>Scope</dt><dd>{p["scope"]}</dd></div></dl>
          <div class="pd-actions">{link("Bekijk het project", f"project-{slug}.html", "ur", "pd-link pd-link--main")}{link("Alle projecten", "projecten.html", "ur", "pd-link")}</div>
        </div>''')
        tabs.append(f'<button class="pd-tab" type="button" role="tab" id="pd-tab-{i}" aria-controls="pd-{slug}" aria-selected="{str(on).lower()}" tabindex="{0 if on else -1}" data-pd-tab="{i}">'
                    f'<span class="pd-tab__img" aria-hidden="true"><img src="images/{p["image"]}-480.webp" alt="" width="480" height="320" loading="lazy" decoding="async"></span>'
                    f'<span class="pd-tab__txt"><span class="pd-tab__no">{i + 1:02d} · {p["sector"]}</span><span class="pd-tab__name">{p["short"]}</span></span>'
                    f'<i class="pd-tab__bar" aria-hidden="true"></i></button>')
    return f'''<section id="projecten" data-theme="forest" class="pd" aria-labelledby="pd-title" data-sig-label="Praktijk" data-pd>
  <div class="pd-stage" aria-hidden="true" data-pd-stage>{"".join(imgs)}<i class="pd-scan"></i><span class="pd-caption">Beeld: technische projectillustratie</span></div>
  <div class="pd-veil" aria-hidden="true"></div>
  <div class="container pd-in">
    <h2 id="pd-title" class="pd-kicker"><span class="pd-kicker__dot" aria-hidden="true"></span>Uit de praktijk <span class="pd-kicker__count" aria-hidden="true"><b data-pd-count>01</b> / {n:02d}</span></h2>
    <div class="pd-copies">{"".join(copies)}</div>
  </div>
  <div class="container pd-index-wrap">
    <div class="pd-index" role="tablist" aria-label="Kies een project">{"".join(tabs)}</div>
  </div>
</section>'''


# ---------------------------------------------------------------- block 5
def werkwijze_block(steps):
    """steps: the list from pages.home(): (name, image, alt, copy dict)."""
    n = len(steps)
    shots, items = [], []
    for i, (name, img, alt, copy) in enumerate(steps):
        def sheet(sizes):
            return (f'<span class="wk-dr">{pic(img + "-tekening", "", sizes)}</span>'
                    f'<span class="wk-ph">{pic(img, alt, sizes)}</span>')
        shots.append(f'<div class="wk-shot{" is-on" if i == 0 else ""}" data-wk-shot>{sheet("(min-width: 900px) 52vw, 1px")}</div>')
        cta = link(copy['link'], contact_url('installatieontwerp'), 'ur', 'wk-link') if 'link' in copy else ''
        items.append(f'''<li class="wk-step" style="--i:{i}" data-wk-step>
          <span class="wk-node" aria-hidden="true"><i></i>{i + 1:02d}</span>
          <div class="wk-mshot" aria-hidden="true">{sheet("(max-width: 899px) 92vw, 1px")}<i class="wk-scan"></i></div>
          <p class="wk-name">{name}</p>
          <h3 class="wk-title">{copy["title"]}</h3>
          <p class="wk-text">{copy["text"]}</p>
          <div class="wk-cols">
            <div><h4 class="wk-h4">Wat u krijgt</h4>{checklist(copy["deliverables"])}</div>
            <div><h4 class="wk-h4">In deze fase</h4><p>{copy["fase"]}</p>{cta}</div>
          </div>
        </li>''')
    names = ''.join(f'<span data-wk-label>{name}</span>' for name, *_ in steps)
    reg = ''.join(f'<i class="sx-reg sx-reg--{c}"></i>' for c in ('tl', 'tr', 'bl', 'br'))
    return f'''<section class="section--home wk" aria-labelledby="steps-title" data-wk>
  <div class="container">
    <div class="wk-head">
      <h2 id="steps-title" class="h2" data-split>{split_lines("Van procesanalyse naar<br><em>werkende installatie.</em>")}</h2>
      <p class="wk-intro">Eén technisch aanspreekpunt voor industriële luchttechniek en bulkverwerking, van ontwerp tot inbedrijfstelling.</p>
    </div>
    <div class="wk-body">
      <div class="wk-visual" aria-hidden="true">
        <div class="wk-frame">{"".join(shots)}<i class="wk-scan"></i>{reg}
          <div class="wk-block"><span class="wk-block__sheet">Blad <b data-wk-no>01</b> / {n:02d}</span><span class="wk-block__names">{names}</span>
            <span class="wk-block__state"><span class="wk-block__dr">Tekening</span><i class="wk-block__bar"><b></b></i><span class="wk-block__ph">Installatie</span></span></div>
        </div>
      </div>
      <ol class="wk-steps" data-wk-steps><i class="wk-rail" aria-hidden="true"><b data-wk-rail></b></i>{"".join(items)}</ol>
    </div>
  </div>
</section>
<script src="{_v("assets/js/home-practice.js")}" defer></script>'''
