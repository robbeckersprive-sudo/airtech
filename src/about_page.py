"""About Airtechnic: expertise, practical engineering and a direct contact path."""
from components import page, breadcrumb, breadcrumb_jsonld, pic, sym, icon, SITE, ORG


def about_page():
    crumbs = [('Home', 'index.html'), ('Over ons', 'over-ons.html')]
    expertise = [
        ('Pneumatisch transport', 'Pneumatisch transport', 'Product in beweging. Met lucht.', 'Ontwerp en levering van druk- en vacuümtransportsystemen voor poeders, granulaten en bulkstoffen.', 'oplossingen-pneumatisch-transport.html', '07-leidingwerk-vrijstaand'),
        ('Industriële luchttechniek', 'Industriële luchttechniek', 'De juiste luchtstroom maakt het verschil.', 'Ventilatoren, blowers, stofafzuiging, filtratie en luchtbehandelingssystemen voor industriële toepassingen.', 'oplossingen-stofafzuiging.html', '03-blower-vrijstaand'),
        ('Scheidingstechnieken', 'Zeven en scheiden', 'Haal meer uit elke fractie.', 'Poederzeven, windzifters, luchtmessen en zigzagunits voor classificatie en productscheiding.', 'oplossingen-zeven-en-scheiden.html', '10-zeef-vrijstaand'),
        ('Solids processing', 'Solids processing', 'Van grondstof naar een beheerst proces.', 'Oplossingen voor het doseren, transporteren, zeven, scheiden en verwerken van bulkgoederen.', 'oplossingen-doseren.html', '06-doseersluis-vrijstaand'),
    ]
    cards = ''.join(f'''<article class="about-expert">
      <div class="about-expert__image">{pic(img, '', '(min-width: 800px) 23vw, 65vw')}</div>
      <div class="about-expert__copy">{sym(symbol)}<h3>{name}</h3><p class="about-expert__claim">{claim}</p><p>{text}</p>
      <a href="{href}">Ontdek {name.lower()}<span class="visually-hidden"> bij Airtechnic</span></a></div>
    </article>''' for name, symbol, claim, text, href, img in expertise)
    reasons = [
        ('Techniek die begint met luisteren', 'We verdiepen ons in uw product, capaciteit en productieomgeving. Zo krijgt technisch advies een praktisch vertrekpunt.'),
        ('Kennis van materiaal én lucht', 'Poeders, granulaten en bulkstoffen vragen elk om een eigen aanpak. We bekijken product- en luchtstromen in samenhang.'),
        ('Een component of het complete geheel', 'Van een zorgvuldig geselecteerd onderdeel tot een complete procesinstallatie: de oplossing sluit aan op uw vraag.'),
        ('Praktisch en energie-efficiënt', 'We stemmen componenten en procescondities op elkaar af, met aandacht voor energiegebruik, bereikbaarheid en onderhoud.'),
        ('Persoonlijk betrokken', 'Korte lijnen en heldere afstemming. We nemen u mee in de technische keuzes en begeleiden u bij de uitwerking.'),
    ]
    reasons_html = ''.join(f'<li>{icon("check")}<div><h3>{title}</h3><p>{text}</p></div></li>' for title, text in reasons)
    body = f'''
    <section class="about-hero" aria-labelledby="about-title">
      <div class="container">{breadcrumb(crumbs)}
        <div class="about-hero__heading"><h1 id="about-title">Grip op uw proces.<br><em>Begint met begrijpen.</em></h1>
          <div class="about-hero__intro"><p>Wij zijn Airtechnic Solutions. We verbinden kennis van lucht en bulkstoffen met de praktijk van uw productie.</p>
          <a class="btn" href="#kennismaken">Maak kennis met ons</a></div></div>
        <figure class="about-hero__figure">
          {pic('about-installatie', 'Illustratieve industriële installatie met RVS transportleidingen en cycloonafscheiders', '90vw', eager=True)}
          <figcaption><strong>Het hele proces in beeld.</strong><span>Van losse component tot complete installatie.</span></figcaption>
        </figure>
        <div class="about-hero__foot"><span>Transporteren · Scheiden · Filteren · Verwerken</span><span>Airtechnic Solutions / Beek en Donk</span></div>
      </div>
    </section>
    <section class="about-section about-intro" aria-labelledby="about-belief"><div class="container about-two">
      <h2 class="h2" id="about-belief">Uw product kennen.<br><em>Uw proces begrijpen.</em></h2>
      <div><p class="about-lead">Een goed proces vraagt om meer dan goede componenten. Het vraagt om inzicht in hoe alles samenwerkt.</p>
      <p>Airtechnic Solutions ondersteunt industriële bedrijven bij het transporteren, scheiden, filteren en verwerken van poeders, granulaten en bulkstoffen. Dankzij onze brede kennis van product- en luchtstromen leveren wij zowel losse componenten als complete procesinstallaties.</p>
      <p>We combineren engineering, praktijkervaring en betrouwbare componenten tot efficiënte procesoplossingen. Altijd met uw materiaal, uw installatie en uw doel als uitgangspunt.</p></div>
    </div></section>
    <section class="about-section about-expertise" aria-labelledby="about-expertise-title"><div class="container">
      <div class="about-two about-section-head"><h2 class="h2" id="about-expertise-title">Vier expertises.<br><em>Eén samenhangend proces.</em></h2><p>Product en lucht laten zich niet los van elkaar bekijken. Daarom brengen wij deze disciplines samen in één technische oplossing.</p></div>
      <div class="about-experts">{cards}</div>
    </div></section>
    <section class="about-section about-why" aria-labelledby="about-why-title"><div class="container about-two">
      <div class="about-why__story"><h2 class="h2" id="about-why-title">Technisch doordacht.<br><em>Persoonlijk betrokken.</em></h2>
        <p>U kent uw productie. Wij kennen de techniek erachter. Samen komen we tot een oplossing die in de praktijk werkt.</p>
        <figure>{pic('about-materiaal', 'Illustratief beeld van materiaalonderzoek met granulaat, poeder en een technisch ontwerp', '(min-width: 800px) 43vw, 90vw')}<figcaption>Elk ontwerp begint bij het materiaal.</figcaption></figure>
      </div><ul class="about-reasons">{reasons_html}</ul>
    </div></section>
    <section class="about-section about-partner" aria-labelledby="about-partner-title"><div class="container">
      <div class="about-two about-section-head"><h2 class="h2" id="about-partner-title">Van eerste vraag<br><em>naar de juiste richting.</em></h2><p>Een nieuwe installatie, een knelpunt in uw proces of een component dat aan vervanging toe is: we denken graag met u mee.</p></div>
      <ol class="about-steps"><li><h3>We luisteren</h3><p>Wat verwerkt u? Wat wilt u bereiken? We brengen uw procesvraag en de randvoorwaarden in beeld.</p></li><li><h3>We denken mee</h3><p>We vertalen uw uitgangspunten naar een technische richting en maken de afwegingen begrijpelijk.</p></li><li><h3>We maken het concreet</h3><p>We stemmen componenten, engineering en de verdere uitwerking af op wat uw proces nodig heeft.</p></li></ol>
      <a class="about-textlink" href="index.html#steps-title">Meer over onze werkwijze</a>
    </div></section>
    <section class="about-section about-contact" id="kennismaken" aria-labelledby="about-contact-title"><div class="container about-two">
      <div><h2 id="about-contact-title">Goed werk begint<br><em>met een goed gesprek.</em></h2><p>Vertel ons wat u verwerkt en waar u tegenaan loopt. Een korte toelichting is genoeg om samen de eerste stap te zetten.</p><a class="btn" href="index.html#contact">Bespreek uw vraagstuk</a></div>
      <div class="about-contact__direct"><h3>Liever direct contact?</h3><a href="tel:+31850660243">+31 (0)85 0660 243</a><a href="mailto:info@airtechnicsolutions.com">info@airtechnicsolutions.com</a><address>Scherpenbeemd 3<br>5741 TX Beek en Donk</address><p>Handig voor het eerste gesprek: uw materiaal, gewenste capaciteit en een korte omschrijving van uw proces.</p></div>
    </div></section>
    <p class="container about-image-note">De sfeer- en productbeelden op deze pagina zijn illustratief.</p>
    '''
    description = 'Maak kennis met Airtechnic Solutions. Technisch advies, engineering en praktische oplossingen voor industriële luchttechniek, pneumatisch transport en bulkverwerking.'
    ld = {'@context': 'https://schema.org', '@type': 'AboutPage', 'name': 'Over Airtechnic Solutions', 'url': SITE+'/over-ons.html', 'about': {'@type': 'Organization', 'name': ORG}}
    return page('over-ons.html', 'Over ons | Airtechnic Solutions', description, 'og-about-installatie.jpg', body,
                [ld, breadcrumb_jsonld(crumbs, SITE+'/over-ons.html')], html_cls='about-page', nav_current='Over ons', stylesheet='assets/css/about.css')
