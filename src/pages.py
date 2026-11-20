"""Page templates for the Airtechnic "Flow" site. Content is copied verbatim from the brief;
missing copy is marked [TBD]. Run build.py to regenerate the HTML."""
import json
from components import (PAGES, SITE, ORG, COMPONENTEN, icon, pic, media, btn, link, eyebrow, section_head, breadcrumb,
                        breadcrumb_jsonld, card, product_tile, checklist, faq, faq_jsonld, faq_section, contact, contact_url, page,
                        org_jsonld, tbd, split_lines, btn_icon, _v)
from components import OPLOSSINGEN, sym, plate_figure, _slug, catalog_sheet
from category_overview import CategoryOption, HERO_SIZES as CATEGORY_HERO_SIZES, category_catalog, category_intro
from component_detail import GALLERY_SIZES, component_intro, component_nav, component_principle
from knowledge_article import (HERO_SIZES as KNOWLEDGE_HERO_SIZES, knowledge_article, knowledge_comparison, knowledge_flow,
                               knowledge_intro, knowledge_scenarios, knowledge_section, knowledge_takeaway)
from cyclone_flow import cyclone_flow
from slide_flow import filter_flow, diverter_flow, hero_traces
from hero_equipment import EQUIPMENT, HALL_IMAGE, HALL_SIZES, equipment_stage, variant_nav


# ---- Hero granule flow (canvas, assets/js/granule-flow.js) over the EMPTY-tube photo.
# Nine cross-sections through the glass tube, measured on 01-hero-pijpleiding-leeg: (bottom wall, top wall) in px of the
# 1536x1024 photo, lower-left flange face to upper-right flange face. GRAIN_BOX is the canvas box (also in site.css and
# baked into images/hero-glass.webp, the front-glass layer cut from the same photo).
TUBE = [((672, 884), (672, 696)), ((800, 878), (800, 690)), ((920, 846), (895, 662)),
        ((1020, 790), (980, 615)), ((1110, 718), (1060, 548)), ((1190, 630), (1120, 478)),
        ((1260, 535), (1175, 400)), ((1320, 450), (1215, 325)), ((1385, 372), (1238, 266))]
GRAIN_BOX = (640, 240, 1420, 904)


# ---- Hero slides (Nov 20): five photos of one process line in the same 1536x1024 framing (equipment right, empty
# wall left), so they share one stage box, one veil and one Tekenblad fold. Slide 1 keeps granules + streamlines.
# Hotspots: (x %, y %, title, text, href, side) measured on each photo. Copy: formal "u", no invented claims.
HERO_SLIDES = [
    {'image': '01-hero-pijpleiding-leeg', 'discipline': 'Pneumatisch transport',
     'alt': 'RVS pijpleiding met een transparant deel waar goudkleurig granulaat doorheen stroomt',
     'title': 'Grip op<br><em>elke stroom.</em>',
     'tab': 'Transport',
     'sub': 'Pneumatisch transport van poeders en granulaten, van losse component tot complete procesinstallatie.',
     'link': ('Meer over pneumatisch transport', PAGES['artikel'])},
    {'image': '30-hero-filter', 'discipline': 'Filtratie &amp; stofafzuiging',
     'alt': 'RVS filterhuis met kijkvenster op drie geplooide filterpatronen boven een conische stofopvang',
     'title': 'Schone lucht,<br><em>niets verloren.</em>',
     'tab': 'Filtratie',
     'sub': 'Filtratie en stofafzuiging die fijnstof uit uw proceslucht halen en product terugwinnen.',
     'link': ('Bekijk filtratie', 'componenten-filters.html'),
     'spots': [(67, 37, 'Filterpatronen', 'Scheiden fijnstof uit de transportlucht', 'filterelement.html', 'r'),
               (66, 79, 'Stofopvang', 'Afgevangen product zakt via de conus terug', 'patroonfilter.html', 'l')]},
    {'image': '31-hero-wissel', 'discipline': 'Leidingwerk &amp; wissels',
     'alt': 'RVS broekstuk-wissel met kijkvenster, omstelklep en pneumatische cilinder',
     'title': 'Wissel<br><em>van route.</em>',
     'tab': 'Wissels',
     'sub': 'Wissels en afsluiters sturen uw bulkgoed via één leiding naar de juiste silo of menger.',
     'link': ('Bekijk leidingwerk', 'componenten-leidingwerk-koppelingen.html'),
     'spots': [(63, 44, 'Omstelklep', 'Stuurt de productstroom naar één van twee uitgangen', 'leidingwissel.html', 'r'),
               (86, 28, 'Pneumatische aandrijving', 'Zet de klep om op een signaal van uw besturing', 'leidingwissel.html', 'l')]},
    {'image': '32-hero-cycloon', 'discipline': 'Cyclonen',
     'alt': 'RVS cycloonafscheider met transparante wand, tangentiële inlaat en dompelbuis',
     'title': 'Laat het<br><em>wervelen.</em>',
     'tab': 'Cyclonen',
     'sub': 'Cyclonen scheiden product en transportlucht met centrifugaalkracht, zonder bewegende delen.',
     'link': ('Bekijk cyclonen', PAGES['categorie']),
     'spots': [(69, 31, 'Dompelbuis', 'De gereinigde lucht verlaat de cycloon bovenaan', PAGES['product'], 'r'),
               (69, 70, 'Conus', 'Product zakt langs de wand naar de uitlaat', PAGES['product'], 'l')]},
    {'image': '33-hero-doseersluis', 'discipline': 'Doseren',
     'alt': 'RVS doseersluis met kijkvenster op de rotor, onder een trechter en met elektromotor',
     'title': 'Elke korrel<br><em>op tijd.</em>',
     'tab': 'Doseren',
     'sub': 'Doseersluizen voeren poeders en granulaten gelijkmatig af en scheiden de drukzones.',
     'link': ('Bekijk doseersluizen', 'componenten-doseersluizen.html'),
     'spots': [(54, 46, 'Rotor met vakken', 'Neemt per omwenteling een vast volume product mee', 'doorvalsluis.html', 'r'),
               (88, 45, 'Aandrijving', 'Het toerental bepaalt de doseercapaciteit', 'doorvalsluis.html', 'l')]},
]
HERO_SLIDE_SECONDS = 8


def _hotspots(spots):
    hs = ''.join(
        f'<li class="hotspot hotspot--{side}" style="--x:{x}%;--y:{y}%;--i:{i}"><a class="hotspot__link" href="{href}">'
        f'<span class="hotspot__dot" aria-hidden="true"></span>'
        f'<span class="hotspot__card"><strong>{t}</strong><span>{sub}</span></span></a></li>'
        for i, (x, y, t, sub, href, side) in enumerate(spots))
    return f'<ul class="hotspots" aria-label="Wat u op deze foto ziet">{hs}</ul>'


def _off(i):
    return '' if i == 0 else ' aria-hidden="true" inert'


def hero_slides_stage():
    """All slide photos inside one cover-box stage. A scan line leads each wipe like a plotter head."""
    out = []
    effects = {"30-hero-filter": filter_flow, "31-hero-wissel": diverter_flow,
               "32-hero-cycloon": cyclone_flow}
    for i, s in enumerate(HERO_SLIDES):
        # Close-up photos (2-5) sit a step smaller, anchored right, over a blurred extension of themselves, so the
        # equipment stays clear of the type column without a seam.
        image = s["image"]
        overlay = hero_traces(image) if i else ""
        if image in effects:
            overlay += effects[image]()
        inner = pipe_stage(inner_only=True) if i == 0 else (
            f'<img class="hero__ambient" src="images/{s["image"]}-480.webp" alt="" aria-hidden="true" loading="lazy" decoding="async">'
            f'<div class="hero__frame"><div class="hero__media">{pic(s["image"], s["alt"], HALL_SIZES)}</div>{overlay}{_hotspots(s["spots"])}</div>')
        cls = ' is-on' if i == 0 else ' hero__slide--framed'
        out.append(f'<div class="hero__slide{cls}" data-slide="{i}"{_off(i)}>{inner}</div>')
    return f'<div class="hero__stage" data-slides>{"".join(out)}<i class="hero__scan" aria-hidden="true"></i></div>'


def hero_slides_copy():
    n = len(HERO_SLIDES)
    out = []
    for i, s in enumerate(HERO_SLIDES):
        out.append(f'''<div class="hero__copy{" is-on" if i == 0 else ""}" id="hero-slide-{i}" role="group" aria-roledescription="dia" aria-label="{i + 1} van {n}: {s['discipline']}" data-copy="{i}" data-discipline="{s['discipline']}"{_off(i)}>
        <p class="display hero__title">{split_lines(s['title'])}</p>
        <p class="hero__sub">{s['sub']}</p>
      </div>''')
    return ''.join(out)


def hero_more_links():
    """One deep link per slide, stacked in one grid cell next to the main CTA."""
    return '<span class="hero__mores">' + ''.join(
        f'<span class="hero__more{" is-on" if i == 0 else ""}" data-more="{i}"{_off(i)}>'
        f'{link(s["link"][0], s["link"][1], "down" if s["link"][1].startswith("#") else "right", "link--green link--quiet")}</span>'
        for i, s in enumerate(HERO_SLIDES)) + '</span>'


def hero_tabs():
    n = len(HERO_SLIDES)
    tabs = ''.join(
        f'<button class="hero-tab" type="button" data-tab="{i}" aria-controls="hero-slide-{i}"'
        f'{" aria-current=" + chr(34) + "true" + chr(34) if i == 0 else ""}>'
        f'<span class="hero-tab__no" aria-hidden="true">{i + 1:02d}</span><span class="hero-tab__label">{s["tab"]}</span>'
        f'<span class="visually-hidden"> (dia {i + 1} van {n})</span><i class="hero-tab__fill" aria-hidden="true"></i></button>'
        for i, s in enumerate(HERO_SLIDES))
    return f'<div class="hero-tabs" role="group" aria-label="Kies een onderwerp">{tabs}</div>'


def pipe_stage(inner_only=False):
    # Stage = exact "object-fit: cover" box of the 1536x1024 photo, so hotspots and the SVG overlay stay
    # glued to the same pixels at every viewport (see .hero__stage in site.css).
    def _streamline(k):
        return (f'M -60 {791 - k} L {560 - .35 * k:.0f} {791 - k} C {880 - .6 * k:.0f} {791 - k}, '
                f'{1150 - .75 * k:.0f} {620 - .8 * k:.0f}, {1380 - .85 * k:.0f} {270 - .6 * k:.0f}')
    lines = ''.join(f'<path class="sl-base" pathLength="1000" d="{_streamline(k)}"/>'
                    f'<path class="sl" pathLength="1000" style="--d:{i * -1.3 - .4:.1f}s;--dur:{6.2 + i * .9:.1f}s" d="{_streamline(k)}"/>'
                    for i, k in enumerate((70, 150, 240, 340, 450)))
    hotspots = [
        (66, 63, 'Pneumatisch transport', 'Poeders en granulaten door een gesloten leiding', 'kennis-druk-of-vacuumtransport.html', 'r'),
        (39.6, 77, 'Leidingwerk &amp; koppelingen', 'RVS leidingen, bochten en flensverbindingen', 'componenten-leidingwerk-koppelingen.html', 'r'),
        (66, 26, 'Opslaan', 'Gecontroleerde opslag van bulkgoederen', 'componenten-bigbag-stations.html', 'l'),
    ]
    hs = ''.join(
        f'<li class="hotspot hotspot--{side}" style="--x:{x}%;--y:{y}%;--i:{i}"><a class="hotspot__link" href="{href}">'
        f'<span class="hotspot__dot" aria-hidden="true"></span>'
        f'<span class="hotspot__card"><strong>{t}</strong><span>{sub}</span></span></a></li>'
        for i, (x, y, t, sub, href, side) in enumerate(hotspots))
    inner = f'''
      <div class="hero__media">{pic("01-hero-pijpleiding-leeg", "RVS pijpleiding met een transparant deel waar goudkleurig granulaat doorheen stroomt", HALL_SIZES, eager=True, img_cls="kenburns")}</div>
      <canvas class="hero__granules" aria-hidden="true" data-granules data-box="{','.join(map(str, GRAIN_BOX))}" data-tube="{json.dumps([[list(b), list(t)] for b, t in TUBE], separators=(',', ':'))}" data-glass="{_v('images/hero-glass.webp')}"></canvas>
      <svg class="hero__flow" viewBox="0 0 1536 1024" preserveAspectRatio="none" aria-hidden="true" focusable="false" data-flow-svg>
        <defs>
          <linearGradient id="sl-fade" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".34" stop-color="#fff" stop-opacity="0"/><stop offset=".55" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity=".9"/></linearGradient>
          <mask id="sl-mask"><rect width="1536" height="1024" fill="url(#sl-fade)"/></mask>
        </defs>
        <g class="hero__lines" mask="url(#sl-mask)">{lines}</g>
      </svg>
      <ul class="hotspots" aria-label="Wat u op deze foto ziet">{hs}</ul>'''
    return inner if inner_only else f'<div class="hero__stage">{inner}\n    </div>'


def home_hero(variant):
    if variant:
        equipment = EQUIPMENT[variant]
        stage = equipment_stage(variant)
        discipline = equipment['discipline']
        sheet = f'{2 + list(EQUIPMENT).index(variant):02d}'
        bar = variant_nav(variant)
        track_class = ' hero-track--equipment'
        script = ''
    else:
        stage = hero_slides_stage()
        discipline = HERO_SLIDES[0]['discipline']
        sheet = f'<span data-plate-sheet>01</span> / {len(HERO_SLIDES):02d}'
        bar = hero_tabs()
        track_class = ' hero-track--slides'
        script = f'<script src="{_v("assets/js/granule-flow.js")}" defer></script>'
    # The shared Tekenblad frame folds into a measured plate on wide screens.
    plate = f'''<div class="plate" aria-hidden="true" data-plate>
    <i class="plate__ruler plate__ruler--x"></i><i class="plate__ruler plate__ruler--y"></i>
    <i class="plate__reg plate__reg--tl"></i><i class="plate__reg plate__reg--tr"></i><i class="plate__reg plate__reg--bl"></i><i class="plate__reg plate__reg--br"></i>
    <dl class="plate__title">
      <div><dt>Project</dt><dd>Proceslijn</dd></div>
      <div><dt>Discipline</dt><dd data-plate-discipline>{discipline}</dd></div>
      <div><dt>Blad</dt><dd>{sheet}</dd></div>
    </dl>
  </div>'''
    if variant:
        copy = f'''<p class="eyebrow hero__eyebrow"><span class="pulse" aria-hidden="true"></span>Industriële luchttechniek &amp; solids processing</p>
      <h1 id="hero-title" class="display hero__title" data-split>{split_lines("Grip op<br><em>elke stroom.</em>")}</h1>
      <p class="hero__sub">Van losse component tot complete procesinstallatie.</p>
      <div class="actions hero__actions">{btn("Bespreek uw vraagstuk", "#contact", "lg")}{link("Verken onze oplossingen", "#specialisaties", "down", "link--green link--quiet")}</div>'''
        section_attrs = 'aria-labelledby="hero-title"'
    else:
        # The H1 carries the search terms and stays put; each slide brings its own statement, lead and deep link.
        copy = f'''<h1 id="hero-title" class="eyebrow hero__eyebrow"><span class="pulse" aria-hidden="true"></span>Industriële luchttechniek &amp; solids processing</h1>
      <div class="hero__copies" data-split data-hero-copies>{hero_slides_copy()}</div>
      <div class="actions hero__actions">{btn("Bespreek uw vraagstuk", "#contact", "lg")}{hero_more_links()}</div>'''
        section_attrs = f'aria-labelledby="hero-title" aria-roledescription="carrousel" data-hero-slides style="--slide-dur:{HERO_SLIDE_SECONDS}s"'
    return f'''<div class="hero-track{track_class}" data-hero-track>
<section class="hero" data-motion-scope data-hero {section_attrs}>
  <div class="hero__visual" data-hero-visual>
    {stage}
  </div>
  {plate}
  <div class="hero__veil" aria-hidden="true"></div>
  <div class="container hero__content">
    <div class="hero__inner">
      {copy}
    </div>
  </div>
  <div class="hero__bar">
    {bar}
    <button class="motion-toggle" type="button" data-motion-toggle aria-pressed="false">{icon("pause", attrs=' data-icon-pause')}{icon("play", attrs=' data-icon-play hidden')}<span data-label>Animatie pauzeren</span></button>
  </div>
</section>
</div>
{script}'''


# =====================================================================  1. HOME
def home(variant=None, footer_variant="stone"):
    if variant:
        hero = home_hero(variant)
    else:
        from hero_concepts import concept
        hero = concept("cinema", embedded=True)

    # Block 2 "Processchema": a process line drops from the hero plate's corner and splits into the two disciplines
    # (geometry + scroll progress in site.js); items swap the discipline's plate figure.
    introductions = {
        'Industriële luchttechniek': 'Schone, veilige en efficiënte luchtoplossingen voor uw proces.',
        'Solids processing': 'Betrouwbaar en gecontroleerd omgaan met poeders en granulaten.',
    }

    def discipline(title, links):
        text = introductions[title]
        items = [name for name, href in links]
        lis = ''.join(f'<li><a href="{href}" data-fig="{_slug(n)}">{sym(n)}<span>{n}</span>{icon("ur")}</a></li>' for n, href in links)
        return f'''<article class="pr-disc" data-disc>
        <div class="pr-disc__top"><span class="pr-node" data-process-node data-sig-node>{sym(title, "sym sym--node")}</span>
          <div><h3 class="h3">{title}</h3><p>{text}</p></div></div>
        {plate_figure(items, title, "(min-width: 960px) 34vw, 92vw")}
        <ul class="pr-list">{lis}</ul>
      </article>'''

    specs = f'''<section class="section--home section--ruled process" id="specialisaties" aria-labelledby="spec-title" data-process>
  <div class="container process__in">
    <div class="process__head"><h2 id="spec-title" class="h2" data-split>{split_lines("Twee specialisaties.<br><em>Eén samenhangend proces.</em>")}</h2></div>
    <div class="process__cols">{"".join(discipline(*d) for d in OPLOSSINGEN)}</div>
  </div>
</section>'''

    # Block 3 "Catalogusbladen": all eight groups as framed plates; hover reveals dimension lines and, where a
    # cross-section exists, a cutting line that opens the machine (components.catalog_sheet, site.js adds .is-in).
    sheets = ''.join(catalog_sheet(t, h, img, i) for i, (t, h, img) in enumerate(COMPONENTEN))
    carousel = f'''<section class="section--home band--sage section--ruled catalog" aria-labelledby="comp-title" data-catalog>
  <div class="container">
    <div class="catalog__head"><h2 id="comp-title" class="h2" data-split>{split_lines("Het juiste component.<br><em>Op de juiste plek.</em>")}</h2>{link("Alle componenten", "componenten.html")}</div>
    <ul class="catalog__grid">{sheets}</ul>
  </div>
</section>'''

    cases = [
        ('food', 'Food', ('Pneumatisch transport bij Driessen Food Extrusion', 'Twee vacuümtransportlijnen brengen extrudaten naar één ontvangststation.'), 'project-food', 'Illustratie van twee transportlijnen naar een centrale ontvanger'),
        ('recycling', 'Recycling', ('Pneumatisch transport voor <span style="white-space:nowrap">PET-recycling</span>', 'Van engineering tot inbedrijfstelling.'),
         'project-pet', 'Illustratieve opstelling voor PET-recycling met transport, opslag en bigbag-vulling'),
    ]  # Feed, Chemie, Hout: hidden until a case exists
    default = 'recycling'
    tabs = ''.join(
        f'<button class="case__tab" role="tab" type="button" id="case-tab-{k}" aria-controls="case-{k}" aria-selected="{str(k == default).lower()}" tabindex="{0 if k == default else -1}">{label}</button>'
        for k, label, *_ in cases)
    panels = ''
    for k, label, copy, img, alt in cases:
        h2, sub = copy
        case_link = (link("Bekijk het project", "project-driessen-food-extrusion.html")
                     if k == "food" else link("Bekijk het project", "project-pet-recycling.html"))
        case_link += '<div style="margin-top:16px">' + link("Alle projecten", "projecten.html") + '</div>'
        on = k == default
        panels += f'''<div class="case__panel{' is-active' if on else ''}" id="case-{k}" role="tabpanel" aria-labelledby="case-tab-{k}" data-crossfade aria-hidden="{str(not on).lower()}">
        <div class="case__text">{eyebrow("Uit de praktijk")}<h2 class="h2 h2--plain">{h2}</h2><p>{sub}</p><p style="font-size:12px;opacity:.8">Beeld: technische projectillustratie</p>{case_link}</div>
        <div class="case__media" data-parallax>{pic(img, alt, "(min-width: 960px) 60vw, 100vw", style="object-fit:contain")}</div>
      </div>'''
    case = f'''<section id="projecten" data-theme="forest" class="case" aria-label="Uit de praktijk" data-sig-label="Praktijk" data-reveal>
  <div class="container case__inner" data-tabs>
    <div class="case__tabs" role="tablist" aria-label="Kies een branche">{tabs}</div>
    <div class="case__panels">
      {panels}
    </div>
  </div>
</section>'''

    steps = [
        ('Analyse', '22-proces-analyse', 'Twee engineers bespreken een procesvraag aan tafel met tekeningen en een tablet', {
            'title': 'Analyse van uw productieproces',
            'text': 'We brengen uw proces en de gewenste capaciteit in kaart. Bij pneumatisch transport kijken we naar het materiaal en het leidingtracé. Bij industriële stofafzuiging onderzoeken we waar stof vrijkomt en welke afzuigpunten nodig zijn.',
            'deliverables': ['Overzicht van procesgegevens en knelpunten', 'Capaciteits- en inpassingseisen', 'Advies over de oplossingsrichting'],
            'fase': 'Samen bepalen we welke procesgegevens nodig zijn om het ontwerp uit te werken.'}),
        ('Engineering', '23-proces-engineering', 'Engineer werkt aan een 3D-model van een cycloon op een computerscherm', {
            'title': 'Engineering van de procesinstallatie',
            'text': 'We ontwerpen een installatie voor uw productieomgeving. Voor het transport van poeders of granulaten werken we luchthoeveelheid, druk en leidingdiameter uit. Voor stofafzuiging stemmen we de ventilator, het leidingwerk en de filtratie op elkaar af.',
            'deliverables': ['Proces- en installatieontwerp', 'Componentselectie en leidingtracé', 'Technische tekeningen voor bouw en montage'],
            'fase': 'We stemmen de aansluitingen op uw productielijn af en houden ruimte vrij voor inspectie en onderhoud.',
            'link': 'Bespreek het ontwerp van uw installatie'}),
        ('Realisatie', '24-proces-realisatie', 'Monteur met helm monteert een flensverbinding aan RVS leidingwerk', {
            'title': 'Bouw en montage van de installatie',
            'text': 'We produceren of leveren de onderdelen volgens het ontwerp en monteren de procesinstallatie op locatie. Daarbij sluiten we het leidingwerk en de geselecteerde componenten aan op de nieuwe of bestaande productielijn.',
            'deliverables': ['Gemonteerd leidingwerk en componenten', 'Aansluitingen op de productielijn', 'Montagecontrole'],
            'fase': 'We stemmen de montageplanning af op de beschikbare ruimte en uw productieplanning.'}),
        ('Inbedrijfstelling', '25-proces-inbedrijfstelling', 'Twee technici nemen een installatie in bedrijf bij het bedieningspaneel', {
            'title': 'Inbedrijfstelling en oplevering',
            'text': 'We starten de installatie op, stellen de bedrijfsparameters af en toetsen de werking aan de afgesproken eisen. Afhankelijk van de toepassing controleren we bijvoorbeeld de transportcapaciteit of de werking van de stofafzuiging.',
            'deliverables': ['Ingestelde en geteste installatie', 'Terugkoppeling over de testresultaten', 'Overdracht aan uw team'],
            'fase': 'Bij de overdracht lopen we de bediening en de aandachtspunten voor dagelijks gebruik met uw team door.'}),
    ]
    active = 1
    step_tabs = ''.join(
        f'<button class="step-btn" role="tab" type="button" id="step-tab-{i}" aria-controls="step-{i}" aria-selected="{str(i == active).lower()}" tabindex="{0 if i == active else -1}">'
        f'<span class="step-btn__num">{i + 1:02d}</span>{name}{icon("chev-right")}</button>'
        for i, (name, *_) in enumerate(steps))
    step_panels = ''
    for i, (_, img, alt, copy) in enumerate(steps):
        contact_link = link(copy["link"], contact_url("installatieontwerp")) if "link" in copy else ""
        body = (f'<p>{copy["text"]}</p><div class="step-cols"><div><h4 class="h4">Wat u krijgt</h4>{checklist(copy["deliverables"])}</div>'
                f'<div><h4 class="h4">In deze fase</h4><p>{copy["fase"]}</p>{contact_link}</div></div>')
        hidden = '' if i == active else ' hidden'
        step_panels += (f'<div class="step-panel" id="step-{i}" role="tabpanel" aria-labelledby="step-tab-{i}" tabindex="0"{hidden}>'
                        f'{media(img, alt, "", False, "(min-width: 960px) 60vw, 100vw")}<h3 class="h3">{copy["title"]}</h3>{body}</div>')
    werkwijze = f'''<section class="section--home werkwijze" aria-labelledby="steps-title" data-reveal>
  <div class="container">
    {section_head("Van procesanalyse naar<br><em>werkende installatie.</em>", "steps-title", "Werkwijze")}
    <div class="steps" data-tabs="vertical">
      <div><p class="steps__intro">Eén technisch aanspreekpunt voor industriële luchttechniek en bulkverwerking, van ontwerp tot inbedrijfstelling.</p>
      <div class="steps__list" role="tablist" aria-orientation="vertical" aria-label="Werkwijze in vier stappen">{step_tabs}</div></div>
      <div>{step_panels}</div>
    </div>
  </div>
</section>'''

    kennis_cards = ''.join([
        card('Druk- of vacuümtransport?', 'Lees meer', PAGES['artikel'], '01-hero-pijpleiding', '', 'ar-16-9', title_cls='card__title card__title--sm',
             sizes='(min-width: 960px) 24vw, (min-width: 640px) 50vw, 100vw', style='object-position: 72% 60%'),
        card('Wanneer vervangt u uw filters?', 'Lees meer', 'kennis-wanneer-filters-vervangen.html', '17-filter-macro', '', 'ar-16-9', title_cls='card__title card__title--sm',
             sizes='(min-width: 960px) 24vw, (min-width: 640px) 50vw, 100vw'),
        card('De juiste blower selecteren?', 'Lees meer', 'kennis-juiste-blower-selecteren.html', '18-blower-macro', '', 'ar-16-9', title_cls='card__title card__title--sm',
             sizes='(min-width: 960px) 24vw, (min-width: 640px) 50vw, 100vw', style='object-position: 40% 50%'),
    ])
    kennis = f'''<section class="section--home section--kennis" aria-labelledby="kennis-title" data-reveal>
  <div class="container kennis">
    <div>{eyebrow("Kennisbank")}<h2 id="kennis-title" class="h2" data-split>{split_lines("Kennis die uw proces<br><em>verder brengt.</em>")}</h2><p class="meta" style="margin-top:18px">{link("Bekijk de volledige kennisbank", "kennisbank.html")}</p></div>
    <div class="cards-3">{kennis_cards}</div>
  </div>
</section>'''

    faq_items = [
        ('Leveren jullie ook losse componenten?', 'Ja. Airtechnic Solutions levert losse componenten en complete procesinstallaties voor industriële luchttechniek en bulkverwerking. Denk aan cyclonen, stoffilters, blowers, ventilatoren en doseersluizen. We helpen u bij de selectie op basis van uw product, de gewenste capaciteit en de aansluiting op uw installatie.'),
        ('Kunnen jullie onze bestaande installatie verbeteren?', 'Ja. We onderzoeken hoe uw bestaande installatie voor pneumatisch transport, stofafzuiging of bulkverwerking kan worden verbeterd. Daarbij kijken we naar knelpunten in capaciteit, energieverbruik, slijtage en onderhoud. Op basis van de procesgegevens adviseren we over aanpassingen aan het leidingwerk, vervanging van componenten of uitbreiding van het systeem.'),
        ('Welke informatie is nodig voor een eerste gesprek?', 'Vertel ons welk product u verwerkt, wat u wilt verbeteren en welke capaciteit u nodig heeft. Bij pneumatisch transport zijn ook de transportafstand, het hoogteverschil en de eigenschappen van het poeder of granulaat relevant. Voor stofafzuiging helpt informatie over de stofbronnen en afzuigpunten. Foto’s, tekeningen en gegevens van uw huidige installatie geven extra inzicht. Samen bepalen we welke aanvullende gegevens nodig zijn.'),
        ('Voor welke industrieën werken jullie?', 'We leveren oplossingen voor onder meer de voedingsmiddelenindustrie, diervoederindustrie, chemie, recycling en houtverwerking. Onze industriële luchttechniek en solids processing worden ingezet voor het afzuigen en filteren van stof, het pneumatisch transport van poeders en granulaten en het scheiden en doseren van bulkgoederen. Het ontwerp stemmen we af op het product en de productieomgeving.'),
        ('Hoe kiezen jullie het juiste pneumatische transportsysteem?', 'De keuze hangt af van het product, de gewenste capaciteit, de transportafstand en de beschikbare ruimte. We bekijken onder meer de korrelgrootte, de bulkdichtheid en de gevoeligheid voor productbeschadiging. Met deze gegevens bepalen we of druktransport of vacuümtransport geschikt is en stemmen we de luchtstroom, het leidingwerk en de componenten op elkaar af.'),
        ('Ontwerpen jullie procesinstallaties op maat?', 'Ja. We ontwerpen installaties voor industriële luchttechniek en solids processing op basis van uw proces en productieomgeving. Daarbij combineren we passende componenten met maatwerk in het leidingtracé, de opstelling en de aansluitingen. Zo kunnen we een nieuwe installatie of een uitbreiding inpassen in uw productielijn.'),
        ('Verzorgen jullie ook onderhoud en revisie?', 'Ja. Airtechnic Solutions verzorgt onderhoud, revisie en optimalisatie van bestaande installaties. We bekijken de technische staat en de bedrijfsomstandigheden om te bepalen welke werkzaamheden nodig zijn. Preventief onderhoud helpt slijtage tijdig te signaleren en ondersteunt de bedrijfszekerheid van uw pneumatisch transport, stofafzuiging of bulkverwerking.'),
        ('Hoe verloopt een project van ontwerp tot oplevering?', 'We starten met een analyse van uw proces, product en capaciteitsvraag. Daarna werken we het installatieontwerp en de componentselectie uit. Na afstemming volgen de levering en montage. Bij de inbedrijfstelling stellen we de installatie af, controleren we de werking aan de hand van de afgesproken eisen en dragen we de installatie over aan uw team.'),
    ]
    body = '\n'.join([
        hero, specs, carousel, case, werkwijze, kennis,
        f'''<section class="section--home faq-home" aria-labelledby="faq-title" data-reveal>
  <div class="container">{section_head("Veelgestelde vragen over<br><em>uw procesinstallatie.</em>", "faq-title", "Veelgestelde vragen", plain=True)}<div class="faq--home">{faq(faq_items, True)}</div></div>
</section>''',
        contact('Wat wilt u<br><em>verbeteren</em><br>aan uw proces?', 'Vertel ons wat u verwerkt en wat u wilt bereiken.', deco=True, topics=('installatieontwerp', 'druk-of-vacuumtransport', 'cyclonen')),
    ])
    return page(PAGES['home'], 'Pneumatisch transport &amp; industriële luchttechniek | Airtechnic Solutions',
                'Pneumatisch transport, filtratie, cyclonen, wissels en doseersluizen voor poeders en granulaten: van losse component tot complete procesinstallatie.',
                'og-01-hero-pijpleiding.jpg', body, [org_jsonld(), faq_jsonld(faq_items)], overlay=bool(variant),
                stylesheet=None if variant else "assets/css/hero-concepts.css",
                preload_img=(HALL_IMAGE if variant else '01-hero-pijpleiding', HALL_SIZES), footer_variant=footer_variant,
                preview=variant is not None or footer_variant != "stone")


# =====================================================================  2. KENNISARTIKEL
def artikel():
    headline = 'Druk- of vacuümtransport: wat past bij uw proces?'
    description = 'Vergelijk druk- en vacuümtransport voor poeders, granulaat en pellets. Bekijk de werking, typische opstellingen en welke gegevens uw keuze bepalen.'
    crumbs = [('Home', 'index.html'), ('Kennisbank', 'kennisbank.html'), ('Druk- of vacuümtransport', PAGES['artikel'])]
    hero_image = '01-hero-pijpleiding'
    topic = 'druk-of-vacuumtransport'
    hero = knowledge_intro(
        'Druk- of<br><em>vacuümtransport?</em>', crumbs,
        'Waar begint de luchtstroom, waar neemt u product op en waar moet het heen? Die drie vragen helpen u kiezen tussen transport met overdruk en transport met vacuüm.',
        hero_image, 'Goudkleurig granulaat in een transparant gedeelte van een RVS transportleiding',
        ('Pneumatisch transport', 'Granulaat in een gesloten leiding'),
        (('Naar de vergelijking', '#vergelijking'), ('Zo werkt het', '#twee-principes')),
    )
    takeaway = knowledge_takeaway('Kort antwoord', [
        ('Druktransport', 'Lucht wordt vóór de productinvoer ingeblazen. Onderzoek dit bij langere routes, een hoog productdebiet of meerdere bestemmingen.'),
        ('Vacuümtransport', 'De vacuümbron zit achter de ontvanger. Onderzoek dit als u op meerdere plekken product wilt aanzuigen.'),
    ])
    principles = knowledge_section('twee-principes', 'Twee principes, <em>één doel</em>', '''
      <p>Pneumatisch transport gebruikt lucht om poeders, granulaten of pellets door een gesloten leiding te verplaatsen. Het drukverschil brengt de lucht in beweging. De ontvanger scheidt het product vervolgens van de transportlucht.</p>
      <p>De plek van de luchtbron bepaalt het basisverschil. In de schema’s volgt u zowel lucht als product, van bron of opnamepunt tot ontvanger.</p>
      <ul class="knowledge-legend" aria-label="Legenda bij de schema’s">
        <li><span aria-hidden="true"></span>Lucht</li>
        <li><span aria-hidden="true"></span>Lucht met product</li>
      </ul>
    ''')
    pressure_flow = knowledge_flow('Procesroute druktransport', [
        ('Hoogvacuüm', 'Luchtbron'), ('Pneumatisch transport', 'Productinvoer'), ('Stofafzuiging', 'Ontvanger'),
    ], True, 'Overdruk · de luchtbron staat vóór de productinvoer.')
    pressure = knowledge_section('druktransport', 'Wanneer kiest u <em>druktransport?</em>', f'''
      <p>Een blower of compressor brengt de leiding op overdruk. Via een geschikte invoer, bijvoorbeeld een doseersluis, komt het product in de luchtstroom. Aan de bestemming wordt het product uit de transportlucht gehaald.</p>
      {pressure_flow}
      <p><strong>Typische situatie.</strong> Eén opslagsilo voedt meerdere proceslijnen. Druktransport komt ook vaak in beeld als de route langer is of als u veel materiaal per uur moet verplaatsen.</p>
    ''')
    vacuum_flow = knowledge_flow('Procesroute vacuümtransport', [
        ('Pneumatisch transport', 'Opnamepunt'), ('Filtratie', 'Ontvanger met filter'), ('Hoogvacuüm', 'Vacuümbron'),
    ], False, 'Onderdruk · na de ontvanger gaat de afgezogen lucht naar de vacuümbron.')
    vacuum = knowledge_section('vacuumtransport', 'Wanneer kiest u <em>vacuümtransport?</em>', f'''
      <p>Een vacuümpomp of vacuümblower achter de ontvanger zuigt lucht door de leiding. Lucht neemt product mee vanaf het opnamepunt. In de ontvanger blijft het product achter terwijl de gefilterde lucht verdergaat richting de vacuümbron.</p>
      {vacuum_flow}
      <p><strong>Typische situatie.</strong> Meerdere big-bagstations vullen één menger. Bij een lekkage in het leidingdeel onder vacuüm stroomt omgevingslucht naar binnen. Dat helpt uitstoot van stof uit dat deel te beperken.</p>
    ''')
    rows = [
        ('Opname en bestemming', 'Vaak van één productbron naar één of meer afgiftepunten.', 'Meerdere opnamepunten naar één ontvanger is een gangbare opstelling.'),
        ('Route en productdebiet', 'Vaak passend bij een langere route of een hoog productdebiet.', 'Vaak passend bij kortere routes en lagere productdebieten.'),
        ('Lekkage in de leiding', 'Bij overdruk kan lucht met stof naar buiten ontsnappen.', 'Bij onderdruk kan omgevingslucht naar binnen komen.'),
        ('Kwetsbaar product', 'Beoordeel luchtsnelheid, transportregime en bochten.', 'Beoordeel dezelfde factoren. Het product bepaalt wat het verdraagt.'),
    ]
    matrix = knowledge_comparison('Selectiecriteria voor druk- en vacuümtransport', ['Afweging', 'Druktransport', 'Vacuümtransport'], rows)
    comparison = knowledge_section('vergelijking', 'Vergelijk <em>uw situatie</em>', f'''
      <p>Gebruik deze vergelijking als eerste afweging. Afstand, hoogteverschil, bochten, capaciteit en de eigenschappen van het product spelen samen een rol in het ontwerp.</p>
      {matrix}
    ''')
    cases = knowledge_scenarios([
        ('Eén silo voedt meerdere proceslijnen', 'Onderzoek druktransport.', 'Breng de afgiftepunten, de langste leidingroute en de piekbelasting in kaart.'),
        ('Meerdere punten vullen één ontvanger', 'Onderzoek vacuümtransport.', 'Leg vast welke punten tegelijk product leveren en wat de ontvanger per uur moet kunnen verwerken.'),
        ('Het product breekt of geeft snel stof af', 'Beoordeel beide principes.', 'Neem productmonsters, deeltjesgrootte en de aanvaardbare productbeschadiging mee. Zo bepaalt u welk transportregime geschikt kan zijn.'),
    ])
    product = knowledge_section('uw-product', 'Van vergelijking <em>naar ontwerp</em>', f'''
      <p>Kies de situatie die het best op uw proces lijkt. De voorbeelden geven een eerste richting en maken duidelijk welke gegevens belangrijk zijn voor de vervolgstap.</p>
      {cases}
    ''')
    summary = knowledge_section('samengevat', 'Wat heeft u nodig <em>voor een eerste advies?</em>', f'''
      <ul class="knowledge-checklist">
        <li><strong>Materiaal</strong><span>Producttype, deeltjesgrootte, bulkdichtheid en gevoeligheid voor breuk.</span></li>
        <li><strong>Capaciteit</strong><span>Gewenste hoeveelheid per uur, piekbelasting en batch- of continubedrijf.</span></li>
        <li><strong>Leidingroute</strong><span>Afstand, hoogteverschil, bochten en alle opname- en afgiftepunten.</span></li>
      </ul>
      <div class="knowledge-summary-action">{link("Bespreek uw transportvraag", contact_url(topic))}</div>
    ''')
    article = knowledge_article(hero, takeaway, [
        ('twee-principes', 'Het principe', principles),
        ('druktransport', 'Druktransport', pressure),
        ('vacuumtransport', 'Vacuümtransport', vacuum),
        ('vergelijking', 'Vergelijking', comparison),
        ('uw-product', 'Praktijksituaties', product),
        ('samengevat', 'Voorbereiding op advies', summary),
    ], [
        ('Coperion · Ingredient Transfer & Handling', 'https://coperion.com/en/industries/food-pet-food/ingredient-transfer-handling/'),
        ('Flexicon · Pneumatic Conveying Systems', 'https://flexicon.com/Bulk-Handling-Equipment-and-Systems/Pneumatic-Conveyors/'),
    ])

    more = f'''<section class="knowledge-more" aria-labelledby="meer-title">
  <div class="container">
    <h2 class="h2" id="meer-title">Verder <em>in de proceslijn</em></h2>
    <div class="knowledge-more__grid">
      {card("Cyclonen &amp; afscheiders", "Vergelijk de uitvoeringen", PAGES['categorie'], "27-cycloon-maatwerk",
            "", "ar-16-9", text="Vergelijk systemen die product en lucht bij de bestemming scheiden.")}
      {card("Zo werkt een cycloonafscheider", "Bekijk de interactieve doorsnede", PAGES['product'] + "#werking",
            "13-cycloon-doorsnede", "", "ar-16-9", True, "Volg de lucht- en productstroom door de afscheider.")}
    </div>
  </div>
</section>'''
    body = '\n'.join([article, more, contact('Advies over<br><em>uw transport?</em>',
                      'Vertel ons welk materiaal u verplaatst, hoeveel u nodig heeft en waar het naartoe moet. We denken mee over een passende opstelling.',
                      topic=topic)])
    url = SITE + '/' + PAGES['artikel']
    og = 'og-01-hero-pijpleiding.jpg'
    ld = {'@context': 'https://schema.org', '@type': 'Article', 'headline': headline, 'description': description,
          'image': SITE + '/images/' + og, 'inLanguage': 'nl-NL', 'mainEntityOfPage': url,
          'author': {'@type': 'Organization', 'name': ORG},
          'publisher': {'@type': 'Organization', 'name': ORG, 'logo': {'@type': 'ImageObject', 'url': SITE + '/assets/img/favicon.svg'}}}
    return page(PAGES['artikel'], f'{headline} | Airtechnic Solutions', description, og, body,
                [ld, breadcrumb_jsonld(crumbs, url)], preload_img=(hero_image, KNOWLEDGE_HERO_SIZES),
                html_cls='knowledge-page', stylesheet='assets/css/knowledge-article.css')


# =====================================================================  3. CATEGORIE
def categorie():
    from category_page import category_page
    from cyclone_category_data import CYCLONES
    return category_page('cyclonen', CYCLONES)


# =====================================================================  4. PRODUCT
def product():
    from product_data import PRODUCTS
    from product_page import product_page
    return product_page(PRODUCTS['cycloonafscheider'])
