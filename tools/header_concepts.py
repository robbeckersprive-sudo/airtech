"""Generate the three header concepts as review pages next to the live build.

    python tools/header_concepts.py

Reads the built index.html and cycloonafscheider.html, swaps the <header> for a concept header and adds
assets/css/header-concepts.css + assets/js/header-concepts.js. Output:
    concept-a.html / concept-a-product.html   A  "Capsule"   morphing island + shared morphing dropdown
    concept-b.html / concept-b-product.html   B  "Doorsnede" instrument bar: rail, ruler, figure drawer
    concept-c.html / concept-c-product.html   C  "Index"     split chips + full-screen index menu
The live pages are not touched.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
import components as C  # noqa: E402
from components import (icon, pic, btn_icon, LOGO_MARK, OPLOSSINGEN, COMPONENTEN,  # noqa: E402
                        PHONE_TEL, PHONE_DISPLAY, EMAIL, ADDRESS, ORG)

SOL_IMG = {
    'Stofafzuiging': '26-multicycloon',
    'Filtratie': '17-filter-macro',
    'Hoogvacuüm': '18-blower-macro',
    'Pneumatisch transport': '02-pijpleiding-contact',
    'Doseren': '15-doseersluis-doorsnede',
    'Zeven en scheiden': '10-zeef-vrijstaand',
    'Opslaan': '08-bigbag-vrijstaand',
}
SOLUTIONS_HREF = 'index.html#specialisaties'
N_SOL = sum(len(i) for _, i in OPLOSSINGEN)
N_COMP = len(COMPONENTEN)


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower().replace('&amp;', 'en').replace('ü', 'u')).strip('-')


def cta(cls=''):
    return (f'<a class="btn btn--sm {cls}" href="#contact" data-magnetic><span class="btn__label">Bespreek uw vraagstuk</span>'
            f'{btn_icon()}</a>')


def burger():
    return ('<button class="hx-burger" type="button" data-hx-burger aria-expanded="false" aria-controls="hx-sheet" '
            'aria-label="Menu openen"><span></span><span></span></button>')


def sheet():
    """Mobile sheet shared by A and B (exclusive accordion via <details name>)."""
    opl = ''.join(f'<li><a href="{h}">{n}</a></li>' for _, items in OPLOSSINGEN for n, h in items)
    tiles = ''.join(f'<a class="hx-sheet__tile" href="{h}"><span>{pic(img, "", "96px")}</span>{t}</a>'
                    for t, h, img in COMPONENTEN)
    return f'''<div class="hx-sheet" id="hx-sheet" data-hx-sheet hidden>
    <nav aria-label="Mobiele navigatie">
      <details class="hx-sheet__acc" name="hx-m"><summary>Oplossingen{icon("chev-down")}</summary><ul>{opl}</ul></details>
      <details class="hx-sheet__acc" name="hx-m"><summary>Componenten{icon("chev-down")}</summary><div class="hx-sheet__tiles">{tiles}</div></details>
      <a class="hx-sheet__link" href="#">Projecten</a>
      <a class="hx-sheet__link" href="#">Over ons</a>
    </nav>
    <a class="btn btn--block" href="#contact"><span class="btn__label">Bespreek uw vraagstuk</span>{btn_icon()}</a>
    <div class="hx-sheet__contact"><a href="tel:{PHONE_TEL}">{icon("phone")}{PHONE_DISPLAY}</a><a href="mailto:{EMAIL}">{icon("mail")}{EMAIL}</a></div>
  </div>'''


# ================================================================= A  Capsule
def concept_a(overlay):
    groups = ''.join(
        f'<div class="hxa-group"><p class="hxa-group__t">{t}</p><ul>'
        + ''.join(f'<li><a href="{h}"><span>{n}</span>{icon("right")}</a></li>' for n, h in items)
        + '</ul></div>' for t, items in OPLOSSINGEN)
    feature = (f'<a class="hxa-feature" href="{SOLUTIONS_HREF}">{pic("19-granulaat-macro", "", "300px")}'
               f'<span class="hxa-feature__txt"><span class="hxa-feature__q">Van losse component tot complete procesinstallatie.</span>'
               f'<span class="hxa-feature__go">Verken onze oplossingen{icon("right")}</span></span></a>')
    tiles = ''.join(f'<li><a class="hxa-tile" href="{h}"><span class="hxa-tile__img">{pic(img, "", "150px")}</span>'
                    f'<span class="hxa-tile__t">{t}</span></a></li>' for t, h, img in COMPONENTEN)
    ov = ' hx--overlay' if overlay else ''
    return f'''<header class="hx hx--a{ov}" data-hx="a">
  <div class="hxa" data-hxa>
    {C.logo()}
    <nav class="hxa-nav" aria-label="Hoofdnavigatie">
      <ul>
        <li><button class="hxa-link" type="button" data-hx-tab="opl" aria-expanded="false" aria-controls="hxa-opl">Oplossingen{icon("chev-down")}</button></li>
        <li><button class="hxa-link" type="button" data-hx-tab="comp" aria-expanded="false" aria-controls="hxa-comp">Componenten{icon("chev-down")}</button></li>
        <li><a class="hxa-link" href="#">Projecten</a></li>
        <li><a class="hxa-link" href="#">Over ons</a></li>
      </ul>
      <span class="hxa-pill" aria-hidden="true"></span>
    </nav>
    <a class="hxa-tel" href="tel:{PHONE_TEL}">{icon("phone")}<span>{PHONE_DISPLAY}</span></a>
    {cta("hxa-cta")}
    {burger()}
    <span class="hxa-progress" aria-hidden="true"></span>
    <div class="hxa-stage" data-hx-stage>
      <div class="hxa-stage__bg"></div>
      <div class="hxa-panel hxa-panel--opl" id="hxa-opl" data-hx-panel="opl" role="region" aria-label="Oplossingen" inert>
        <div class="hxa-groups">{groups}</div>{feature}
      </div>
      <div class="hxa-panel hxa-panel--comp" id="hxa-comp" data-hx-panel="comp" role="region" aria-label="Componenten" inert>
        <ul class="hxa-tiles">{tiles}</ul>
        <div class="hxa-panel__foot"><span>{N_COMP} productgroepen, los of als complete installatie</span>{C.link("Alle componenten", "#")}</div>
      </div>
    </div>
  </div>
  {sheet()}
</header>'''


# ================================================================= B  Doorsnede
def concept_b(overlay):
    first = OPLOSSINGEN[0][1][0][0]
    groups = ''.join(
        f'<div class="hxb-group"><p class="hxb-group__t">{t}</p><ul>'
        + ''.join(f'<li><a href="{h}" data-fig="{slug(n)}"><span>{n}</span>{icon("ur")}</a></li>' for n, h in items)
        + '</ul></div>' for t, items in OPLOSSINGEN)
    figs = ''.join(f'<div class="hxb-fig__img{" is-on" if n == first else ""}" data-fig-img="{slug(n)}" data-cap="{n}" data-grp="{g}">'
                   f'{pic(SOL_IMG[n], "", "(min-width: 1040px) 40vw, 1px")}</div>'
                   for g, items in OPLOSSINGEN for n, _h in items)
    marks = '<i class="hxb-reg hxb-reg--tl"></i><i class="hxb-reg hxb-reg--tr"></i><i class="hxb-reg hxb-reg--bl"></i><i class="hxb-reg hxb-reg--br"></i>'
    clist = ''.join(f'<li><a href="{h}" data-fig="{slug(t)}"><span class="hxb-thumb">{pic(img, "", "56px")}</span>'
                    f'<span>{t}</span>{icon("ur")}</a></li>' for t, h, img in COMPONENTEN)
    cfigs = ''.join(f'<div class="hxb-fig__img hxb-fig__img--cut{" is-on" if i == 0 else ""}" data-fig-img="{slug(t)}" data-cap="{t}" data-grp="{i + 1} / {N_COMP}">'
                    f'{pic(img, "", "(min-width: 1040px) 30vw, 1px")}</div>' for i, (t, _h, img) in enumerate(COMPONENTEN))
    ov = ' hx--overlay' if overlay else ''
    return f'''<header class="hx hx--b{ov}" data-hx="b">
  <div class="hxb-rail">
    <div class="container hxb-rail__in">
      <nav class="hxb-rail__links" aria-label="Service"><a href="{C.PAGES['artikel']}">Kennisbank</a><a href="#contact">Contact</a></nav>
      <ul>
        <li>{icon("pin")}<span>{ADDRESS[0]}, {ADDRESS[1]}</span></li>
        <li><a href="tel:{PHONE_TEL}">{icon("phone")}<span>{PHONE_DISPLAY}</span></a></li>
        <li><a href="mailto:{EMAIL}">{icon("mail")}<span>{EMAIL}</span></a></li>
      </ul>
    </div>
  </div>
  <div class="hxb-bar">
    <div class="container hxb-bar__in">
      {C.logo()}
      <nav class="hxb-nav" aria-label="Hoofdnavigatie">
        <ul>
          <li><button class="hxb-link" type="button" data-hx-tab="opl" aria-expanded="false" aria-controls="hxb-opl">Oplossingen<sup>{N_SOL}</sup>{icon("chev-down")}</button></li>
          <li><button class="hxb-link" type="button" data-hx-tab="comp" aria-expanded="false" aria-controls="hxb-comp">Componenten<sup>{N_COMP}</sup>{icon("chev-down")}</button></li>
          <li><a class="hxb-link" href="#">Projecten</a></li>
          <li><a class="hxb-link" href="#">Over ons</a></li>
        </ul>
      </nav>
      {cta("hxb-cta")}
      {burger()}
    </div>
    <div class="hxb-ruler" aria-hidden="true"><span class="hxb-ruler__progress"></span><span class="hxb-ruler__marker"></span></div>
  </div>
  <div class="hxb-drawer" id="hxb-opl" data-hx-panel="opl" role="region" aria-label="Oplossingen" inert>
    <div class="container hxb-drawer__in">
      <div class="hxb-drawer__nav">{groups}
        <a class="link hxb-drawer__all" href="{SOLUTIONS_HREF}">Verken onze oplossingen{icon("ur")}</a>
      </div>
      <figure class="hxb-fig" data-fig-frame>{figs}{marks}
        <figcaption><span data-fig-cap>{first}</span><span data-fig-grp>{OPLOSSINGEN[0][0]}</span></figcaption>
      </figure>
    </div>
  </div>
  <div class="hxb-drawer" id="hxb-comp" data-hx-panel="comp" role="region" aria-label="Componenten" inert>
    <div class="container hxb-drawer__in hxb-drawer__in--comp">
      <div class="hxb-drawer__nav"><ul class="hxb-clist">{clist}</ul>
        <a class="link hxb-drawer__all" href="#">Alle componenten{icon("ur")}</a>
      </div>
      <figure class="hxb-fig hxb-fig--cut" data-fig-frame>{cfigs}{marks}
        <figcaption><span data-fig-cap>{COMPONENTEN[0][0]}</span><span data-fig-grp>1 / {N_COMP}</span></figcaption>
      </figure>
    </div>
  </div>
  {sheet()}
</header>'''


# ================================================================= C  Index
def concept_c(overlay):
    opl = ''.join(f'<li><a href="{h}">{n}</a></li>' for _, items in OPLOSSINGEN for n, h in items)
    comp_sub = ''.join(f'<li><a href="{h}">{t}</a></li>' for t, h, _ in COMPONENTEN)
    comp_tiles = ''.join(f'<li><a class="hxc-ctile" href="{h}"><span>{pic(img, "", "120px")}</span>{t}</a></li>'
                         for t, h, img in COMPONENTEN)
    opl_groups = ''.join(
        f'<div><p class="hxc-peek__t">{t}</p><ul>' + ''.join(f'<li><a href="{h}">{n}{icon("ur")}</a></li>' for n, h in items)
        + '</ul></div>' for t, items in OPLOSSINGEN)
    items = [
        ('opl', 'Oplossingen', SOLUTIONS_HREF, f'<ul class="hxc-sub">{opl}</ul>'),
        ('comp', 'Componenten', '#', f'<ul class="hxc-sub">{comp_sub}</ul>'),
        ('proj', 'Projecten', '#', ''),
        ('over', 'Over ons', '#', ''),
        ('contact', 'Contact', '#contact', ''),
    ]
    index = ''.join(
        f'<li style="--i:{i}"><a class="hxc-big" href="{h}" data-peek="{k}"><span class="hxc-big__a">{t}</span>'
        f'<span class="hxc-big__b" aria-hidden="true">{t}</span></a>{sub}</li>'
        for i, (k, t, h, sub) in enumerate(items))
    ov = ' hx--overlay' if overlay else ''
    return f'''<header class="hx hx--c{ov}" data-hx="c">
  <div class="container hxc">
    <div class="hxc-chip hxc-chip--brand">
      {C.logo()}
      <span class="hxc-sec" aria-hidden="true"><span class="hxc-sec__in" data-hxc-sec></span></span>
    </div>
    <div class="hxc-chip hxc-chip--act">
      <a class="hxc-round" href="tel:{PHONE_TEL}" aria-label="Bel {PHONE_DISPLAY}">{icon("phone")}</a>
      {cta("hxc-cta")}
      <button class="hxc-menu" type="button" data-hxc-open aria-haspopup="dialog" aria-controls="hxc-dialog" aria-expanded="false">
        <span class="hxc-menu__lbl">Menu</span><span class="hxc-menu__ico" aria-hidden="true"><i></i><i></i></span></button>
    </div>
  </div>
  <dialog class="hxc-dialog" id="hxc-dialog" aria-label="Menu" data-hxc-dialog>
    <div class="hxc-dialog__grain" aria-hidden="true"></div>
    <div class="container hxc-dtop">
      <a class="logo logo--on-dark" href="index.html" aria-label="{ORG}, naar de homepage">{LOGO_MARK}<span aria-hidden="true">Airtechnic<br>Solutions</span></a>
      <button class="hxc-menu hxc-menu--close" type="button" data-hxc-close autofocus><span class="hxc-menu__lbl">Sluiten</span><span class="hxc-menu__ico" aria-hidden="true"><i></i><i></i></span></button>
    </div>
    <div class="container hxc-body">
      <nav class="hxc-index" aria-label="Hoofdnavigatie"><ol>{index}</ol></nav>
      <div class="hxc-peek" data-hxc-peek>
        <div class="hxc-peek__p is-on" data-peek-panel="default">
          <div class="hxc-peek__media">{pic("02-pijpleiding-contact", "", "40vw")}</div>
          <p class="hxc-peek__q">Wat wilt u <em>verbeteren</em> aan uw proces?</p>
          <p class="hxc-peek__s">Van losse component tot complete procesinstallatie.</p>
        </div>
        <div class="hxc-peek__p" data-peek-panel="opl">
          <div class="hxc-peek__media hxc-peek__media--short">{pic("19-granulaat-macro", "", "40vw")}</div>
          <div class="hxc-peek__cols">{opl_groups}</div>
        </div>
        <div class="hxc-peek__p" data-peek-panel="comp"><ul class="hxc-ctiles">{comp_tiles}</ul></div>
        <div class="hxc-peek__p" data-peek-panel="proj">
          <div class="hxc-peek__media">{pic("20-project-recycling", "", "40vw")}</div>
          <p class="hxc-peek__q">Pneumatisch transport voor PET-recycling</p>
          <p class="hxc-peek__s">Van engineering tot inbedrijfstelling.</p>
        </div>
        <div class="hxc-peek__p" data-peek-panel="over">
          <div class="hxc-peek__media">{pic("22-proces-analyse", "", "40vw")}</div>
          <p class="hxc-peek__q">Industriële luchttechniek <em>&amp;</em> solids processing</p>
          <p class="hxc-peek__s">{ADDRESS[0]}, {ADDRESS[1]}</p>
        </div>
        <div class="hxc-peek__p" data-peek-panel="contact">
          <div class="hxc-peek__media">{pic("02-pijpleiding-contact", "", "40vw")}</div>
          <p class="hxc-peek__q"><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></p>
          <p class="hxc-peek__s"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
        </div>
      </div>
    </div>
    <div class="container hxc-foot">
      <a href="tel:{PHONE_TEL}">{icon("phone")}{PHONE_DISPLAY}</a>
      <a href="mailto:{EMAIL}">{icon("mail")}{EMAIL}</a>
      <span>{icon("pin")}{ADDRESS[0]}, {ADDRESS[1]}</span>
      <a class="btn btn--sm hxc-foot__cta" href="#contact" data-hxc-close-link><span class="btn__label">Bespreek uw vraagstuk</span>{btn_icon()}</a>
    </div>
  </dialog>
</header>'''


CONCEPTS = {
    'a': ('Capsule', concept_a),
    'b': ('Doorsnede', concept_b),
    'c': ('Index', concept_c),
}
SOURCES = {'': 'index.html', '-product': 'cycloonafscheider.html'}


def switcher(cur, suffix):
    def href(k, s=suffix):
        return f'concept-{k}{s}.html'
    opts = ''.join(f'<a href="{href(k)}"{" aria-current=page" if k == cur else ""}><b>{k.upper()}</b><span>{name}</span></a>'
                   for k, (name, _) in CONCEPTS.items())
    other = '-product' if suffix == '' else ''
    page_lbl = 'Productpagina' if suffix == '' else 'Homepage'
    live = SOURCES[suffix]
    return (f'<div class="hx-review" role="navigation" aria-label="Headerconcepten (review)">'
            f'<span class="hx-review__t">Header</span>{opts}'
            f'<span class="hx-review__sep"></span><a href="{href(cur, other)}">{page_lbl}</a>'
            f'<a href="{live}">Huidig</a></div>')


def main():
    css_v = int(os.path.getmtime(os.path.join(ROOT, 'assets', 'css', 'header-concepts.css')))
    js_v = int(os.path.getmtime(os.path.join(ROOT, 'assets', 'js', 'header-concepts.js')))
    for suffix, src in SOURCES.items():
        html = open(os.path.join(ROOT, src), encoding='utf-8').read()
        m = re.search(r'<header class="([^"]*)"[^>]*>.*?</header>', html, re.S)
        overlay = 'overlay' in m.group(1)
        for k, (name, fn) in CONCEPTS.items():
            out = html[:m.start()] + fn(overlay) + html[m.end():]
            out = out.replace('<html lang="nl"', f'<html lang="nl" data-concept="{k}"', 1)
            out = re.sub(r'(<link rel="stylesheet" href="assets/css/site\.css[^"]*">)',
                         rf'\1\n<link rel="stylesheet" href="assets/css/header-concepts.css?v={css_v}">', out, count=1)
            out = re.sub(r'(<script src="assets/js/site\.js[^"]*" defer></script>)',
                         rf'\1\n<script src="assets/js/header-concepts.js?v={js_v}" defer></script>', out, count=1)
            out = out.replace('<meta name="robots" content="index, follow">', '')
            out = out.replace('</head>', '<meta name="robots" content="noindex">\n</head>', 1)
            out = out.replace('</body>', switcher(k, suffix) + '\n</body>', 1)
            dst = f'concept-{k}{suffix}.html'
            with open(os.path.join(ROOT, dst), 'w', encoding='utf-8', newline='\n') as f:
                f.write(out)
            print('wrote', dst, '(overlay)' if overlay else '')


if __name__ == '__main__':
    main()
