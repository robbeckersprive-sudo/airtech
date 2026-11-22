"""Build Flow pages, all component categories and hero previews into ../.

Usage:  python src/build.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from components import ROOT, PAGES  # noqa: E402
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

FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="6" fill="#22498C"/>'
           '<path fill="#fff" fill-rule="evenodd" d="M4 26 13 6h6l9 20h-6l-2-5h-8l-2 5zm10-10h4l-2-5z"/></svg>')


def main():
    os.makedirs(os.path.join(ROOT, 'assets', 'img'), exist_ok=True)
    with open(os.path.join(ROOT, 'assets', 'img', 'favicon.svg'), 'w', encoding='utf-8') as f:
        f.write(FAVICON)
    home = pages.home()
    templates = (('projecten.html', project_index()), ('over-ons.html', about_page()), ('kennisbank.html', knowledge_index()), ('index.htm', home), ('componenten.html', component_index()), ('toepassing-pet-recycling.html', recycling_application()),
                 (PAGES['home'], home),
                 (PAGES['artikel'], pages.artikel()),
                 (PAGES['categorie'], pages.categorie()), (PAGES['product'], pages.product()))
    previews = ((f'hero-{variant}.html', pages.home(variant)) for variant in EQUIPMENT)
    categories = ((f'componenten-{slug}.html', category_page(slug, data)) for slug, data in CATEGORIES.items())
    products = ((slug+'.html', product_page(data)) for slug, data in PRODUCTS.items() if slug != 'cycloonafscheider')
    articles = (('kennis-'+slug+'.html', knowledge_page(slug, data)) for slug, data in ARTICLES.items())
    solutions = (('oplossingen-'+slug+'.html', solution_page(slug, data)) for slug, data in SOLUTIONS.items())
    projects = (('project-'+slug+'.html', project_page(slug, data)) for slug, data in PROJECTS.items())
    for filename, html in (*templates, *previews, *categories, *products, *articles, *solutions, *projects):
        path = os.path.join(ROOT, filename)
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(html)
        print(f'{filename:40s} {len(html) // 1024} KB')


if __name__ == '__main__':
    main()
    from hero_concepts import build_concepts
    build_concepts()
