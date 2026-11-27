"""Verify generated product structure, assets, anchors and catalogue routes."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
sys.path.insert(0,str(ROOT/'tools'))
from structure_norm import normalize, count_faq
from product_data import PRODUCTS
from product_routes import PRODUCT_ROUTES
from components import MANIFEST
from contact_delivery import CONTACT_TOPICS

class Document(HTMLParser):
    def __init__(self):
        super().__init__();self.main=False;self.shape=[];self.ids=[];self.links=[];self.assets=[];self.ld=[];self.in_ld=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='main':self.main=True
        if self.main and tag not in ('br','em','span','strong','svg','path','circle','rect','source','option'):
            self.shape.append((tag,a.get('class','')))
        if self.main and tag=='a':self.links.append(a.get('href',''))
        if tag=='img':self.assets.append(a.get('src',''))
        if tag=='source':self.assets.extend(x.strip().split()[0] for x in a.get('srcset','').split(',') if x.strip())
        if tag=='script' and a.get('type')=='application/ld+json':self.in_ld=True
    def handle_endtag(self,tag):
        if tag=='main':self.main=False
        if tag=='script':self.in_ld=False
    def handle_data(self,data):
        if self.in_ld:self.ld.append(json.loads(data))

documents={}
for filename in [*(s+'.html' for s in PRODUCTS),*('componenten-'+c+'.html' for c in PRODUCT_ROUTES)]:
    p=Document();p.feed((ROOT/filename).read_text(encoding='utf-8'));documents[filename]=p
    s=Document();s.feed(normalize((ROOT/filename).read_text(encoding='utf-8')));p.shape=s.shape
reference=documents['cycloonafscheider.html'].shape
for slug,data in PRODUCTS.items():
    p=documents[slug+'.html']
    assert p.shape==reference,(slug,'structure differs')
    assert len(p.ids)==len(set(p.ids)),(slug,'duplicate IDs')
    for src in p.assets:assert (ROOT/src).is_file(),(slug,src)
    for href in p.links:
        assert href and href!='#',(slug,'placeholder link')
        parts=urlsplit(href)
        if parts.scheme or parts.netloc:continue
        filename=parts.path or slug+'.html'
        assert (ROOT/filename).is_file(),(slug,href)
        if parts.fragment:
            html=(ROOT/filename).read_text(encoding='utf-8')
            assert f'id="{unquote(parts.fragment)}"' in html,(slug,href,'missing anchor')
    assert len(data['views'])==4 and len(data['steps'])==4 and len(data['spec_rows'])==6 and len(data['applications'])==3 and len(data['faq_items'])==6
    assert data['topic'] in CONTACT_TOPICS and data['documentation_topic'] in CONTACT_TOPICS
    assert (ROOT/'images'/f'og-product-{slug}.jpg').exists()
    assert any(x.get('@type')=='Product' and x['name']==data['name'] for x in p.ld)
    assert any(x.get('@type')=='FAQPage' for x in p.ld)
for category,routes in PRODUCT_ROUTES.items():
    links=documents['componenten-'+category+'.html'].links
    for slug in routes.values():assert slug+'.html' in links,(category,slug)
print(f'{len(PRODUCTS)} product pages: identical structure, valid assets, links, enquiry topics and metadata. All 32 category cards link to their product.')
