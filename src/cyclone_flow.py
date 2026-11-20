"""Animated flow registered to the transparent chamber in 32-hero-cycloon."""
from math import cos, sin, tau


def cyclone_flow():
    paths = []
    particles = []
    for lane in range(5):
        # Trace the outer vortex down the cylinder and into the narrowing cone.
        points = []
        for step in range(121):
            t = step / 120
            radius = min(77, 8 + 100 * (1 - t)) - lane * 0.8
            angle = tau * (2.85 * t + 0.5 + lane * 0.015)
            x = 391 + 6 * t + radius * cos(angle)
            y = 90 + 243 * t + 0.14 * radius * sin(angle) + lane
            points.append(f"{x:.2f},{y:.2f}")
        guide = f"cyclone-grain-{lane}"
        paths.append(f'<path id="{guide}" d="M {" L ".join(points)}"/>')
        for j in range(24):
            duration = 4.7 + lane * 0.16
            phase = ((j * 0.618034 + lane * 0.37) % 1) * duration
            r = 0.85 + (j * 3 + lane) % 5 * 0.21
            particles.append(f'<circle r="{r:.2f}" fill="url(#cyclone-gold)">'
                             f'<animateMotion dur="{duration:.2f}s" begin="-{phase:.2f}s" repeatCount="indefinite">'
                             f'<mpath href="#{guide}"/></animateMotion></circle>')
    air = []
    for offset in (-3, 3):
        air.append(f'<path transform="translate({offset} 0)" d="M396 267 C371 243 414 229 397 208 S382 184 399 167 S408 143 398 126" '
                   'fill="none" stroke="#bed9ea" opacity=".64" stroke-width="1.3" stroke-dasharray="6 23">'
                   '<animate attributeName="stroke-dashoffset" from="0" to="-29" dur="1.2s" repeatCount="indefinite"/></path>')
    return f'''<svg class="hero__flow" data-flow-svg viewBox="0 0 570 380" aria-hidden="true" focusable="false">
      <defs>{"".join(paths)}
        <radialGradient id="cyclone-gold" cx=".32" cy=".26" r=".77"><stop stop-color="#fff0c8"/>
          <stop offset=".5" stop-color="#e9bd60"/><stop offset="1" stop-color="#a66c1f"/></radialGradient>
        <clipPath id="cyclone-window"><path clip-rule="evenodd" d="M316 86 Q382 61 465 75 L465 146 L408 334 L381 334 L316 160 Z
          M374 72 L374 126 Q400 141 429 127 L429 69 Z"/></clipPath>
      </defs><g clip-path="url(#cyclone-window)">{"".join(air)}{"".join(particles)}</g></svg>'''
