# Performance maintenance

Changes on 22 November 2026:

- Self-host the existing Archivo and IBM Plex Mono fonts. Character subsets retain the original full fonts as Unicode fallbacks; the two fixed italic headline styles use the same original weight/width instances.
- Serve responsive WebP logos instead of the large PNG.
- Bundle and minify CSS in document order, recursively resolving local imports. Minify JavaScript during the production build. CSS bundle names and source asset query strings use content hashes.
- Load the Three.js rotor renderer and the inactive slide's SVG images when the dosing slide is selected. Keep the existing SVG fallback.
- Render particles in an OffscreenCanvas worker where supported, with a main-thread fallback, a 30 fps limit and a 1.25 backing-pixel-ratio cap. Preserve pause, pointer interaction, off-screen/hidden-tab suspension and reduced-motion behavior.
- Avoid measuring a straight signature line thousands of times. Keep inactive hero sheets hidden and preserve their transitions when selected.
- Show initial hero photography immediately; retain the scan line, subsequent slide transitions and scroll effects.
- Correct low-contrast small labels and accessible names. Use the supplied live Vercel origin for default canonical/structured-data URLs.

## Build

Use Node.js 24. Run `python src/build.py`, `npm ci`, then `npm run build`.
Vercel runs the Node build against checked-in HTML. The Python generation step therefore belongs before committing.

Font subset maintenance is optional: install `fonttools[woff]==4.64.0` and run `python tools/subset-fonts.py` after generating the HTML. Generated fonts are checked in; Vercel does not need font tooling. Full character sets remain available when future text uses additional characters.

## Validation status

The original public PageSpeed report on 22 November showed Performance 35 mobile / 58 desktop. This is historical baseline data, not a measurement of this commit.

Local optimization runs improved the results substantially, but did **not** establish a reproducible score of 95 across all pages and devices. The animated mobile homepage still needs investigation. A score of 100 in accessibility audits is not a complete accessibility certification.

Checked during development: eleven representative routes at 360, 390, 768, 1280 and 1440 CSS pixels; navigation and focus handling; hero controls and 3D loading; filters and search; product gallery and lightbox; contact-field validation. No physical iPhone/Safari or screen-reader test was available, and no live enquiry was sent.

`check_products.py`, `check_knowledge.py` and `check_solutions.py` pass on the release checkout. `check_categories.py` also fails on the unchanged baseline, with `blowers-ventilatoren: structural drift`; this pre-existing assertion is not a passing check.

For release measurement, run at least three Lighthouse 13.6 mobile and desktop audits of each selected route and report the median and range. Keep the machine otherwise idle. Local gzip/HTTP lab results do not measure the Vercel CDN or real-user Core Web Vitals. Check the deployed commit separately in PageSpeed Insights. Missing CrUX/INP data must remain marked as missing; historical field data does not immediately evaluate a new release.
