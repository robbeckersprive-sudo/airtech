"""Build Flow pages, all component categories and hero previews into ../ (Dutch), ../en/ and ../de/.

Usage:  python src/build.py          all languages
        python src/build.py nl       one language
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from components import ROOT, PAGES  # noqa: E402
import i18n  # noqa: E402
from hero_equipment import EQUIPMENT  # noqa: E402
import pages  # noqa: E402
from category_data import CATEGORIES
from category_page import category_page
from product_data import PRODUCTS
from product_page import product_page
from home_destinations import component_index, recycling_application
from knowledge_data import ARTICLES
from knowledge_page import knowledge_page
from knowledge_index import knowledge_index
from solution_data import SOLUTIONS
from solution_page import solution_page
from about_page import about_page
from project_data import PROJECTS
from project_page import project_index, project_page
from sector_data import SECTORS, ORDER as SECTOR_ORDER, sector_file
from sector_page import sector_index, sector_page

FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="6" fill="#22498C"/>'
           '<path fill="#fff" fill-rule="evenodd" d="M4 26 13 6h6l9 20h-6l-2-5h-8l-2 5zm10-10h4l-2-5z"/></svg>')


def page_builders():
    """(Dutch file name, builder) for every page. Builders render in the active i18n language."""
    home = lambda: pages.home()
    yield from (('projecten.html', project_index), ('over-ons.html', about_page), ('kennisbank.html', knowledge_index),
                ('index.htm', home), ('componenten.html', component_index),
                ('toepassing-pet-recycling.html', recycling_application),
                (PAGES['home'], home), (PAGES['artikel'], pages.artikel),
                (PAGES['categorie'], pages.categorie), (PAGES['product'], pages.product))
    yield from ((f'hero-{variant}.html', lambda v=variant: pages.home(v)) for variant in EQUIPMENT)
    yield from ((f'componenten-{slug}.html', lambda s=slug, d=data: category_page(s, d)) for slug, data in CATEGORIES.items())
    yield from ((slug + '.html', lambda d=data: product_page(d)) for slug, data in PRODUCTS.items() if slug != 'cycloonafscheider')
    yield from (('kennis-' + slug + '.html', lambda s=slug, d=data: knowledge_page(s, d)) for slug, data in ARTICLES.items())
    yield from (('oplossingen-' + slug + '.html', lambda s=slug, d=data: solution_page(s, d)) for slug, data in SOLUTIONS.items())
    yield from (('project-' + slug + '.html', lambda s=slug, d=data: project_page(s, d)) for slug, data in PROJECTS.items())
    yield ('sectoren.html', sector_index)
    yield from ((sector_file(slug), lambda s=slug: sector_page(s, SECTORS[s])) for slug in SECTOR_ORDER)


def write(rel, html):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline=chr(10)) as f:
        f.write(html)
    print(f'{rel:58s} {len(html) // 1024} KB')


def main(langs=i18n.LANGS):
    os.makedirs(os.path.join(ROOT, 'assets', 'img'), exist_ok=True)
    with open(os.path.join(ROOT, 'assets', 'img', 'favicon.svg'), 'w', encoding='utf-8') as f:
        f.write(FAVICON)
    cache = {}
    for code in langs:
        with i18n.use(code):
            for filename, build in page_builders():
                if code != i18n.DEFAULT and not i18n.localized(filename):
                    continue          # review / preview pages stay Dutch-only
                if build not in cache or code != i18n.DEFAULT:
                    cache[build] = build()
                write(i18n.DIR[code] + i18n.filename(filename, code), i18n.finalize(cache[build], code))
    # Untranslated content segments (Dutch fallback): list them for tools/i18n_sync.py
    for code in langs:
        if code == i18n.DEFAULT:
            continue
        report = os.path.join(i18n.LOCALES, f'missing-{code}.json')
        misses = i18n.MISSES[code]
        if misses:
            os.makedirs(i18n.LOCALES, exist_ok=True)
            with open(report, 'w', encoding='utf-8', newline=chr(10)) as f:
                json.dump(misses, f, ensure_ascii=False, indent=1)
            print(f'[i18n] {code}: {len(misses)} untranslated segments -> {os.path.relpath(report, ROOT)}')
        elif os.path.exists(report):
            os.remove(report)


if __name__ == '__main__':
    main(tuple(sys.argv[1:]) or i18n.LANGS)
    from hero_concepts import build_concepts
    build_concepts()
    import kiosk_page  # Beurs Kiosk Modus: beheer.html, kiosk.html, kiosk-sw.js (Dutch for now)
    kiosk_page.main()
