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
