"""Knowledge article: ATEX and dust explosion safety (group "Veiligheid en hygiëne").

Every regulatory statement, zone definition, St class and standard number below was checked on 2026-11-27 against
the primary or authoritative source listed in `sources` (EUR-Lex / Publications Office, wetten.overheid.nl via the
official BWB repository, Arboportaal, IFA GESTIS-STAUB-EX, NEN / BSI / IEC catalogues). Zone definitions follow
the Dutch text of Annex I of Directive 1999/92/EC. Nothing here claims that Airtechnic components are certified or
that Airtechnic draws up zone classifications or explosion protection documents.
"""
from components import tbd

TBD_AT = tbd('TBD: bevestigen door Airtechnic')

ZONE_FIGURE = '''<figure class="atex-zones" aria-labelledby="atex-zones-cap">
  <svg viewBox="0 0 640 300" role="img" aria-labelledby="atex-zones-title" focusable="false">
    <title id="atex-zones-title">Schematisch voorbeeld van stofzones rond een filter en een stortpunt</title>
    <defs><pattern id="atex-hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><path d="M0 0v8" class="atex-zones__hatch"/></pattern></defs>
    <rect x="24" y="252" width="592" height="2" class="atex-zones__floor"/>
    <!-- zone 22 around the tipping point -->
    <ellipse cx="150" cy="196" rx="132" ry="74" class="atex-zones__z22"/>
    <!-- zone 21 directly around the opening -->
    <ellipse cx="150" cy="176" rx="74" ry="42" class="atex-zones__z21"/>
    <!-- tipping station -->
    <path d="M96 150h108l-22 50h-64z" class="atex-zones__steel"/>
    <path d="M140 200h20v52h-20z" class="atex-zones__steel"/>
    <!-- duct to filter -->
    <path d="M150 150V96h250" class="atex-zones__duct"/>
    <!-- filter housing, inside = zone 20 -->
    <rect x="400" y="40" width="150" height="150" rx="4" class="atex-zones__steel"/>
    <rect x="410" y="50" width="130" height="130" class="atex-zones__z20"/>
    <path d="M400 190l40 46h70l40-46" class="atex-zones__steel"/>
    <path d="M440 236h70v16h-70z" class="atex-zones__steel"/>
    <!-- markers -->
    <g class="atex-zones__mark"><circle cx="475" cy="115" r="15"/><text x="475" y="120">1</text></g>
    <g class="atex-zones__mark"><circle cx="150" cy="128" r="15"/><text x="150" y="133">2</text></g>
    <g class="atex-zones__mark"><circle cx="40" cy="196" r="15"/><text x="40" y="201">3</text></g>
  </svg>
  <ol class="atex-zones__legend">
    <li><span class="atex-zones__key atex-zones__key--20" aria-hidden="true"></span><span><strong>1 · Zone 20</strong> Vaak de binnenkant van een filter of silo.</span></li>
    <li><span class="atex-zones__key atex-zones__key--21" aria-hidden="true"></span><span><strong>2 · Zone 21</strong> Vaak direct rond de opening van een stortpunt.</span></li>
    <li><span class="atex-zones__key atex-zones__key--22" aria-hidden="true"></span><span><strong>3 · Zone 22</strong> Vaak de ruimere omgeving waar stof alleen bij een storing vrijkomt.</span></li>
  </ol>
  <figcaption id="atex-zones-cap">Schematisch, niet op schaal. Een voorbeeld, geen zone-indeling: die volgt uit de beoordeling van uw eigen situatie.</figcaption>
</figure>'''

ARTICLES = {
 'atex-explosieveiligheid': dict(
  name='Stofexplosiegevaar: waar let u op bij ATEX?',
  seo_title='ATEX en stofexplosie bij afzuiging en transport',
  title='Stofexplosiegevaar:<br><em>waar let u op bij ATEX?</em>',
  description='ATEX en stofexplosiegevaar bij stofafzuiging, filtratie en pneumatisch transport. Zones 20, 21 en 22, stofgegevens, ontsteking voorkomen en gevolgen beperken.',
  intro='Een stofexplosie vraagt vijf dingen tegelijk: brandbaar stof, zuurstof, een ontstekingsbron, een stofwolk en een besloten ruimte. Filters, cyclonen, silo’s en transportleidingen brengen die vijf vaak samen. Daarom hoort explosieveiligheid in het ontwerp, en niet pas achteraf.',
  image='30-hero-filter', alt='Filterhuis met geplooide filterpatronen en een conische stofopvang',
  caption=('Veiligheid & hygiëne', 'Het filter: vaak de plek met de meeste stof in de lucht'),
  topic='atex-explosieveiligheid', og='og-knowledge-atex-explosieveiligheid.jpg',
  takeaway=[('Begin bij de stofgegevens', 'Kst-waarde, maximale explosiedruk, ontstekingsenergie en ontstekingstemperatuur bepalen welke maatregelen nodig zijn. Een veiligheidsinformatieblad noemt ze vaak niet.'),
            ('Zone-indeling bepaalt de uitvoering', 'De zones op uw locatie bepalen welke categorie apparatuur nodig is. U stelt die indeling als werkgever op, op basis van uw risicobeoordeling.')],
  principle_title='Vijf voorwaarden <em>voor een stofexplosie</em>',
  principle=['Een brand heeft brandstof, zuurstof en een ontstekingsbron nodig. Bij een stofexplosie komen daar twee voorwaarden bij: het stof hangt als wolk in de lucht, en de ruimte is besloten, zodat de druk zich opbouwt. Samen vormen ze de explosievijfhoek. Neem één zijde weg en er volgt geen explosie.',
             'Fijner stof is gevaarlijker. Kleine deeltjes hebben veel oppervlak, ontsteken makkelijker en verbranden sneller. Droog stof blijft bovendien langer zweven. Een product dat als korrel onschuldig lijkt, kan als fijne fractie in een filter wel explosief zijn. Kijk daarom naar het stof op de plek waar het ontstaat, niet alleen naar het product.',
             'Een eerste, kleine explosie kan neergeslagen stof opwervelen. Die nieuwe wolk kan een veel zwaardere tweede explosie geven. Goede housekeeping hoort daarom ook bij explosieveiligheid.',
             'Dit artikel helpt u de juiste vragen te stellen. Het vervangt geen risicobeoordeling: die maakt u voor uw eigen situatie, zo nodig met een deskundige.'],
  legend=('Voorkomen: geen wolk, geen ontsteking', 'Beperken: druk, vlam en voortplanting'),
  paths=[
   dict(id='richtlijnen', nav='Twee richtlijnen', title='Twee richtlijnen, <em>twee rollen</em>',
    before='ATEX bestaat uit twee Europese richtlijnen. Richtlijn 2014/34/EU, ook wel ATEX 114, gaat over apparaten en beveiligingssystemen voor plaatsen waar ontploffingsgevaar kan heersen. Die richtlijn richt zich op de fabrikant. Richtlijn 1999/92/EG, ook wel ATEX 153, gaat over de veiligheid en gezondheid van werknemers. Die richtlijn richt zich op de werkgever.',
    stages=[('Industriële luchttechniek', 'Apparatuur · ATEX 114'), ('Opslaan', 'Werkplek · ATEX 153'), ('Filtratie', 'Samen · de installatie')],
    caption='De ene richtlijn gaat over de apparatuur, de andere over de werkplek waar die staat.',
    after='In Nederland is ATEX 153 uitgewerkt in het Arbobesluit, in de paragraaf Explosieve atmosferen (artikel 3.5a tot en met 3.5f). De werkgever legt de risico’s vast in een explosieveiligheidsdocument (artikel 3.5c) en deelt de ruimten met explosiegevaar in zones in (artikel 3.5d). Voor de samenwerking betekent dit: u levert de zone-indeling en de risicobeoordeling aan, en wij stemmen de uitvoering van de installatie daarop af.'),
   dict(id='zones', nav='Zones voor stof', title='Zone 20, 21 en 22: <em>waar hangt de wolk?</em>',
    before='Richtlijn 1999/92/EG deelt plaatsen met brandbaar stof in drie zones in. Zone 20 is een plaats waar een explosieve atmosfeer, bestaande uit een wolk brandbaar stof in lucht, voortdurend, gedurende lange perioden of herhaaldelijk aanwezig is. Zone 21 is een plaats waar zo’n atmosfeer in normaal bedrijf af en toe aanwezig kan zijn. Zone 22 is een plaats waar die bij normaal bedrijf niet waarschijnlijk is, en als het toch gebeurt, van korte duur is.',
    stages=[('Filtratie', 'Zone 20 · categorie 1D'), ('Opslaan', 'Zone 21 · categorie 1D of 2D'), ('Stofafzuiging', 'Zone 22 · categorie 1D, 2D of 3D')],
    caption='Apparatuur per zone volgens bijlage II van Richtlijn 1999/92/EG, tenzij het explosieveiligheidsdocument anders bepaalt. De D staat voor stof.',
    figure=ZONE_FIGURE,
    after='De binnenkant van een filter of silo is vaak zone 20, de omgeving van een stortpunt vaak zone 21 of 22. Dat zijn voorbeelden, geen regel. De zone-indeling wordt per situatie bepaald, met NEN-EN-IEC 60079-10-2 als norm voor de indeling van gebieden met brandbaar stof.'),
   dict(id='stofgegevens', nav='Stofgegevens', title='Stofgegevens <em>sturen het ontwerp</em>',
    before='Welke maatregelen nodig zijn, hangt af van het stof. De belangrijkste kenmerken zijn de Kst-waarde (hoe snel de druk bij een explosie stijgt), de maximale explosiedruk Pmax, de minimale ontstekingsenergie (MIE), de minimale ontstekingstemperatuur van een stofwolk en van een stoflaag, en de onderste explosiegrens. Korrelgrootte en vochtgehalte beïnvloeden al deze waarden.',
    stages=[('Zeven en scheiden', 'Korrelgrootte en vocht'), ('Filtratie', 'Kst · Pmax · St-klasse'), ('Doseren', 'MIE · ontstekingstemperatuur')],
    caption='Op basis van de Kst-waarde valt stof in een St-klasse: St 1 tot 200, St 2 van 200 tot 300 en St 3 boven 300 bar·m/s.',
    after='Deze gegevens staan vaak niet in een veiligheidsinformatieblad. Laboratoriumonderzoek aan een representatief monster geeft de betrouwbaarste waarden. Een referentiedatabase zoals GESTIS-STAUB-EX van het IFA geeft een eerste indicatie. Het IFA wijst er zelf op dat stof dat gelijk lijkt, sterk verschillende waarden kan hebben. Gebruik zulke waarden daarom niet als ontwerpbasis.'),
   dict(id='ontsteking', nav='Ontsteking voorkomen', title='Ontsteking <em>voorkomen</em>',
    before='De eerste lijn is voorkomen: geen stofwolk waar het niet hoeft, en geen ontstekingsbron waar wel een wolk kan zijn. Houd de installatie stofdicht en ruim neergeslagen stof op. Aard alle geleidende delen van leidingwerk en componenten en verbind ze onderling (potentiaalvereffening), zodat statische lading kan afvloeien.',
    stages=[('pipe', 'Aarding en potentiaalvereffening'), ('Filtratie', 'Geleidend of antistatisch medium'), ('Zeven en scheiden', 'Magneet en zeef tegen vreemde delen')],
    caption='Voorkomen gaat vóór beperken: houd de stofwolk en de ontstekingsbron uit elkaar.',
    after='Statische lading vraagt ook aandacht in het filter, met een geleidend of antistatisch filtermedium, en bij big bags. Een big bag van type C is geleidend en moet tijdens vullen en lossen geaard zijn. Type D is van isolerend materiaal en beperkt de lading zonder aarding. Roterende delen, zoals sluizen en ventilatoren, kunnen mechanische vonken of hete oppervlakken geven. Vreemde delen in het product, zoals bouten of steentjes, vangt u vooraf af met magneten en zeven.'),
   dict(id='beperken', nav='Gevolgen beperken', title='Gevolgen <em>beperken</em>',
    before='Is ontsteking niet uit te sluiten, dan beperken constructieve maatregelen de gevolgen. Bij explosiedrukontlasting opent een explosieluik, zodat druk en vlam naar een veilige richting ontwijken (EN 14491). Staat het apparaat binnen, dan houdt vlamloze ontlasting de vlam en het hete stof binnen het apparaat (EN 16009). Explosieonderdrukking detecteert een explosie in een vroeg stadium en dooft haar voordat de druk hoog oploopt (EN 14373). Een explosiedrukvaste uitvoering is zo gebouwd dat zij de explosiedruk weerstaat (EN 14460).',
    stages=[('Filtratie', 'Ontlasten of onderdrukken'), ('valve', 'Ontkoppelen'), ('pipe', 'Vonkdetectie en blussing')],
    caption='Beperken: de explosie in het apparaat houden en voorkomen dat zij zich door de leidingen voortplant.',
    after='Een explosie mag zich niet via leidingen naar andere delen van de installatie voortplanten. Explosie-ontkoppeling (EN 15089) voorkomt dat, bijvoorbeeld met terugslagkleppen, snelafsluiters of een doseersluis. Een doseersluis telt alleen als ontkoppeling in een uitvoering die daarvoor is beproefd. Bij houtverwerking is vonkdetectie met blussing in het leidingwerk een gangbaar principe: een vonk wordt gedoofd voordat zij het filter bereikt.'),
   dict(id='per-component', nav='Per component', title='Wat dit betekent <em>per component</em>',
    before='Explosieveiligheid is een eigenschap van de hele installatie, niet van één component. Het filter is vaak de plek met de hoogste stofconcentratie en krijgt daarom meestal ontlasting, onderdrukking of een drukvaste uitvoering. Een cycloon scheidt het grove stof af, maar is zelf ook een besloten ruimte met een stofwolk. Een doseersluis onder filter of cycloon kan ontkoppelen, mits beproefd. Een ventilator aan de schone zijde van het filter krijgt veel minder stof te verwerken dan een ventilator aan de stofzijde.',
    stages=[('Filtratie', 'Filter en cycloon'), ('Doseren', 'Doseersluis'), ('Pneumatisch transport', 'Leidingwerk en transport')],
    caption='Elke component draagt bij; de combinatie bepaalt het veiligheidsniveau.',
    after='Leidingwerk moet geaard en doorverbonden zijn, en is de route waarlangs een explosie zich kan voortplanten. Een silo met ontluchtingsfilter is tijdens pneumatisch vullen een klassieke plek voor een stofwolk. Bij een big-bagstation spelen het storten, statische lading en het type big bag. Bij pneumatisch transport verschilt de situatie per systeem: bij vacuümtransport blijft stof bij een lek binnen de leiding, bij druktransport komt het naar buiten. Transport met stikstof of een ander inert gas houdt het zuurstofgehalte zo laag dat een explosie niet kan ontstaan; dat is een principe dat per toepassing wordt ontworpen.',
    note='Transport met inert gas door Airtechnic: ' + TBD_AT,
    links=[('Patroonfilter', 'patroonfilter.html'), ('Zakkenfilter', 'zakkenfilter.html'), ('Cycloonafscheider', 'cycloonafscheider.html'),
           ('Doorvalsluis', 'doorvalsluis.html'), ('Doorblaassluis', 'doorblaassluis.html'), ('Centrifugaalventilator', 'centrifugaalventilator.html'),
           ('Ontluchtingsfilter', 'ontluchtingsfilter.html'), ('Big-baglosstation', 'bigbag-losstation.html'),
           ('Druk- of vacuümtransport?', 'kennis-druk-of-vacuumtransport.html')]),
  ],
  practice=[('PET-recycling', 'project-pet-recycling.html', 'Een ATEX-conforme filterinstallatie van 18.000 m³/u maakt deel uit van de stofafzuiging.'),
            ('Dierenvoeding', 'project-dierenvoeding.html', 'De ontvangststations zijn uitgerust met persluchtgereinigde ATEX-filters en een veiligheids-HEPA-filter.')],
  comparison_title='Maatregelen <em>naast elkaar</em>',
  comparison_intro='Een overzicht van de gangbare maatregelen. Welke combinatie past, volgt uit de stofgegevens, de zone-indeling, de opstelling en uw risicobeoordeling.',
  headings=['Maatregel', 'Wat het doet', 'Waar toegepast', 'Norm'],
  rows=[('Explosiedrukontlasting', 'Een luik opent en laat druk en vlam naar een veilige richting ontwijken.', 'Filters, cyclonen en silo’s met een veilige uitblaasrichting, meestal buiten.', 'EN 14491'),
        ('Vlamloze ontlasting', 'Ontlast de druk en houdt vlam en heet stof in het apparaat.', 'Apparaten binnen, zonder veilige uitblaasrichting.', 'EN 16009'),
        ('Explosieonderdrukking', 'Detecteert de explosie vroeg en dooft haar met een blusmiddel.', 'Apparaten waar ontlasten niet kan of niet gewenst is.', 'EN 14373'),
        ('Explosiedrukvaste uitvoering', 'Het apparaat weerstaat de explosiedruk.', 'Apparaten waar ontlasten niet kan, vaak samen met ontkoppeling.', 'EN 14460'),
        ('Explosie-ontkoppeling', 'Voorkomt dat de explosie zich via leidingen voortplant.', 'Leidingen tussen filter, cycloon, silo en proces.', 'EN 15089'),
        ('Aarding en antistatisch', 'Laat statische lading afvloeien en voorkomt ontladingen.', 'Leidingwerk, filters, big bags en alle geleidende delen.', 'EN 1127-1 (basis)'),
        ('Vonkdetectie en blussing', 'Detecteert vonken in de leiding en dooft ze vóór het filter.', 'Houtverwerking en andere processen met vonken.', 'Per toepassing')],
  scenarios=[('Een houtstoffilter binnen wordt uitgebreid', 'Kijk opnieuw waar de druk heen kan.', 'Een luik dat in de hal uitblaast is geen optie. Vlamloze ontlasting, onderdrukking of het filter naar buiten verplaatsen zijn alternatieven. Meer afzuigpunten betekenen bovendien een nieuwe luchtbalans.'),
             ('Een meel- of suikersilo wordt pneumatisch gevuld', 'Neem de vulcyclus mee.', 'Tijdens het vullen hangt er een stofwolk in de silo. Ontluchtingsfilter, aarding, vulsnelheid en ontlasting van de silo horen samen te worden beoordeeld.'),
             ('Een bestaande installatie krijgt extra afzuigpunten', 'Werk het explosieveiligheidsdocument bij.', 'Nieuwe afzuigpunten veranderen de luchtstroom, de stofbelasting van het filter en soms de zones. Bekijk het explosieveiligheidsdocument en de zone-indeling daarom opnieuw voordat de uitbreiding in bedrijf gaat.')],
  checklist=[('Product', 'Productnaam en veiligheidsinformatieblad.'),
             ('Stofgegevens', 'Kst, Pmax, St-klasse, MIE en minimale ontstekingstemperatuur, voor zover bekend.'),
             ('Zone-indeling', 'De zone-indeling of het explosieveiligheidsdocument.'),
             ('Opstelling', 'Binnen of buiten, afstand tot werkplekken en vrije ruimte voor ontlasting.'),
             ('Bestaande maatregelen', 'Luiken, ontkoppeling, aarding of vonkdetectie die er al zijn.'),
             ('Tekening of foto’s', 'Van de installatie en de omgeving.')],
  action='Bespreek uw situatie', contact_title='Explosieveiligheid<br><em>in uw installatie?</em>',
  contact_intro='Vertel welk product u verwerkt en of er al een zone-indeling of explosieveiligheidsdocument is. We stemmen de uitvoering af op de zone-indeling en de stofgegevens die u aanlevert.',
  related=[('Filters & ontstoffing', 'Vergelijk de filters', 'componenten-filters.html', '17-filter-macro', False, 'Filteruitvoeringen voor afzuiging, productopvang en ontluchting.'),
           ('Doseersluizen', 'Vergelijk de sluizen', 'componenten-doseersluizen.html', '06-doseersluis-vrijstaand', True, 'Sluizen onder filter of cycloon en voor invoer in transport.')],
  sources=[('EUR-Lex · Richtlijn 2014/34/EU (ATEX 114), apparaten en beveiligingssystemen', 'https://eur-lex.europa.eu/legal-content/NL/TXT/?uri=CELEX:32014L0034'),
           ('EUR-Lex · Richtlijn 1999/92/EG (ATEX 153), explosieve atmosferen op de werkplek', 'https://eur-lex.europa.eu/legal-content/NL/TXT/?uri=CELEX:31999L0092'),
           ('Europese Commissie · ATEX-richtsnoeren, 6e editie (januari 2026)', 'https://single-market-economy.ec.europa.eu/sectors/mechanical-engineering/equipment-potentially-explosive-atmospheres-atex_en'),
           ('Arbobesluit · paragraaf Explosieve atmosferen, artikel 3.5a–3.5f', 'https://wetten.overheid.nl/BWBR0008498/'),
           ('Arboportaal · Arbobesluit artikel 3.5c, explosieveiligheidsdocument', 'https://www.arboportaal.nl/externe-bronnen/wetgeving/arbobesluit-artikel-3.5c'),
           ('IFA · GESTIS-STAUB-EX, database met explosiekenmerken', 'https://www.dguv.de/ifa/gestis/gestis-staub-ex/index-2.jsp'),
           ('IFA · St-klassen bij de Kst-waarde', 'https://staubex.ifa.dguv.de/HTML-Dokumente/ERLT61E.HTM'),
           ('IFA · Grenzen van de databasewaarden', 'https://staubex.ifa.dguv.de/HTML-Dokumente/ERLT12E.HTM'),
           ('IEC · 60079-10-2, classification of areas, explosive dust atmospheres', 'https://webstore.iec.ch/en/publication/90124'),
           ('BSI · EN 14491, dust explosion venting protective systems', 'https://knowledge.bsigroup.com/products/dust-explosion-venting-protective-systems'),
           ('BSI · EN 16009, flameless explosion venting devices', 'https://knowledge.bsigroup.com/products/flameless-explosion-venting-devices'),
           ('BSI · EN 15089, explosion isolation systems', 'https://knowledge.bsigroup.com/products/explosion-isolation-systems'),
           ('DIN · EN 61340-4-4, big bags (FIBC) type A, B, C en D', 'https://din.de/en/getting-involved/standards-committees/dke/publications/wdc-beuth:din21:239470920'),
           ('NEN · EN 14373, explosion suppression systems', 'https://www.nen.nl/en/nen-en-14373-2021-en-289244'),
           ('NEN · EN 14460, explosion resistant equipment', 'https://www.nen.nl/en/nen-en-14460-2018-en-243501'),
           ('NEN · EN 1127-1, explosion prevention and protection, basic concepts', 'https://www.nen.nl/en/nen-en-1127-1-2019-en-262504')]),
}
