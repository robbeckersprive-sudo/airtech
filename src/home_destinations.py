"""Destinations for the homepage catalogue and recycling application."""
from components import COMPONENTEN, breadcrumb, link, page, pic
from product_routes import PRODUCT_ROUTES
from product_data import PRODUCTS


def component_index():
    """componenten.html (Nov 21): the eight groups as Röntgen plates (same plates and scan line as home block 3, styles
    in home-blocks.css "OVERVIEW", behaviour home-blocks.js with a vertical grid: on phones the page scroll moves the
    scan). Each plate carries its group's uitvoeringen as a numbered list."""
    import re
    from components import split_lines, sym, icon, COMP_SYM, _v
    from home_blocks import SECTION_IMG, _items
    from category_data import CATEGORIES
    from cyclone_category_data import CYCLONES
    sizes = '(min-width: 900px) 30vw, 92vw'
    cards, total = [], 0
    for i, (title, href, image) in enumerate(COMPONENTEN):
        family = href.removeprefix("componenten-").removesuffix(".html")
        intro = (CYCLONES if family == 'cyclonen' else CATEGORIES[family])['intro']
        intro = re.match(r'(.+?[.!?])(\s|$)', intro).group(1)
        sec, mode = SECTION_IMG[title]
        names = _items(href)
        total += len(names)
        rows = "".join(f'<li><a href="{slug}.html"><span class="co-row__no">{i + 1}.{k + 1}</span><span>{PRODUCTS[slug]["name"]}</span>{icon("ur")}</a></li>'
                       for k, slug in enumerate(PRODUCT_ROUTES[family].values()))
        reg = ''.join(f'<i class="cx-reg cx-reg--{c}"></i>' for c in ('tl', 'tr', 'bl', 'br'))
        cards.append(f'''<article class="co-card" id="{family}" style="--i:{i}">
      <a class="cx-link co-plate" href="{href}" data-cx-card data-scan="{mode}" aria-label="{title}: alle uitvoeringen — Doorsnede {i + 1:02d}/{len(COMPONENTEN):02d}">
        <span class="cx-plate" aria-hidden="true">
          <span class="cx-img cx-img--ext">{pic(image, "", sizes, eager=i == 0)}</span>
          <span class="cx-img cx-img--sec">{pic(sec, "", sizes)}</span>
          <i class="cx-scan"><b>Doorsnede</b></i>{reg}
          <span class="cx-no">{i + 1:02d}<small>/{len(COMPONENTEN):02d}</small></span>
        </span>
      </a>
      <div class="co-body">
        <h2 class="co-name">{sym(COMP_SYM[title], "sym co-sym")}<a href="{href}">{title}</a></h2>
        <p class="co-intro">{intro}</p>
        <ol class="co-rows">{rows}</ol>
      </div>
    </article>''')
    chips = ''.join(f'<li><a href="#{h.removeprefix("componenten-").removesuffix(".html")}">{t}</a></li>' for t, h, _img in COMPONENTEN)
    body = f'''<section class="co" data-cx>
  <div class="container">
    <div class="category-crumbs co-crumbs">{breadcrumb([("Home", "index.html"), ("Componenten", "")])}</div>
    <header class="co-head">
      <p class="cv-kicker"><span class="cv-kicker__dot" aria-hidden="true"></span>Componenten</p>
      <h1 class="h1">{split_lines("Alle<br><em>componenten.</em>")}</h1>
      <div class="co-lead">
        <p>{len(COMPONENTEN)} componentgroepen voor industriële luchttechniek en solids processing, samen {total} uitvoeringen. Beweeg over een groep en kijk erin.</p>
        <ul class="co-jump" aria-label="Spring naar een groep">{chips}</ul>
      </div>
    </header>
    <div class="co-grid" data-cx-deck data-cx-vertical>{"".join(cards)}</div>
  </div>
</section>
<script src="{_v("assets/js/home-blocks.js")}" defer></script>'''
    return page("componenten.html", "Alle componenten | Airtechnic Solutions",
                "Vergelijk de acht componentgroepen en bekijk elke uitvoering.", "og-04-cycloon-vrijstaand.jpg", body,
                stylesheet="assets/css/home-blocks.css", nav_current="Componenten")


def recycling_application():
    """Keep the old homepage URL usable with the complete, canonical case."""
    from project_data import PROJECTS
    from project_page import project_page
    return project_page('pet-recycling', PROJECTS['pet-recycling'])
