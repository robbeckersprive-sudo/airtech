"""Three isolated, working hero concepts for desktop comparison."""
from components import page, pic, icon, btn, link
from pages import HERO_SLIDES

NAMES={'cinema':'Cinematisch','editorial':'Redactioneel','atelier':'Technisch atelier'}
def concept(kind, embedded=False):
    slides=[]
    for i,s in enumerate(HERO_SLIDES):
        spots=s.get('spots',[(71,53,'Transportleiding','Ontdek het leidingwerk','leidingdelen.html','r'),(89,28,'Transportbocht','Bekijk transportbochten','transportbocht.html','l')])
        anchors=''.join(f'<a class="hc-spot" style="--x:{x}%;--y:{y}%" href="{href}" aria-label="Bekijk {title}"><span class="hc-dot">+</span><span class="hc-tip">{title}{icon("ur")}</span></a>' for x,y,title,sub,href,side in spots)
        image=s['image'] if i else '01-hero-pijpleiding'
        target=s['link'][1] if i else 'oplossingen-pneumatisch-transport.html'
        slides.append(f'''<section class="hc-slide{' is-active' if i==0 else ''}" data-hc-slide aria-label="{s['tab']}" {'' if i==0 else 'inert aria-hidden="true"'}><div class="hc-visual">{pic(image,s['alt'],'(max-aspect-ratio: 6/5) 150vh, 100vw',eager=i==0)}<div class="hc-spots">{anchors}</div></div><div class="hc-copy"><p class="hc-kicker">AIRTECHNIC / {s['discipline']}</p><h1 class="h1">{s['title']}</h1><p class="hc-description">{s['sub']}</p><div class="hc-actions">{btn('Ontdek '+s['tab'].lower(),target)}{link('Bespreek uw proces','index.html#contact')}</div></div></section>''')
    choices=''.join(f'<a href="hero-concept-{k}.html" {"aria-current=page" if k==kind else ""}><small>{i:02d}</small> {v}</a>' for i,(k,v) in enumerate(NAMES.items(),1))
    tabs=''.join(f'<button type="button" data-hc-tab="{i}" aria-pressed="{str(i==0).lower()}"><span>0{i+1}</span>{s["tab"]}<i></i></button>' for i,s in enumerate(HERO_SLIDES))
    body=f'''<nav class="hc-compare" aria-label="Vergelijk de hero-varianten"><span>HERO STUDIES</span>{choices}</nav><div class="hc hc--{kind}" data-hc><div class="hc-stage">{''.join(slides)}</div><div class="hc-bottom"><div class="hc-index"><span data-hc-number>01</span> / 05</div><nav class="hc-tabs" aria-label="Kies een techniek">{tabs}</nav><button class="hc-play" type="button" data-hc-play aria-label="Automatisch afspelen" aria-pressed="false">{icon('play')}<span>Afspelen</span></button></div><p class="hc-hint">Klik op een + in het beeld en ontdek het component {icon('ur')}</p></div><section class="hc-after container"><p class="hc-kicker">VAN COMPONENT TOT COMPLETE INSTALLATIE</p><h2 class="h2">Uw proces vraagt om<br><em>samenhang.</em></h2>{link('Verken alle componenten','componenten.html')}{link('Terug naar de homepage','index.html')}</section><script src="assets/js/hero-concepts.js" defer></script>'''
    if embedded:
        hero = body[body.index('<div class="hc hc--'):body.index('<section class="hc-after')]
        hero = hero.replace('<h1 class="h1">', '<h2 class="h1">').replace('</h1>', '</h2>')
        hero = '<h1 class="sr-only">Industriële luchttechniek en solids processing</h1>' + hero
        from components import _v
        return hero + '<script src="' + _v('assets/js/hero-concepts.js') + '" defer></script>'
    return page('hero-concept-'
+kind+'.html',NAMES[kind]+' · Hero studie | Airtechnic','Interactieve hero studie','og-20-project-recycling.jpg',body,stylesheet='assets/css/hero-concepts.css',preview=True)

def build_concepts():
    from components import ROOT
    from pathlib import Path
    for kind in NAMES: (Path(ROOT)/('hero-concept-'+kind+'.html')).write_text(concept(kind),encoding='utf8')
if __name__=='__main__': build_concepts()
