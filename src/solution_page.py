"""One consistent process-oriented layout for all seven solutions."""
from html import escape
from components import (SITE, ORG, page, pic, card, faq, faq_jsonld, contact, contact_url,
                        link, breadcrumb_jsonld)
from knowledge_article import knowledge_intro, HERO_SIZES, knowledge_takeaway, knowledge_scenarios
from product_data import PRODUCTS
from sector_data import SECTORS, SECTORS_OF_SOLUTION, sector_file


def solution_page(slug, d):
    filename='oplossingen-'+slug+'.html'
    crumbs=[('Home','index.html'),('Oplossingen','index.html#specialisaties'),(d['name'],filename)]
    hero=knowledge_intro(d['title'],crumbs,d['lead'],d['image'],d['alt'],
        (d['group'],'Illustratieve procesopstelling'),
        (('Bekijk de procesroute','#werking'),('Bespreek uw toepassing',contact_url(d['topic']))))
    summary=knowledge_takeaway('Uw proces centraal', [('Vertrekpunt',d['focus']),('Samenhang',d['result'])])
    nav='<nav class="solution-nav" aria-label="Op deze pagina" data-scrollspy="145"><div class="container">'+''.join(
        '<a href="#'+i+'">'+t+'</a>' for i,t in [('proces','Procesvraag'),('werking','Werking'),('toepassingen','Toepassingen'),('selectie','Ontwerp'),('componenten','Componenten'),('vragen','Vragen')])+'</div></nav>'
    applied=''.join(f'<li><a href="{sector_file(s)}">{escape(SECTORS[s]["name"])}</a></li>' for s in SECTORS_OF_SOLUTION.get(slug,[]))
    applied=f'<p class="solution-applied"><span>Toegepast in</span></p><ul class="solution-applied__list">{applied}</ul>' if applied else ''
    intro=f'<section class="solution-section" aria-labelledby="proces"><div class="container solution-heading"><h2 id="proces" class="h2" tabindex="-1">Van procesvraag<br><em>naar passende oplossing.</em></h2><div><p>{escape(d["intro"])}</p><p>{escape(d["request"])}</p>{d.get("note","")}{applied}</div></div></section>'
    stages=''.join(f'<li><span class="solution-step">{i:02d}</span><h3 class="h3">{escape(t)}</h3><p>{escape(p)}</p></li>' for i,(t,p) in enumerate(d['steps'],1))
    flow=f'<section class="solution-section solution-route" aria-labelledby="werking"><div class="container"><div class="solution-heading"><h2 class="h2" id="werking" tabindex="-1">Zo loopt<br><em>uw proces.</em></h2><p>Vier samenhangende stappen. De uiteindelijke uitvoering volgt uit uw materiaal, belasting en installatie.</p></div><ol class="solution-stages">{stages}</ol></div></section>'
    cases=f'<section class="solution-section" aria-labelledby="toepassingen"><div class="container solution-two"><div><h2 class="h2" id="toepassingen" tabindex="-1">Herkenbaar<br><em>in de praktijk.</em></h2><p>Bekijk welk uitgangspunt aansluit bij uw situatie. De voorbeelden geven richting aan de technische uitwerking.</p></div>{knowledge_scenarios(d["cases"])}</div></section>'
    criteria=''.join(f'<div><dt>{escape(t)}</dt><dd>{escape(p)}</dd></div>' for t,p in d['criteria'])
    selection=f'<section class="solution-section solution-selection" aria-labelledby="selectie"><div class="container solution-two"><div><h2 class="h2" id="selectie" tabindex="-1">Hierop stemmen we<br><em>het ontwerp af.</em></h2><p>Deze gegevens maken een eerste beoordeling concreet. Ontbrekende informatie en eventuele metingen bespreken we samen.</p>{link("Bespreek uw uitgangspunten",contact_url(d["topic"]))}</div><dl class="solution-criteria">{criteria}</dl></div></section>'
    cards=''.join(card(PRODUCTS[s]['name'],'Bekijk de component',s+'.html',PRODUCTS[s]['image'],PRODUCTS[s]['name']+' · illustratieve uitvoering','ar-4-3',True,PRODUCTS[s]['lead']) for s in d['products'])
    components=f'<section class="solution-section" aria-labelledby="componenten"><div class="container"><div class="solution-heading"><h2 class="h2" id="componenten" tabindex="-1">De bouwstenen<br><em>van uw oplossing.</em></h2><p>Voorbeelden van componenten die een rol kunnen spelen. De combinatie en uitvoering worden per toepassing geselecteerd.</p></div><div class="solution-products">{cards}</div></div></section>'
    questions=f'<section class="solution-section solution-questions" aria-labelledby="vragen"><div class="container solution-two"><div><h2 class="h2" id="vragen" tabindex="-1">Vragen over<br><em>{escape(d["name"].lower())}.</em></h2>{link(*d["knowledge"])}{link(*d["knowledge2"]) if d.get("knowledge2") else ""}</div>{faq(d["faq"],True)}</div></section>'
    body='\n'.join([hero,summary,nav,intro,flow,cases,selection,components,questions,
        contact('Bespreek<br><em>uw toepassing.</em>',d['request'],topic=d['topic'])])
    url=SITE+'/'+filename;og='og-solution-'+slug+'.jpg'
    ld={'@context':'https://schema.org','@type':'Service','name':d['name'],'description':d['lead'],
        'url':url,'provider':{'@type':'Organization','name':ORG},'image':SITE+'/images/'+og}
    return page(filename,d['name']+' | Airtechnic Solutions',d['lead'],og,body,
        [ld,breadcrumb_jsonld(crumbs,url),faq_jsonld(d['faq'])],preload_img=(d['image'],HERO_SIZES),
        html_cls='knowledge-page solution-page',stylesheet='assets/css/solutions.css')
