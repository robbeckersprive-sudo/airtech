"""The cycloonafscheider structure, shared verbatim by all product pages."""
from html import escape
from components import (SITE, ORG, pic, media, link, contact, contact_url, page, icon, COMPONENTEN, _v,
                        breadcrumb_jsonld, faq_jsonld, faq_section)
from home_knowledge import faq_block
from product_routes import PRODUCT_ROUTES
from component_detail import GALLERY_SIZES, component_intro, component_nav, component_principle


def product_page(d):
    name, slug = d['name'], d['slug']
    filename = slug+'.html'
    category_url = 'componenten-'+d['category']+'.html'
    crumbs = [('Home','index.html'),('Componenten','componenten.html'),
              (d['family_name'],category_url),(name,filename)]
    hrefs = [h for _t, h, _i in COMPONENTEN]
    g = hrefs.index(category_url) + 1 if category_url in hrefs else 0
    family = list(PRODUCT_ROUTES.get(d['category'], {}).values())
    k = family.index(slug) + 1 if slug in family else 0
    kicker = f"{escape(d['family_name'])}" + (f" · {g}.{k}" if g and k else '')
    hero = component_intro(name, crumbs, d['lead'], d['facts'], d['views'], contact_url(d['topic']), kicker=kicker)
    subnav = component_nav([('overzicht','Overzicht'),('werking','Werking'),('uitvoering','Selectie'),
                           ('toepassingen','Toepassingen'),('faq-title','Vragen')])
    werking = component_principle(d['principle_title'], d['principle_intro'], d['cutaway'],
        name+' · schematische doorsnede', d['steps'], d['note'], d['step_heading'])
    trs = ''.join(f'<tr><th scope="row">{k}</th><td>{escape(v)}</td></tr>' for k,v in d['spec_rows'])
    uitvoering = f'''<section class="section detail-selection" id="uitvoering" aria-labelledby="uitv-title">
  <div class="container detail-selection__grid">
    <div>
      <h2 id="uitv-title" class="h2">Afgestemd op<br><em>uw proces</em></h2>
      <p>{escape(d['selection_intro'])}</p>
      <aside class="detail-documentation" aria-labelledby="detail-doc-title">
        <h3 class="h3" id="detail-doc-title">Technische documentatie</h3>
        <p>Vraag informatie aan over inbouwmaten, aansluitingen, materialen of procescondities.</p>
        {link('Vraag documentatie aan',contact_url(d['documentation_topic']))}
      </aside>
    </div>
    <table class="detail-specs">
      <caption class="visually-hidden">Selectiecriteria voor {escape(name)}</caption>
      <thead><tr><th scope="col">Criterium</th><th scope="col">Waar we op letten</th></tr></thead>
      <tbody>{trs}</tbody>
    </table>
  </div>
</section>'''
    uses=''.join(f'<div><dt>{escape(title)}</dt><dd>{escape(text)}</dd></div>' for title,text in d['applications'])
    toepassingen = f'''<section class="section detail-section" id="toepassingen" aria-labelledby="toep-title">
  <div class="container">
    <header class="detail-section__head">
      <h2 id="toep-title" class="h2">{d['context_title']}</h2>
      <p>{escape(d['context_intro'])}</p>
    </header>
    <div class="detail-context">
      <figure>
        {pic(d['context_image'],d['context_caption'],'(min-width: 1240px) 710px, (min-width: 900px) 57vw, 94vw')}
        <figcaption>{escape(d['context_caption'])}</figcaption>
      </figure>
      <dl class="detail-use">{uses}</dl>
    </div>
    <p class="detail-sectors"><strong>{'Sectoren' if slug=='cycloonafscheider' else 'Toepasbaarheid'}</strong> <span>{escape(d['sectors'])}</span></p>
  </div>
</section>'''
    related_cards=''.join(f'''<li style="--i:{i}"><a class="pd-rel" href="{href}">
          <span class="pd-rel__plate">{pic(image,"","(min-width: 900px) 30vw, 88vw")}</span>
          <span class="pd-rel__name" data-eq>{escape(label)}{icon("ur")}</span><span class="pd-rel__text" data-eq>{escape(text)}</span></a></li>'''
                          for i,(label,image,text,href) in enumerate(d['related']))
    related=f'''<section class="detail-related" aria-labelledby="relc-title">
  <div class="container">
    <header class="detail-section__head">
      <h2 id="relc-title" class="h2">{d['related_title']}</h2>
      {link('Alle '+escape(d['family_name']).lower(), category_url)}
    </header>
    <ul class="detail-related__grid">{related_cards}</ul>
  </div>
</section>'''
    body='\n'.join([hero,subnav,werking,uitvoering,toepassingen,related,
        faq_block(d['faq_items'], f"Veelgestelde vragen over<br><em>{escape(name).lower()}.</em>", card=False, cls='section'),
        contact(d['contact_title'],d['contact_intro'],topic=d['topic'],topics=(d['documentation_topic'],))])
    url=SITE+'/'+filename
    og='og-product-'+slug+'.jpg'
    product={'@context':'https://schema.org','@type':'Product','name':name,'category':d['family_name'],
             'description':d['lead'],'image':[SITE+'/images/'+og],'brand':{'@type':'Brand','name':ORG},'url':url}
    return page(filename,name+' op maat | Airtechnic Solutions',d['lead'],og,body,
                [product,breadcrumb_jsonld(crumbs,url),faq_jsonld(d['faq_items'])],
                preload_img=(d['image'],GALLERY_SIZES),html_cls='has-subnav component-detail',
                nav_current=d['nav'],stylesheet='assets/css/component-detail.css').replace('</main>', '<script src="'+_v('assets/js/home-knowledge.js')+'" defer></script>\n<script src="'+_v('assets/js/subnav.js')+'" defer></script>\n</main>', 1)
