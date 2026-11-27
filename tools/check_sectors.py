"""Check the sector family (sectoren.html + sectoren-<slug>.html) in nl / en / de, after the model of check_solutions.

- fixed section order and unique IDs on every sector page; identical structure across sectors (practice block aside)
- all internal links and anchors exist; no href="#"
- images are local and registered in images/manifest.json
- every page has its own contact topic that exists in CONTACT_TOPICS and is preselected
- no project block without a project; projects shown = projects whose sector matches; the projecten.html?sector=
  value is a real filter value
- metadata present: title, description, canonical, og:image (file exists), hreflang, BreadcrumbList; FAQPage only
  with answered questions; CollectionPage on the overview
- navigation: Sectoren in header drawer, mobile menu and footer; derived sector chips / "Toegepast in" consistent
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from sector_data import SECTORS, ORDER, INDEX_FILE, sector_file, SECTORS_OF_PRODUCT, SECTORS_OF_SOLUTION
from contact_delivery import CONTACT_TOPICS
from components import MANIFEST
from project_data import PROJECTS
import i18n

SECTIONS = ['uitdagingen', 'route', 'oplossingen', 'componenten', 'ontwerpeisen', 'praktijk', 'kennis', 'vragen', 'contact-title']


class Doc(HTMLParser):
    def __init__(self):
        super().__init__(); self.main = False; self.ids = []; self.links = []; self.assets = []; self.sections = []
        self.meta = {}; self.ld = []; self.in_ld = False; self.canonical = None; self.hreflang = []; self.title = ''
        self.in_title = False; self.shape = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'main': self.main = True
        if tag == 'title': self.in_title = True
        if tag == 'meta': self.meta[a.get('property') or a.get('name')] = a.get('content')
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical = a.get('href')
        if tag == 'link' and a.get('rel') == 'alternate': self.hreflang.append(a.get('hreflang'))
        if tag == 'script' and a.get('type') == 'application/ld+json': self.in_ld = True
        if tag == 'img': self.assets.append(a.get('src', ''))
        if tag == 'source': self.assets.extend(x.strip().split()[0] for x in a.get('srcset', '').split(',') if x.strip())
        if self.main:
            if tag == 'a': self.links.append(a.get('href', ''))
            if tag == 'section' and a.get('aria-labelledby'): self.sections.append(a['aria-labelledby'])

    def handle_endtag(self, tag):
        if tag == 'main': self.main = False
        if tag == 'script': self.in_ld = False
        if tag == 'title': self.in_title = False

    def handle_data(self, data):
        if self.in_ld: self.ld.append(json.loads(data))
        if self.in_title: self.title += data


def check_links(lang_dir, filename, doc):
    for href in doc.links:
        assert href and href != '#', (filename, 'placeholder link')
        u = urlsplit(href)
        if u.scheme or u.netloc: continue
        target = (lang_dir / unquote(u.path)) if u.path else lang_dir / filename
        if u.path.startswith('/'): target = ROOT / u.path.lstrip('/')
        assert target.is_file(), (filename, href)
        if u.fragment:
            assert f'id="{u.fragment}"' in target.read_text(encoding='utf-8'), (filename, href)


def check_assets(lang_dir, filename, doc):
    for src in doc.assets:
        path = (lang_dir / src).resolve()
        assert path.is_file(), (filename, src)
        if path.parent.name != 'images': continue      # logo / favicon live in assets/img
        name = re.sub(r'-\d+\.(avif|webp)$', '', path.name)
        assert name in MANIFEST, (filename, 'not in images/manifest.json', name)


filters = set(p['sector'] for p in PROJECTS.values())
problems = 0
for lang in i18n.LANGS:
    lang_dir = ROOT / i18n.DIR[lang] if i18n.DIR[lang] else ROOT
    ref_shape = None
    for slug in ORDER:
        nl_name = sector_file(slug)
        filename = i18n.filename(nl_name, lang)
        html = (lang_dir / filename).read_text(encoding='utf-8')
        d = Doc(); d.feed(html)
        assert d.sections == SECTIONS, (lang, slug, d.sections)
        assert len(d.ids) == len(set(d.ids)), (lang, slug, 'duplicate ids')
        check_links(lang_dir, filename, d); check_assets(lang_dir, filename, d)
        topic = 'sector-' + slug
        assert topic in CONTACT_TOPICS, topic
        assert f'<option value="{topic}" data-hint=' in html and f'value="{topic}"' in html and f'data-ct-topic="{topic}"' in html, (lang, slug, 'topic')
        assert re.search(rf'<option value="{topic}"[^>]* selected>', html), (lang, slug, 'topic not preselected')
        # practice: real projects only, never an empty block
        expected = [s for s, p in PROJECTS.items() if p['sector'] == SECTORS[slug]['project_sector']]
        shown = re.findall(r'href="(project-[a-z-]+\.html|projekt-[a-z-]+\.html)"', html.split('id="praktijk"', 1)[1].split('</section>', 1)[0])
        assert len(shown) == len(expected), (lang, slug, 'projects', shown, expected)
        if expected:
            assert f'projecten.html?sector={SECTORS[slug]["project_sector"]}' in html or f'?sector={SECTORS[slug]["project_sector"]}' in html
            assert SECTORS[slug]['project_sector'] in filters
            assert 'data-sector-projects' in html
        else:
            assert 'data-sector-projects' not in html and 'sector-invite' in html, (lang, slug, 'empty project block')
        # metadata
        assert d.title.strip() and d.meta.get('description') and d.canonical and d.meta.get('og:image'), (lang, slug, 'meta')
        assert (ROOT / 'images' / d.meta['og:image'].rsplit('/', 1)[-1]).is_file(), (lang, slug, 'og image')
        assert d.canonical.endswith('/' + (i18n.DIR[lang] + filename)), (lang, slug, d.canonical)
        assert {'nl', 'en', 'de', 'x-default'} <= set(d.hreflang), (lang, slug, d.hreflang)
        types = [x.get('@type') for x in d.ld]
        assert 'BreadcrumbList' in types, (lang, slug, types)
        assert ('FAQPage' in types) == any(a for _q, a in SECTORS[slug]['faq']), (lang, slug, 'FAQPage')
        assert not re.search(r'(?i)(gecertificeerd|certified|zertifiziert)', html.split('<main', 1)[1].split('</main>', 1)[0]), (lang, slug, 'certification wording')
        # same skeleton for every sector (practice section content and FAQ count aside)
        shape = [s for s in d.sections]
        ref_shape = ref_shape or shape
        assert shape == ref_shape, (lang, slug, 'structure')
        print(f'{lang} {filename}: PASS order, ids, links, images, topic {topic}, projects {len(expected)}, metadata')
    # overview
    filename = i18n.filename(INDEX_FILE, lang)
    html = (lang_dir / filename).read_text(encoding='utf-8')
    d = Doc(); d.feed(html)
    check_links(lang_dir, filename, d); check_assets(lang_dir, filename, d)
    assert len(d.ids) == len(set(d.ids))
    assert html.count('class="sector-card"') == len(ORDER), 'five sector cards'
    assert 'CollectionPage' in [x.get('@type') for x in d.ld] and 'BreadcrumbList' in [x.get('@type') for x in d.ld]
    assert re.search(r'<option value="algemeen"[^>]* selected>', html), 'overview topic algemeen'
    print(f'{lang} {filename}: PASS overview, five cards, CollectionPage, topic algemeen')
    # navigation: header drawer, mobile pane, footer on a page without sector context
    home = (lang_dir / 'index.html').read_text(encoding='utf-8')
    assert 'data-hx-tab="sec"' in home and 'id="hxb-sec"' in home and 'data-mnav-open="sec"' in home and 'id="mnav-sec"' in home
    for slug in ORDER:
        assert f'href="{i18n.filename(sector_file(slug), lang)}"' in home, (lang, slug, 'nav link')
    assert home.split('<footer', 1)[1].count(f'href="{filename}"') >= 1, (lang, 'footer link')
    # ruler marker rests on Sectoren on sector pages
    page = (lang_dir / i18n.filename(sector_file('food'), lang)).read_text(encoding='utf-8')
    assert re.search(r'class="hxb-link is-current"[^>]*data-hx-tab="sec"', page), (lang, 'nav_current')

# derived relations: one source, no second list
for product, sectors in SECTORS_OF_PRODUCT.items():
    html = (ROOT / (product + '.html')).read_text(encoding='utf-8')
    for s in sectors:
        assert f'href="{sector_file(s)}"' in html.split('detail-sectors', 1)[1], (product, s)
for solution, sectors in SECTORS_OF_SOLUTION.items():
    html = (ROOT / ('oplossingen-' + solution + '.html')).read_text(encoding='utf-8')
    block = html.split('solution-applied__list', 1)[1].split('</ul>', 1)[0]
    assert all(f'href="{sector_file(s)}"' in block for s in sectors), (solution, sectors)
print('Derived sector chips on product pages and "Toegepast in" on solution pages match sector_data.')
print('All sector checks passed.')
