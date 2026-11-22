# Performance maintenance

Changes on 22 November 2026:

- Self-host the existing Archivo and IBM Plex Mono fonts. Character subsets retain the original full fonts as Unicode fallbacks; the two fixed italic headline styles use the same original weight/width instances.
- Serve responsive WebP logos instead of the large PNG.
- Bundle and minify CSS in document order, recursively resolving local imports. Minify JavaScript during the production build. CSS bundle names and source asset query strings use content hashes.
- Load the Three.js rotor renderer and the inactive slide's SVG images when the dosing slide is selected. Keep the existing SVG fallback.
- Render particles in an OffscreenCanvas worker where supported, with a main-thread fallback. The follow-up below uses cached, pixel-aligned textures at up to 60 fps on desktop; phones retain the existing renderer, 30 fps timer budget and 1.25 backing-pixel-ratio cap. Preserve pause, pointer interaction, off-screen/hidden-tab suspension and reduced-motion behavior.
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


## Follow-up: desktop motion, project tabs and contact text (22 November 2026)

Desktop reuses small rotated grain textures and draws them at integer pixel destinations. This removes repeated per-grain resampling. One visible packed layer over the bed fill replaces two overlapping layers, with a 1x backing-pixel cap. Worker requestAnimationFrame follows presentation frames up to 60 fps; the timer fallback accounts for drawing time. Phones keep the original two layers, backing resolution and worker timer cadence. No runtime dependency was added.

Desktop texture preparation waits until the existing hero photo has decoded and painted. The glass image is fetched alongside the photo and its Blob is passed into the worker, avoiding a second download or a serial image request. Pause, offscreen suspension, reduced motion, the main-thread fallback, both regimes and pointer interaction remain available.

The five project panels use div elements with role="tabpanel" rather than overriding article semantics. The existing labelled tabs, selected states, keyboard controls and inert inactive panels are preserved. Contact email text has a semantic break after @, with its domain kept intact. Phone contact rows reserve enough text space while retaining their full touch height; the mailto value and copied address remain unchanged.

Validation of this change:

- Production build: 100 pages, 15 CSS bundles; generated HTML review confirmed only the requested markup and asset-version changes across 74 pages.
- Browser checks: worker animation, pause/resume, dilute mode, reduced-motion suspension, offscreen suspension and main-thread fallback; no page errors.
- Contact address: fits its text column at 320, 360, 375, 390, 430, 768, 1024 and 1440 CSS pixels without orphan trailing characters. Visually checked on a 375px phone viewport.
- axe-core project-tab checks: aria-allowed-role, aria-required-children, aria-required-parent and aria-valid-attr-value pass. Arrow keys, Home/End, selected states and inert inactive panels pass.
- Product, knowledge and solution validation scripts pass.
- Desktop canvas sampling: approximately 15 fps before, 56-60 fps after; the final 2.5-second sample recorded 140 frames, a 16.7ms median interval and a 32ms 95th-percentile interval. This is a local browser observation, not a guarantee for every device.

Lighthouse 12.8.2, bundled Chromium 1243, local HTTP server, three successful runs per device and version. Compare against commit 13c448d. Failed baseline audits with TARGET_CRASHED were excluded and replaced; they were not counted as zero performance scores. Earlier experimental renderers were rejected and are not included below. Scores fluctuate on the unchanged baseline too.

| Device | Version | Performance median (range) | LCP median | TBT median |
|---|---|---:|---:|---:|
| Desktop | Before | 65 (54-65) | 8114 ms | 42 ms |
| Desktop | After | 65 (64-65) | 7965 ms | 36 ms |
| Mobile | Before | 65 (65-71) | 8116 ms | 29 ms |
| Mobile | After | 65 (65-68) | 8112 ms | 48 ms |

The below-fold final contact-row alignment adjustment changes only CSS spacing, not animation or resource loading. These laboratory results do not certify an unchanged live PageSpeed score or real-user Core Web Vitals. Recheck the deployed commit on Vercel; no physical iPhone/Safari test or real enquiry was performed.
