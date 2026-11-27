"""Sector family: sectoren.html (overview) + one fixed layout for every sector page.

Same building blocks as the solution pages (knowledge_intro hero, solution-nav, solution sections, card(), faq(),
contact()); sectors.css imports solutions.css and only adds the sector-specific pieces (issues, linked route
stations, solution links, invitation, overview cards). Data: sector_data.py. Check: tools/check_sectors.py.

Fixed order (README "Sectoren"): hero · uitdagingen · route · oplossingen · componenten · ontwerpeisen · praktijk ·
kennis · vragen · contact. `praktijk` shows real projects only; without a project it is an invitation, never an
empty block or a placeholder.
"""
from html import escape
from components import (SITE, ORG, SOL_IMG, page, pic, card, faq, faq_jsonld, contact, contact_url, link, icon,
                        breadcrumb_jsonld)
from knowledge_article import knowledge_intro, HERO_SIZES
from product_data import PRODUCTS
from project_data import PROJECTS
from solution_data import SOLUTIONS
from knowledge_data import ARTICLES
from sector_data import SECTORS, ORDER, INDEX, INDEX_FILE, sector_file

STYLESHEET = 'assets/css/sectors.css'
CARD_SIZES = '(min-width: 960px) 30vw, (min-width: 640px) 50vw, 100vw'
NAV = [('uitdagingen', 'Vraagstukken'), ('route', 'Productroute'), ('oplossingen', 'Oplossingen'),
       ('componenten', 'Componenten'), ('ontwerpeisen', 'Ontwerpeisen'), ('praktijk', 'Praktijk'),
       ('kennis', 'Kennis'), ('vragen', 'Vragen')]
# The druk/vacuüm article lives on its own template (pages.artikel); give it the same record shape here.
_PRESSURE = dict(name='Druk- of vacuümtransport?', image='01-hero-pijpleiding',
                 description='Vergelijk druk- en vacuümtransport voor poeders, granulaat en pellets.')


def topic(slug):
    return 'sector-' + slug


def article(slug):
    return _PRESSURE if slug == 'druk-of-vacuumtransport' else ARTICLES[slug]


def projects_for(sector):
    return [s for s, p in PROJECTS.items() if sector and p['sector'] == sector]


def _sources(items):
    lis = ''.join(f'<li>{link(escape(label), url)}</li>' for label, url in items)
    return f'<details class="knowledge-sources sector-sources"><summary>Bronnen bij deze pagina {icon("chev-down")}</summary><ul>{lis}</ul></details>'


def sector_page(slug, d):
    filename = sector_file(slug)
    crumbs = [('Home', 'index.html'), ('Sectoren', INDEX_FILE), (d['name'], filename)]
    hero = knowledge_intro(d['title'], crumbs, d['lead'], d['image'], d['alt'], d['caption'],
                           (('Bespreek uw proces', contact_url(topic(slug))), ('Bekijk de productroute', '#route')))
    nav = ('<nav class="solution-nav sector-nav" aria-label="Op deze pagina" data-scrollspy="145"><div class="container">'
           + ''.join(f'<a href="#{i}">{t}</a>' for i, t in NAV) + '</div></nav>')

    issues = ''.join(f'''<li><span class="solution-step" aria-hidden="true">{i:02d}</span><h3 class="h3">{escape(t)}</h3>
      <p>{p}</p><p class="sector-issue__design"><strong>Voor het ontwerp</strong> {o}</p></li>'''
                     for i, (t, p, o) in enumerate(d['issues'], 1))
    s_issues = f'''<section class="solution-section" aria-labelledby="uitdagingen"><div class="container">
  <div class="solution-heading"><h2 class="h2" id="uitdagingen" tabindex="-1">Wat speelt er<br><em>in uw sector?</em></h2>
  <p>{escape(d['long'])}: de vraagstukken die we hier het vaakst tegenkomen, en wat ze betekenen voor het ontwerp van de installatie.</p></div>
  <ol class="sector-issues">{issues}</ol></div></section>'''

    stations = ''.join(f'''<li><span class="solution-step">{i:02d}</span><h3 class="h3">{escape(step)}</h3><p>{escape(text)}</p>
      <a class="sector-route__link" href="oplossingen-{sol}.html">{escape(SOLUTIONS[sol]['name'])}{icon('ur')}</a></li>'''
                       for i, (step, sol, text) in enumerate(d['route'], 1))
    s_route = f'''<section class="solution-section solution-route" aria-labelledby="route"><div class="container">
  <div class="solution-heading"><h2 class="h2" id="route" tabindex="-1">Een typische lijn<br><em>in {escape(d['long'].lower())}.</em></h2>
  <p>Van ontvangst tot afzuigen: elke stap verwijst naar de oplossing die erbij hoort. Uw eigen lijn kan afwijken; we beginnen altijd bij uw proces.</p></div>
  <ol class="solution-stages sector-route" style="--n:{len(d['route'])}">{stations}</ol></div></section>'''

    sols = ''.join(f'''<li><a class="sector-sol" href="oplossingen-{s}.html"><span class="sector-sol__img">{pic(SOL_IMG[SOLUTIONS[s]['name']], '', '88px')}</span>
      <span class="sector-sol__txt"><span class="sector-sol__name">{escape(SOLUTIONS[s]['name'])}</span><span class="sector-sol__why">{escape(why)}</span></span>{icon('ur')}</a></li>'''
                   for s, why in d['solutions'])
    s_solutions = f'''<section class="solution-section" aria-labelledby="oplossingen"><div class="container solution-two">
  <div><h2 class="h2" id="oplossingen" tabindex="-1">Oplossingen<br><em>die hier tellen.</em></h2>
  <p>Per processtap leest u op de oplossingspagina hoe de installatie werkt en welke gegevens we nodig hebben.</p></div>
  <ul class="sector-sols">{sols}</ul></div></section>'''

    cards = ''.join(card(PRODUCTS[s]['name'], 'Bekijk de component', s + '.html', PRODUCTS[s]['image'],
                         PRODUCTS[s]['name'] + ' · illustratieve uitvoering', 'ar-4-3', True, escape(reason))
                    for s, reason in d['components'])
    s_components = f'''<section class="solution-section" aria-labelledby="componenten"><div class="container">
  <div class="solution-heading"><h2 class="h2" id="componenten" tabindex="-1">Componenten die<br><em>hier vaak terugkomen.</em></h2>
  <p>Met de reden waarom ze in deze sector een rol spelen. De uitvoering stemmen we af op uw product en installatie.</p></div>
  <div class="solution-products">{cards}</div></div></section>'''

    reqs = ''.join(f'<div><dt>{escape(t)}</dt><dd>{escape(p)}</dd></div>' for t, p in d['requirements'])
    s_requirements = f'''<section class="solution-section solution-selection" aria-labelledby="ontwerpeisen"><div class="container solution-two">
  <div><h2 class="h2" id="ontwerpeisen" tabindex="-1">Wat de doorslag<br><em>geeft in het ontwerp.</em></h2>
  <p>Deze criteria wegen in {escape(d['long'].lower())} het zwaarst. Ontbrekende gegevens en eventuele tests bespreken we samen.</p>
  {link('Bespreek uw uitgangspunten', contact_url(topic(slug)))}</div>
  <dl class="solution-criteria">{reqs}</dl></div></section>'''

    found = projects_for(d['project_sector'])
    if found:
        pcards = ''.join(card(escape(PROJECTS[p]['short']), 'Bekijk het project', 'project-' + p + '.html', PROJECTS[p]['image'],
                              'Technische projectillustratie: ' + PROJECTS[p]['name'], 'ar-16-10', False,
                              escape(PROJECTS[p]['lead']), sizes=CARD_SIZES) for p in found)
        s_practice = f'''<section class="solution-section" aria-labelledby="praktijk"><div class="container">
  <div class="solution-heading"><h2 class="h2" id="praktijk" tabindex="-1">Uit de praktijk<br><em>in {escape(d['long'].lower())}.</em></h2>
  <div><p>Gerealiseerde projecten in deze sector. Capaciteiten en uitvoeringen gelden voor die installaties.</p>
  {link('Alle projecten in ' + escape(d['name'].lower()), 'projecten.html?sector=' + d['project_sector'] + '#projectenoverzicht')}</div></div>
  <div class="solution-products sector-projects" data-sector-projects>{pcards}</div></div></section>'''
    else:
        s_practice = f'''<section class="solution-section" aria-labelledby="praktijk"><div class="container solution-two sector-invite">
  <div><h2 class="h2" id="praktijk" tabindex="-1">Een vergelijkbaar<br><em>vraagstuk?</em></h2></div>
  <div><p>{escape(d['invite'])}</p><p class="sector-invite__note">Ervaring in deze sector: {d['activity']}</p>
  {link('Beschrijf uw vraagstuk', contact_url(topic(slug)))}</div></div></section>'''

    kcards = ''.join(card(escape(article(k)['name']), 'Lees artikel', 'kennis-' + k + '.html', article(k)['image'], '',
                          'ar-16-9', False, escape(article(k)['description']), sizes=CARD_SIZES) for k in d['knowledge'])
    s_knowledge = f'''<section class="solution-section" aria-labelledby="kennis"><div class="container">
  <div class="solution-heading"><h2 class="h2" id="kennis" tabindex="-1">Verdiep u<br><em>in de techniek.</em></h2>
  <p>Praktische artikelen uit onze kennisbank die in deze sector vaak terugkomen.</p></div>
  <div class="solution-products">{kcards}</div></div></section>'''

    s_questions = f'''<section class="solution-section solution-questions" aria-labelledby="vragen"><div class="container solution-two">
  <div><h2 class="h2" id="vragen" tabindex="-1">Vragen uit<br><em>{escape(d['long'].lower())}.</em></h2>
  {link('Alle sectoren', INDEX_FILE)}{_sources(d['sources'])}</div>{faq(d['faq'], True)}</div></section>'''

    body = '\n'.join([hero, nav, s_issues, s_route, s_solutions, s_components, s_requirements, s_practice, s_knowledge,
                      s_questions, contact('Bespreek<br><em>uw proces.</em>', d['topic_help'], topic=topic(slug))])
    url = SITE + '/' + filename
    og = 'og-sector-' + slug + '.jpg'
    ld = {'@context': 'https://schema.org', '@type': 'WebPage', 'name': d['seo_title'], 'description': d['description'],
          'url': url, 'image': SITE + '/images/' + og, 'publisher': {'@type': 'Organization', 'name': ORG},
          'about': {'@type': 'Thing', 'name': d['long']}}
    return page(filename, d['seo_title'] + ' | Airtechnic Solutions', d['description'], og, body,
                [ld, breadcrumb_jsonld(crumbs, url), faq_jsonld(d['faq'])], preload_img=(d['image'], HERO_SIZES),
                html_cls='knowledge-page solution-page sector-page', stylesheet=STYLESHEET, nav_current='Sectoren')


def sector_index():
    crumbs = [('Home', 'index.html'), ('Sectoren', INDEX_FILE)]
    hero = knowledge_intro(INDEX['title'], crumbs, INDEX['lead'], INDEX['image'], INDEX['alt'],
                           ('Sectoren', 'Illustratieve procesopstelling'),
                           (('Kies uw sector', '#sectoren-overzicht'), ('Bespreek uw proces', contact_url('algemeen'))))
    cards = []
    for i, slug in enumerate(ORDER, 1):
        d = SECTORS[slug]
        points = ''.join(f'<li>{escape(t)}</li>' for t, _p, _o in d['issues'][:2])
        cards.append(f'''<li class="sector-card" style="--i:{i}"><a class="sector-card__link" href="{sector_file(slug)}" data-spotlight>
      <span class="sector-card__img">{pic(d['image'], '', CARD_SIZES)}</span>
      <span class="sector-card__body"><span class="sector-card__no" aria-hidden="true">{i:02d} / {len(ORDER):02d}</span>
      <h3 class="sector-card__name">{escape(d['name'])}<small>{escape(d['long'])}</small></h3>
      <ul class="sector-card__points">{points}</ul>
      <span class="sector-card__go">Bekijk {escape(d['name'].lower())}<span class="visually-hidden">: {escape(d['long'])}</span>{icon('ur')}</span></span></a></li>''')
    body = '\n'.join([hero, f'''<section class="solution-section" aria-labelledby="sectoren-overzicht"><div class="container">
  <div class="solution-heading"><h2 class="h2" id="sectoren-overzicht" tabindex="-1">Uw product<br><em>bepaalt het ontwerp.</em></h2>
  <p>Elke sector heeft eigen vraagstukken: hygiëne in food, routering in feed, slijtage in recycling, materiaalkeuze in de chemie en houtstof in de houtverwerking. Per sector ziet u de typische productroute, de componenten en de vragen die we vaak krijgen.</p></div>
  <ol class="sector-cards">{"".join(cards)}
    <li class="sector-card sector-card--other"><div class="sector-card__body"><h3 class="sector-card__name">Een andere sector?<small>Ook buiten deze vijf</small></h3>
      <p>Werkt u in een andere sector? Vertel ons wat u verwerkt. Het product en het proces bepalen het ontwerp, niet de branche.</p>
      {link('Vertel ons wat u verwerkt', contact_url('algemeen'))}</div></li></ol></div></section>''',
        contact('Uw product.<br><em>Ons ontwerp.</em>', 'Vertel ons welk product u verwerkt en wat u wilt bereiken. Dan bespreken we welke oplossing past.', topic='algemeen')])
    url = SITE + '/' + INDEX_FILE
    items = [{'@type': 'ListItem', 'position': i, 'name': SECTORS[s]['long'], 'url': SITE + '/' + sector_file(s)}
             for i, s in enumerate(ORDER, 1)]
    ld = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': INDEX['seo_title'],
          'description': INDEX['description'], 'url': url,
          'mainEntity': {'@type': 'ItemList', 'numberOfItems': len(items), 'itemListElement': items}}
    return page(INDEX_FILE, INDEX['seo_title'] + ' | Airtechnic Solutions', INDEX['description'], 'og-sector-index.jpg', body,
                [ld, breadcrumb_jsonld(crumbs, url)], preload_img=(INDEX['image'], HERO_SIZES),
                html_cls='knowledge-page solution-page sector-page', stylesheet=STYLESHEET, nav_current='Sectoren')
