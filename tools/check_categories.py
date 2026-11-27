from pathlib import Path
from html.parser import HTMLParser
import json,sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
sys.path.insert(0,str(ROOT/'tools'))
from structure_norm import normalize, count_faq
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
    _html=(root/f'componenten-{slug}.html').read_text(encoding='utf-8')
    assert count_faq(_html) in (6,7),(slug,'FAQ count',count_faq(_html))
    parser=Structure();parser.feed(normalize(_html));_ids=Structure();_ids.feed(_html);parser.ids=_ids.ids
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

# Nov 27 · Uitvoeringen (ATEX / food-grade): data drives the truth
import re
from category_data import CATEGORIES as _C
from cyclone_category_data import CYCLONES as _Y
from execution_data import EXECUTIONS, CONFIRMED
import i18n
_items = [('cyclonen', it.variant, it.executions) for it in _Y['items']] + \
         [(c, it['variant'], it['executions']) for c, d in _C.items() for it in d['items']]
for cat, variant, ex in _items:
    assert all(v in EXECUTIONS for v in ex), (cat, variant, 'unknown execution value', ex)
for cat, variant, ex in CONFIRMED:
    assert ex in EXECUTIONS and (cat, variant) in {(c, v) for c, v, _e in _items}, ('CONFIRMED entry unknown', cat, variant, ex)
for cat in ['cyclonen', *_C]:
    has = any(c == cat for c, _v, _e in CONFIRMED)
    for code in i18n.LANGS:
        html = (root / i18n.DIR[code] / i18n.filename(f'componenten-{cat}.html', code)).read_text(encoding='utf-8')
        assert ('data-cv-exec' in html) == has, (cat, code, 'Uitvoering filter group must appear only with confirmed data')
        assert ('cv-card__exec' in html) == has and ('data-uitvoering=' in html) == has, (cat, code, 'execution labels without confirmed data')
print(f'Uitvoeringen: every executions value is in EXECUTIONS; {len(CONFIRMED)} confirmed; filter group only with confirmed data.')

# Safety net: no "certified" wording next to ATEX / EHEDG / food in generated HTML (visible text and attributes)
_bad = re.compile(r'(?i)(?:\b(?:atex|ex|ehedg|food|fda)\b[\w\s\-–·,/]{0,40}?(?:gecertificeerd|certified|zertifiziert))|'
                  r'(?:(?:gecertificeerd|certified|zertifiziert)[\w\s\-–·,/]{0,40}?\b(?:atex|ehedg|food|fda)\b)')
_hits = []
for code in i18n.LANGS:
    for f in sorted((root / i18n.DIR[code]).glob('*.html')) if i18n.DIR[code] else sorted(root.glob('*.html')):
        text = f.read_text(encoding='utf-8')
        text = re.sub(r'<script\b.*?</script>|<style\b.*?</style>', ' ', text, flags=re.S)
        for m in _bad.finditer(re.sub(r'<[^>]+>', ' ', text)):
            _hits.append((f.relative_to(root).as_posix(), ' '.join(m.group(0).split())))
# Known, sourced exception: the dierenvoeding case names third-party "EX-gecertificeerde VDL draaisluizen" (project_data.py)
_allowed = re.compile(r'(?i)^ex[\s-]*(gecertificeerd|certified|zertifiziert)')
_hits = [h for h in _hits if not _allowed.match(h[1])]
assert not _hits, ('certification wording next to ATEX/EHEDG/food', _hits[:10])
print('Wording: no "gecertificeerd / certified / zertifiziert" next to ATEX, EHEDG or food in generated HTML.')
