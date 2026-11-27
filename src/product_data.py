"""Complete detail-page records composed from catalogue and product knowledge."""
from dataclasses import asdict
from category_data import CATEGORIES
from cyclone_category_data import CYCLONES
from cyclone_product_data import CYCLONE
from product_routes import PRODUCT_ROUTES
from product_knowledge import PROFILES, MECHANICS, FAMILY_SELECTION, MAINTENANCE

REUSED_CUTAWAYS = {
 'cycloonafscheider':'13-cycloon-doorsnede', 'centrifugaalventilator':'14-blower-doorsnede',
 'filterelement':'05-filter-doorsnede', 'doorvalsluis':'15-doseersluis-doorsnede',
 'leidingdelen':'07-leidingwerk-doorsnede', 'bigbag-losstation':'08-bigbag-doorsnede',
 'afsluiter-op-maat':'09-afsluiter-doorsnede', 'trilzeef':'10-zeef-doorsnede',
}
POSITIONS = {
 'cycloon': [(15,20),(78,40),(54,83),(60,8)], 'multi': [(15,15),(35,44),(60,86),(66,10)],
 'ontvanger': [(16,41),(52,65),(59,24),(52,88)],
 'centrifugaal': [(22,44),(45,46),(69,30),(54,8)], 'lobben':[(32,16),(32,42),(13,67),(79,40)],
 'zijkanaal':[(22,75),(43,45),(23,22),(43,79)],
 'patronen':[(83,22),(45,39),(51,14),(52,81)], 'zakken':[(17,24),(50,42),(52,15),(50,80)],
 'ontluchting':[(47,90),(43,57),(50,16),(76,30)], 'element':[(18,40),(47,48),(64,64),(53,10)],
 'doorval':[(34,13),(35,46),(36,77),(75,39)], 'doorblaas':[(34,12),(35,43),(48,79),(76,36)],
 'uittrek':[(48,14),(42,48),(73,55),(85,76)],
 'leiding':[(52,12),(26,56),(48,85),(79,48)], 'bocht':[(48,87),(49,46),(24,49),(75,24)],
 'koppeling':[(10,51),(32,53),(53,18),(86,50)], 'wissel':[(48,12),(50,45),(28,80),(83,38)],
 'lossen':[(51,12),(50,49),(51,64),(51,82)], 'vullen':[(51,31),(48,8),(52,47),(52,85)],
 'bagdoseer':[(33,21),(34,64),(65,67),(87,50)],
 'schuif':[(17,31),(43,48),(17,82),(80,25)], 'vlinder':[(30,70),(54,63),(59,81),(52,25)],
 'manchet':[(17,57),(51,17),(49,51),(82,42)],
 'trillen':[(50,14),(28,79),(48,45),(82,47)], 'trommel':[(21,15),(53,39),(51,69),(87,76)],
 'meerdeks':[(50,10),(54,32),(53,52),(85,62)],
}
DETAIL_FOCUS = {
 'cyclonen': [('Inlaat', '28% 20%'),('Productafvoer','55% 83%')],
 'blowers-ventilatoren': [('Luchtaansluiting','25% 40%'),('Aandrijving','80% 45%')],
 'filters': [('Filtersectie','50% 30%'),('Aansluiting','50% 80%')],
 'doseersluizen': [('Productinlaat','35% 20%'),('Rotor en huis','35% 58%')],
 'leidingwerk-koppelingen': [('Verbinding','30% 40%'),('Constructie','70% 60%')],
 'bigbag-stations': [('Zakaansluiting','50% 35%'),('Productoverdracht','50% 76%')],
 'afsluiters': [('Doorlaat','30% 58%'),('Bediening','75% 25%')],
 'zeven': [('Toevoer','45% 20%'),('Afvoer','78% 55%')],
}
PRODUCT_FOCUS = {
 'multicycloon': [('Toevoer','20% 15%'),('Opvang','55% 82%')],
 'transportafscheider': [('Filtersectie','50% 24%'),('Productafvoer','50% 83%')],
 'centrifugaalventilator': [('Luchtinlaat','60% 45%'),('Aandrijving','18% 45%')],
 'zijkanaalblower': [('Luchtaansluitingen','28% 76%'),('Aandrijving','80% 42%')],
 'ontluchtingsfilter': [('Reiniging','50% 16%'),('Montageflens','50% 88%')],
 'filterelement': [('Medium','50% 46%'),('Aansluiting','50% 12%')],
 'doseersluis-uitneembare-rotor': [('Productinlaat','50% 15%'),('Uittrekconstructie','78% 62%')],
 'bigbag-vulstation': [('Vulkop','50% 22%'),('Platform','50% 88%')],
 'vlinderklep': [('Klepschijf','50% 72%'),('Aandrijving','50% 18%')],
 'manchetafsluiter': [('Doorlaat','17% 55%'),('Luchtaansluiting','52% 15%')],
 'trommelzeef': [('Invoer','23% 18%'),('Zeefmantel','60% 45%')],
}

PRODUCTS = {}
for category, family in {'cyclonen': CYCLONES, **CATEGORIES}.items():
    for source in family['items']:
        item = asdict(source) if not isinstance(source, dict) else source
        slug = PRODUCT_ROUTES[category][item['variant']]
        name = 'Cycloonafscheider' if slug == 'cycloonafscheider' else item['name']
        cutaway = REUSED_CUTAWAYS.get(slug, 'detail-' + slug + '-doorsnede')
        d = dict(slug=slug, name=name, category=category, family_name=family['name'], nav=family['nav'],
                 image=item['image'], cutaway=cutaway, context_image=family['hero'],
                 context_caption='Voorbeeldopstelling binnen deze productfamilie',
                 topic=slug, documentation_topic=slug+'-documentatie', variant=item['variant'])
        if slug == 'cycloonafscheider':
            d.update(CYCLONE)
            d.update(step_heading='Volg de lucht en de deeltjes',
                note='De gewenste luchtkwaliteit en de resterende fijne stoffractie bepalen of nafiltratie nodig is.',
                context_title='De cycloon <em>in uw installatie</em>',
                context_intro='De positie van de cycloon hangt af van wat u wilt terugwinnen en welke eisen u aan de uitgaande lucht stelt.',
                context_caption='Voorbeeldopstelling met leidingwerk en productafvoer',
                sectors='Food · Feed · Recycling · Chemie · Hout',
                documentation_topic='cycloon-documentatie', related_title='Rondom <em>de cycloon</em>',
                contact_title='Past deze cycloon bij uw proces?',
                contact_intro='Vertel ons uw proces en uw wensen. We denken graag met u mee over de juiste uitvoering.')
        else:
            mechanism, principle, lead, question, answer = PROFILES[slug]
            focus = PRODUCT_FOCUS.get(slug, DETAIL_FOCUS[category])
            views = [('Overzicht',item['image'],name+' · illustratieve uitvoering')]
            for label, origin in focus:
                views.append((label,item['image'],f'{name} · detailuitsnede {label.lower()}',
                    f'transform:scale(1.8);transform-origin:{origin};'))
            views.append(('Doorsnede',cutaway,name+' · schematische doorsnede van het werkingsprincipe'))
            selection = [('Uitvoeringskeuze',answer), *FAMILY_SELECTION[category]]
            d.update(lead=lead, views=views,
                facts=[('Principe',principle),('Functie',item['feature'].rstrip('.')),('Uitvoering','Afgestemd op uw proces')],
                principle_title='Zo werkt <em>deze uitvoering</em>', principle_intro=lead,
                steps=[(*s,*position) for s,position in zip(MECHANICS[mechanism],POSITIONS[mechanism])],
                step_heading='Volg het werkingsprincipe',
                note='De doorsnede toont het principe. De definitieve constructie en procesinstellingen volgen uit de technische selectie.',
                spec_rows=selection,
                selection_intro=family['request']+' De gekozen uitvoering en leveringsomvang leggen we vast in het technische voorstel.',
                context_title='Een passende plek <em>in uw installatie</em>',
                context_intro='De toepassing: '+item['use'][0].lower()+item['use'][1:]+' De toevoer, afvoer en beschikbare ruimte worden samen met de omliggende processtappen beoordeeld.',
                applications=[('Passende processtap',item['use']),('Aansluiten op het proces',family['criteria'][2][1]),('Bereikbaar voor inspectie',MAINTENANCE[category]+' Neem de benodigde toegang mee in de opstelling.')],
                sectors='Toepasbaarheid wordt beoordeeld op materiaal, procescondities en producteisen.',
                faq_items=[('Wat kenmerkt deze uitvoering?',item['feature']+' '+lead), (question,answer),
                  ('Waar past deze uitvoering in het proces?',item['use']+' '+family['criteria'][0][1]),
                  ('Welke aandachtspunten zijn er voor onderhoud?',MAINTENANCE[category]+' Leg de inspectiefrequentie vast op basis van bedrijfsuren, productbelasting en de instructies van de geleverde uitvoering.'),
                  ('Kan deze uitvoering in een bestaande installatie worden opgenomen?',family['criteria'][2][1]+' Een foto of tekening helpt om de aansluitingen en beschikbare ruimte te beoordelen.'),
                  ('Welke informatie is nodig voor een gericht voorstel?',family['request']+' Vermeld of u een losse component of ook montage en aansluiting zoekt. Geef bijzondere product- of reinigingseisen vooraf door.')],
                related_title='Vergelijk <em>verwante uitvoeringen</em>',
                contact_title='Past deze uitvoering bij uw proces?', contact_intro=family['request'])
        PRODUCTS[slug] = d

for slug, d in PRODUCTS.items():
    others = (['filterelement','centrifugaalventilator','doorvalsluis'] if slug=='cycloonafscheider'
              else [v for v in PRODUCT_ROUTES[d['category']].values() if v != slug])
    d['related'] = [(PRODUCTS[k]['name'],PRODUCTS[k]['image'],PRODUCTS[k]['lead'],k+'.html') for k in others]
