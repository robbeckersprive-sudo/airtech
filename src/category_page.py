"""One structural template for every component category, including Cyclonen."""
from html import escape
from dataclasses import replace
from product_routes import PRODUCT_ROUTES
from components import (SITE, PAGES, page, pic, link, contact, contact_url,
                        breadcrumb_jsonld, faq_jsonld, faq_section)
from category_overview import CategoryOption, HERO_SIZES, category_intro, category_catalog


def category_page(slug, data):
    filename = f'componenten-{slug}.html'
    topic = data.get('topic', slug)
    name = data['name']
    crumbs = [('Home', 'index.html'), ('Componenten', 'index.html#comp-title'),
              (data.get('crumb', name), filename)]
    items = []
    for item in data['items']:
        if isinstance(item, CategoryOption):
            items.append(replace(item, href=PRODUCT_ROUTES[slug][item.variant]+'.html', action='Bekijk de uitvoering'))
        else:
            items.append(CategoryOption(**item, alt=item['name'] + ' · illustratieve uitvoering',
                                        href=PRODUCT_ROUTES[slug][item['variant']]+'.html',
                                        action='Bekijk de uitvoering'))
    hero = category_intro(data['heading'], crumbs, data['intro'], data['hero'],
                          data.get('hero_alt', data['caption']), data['caption'])
    catalog = category_catalog('Vergelijk <em>de uitvoeringen</em>',
        'Bekijk per uitvoering het belangrijkste kenmerk en waar zij past. Zoek op trefwoord of filter op uw proces.',
        items, data['applications'], [(item.variant, item.name) for item in items], contact_url(topic))
    criteria = ''.join(f'<div><dt>{escape(title)}</dt><dd>{escape(text)}</dd></div>' for title, text in data['criteria'])
    advice = f'''<section class="section category-advice" id="advies" aria-labelledby="advies-title">
  <div class="container">
    <header class="category-heading">
      <h2 id="advies-title" class="h2">Welke uitvoering past <em>bij uw proces?</em></h2>
      <p>Gebruik deze uitgangspunten om een keuze voor te bereiden. We beoordelen ze samen, inclusief de aansluiting op de rest van uw installatie.</p>
    </header>
    <div class="category-advice__grid">
      <div>
        <dl class="category-criteria">{criteria}</dl>
        {link('Bespreek uw uitgangspunten', contact_url(topic))}
      </div>
      <figure class="category-plate category-cutaway">
        <div class="category-cutaway__image">
          {pic(data['cutaway'], data.get('cutaway_alt', data['principle'] + ' · schematische doorsnede'), '(min-width: 900px) 280px, 48vw')}
          <div>
            <h3 class="h3">{escape(data['principle'])}</h3>
            <p>{escape(data['explanation'])}</p>
            {link(data.get('principle_action', 'Bekijk de werking'), data.get('principle_href', items[0].href+'#werking'))}
          </div>
        </div>
        <figcaption><span>Doorsnede</span><span>Werkingsprincipe · niet op schaal</span></figcaption>
      </figure>
    </div>
  </div>
</section>'''
    questions = data.get('faq') or [*data['questions'],
        ('Is inbouw in een bestaande installatie mogelijk?',
         'We beoordelen de aansluitingen, capaciteit en beschikbare inbouwruimte samen met de bestaande processtappen. Deel een tekening of foto en beschrijf wat u wilt verbeteren.'),
        ('Welke gegevens zijn nodig voor gericht advies?', data['request'] + ' Een tekening of foto van de huidige situatie helpt bij de beoordeling. Ontbrekende gegevens bespreken we tijdens de analyse.'),
        ('Waarvan hangen uitvoering en kosten af?',
         'Afmetingen, materiaalkeuze, aandrijving en benodigde toebehoren bepalen de uitvoering. Ook montage, besturing en aansluiting op de bestaande installatie tellen mee. Een offerte volgt op de vastgelegde uitgangspunten en leveringsomvang.')]
    related = f'''<section class="category-related" aria-labelledby="rel-title">
  <div class="container">
    <h2 id="rel-title" class="h3">Verder in de installatie</h2>
    <ul>
      <li>{link('Druk- of vacuümtransport', PAGES['artikel'])}</li>
      <li>{link('Alle componenten', 'index.html#comp-title')}</li>
    </ul>
  </div>
</section>'''
    topics = data.get('topics', tuple(topic + '-' + item.variant for item in items))
    body = '\n'.join([hero, catalog, advice, faq_section('Veelgestelde vragen', questions, 'faq-title'), related,
        contact(data.get('contact_title', 'Samen de juiste uitvoering kiezen?'), data['request'], topic=topic, topics=topics)])
    url = SITE + '/' + filename
    item_list = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': name,
        'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': item.name,
          'url': SITE + '/' + item.href if item.href.endswith('.html') else url + '#oplossing-' + item.variant}
          for i, item in enumerate(items)]}
    return page(filename, data.get('title', name + ' op maat | Airtechnic Solutions'),
        data.get('description', data['intro']), data.get('og', 'og-' + data['hero'] + '.jpg'), body,
        [item_list, breadcrumb_jsonld(crumbs, url), faq_jsonld(questions)],
        preload_img=(data['hero'], HERO_SIZES), nav_current=data['nav'], html_cls='category-overview',
        stylesheet='assets/css/category-overview.css')
