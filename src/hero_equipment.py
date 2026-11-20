"""Process-line hero variants using the existing cutaway illustrations."""
from html import escape

from components import MANIFEST, PAGES, pic


HALL_IMAGE = '29-hero-productiehal'
HALL_SIZES = '(min-width: 720px) 100vw, 170vw'

# Paths use a 1000 × 1000 grid over each cutaway, regardless of its aspect ratio.
EQUIPMENT = {
    'doseersluis': {
        'name': 'Doseersluis',
        'image': '15-doseersluis-doorsnede',
        'alt': 'Doorsnede van een RVS doseersluis met granulaat in de rotorvakken',
        'discipline': 'Doseren',
        'caption': 'De rotor neemt granulaat mee in vakken en laat het onderaan vallen.',
        'flow': (
            ('product', 'M 283 120 Q 297 176 309 221 T 336 327 Q 347 353 368 390', 2.8, 13),
            ('product', 'M 358 127 Q 386 177 406 226 T 426 369', 2.6, 12),
            ('product', 'M 431 148 Q 434 200 441 237 T 439 347', 3.1, 10),
            ('product', 'M 368 758 Q 355 809 358 866 T 362 927', 2.3, 8),
            ('product', 'M 402 769 Q 406 826 397 883 L 399 925', 2.5, 7),
        ),
    },
    'blower': {
        'name': 'Blower',
        'image': '14-blower-doorsnede',
        'alt': 'Doorsnede van een centrifugaalblower met waaier en elektromotor',
        'discipline': 'Lucht verplaatsen',
        'caption': 'Lucht komt door de ronde inlaat binnen. De waaier voert haar naar de uitlaat bovenaan.',
        'flow': (
            ('air', 'M 82 585 C 105 612 170 652 229 658 C 311 699 381 774 472 734 C 569 693 582 516 530 377 C 477 238 360 177 242 199 C 172 212 148 167 143 67', 5.6, 8),
            ('air', 'M 99 550 C 122 563 180 578 233 599 C 319 637 384 711 471 689 C 551 669 551 492 501 363 C 449 232 345 205 231 225 C 160 236 120 187 117 70', 5.2, 8),
            ('air', 'M 110 512 C 137 520 198 523 239 554 C 324 596 392 658 460 641 C 536 617 521 478 477 357 C 421 244 328 237 222 251 C 137 261 98 201 92 75', 4.9, 7),
        ),
    },
    'cycloon': {
        'name': 'Cycloonafscheider',
        'image': '13-cycloon-doorsnede',
        'alt': 'Doorsnede van een cycloonafscheider met tangentiële inlaat en conische opvang',
        'discipline': 'Scheiden',
        'caption': 'Granulaat zakt langs de wand. De lucht verlaat de cycloon via de bovenkant.',
        'flow': (
            ('product', 'M 186 221 C 315 219 280 285 526 254 C 795 223 917 273 843 316 C 758 363 322 356 350 415 C 387 464 805 461 783 516 C 768 558 555 550 570 607 Q 586 663 610 708', 5.9, 27),
            ('product', 'M 192 241 C 316 246 305 284 539 268 C 804 247 917 280 821 324 C 733 365 342 367 369 421 C 416 466 793 470 766 523 C 743 564 564 565 579 612 L 599 701', 6.5, 24),
            ('air', 'M 467 415 C 572 396 696 389 679 356 C 655 326 552 343 560 304 C 560 273 697 261 685 222 C 676 189 597 204 600 163 C 603 136 675 116 654 80 Q 643 55 650 31', 4.5, 9),
        ),
    },
}


def flow_svg(equipment):
    image = MANIFEST[equipment['image']]
    ratio = image['w'] / image['h']
    guides, moving = [], []
    for i, (material, path, seconds, count) in enumerate(equipment['flow']):
        guide = f'equipment-flow-{i}'
        guides.append(f'<path id="{guide}" class="equipment-guide equipment-guide--{material}" d="{path}"/>')
        for j in range(count):
            radius = (1.9, 3.2, 2.5, 4.1)[(j * 3 + i) % 4]
            opacity = (0.55, 0.92, 0.75, 0.66)[(j + i) % 4]
            phase = -(j + i * .41 + (j % 3) * .19) * seconds / count
            moving.append(f'<ellipse class="equipment-particle equipment-particle--{material}" '
                          f'rx="{radius / ratio:.2f}" ry="{radius}" opacity="0">'
                          f'<animateMotion dur="{seconds}s" begin="{phase:.3f}s" repeatCount="indefinite">'
                          f'<mpath href="#{guide}"/></animateMotion>'
                          f'<animate attributeName="opacity" values="0;{opacity};{opacity};0" keyTimes="0;.08;.9;1" '
                          f'dur="{seconds}s" begin="{phase:.3f}s" repeatCount="indefinite"/></ellipse>')
    return f'''<svg class="hero__flow" viewBox="0 0 {ratio * 1000:.6f} 1000" aria-hidden="true" focusable="false" data-flow-svg>
        <g transform="scale({ratio:.8f} 1)">{''.join(guides)}{''.join(moving)}</g>
      </svg>'''


def equipment_stage(variant):
    equipment = EQUIPMENT[variant]
    image = MANIFEST[equipment['image']]
    return f'''<div class="hero__media hero__hall">{pic(HALL_IMAGE, sizes=HALL_SIZES, eager=True)}</div>
    <figure class="hero__equipment-area" style="--equipment-ratio:{image['w'] / image['h']:.8f}">
      <div class="hero__equipment">
        {pic(equipment['image'], equipment['alt'], '(min-width: 720px) 52vw, 92vw', eager=True)}
        {flow_svg(equipment)}
      </div>
      <figcaption class="hero__equipment-caption">{escape(equipment['caption'])}</figcaption>
    </figure>'''


def variant_nav(active):
    links = [f'<a href="{PAGES["home"]}">Pijpleiding</a>']
    for variant, equipment in EQUIPMENT.items():
        current = ' aria-current="page"' if variant == active else ''
        links.append(f'<a href="hero-{variant}.html"{current}>{equipment["name"]}</a>')
    return f'<nav class="hero__variants" aria-label="Vergelijk hero’s">{"".join(links)}</nav>'
