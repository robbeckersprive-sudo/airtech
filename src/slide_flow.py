"""Photo-space flow paths for the equipment hero slides (570 x 380)."""


def moving_grains(name, lanes):
    guides, grains = [], []
    for i, (path, count, seconds, radius) in enumerate(lanes):
        guide = f'{name}-lane-{i}'
        guides.append(f'<path id="{guide}" d="{path}"/>')
        for j in range(count):
            phase = ((j + (i * .37 + j * .17) % 1) / count) * seconds
            size = radius * (.78 + .12 * ((j + i) % 5))
            timing = f'dur="{seconds}s" begin="-{phase:.2f}s" repeatCount="indefinite"'
            grains.append(f'<circle r="{size:.2f}" fill="url(#{name}-gold)">'
                          f'<animateMotion {timing}><mpath href="#{guide}"/></animateMotion>'
                          f'<animate attributeName="opacity" values="0;.95;.95;0" keyTimes="0;.08;.9;1" {timing}/></circle>')
    return ''.join(guides), ''.join(grains)


def overlay(name, window, lanes, air=()):
    guides, grains = moving_grains(name, lanes)
    streams = ''.join(f'<path d="{d}" fill="none" stroke="#bdd9ed" stroke-width="1.25" '
                      'opacity=".72" stroke-dasharray="4 13"><animate attributeName="stroke-dashoffset" '
                      'from="0" to="-17" dur="1s" repeatCount="indefinite"/></path>' for d in air)
    return f'''<svg class="hero__flow" data-flow-svg viewBox="0 0 570 380" aria-hidden="true" focusable="false">
      <defs>{guides}<clipPath id="{name}-window"><path clip-rule="evenodd" d="{window}"/></clipPath>
        <radialGradient id="{name}-gold" cx=".32" cy=".26" r=".77"><stop stop-color="#fff0c8"/>
        <stop offset=".5" stop-color="#e9bd60"/><stop offset="1" stop-color="#a66c1f"/></radialGradient></defs>
      <g clip-path="url(#{name}-window)">{streams}{grains}</g></svg>'''


def filter_flow():
    window = 'M313 91 Q382 72 466 83 L467 267 L313 269 Z'
    lanes = []
    air = []
    for x in (342, 390, 433):
        # Fine dust reaches the pleats, then shed dust falls below each cartridge.
        lanes.extend([(f'M{x-20} 189 Q{x-22} 165 {x-11} 154', 10, 2.4, .98),
                      (f'M{x-8} 200 Q{x-11} 218 {x-2} 235 T{x+4} 272', 8, 2.1, 1.1),
                      (f'M{x+5} 202 Q{x+12} 226 {x+7} 241 T{x+10} 270', 6, 2.4, .85)])
        air.append(f'M{x-19} 172 Q{x-1} 164 {x} 149 L{x} 96')
    return overlay('filter', window, lanes, air)


def diverter_flow():
    window = 'M293 96 L366 95 L369 142 Q327 170 312 213 L285 246 L254 287 Q232 294 223 277 L253 193 Z'
    lanes = [(f'M{300+i*5} 91 Q{301+i*4} 145 {284+i*4} 178 T{234+i*5} 294',
              14, 2.1 + i*.09, 1.55) for i in range(5)]
    return overlay('diverter', window, lanes)


# Drawn in the same 570 x 380 photo coordinates as the machinery overlays.
# These outer traces leave the inspection windows and the copy column clear.
HERO_TRACES = {
    "30-hero-filter": (
        "M145 16 C208 18 271 39 278 99 S265 239 288 287 Q310 329 354 348",
        "M166 6 C245 9 288 39 289 96 S280 235 299 276 Q321 315 354 331",
        "M488 252 C507 205 499 158 506 98 S532 29 566 10",
    ),
    "31-hero-wissel": (
        "M273 7 C271 75 267 101 239 154 S192 221 155 319",
        "M285 7 C283 73 280 110 250 163 S201 236 168 328",
        "M296 12 C298 80 290 118 262 172 S215 238 181 332",
    ),
    "32-hero-cycloon": (
        "M195 78 C244 95 304 75 321 73 C385 44 496 67 485 132 C479 181 353 180 337 219 S394 269 417 299 Q424 318 401 344",
        "M202 68 C259 84 302 64 322 63 C392 33 506 61 496 131 C488 190 364 192 349 223 S411 266 425 298 Q437 322 410 348",
    ),
    "33-hero-doseersluis": (
        "M259 15 C288 53 342 45 380 84 C431 138 428 217 386 267 Q360 298 324 321",
        "M273 12 C300 42 355 40 391 80 C444 136 442 221 396 277 Q363 312 331 330",
    ),
}


def hero_traces(image):
    name = "trace-" + image[:2]
    lines = []
    for i, path in enumerate(HERO_TRACES[image]):
        lines.append(f'<path class="sl-base" pathLength="1000" d="{path}"/>'
                     f'<path class="machine-trace" pathLength="1000" d="{path}">'
                     f'<animate attributeName="stroke-dashoffset" from="1000" to="0" '
                     f'dur="{5.8 + .65*i:.2f}s" begin="-{1.1 + 1.6*i:.2f}s" repeatCount="indefinite"/>'
                     '</path>')
    return f'''<svg class="hero__flow" data-flow-svg viewBox="0 0 570 380" aria-hidden="true" focusable="false">
      <defs><linearGradient id="{name}-fade"><stop stop-color="black" offset=".21"/>
        <stop stop-color="white" offset=".49"/></linearGradient>
        <mask id="{name}-mask"><rect width="570" height="380" fill="url(#{name}-fade)"/></mask></defs>
      <g class="hero__lines" mask="url(#{name}-mask)">{"".join(lines)}</g></svg>'''
