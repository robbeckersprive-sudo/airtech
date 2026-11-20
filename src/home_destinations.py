"""Destinations for the homepage catalogue and recycling application."""
from components import COMPONENTEN, breadcrumb, link, page, pic
from product_routes import PRODUCT_ROUTES
from product_data import PRODUCTS


def component_index():
    groups = []
    for title, href, image in COMPONENTEN:
        family = href.removeprefix("componenten-").removesuffix(".html")
        rows = "".join(f'<li>{link(PRODUCTS[slug]["name"], slug + ".html")}</li>'
                       for slug in PRODUCT_ROUTES[family].values())
        groups.append(f'<section><h2 class="h3">{link(title, href)}</h2><ul class="pr-list">{rows}</ul></section>')
    body = (breadcrumb([("Home", "index.html"), ("Componenten", "")])
            + '<section class="section--home"><div class="container"><h1 class="h1">Alle componenten</h1>'
            + '<div class="process__cols">' + ''.join(groups) + '</div></div></section>')
    return page("componenten.html", "Alle componenten | Airtechnic Solutions",
                "Vergelijk de acht componentgroepen en bekijk elke uitvoering.", "og-04-cycloon-vrijstaand.jpg", body)


def recycling_application():
    """Keep the old homepage URL usable with the complete, canonical case."""
    from project_data import PROJECTS
    from project_page import project_page
    return project_page('pet-recycling', PROJECTS['pet-recycling'])
