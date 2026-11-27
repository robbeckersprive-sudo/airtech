# Oplevering 27-11-2026 — Sectorpagina's (prompt 1) en ATEX / explosieveiligheid (prompt 2)

Niets gecommit. Alle pagina's opnieuw gebouwd in nl / en / de (`python src/build.py`), 0 ontbrekende vertalingen.

## 1. Wat er gebouwd is

**Prompt 1 — ingang per sector**
- `sectoren.html` + vijf sectorpagina's (food, feed, recycling, chemie, hout) in drie talen
  (EN `industries-*.html`, DE `branchen-*.html`). Vaste opbouw: hero · vraagstukken · productroute (stations linken
  naar de oplossingen) · oplossingen · componenten · ontwerpeisen · praktijk · kennis · vragen (+ bronnen) · contact.
- Praktijk toont alleen echte projecten (Food 3, Feed 1, Recycling 1) met link `projecten.html?sector=…`; Chemie en
  Hout krijgen een uitnodiging in plaats van een leeg blok.
- Navigatie: "Sectoren" als derde drawer in de header (foto per sector), derde paneel in het mobiele menu, footer
  (Techniek). Liniaalmarkering rust op Sectoren.
- Afgeleid uit één bron (`SECTORS`): sectorchips op 17 productpagina's, "Toegepast in" op alle 7 oplossingspagina's,
  contactonderwerpen `sector-<slug>`. Homepage: FAQ-antwoord over industrieën linkt naar de vijf pagina's
  (FAQPage-JSON-LD houdt platte tekst); sectorlabels in het projectdossier linken. Projectpagina's: regel "Sector".
- SEO: unieke titles (≤ 60 tekens incl. merk waar mogelijk), descriptions, BreadcrumbList overal, FAQPage alleen met
  antwoorden, CollectionPage op het overzicht, eigen OG-beeld per sector, hreflang/canonical via `page()`.

**Prompt 2 — ATEX en explosieveiligheid**
- A. Kennisartikel "Stofexplosiegevaar: waar let u op bij ATEX?" met zes inhoudssecties, zone-schema (inline SVG,
  "schematisch, niet op schaal"), vergelijkingstabel (7 maatregelen met norm), drie praktijksituaties, checklist,
  "Uit eigen werk" (letterlijke projectformulering PET en dierenvoeding), 16 geverifieerde bronnen, contactonderwerp
  `atex-explosieveiligheid`. Vierde kennisgroep **Veiligheid en hygiëne** op kennisbank en homepage (past zonder
  layoutproblemen; op telefoons scrolt de chiprij zijwaarts zoals voorheen).
- B. Uitvoeringen-mechanisme: `executions` op alle 32 uitvoeringen, `src/execution_data.py` (`EXECUTIONS`,
  `CONFIRMED` = **leeg**), `docs/uitvoeringen-matrix.csv` (32 regels, alles `?`), `tools/import_executions.py`.
  Filtergroep "Uitvoering", tabelkolom, kaartlabel, URL `?uitvoering=`, productregel: verschijnen alleen bij
  bevestigde data. Zonder data byte-gelijk (gecontroleerd).
- C. Stofafzuiging: criterium "explosieveiligheid (zone-indeling, stofgegevens)", vraag "Hoe gaat u om met
  stofexplosiegevaar?" en een tweede kennislink. Filtratie, Pneumatisch transport, Opslaan: één korte vermelding met
  link. Filters, Cyclonen, Doseersluizen: één ATEX-vraag + link. Homepage-FAQ "Leveren jullie installaties voor
  ATEX-zones?" met alleen `[TBD]` (niet in FAQPage). Projecten PET en dierenvoeding: ATEX-vermelding linkt naar het
  artikel. Kiosk: niets aangepast (`check_kiosk.py` PASS, kioskbestanden ongewijzigd).

**Bestanden**
- Nieuw: `src/sector_data.py`, `src/sector_page.py`, `src/knowledge_safety.py`, `src/execution_data.py`,
  `assets/css/sectors.css`, `tools/check_sectors.py`, `tools/import_executions.py`, `tools/structure_norm.py`,
  `docs/uitvoeringen-matrix.csv`, `images/generated-sector-assets.json`, 7 × `images/og-sector-*.jpg` /
  `og-knowledge-atex-explosieveiligheid.jpg`, `.claude/launch.json` (preview), deze map.
- Gewijzigd (bron): `src/build.py`, `components.py` (header/menu/footer), `contact_delivery.py`, `i18n_slugs.py`,
  `i18n_strings.py`, `locales/en.json` + `de.json` (+513 segmenten), `category_data.py`, `cyclone_category_data.py`,
  `category_overview.py`, `category_page.py`, `product_data.py`, `product_page.py`, `solution_data.py`,
  `solution_page.py`, `project_page.py`, `home_practice.py`, `home_knowledge.py`, `knowledge_index.py`,
  `knowledge_page.py`, `knowledge_data.py`, `pages.py`; CSS `category-overview`, `component-detail`, `home-blocks`,
  `knowledge-article`, `polish`, `solutions`; JS `category.js`; checks `check_categories`, `check_knowledge`,
  `check_products`, `check_solutions`; `README.md`. Plus alle gegenereerde HTML.

## 2. Screenshots (deze map)
`sector-food-1440.png`, `sector-food-390.png`, `sector-overzicht-1440.png`, `sector-feed-de-1440.png`,
`atex-artikel-1440.png`, `atex-artikel-390.png`, `atex-artikel-en-1440.png`, en met **tijdelijke fictieve testdata**
(niet opgeleverd): `filter-testdata-1440.png`, `filter-testdata-390.png`, `product-uitvoeringen-testdata.png`.

## 3. Vragenlijst voor Airtechnic
1. Welke componenten zijn in een ATEX-uitvoering leverbaar, en in welke categorie / zone? (vul `docs/uitvoeringen-matrix.csv`)
2. Welke zijn food-grade leverbaar, met welke materialen en welke documentatie (verklaring 1935/2004)?
3. Stelt Airtechnic zone-indelingen of een explosieveiligheidsdocument op, of werkt het met een partner?
4. Levert Airtechnic explosiedrukontlasting, ontkoppeling (bv. beproefde sluizen) of vonkdetectie, zelf of via partners?
5. Voert Airtechnic transport met stikstof / inert gas uit?
6. Wat mag concreter gezegd worden over de ATEX-uitvoering in de projecten PET-recycling en dierenvoeding?
7. Is Airtechnic actief in de chemie en in de houtverwerking? Zijn er referenties of cases (met toestemming)?
8. Mogen klantlogo's of referenties per sector worden getoond?

## 4. `[TBD]`-markeringen
| Locatie | Bron | Vraag |
|---|---|---|
| `sectoren-chemie.html`, vraagstuk "Gesloten systemen" | `sector_data.py` r.236 | Voert Airtechnic inert transport uit? |
| `sectoren-chemie.html`, praktijk "Ervaring in deze sector" | `sector_data.py` r.267 | Actief in chemie? |
| `sectoren-hout.html`, praktijk "Ervaring in deze sector" | `sector_data.py` r.328 | Actief in houtverwerking? |
| `kennis-atex-explosieveiligheid.html`, sectie "Per component" | `knowledge_safety.py` r.95 | Transport met inert gas door Airtechnic? |
| `index.html`, FAQ "Leveren jullie installaties voor ATEX-zones?" | `pages.py` r.386 | Antwoord na bevestiging (zie vraag 1–4) |
Zelfde markeringen in EN/DE (ongewijzigd `[TBD: bevestigen door Airtechnic]`).

## 5. Gebruikte bronnen (alle geopend en gecontroleerd op 27-11-2026)
- EUR-Lex: Richtlijn 2014/34/EU, 1999/92/EG (zone-definities NL/EN/DE, bijlage II B, art. 8), Verordening (EG)
  1935/2004, Richtlijn 2004/37/EG (geconsolideerd 2024-04-08; hardhoutstof bijlage I/III).
- wetten.overheid.nl: Arbobesluit (§ Explosieve atmosferen, art. 3.5a–3.5f; EVD art. 3.5c; zones art. 3.5d lid 5),
  Arbeidsomstandighedenregeling bijlage XIII (hardhoutstof 2 mg/m³, TGG 8 uur).
- Arboportaal: Arbobesluit artikel 3.5c. Europese Commissie: ATEX-richtsnoeren 6e editie (jan. 2026).
- IFA GESTIS-STAUB-EX: database, St-klassen (St 1 ≤ 200, St 2 200–300, St 3 > 300 bar·m/s), toepasbaarheidsgrenzen.
- Normen: BSI EN 14491:2012, EN 16009:2011, EN 15089:2009; NEN EN 14373 (2021+A1:2025), EN 14460:2018,
  EN 1127-1:2019; IEC 60079-10-2; DIN EN 61340-4-4 (big bags type A–D).
- GMP+ International (Feed Safety Assurance), EHEDG.
- Correcties t.o.v. de opdracht: EVD staat in art. **3.5c** (niet 3.5e); big bag type D is *isolerend* (niet
  antistatisch); St 0 niet opgenomen (niet primair te bevestigen).

## 6. Resultaten van de controles
| Controle | Resultaat |
|---|---|
| `python src/build.py` | OK, 0 ontbrekende segmenten (en/de) |
| `check_sectors.py` (nieuw) | PASS, 18 pagina's in 3 talen + navigatie + afgeleide chips |
| `check_knowledge.py` | PASS (incl. vierde groep) |
| `check_categories.py` | PASS (incl. uitvoeringen + certificeringsvangnet) |
| `check_products.py`, `check_solutions.py` | PASS |
| `check_i18n.py` | 219 pagina's, 0 problemen |
| `check_i18n_browser.py` | 0 problemen |
| `check_kiosk.py` | PASS |
| `i18n_sync.py check` | 0 issues |
| Playwright-matrix: 6 pagina's × 3 talen × 5 breedtes × met/zonder JS, reduced motion | sector- en kennispagina's: 0 overflow, 0 console-fouten |
| Filter met testdata | dimmen, EN-combinatie, teller, URL (deep link, onbekende waarde genegeerd), tabelkolom, toetsenbord, zonder JS alles zichtbaar; na terugzetten byte-gelijk |
| Header 1024–1440 px nl/en/de | geen overflow na compactere afstand 1040–1319 px |
| Externe bronlinks | alle bereikbaar en juist document (EUR-Lex en wetten.overheid.nl via browser i.v.m. botcontrole) |
| `npm run build` vs HEAD | +0,8–1,9 KB gzip HTML per pagina (header-drawer), CSS/JS ±1 KB; geen extra beeldrequests |

**Al aanwezig vóór deze opdracht (gevonden en vermeld):**
- `check_knowledge`, `check_categories` en `check_products` faalden al op HEAD (inhoudsverschillen sinds de
  v2-templates, en de `/beheer.html`-link). Opgelost met `tools/structure_norm.py`; de controles bewaken het skelet weer.
- `check_i18n_browser` faalde op HEAD: `polish.css` verborg NL en DE in de taalwissel op desktop. **Gerepareerd.**
- DE-footer liep 10 px over op 320 px. **Gerepareerd** (links mogen afbreken).
- Homepage-hero (`.ds-box`) loopt op 320 px 9–32 px over; niet aangeraakt (buiten scope).
- Header-drawers (ook Oplossingen/Componenten): Tab na openen gaat naar het volgende menu-item, niet de drawer in.

## 7. Bewust niet doorgevoerd (voorstellen)
- **Hygiënisch ontwerp in poederhandling** — tweede artikel (EHEDG-principes, Verordening 1935/2004, droog/nat reinigen,
  allergenen), de food-tegenhanger van het ATEX-artikel, aansluitend op de sectorpagina Food.
- **Compacte rij "Uw sector" op de homepage** — niet gebouwd zonder akkoord (homepage is afgesteld).
- **`sitemap.xml`** met hreflang-alternates vanuit `build.py` (lijst `i18n.SLUGS`; `build-vercel.mjs` kopieert hem mee).
- **Sectorfilter in de kennisbank.**
- **Link "Componenten in ATEX-uitvoering"** op `componenten.html` en filterlinks vanuit het ATEX-artikel, zodra er
  bevestigde data is.
