"""One structural template for every component category, including Cyclonen."""
from html import escape
from dataclasses import replace
from product_routes import PRODUCT_ROUTES
from components import (SITE, PAGES, page, pic, link, contact, contact_url, icon, btn, breadcrumb, COMPONENTEN,
                        breadcrumb_jsonld, faq_jsonld, faq_section)
from home_knowledge import faq_block
from components import _v as _vv
from category_overview import CategoryOption, HERO_SIZES, category_intro, category_catalog
from execution_data import EXECUTIONS, confirmed, category_has_confirmed


# ---------------------------------------------------------------- template v2 (Nov 21): "Catalogusblad"
# One structure for all eight groups. Hero with an index of the uitvoeringen (stations with thumbnails), a comparison
# that dims instead of filtering (toepassing chips) and switches between cards and a spec table, the criteria as a
# numbered index, the FAQ index (home_knowledge.faq_block), a rail with the other groups. Styles: category-overview.css
# ("TEMPLATE V2"), behaviour: assets/js/category.js.
CARD_V2 = '(min-width: 1120px) 290px, (min-width: 620px) 46vw, 88vw'


def _group_no(filename):
    hrefs = [h for _t, h, _i in COMPONENTEN]
    return (hrefs.index(filename) + 1 if filename in hrefs else 0), len(hrefs)


def _hero_v2(data, crumbs, items, apps, filename):
    no, total = _group_no(filename)
    tags = ''.join(f'<li>{text}</li>' for _v, text in apps)
    stations = ''.join(
        f'''<li style="--i:{i}"><a href="#oplossing-{item.variant}"><span class="cv-st__img">{pic(item.image, "", "96px")}</span>
          <span class="cv-st__no">{i + 1:02d}</span><span class="cv-st__name" title="{item.name}">{item.name}</span></a></li>''' for i, item in enumerate(items))
    kicker = f'Componenten · {no:02d} / {total:02d}' if no else 'Componenten'
    return f'''<div class="category-sheet cv-sheet">
  <div class="container">
    <div class="category-crumbs">{breadcrumb(crumbs)}</div>
    <section class="category-hero cv-hero" aria-labelledby="cat-h1">
      <div class="category-hero__copy">
        <p class="cv-kicker"><span class="cv-kicker__dot" aria-hidden="true"></span>{kicker}</p>
        <h1 id="cat-h1" class="h1">{data['heading']}</h1>
        <p class="category-hero__lead">{escape(data['intro'])}</p>
        <ul class="cv-tags" aria-label="Toepassingen">{tags}</ul>
        <div class="category-actions">
          {btn("Vergelijk de uitvoeringen", "#cat-grid-title", "lg", icon_name="down")}
          {link("Hulp bij uw keuze", "#advies", "down")}
        </div>
      </div>
      <figure class="category-plate">
        <div class="category-plate__photo">{pic(data['hero'], data.get('hero_alt', data['caption']), HERO_SIZES, eager=True)}</div>
        <figcaption><span>In de installatie</span><span>{escape(data['caption'])}</span></figcaption>
      </figure>
    </section>
    <nav class="cv-index" aria-label="Uitvoeringen op deze pagina"><p class="cv-index__t">{len(items)} uitvoeringen</p><ol>{stations}</ol></nav>
  </div>
</div>'''


def _compare_v2(items, apps, category=''):
    label = dict(apps)
    chips = (f'<button type="button" class="cv-chip" aria-pressed="true" data-cv-app="">Alle toepassingen</button>'
             + ''.join(f'<button type="button" class="cv-chip" aria-pressed="false" data-cv-app="{v}">{t}</button>' for v, t in apps))
    # Uitvoering (ATEX / food-grade): rendered only when Airtechnic confirmed at least one item in this category
    # (execution_data.CONFIRMED). Without confirmed data the page is byte-for-byte what it was.
    with_exec = category_has_confirmed(category)
    shown = {it.variant: confirmed(category, it.variant) for it in items}
    exec_keys = [k for k in EXECUTIONS if any(k in v for v in shown.values())]
    exec_group = ''
    if with_exec:
        exec_group = ('<div class="cv-chips cv-chips--exec" role="group" aria-label="Uitvoering"><span class="cv-chips__t" aria-hidden="true">Uitvoering</span>'
                      '<button type="button" class="cv-chip" aria-pressed="true" data-cv-exec="">Alle</button>'
                      + ''.join(f'<button type="button" class="cv-chip" aria-pressed="false" data-cv-exec="{k}" title="{escape(EXECUTIONS[k]["explain"])}">{EXECUTIONS[k]["chip"]}</button>' for k in exec_keys)
                      + '</div>')
    exec_attr = lambda it: f' data-uitvoering="{" ".join(shown[it.variant])}"' if with_exec else ''
    cards, rows = [], []
    for i, it in enumerate(items):
        tags = ''.join(f'<li>{label[a]}</li>' for a in it.applications.split() if a in label)
        photo = ' cv-card__plate--photo' if it.photo else ''
        exec_tags = ''.join(f'<li>{EXECUTIONS[k]["label"]}</li>' for k in shown[it.variant])
        exec_html = f'<ul class="cv-card__exec" aria-label="Uitvoeringen">{exec_tags}</ul>' if exec_tags else ''
        cards.append(f'''<article class="cv-card" id="oplossing-{escape(it.variant)}" data-cv-item data-toepassing="{escape(it.applications)}"{exec_attr(it)} style="--i:{i}">
        <a class="cv-card__link" href="{it.href}">
          <span class="cv-card__plate{photo}">{pic(it.image, it.alt, CARD_V2)}<span class="cv-card__no">{i + 1:02d}<small>/{len(items):02d}</small></span></span>
          <span class="cv-card__body">
            <h3 class="cv-card__name" data-eq>{escape(it.name)}</h3>
            <dl class="cv-card__spec"><div><dt>Kenmerk</dt><dd>{escape(it.feature)}</dd></div><div><dt>Past bij</dt><dd>{escape(it.use)}</dd></div></dl>
            <ul class="cv-card__tags">{tags}</ul>{exec_html}
            <span class="cv-card__go">{it.action}<span class="visually-hidden"> · {escape(it.name)}</span>{icon("ur")}</span>
          </span>
        </a>
      </article>''')
        exec_cell = (f'<td>{", ".join(EXECUTIONS[k]["fact"] for k in shown[it.variant]) or "—"}</td>' if with_exec else '')
        rows.append(f'''<tr data-cv-item data-toepassing="{escape(it.applications)}"{exec_attr(it)}><th scope="row"><span class="cv-t__img">{pic(it.image, "", "72px")}</span>{escape(it.name)}</th>
          <td>{escape(it.feature)}</td><td>{escape(it.use)}</td><td>{", ".join(label[a] for a in it.applications.split() if a in label)}</td>{exec_cell}
          <td><a href="{it.href}" aria-label="Bekijk {escape(it.name)}">{icon("ur")}</a></td></tr>''')
    return f'''<section class="section category-catalog cv-compare" aria-labelledby="cat-grid-title" data-cv>
  <div class="container">
    <header class="category-heading">
      <h2 id="cat-grid-title" class="h2">Vergelijk <em>de uitvoeringen</em></h2>
      <p>Bekijk per uitvoering het belangrijkste kenmerk en waar zij past. Kies uw toepassing: wat erbij past, blijft in beeld.</p>
    </header>
    <div class="cv-bar">
      <div class="cv-chips" role="group" aria-label="Toepassing">{chips}</div>{exec_group}
      <p class="cv-count" role="status" data-cv-count>{len(items)} van {len(items)} uitvoeringen</p>
      <div class="cv-view" role="group" aria-label="Weergave"><button type="button" aria-pressed="true" data-cv-view="cards">Kaarten</button><button type="button" aria-pressed="false" data-cv-view="table">Tabel</button></div>
    </div>
    <div class="cv-cards" id="cat-grid" data-cv-cards>{"".join(cards)}</div>
    <div class="cv-table-wrap" data-cv-table hidden><table class="cv-table"><caption class="visually-hidden">Uitvoeringen vergeleken</caption>
      <thead><tr><th scope="col">Uitvoering</th><th scope="col">Kenmerk</th><th scope="col">Past bij</th><th scope="col">Toepassing</th>{'<th scope="col">Uitvoeringen</th>' if with_exec else ''}<th scope="col"><span class="visually-hidden">Link</span></th></tr></thead>
      <tbody>{"".join(rows)}</tbody></table></div>
  </div>
</section>'''


def _related_v2(filename, extra=None):
    others = [(t, h, img) for t, h, img in COMPONENTEN if h != filename]
    extra_link = link(*extra) if extra else ''
    lis = ''.join(f'<li><a href="{h}"><span class="cv-rel__img">{pic(img, "", "120px")}</span><span class="cv-rel__name" data-eq>{t}</span>{icon("ur")}</a></li>' for t, h, img in others)
    return f'''<section class="cv-related" aria-labelledby="rel-title">
  <div class="container">
    <div class="cv-related__head"><h2 id="rel-title" class="h3">Verder in de installatie</h2>{link("Druk- of vacuümtransport?", PAGES["artikel"])}{extra_link}{link("Alle componenten", "componenten.html")}</div>
    <ul class="cv-rel">{lis}</ul>
  </div>
</section>'''


def category_page(slug, data):
    filename = f'componenten-{slug}.html'
    topic = data.get('topic', slug)
    name = data['name']
    crumbs = [('Home', 'index.html'), ('Componenten', 'componenten.html'),
              (data.get('crumb', name), filename)]
    items = []
    for item in data['items']:
        if isinstance(item, CategoryOption):
            items.append(replace(item, href=PRODUCT_ROUTES[slug][item.variant]+'.html', action='Bekijk de uitvoering'))
        else:
            items.append(CategoryOption(**item, alt=item['name'] + ' · illustratieve uitvoering',
                                        href=PRODUCT_ROUTES[slug][item['variant']]+'.html',
                                        action='Bekijk de uitvoering'))
    hero = _hero_v2(data, crumbs, items, data['applications'], filename)
    catalog = _compare_v2(items, data['applications'], slug)
    criteria = ''.join(f'<div><dt>{escape(title)}</dt><dd>{escape(text)}</dd></div>' for title, text in data['criteria'])
    advice = f'''<section class="section category-advice cv-advice" id="advies" aria-labelledby="advies-title">
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
    faq_title = f"Veelgestelde vragen over<br><em>{data.get('crumb', name).lower()}.</em>"
    body = '\n'.join([hero, catalog, advice, faq_block(questions, faq_title, card=False, cls='section'), _related_v2(filename, data.get('related_extra')),
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
        stylesheet='assets/css/category-overview.css').replace('</main>', '<script src="' + _vv('assets/js/category.js') + '" defer></script>\n<script src="' + _vv('assets/js/home-knowledge.js') + '" defer></script>\n</main>', 1)
