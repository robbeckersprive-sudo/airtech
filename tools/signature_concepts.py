"""Generate the two "site signature" variants as review pages (home + one page of each other template).

    python src/build.py && python tools/signature_concepts.py

Reads the built pages, sets html[data-sig], adds assets/css/signature.css + assets/js/signature.js and a review switcher.
    sig-a*.html  A  "Hartlijn"    a drawing's centre axis in the left margin: dash-dot hairline that turns off the hero's
                                  tab rule, a datum point + leader + vertical label at every section head
    sig-b*.html  B  "Stroomlijn"  a streamline that peels off the tab rule, runs down the margin and swings in to touch
                                  every section head; a granule rides the drawn tip with a short fading tail
Both also make the hero -> block 2 seam one sheet (the tab bar loses its glass after the fold, the hero grid carries on
into the next section) and replace the orange process line in block 2. The live pages are not touched.
"""
import os
import re
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = [('', 'index.html', 'Home'), ('-categorie', 'componenten-cyclonen.html', 'Categorie'),
         ('-product', 'cycloonafscheider.html', 'Product'), ('-kennis', 'kennis-druk-of-vacuumtransport.html', 'Kennis')]
VARIANTS = [('a', 'A Hartlijn'), ('b', 'B Stroomlijn')]
LABELS = {  # short station labels (aria-labelledby id -> label); other headings fall back to their first line
    'spec-title': 'Specialisaties', 'comp-title': 'Componenten', 'steps-title': 'Werkwijze', 'kennis-title': 'Kennis',
    'faq-title': 'Vragen', 'contact-title': 'Contact', 'werking-title': 'Werking', 'uitv-title': 'Uitvoering',
    'toep-title': 'Toepassingen', 'relc-title': 'Verwant', 'advies-title': 'Advies', 'principe-title': 'Principe',
    'rel-title': 'Verwant', 'meer-title': 'Verder lezen', 'vergelijking': 'Vergelijking', 'cat-grid-title': 'Overzicht',
}


def switcher(v, suffix):
    pages = ''.join(f'<a href="sig-{v}{s}.html"{" aria-current=page" if s == suffix else ""}>{n}</a>' for s, _, n in PAGES)
    vs = ''.join(f'<a href="sig-{k}{suffix}.html"{" aria-current=page" if k == v else ""}>{n}</a>' for k, n in VARIANTS)
    return f'<nav class="sig-switch" aria-label="Signature-varianten"><span>Signature</span>{vs}<i></i>{pages}</nav>'


def make(html, v, suffix):
    ver = int(time.time())
    html = re.sub(r'<html lang="nl"', f'<html lang="nl" data-sig="{v}"', html, count=1)
    html = re.sub(r'(<link rel="stylesheet" href="assets/css/site\.css[^>]*>)',
                  rf'\1\n<link rel="stylesheet" href="assets/css/signature.css?v={ver}">', html, count=1)
    html = re.sub(r'(<script src="assets/js/site\.js[^>]*></script>)',
                  rf'\1\n<script src="assets/js/signature.js?v={ver}" defer></script>', html, count=1)
    html = html.replace(' data-process-line>', '>')          # site.js leaves the old line alone
    html = html.replace('data-process-node>', 'data-process-node data-sig-node>')
    html = html.replace('aria-label="Uit de praktijk"', 'aria-label="Uit de praktijk" data-sig-label="Praktijk"')
    for k, lab in LABELS.items():
        html = html.replace(f'aria-labelledby="{k}"', f'aria-labelledby="{k}" data-sig-label="{lab}"', 1)
    html = re.sub(r'<title>', '<title>[Signature ' + v.upper() + '] ', html, count=1)
    return html.replace('</body>', switcher(v, suffix) + '\n</body>', 1)


def main():
    for suffix, src, _ in PAGES:
        with open(os.path.join(ROOT, src), encoding='utf-8') as f:
            html = f.read()
        for v, _ in VARIANTS:
            out = f'sig-{v}{suffix}.html'
            with open(os.path.join(ROOT, out), 'w', encoding='utf-8', newline='\n') as f:
                f.write(make(html, v, suffix))
            print(out)


if __name__ == '__main__':
    main()
