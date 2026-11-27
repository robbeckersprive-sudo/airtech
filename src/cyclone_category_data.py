"""Approved Cyclonen content, rendered through the shared category template."""
from category_overview import CategoryOption

CYCLONES = {'name': 'Cyclonen & afscheiders',
 'heading': 'Cyclonen &amp;<br><em>afscheiders</em>',
 'nav': 'Cyclonen',
 'crumb': 'Cyclonen',
 'intro': 'Van productterugwinning tot voorafscheiding. Vind een uitvoering die past bij uw materiaal, '
          'luchtdebiet en de plek in uw proces.',
 'hero': '27-cycloon-maatwerk',
 'hero_alt': 'RVS cycloon met aangesloten leidingwerk en een blauw draagframe',
 'caption': 'Cycloon met aangesloten leidingwerk',
 'items': [CategoryOption(name='Enkelvoudige cycloon',
                          feature='Eén scheidingskamer.',
                          use='Productterugwinning of voorafscheiding uit proceslucht.',
                          image='04-cycloon-vrijstaand',
                          alt='RVS cycloon op een blauw onderstel',
                          href='cycloonafscheider.html',
                          action='Bekijk de cycloon',
                          applications='luchtstroom',
                          variant='enkelvoudig',
                          photo=False,
                          executions=('atex', 'food')),
           CategoryOption(name='Multicycloon',
                          feature='Meerdere kleinere cyclonen parallel.',
                          use='Verdeling van het luchtdebiet over meerdere scheidingskamers.',
                          image='26-multicycloon',
                          alt='Vier RVS cyclonen parallel in één frame',
                          href='?aanvraag=multicycloon#contact',
                          action='Bespreek de uitvoering',
                          applications='luchtstroom capaciteit',
                          variant='multi',
                          photo=False,
                          executions=('atex', 'food')),
           CategoryOption(name='Cycloon op maat',
                          feature='Afmetingen, materiaal en aansluitingen op maat.',
                          use='Een nieuwe of bestaande proceslijn met specifieke inbouweisen.',
                          image='16-cycloon-maatwerk-vrijstaand',
                          alt='Voorbeeld van een RVS cycloon met tangentiële inlaat en blauw onderstel',
                          href='?aanvraag=cycloon-maatwerk#contact',
                          action='Bespreek uw inbouw',
                          applications='luchtstroom',
                          variant='maatwerk',
                          photo=False,
                          executions=('atex', 'food')),
           CategoryOption(name='Transportafscheider',
                          feature='Scheidt product van transportlucht bij het afgiftepunt.',
                          use='Overdracht van poeders of granulaten naar opvang of een volgende processtap.',
                          image='28-transportafscheider',
                          alt='RVS afscheider met aansluitingen voor pneumatisch transport',
                          href='?aanvraag=transportafscheider#contact',
                          action='Bespreek uw transportsituatie',
                          applications='luchtstroom pneumatisch',
                          variant='transport',
                          photo=False,
                          executions=('atex', 'food'))],
 'applications': [('luchtstroom', 'Scheiding uit luchtstroom'),
                  ('capaciteit', 'Hoger luchtdebiet'),
                  ('pneumatisch', 'Pneumatisch transport')],
 'criteria': [('Materiaal en gewenste afscheiding',
               'Wat moet uit de luchtstroom worden gehaald? Deel het producttype, de deeltjesgrootte en wat '
               'u met het afgescheiden materiaal wilt doen.'),
              ('Luchtdebiet en procescondities',
               'Geef het luchtdebiet, de materiaalbelasting, temperatuur en bedrijfsdruk door. Bepaal ook '
               'hoeveel drukverlies de installatie toelaat.'),
              ('Inbouw, afvoer en filtratie',
               'Breng opstelruimte, aansluitmaten en productafvoer in beeld. Vermeld de eisen aan de '
               'uitgaande lucht en welke filtratie al aanwezig is.')],
 'cutaway': '13-cycloon-doorsnede',
 'cutaway_alt': 'Doorsnede met lucht in de kern en afgescheiden materiaal langs de wand',
 'principle': 'Zo werkt de scheiding',
 'explanation': 'Volg de lucht en het product van inlaat tot uitlaat.',
 'principle_action': 'Bekijk de interactieve doorsnede',
 'principle_href': 'cycloonafscheider.html#werking',
 'faq': [('Wanneer kies ik voor een enkelvoudige cycloon of een multicycloon?',
          'Een enkelvoudige cycloon heeft één scheidingskamer. Een multicycloon verdeelt de luchtstroom over '
          'meerdere kleinere cyclonen. Welke opstelling past, hangt af van het luchtdebiet, de '
          'deeltjesverdeling, het toegestane drukverlies en de inbouwruimte. We vergelijken deze '
          'uitgangspunten voordat we een uitvoering adviseren.'),
         ('In welke processen worden cyclonen en afscheiders toegepast?',
          'Cyclonen worden ingezet bij industriële stofafzuiging, productterugwinning en het scheiden van '
          'vaste stoffen uit transportlucht. Denk aan poeders, granulaten, vezels of spaanders. Of '
          'cycloontechniek geschikt is, beoordelen we op basis van het materiaal en de gewenste scheiding.'),
         ('Wat is het verschil tussen een cycloon en een filter?',
          'Een cycloon scheidt deeltjes door de beweging van de luchtstroom, zonder filtermedium. Een filter '
          'vangt deeltjes op met bijvoorbeeld een filterpatroon of filterdoek. Voor fijnere deeltjes kan '
          'aanvullende filtratie nodig zijn. Een cycloon kan dan als voorafscheider de stofbelasting van het '
          'filter beperken.'),
         ('Kan een cycloon in een bestaande installatie worden ingebouwd?',
          'Bij een bestaande installatie beoordelen we de aansluitmaten, beschikbare hoogte, luchtbalans en '
          'productafvoer. Ook de capaciteit van de aanwezige ventilator of blower en de ruimte voor '
          'inspectie zijn belangrijk. Zo wordt duidelijk welke aanpassingen nodig zijn voor een passende '
          'integratie.'),
         ('Welke gegevens zijn nodig voor advies over een afscheider?',
          'Deel bij voorkeur het producttype, de deeltjesgrootte, het luchtdebiet, de hoeveelheid meegevoerd '
          'materiaal en de procestemperatuur. Vermeld ook de bedrijfsdruk, gewenste afscheiding en '
          'beschikbare ruimte. Een installatietekening of foto helpt om de aansluitingen te beoordelen. '
          'Ontbrekende gegevens bespreken we tijdens de analyse.'),
         ('Waarvan hangen de kosten van een cyclooninstallatie af?',
          'De kosten hangen af van de afmetingen, materiaalkeuze, uitvoering en benodigde onderdelen rondom '
          'de cycloon. Ook leidingwerk, productafvoer, eventuele nafiltratie en montage bepalen de omvang '
          'van het project. Voor een gerichte offerte brengen we eerst uw procesgegevens en de '
          'leveringsomvang in kaart.'),
         ('Wat betekent ATEX voor een cycloon?',
          'Een cycloon is een besloten ruimte waarin bij brandbaar stof een stofwolk hangt. De stofgegevens en uw '
          'zone-indeling bepalen dan de uitvoering, bijvoorbeeld aarding, explosiedrukontlasting en ontkoppeling '
          'naar de rest van de installatie. We stemmen de uitvoering af op de zone-indeling en de stofgegevens die '
          'u aanlevert. In ons artikel over ATEX en explosieveiligheid leest u welke gegevens nodig zijn.')],
 'related_extra': ('Stofexplosiegevaar en ATEX', 'kennis-atex-explosieveiligheid.html'),
 'topic': 'cyclonen',
 'topics': ('multicycloon', 'cycloon-maatwerk', 'transportafscheider'),
 'contact_title': 'Samen de juiste afscheider kiezen?',
 'request': 'Deel uw materiaal, luchtdebiet en gewenste afscheiding. We denken mee over de uitvoering en de '
            'aansluiting op uw installatie.',
 'title': 'Cyclonen en afscheiders op maat | Airtechnic Solutions',
 'description': 'Vergelijk cyclonen, multicyclonen en afscheiders voor stofafscheiding en pneumatisch '
                'transport. Airtechnic Solutions adviseert over de juiste uitvoering.',
 'og': 'og-16-cycloon-detail-inlaat.jpg'}
