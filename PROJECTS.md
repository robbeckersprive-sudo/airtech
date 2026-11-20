# Projecten

The project collection is `projecten.html`. All five detail pages use
`src/project_page.py` and `assets/css/projects.css`, with verified content in
`src/project_data.py`. Rebuild using `python src/build.py`.

## Published routes

- `project-pet-recycling.html`
- `project-eischaalverwerking.html`
- `project-centraal-stofzuigsysteem.html`
- `project-dierenvoeding.html`
- `project-driessen-food-extrusion.html`

The old `toepassing-pet-recycling.html` remains usable and renders the complete
PET case with a canonical URL pointing to `project-pet-recycling.html`.
Desktop/mobile menus, footer and homepage cases link into the collection.

## Content contract

Each case contains: introduction, verified figures, question/brief, four key
functions, three engineering choices, two documentary images, result,
related projects, related knowledge and the shared enquiry form.

Client names are only used when explicitly identified by the source. The four
cases from the original case collection retain anonymous client descriptions.
Driessen is a separate, named case from the June 2022 BULK publication; it is
not assumed to be the client of the anonymous central vacuum project.
Capacities are project-specific, not universal performance promises.

## Visuals

Five original illustrations use a consistent navy studio background, stainless
steel equipment and blue support frames. They are labelled as illustrations
and must never be presented as actual installed equipment photographs.
Built-in image_gen prompts, origins and saved image paths are recorded in
`images/generated-project-assets.json`. Responsive AVIF/WebP images and social
previews are stored in `images/` and registered in `images/manifest.json`.

`images/project-originals/` retains the original case photography and smaller
WebP previews. Photo cards fill their frames using responsive cover crops; enlargement displays the complete original image.
Photo source URLs are retained internally in that folder's `sources.json`; Driessen's two photos
were extracted from the linked original BULK PDF. No fabricated documentary
photographs or customer performance figures were added.

## Interaction contract

`assets/js/projects.js` progressively enhances sector, application and text
filters. Filters combine with AND, text matches ignore case/diacritics, the
result count is announced, and query parameters persist selections. An empty
result includes a reset action. Without JavaScript every project remains
readable and accessible. Original photo links are enhanced into a native modal
dialog with previous/next, arrow keys, Escape and focus restoration.

## Verification (2026-11-20)

All six pages were browser-checked at 320, 375, 768, 1024 and 1440 pixels.
Verified local routes and anchors, loaded images, no horizontal overflow,
section navigation/focus, photo enlargement/navigation/closing, sector and
application filters, no-results reset, URL persistence, desktop/mobile main
navigation, and direct mobile loads with and without JavaScript. No contact
form was submitted. Shared contact-topic handling uses the existing
`installatieontwerp` topic.

2026-11-20 follow-up: removed all visible links/references to the replaced case website and citation URLs from page metadata. Source provenance remains internal. Larger WebP previews fill the gallery frames without padding. All five galleries checked on mobile and desktop, including enlargement and overflow.
