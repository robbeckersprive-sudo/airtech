"""Project collection and a single editorial template for every case."""
from html import escape as e
from components import SITE, page, pic, link, btn, icon, breadcrumb, breadcrumb_jsonld, contact, contact_url
from knowledge_article import knowledge_intro, HERO_SIZES
from project_data import PROJECTS


def project_card(slug, d):
    return f'''<article class="project-card" data-project data-sector="{e(d['sector'])}" data-category="{e(d['category'])}">
    <a class="project-card__image" href="project-{slug}.html" tabindex="-1" aria-hidden="true">{pic(d['image'], '', '(min-width: 900px) 44vw, 94vw')}<span>Projectillustratie</span></a>
    <div class="project-card__body"><p class="project-label">{e(d['sector'])} <span>/</span> {e(d['category'])}</p>
    <h3 class="h3"><a href="project-{slug}.html">{e(d['short'])}{icon('ur')}</a></h3><p>{e(d['lead'])}</p>
    <div class="project-card__fact"><strong>{e(d['facts'][0][0])}</strong><span>{e(d['facts'][0][1])}</span></div></div></article>'''


def project_index():
    crumbs=[('Home','index.html'),('Projecten','projecten.html')]
    hero=knowledge_intro('Projecten.<br><em>Techniek in de praktijk.</em>',crumbs,
       'Bekijk hoe transport, verwerking en luchttechniek samenkomen in onze projecten. Van een afzonderlijk vacuümnetwerk tot een complete recyclinglijn.',
       'project-pet','Illustratieve opstelling van transport, opslag en bigbag-vulling voor PET-recycling',
       ('Projecten / Airtechnic','Technische projectillustratie'),
       (('Ontdek de projecten','#projectenoverzicht'),('Bespreek uw project',contact_url('installatieontwerp'))))
    opts=lambda values: ''.join(f'<option value="{e(v)}">{e(v)}</option>' for v in sorted(set(values)))
    cards=''.join(project_card(s,d) for s,d in PROJECTS.items())
    cards += '<aside class="project-invitation" data-project-invitation><p class="project-label">Uw volgende stap</p><h3 class="h2">Een eigen<br><em>procesvraag?</em></h3><p>Een nieuw leidingtracé, betere stofbeheersing of een complete verwerkingslijn. Vertel ons waar uw uitdaging ligt.</p>'+link('Bespreek uw project',contact_url('installatieontwerp'))+'</aside>'
    body=hero+f'''<section class="project-library" aria-labelledby="projectenoverzicht"><div class="container">
    <div class="project-library__head"><div><p class="project-label">Projecten / Case studies</p><h2 id="projectenoverzicht" class="h2" tabindex="-1">Techniek die werkt.<br><em>In uw praktijk.</em></h2></div><p>Zoek op materiaal, toepassing of opdrachtgever. Elk verhaal brengt de vraag, de technische keuzes en de gerealiseerde installatie bij elkaar.</p></div>
    <form class="project-filters" data-project-filters hidden role="search" aria-label="Projecten zoeken en filteren">
    <div class="project-filter-fields"><label for="project-query">Zoek een project<input id="project-query" name="q" type="search" placeholder="Bijvoorbeeld: eierschalen, vacuüm" autocomplete="off"></label>
    <label for="project-sector">Sector<select name="sector" id="project-sector"><option value="">Alle sectoren</option>{opts(d['sector'] for d in PROJECTS.values())}</select></label>
    <label for="project-category">Toepassing<select name="toepassing" id="project-category"><option value="">Alle toepassingen</option>{opts(d['category'] for d in PROJECTS.values())}</select></label></div>
    <div class="project-filter-feedback"><p role="status" aria-live="polite" aria-atomic="true" data-project-count>{len(PROJECTS)} projecten gevonden</p><button type="reset" hidden>Wis filters</button></div></form>
    <div class="project-grid">{cards}</div><div class="project-empty" data-project-empty hidden><h3 class="h3">Geen project gevonden.</h3><p>Probeer een ander zoekwoord of wis de filters om alle projecten te bekijken.</p><button type="button" data-project-reset>Toon alle projecten {icon('right')}</button></div>
    </div></section>'''+contact('Uw proces.<br><em>Ons volgende project?</em>',
       'Vertel ons welk materiaal u verwerkt, wat u wilt verbeteren en welke ruimte beschikbaar is. Dan bespreken we de mogelijkheden voor uw installatie.',topic='installatieontwerp')
    items=[{'@type':'ListItem','position':i,'name':d['name'],'url':SITE+'/project-'+s+'.html'} for i,(s,d) in enumerate(PROJECTS.items(),1)]
    ld={'@context':'https://schema.org','@type':'CollectionPage','name':'Projecten van Airtechnic Solutions','url':SITE+'/projecten.html','mainEntity':{'@type':'ItemList','numberOfItems':len(items),'itemListElement':items}}
    body+='<script src="assets/js/projects.js" defer></script>'
    return page('projecten.html','Projecten | Airtechnic Solutions','Projecten in food, feed en recycling. Ontdek onze aanpak voor pneumatisch transport, verwerking en stofafzuiging.','og-project-pet.jpg',body,[ld,breadcrumb_jsonld(crumbs,SITE+'/projecten.html')],html_cls='knowledge-page projects-page',preload_img=('project-pet',HERO_SIZES),stylesheet='assets/css/projects.css',nav_current='Projecten')


def project_page(slug,d):
    filename='project-'+slug+'.html'
    crumbs=[('Home','index.html'),('Projecten','projecten.html'),(d['client'],filename)]
    hero=knowledge_intro(d['title'],crumbs,d['lead'],d['image'],'Technische projectillustratie: '+d['name'],
        (d['sector']+' / '+d['material'],'Illustratie · geen projectfoto'),
        (('Bekijk het project','#vraagstuk'),('Alle projecten','projecten.html')))
    hero=hero.replace(link('Alle projecten','projecten.html',arrow='down'),link('Alle projecten','projecten.html',arrow='left'))
    facts='<section class="project-facts" aria-label="Project in cijfers"><div class="container"><dl>'+''.join(f'<div><dt>{e(label)}</dt><dd>{e(value)}</dd></div>' for value,label in d['facts'])+'</dl></div></section>'
    nav='<nav class="solution-nav" aria-label="In dit project" data-scrollspy="145"><div class="container">'+''.join(f'<a href="#{id}">{label}</a>' for id,label in [('vraagstuk','De vraag'),('oplossing','De oplossing'),('uitvoering','Technische keuzes'),('projectbeelden','Projectbeelden'),('resultaat','Het resultaat')])+'</div></nav>'
    brief=''.join(f'<div><dt>{label}</dt><dd>{e(value)}</dd></div>' for label,value in [('Opdrachtgever',d['client']),('Materiaal',d['material']),('Onze rol',d['scope'])])
    intro=f'''<section class="solution-section"><div class="container solution-two"><div><p class="project-label">01 / Het vertrekpunt</p><h2 id="vraagstuk" class="h2" tabindex="-1">Een concrete vraag.<br><em>Een passend ontwerp.</em></h2><p>{e(d['challenge'])}</p></div><dl class="project-brief">{brief}</dl></div></section>'''
    stages=''.join(f'<li><span class="solution-step">{i:02d}</span><h3 class="h3">{e(title)}</h3><p>{e(text)}</p></li>' for i,(title,text) in enumerate(d['steps'],1))
    route=f'''<section class="solution-section solution-route"><div class="container"><div class="solution-heading"><div><p class="project-label">02 / De oplossing</p><h2 id="oplossing" class="h2" tabindex="-1">De onderdelen.<br><em>Het geheel.</em></h2></div><p>{e(d['solution'])}</p></div><ol class="solution-stages">{stages}</ol><p class="project-route-note">De belangrijkste functies in dit project, vereenvoudigd weergegeven.</p></div></section>'''
    decisions=''.join(f'<div><dt>{e(title)}</dt><dd>{e(text)}</dd></div>' for title,text in d['decisions'])
    engineering=f'''<section class="solution-section"><div class="container solution-two"><div><p class="project-label">03 / De uitwerking</p><h2 id="uitvoering" class="h2" tabindex="-1">De keuzes<br><em>achter de installatie.</em></h2><p>Een installatie werkt als de onderdelen op elkaar én op het proces zijn afgestemd. Deze punten waren bepalend in dit project.</p>{link(*d['solution_link'])}</div><dl class="solution-criteria">{decisions}</dl></div></section>'''
    pictures=''.join(f'''<figure class="project-document"><a href="images/project-originals/{e(file)}" data-project-photo data-caption="{e(caption)}" aria-label="Vergroot projectbeeld {i}: {e(caption)}"><img src="images/project-originals/{file.rsplit('.',1)[0]}-preview.webp" width="1200" height="900" loading="lazy" alt="{e(caption)}"><span>{icon('zoom')} Vergroot beeld</span></a><figcaption><span class="project-label">{'Projecttekening' if file == 'vacuum-1.png' else 'Projectfoto'} / {i:02d}</span>{e(caption)}</figcaption></figure>''' for i,(file,caption) in enumerate(d['photos'],1))
    gallery=f'''<section class="solution-section project-documentation"><div class="container"><div class="solution-heading"><div><p class="project-label">04 / Op locatie</p><h2 id="projectbeelden" class="h2" tabindex="-1">Van ontwerp<br><em>naar werkelijkheid.</em></h2></div><div><p>Bekijk de installatie en de technische uitwerking van dit project. Vergroot een beeld om de details te bekijken.</p></div></div><div class="project-documents">{pictures}</div></div></section>'''
    result=f'''<section class="solution-section project-result"><div class="container solution-two"><div><p class="project-label">05 / Het resultaat</p><h2 id="resultaat" class="h2" tabindex="-1">Samenhang<br><em>in de praktijk.</em></h2></div><div><p class="project-result__lead">{e(d['result'])}</p><p class="project-source">Capaciteiten en uitvoeringen gelden voor deze installatie.</p></div></div></section>'''
    related=f'''<section class="solution-section"><div class="container"><div class="project-library__head"><div><p class="project-label">Verder kijken</p><h2 class="h2">Meer uit<br><em>de praktijk.</em></h2></div>{link('Alle projecten','projecten.html')}</div><div class="project-grid">{''.join(project_card(s,PROJECTS[s]) for s in d['related'])}</div><div class="project-knowledge"><span>Verdiep u in de techniek</span>{link(*d['knowledge'])}</div></div></section>'''
    dialog='''<dialog class="project-lightbox" aria-labelledby="project-photo-title"><div class="project-lightbox__head"><h2 id="project-photo-title">Projectbeeld</h2><button type="button" data-photo-close aria-label="Sluit projectbeeld">'''+icon('close')+'''</button></div><img data-photo-image alt=""><p data-photo-caption></p><div class="project-lightbox__controls"><button type="button" data-photo-prev>Vorig beeld</button><span data-photo-position></span><button type="button" data-photo-next>Volgend beeld</button></div></dialog>'''
    body=hero+facts+nav+intro+route+engineering+gallery+result+related+contact('Een vergelijkbare vraag?<br><em>Laten we meedenken.</em>','Beschrijf uw materiaal, proces en gewenste verandering. We bespreken welke aanpak bij uw installatie past.',topic='installatieontwerp')+dialog+'<script src="assets/js/projects.js" defer></script>'
    ld={'@context':'https://schema.org','@type':'Article','headline':d['name'],'description':d['lead'],'url':SITE+'/'+filename,'image':SITE+'/images/og-'+d['image']+'.jpg','author':{'@type':'Organization','name':'Airtechnic Solutions'},'inLanguage':'nl-NL'}
    return page(filename,d['name']+' | Airtechnic Solutions',d['lead'],'og-'+d['image']+'.jpg',body,[ld,breadcrumb_jsonld(crumbs,SITE+'/'+filename)],html_cls='knowledge-page projects-page',preload_img=(d['image'],HERO_SIZES),stylesheet='assets/css/projects.css',nav_current='Projecten')
