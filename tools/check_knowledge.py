"""Verify article structure, assets, internal links and homepage discovery."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from knowledge_data import ARTICLES

class Document(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.assets=[];self.links=[];self.sections=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a':self.links.append(a.get('href',''))
        if tag=='img':self.assets.append(a.get('src',''))
        if tag=='source':self.assets.extend(v.strip().split()[0] for v in a.get('srcset','').split(',') if v.strip())
        if tag=='section' and a.get('class')=='knowledge-section':self.sections.append(a['aria-labelledby'])

home=(ROOT/'index.html').read_text(encoding='utf-8')
hub=(ROOT/'kennisbank.html').read_text(encoding='utf-8')
assert 'href="kennisbank.html"' in home
for slug in ['druk-of-vacuumtransport',*ARTICLES]:
    filename='kennis-'+slug+'.html';html=(ROOT/filename).read_text(encoding='utf-8')
    d=Document();d.feed(html)
    assert len(d.ids)==len(set(d.ids)),filename
    paths=len(ARTICLES[slug]['paths']) if slug in ARTICLES else 2   # template: principle + paths + 3 closing sections
    assert len(d.sections)==4+paths,(filename,len(d.sections))
    assert all('#'+s in d.links for s in d.sections),filename
    assert html.count('class="knowledge-flow"')==paths and html.count('name="knowledge-situation"')==3,filename
    assert f'href="{filename}"' in hub,filename
    assert 'kennisbank.html' in d.links,filename
    for a in d.assets:assert (ROOT/a).is_file(),(filename,a)
    for href in d.links:
        u=urlsplit(href)
        if u.scheme or u.netloc or href=='#':continue
        target=ROOT/((u.path.lstrip('/')) or filename)
        assert target.exists(),(filename,href)
        if u.fragment:assert 'id="'+u.fragment+'"' in target.read_text(encoding='utf-8'),(filename,href)
    print(filename+': PASS six sections, navigation, diagrams, scenarios, local links and images')

# Nov 27: fourth group "Veiligheid en hygiëne" with the ATEX article, on the hub and in the homepage list
from knowledge_index import GROUPS
from home_knowledge import TOPICS, TOPIC_OF
assert [g[0] for g in GROUPS]==['transport','scheiden','bulkhandling','veiligheid'],GROUPS
assert 'atex-explosieveiligheid' in dict((g[0],g[2]) for g in GROUPS)['veiligheid']
assert 'id="veiligheid"' in hub and 'href="#veiligheid"' in hub
assert TOPIC_OF['atex-explosieveiligheid']=='veiligheid' and 'veiligheid' in dict(TOPICS)
assert 'data-kq-topic="veiligheid"' in home and 'href="kennis-atex-explosieveiligheid.html"' in home
assert set(TOPIC_OF)==set(ARTICLES),'every article needs a homepage topic'
atex=(ROOT/'kennis-atex-explosieveiligheid.html').read_text(encoding='utf-8')
assert 'value="atex-explosieveiligheid"' in atex,'contact topic preselected'
assert atex.count('href="https://')>=10,'sources'
assert '"@type": "Article"' in atex and '"@type": "BreadcrumbList"' in atex and 'FAQPage' not in atex
print('Knowledge groups: PASS fourth group veiligheid on hub and homepage; ATEX article topic, sources, JSON-LD')
