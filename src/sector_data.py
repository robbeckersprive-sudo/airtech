"""Sector pages (sectoren.html + sectoren-<slug>.html): editorial data. Layout is owned by sector_page.py.

One record per sector; everything else is derived from it, so there is one place to maintain:
- `components` -> the sector chips on product pages (product_page.py via SECTORS_OF_PRODUCT)
- `solutions` + `route` -> "Toegepast in" on solution pages (solution_page.py via SECTORS_OF_SOLUTION)
- `topic_title` / `topic_help` -> contact topic 'sector-<slug>' (contact_delivery.py)
- `project_sector` -> real projects from project_data.PROJECTS whose `sector` equals it (none: no project block)

Honesty rules (README "Sectoren"): no invented clients, figures, certifications or experience. Statements about
Airtechnic that the repository cannot support carry tbd('TBD: bevestigen door Airtechnic'). General regulatory
facts are listed under `sources` (checked 2026-11-27).
"""

ATEX = 'kennis-atex-explosieveiligheid.html'
# same markup as components.tbd(); not imported because contact_delivery (imported by components) reads this module
TBD_AT = '<span class="tbd">[TBD: bevestigen door Airtechnic]</span>'

SECTOR_FILE = 'sectoren-{}.html'
INDEX_FILE = 'sectoren.html'

# Shared regulatory sources (each opened and checked; see README "Sectoren")
SRC_1935 = ('EUR-Lex · Verordening (EG) nr. 1935/2004, materialen in contact met levensmiddelen',
            'https://eur-lex.europa.eu/legal-content/NL/TXT/?uri=CELEX:32004R1935')
SRC_ATEX153 = ('EUR-Lex · Richtlijn 1999/92/EG, explosieve atmosferen op de werkplek',
               'https://eur-lex.europa.eu/legal-content/NL/TXT/?uri=CELEX:31999L0092')
SRC_ARBO_EX = ('Arboportaal · Arbobesluit artikel 3.5c, explosieveiligheidsdocument',
               'https://www.arboportaal.nl/externe-bronnen/wetgeving/arbobesluit-artikel-3.5c')
SRC_GESTIS = ('IFA · GESTIS-STAUB-EX, explosiekenmerken van stof', 'https://www.dguv.de/ifa/gestis/gestis-staub-ex/index-2.jsp')
SRC_GMP = ('GMP+ International · schema voor veilig diervoeder (Feed Safety Assurance)', 'https://www.gmpplus.org/')
SRC_EHEDG = ('EHEDG · European Hygienic Engineering & Design Group', 'https://www.ehedg.org/')
SRC_HOUT = ('Arbeidsomstandighedenregeling · bijlage XIII, wettelijke grenswaarden (hardhoutstof)',
            'https://wetten.overheid.nl/BWBR0008587/')
SRC_2004_37 = ('EUR-Lex · Richtlijn 2004/37/EG, carcinogene, mutagene of reprotoxische stoffen op het werk',
               'https://eur-lex.europa.eu/legal-content/NL/TXT/?uri=CELEX:02004L0037-20240408')

SECTORS = {
 'food': dict(
  name='Food', long='Voedingsmiddelen', nav='Food',
  title='Voedingsmiddelen.<br><em>Hygiënisch verwerken.</em>',
  lead='Ingrediënten, extrudaten en poeders vragen om een installatie die reinigbaar is en het product heel laat. Hygiëne, productwissels en stofexplosiegevaar bepalen samen het ontwerp.',
  image='21-project-food', alt='Illustratie van een voedingsmiddelenfabriek met silo’s, stoffilter en transportleidingen in RVS',
  caption=('Food · voedingsmiddelen', 'Illustratieve procesopstelling'),
  seo_title='Transport en stofafzuiging voor food',
  description='Pneumatisch transport, doseren en stofafzuiging voor de voedingsmiddelenindustrie. Hygiënisch ontwerp, productwissels, breuk van extrudaten en stofexplosiegevaar.',
  topic_title='Proces in de voedingsmiddelenindustrie',
  topic_help='Welk product verwerkt u, hoe vaak wisselt u van product en hoe reinigt u: droog of nat? Noem ook de capaciteit als u die weet.',
  issues=[
   ('Reinigen en demonteren', 'Bij productwissels moet de installatie snel en controleerbaar schoon zijn, droog of nat.',
    'Dode hoeken vermijden, delen bereikbaar maken en demontage zonder gereedschap waar dat kan.'),
   ('Materialen in contact met het product', 'Materialen die levensmiddelen raken, vallen onder Verordening (EG) 1935/2004.',
    'De materiaalkeuze en afdichtingen leggen we per toepassing vast, met de documentatie die u nodig heeft.'),
   ('Allergenen en kruisbesmetting', 'Restanten van een vorige batch mogen niet in de volgende terechtkomen.',
    'Productroutes, wissels en restlegen ontwerpen we op uw reinigingsprocedure.'),
   ('Breuk en stofexplosiegevaar', 'Extrudaten breken bij hoge snelheid; fijn meel, suiker en zetmeel kunnen een stofexplosie veroorzaken.',
    'Het transportregime kiest u op productbehoud; stofgegevens en zone-indeling sturen de uitvoering.'),
  ],
  route=[
   ('Ontvangen', 'opslaan', 'Grondstoffen uit zak, big bag of silo, met een stofarme overdracht.'),
   ('Doseren', 'doseren', 'Een sluis voert gelijkmatig toe; een uitneembare rotor maakt reinigen eenvoudiger.'),
   ('Transporteren', 'pneumatisch-transport', 'Druk- of vacuümtransport, met het regime afgestemd op breukgevoeligheid.'),
   ('Controleren', 'zeven-en-scheiden', 'Een controlezeef houdt vreemde delen en klonten tegen vóór de volgende stap.'),
   ('Afzuigen', 'stofafzuiging', 'Stof bij stort- en overslagpunten gericht afvangen.'),
  ],
  solutions=[
   ('pneumatisch-transport', 'Gesloten transport beperkt stof en contact met de omgeving; het regime bepaalt hoeveel het product beschadigt.'),
   ('doseren', 'Een constante toevoer houdt transport en verwerking stabiel, ook bij wisselende ingrediënten.'),
   ('zeven-en-scheiden', 'Een controlezeef vangt vreemde delen af voordat het product de volgende stap of verpakking bereikt.'),
   ('hoogvacuum', 'Centraal reinigen met vaste aansluitpunten houdt de vloer en machines schoon zonder stof op te werpen.'),
  ],
  components=[
   ('doseersluis-uitneembare-rotor', 'De rotor schuift uit het huis, zodat u bij productwissels snel kunt inspecteren en reinigen.'),
   ('transportafscheider', 'Scheidt het product na vacuümtransport uit de lucht en geeft het rustig af aan de volgende stap.'),
   ('controlezeef', 'Een laatste controle op vreemde delen en klonten vóór menger, verpakking of silo.'),
   ('ontluchtingsfilter', 'Houdt stof binnen wanneer een silo pneumatisch wordt gevuld.'),
   ('bigbag-losstation', 'Ingrediënten uit big bags gecontroleerd en stofarm overdragen.'),
  ],
  requirements=[
   ('Hygiëne', 'Reinigbaarheid, demontage, oppervlakken en het vermijden van dode hoeken.'),
   ('Productcontact', 'Materialen en afdichtingen volgens Verordening (EG) 1935/2004.'),
   ('Productwissels', 'Restlegen, allergenenscheiding en de duur van een omstelling.'),
   ('Productbehoud', 'Breuk, ontmenging en slijtage van het product tijdens transport.'),
   ('Explosieveiligheid', 'Stofgegevens van het product en de zone-indeling van uw locatie.'),
  ],
  project_sector='Food',
  knowledge=['druk-of-vacuumtransport', 'controlezeef-of-fractioneerzeef', 'atex-explosieveiligheid'],
  faq=[
   ('Hoe voorkomt u breuk van extrudaten tijdens transport?',
    'Breuk ontstaat vooral door hoge snelheid en harde inslagen in bochten en bij de ontvangst. Transport in dichte fase met een lagere snelheid is vaak productvriendelijker dan verdunde fase. De keuze volgt uit het product, de afstand en de capaciteit.'),
   ('Hoe gaat u om met productwissels en allergenen?',
    'We beginnen bij uw reinigingsprocedure: droog of nat, hoe vaak, en wat zichtbaar en bereikbaar moet zijn. Daarop stemmen we demontage, routes en restlegen af. De validatie van de reiniging blijft onderdeel van uw eigen voedselveiligheidssysteem.'),
   ('Aan welke eisen moeten materialen met productcontact voldoen?',
    'Materialen die in contact komen met levensmiddelen vallen onder Verordening (EG) 1935/2004 en de specifieke regels per materiaalsoort. Vraag bij een voorstel naar de materiaalspecificatie en de documenten die u voor uw kwaliteitssysteem nodig heeft.'),
   ('Is meel- of suikerstof explosief?',
    'Veel organische poeders, zoals meel, suiker en zetmeel, kunnen in een stofwolk tot ontploffing komen. Hoe gevoelig een product is, hangt af van onder meer korrelgrootte en vocht. Stofgegevens en uw zone-indeling bepalen de uitvoering van filters, sluizen en leidingwerk.'),
   ('Kan een bestaande lijn worden uitgebreid?',
    'Vaak wel. We beoordelen de capaciteit van de bestaande blower, het leidingtracé en de ontvangst. Deel een tekening of foto’s en beschrijf wat er verandert in product of capaciteit.'),
  ],
  sources=[SRC_1935, SRC_EHEDG, SRC_GESTIS, SRC_ATEX153],
 ),
 'feed': dict(
  name='Feed', long='Diervoeding en petfood', nav='Feed',
  title='Diervoeding.<br><em>Elke grondstof op zijn plek.</em>',
  lead='Veel grondstoffen, veel bestemmingen en producten die vet of vochtig kunnen zijn. Een goede route houdt grondstoffen gescheiden en voorkomt verstopping en stof.',
  image='project-feed', alt='Illustratie van een zakkenstortkabinet dat via wissels vier ontvangststations voedt',
  caption=('Feed · diervoeding en petfood', 'Illustratie · geen projectfoto'),
  seo_title='Pneumatisch transport voor diervoeding',
  description='Pneumatisch transport, opslag en stofafzuiging voor diervoeding en petfood. Routering naar meerdere bestemmingen, kleverige producten, kruisbesmetting en stofexplosiegevaar.',
  topic_title='Proces in diervoeding of petfood',
  topic_help='Hoeveel grondstoffen en bestemmingen heeft u, en welke producten zijn vet, vochtig of kleverig? Noem ook de capaciteit als u die weet.',
  issues=[
   ('Veel grondstoffen, veel bestemmingen', 'Eén ontvangstpunt moet vaak meerdere silo’s of mengers bedienen.',
    'Wissels, routelogica en ontvangststations ontwerpen we als één systeem, met duidelijke routes.'),
   ('Vet, vochtig en kleverig', 'Zulke producten stromen slecht uit silo en big bag en hechten aan wanden.',
    'Uitloopgeometrie, uitloophulp en de keuze van de sluis volgen uit het werkelijke stroomgedrag.'),
   ('Kruisbesmetting', 'Restanten van medicinale of specifieke grondstoffen mogen niet in de volgende partij komen.',
    'Restlegen, reinigbaarheid en de volgorde van routes nemen we mee in het ontwerp.'),
   ('Stof en explosieveiligheid', 'Bij storten en ontvangen komt fijn, vaak brandbaar stof vrij.',
    'Afzuiging bij de bron en filters afgestemd op de stofgegevens en uw zone-indeling.'),
  ],
  route=[
   ('Ontvangen', 'opslaan', 'Grondstoffen uit zakken, big bags of bulkwagen in een stortstation.'),
   ('Doseren', 'doseren', 'Een sluis voert het product gelijkmatig in de transportleiding.'),
   ('Transporteren', 'pneumatisch-transport', 'Druk- of vacuümtransport naar de gekozen bestemming.'),
   ('Verdelen', 'pneumatisch-transport', 'Wissels leiden de stroom naar silo, weger of menger.'),
   ('Afzuigen', 'stofafzuiging', 'Stof bij stortpunten en ontvangers gericht afvangen.'),
  ],
  solutions=[
   ('pneumatisch-transport', 'Eén leidingnet met wissels brengt grondstoffen naar meerdere bestemmingen.'),
   ('opslaan', 'Silo’s en big bags moeten ook kleverige producten betrouwbaar laten uitstromen.'),
   ('doseren', 'Een constante toevoer voorkomt overladen leidingen en verstopping.'),
   ('stofafzuiging', 'Afzuiging bij stortpunten beperkt stof in de hal en rond de ontvangers.'),
  ],
  components=[
   ('leidingwissel', 'Leidt de productstroom naar de gekozen silo, weger of menger.'),
   ('doorblaassluis', 'Voert het product vanuit een stortstation of silo in de transportleiding.'),
   ('bigbag-losstation', 'Laat ook slecht stromende grondstoffen gecontroleerd uit de big bag lopen.'),
   ('patroonfilter', 'Vangt stof af bij stortpunten en ontvangers.'),
   ('ontluchtingsfilter', 'Houdt stof binnen tijdens het pneumatisch vullen van een silo.'),
  ],
  requirements=[
   ('Routering', 'Aantal grondstoffen, bestemmingen en de volgorde waarin routes worden gebruikt.'),
   ('Stroomgedrag', 'Vet- en vochtgehalte, kleefgedrag en neiging tot brugvorming.'),
   ('Kruisbesmetting', 'Restlegen, reinigbaarheid en scheiding van kritische grondstoffen.'),
   ('Explosieveiligheid', 'Stofgegevens en de zone-indeling rond stortpunten, filters en silo’s.'),
  ],
  project_sector='Feed',
  knowledge=['druk-of-vacuumtransport', 'bigbag-lossen-onregelmatige-productstroom', 'atex-explosieveiligheid'],
  faq=[
   ('Hoeveel bestemmingen kan één transportlijn bedienen?',
    'Dat hangt af van de capaciteit per route en hoe vaak er wordt gewisseld. Met wissels kan één ontvangstpunt meerdere silo’s of ontvangers bedienen. In het dierenvoedingsproject verdelen drie wisselkleppen het product over vier ontvangststations.'),
   ('Waarom stroomt een vetrijk product slecht uit silo of big bag?',
    'Vet en vocht maken een product samenhangend: het vormt bruggen of blijft aan de wand hangen. De uitloopgeometrie, uitloophulpmiddelen en de afvoersluis stemmen we af op het werkelijke stroomgedrag van uw product.'),
   ('Hoe beperkt u het risico op kruisbesmetting?',
    'Door routes zo te ontwerpen dat ze goed leeglopen, restanten zichtbaar en bereikbaar te maken en de volgorde van partijen mee te nemen. Leg vast welke grondstoffen strikt gescheiden moeten blijven.'),
   ('Speelt GMP+ een rol in het ontwerp?',
    'GMP+ is een certificatieschema voor veilig diervoeder, beheerd door GMP+ International, waarmee veel bedrijven in de sector werken. De eisen gelden voor uw bedrijf. Deel de eisen die voor uw locatie gelden, dan nemen we ze mee in de uitgangspunten voor reinigbaarheid en restanten.'),
   ('Is stof van diervoedergrondstoffen explosief?',
    'Veel organische grondstoffen kunnen in een stofwolk tot ontploffing komen. Of dat bij uw product speelt, blijkt uit de stofgegevens. Samen met uw zone-indeling bepalen die de uitvoering van filters en sluizen.'),
  ],
  sources=[SRC_GMP, SRC_GESTIS, SRC_ATEX153],
 ),
 'recycling': dict(
  name='Recycling', long='Kunststofrecycling', nav='Recycling',
  title='Flakes en regrind.<br><em>Beheerst verplaatsen.</em>',
  lead='Schurende flakes, licht en pluizig materiaal en veel stof uit malen en wassen. Slijtage, verstopping en statische lading bepalen hier het ontwerp.',
  image='20-project-recycling', alt='Illustratie van een recyclinglijn met cyclonen, filter en big-bag-vulling',
  caption=('Recycling · kunststof', 'Illustratieve procesopstelling'),
  seo_title='Transport en afzuiging voor recycling',
  description='Pneumatisch transport, big-bag-vulling en stofafzuiging voor kunststofrecycling. Slijtage door flakes, lage stortgewichten, verstopping en statische lading.',
  topic_title='Proces in kunststofrecycling',
  topic_help='Welk materiaal verwerkt u (flakes, regrind, fluff), hoeveel per uur en over welke afstand? Noem ook waar slijtage of verstopping optreedt.',
  issues=[
   ('Slijtage door schurend materiaal', 'Flakes en regrind slijten bochten, leidingen en sluizen, vooral bij hoge snelheid.',
    'Bochtvorm, wanddikte en snelheid kiezen we op het materiaal; slijtdelen moeten bereikbaar zijn.'),
   ('Laag stortgewicht en fluff', 'Licht, pluizig materiaal vormt bruggen en verstopt uitlopen en sluizen.',
    'Ruime doorlaten, aangepaste uitlopen en een transportregime dat bij het lage stortgewicht past.'),
   ('Stof en statische lading', 'Malen en drogen geven fijn stof; kunststof laadt zich op tijdens transport.',
    'Aarding en potentiaalvereffening van leidingwerk en componenten, en afzuiging bij de bron.'),
   ('Vullen en afvoeren', 'Big bags moeten vol, stofarm en zonder lange stilstand worden gewisseld.',
    'Vulstations met stofafzuiging en een buffer zodat de lijn doorloopt tijdens het wisselen.'),
  ],
  route=[
   ('Ontvangen', 'opslaan', 'Materiaal uit maal- of wasstap, of uit big bags.'),
   ('Doseren', 'doseren', 'Een sluis voert flakes gelijkmatig in, met aandacht voor slijtage en brugvorming.'),
   ('Transporteren', 'pneumatisch-transport', 'Pneumatisch transport naar silo, extruder of vulstation.'),
   ('Afscheiden', 'zeven-en-scheiden', 'Cyclonen scheiden het product uit de transportlucht.'),
   ('Afzuigen en vullen', 'stofafzuiging', 'Een filterinstallatie vangt het stof af; big bags worden stofarm gevuld.'),
  ],
  solutions=[
   ('pneumatisch-transport', 'Veel stromen over afstand verbinden, met een regime dat slijtage beperkt.'),
   ('stofafzuiging', 'Stof uit malen, drogen en vullen afvangen bij de bron.'),
   ('opslaan', 'Silo’s en big bags vullen en lossen zonder verstopping of stofwolk.'),
   ('zeven-en-scheiden', 'Product uit de lucht halen en fijne delen afscheiden.'),
  ],
  components=[
   ('transportbocht', 'De bocht met de meeste slijtage: radius en wanddikte kiest u op het materiaal.'),
   ('cycloonafscheider', 'Scheidt flakes uit de transportlucht en ontlast het filter.'),
   ('doorblaassluis', 'Voert schurend materiaal in de transportleiding; slijtage en doorlaat wegen mee.'),
   ('bigbag-vulstation', 'Vult big bags met stofafzuiging bij de vulkop.'),
   ('zakkenfilter', 'Centrale afzuiging van stof uit malen, drogen en vullen.'),
  ],
  requirements=[
   ('Slijtage', 'Hardheid en vorm van het materiaal, snelheid en bochtvorm.'),
   ('Stortgewicht', 'Laag stortgewicht, fluff en de neiging tot brugvorming.'),
   ('Statische lading', 'Aarding en potentiaalvereffening van alle geleidende delen.'),
   ('Stof', 'Stof uit malen en drogen, en de stofgegevens voor explosieveiligheid.'),
  ],
  project_sector='Recycling',
  knowledge=['slijtage-transportbochten', 'cycloon-als-voorafscheider', 'atex-explosieveiligheid'],
  faq=[
   ('Hoe lang gaat een transportbocht mee bij flakes?',
    'Daar is geen vast getal voor. De levensduur hangt af van het materiaal, de snelheid, de bochtvorm en de wanddikte. Meet de wanddikte op vaste momenten; dat geeft de beste voorspelling voor uw installatie.'),
   ('Waarom verstopt licht materiaal sneller?',
    'Fluff en flakes met een laag stortgewicht haken in elkaar en vormen bruggen in uitlopen en sluizen. Ruimere doorlaten, aangepaste uitlopen en een passende transportsnelheid helpen. Test bij twijfel met uw eigen materiaal.'),
   ('Hoe beperkt u statische lading bij kunststof?',
    'Door alle geleidende delen te aarden en onderling te verbinden, en waar nodig geleidende of antistatische materialen te gebruiken. Bij brandbaar stof hoort dit bij de explosieveiligheid van de installatie.'),
   ('Kunnen big bags automatisch worden gevuld?',
    'Ja, dat kan. In het PET-recyclingproject zijn drie dubbele automatische big-bag-vulstations gerealiseerd. De uitvoering hangt af van het materiaal, het gewenste vulgewicht en de wisseltijd.'),
  ],
  sources=[SRC_ATEX153, SRC_ARBO_EX],
 ),
 'chemie': dict(
  name='Chemie', long='Chemische industrie', nav='Chemie',
  title='Elk product anders.<br><em>Gesloten verwerken.</em>',
  lead='Corrosief, hygroscopisch, toxisch of brandbaar: in de chemie verschillen producten sterk. Materiaalkeuze, afdichtingen en een gesloten proces zijn daarom het vertrekpunt.',
  image='19-granulaat-macro', alt='Granulaat valt uit een RVS uitloop in een gesloten opvangvat',
  caption=('Chemie', 'Illustratieve procesopstelling'),
  seo_title='Gesloten transport voor de chemie',
  description='Gesloten pneumatisch transport, doseren en filtratie voor de chemische industrie. Materiaalkeuze, afdichtingen, operatorbescherming en explosieveiligheid.',
  topic_title='Proces in de chemie',
  topic_help='Welk product verwerkt u en wat zijn de belangrijkste eigenschappen (corrosief, hygroscopisch, toxisch, brandbaar)? Een veiligheidsinformatieblad helpt ons op weg.',
  issues=[
   ('Uiteenlopende producteigenschappen', 'Corrosieve, hygroscopische of toxische producten stellen elk eigen eisen.',
    'Materialen en afdichtingen kiezen we op het product; het veiligheidsinformatieblad is het startpunt.'),
   ('Gesloten systemen', 'Vocht, zuurstof of de omgeving mogen het product soms niet raken.',
    'Gesloten overdracht en, als principe, transport met stikstof of een ander inert gas. Of Airtechnic dit uitvoert: ' + TBD_AT),
   ('Bescherming van de operator', 'Bij storten en lossen kan de operator worden blootgesteld aan stof.',
    'Gesloten aansluitingen en afzuiging bij het stortpunt beperken blootstelling.'),
   ('Explosieveiligheid', 'Brandbare poeders en oplosmiddeldampen kunnen een explosieve atmosfeer vormen.',
    'Stofgegevens en de zone-indeling van uw locatie bepalen de uitvoering.'),
  ],
  route=[
   ('Ontvangen', 'opslaan', 'Product uit big bag, vat of silo, zo gesloten mogelijk.'),
   ('Doseren', 'doseren', 'Een sluis voert gelijkmatig toe, met materialen en afdichtingen op het product.'),
   ('Transporteren', 'pneumatisch-transport', 'Gesloten transport naar reactor, menger of opslag.'),
   ('Filtreren', 'filtratie', 'Proceslucht wordt gefilterd voordat ze de installatie verlaat.'),
  ],
  solutions=[
   ('pneumatisch-transport', 'Een gesloten leiding houdt het product binnen en de omgeving buiten.'),
   ('doseren', 'Nauwkeurige toevoer naar een volgende processtap, met passende materialen.'),
   ('filtratie', 'Proceslucht schoon houden en product terugwinnen.'),
  ],
  components=[
   ('doseersluis-op-maat', 'Rotor, huis en afdichtingen afgestemd op een corrosief of slijtend product.'),
   ('bigbag-losstation', 'Lossen met een afgesloten aansluiting en afzuiging bij de uitloop.'),
   ('manchetafsluiter', 'Sluit een productstroom af met een manchet die bij het medium past.'),
   ('patroonfilter', 'Filtert proceslucht en vangt het product af voor hergebruik.'),
  ],
  requirements=[
   ('Materiaal', 'Corrosie, abrasie en de chemische bestendigheid van afdichtingen.'),
   ('Afscherming', 'Gesloten overdracht en bescherming tegen vocht of zuurstof.'),
   ('Operator', 'Blootstelling bij storten, lossen en onderhoud.'),
   ('Explosieveiligheid', 'Stofgegevens, eventuele dampen en de zone-indeling.'),
  ],
  project_sector=None,
  invite='Er staat nog geen chemieproject op deze site. Heeft u een vergelijkbaar vraagstuk? Beschrijf uw product en proces; dan bespreken we wat mogelijk is.',
  activity=TBD_AT,
  knowledge=['druk-of-vacuumtransport', 'doorvalsluis-of-doorblaassluis', 'atex-explosieveiligheid'],
  faq=[
   ('Welke materialen en afdichtingen zijn geschikt?',
    'Dat hangt af van het product. Corrosieve of oplosmiddelhoudende producten vragen andere materialen en afdichtingen dan een droog, neutraal poeder. Deel het veiligheidsinformatieblad en de procescondities; daarop baseren we de keuze.'),
   ('Waarom kiest u voor een gesloten systeem?',
    'Een gesloten systeem houdt het product binnen en vocht, zuurstof of verontreiniging buiten. Dat beschermt het product, de operator en de omgeving.'),
   ('Hoe wordt de operator beschermd bij het lossen?',
    'Met gesloten aansluitingen tussen verpakking en installatie en met afzuiging bij het stortpunt. Welke maatregelen nodig zijn, volgt uit de risicobeoordeling van uw locatie.'),
   ('Wat als het product brandbaar is?',
    'Dan bepalen de stofgegevens en uw zone-indeling de uitvoering van filters, sluizen en leidingwerk. In ons artikel over ATEX leest u welke gegevens daarvoor nodig zijn.'),
  ],
  sources=[SRC_ATEX153, SRC_ARBO_EX, SRC_GESTIS],
 ),
 'hout': dict(
  name='Hout', long='Houtverwerking', nav='Hout',
  title='Spanen en houtstof.<br><em>Afzuigen bij de bron.</em>',
  lead='Zagen, frezen en schuren geven spanen en fijn stof. Een centrale afzuiging met voorafscheiding en filtratie beschermt de mensen in de werkplaats en beperkt brand- en explosiegevaar.',
  image='32-hero-cycloon', alt='RVS cycloon met aangesloten leidingwerk in een productiehal',
  caption=('Hout · houtverwerking', 'Illustratieve procesopstelling'),
  seo_title='Stofafzuiging voor houtbewerking',
  description='Centrale stof- en spanenafzuiging voor houtverwerking. Cyclonen als voorafscheider, filters, houtstof als gezondheidsrisico en brand- en explosiegevaar.',
  topic_title='Afzuiging in de houtverwerking',
  topic_help='Welke machines wilt u aansluiten, hoeveel draaien er tegelijk en welke houtsoorten verwerkt u? Noem ook of de installatie binnen of buiten komt.',
  issues=[
   ('Spanen en stof bij de machine', 'Elke machine geeft een andere mix van grove spanen en fijn stof.',
    'Afzuigpunten, luchtsnelheid en gelijktijdigheid bepalen het leidingnet en de ventilator.'),
   ('Houtstof en gezondheid', 'Hardhoutstof is kankerverwekkend. In Nederland geldt een wettelijke grenswaarde van 2 mg/m³ als 8-uursgemiddelde.',
    'Afzuiging bij de bron en een filter dat het fijne stof betrouwbaar tegenhoudt.'),
   ('Brand en explosie', 'Houtstof is brandbaar; vonken uit machines kunnen een brand of stofexplosie veroorzaken.',
    'Vonkdetectie en blussing als principe, en een filter dat past bij de stofgegevens en de opstelling.'),
   ('Voorafscheiding', 'Veel grove spanen belasten het filter onnodig.',
    'Een cycloon als voorafscheider vangt de grove fractie af vóór het filter.'),
  ],
  route=[
   ('Afzuigen', 'stofafzuiging', 'Afzuigpunten bij zaag-, frees- en schuurmachines.'),
   ('Transporteren', 'stofafzuiging', 'Een leidingnet met de juiste luchtsnelheid voor spanen en stof.'),
   ('Voorafscheiden', 'zeven-en-scheiden', 'Een cycloon scheidt de grove spanen af.'),
   ('Filtreren', 'filtratie', 'Het filter vangt het fijne houtstof af.'),
   ('Opslaan', 'opslaan', 'Spanen en stof gaan naar silo, container of briketteerpers.'),
  ],
  solutions=[
   ('stofafzuiging', 'Centrale afzuiging bij alle machines, afgestemd op gelijktijdig gebruik.'),
   ('filtratie', 'Het fijne houtstof betrouwbaar tegenhouden en de filters reinigen.'),
   ('zeven-en-scheiden', 'Een cycloon als voorafscheider ontlast het filter.'),
  ],
  components=[
   ('cycloonafscheider', 'Vangt grove spanen af vóór het filter.'),
   ('zakkenfilter', 'Centrale filtratie van fijn houtstof.'),
   ('centrifugaalventilator', 'Brengt de luchtstroom op gang, bij voorkeur aan de schone zijde van het filter.'),
   ('doorvalsluis', 'Voert spanen en stof af onder cycloon of filter en houdt de lucht binnen.'),
   ('leidingdelen', 'Het leidingnet tussen machines, cycloon en filter.'),
  ],
  requirements=[
   ('Gezondheid', 'Blootstelling aan houtstof en de wettelijke grenswaarde.'),
   ('Gelijktijdigheid', 'Welke machines tegelijk draaien en hoeveel lucht elk afzuigpunt nodig heeft.'),
   ('Brand en explosie', 'Vonkdetectie, opstelling van het filter en de stofgegevens.'),
   ('Afvoer', 'Waar spanen en stof naartoe gaan: silo, container of hergebruik.'),
  ],
  project_sector=None,
  invite='Er staat nog geen houtverwerkingsproject op deze site. Heeft u een vergelijkbaar vraagstuk? Vertel welke machines u wilt aansluiten; dan bespreken we de mogelijkheden.',
  activity=TBD_AT,
  knowledge=['cycloon-als-voorafscheider', 'wanneer-filters-vervangen', 'atex-explosieveiligheid'],
  faq=[
   ('Is een cycloon vóór het filter zinvol?',
    'Bij veel grove spanen vaak wel. De cycloon vangt de grove fractie af, zodat het filter minder belast wordt en het fijne stof overblijft. Of het loont, hangt af van de verhouding tussen spanen en fijn stof.'),
   ('Welke grenswaarde geldt voor houtstof?',
    'Voor hardhoutstof geldt in Nederland een wettelijke grenswaarde van 2 mg/m³, gemiddeld over 8 uur. Is hardhoutstof gemengd met ander houtstof, dan geldt die waarde voor al het houtstof. Hardhoutstof is kankerverwekkend; houd de blootstelling daarom zo laag mogelijk. Afzuiging bij de bron is de eerste maatregel.'),
   ('Hoe gaat u om met brand- en explosiegevaar?',
    'Vonkdetectie en blussing in het leidingwerk zijn bij houtverwerking een gangbaar principe. Daarnaast bepalen de stofgegevens en de opstelling van het filter welke beschermende maatregelen nodig zijn. Lees meer in ons artikel over ATEX.'),
   ('Kunnen meerdere machines op één afzuiging?',
    'Ja, mits het net is ontworpen op de machines die tegelijk draaien. Afsluiters per machine houden de luchtsnelheid in de rest van het net op peil.'),
  ],
  sources=[SRC_HOUT, SRC_2004_37, SRC_ATEX153, SRC_GESTIS],
 ),
}

ORDER = ('food', 'feed', 'recycling', 'chemie', 'hout')
INDEX = dict(
  title='Elke sector.<br><em>Een eigen ontwerp.</em>',
  lead='Meel gedraagt zich anders dan flakes, en houtstof anders dan een corrosief poeder. Kies uw sector en zie welke vraagstukken daar spelen en hoe we ze oplossen.',
  image='29-hero-productiehal', alt='Lichte productiehal met RVS silo’s en een blauw draagframe',
  seo_title='Sectoren: food, feed, recycling, chemie, hout',
  description='Pneumatisch transport, stofafzuiging en filtratie per sector: food, diervoeding, kunststofrecycling, chemie en houtverwerking. Zie welke vraagstukken in uw sector spelen.',
)


def sector_file(slug):
    return SECTOR_FILE.format(slug)


def _reverse(field):
    out = {}
    for slug in ORDER:
        for key in SECTORS[slug][field]:
            key = key[0] if isinstance(key, tuple) else key
            out.setdefault(key, [])
            if slug not in out[key]:
                out[key].append(slug)
    return out


# Derived, never maintained by hand
SECTORS_OF_PRODUCT = _reverse('components')
SECTORS_OF_SOLUTION = {}
for _slug in ORDER:
    for _sol in [s for s, _w in SECTORS[_slug]['solutions']] + [r[1] for r in SECTORS[_slug]['route']]:
        SECTORS_OF_SOLUTION.setdefault(_sol, [])
        if _slug not in SECTORS_OF_SOLUTION[_sol]:
            SECTORS_OF_SOLUTION[_sol].append(_slug)
