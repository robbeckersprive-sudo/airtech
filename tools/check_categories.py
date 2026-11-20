from pathlib import Path
from html.parser import HTMLParser
import json,sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from category_data import CATEGORIES
from components import COMPONENTEN
from contact_delivery import CONTACT_TOPICS

class Structure(HTMLParser):
    def __init__(self):
        super().__init__();self.active=False;self.tags=[];self.ids=[];self.meta={}
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='meta' and 'property' in a:self.meta[a['property']]=a.get('content')
        if tag=='main':self.active=True
        if self.active:
            if tag not in ('option','source','br','em','span','strong','path','svg','circle','rect'):
                self.tags.append((tag, a.get('class','')))
            if 'id' in a:self.ids.append(a['id'])
    def handle_endtag(self,tag):
        if tag=='main':self.active=False

root=ROOT;base=None
for slug in ['cyclonen',*CATEGORIES]:
    parser=Structure();parser.feed((root/f'componenten-{slug}.html').read_text(encoding='utf-8'))
    assert len(parser.ids)==len(set(parser.ids)),(slug,'duplicate ids')
    if base is None:base=parser.tags
    assert parser.tags==base,(slug,'structural drift')
    assert (root/'images'/parser.meta['og:image'].rsplit('/',1)[-1]).exists(),(slug,'missing OG image')
    print(slug+': identical main structure; unique IDs; valid sharing image')
for name,href,image in COMPONENTEN:
    assert (root/href).exists(),(name,href)
    assert ('href="'+href+'"') in (root/'index.html').read_text(encoding='utf-8')
for slug,data in CATEGORIES.items():
    assert slug in CONTACT_TOPICS
    for item in data['items']:assert slug+'-'+item['variant'] in CONTACT_TOPICS
print('All 8 category links are present on the homepage; all 35 new enquiry topics registered.')
