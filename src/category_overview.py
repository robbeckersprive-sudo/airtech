"""Reusable opening, filters and comparison cards for category pages."""
from dataclasses import dataclass
from html import escape

from components import breadcrumb, btn, icon, link, pic

HERO_SIZES = '(min-width: 1280px) 635px, (min-width: 900px) 50vw, 94vw'
CARD_SIZES = '(min-width: 1120px) 300px, (min-width: 620px) 46vw, 94vw'


@dataclass(frozen=True)
class CategoryOption:
    name: str
    feature: str
    use: str
    image: str
    alt: str
    href: str
    action: str
    applications: str
    variant: str
    photo: bool = False
    executions: tuple = ()   # candidate uitvoeringen (execution_data.EXECUTIONS); shown only when CONFIRMED


def category_intro(title, crumbs, intro, image, alt, caption):
    return f'''<div class="category-sheet">
  <div class="container">
    <div class="category-crumbs">{breadcrumb(crumbs)}</div>
    <section class="category-hero" aria-labelledby="cat-h1">
      <div class="category-hero__copy">
        <h1 id="cat-h1" class="h1">{title}</h1>
        <p class="category-hero__lead">{escape(intro)}</p>
        <div class="category-actions">
          {btn("Vergelijk de uitvoeringen", "#cat-grid-title", "lg", icon_name="down")}
          {link("Hulp bij uw keuze", "#advies", "down")}
        </div>
      </div>
      <figure class="category-plate">
        <div class="category-plate__photo">{pic(image, alt, HERO_SIZES, eager=True)}</div>
        <figcaption><span>In de installatie</span><span>{escape(caption)}</span></figcaption>
      </figure>
    </section>
  </div>
</div>'''


def _filter_field(name, label, options):
    choices = ''.join(f'<option value="{escape(value)}">{escape(text)}</option>' for value, text in options)
    return f'''<div class="category-field">
      <label for="{name}">{label}</label>
      <select id="{name}" name="{name}"><option value="">Alle {label.lower()}en</option>{choices}</select>
    </div>'''


def category_catalog(title, intro, items, applications, variants, advice_url):
    """Show the same information in the same order for every solution."""
    cards = ''.join(
        f'''<article class="category-option" id="oplossing-{escape(item.variant)}" data-item
        data-toepassing="{escape(item.applications)}" data-uitvoering="{escape(item.variant)}">
      <div class="category-option__image{' category-option__image--photo' if item.photo else ''}">
        {pic(item.image, item.alt, CARD_SIZES)}
      </div>
      <div class="category-option__body">
        <h3 class="h3">{escape(item.name)}</h3>
        <dl>
          <div><dt>Kenmerk</dt><dd>{escape(item.feature)}</dd></div>
          <div><dt>Past bij</dt><dd>{escape(item.use)}</dd></div>
        </dl>
        {link(item.action, item.href, extra=f'<span class="visually-hidden"> · {escape(item.name)}</span>')}
      </div>
    </article>''' for item in items)
    return f'''<section class="section category-catalog" aria-labelledby="cat-grid-title">
  <div class="container">
    <header class="category-heading">
      <h2 id="cat-grid-title" class="h2">{title}</h2>
      <p>{escape(intro)}</p>
    </header>
    <form class="category-filters" role="search" aria-label="Filter oplossingen" data-filter="cat-grid" data-status="filter-status" data-empty="filter-empty">
      <div class="category-field">
        <label for="q">Zoeken</label>
        <span class="category-search">{icon("search")}<input id="q" name="q" type="search" placeholder="Bijv. granulaten" autocomplete="off"></span>
      </div>
      {_filter_field("toepassing", "Toepassing", applications)}
      {_filter_field("uitvoering", "Uitvoering", variants)}
      <button class="text-btn category-reset" type="button" data-reset>Wis filters</button>
      <p class="category-count" id="filter-status" role="status">{len(items)} oplossingen gevonden</p>
    </form>
    <div class="category-options" id="cat-grid">{cards}</div>
    <div class="empty-state category-empty" id="filter-empty" hidden>
      <h3 class="h3">Geen oplossingen gevonden</h3>
      <p>Pas uw zoekterm aan of wis de filters om alle uitvoeringen te bekijken.</p>
      <div class="category-actions"><button class="text-btn" type="button" data-reset>Wis filters</button>{link("Vraag technisch advies", advice_url)}</div>
    </div>
  </div>
</section>'''
