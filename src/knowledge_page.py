"""Render editorial records with the approved pressure/vacuum article components."""
from html import escape
from components import SITE, ORG, page, card, contact, contact_url, link, breadcrumb_jsonld
from knowledge_article import (HERO_SIZES, knowledge_intro, knowledge_takeaway,
    knowledge_section, knowledge_flow, knowledge_comparison, knowledge_scenarios, knowledge_article)


def knowledge_page(slug, d):
    filename = 'kennis-' + slug + '.html'
    crumbs = [('Home','index.html'),('Kennisbank','kennisbank.html'),(d['name'],filename)]
    hero = knowledge_intro(d['title'], crumbs, d['intro'], d['image'], d['alt'], d['caption'],
                           (('Naar de vergelijking','#vergelijking'),('Waar begint u?','#het-principe')))
    paragraphs = lambda items: ''.join('<p>'+escape(p)+'</p>' for p in items)
    legend = '<ul class="knowledge-legend" aria-label="Leeswijzer bij de schema’s">'+''.join(
        '<li><span aria-hidden="true"></span>'+escape(t)+'</li>' for t in d['legend'])+'</ul>'
    sections = [('het-principe','Het uitgangspunt',knowledge_section('het-principe',d['principle_title'],paragraphs(d['principle'])+legend))]
    for i, path in enumerate(d['paths']):
        flow = knowledge_flow(path['nav'],path['stages'],i==0,path['caption'])
        # optional per section (ATEX article): a schematic figure, a marked note (may hold a tbd()), and onward links
        figure = path.get('figure', '')
        note = '<p class="knowledge-note">'+path['note']+'</p>' if path.get('note') else ''
        links = ('<ul class="knowledge-links">'+''.join('<li>'+link(escape(t),h)+'</li>' for t,h in path['links'])+'</ul>') if path.get('links') else ''
        sections.append((path['id'],path['nav'],knowledge_section(path['id'],path['title'],paragraphs([path['before']])+flow+figure+paragraphs([path['after']])+note+links)))
    if d.get('practice'):
        # "Uit eigen werk": verified project wording only (project_data.py), linked to the project pages
        items = ''.join('<li><strong>'+link(escape(t),h)+'</strong><span>'+escape(x)+'</span></li>' for t,h,x in d['practice'])
        sections[-1] = (sections[-1][0], sections[-1][1], sections[-1][2].replace('</section>',
            '<div class="knowledge-practice"><h3 class="h3">Uit eigen werk</h3><ul>'+items+'</ul></div></section>'))
    sections.append(('vergelijking','Vergelijking',knowledge_section('vergelijking',d['comparison_title'],
        paragraphs([d['comparison_intro']])+knowledge_comparison(d['name'],d['headings'],d['rows']))))
    sections.append(('uw-situatie','Praktijksituaties',knowledge_section('uw-situatie','Van inzicht <em>naar uw situatie</em>',
        '<p>Herken uw situatie en bekijk welke informatie de volgende stap helpt bepalen.</p>'+knowledge_scenarios(d['scenarios']))))
    checklist = '<ul class="knowledge-checklist">'+''.join('<li><strong>'+escape(a)+'</strong><span>'+escape(b)+'</span></li>' for a,b in d['checklist'])+'</ul>'
    sections.append(('samengevat','Voorbereiding op advies',knowledge_section('samengevat','Wat heeft u nodig <em>voor een eerste advies?</em>',
        checklist+'<div class="knowledge-summary-action">'+link(d['action'],contact_url(d['topic']))+'</div>')))
    article = knowledge_article(hero,knowledge_takeaway('Kort antwoord',d['takeaway']),sections,d['sources'])
    cards = ''.join(card(title,action,url,img,'','ar-16-9',contain,text) for title,action,url,img,contain,text in d['related'])
    more = '<section class="knowledge-more" aria-labelledby="meer-title"><div class="container"><h2 class="h2" id="meer-title">Verder <em>in de proceslijn</em></h2><div class="knowledge-more__grid">'+cards+'</div></div></section>'
    body = '\n'.join([article,more,contact(d['contact_title'],d['contact_intro'],topic=d['topic'])])
    og = d.get('og', 'og-knowledge-'+slug+'.jpg')
    url = SITE+'/'+filename
    ld = {'@context':'https://schema.org','@type':'Article','headline':d['name'],'description':d['description'],
          'image':SITE+'/images/'+og,'inLanguage':'nl-NL','mainEntityOfPage':url,
          'author':{'@type':'Organization','name':ORG},
          'publisher':{'@type':'Organization','name':ORG,'logo':{'@type':'ImageObject','url':SITE+'/assets/img/favicon.svg'}}}
    return page(filename,d.get('seo_title',d['name'])+' | Airtechnic Solutions',d['description'],og,body,
                [ld,breadcrumb_jsonld(crumbs,url)],preload_img=(d['image'],HERO_SIZES),
                html_cls='knowledge-page',stylesheet='assets/css/knowledge-article.css')
