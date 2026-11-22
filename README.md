# Airtechnic Solutions — "Flow" templates

Static, responsive build of the four Flow templates. No framework, no runtime dependencies.

## GitHub en Vercel

De website wordt beheerd in [robbeckers/airtechnology](https://github.com/robbeckers/airtechnology).
Zie [DEPLOYMENT.md](DEPLOYMENT.md) voor de Vercel-instellingen en configuratie van het contactformulier.
`npm run build` zet de ingecheckte pagina's en websitebestanden klaar in `dist/`.

| Template | File |
|---|---|
| 1. Home | `index.html` |
| 2. Kennisartikel | `kennis-druk-of-vacuumtransport.html` |
| 3. Categorie-overzicht | `componenten-cyclonen.html` |
| 4. Productpagina | `cycloonafscheider.html` |

## Structure

```
assets/css/tokens.css   design tokens (CSS custom properties) + @font-face
assets/css/site.css     component library + page sections
assets/js/site.js       behaviour, opt-in via data-attributes (menus, carousel, tabs,
                        scrollspy, share, filters, gallery/lightbox, form validation)
assets/fonts/           legacy Archivo + Inter woff2 (no longer referenced; see Design system v2)
images/                 flow-beeldbibliotheek as AVIF + WebP at 480/800/1200/1600w,
                        OG images (og-*.jpg), manifest.json (dimensions)
src/components.py       shared components: header, breadcrumb, picture, card, product tile,
                        FAQ, contact block, footer, page shell, JSON-LD, SVG illustrations
src/pages.py            the four page templates (content verbatim from the brief)
src/build.py            regenerates the HTML
src/serve.py            tiny static server (works on the D: drive)
```

The HTML files are generated: edit `src/` and run `python src/build.py` (Python 3, no packages).
Asset URLs get an mtime-based `?v=` so browsers pick up CSS/JS changes after a rebuild.

## Airtechnic-logo

`logo()` gebruikt `assets/img/airtechnic-logo-transparent.png`: een met beeldbewerking gemaakte
RGBA-versie van het aangeleverde woordmerk, met echte transparantie. Het origineel blijft bewaard.
`assets/css/brand.css` verzorgt de uitsnede en een eenmalige luchtstroom bij hover/toetsenbordfocus.
Reduced motion toont een stil accent. Desktop en footer tonen de onderregel; de mobiele header
toont alleen het krachtige woordmerk. Op de mobiele fotoheader en in het geopende menu is het
logo wit; in een lichte header blauw. Er is geen afhankelijkheid meer van een extern SVG-filter.
Het bestand is een rasterafbeelding; een officieel SVG blijft de voorkeur voor exacte vectorweergave.

## Componentdetailpagina als sjabloon

Gebruik `product()` in `src/pages.py` als voorbeeld. `src/component_detail.py` levert de
introductie met galerij, sectienavigatie en interactieve doorsnede. `assets/css/component-detail.css`
gebruikt de bestaande kleuren, typografie en knopstijlen.

1. Open met de taak van het component, drie kerngegevens en één adviesactie.
2. Kies herkenbare productaanzichten, met een consistente uitsnede en een vrijstaande achtergrond.
   Registreer AVIF- en WebP-varianten in `images/manifest.json`. Benoem een illustratieve doorsnede als zodanig.
3. Leg de werking uit in korte stappen. Meet de positie van elke markering op de ongecropte
   afbeelding als een horizontaal en verticaal percentage.
4. Geef aan welke gegevens de selectie bepalen, toon waar het component in de installatie past
   en koppel documentatie en advies aan het passende contactonderwerp.
5. Bouw opnieuw met `python src/build.py`. Controleer de galerij, doorsnede, sectielinks en
   het adviespad op desktop en mobiel.

## Categoriepagina als sjabloon

Alle acht componentcategorieën gebruiken één renderer: `category_page()` in `src/category_page.py`.
De goedgekeurde Cycloneninhoud staat in `src/cyclone_category_data.py`; de zeven overige categorieën
staan in `src/category_data.py`. `src/category_overview.py` levert de introductie en de filterkaarten.
De stijlen staan in `assets/css/category-overview.css`. Voeg geen aparte pagina-indelingen toe.

De vaste volgorde is: broodkruimel en hero, vier uitvoeringen met filters, keuzeadvies met drie
criteria en doorsnede, zes veelgestelde vragen, gerelateerde links en het contactformulier.
Adviesonderwerpen worden voor de nieuwe categorieën uit dezelfde inhoud afgeleid in `contact_delivery.py`.
Nieuwe categoriebeelden zijn illustratieve productrenders met transparantie, geoptimaliseerd als AVIF/WebP.
Alle uitvoeringskaarten gebruiken dezelfde donkere rasterachtergrond; installatiebeelden blijven in de hero.

1. Gebruik een installatiebeeld voor de categorie en geef de uitvoeringen herkenbare
   productaanzichten in hetzelfde kader. Voeg de beelden en hun maten toe aan `images/manifest.json`.
2. Beschrijf per uitvoering het onderscheidende kenmerk en de toepassing. Leid de keuzelijst
   voor uitvoering af uit dezelfde gegevens als de kaarten.
3. Gebruik een detailpagina als die beschikbaar is. Koppel de overige kaarten aan een
   passend adviesonderwerp.
4. Bouw met `python src/build.py`. Controleer de vaste structuur, unieke IDs, deelbeelden en navigatie
   met `python tools/check_categories.py`. Controleer vervolgens zoeken, gecombineerde filters, de lege staat,
   adviesonderwerpen en beeldweergave in de browser op 320, 375, 768, 1024 en 1440 pixels.

## Kennisartikel als sjabloon

Gebruik `artikel()` in `src/pages.py` als voorbeeld. `src/knowledge_article.py` levert de
introductie, kernpunten, artikelindeling, vergelijking en uitklapbare voorbeelden.
De stijlen staan in `assets/css/knowledge-article.css`.

1. Open met een herkenbare procesvraag en geef meteen de kern van het antwoord.
2. Beschrijf de werking in korte onderdelen. Koppel de inhoudsnavigatie aan de vaste
   sectie-ID’s en gebruik waar nuttig een schema met labels en een legenda.
3. Vergelijk de relevante situaties op dezelfde criteria. Gebruik de praktijksituaties
   om te laten zien welke gegevens de uitkomst beïnvloeden.
4. Sluit af met de gegevens voor een eerste advies, de gebruikte vakbronnen en bestaande vervolglinks.
5. Bouw met `python src/build.py` en controleer de inhoudslinks, tabel, praktijksituaties en adviesroute op desktop en mobiel.

## Preview

On the D: drive Python's `http.server` fails (`os.fstat` → WinError 87), so use the bundled server:

```
python src/serve.py D:\websites\flow 5183
```

Config `flow-d` in `Documents/Claude/.claude/launch.json` runs the same thing.

## Design system v2 ("precision meets flow", Nov 2026)

- **Type.** Instrument Sans (wdth 92%, 600) for headings and UI; **Instrument Serif italic** as the one expressive
  voice, for the "flow" phrase in a heading (`<em>` inside `split_lines(...)`); JetBrains Mono for technical labels
  (eyebrows, step numbers, counters, table heads, breadcrumbs). Loaded from Google Fonts in `components.page()`.
  **[TBD] self-host before launch** (EU privacy): download the woff2 files and swap the `<link>` for `@font-face`.
- **Depth.** Tonal ramps (`--paper`, `--cream-2`, `--green-950`…), green-tinted layered shadows (`--shadow-1..3`),
  a fixed paper-grain overlay (`body::after`), glass only on floating chrome (header, filter bar, subnav, hotspot cards).
- **Home hero.** The photo is the stage. `.hero__stage` is the exact `object-fit: cover` box of the 3:2 photo,
  computed with container-query units, so the granule canvas, the SVG streamlines and the three hotspots stay on their
  pixels at every viewport. Hotspots map the photo to the
  disciplines and run a slow guided tour. Wide screens: type on the photo's empty wall; portrait/mobile: headline
  first, photo as a framed card.
- **Granule flow** (`assets/js/granule-flow.js`, canvas). The hero uses the photo with an EMPTY glass tube
  (`01-hero-pijpleiding-leeg`, a re-render of the original: same framing, small differences everywhere, so the two
  photos cannot be mixed). `TUBE` in `src/pages.py` = nine cross-sections (bottom wall, top wall) measured on that
  photo; the canvas sits on `GRAIN_BOX` (640,240)-(1420,904). Simulation in tube coordinates (u along the arc,
  v across): a packed bed of ~1,600 granules in 11 sheared rows and two depth layers, with travelling dunes, a solid
  bed body behind it, and ~95 granules hopping through the air above. `images/hero-glass.webp` (walls + long
  reflection streaks cut from the same photo, with alpha) is drawn on top so the granules sit inside the glass.
  Realism pass (Nov 20): bed surface 840 px/s with speed-proportional motion blur (EXPO 1/110 s; prevents row strobing), sprites with a soft contact shadow (ambient occlusion), a travelling
  compression wave applied as a displacement (a velocity field made granules clump and open holes), shade where
  granules enter/leave the steel flanges. Judge: the rendered frame vs the ORIGINAL filled photo, same colour mask,
  CIELAB: mean dE 2.5-3.0 (L p10/50/90 51-55/68-70/84-85 vs 51.8/69/84.7; coverage 13-14% vs 12.9%), stable after
  50 s of simulation (colour judge run at 178 px/s). ~4 ms per frame at 1440 px; pauses off-screen and with the pause button; one still (filled) frame under
  reduced motion.
  If the empty photo changes, re-measure `TUBE` and rebuild `hero-glass.webp` (`python tools/hero_glass.py`, needs numpy, scipy, Pillow; edit its paths/SEC first).
  Earlier tries, both rejected: SVG particles over the filled photo, and a Kling image-to-video loop (Nov 20).
- **Hero proportions + heading** (Nov 20). `--fs-hero` 44 -> 88 px (81 at 1440; was 126) with tracking -0.018 ->
  -0.032em, leading .98, `text-wrap: balance` in an 11ch measure; 8.8vh cap on screens <= 880 px tall. Wide layout
  zooms the stage (`--z` 1.12, anchors `--ax`/`--ay`) so the pipe fills the right side like the first version; hero
  frames of 17:10 and wider (container query on `.hero__visual`) show the photo whole, else the steel pipe runs into
  the type. Measured clearance type block -> lower flange / steel pipe: 6-256 px at 1024x768 ... 2560x1440.
- **Motion** (all off under `prefers-reduced-motion`; the hero has a pause button for WCAG 2.2.2):
  split-line heading reveals (`[data-split]`), staggered section reveals (`[data-reveal]`), scroll-linked hero
  fade + parallax, `[data-parallax]` media, article hero that expands from inset card to full bleed (`[data-expand]`),
  callout lines that draw in, hide-on-scroll header (sticky subnav / filter bar move up with it), reading progress bar.
- **Micro-interactions.** Buttons with arrow-swap disc, light sweep and magnetic pull (`[data-magnetic]`);
  cursor spotlight on cards/tiles (`[data-spotlight]`); sliding pill indicator on case tabs; FAQ icon morph;
  animated underlines; inline form validation.
- Mockup fidelity from the first pass (uppercase Archivo, flat surfaces, section heights) was intentionally
  traded for this direction on request.

## Header "Doorsnede" (Nov 20, concept B rolled out)

`components.header()` renders a contact rail (Kennisbank, Contact, address, phone, email) above a 72px sticky bar.
The header sticks at `top: -var(--rail-h)`, so the rail scrolls away and the bar stays; it never hides on scroll
(the old hide-on-scroll and `html.header-hidden` are gone). Tokens: `--header-h` = sticky bar (72), `--rail-h`
(36, 0 below 760px), `--header-total` = both (hero / split-hero offsets). A ruler along the bar's bottom edge is the
scroll gauge (CSS scroll-driven animation, JS fallback via `data-scroll-progress`; the old top progress bar is
removed) and carries a marker that slides under the hovered item and rests on the current section
(`page(..., nav_current='Cyclonen')` marks Componenten and the item in its drawer). Oplossingen / Componenten open
full-width drawers that swap a figure per hovered item (`SOL_IMG` in components.py maps solutions to photos).
Mobile: burger opens a sheet with an exclusive accordion (`<details name>`). Behaviour in `site.js`, hook
`[data-site-header]`. The three review concepts stay available: `python tools/header_concepts.py` writes
`concept-{a,b,c}[-product].html`.

## Hero "Tekenblad" (Nov 20, hero concept B rolled out)

Wide screens (>= 720px, landscape): `.hero-track` pins the hero for one scroll length (210svh, CSS sticky, native
scroll). `site.js` writes `--q` (linear 0..1) and `--qe` (smoothstep) on the track; the full-bleed photo folds via
`clip-path: inset()` into a framed drawing plate right of the type: drawing grid behind, rulers on two edges,
registration marks, and a title block (Project / Discipline / Blad) whose Discipline follows the hotspot tour.
Plate geometry is measured, not fixed: `--ix` = right edge of the type's *text* (DOM Range, not the wider block boxes)
+ 64px, clamped to 42-60vw; `--ir` aligns with the content edge; on tall screens the plate is capped at 4:5 and the
spare height is shared above/below. Hotspots whose dot falls outside the plate fade, get `inert`, and the tour skips
them. The marquee fades but the pause button stays (granules keep moving, WCAG 2.2.2). Reduced motion: no pin, the
plate state is shown statically. Portrait/phones keep the framed-card hero. `.section--ruled` carries the ruler on
above "Twee specialisaties". Checked at 1024x768, 1440x900, 2560x1440 and 390x844: CLS 0, no overlap with the type.
The review pages `hero-{a,b,c}.html` were generated from the pre-rollout hero; `tools/hero_concepts.py` no longer
applies to the current build.

## Home hero "Doorstroom" + header refinements (Nov 20, current home)

Replaces the "cinema" hero on `index.html` (that one stays reviewable as `hero-concept-cinema.html`). Markup
`src/hero_doorstroom.py` (`doorstroom_hero()`, called from `pages.home()`), styles `assets/css/top.css` (loaded on every
page, after signature.css), behaviour `assets/js/doorstroom.js`.
- **One sheet.** The header overlays the hero (`page(..., overlay=True)`); the photo stage fades into the stone ground at
  the bottom, the drawing grid is anchored to the hero's bottom edge and carries on into "Twee specialisaties" with the
  same pitch; no ruler, no band in between. The Proceslijn's datum mark carries `data-sig-origin`: `signature.js` starts
  the Hartlijn there, so the line visibly turns from the hero down into block 2.
- **Live flow.** Sheet 1 is the empty tube with the granule canvas again (`granule-flow.js`), not the baked photo. New in
  the sim, both opt-in via `data-mode` on the canvas: an eased regime switch *dichte fase* (bed + dunes) / *verdunde
  fase* (thin saltating layer, granules suspended and fast), driven by the "Stromingsbeeld" instrument; and an air pulse
  where a fine pointer moves over the tube (bed bulges, granules kicked up and sped up locally). Sheets 2-5 keep their
  SVG grain flows and traces.
- **Instruments on more sheets** (`src/hero_modes.py`, `SHEET_MODES` + `EFFECTS`): only where the two states teach
  something. Filtratie *Filteren / Afreinigen* (dust cake grows on the cartridges / an air pulse runs down each cartridge
  in turn and the cake falls into the cone), Cyclonen *Grof / Fijn* (coarse product spirals to the outlet / the finest
  part rides the inner vortex up into the dompelbuis), Doseren *Laag / Hoog toerental* (the photographed rotor really
  turns: a glare-free rotor texture from `tools/rotor_texture.py` spins in unsquashed space because the rotor is seen
  in perspective, rx 79 / ry 98; the window glare stays on the glass; `doorstroom.js` integrates the angle so a speed
  change eases, pockets fill under the inlet and empty over the outlet). Wissels has none on purpose: the flap is fixed
  in the photo, a route switch would contradict it. One instrument per sheet (`data-for`, `.is-for`); a choice sets
  `data-mode` (a | b) on its slide and keeps the visitor on that sheet until another station is picked.
- **No bounce.** A box's animation list never depends on slide state (only sheet 1 has the develop intro); the wipe
  is clip-path only. Measured headless: scale jumps > 0.5 % during a sheet change 12 → 0.
- **Proceslijn = the buttons under the hero.** Five stations on a dash-dot centre line with granules running along it,
  red fill to the active sheet, preview plate on hover, the play/pause button's ring is the slide clock (10 s). The
  clock holds on hover/focus of copy, line, callouts or instrument, while the tube is being blown, off-screen, hidden
  tab, and under reduced motion (then nothing moves at all). Pause stops clock, canvas, SVG flows and pulses (2.2.2).
- **Callouts** A/B: ringed point + leader + label chip; hovering shows no extra text (client request; the line stays for
  screen readers). JS hides callouts that would sit under the type, the instrument or in the faded edges, and puts the
  chip on the free side.
- **Header (all pages):** light rail (paper, steel type, red icons, hairline dividers) instead of the black band; nav
  pills on hover/open, chevron turns. On the home page rail + bar are transparent over the hero until scrolled.
- **Breakpoints:** desktop layout from 900px wide and landscape; below that type, sheet, instrument, line stack (swipe
  on the sheet; only the active station shows its label below 640px).
- Checked headless (Chromium, playwright-core) at 1920x1080, 1440x900, 1024x768, 390x844: no console errors, no
  horizontal overflow, keyboard arrows on the stations, one H1, inactive sheets `inert`, reduced motion holds sheet 1.

## Home blocks 2 "Processchema" + 3 "Röntgen" (Nov 20, replace "Processchema A" and "Catalogusbladen")

Markup `src/home_blocks.py` (`schema_block()`, `catalog_block()`, used by `pages.home()`; the old `specs` / `carousel`
markup is left in `pages.py` but not rendered), styles `assets/css/home-blocks.css` (home only, via `page(stylesheet=)`),
behaviour `assets/js/home-blocks.js`. Copy comes from `solution_data` / `category_data` / `cyclone_category_data`.
- **Block 2** draws the heading's promise: two lines of one installation. A Solids processing (product line, steel with
  running granules): Opslaan → Doseren → Pneumatisch transport → Zeven en scheiden → "naar uw proces". B Industriële
  luchttechniek (air line, dashed with running air): Stofafzuiging → Hoogvacuüm → Filtratie → "schone lucht". A dashed
  join drops from A3 to B3: the transport air goes to the filter. Every station is a link (two `<ol>` under an h3 each);
  hover/focus fills the inspector plate next to the heading (render, solution title, first sentence of the lead).
  Arrival: lines draw, stations come in one by one. Below 900px: two vertical lines with photo rows (64px thumbs), the
  join becomes a note between the lines, no inspector.
- **Block 3** keeps the eight groups as light catalogue plates (drawing grid, registration marks, `01/08`) and makes the
  cross-sections the point: a red scan line follows the pointer, left of it the section, right of it the exterior
  (`--x`, a registered `@property`). Hover also lists the group's four uitvoeringen (hidden 900-1199px, where they would
  cover the machine); focus opens the plate halfway. Cycloon, doseersluis and blower sections are registered onto their
  exteriors by `tools/register_sections.py` (alpha bounding box fit; blower mirrored first) as `*-doorsnede-reg`
  (+ manifest entries). Below 900px: a snap deck (78vw cards) where the swipe itself moves the scan line (centred = half
  open) and a dash-dot progress line with dots.
- Checked headless at 1440x900, 1024x768, 390x844: no page errors, keyboard focus drives inspector and scan, reduced
  motion shows everything at once with nothing travelling.

## Home blocks 4 "Projectdossier" + 5 "Van tekening tot installatie" (Nov 21)

Markup `src/home_practice.py` (`dossier_block()`, `werkwijze_block(steps)`, used by `pages.home()`; the old `case` /
`werkwijze` markup stays in `pages.py` unrendered), styles appended to `assets/css/home-blocks.css`, behaviour
`assets/js/home-practice.js`.
- **Block 4 (#projecten)** shows all five projects from `project_data.PROJECTS` (order in `ORDER`) instead of two tabs.
  The illustration fills the right of the steel band and fades into it (mask, no boxed picture); a project changes
  behind the hero's red scan line (`ds-wipe` / `ds-scan` from top.css). Copy: sector chip, project title, lead, the
  project's facts as large readings (numbers count up, Dutch formatting; "3 × 2" and words do not count), client /
  material / scope, links to the project page and all projects. Dossier index = ARIA tabs with thumbnails (arrow keys,
  Home/End); phones: picture on top, swipe it, index scrolls sideways. "Beeld: technische projectillustratie" stays.
- **Block 5 (#steps-title)**: all four steps are readable (no hidden tab panels). Desktop: a sticky sheet shows the step
  under the reading line, first as a blueprint drawing of its photo, then scrolling plots the photo over it behind the
  scan line (`--x`); title block "Blad 0n / 04 · step · Tekening → Installatie"; a dashed rail with numbered nodes
  fills red down to the reading line. Phones: each step carries its own sheet, plotted by its own scroll position.
  Drawings: `tools/drawing_versions.py` (difference of Gaussians on the photo, pale lines on a steel 24px grid) writes
  `*-tekening-{480,800,1200}` + manifest entries. Designer drawings in `tools/drawing-src/<name>.webp` (registered to the
  photo, 1672 x 941) replace the generated ones: all four are designer drawings (inbedrijfstelling added Nov 22).
- Checked headless at 1440x900, 1024x768, 390x844: no page errors; keyboard tabs; inactive dossiers `inert`; reduced
  motion shows final numbers and full photos.

## Home blocks 6 "Vraagbaak" + 7 "Vragen" (Nov 21)

Markup `src/home_knowledge.py` (`kennis_block()`, `faq_block(items)`, used by `pages.home()`), styles appended to
`assets/css/home-blocks.css`, behaviour `assets/js/home-knowledge.js`.
- **Block 6** shows all nine knowledge articles (the druk/vacuüm article + `knowledge_data.ARTICLES`) as a numbered
  editorial index: K.0n, the question, its first description sentence, topic, arrow. Topic chips (`TOPICS`, `TOPIC_OF`)
  fold rows away; on a fine pointer a preview plate glides along the side column level with the hovered row (never over
  the side text; hidden when there is no room). Phones: rows with a 64px thumbnail, chips scroll sideways.
- **Block 7** keeps `components.faq()` (and the FAQPage JSON-LD) but as an exclusive accordion (`details name`), numbered
  V.0n, red rule on the open item, smooth opening via `::details-content` + `interpolate-size` where supported. A sticky
  steel card "Staat uw vraag er niet bij?" carries the contact button, phone and e-mail (below the list on phones).
- Gotcha: a single-column grid on phones needs `minmax(0, 1fr)`; a sideways-scrolling chip row otherwise widens it.

## Contact block + footer "Titelblok" (Nov 21, every page)

`components.contact()` and `components.footer()` keep their signatures (all templates call them unchanged); styles in
`assets/css/top.css` ("CONTACT" / "FOOTER"), extras in `assets/js/contact-plus.js`.
- **Contact**: the form logic stays in `site.js` (it needs `#contact`, `.contact__lines a[href^=mailto]`, the
  `<select data-contact-topic>` and the `[data-validate]` fields). Topic chips (ARIA radiogroup) drive that select and
  fire its `change` event, so hints and `?aanvraag=` keep working; the select is visually hidden once the chips show.
  A progress line over the card (Vraag, Naam, E-mail) lights up per required field. Left: "Handig om te noemen" (from
  the FAQ answer), large call / mail lines, address. Phones: one column, chips scroll sideways, full-width submit.
- **Footer** = the drawing's title block: a framed grid of cells (brand, motto, Techniek, Airtechnic, Direct contact,
  Blad / Schaal / Rev. with the current page name from `<title>` via `_sheet_name()`, "Naar boven"). 2 columns below
  900px, 1 column below 480px.

## Component pages: overview + category template v2 "Catalogusblad" (Nov 21)

- **componenten.html** (`home_destinations.component_index`, styles `home-blocks.css` "OVERVIEW", script
  `home-blocks.js`): the eight groups as the home Röntgen plates (pointer scan; on phones the page scroll moves the scan,
  grid `data-cx-deck data-cx-vertical`), each with its uitvoeringen as a numbered list, jump chips, "8 groepen, 32
  uitvoeringen" counted from the data.
- **Category template** (`category_page.py`, all eight groups incl. Cyclonen; styles appended to
  `category-overview.css` "TEMPLATE V2", script `assets/js/category.js`): hero with kicker "Componenten · 0n / 08",
  toepassing tags and an index of the uitvoeringen (thumbnail stations on a dash-dot line, anchors to the cards);
  "Vergelijk de uitvoeringen" with toepassing chips that dim what does not fit (nothing disappears) and a
  Kaarten / Tabel switch (spec table); criteria as a numbered index; the FAQ as the home FAQ index
  (`home_knowledge.faq_block(card=False)`; `.fq` CSS now lives in `top.css`); "Verder in de installatie" = rail with
  the other seven groups. The old filter form (`category_overview.category_catalog`) is no longer used by the template.
  Breadcrumb "Componenten" now points to componenten.html.

## Product pages: template upgrade (Nov 22)

`product_page.py` (all 32 product pages) + `component_detail.component_intro(kicker=)`, styles appended to
`component-detail.css` ("PRODUCT TEMPLATE UPGRADE"): kicker "Family · g.k" (same numbering as componenten.html), the
section nav as a process line (stations on a dash-dot line, current one red; scrolls sideways on phones), a calm spec
table head, related uitvoeringen as light catalogue plates (sideways deck on phones), the FAQ as the shared `.fq` index,
breadcrumb "Componenten" and the related link point to componenten.html / the category. Checked: 32 of 32 pages
render kicker, FAQ index and plates without page errors; no horizontal overflow at 390px.

## Fine-tuning (Nov 22)

- Category index: the dash-dot line runs through the thumbnail centres and starts at the first one; number 8px above,
  name 7px below it; long names end in "…" with the full name as tooltip.
- Signature start (`signature.js`, all templates without the home hero): skips zero-height siblings (closed lightbox),
  counts a page subnav as part of the opening and puts the datum 36px below it, clear of borders and bars.
- Names in card rows (`[data-eq]` + `assets/js/equalize.js`, loaded on every page): balanced line breaks, at most two
  lines, and the cards in one row share the tallest name height, so rows always end level. Rail arrows have their own
  column. Measured: rail cards one height (177px), no name/arrow overlap, home catalogue metas one height at 1024px.

## Product section nav "reading line" (Nov 22)

`assets/js/subnav.js` (product pages): the sticky nav gets `.is-stuck` (frosted, shadow) once it sticks; one pill glides
to the current station (site.js scrollspy); the line is drawn as segments only in the gaps between stations (never under a label), each filling red as you read on, with a granule at the head; read stations get a filled dot.
Styles: component-detail.css "STICKY NAV". Category index got more space below it.

## Mobile text (Nov 22)

top.css "MOBILE TEXT": form fields 16px (no iOS zoom), contact topic chips wrap instead of scrolling behind the card
edge, headings hyphenate long Dutch compounds, sideways rows get a right-edge fade plus end padding so the last item
scrolls clear. Audit: `tools/mobile_text_audit.js` (10 templates at 360 / 390px: clipped text, off-screen text, rows cut
without a fade, form text under 16px, tiny text). Before: 8 / 0 / 34 / 70 / 4. After: all 0.

## Header current state (Nov 22)

top.css "HEADER CURRENT STATE": the ruler marker is a 2px steel dimension line with end ticks (gold dot removed); the
current item's label is set heavier; while hovering another item the marker previews there in a lighter steel. The
product reading line has no granule head any more (red segments only).

## Contact: the way there + low-threshold form (Nov 22)

- `contact-plus.js` catches every link to `#contact` in the capture phase (before site.js): far away, a steel sheet
  slides up, the page jumps behind it in one step, the sheet lifts off and focus lands on the topic chips; close by, a
  short smooth scroll; reduced motion, an instant jump. Links to another page's #contact (header CTA) stay on the
  current page when it has its own contact block. `?aanvraag=topic` still preselects the topic.
- Topics (`components.contact`): at most two page-specific topics, then four intent shortcuts on every page
  (`installatieontwerp`, `bestaande-installatie`, `onderdelen`, `terugbellen`; new keys in
  `contact_delivery.CONTACT_TOPICS`, so the API accepts them), "Algemene vraag" last. "Liever teruggebeld" marks the
  phone field. Message helpers (+ Product, + Capaciteit, + Afstand, + Huidige situatie) start a line to complete.
  "Vrijblijvend" next to the privacy link (confirm with the client).
- Measured: hero CTA, product advice and header CTA each move the page in 1 scroll step (was 5 to 14), sheet shown,
  focus in the form, topic correct; no page errors.

## Hero dosing sheet: real-time 3D rotor (Nov 22)

`assets/js/rotor3d.js` (bundle of `tools/rotor3d/rotor3d.src.js`, adapted from the supplied 3D package, Three.js 0.180.0
MIT): housing photo without rotor + WebGL rotor (8 vanes with depth, hub, screws; only its local axis turns) + the
photo's front rim as SVG, in the same 3:2 stage box. 3D granules fill each pocket under the inlet and empty over the
outlet. Laag / Hoog = 4 / 12 rpm, eased; builds lazily when the sheet is first shown; runs only while shown, on screen,
not paused, no reduced motion. Without WebGL the previous SVG rotor stays. ~500 KB (~130 KB gzip). Rebuild:
tools/rotor3d/README.txt.

## Hero slides (Nov 20, on top of Tekenblad)

The home hero shows five sheets of one process line, all 1536x1024 in the same framing (equipment right, empty wall
left): 01 pneumatisch transport (`01-hero-pijpleiding-leeg` + granule canvas + streamlines), 02 filtratie
(`30-hero-filter`), 03 wissels (`31-hero-wissel`), 04 cyclonen (`32-hero-cycloon`), 05 doseren (`33-hero-doseersluis`).
Data in `HERO_SLIDES` (`src/pages.py`): image, discipline (plate title block), tab label, statement, lead, deep link and
hotspots (x %, y % of the photo). Source PNGs of the new photos: `tools/hero-src/`.
- **Shared stage.** All slides sit in the one `.hero__stage` cover box, so the Tekenblad fold (clip-path on
  `.hero__visual`) works for every slide unchanged. Slides 2-5 are close-ups: `.hero__frame` scales them to 0.84
  (anchored right) over `.hero__ambient`, a blurred copy of the same photo, so the equipment clears the type column
  without a seam. Phones/portrait: scale 1.
- **Transition.** The incoming photo wipes in from the equipment side (clip-path, 1.4 s) behind `.hero__scan`, an orange
  scan line with a short drawing grid trailing it; the statement leaves upward and the next one rises line by line in
  the split-heading masks; lead + deep link fade. The plate title block follows (Discipline, Blad 0n / 05).
- **Clock.** The active tab's hairline (`.hero-tab__fill`, `--slide-dur` 8 s) is the timer; its `animationend` advances.
  It pauses with the pause button, hover over the copy/tabs/hotspots, keyboard focus (`:focus-visible`) and off-screen.
  Arrow keys move between tabs. Reduced motion: no autoplay, instant swaps. The granule sim only runs while slide 1 shows.
- **SEO.** H1 = the static line "Industriële luchttechniek & solids processing"; the five statements are `<p>` and all
  copy stays in the DOM (inactive slides `inert` + `aria-hidden`). Title/description of the home page now lead with
  pneumatisch transport, filtratie, cyclonen, wissels and doseersluizen. Deep links still point to `#specialisaties`
  where no page exists yet [TBD].
- Checked headless (playwright-core, Chromium) at 1440x900, 1024x768, 390x844: no console errors, autoplay advances,
  keyboard hold works. The hidden Browser pane freezes CSS animations, so judge motion headless or with the pane shown.

## Block 2 "Processchema" (Nov 20, block variant A rolled out)

`#specialisaties` (`.process`, `[data-process]`): a process line leaves the hero plate's bottom-left corner (x = the
hero track's `--ix`, y = `--ib` above the section), drops past the heading and splits at a rounded T into the two
disciplines. The orange stroke is drawn by scroll (tip at ~62% of the viewport) with a granule on its tip; a node lights
up when its branch arrives. Base line is dash-dot (a drawn centre line). Each discipline has a plate figure
(`components.plate_figure`, images from `SOL_IMG`, transparent ones in `CUTOUT` get a light ground) that swaps per
hovered/focused item. Items and nodes use `components.sym()`: process-flow symbols after ISO 10628, the site's icon set
for disciplines. Phones (< 960px): no line, same content. Reduced motion: line fully drawn, no granule. The "Wat wij doen"
eyebrow is gone (Impeccable bans kickers above headings). Review pages `block-{a,b,c}.html` came from the earlier block;
`tools/block_concepts.py` no longer applies to the current build.

## Block 3 "Catalogusbladen" (Nov 20, block 3 variant B rolled out; replaces the carousel)

`.catalog` / `[data-catalog]`: all eight component groups at once as framed plates (`components.catalog_sheet`), no
paging. Registration marks open out from the centre as each sheet arrives (site.js adds `.is-in`, staggered by `--i`).
Hover/focus: dimension lines (deliberately without numbers) and, for groups with a cross-section render
(`COMP_SECTION`: blower, cyclone, rotary valve; tag "A–A"), a dash-dot cutting line sweeps across and reveals the
inside. The blower *section* is mirrored so it registers with the untouched product photo. Touch screens (`hover: none`)
hide the tag and cut, since they can't reach them. Labels use `COMP_SYM` (process-flow symbols, three added: pipe, bag,
valve). The "Componenten" eyebrow is gone. The carousel CSS block was removed; `site.js` still has the carousel module
(it no-ops without `[data-carousel]`). Review pages `comp-{a,b,c}.html` came from the old carousel.

## Themes (Nov 20, from the design system)

`tokens.css` now has the same two-layer colour model as the Airtechnic Solutions design system: the fixed palette
(`--cream` … `--granulate`) plus semantic tokens (`--surface`, `--text`, `--text-muted`, `--heading`, `--eyebrow-ink`,
`--accent-line`, `--accent-word`, `--link`, `--link-hover`, `--border`, `--border-strong`, `--tbd-fill`).
`data-theme="forest"` on a section turns it into a green band (contact, case, advies, statement, cta-card carry it);
`data-theme="light"` resets a light card inside one (the contact form card). This replaces the old per-class
overrides (`.on-dark`, `.band--green …`, `.contact .link`, `.statement h2 em` …). Base styles for body, headings,
accent word, eyebrow, links, `.muted` and `.tbd` read the semantic tokens; use them for anything that sits on the
ground, palette tokens only inside cards that keep their own surface.

## Decisions worth knowing

- **Cross-section mirrored.** `13-cycloon-doorsnede` has its inlet on the left; on the product page it is mirrored with CSS so the inlet sits on the right, matching the mockup and the callout positions.
- **Cut-outs trimmed.** Transparent PNGs were trimmed to their visible area (plus 2% margin) so they fill tiles; nothing is cropped by CSS.
- **Case tabs.** Only Food and Recycling are shown; Feed, Chemie and Hout stay hidden until a case exists. The Food case has an image but no copy, so its title and subline are `[TBD]`.
- **Category filters.** Toepassing and Uitvoering values are derived only from the card copy (e.g. "Pneumatisch transport", "Maatwerk"). Confirm the real taxonomy.
- **FAQPage JSON-LD** is emitted only for answered questions, so the category and product pages have none until their answers are written.
- **Article layout.** The sticky sidebar runs alongside sections 1–5; the comparison table then breaks out to full container width (as in the mockup), and "Samengevat" follows in the article column.
- **Form.** The page sets a default topic. Contact links can override it with `?aanvraag=<topic>#contact` from that page’s list of topics. The form posts JSON to `api/contact`. The server validates the selected topic and sends to `info@airtechnicsolutions.com`, with the visitor as Reply-To. A confirmation appears after the mail server accepts the message.

## Homepage fidelity pass (mockup match)

- The homepage mockup represents a **~1207px viewport** (measured from nav text width), not 1440. Compare at that width.
- Judge used: section start positions as a fraction of page height vs. the mockup. Result: all 8 boundaries within ±1.4 points; total height +4.8%.
- Headings use **Archivo with its width axis** (`archivo-latin-wdth-normal.woff2`, `--head-stretch: 90%`) to get the mockup's semi-condensed heavy look.
- Home spacing uses `--home-y` (36px desktop) instead of `--section-y`; other templates keep their own rhythm.
- impeccable `comp-diff` (engine 0.1.25): full page 0.69, first viewport 0.64 (hero gate is 0.72). Control test: the same build with only the mockup's hero photo pasted in scores 0.73, so layout and type pass; the gap is the photography (library images vs. the mockup's own renders).
- impeccable `detect`: eyebrow, cream ground and Inter are flagged as category defaults but are pinned by the brief, so they stay; the "flush children" warnings are full-bleed bands whose `.container` carries the inset.
- Remaining intentional differences: photos come from the image library (the mockup has its own renders); case tabs show only Food and Recycling (brief: hide tabs without a case); inputs and buttons stay 44px tall (brief's touch-target rule) where the mockup draws them slightly smaller.

## Open items (`[TBD]` in the pages)

- Production domain for canonical / OG URLs (`SITE` in `src/components.py`, now `https://www.airtechnicsolutions.nl`).
- Werkwijze copy for Analyse, Realisatie, Inbedrijfstelling.
- FAQ answers (home items 2–4, all category and product questions).
- Food case title/subline; per-industry descriptions under Toepassingen.
- Spec table label "Procestemperatuur" is marked `[verify label]`.
- Real URLs for Projecten, Over ons, Kennis, other components, Privacyverklaring, LinkedIn (now `#`).

## Site signature concepts (Nov 20, review pages; live pages untouched)

`python tools/signature_concepts.py` turns the built home, category, product and kennis pages into `sig-{a,b}[-categorie|-product|-kennis].html`
(sets `html[data-sig]`, adds `assets/css/signature.css` + `assets/js/signature.js`, a review switcher at the bottom).
One measured SVG line runs down the left margin of every page (>= 1100px) from the hero's tab rule (home) or under the page hero,
with a station at every section head (`main section` not nested + article h2s; labels via `data-sig-label`), drawn by scroll
to ~62% of the viewport, inverted inside `data-theme="forest"` bands; `[data-sig-node]` (block 2 discipline nodes) light up as the
tip passes. A "Hartlijn": dash-dot axis, 90-degree turn off the tab rule, datum cross + dotted leader + vertical label fitted to the
gap. B "Stroomlijn": curve off the tab rule, swings in to touch each head, granule + fading tail. Both also make the hero/block 2 seam
one sheet (tab bar glass fades with `--qe`, hero grid bottom-anchored and continued into block 2) and hide the orange `.pr-line`.
Preview: launch config "flow-d-sig" port 5191.

**Rolled out (Nov 20): variant A "Hartlijn" is live on every page.** `components.page()` sets `html[data-sig="a"]`, loads
signature.css/js and adds `data-sig-label` from `SIG_LABELS`; block 2 no longer renders `.pr-line` and its nodes carry
`data-sig-node`. The `sig-*` review pages stay for comparison (regenerate with tools/signature_concepts.py after a build).

**Start "Nulpunt" (Nov 20):** `html[data-sig-start="origin"]` (set in `components.page()`): on the home the line no longer hooks off
the tab rule; it starts one grid step below the hero at a datum mark (ring with two filled quarters). The other start concepts
(Instroom, Bron) stay in signature.js and as `sig-start-{b,c}.html` via tools/sig_start_concepts.py.

## Contact delivery

Run `python src/serve.py D:/websites/flow 5186` with Airtechnic's SMTP settings in the server process environment. Restart the process after changing them:

- `AIRTECHNIC_SMTP_HOST`, `AIRTECHNIC_SMTP_USERNAME`, `AIRTECHNIC_SMTP_PASSWORD`
- `AIRTECHNIC_SMTP_FROM` if the authorised sender differs from the username
- `AIRTECHNIC_SMTP_SECURITY` (`smtps` by default, or `starttls`) and `AIRTECHNIC_SMTP_PORT` if needed

Keep credentials out of the website files. For deployment, serve the form and its endpoint on the same HTTPS origin. Route only `POST /api/contact` to the loopback server behind the HTTPS reverse proxy and preserve the public Host header. Configure per-visitor throttling at that proxy. The local server caps total volume and uses the immediate remote address as its per-client key. Do not expose its port publicly.

Verify one labelled test in the target mailbox before launch. SMTP acceptance confirms the upstream server accepted the request for delivery.

## Productdetailpagina's

Alle 32 uitvoeringen gebruiken `src/product_page.py`, met de goedgekeurde cycloonpagina als vaste structuur: introductie en vier beelden, sectienavigatie, werking met vier stappen, zes selectiecriteria, drie toepassingen, gerelateerde producten, zes vragen en contact. `src/product_routes.py` koppelt de categoriekaarten aan eigen detailpagina's. `src/product_knowledge.py` bevat de productspecifieke principes en selectie-inhoud; `src/product_data.py` combineert die met beeldkeuzes en contactonderwerpen. De oorspronkelijke cyclooninhoud staat in `src/cyclone_product_data.py`.

De nieuwe galerijen bevatten een totaalbeeld, twee expliciet benoemde detailuitsneden en een principedoorsnede. 24 nieuwe transparante doorsneden staan met generatieherkomst in `images/generated-product-assets.json`; acht bestaande doorsneden worden hergebruikt. Contextfoto's zijn als voorbeeldopstelling van de productfamilie aangeduid. Illustraties zijn geen maatvoering of definitieve constructietekeningen.

Na wijzigingen: `python src/build.py`, `python tools/check_products.py` en `python tools/check_categories.py`. De productcontrole bewaakt gelijke structuur, lokale afbeeldingen, links en ankers, metadata, contactonderwerpen en alle categorie-productroutes. Browsercontrole omvat beeldladen, galerij en toetsenbordbediening, werkingsstappen, contactselectie en categoriefilters op schermbreedtes 320, 375, 768, 1024 en 1440 pixels.

Aanvullende inhoudelijke referenties: [Coperion over doorval- en doorblaassluizen](https://www.coperion.com/en/know-how/ask-the-expert/difference-discharge-valve-and-blow-through-valve), [Busch blowerprincipes](https://www.buschvacuum.com/uk/en/products/blowers/blowers-overview/) en [CAGI blower guide](https://www.cagi.org/blower-guide). De tekst beschrijft selectieprincipes; concrete prestaties worden pas bij technische selectie vastgesteld.

Algemene terminologie voor uitvoeringsprincipes is gecontroleerd aan de hand van [Coperion rotary valves](https://www.coperion.com/en/products-services/process-equipment/rotary-valves) en [Palamatic bulk handling equipment](https://www.palamaticprocess.com/en-us/bulk-handling-equipment). Dit onderbouwt de principebeschrijvingen, niet leveranciersspecifieke prestaties of leverbaarheid. Er zijn geen capaciteits-, efficiëntie- of certificeringsclaims toegevoegd.

## Oplossingen

Alle zeven menu-items onder Oplossingen hebben een eigen `oplossingen-*.html` pagina. `src/solution_data.py` beheert de specifieke inhoud; `src/solution_page.py` en `assets/css/solutions.css` leggen één structuur vast: hero, proceskern, sectienavigatie, procesvraag, vier werkingsstappen, drie toepassingssituaties, vier ontwerpcriteria, drie componenten, drie vragen en contact. Menu en specialisaties op de homepage verwijzen naar deze pagina's. Iedere oplossing heeft een eigen contactonderwerp.

Stofafzuiging en hoogvacuüm gebruiken nieuwe illustratieve toepassingsbeelden. De overige oplossingen hergebruiken passende bestaande beelden; herkomst staat in `images/generated-solution-assets.json`. Procesbeelden zijn illustratief, geen gedocumenteerde klantprojecten of uitvoeringsschema's. Terminologie is getoetst aan [Palamatic bulk handling](https://www.palamaticprocess.com/bulk-handling-equipment), [Palamatic doseren](https://www.palamaticprocess.com/en-us/bulk-handling-equipment/dose) en [Nederman industriële hoogvacuümafzuiging](https://www.nederman.com/en-US/products/stationary-high-vacuum-extraction-systems).

Controle: `python src/build.py` en `python tools/check_solutions.py`. Browsercontrole omvat 320, 375, 768, 1024 en 1440 pixels, beeldladen, sectielinks en focus, uitklappers, contactselectie, desktop- en mobiele menuroutes, en direct mobiel openen met en zonder JavaScript. Herstart de lokale contactserver na wijzigingen in contactonderwerpen, met behoud van de bestaande configuratie.

## Kennisartikelen

De drie aangekondigde kennisartikelen zijn beschikbaar via de homepage. Naast `kennis-druk-of-vacuumtransport.html` zijn dit `kennis-wanneer-filters-vervangen.html` en `kennis-juiste-blower-selecteren.html`. De nieuwe inhoud staat in `src/knowledge_data.py`; `src/knowledge_page.py` gebruikt de bestaande componenten uit `src/knowledge_article.py` en dezelfde stylesheet als het referentieartikel.

De vaste opbouw omvat hero, kort antwoord, inhoudsnavigatie, zes inhoudssecties, twee processchema's, vergelijking, drie praktijksituaties, advieschecklist, technische bronnen, twee relevante componentlinks en contact. Bestaande filter- en ventilatorbeelden worden hergebruikt met specifieke alternatieve teksten, bijschriften en deelafbeeldingen. Er zijn geen onbewezen universele vervangingstermijnen of prestatiegrenzen toegevoegd. Bronverwijzingen van Donaldson, CAGI en Busch staan per artikel onder Technische bronnen.

Controleer na wijzigingen met `python src/build.py` en `python tools/check_knowledge.py`. Browsercontrole: 320, 375, 768, 1024 en 1440 pixels; beelden, inhoudslinks en focus, praktijksituaties, deelknop, contactonderwerp en rechtstreeks mobiel openen met en zonder JavaScript.

## Mobile layer + page transitions (Nov 20)

New files, loaded last on every page by `components.page()`: `assets/css/mobile.css`, `assets/js/mobile.js` (defer) and
`assets/js/page-transitions.js` (no defer, in `<head>`, plus `<link rel="expect" href="#main" blocking="render">`).
Shared files were only touched surgically: `components._header_sheet()` (new menu markup, same `id="hx-sheet"` /
`data-hx-sheet` hooks), the old burger block in `site.js` removed (now in `mobile.js`), and the hero clock's hold logic in
`site.js` ignores sticky `:hover` on touch (a tap used to stop the slides for good).
- **Menu "Tekenblad"** (< 1040px): full-screen steel sheet drawn down behind a red scan line (registered `--mnav-r`
  drives clip + line), numbered index rising row by row, Oplossingen / Componenten drill in sideways (photo rows /
  product plates), contact (CTA, Bel ons, Mail ons) in thumb reach. `role="dialog"`, rest of the page `inert`, focus to
  the first item, Escape = back, then close; closes on bfcache restore and above 1040px.
- **Page transitions "Nieuw blad"** (cross-document View Transitions, all viewports, off under reduced motion): forward =
  the next page slides up like a fresh sheet (red top edge) while the old one sinks into steel; back = the reverse; from
  the open menu the menu lifts off (type `from-menu`, passed via sessionStorage because the animation runs in the new
  document); a tapped card's picture morphs into the next page's hero plate (`vt-media`; hero selectors in
  `HERO_MEDIA`). Header is its own layer (`view-transition-name: site-header`). Unsupported browsers just navigate.
- **Home hero cover** (portrait / < 720px): full-screen photo under the transparent header, statement on a steel fade,
  one-row sheet index under the thumb, swipe between sheets (`mobile.js` clicks the hero's own tabs), photo folds into
  a plate on scroll (`--p`). Two sets of rules in `mobile.css`: `.hero` (Tekenblad slides, still used by
  `hero-{variant}.html`) and `.hc--cinema` (the live home carousel from `hero_concepts.py`; also portrait tablets up to
  1100px). For `.hc`: object-position per sheet (transport + wissels 90%, others 70%), hotspots only in the upper half,
  labels open towards the middle on portrait. Three small edits in the carousel's own files: `sizes` of its pictures is
  `(max-aspect-ratio: 6/5) 150vh, 100vw` (phones loaded the 480w file and upscaled it), and `hero-concepts.js` reads the
  computed object-position percentage instead of only recognising "70" (desktop positions unchanged, checked).
- **Home hero "Doorstroom" cover** (`.ds`, live since Nov 20 23:05, `mobile.css` section 3c): same cover on portrait
  screens (< 720px, portrait up to 1100px) with the hero's own animations kept: live granule canvas, SVG streamlines,
  grain flows of sheets 2-5, grains on the Proceslijn and the play ring. The Proceslijn is the dark index under the
  thumb; the flow-regime switch (Dichte / Verdunde fase) floats as a glass pill top right on sheet 1 (title + notes
  hidden there); hotspots only in the upper 42%; per-sheet framing `--px` (transport + wissels .9, others .7); fold on
  scroll via the hero's own `--sp`; swipe also on the copy (`mobile.js`, skips the stage where `doorstroom.js`
  already swipes). The hero's own stacked phone layout in `top.css` still applies to landscape tablets 720-899px.
- **Sub-page heroes** (< 960px): plates are "plotted" in (scan line + clip), copy rises, taller plates on phones,
  scroll-driven zoom/drift on hero and card photos (CSS `animation-timeline: view()`).
- **Animations on phones too** (Nov 20, measured with `document.getAnimations()` desktop vs 390px on 10 page types: the
  site signature was the only desktop-only animation on every page). `signature.js` now draws at every width
  (`wide = matchMedia('all')`); below 1100px `mobile.css` 5b drops the vertical labels and leaders (no room in the 22px
  margin), axis + drawn progress + datum crosses + station dots stay. Catalogusbladen on touch: the red cutting line
  shows when "Doorsnede" is tapped, and each sheet with a section plays the cut once by itself at mid-screen
  (`.is-demo`, `mobile.js` 2b). Werkwijze: the open step's intro (step-in / clip-in / settle) now replays when the block
  scrolls into view instead of running unseen at page load (`mobile.js` 2c, all widths).
- **Details**: one-line scrolling breadcrumbs (scrolled to the current page), 44px hit areas for text links and
  crumbs, press feedback on cards/plates/tiles/FAQ, button light sweep on tap, contact dock (call + "Stel uw vraag")
  from the second screen on, hidden near the contact form, footer, menu and while typing. `@keyframes rise` (used by
  the hero intro but never defined) and a `.sr-only` alias now exist in `mobile.css`.
- Verified headless (Chromium, 390x844 / 768x1024 / 1440x900): no console errors, no horizontal overflow, menu focus
  + inert + Escape, VT types (`forward`, `back`, `from-menu`, `morph`), desktop unchanged.

## Productfolder (POC, Nov 22)

A 4-page A4 PDF per product, from the same data as the product page (`PRODUCTS`) and the same tokens.
POC covers `cycloonafscheider` only (`FOLDER_SLUGS` in `src/folder_page.py`); the template works for any slug.

- `src/folder_page.py`: print HTML (cover · werking with numbered cutaway · toepassing + selectie ·
  praktijkcase + gerelateerd + contact), drawing title block on every sheet. `BRANDS` holds the brand
  (name, logo, `--brand-*` tokens); a second brand or dealer co-brand is one more entry.
  `folder_html(slug, recipient={...})` prints "Opgesteld voor" on the cover (hook for personalised folders).
  `PRACTICE` maps a product to a verified case in `project_data.py`.
- `assets/css/folder-print.css`: print layout (mm units, `@page A4`).
- `tools/render_folders.py`: writes `folders/<slug>.print.html`, renders `folders/<slug>.pdf` with headless
  Chromium (Python Playwright; uses the newest installed `ms-playwright/chromium-*`, or `FOLDER_CHROMIUM`),
  then checks it: 4 A4 pages, every font embedded, real text, no broken images, < 2 MB. Exits 1 on a failure.
- Product page: "Download productfolder (PDF · n KB)" appears in the Technische documentatie card only when
  the PDF exists. `tools/build-vercel.mjs` publishes `folders/*.pdf` only.

Run after content changes: `python tools/render_folders.py`, then `python src/build.py` (or the product page).

Gotchas: Chromium writes variable fonts as Type3 glyphs, so the folder uses static Archivo instances cut by
fontTools into `folders/fonts/` (built on demand). CSS `filter` on an image makes Chromium rasterise it at
screen size: no drop-shadow in print. Transparent images become lossless PNG in the PDF, so cut-outs get
print-sized copies in `folders/img/` (256-colour palette on gradients, JPEG on a flat matte). No font has `≈`;
the folder prints "ca.". Links in the PDF use `SITE` (set `SITE_URL` to the production domain before rendering).
Result 2026-11-22: 951 KB, 7 embedded fonts, render 2.4 s.

## Beurs Kiosk Modus + Beheer (Nov 22)

Opleverfunctie voor de eigenaar: via **Beheer** (`/beheer.html`, discrete link "Beheer" in de footer) logt de
eigenaar in en start een doorlopende presentatie op één of twee beursschermen, in de stijl van de site.

| Bestand | Rol |
|---|---|
| `src/kiosk_page.py` | genereert `beheer.html`, `kiosk.html` (alle bladen als `<template>` met faces a/b/s) en `kiosk-sw.js`; draait mee aan het eind van `src/build.py` |
| `assets/js/kiosk.js` | speler: klok-synchronisatie, scanlijn-overgang over beide schermen, granulaatstroom over het panorama, count-ups, wake lock, stoppen (Esc / 3 s linksboven), nachtelijke herstart 04:00 |
| `assets/js/beheer.js` | login, welkomst bij eerste login (overdrachtsmoment), instellingen, live voorbeeld, start op 1 of 2 schermen (Window Management API) |
| `assets/css/kiosk.css` | kiosk + beheer; maten in `--u` (1 % schermhoogte) zodat 1080p, 4K en grote beursschermen gelijk ogen |
| `src/beheer_auth.py`, `api/beheer.py` | login (PBKDF2-hash, ondertekende HttpOnly-sessiecookie, rem op mislukte pogingen); lokaal via `src/serve.py` |
| `tools/kiosk_images.py` | zet de aangeleverde kioskrenders om naar `images/kiosk/` (AVIF/WebP, 1920/3840, panorama 3840/7680) |
| `tools/beheer_password.py` | maakt de wachtwoord-hash en het sessiegeheim voor Vercel |

**Synchronisatie zonder netwerk.** Elk scherm rekent het huidige blad uit `Date.now()` en een vaste start (t0 = 0):
twee vensters op één pc, of twee apparaten met een gelijke klok, tonen hetzelfde blad. Binnen een blad verschuift
`--late` (seconden dat een scherm later aansloot) alle CSS-animaties, dus ook een later geopend scherm loopt in de pas.
Rol a = linkerscherm, b = rechterscherm, s = één scherm. De scanlijn kruist eerst A, dan B; de voortgangslijn in het
titelblok loopt ook door over beide schermen. Het panorama (`01-proceslijn-panorama`) is één beeld over twee schermen;
de granulaten bewegen alleen in de glazen bochten (contouren gemeten in `GLASS` in kiosk.js), door het staal loopt een glans.

**Inhoud uit de site.** Componentgroepen komen uit `category_data.CATEGORIES` / `cyclone_category_data.CYCLONES`
(naam, kop, intro, principe, uitvoeringen; Röntgen-paar exterieur + geregistreerde doorsnede), projecten uit
`project_data.PROJECTS` (twee per ronde, wisselend), materialen uit de projecten. Alleen de werkwijze-stappen staan
dubbel (`STEPS` in kiosk_page.py; in `pages.home()` zijn ze lokaal). Nieuwe groep: voeg een regel toe aan `GROUPS`.

**Offline.** `kiosk-sw.js` pre-cachet alle kioskbestanden; versie-hash wisselt bij elke build. Pagina's network-first,
assets cache-first. Een recente login op het apparaat geldt offline (`at-kiosk-pass` in localStorage).

**Twee schermen.** In Beheer "Schermen zoeken" (Chrome/Edge, toestemming Vensterbeheer) → Start: scherm A gaat
fullscreen op het gekozen scherm en scherm B opent als venster op het tweede scherm (één klik daar = fullscreen).
Zonder die API: B opent als venster dat u zelf versleept. Een tweede apparaat: link onder "Scherm B op een tweede apparaat".
Stoppen op één scherm stopt alle vensters op dezelfde pc (BroadcastChannel).

**Lokaal testen.** Preview-config `flow-d-kiosk` (poort 5194). `src/serve.py` leest de testlogin uit `.env.beheer`
(gitignored, testwachtwoord staat in dat bestand).

**NL / EN / DE.** Beheer is beschikbaar op `beheer.html`, `beheer-en.html` en `beheer-de.html`; de taalwissel
bovenaan verandert de bedieningstaal. De instelling bij "Tempo en taal" bepaalt onafhankelijk daarvan de taal
van beide presentatieschermen, het live voorbeeld en de link voor scherm B. Instellingen blijven op dit apparaat
bewaard. De generator gebruikt de bestaande sitecatalogi plus `src/kiosk_strings.json` voor kiosk- en beheerteksten.
De speler gebruikt de gekozen taal voor getallen en `/h` voor uur-eenheden in EN/DE.

**Beelden en bediening.** De volgende slide wordt acht seconden vooraf opgebouwd en gedecodeerd; de speler
houdt het vorige blad vast tot het nieuwe beeld klaar is. WebP is ook offline beschikbaar als AVIF niet werkt.
Het live voorbeeld is te pauzeren en gebruikt minder frames om de beheerpagina soepel te houden. Stoppen ruimt
luisteraars en de scherm-wake-lock op; Esc na het verlaten van fullscreen opent ook de stopdialoog. De dialoog
houdt toetsenbordfocus vast. Reduced motion schakelt de panorama-beweging en scanovergang uit.

**Offline voorbereiden.** Open Beheer eerst online en wacht op "Gereed voor offline gebruik". De service worker
haalt maximaal vier bestanden tegelijk op en controleert de volledige inventaris (115 bronbestanden, plus de
gebundelde stylesheet in de publicatiebouw), inclusief de drie talen en beide beeldformaten. Met een geldige recente login kunnen Beheer en de kiosk vervolgens offline worden herladen.
Twee apparaten hebben elk deze voorbereiding en een gelijke systeemklok nodig. BroadcastChannel stopt alleen
vensters op hetzelfde apparaat; op een tweede apparaat stopt u de kiosk apart.

**Controle.** `python src/kiosk_page.py` genereert de kiosk en Beheer. Daarna controleert
`python tools/check_kiosk.py` de volledigheid van vertalingen, 18 bladen × 3 schermrollen per taal, lokale links,
beelden en de offline-inventaris. `npm run build` maakt de publicatiemap; `python tools/check_kiosk.py --dist`
controleert ook de werkelijk gepubliceerde bestanden en hun offline-cache. Browsercontrole omvat inloggen,
taal bewaren, preview/pauze, starten/stoppen, twee vensters en offline herladen. Automatische plaatsing op
fysieke monitoren blijft afhankelijk van browsertoestemming en moet op de beurs-pc worden gecontroleerd.

## Meertaligheid (nl / en / de, Nov 22)

De site wordt in drie talen gebouwd: Nederlands op de root, Engels in `en/`, Duits in `de/`. De Nederlandse
data in `src/` blijft de enige inhoudsbron; `python src/build.py` schrijft alle talen (`python src/build.py nl`
alleen Nederlands), `npm run build` publiceert `en/` en `de/` mee in `dist/` (eigen stylesheetbundels via `../`).

- **`src/i18n.py`** — het mechanisme. Taalcontext (`i18n.use('de')`), `t(key)` voor sleutelteksten,
  `tr('Nederlandse tekst')` voor inhoud, `localize_html()` (vertaalt een gerenderd NL-fragment segment voor
  segment: tekst met inline opmaak als `<em>`, `<a>`, `<strong>`, plus `alt`, `aria-label`, `title`, `data-cap`,
  `data-hint` e.d.), `localize_jsonld()`, `rewrite_urls()` (assets één map hoger, paginalinks naar de vertaalde
  bestandsnaam), `localize_units()` (`m³/u` → `m³/h`, Engelse decimalen) en `alternates()` (hreflang).
  `components.page()` roept dit aan wanneer de taal niet `nl` is; `build.py` doet met `finalize()` een laatste,
  idempotente URL- en eenhedenronde (voor scripts die templates na `page()` toevoegen).
- **`src/i18n_strings.py`** — gesleutelde UI-teksten per taal: header, Tekenblad-menu, footer-titelblok,
  contactblok en formulier, knoppen, aria-labels, `SIG_LABELS` (`sig.*`) en de JS-teksten (`js.*`).
- **`src/locales/en.json`, `de.json`** — inhoudscatalogi, sleutel = Nederlands segment (gettext-stijl).
  Ontbrekende vertalingen vallen terug op NL en komen in `src/locales/missing-<taal>.json` (alleen als er iets ontbreekt).
- **`src/i18n_slugs.py`** — vertaalde bestandsnamen (bv. `cycloonafscheider.html` → `en/cyclone-separator.html`,
  `de/zyklonabscheider.html`). Alleen pagina's in deze lijst worden vertaald; review-/conceptpagina's blijven NL.
  `toepassing-pet-recycling.html` is een NL-alias van de projectpagina en heeft daarom geen eigen vertaling.
- **JS**: `components.page()` zet `window.ATI18N` (uit `i18n.js_strings()`); `site.js`, `contact-plus.js`,
  `category.js`, `knowledge-index.js`, `mobile.js`, `signature.js`, `doorstroom.js` en `home-practice.js`
  lezen hun teksten en `locale` daaruit, met de Nederlandse tekst als fallback.
- **Taalwisselaar**: `components.lang_switch()` — NL/EN/DE in de header-rail en onderaan het Tekenblad-menu,
  naar de equivalente pagina. Stijl in `assets/css/lang.css`.
- **SEO**: `<html lang>`, canonical per taal, wederkerige `hreflang` (nl/en/de + x-default = nl), `og:locale`
  + `og:locale:alternate`, vertaalde `<title>`, description, OG en JSON-LD (incl. kruimelpad-URL's).
- **Stijl**: EN neutraal-zakelijk (Brits), DE met "Sie"; vakterminologie o.a. Zellenradschleuse, Durchfall-/
  Durchblasschleuse, Zyklonabscheider, Tauchrohr, Saug-/Druckförderung, Dichtstrom/Flugförderung, Abreinigung.
  `[TBD]`-markers blijven staan. Productfolders (PDF) zijn alleen Nederlands; de downloadlink zegt dat.
  Het contactformulier stuurt dezelfde onderwerpsleutels naar `api/contact`; de mail naar Airtechnic blijft NL.

**Kiosk / andere renderers** gebruiken dezelfde tabellen: `with i18n.use('en'): i18n.t('nav.solutions')`,
`i18n.tr(nl_tekst)`, `i18n.localize_html(fragment)`, `i18n.js_strings('de')`.

**Tekst gewijzigd?** Bouw opnieuw; nieuwe of gewijzigde NL-segmenten verschijnen in `missing-*.json`.
`python tools/i18n_sync.py export <map>` maakt genummerde batches, vertaal naar `{id: [en, de]}` en
`python tools/i18n_sync.py import <bestand>` voegt ze toe (controleert inline opmaak, `[TBD]` en placeholders).
`python tools/i18n_sync.py check` valideert de catalogi.

**Controle**: `python tools/check_i18n.py` (NL-restanten in tekst/attributen/meta/JSON-LD van alle EN/DE-pagina's,
wederkerige hreflang, canonical, lang/og:locale, taalwisselaar, kapotte relatieve links) en
`python tools/check_i18n_browser.py [--out map]` (Python Playwright + lokale Playwright-Chromium: home, categorie,
product en kennisartikel per taal op 1440×900 en 390×844, geen console- of paginafouten, wisselaar naar elke taal).
Resultaat Nov 22: 3.094 segmenten per taal vertaald, 0 ontbrekend; check_i18n 198 pagina's 0 problemen;
browsercheck 12 pagina's × 2 viewports 0 problemen.
