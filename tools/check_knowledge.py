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
    assert len(d.sections)==6,filename
    assert all('#'+s in d.links for s in d.sections),filename
    assert html.count('class="knowledge-flow"')==2 and html.count('name="knowledge-situation"')==3,filename
    assert f'href="{filename}"' in hub,filename
    assert 'kennisbank.html' in d.links,filename
    for a in d.assets:assert (ROOT/a).is_file(),(filename,a)
    for href in d.links:
        u=urlsplit(href)
        if u.scheme or u.netloc or href=='#':continue
        target=ROOT/(u.path or filename)
        assert target.exists(),(filename,href)
        if u.fragment:assert 'id="'+u.fragment+'"' in target.read_text(encoding='utf-8'),(filename,href)
    print(filename+': PASS six sections, navigation, diagrams, scenarios, local links and images')
