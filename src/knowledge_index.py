"""Topic index for the editorial knowledge base."""
from html import escape
from html.parser import HTMLParser
from knowledge_page import knowledge_page
from pages import artikel
from components import SITE, _v, breadcrumb, breadcrumb_jsonld, card, icon, page, pic
from knowledge_data import ARTICLES

FILENAME = 'kennisbank.html'
HERO = '20-project-recycling'
SIZES = '(min-width: 1000px) 44vw, (min-width: 740px) 50vw, 100vw'
GROUPS = (
    ('transport', 'Pneumatisch transport', (
        'druk-of-vacuumtransport', 'juiste-blower-selecteren', 'slijtage-transportbochten')),
    ('scheiden', 'Filtreren en scheiden', (
        'wanneer-filters-vervangen', 'cycloon-als-voorafscheider', 'controlezeef-of-fractioneerzeef')),
    ('bulkhandling', 'Opslag en dosering', (
        'bigbag-lossen-onregelmatige-productstroom', 'silo-ontluchting-pneumatisch-vullen', 'doorvalsluis-of-doorblaassluis')),
)
PRESSURE_ARTICLE = dict(name='Druk- of vacuümtransport?', image='01-hero-pijpleiding',
    description='Volg het poeder van afnamepunt tot bestemming en vergelijk de rol van overdruk en onderdruk in uw leidingtracé.')



class ArticleText(HTMLParser):
    """Extract the rendered editorial text for the search index."""
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, text):
        self.parts.append(text)


def article_search_text(slug, data):
    html = artikel() if slug == 'druk-of-vacuumtransport' else knowledge_page(slug, data)
    article = html.split('<article class="knowledge-article"', 1)[1].split('</article>', 1)[0]
    parser = ArticleText()
    parser.feed('<article' + article + '</article>')
    return ' '.join(' '.join(parser.parts).split())


def knowledge_index():
    records = {'druk-of-vacuumtransport': PRESSURE_ARTICLE, **ARTICLES}
    crumbs = [('Home', 'index.html'), ('Kennisbank', FILENAME)]
    options = []
    jumps = []
    sections = []
    entries = []
    for anchor, label, slugs in GROUPS:
        options.append(f'<option value="{anchor}">{label}</option>')
        jumps.append(f'<a href="#{anchor}">{label}{icon("down")}</a>')
        cards = []
        for slug in slugs:
            data = records[slug]
            url = 'kennis-' + slug + '.html'
            cards.append(card(escape(data['name']), 'Lees artikel', url, data['image'],
                              ratio='ar-16-9', text=escape(data['description']),
                              attrs=' data-search-text="' + escape(article_search_text(slug, data), quote=True) + '"'))
            entries.append({'@type': 'ListItem', 'position': len(entries) + 1,
                            'name': data['name'], 'url': SITE + '/' + url})
        sections.append(f'<section class="kb-group" aria-labelledby="{anchor}"><h2 id="{anchor}" class="h2" tabindex="-1">{label}</h2>'
                        f'<div class="kb-cards">{"".join(cards)}</div></section>')
    title = 'Kennisbank voor luchttechniek en bulkhandling'
    description = 'Praktische artikelen over pneumatisch transport, filtratie, scheiding en bulkhandling. Vergelijk uitvoeringen en herken knelpunten in uw installatie.'
    body = f"""<div class="kb-head"><div class="container">{breadcrumb(crumbs)}
    <div class="kb-intro"><div><h1 class="h1">Kennisbank<br><em>luchttechniek.</em></h1>
    <p>Hoe kiest u een transportbocht? Wanneer is een filter aan vervanging toe? Vind de afwegingen, meetgegevens en praktijkvoorbeelden voor uw installatie.</p></div>
    <figure>{pic(HERO, 'Industriële procesinstallatie met leidingwerk en cyclonen', SIZES, eager=True)}</figure></div>
    <div class="kb-controls" hidden>
      <div class="kb-fields" role="search" aria-label="Kennisbank">
        <label>Zoek in de kennisbank<input type="search" id="kb-search" placeholder="Bijvoorbeeld filter of transportbocht"></label>
        <div><label for="kb-topic">Onderwerp</label><select id="kb-topic"><option value="">Alle onderwerpen</option>{"".join(options)}</select></div>
      </div>
      <div class="kb-feedback"><p role="status" id="kb-count"></p><button type="button" id="kb-reset" hidden>Toon alle artikelen</button></div>
    </div>
    <nav class="kb-topics" aria-label="Onderwerpen">{"".join(jumps)}</nav></div></div>
    <div class="container kb-library">{"".join(sections)}</div>
    <script defer src="{_v('assets/js/knowledge-index.js')}"></script>"""
    collection = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': title,
                  'description': description, 'url': SITE + '/' + FILENAME, 'inLanguage': 'nl-NL',
                  'mainEntity': {'@type': 'ItemList', 'numberOfItems': len(entries), 'itemListElement': entries}}
    return page(FILENAME, title + ' | Airtechnic Solutions', description, 'og-20-project-recycling.jpg',
                body, [collection, breadcrumb_jsonld(crumbs, SITE + '/' + FILENAME)],
                preload_img=(HERO, SIZES), stylesheet='assets/css/knowledge-index.css')
