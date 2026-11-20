"""Three review concepts for where the site signature (Hartlijn) starts on the home page.

    python src/build.py && python tools/sig_start_concepts.py

All three start one grid step below the hero, so the line no longer hooks off the tab rule through the tab labels.
    sig-start-a.html  Nulpunt   a datum mark (ring with two filled quarters) on the grid: the drawing's origin
    sig-start-b.html  Instroom  the line enters from the sheet edge with a flow arrow and bends down into the margin
    sig-start-c.html  Bron      the line rises out of the grid (fade) and turns solid at the H1's pulsing source dot
The live index.html is not touched.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONCEPTS = [('a', 'origin', 'A Nulpunt'), ('b', 'inlet', 'B Instroom'), ('c', 'source', 'C Bron')]


def main():
    with open(os.path.join(ROOT, 'index.html'), encoding='utf-8') as f:
        html = f.read()
    for k, mode, name in CONCEPTS:
        links = ''.join(f'<a href="sig-start-{kk}.html"{" aria-current=page" if kk == k else ""}>{nn}</a>' for kk, _, nn in CONCEPTS)
        out = html.replace('data-sig-start="origin"', f'data-sig-start="{mode}"', 1)
        out = re.sub(r'<title>', f'<title>[Start {name}] ', out, count=1)
        out = out.replace('</body>', f'<nav class="sig-switch" aria-label="Startconcepten"><span>Start</span>{links}</nav>\n</body>', 1)
        with open(os.path.join(ROOT, f'sig-start-{k}.html'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(out)
        print(f'sig-start-{k}.html')


if __name__ == '__main__':
    main()
