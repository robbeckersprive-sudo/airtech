"""Check consistent solution structure and real local destinations."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
sys.path.insert(0,str(ROOT/'tools'))
from structure_norm import normalize, count_faq
from solution_data import SOLUTIONS
from components import OPLOSSINGEN
class Document(HTMLParser):
    def __init__(self):
        super().__init__();self.main=False;self.shape=[];self.links=[];self.assets=[];self.ids=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='main':self.main=True
        if 'id' in a:self.ids.append(a['id'])
        if self.main:
            self.shape.append((tag,a.get('class','')))
            if tag=='a':self.links.append(a.get('href',''))
        if tag=='img':self.assets.append(a['src'])
        if tag=='source':self.assets.extend(x.strip().split()[0] for x in a['srcset'].split(','))
    def handle_endtag(self,tag):
        if tag=='main':self.main=False
reference=None
for slug in SOLUTIONS:
    filename='oplossingen-'+slug+'.html';_html=(ROOT/filename).read_text(encoding='utf-8');d=Document();d.feed(_html)
    assert count_faq(_html) in (3,4),(slug,'FAQ count')
    _n=Document();_n.feed(normalize(_html));d.shape=_n.shape
    if reference is None:reference=d.shape
    assert reference==d.shape,(slug,'inconsistent structure')
    assert len(d.ids)==len(set(d.ids)),slug
    for asset in d.assets:assert (ROOT/asset).is_file(),(slug,asset)
    for href in d.links:
        assert href and href!='#',(slug,'placeholder')
        u=urlsplit(href)
        if u.scheme or u.netloc:continue
        path=ROOT/(u.path or filename);assert path.is_file(),(slug,href)
        if u.fragment:assert 'id="'+u.fragment+'"' in path.read_text(encoding='utf-8'),(slug,href)
    assert (ROOT/'images'/('og-solution-'+slug+'.jpg')).exists()
    print(slug+': PASS identical structure, links, anchors, images and sharing asset')
assert {h for _,items in OPLOSSINGEN for _,h in items}=={'oplossingen-'+s+'.html' for s in SOLUTIONS}
print('All seven navigation entries match the solution pages.')
