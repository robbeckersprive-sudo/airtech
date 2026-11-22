"""Translated file names: Dutch file (site root) -> file name in en/ and de/.

Every page listed here is built in all three languages (build.py) and gets hreflang links and a language switcher
target. Pages that are not listed (review / concept pages) stay Dutch-only; links to them from en/ and de/ point
to the Dutch original.
"""

_PAGES = [
    # (nl, en, de)
    ('index.html', 'index.html', 'index.html'),
    ('projecten.html', 'projects.html', 'projekte.html'),
    ('over-ons.html', 'about-us.html', 'ueber-uns.html'),
    ('kennisbank.html', 'knowledge-base.html', 'wissensdatenbank.html'),
    ('componenten.html', 'components.html', 'komponenten.html'),
    # toepassing-pet-recycling.html renders the PET project page (canonical = project-pet-recycling.html): NL-only alias
    # component categories
    ('componenten-cyclonen.html', 'components-cyclones.html', 'komponenten-zyklone.html'),
    ('componenten-blowers-ventilatoren.html', 'components-blowers-fans.html', 'komponenten-geblaese-ventilatoren.html'),
    ('componenten-filters.html', 'components-filters.html', 'komponenten-filter.html'),
    ('componenten-doseersluizen.html', 'components-rotary-valves.html', 'komponenten-zellenradschleusen.html'),
    ('componenten-leidingwerk-koppelingen.html', 'components-piping-couplings.html', 'komponenten-rohrleitungen-kupplungen.html'),
    ('componenten-bigbag-stations.html', 'components-big-bag-stations.html', 'komponenten-big-bag-stationen.html'),
    ('componenten-afsluiters.html', 'components-valves.html', 'komponenten-absperrorgane.html'),
    ('componenten-zeven.html', 'components-screens.html', 'komponenten-siebe.html'),
    # products
    ('cycloonafscheider.html', 'cyclone-separator.html', 'zyklonabscheider.html'),
    ('multicycloon.html', 'multicyclone.html', 'multizyklon.html'),
    ('cycloon-op-maat.html', 'custom-cyclone.html', 'zyklon-nach-mass.html'),
    ('transportafscheider.html', 'conveying-separator.html', 'foerderabscheider.html'),
    ('centrifugaalventilator.html', 'centrifugal-fan.html', 'radialventilator.html'),
    ('draaizuigerblower.html', 'rotary-lobe-blower.html', 'drehkolbengeblaese.html'),
    ('zijkanaalblower.html', 'side-channel-blower.html', 'seitenkanalverdichter.html'),
    ('ventilatorunit.html', 'fan-unit.html', 'ventilatoreinheit.html'),
    ('patroonfilter.html', 'cartridge-filter.html', 'patronenfilter.html'),
    ('zakkenfilter.html', 'bag-filter.html', 'schlauchfilter.html'),
    ('ontluchtingsfilter.html', 'vent-filter.html', 'entlueftungsfilter.html'),
    ('filterelement.html', 'filter-element.html', 'filterelement.html'),
    ('doorvalsluis.html', 'drop-through-rotary-valve.html', 'durchfall-zellenradschleuse.html'),
    ('doorblaassluis.html', 'blow-through-rotary-valve.html', 'durchblas-zellenradschleuse.html'),
    ('doseersluis-uitneembare-rotor.html', 'rotary-valve-removable-rotor.html', 'zellenradschleuse-ausziehbarer-rotor.html'),
    ('doseersluis-op-maat.html', 'custom-rotary-valve.html', 'zellenradschleuse-nach-mass.html'),
    ('leidingdelen.html', 'pipe-components.html', 'rohrleitungsteile.html'),
    ('transportbocht.html', 'conveying-bend.html', 'foerderbogen.html'),
    ('buiskoppeling.html', 'pipe-coupling.html', 'rohrkupplung.html'),
    ('leidingwissel.html', 'diverter-valve.html', 'rohrweiche.html'),
    ('bigbag-losstation.html', 'big-bag-discharge-station.html', 'big-bag-entleerstation.html'),
    ('bigbag-vulstation.html', 'big-bag-filling-station.html', 'big-bag-befuellstation.html'),
    ('bigbag-losframe.html', 'big-bag-discharge-frame.html', 'big-bag-entleergestell.html'),
    ('bigbag-doseerstation.html', 'big-bag-dosing-station.html', 'big-bag-dosierstation.html'),
    ('schuifafsluiter.html', 'slide-gate-valve.html', 'flachschieber.html'),
    ('vlinderklep.html', 'butterfly-valve.html', 'absperrklappe.html'),
    ('manchetafsluiter.html', 'pinch-valve.html', 'quetschventil.html'),
    ('afsluiter-op-maat.html', 'custom-valve.html', 'absperrorgan-nach-mass.html'),
    ('trilzeef.html', 'vibrating-screen.html', 'vibrationssieb.html'),
    ('controlezeef.html', 'check-screener.html', 'kontrollsieb.html'),
    ('trommelzeef.html', 'drum-screen.html', 'trommelsieb.html'),
    ('meerdekszeef.html', 'multi-deck-screen.html', 'mehrdecksieb.html'),
    # knowledge articles
    ('kennis-druk-of-vacuumtransport.html', 'knowledge-pressure-or-vacuum-conveying.html', 'wissen-druck-oder-saugfoerderung.html'),
    ('kennis-wanneer-filters-vervangen.html', 'knowledge-when-to-replace-filters.html', 'wissen-wann-filter-wechseln.html'),
    ('kennis-juiste-blower-selecteren.html', 'knowledge-selecting-the-right-blower.html', 'wissen-das-richtige-geblaese-auswaehlen.html'),
    ('kennis-slijtage-transportbochten.html', 'knowledge-wear-in-conveying-bends.html', 'wissen-verschleiss-in-foerderboegen.html'),
    ('kennis-doorvalsluis-of-doorblaassluis.html', 'knowledge-drop-through-or-blow-through-valve.html', 'wissen-durchfall-oder-durchblasschleuse.html'),
    ('kennis-cycloon-als-voorafscheider.html', 'knowledge-cyclone-as-pre-separator.html', 'wissen-zyklon-als-vorabscheider.html'),
    ('kennis-controlezeef-of-fractioneerzeef.html', 'knowledge-check-screening-or-grading.html', 'wissen-kontrollsieb-oder-klassiersieb.html'),
    ('kennis-bigbag-lossen-onregelmatige-productstroom.html', 'knowledge-big-bag-discharge-irregular-flow.html', 'wissen-big-bag-entleerung-ungleichmaessiger-produktfluss.html'),
    ('kennis-silo-ontluchting-pneumatisch-vullen.html', 'knowledge-silo-venting-pneumatic-filling.html', 'wissen-siloentlueftung-pneumatische-befuellung.html'),
    # solutions
    ('oplossingen-stofafzuiging.html', 'solutions-dust-extraction.html', 'loesungen-staubabsaugung.html'),
    ('oplossingen-filtratie.html', 'solutions-filtration.html', 'loesungen-filtration.html'),
    ('oplossingen-hoogvacuum.html', 'solutions-high-vacuum.html', 'loesungen-hochvakuum.html'),
    ('oplossingen-pneumatisch-transport.html', 'solutions-pneumatic-conveying.html', 'loesungen-pneumatische-foerderung.html'),
    ('oplossingen-doseren.html', 'solutions-dosing.html', 'loesungen-dosieren.html'),
    ('oplossingen-zeven-en-scheiden.html', 'solutions-screening-and-separating.html', 'loesungen-sieben-und-trennen.html'),
    ('oplossingen-opslaan.html', 'solutions-storage.html', 'loesungen-lagern.html'),
    # projects
    ('project-pet-recycling.html', 'project-pet-recycling.html', 'projekt-pet-recycling.html'),
    ('project-eischaalverwerking.html', 'project-eggshell-processing.html', 'projekt-eierschalenverarbeitung.html'),
    ('project-centraal-stofzuigsysteem.html', 'project-central-vacuum-cleaning-system.html', 'projekt-zentrale-staubsauganlage.html'),
    ('project-dierenvoeding.html', 'project-animal-feed.html', 'projekt-tierfutter.html'),
    ('project-driessen-food-extrusion.html', 'project-driessen-food-extrusion.html', 'projekt-driessen-food-extrusion.html'),
]

SLUGS = {nl: {'nl': nl, 'en': en, 'de': de} for nl, en, de in _PAGES}
