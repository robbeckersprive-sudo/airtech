"""Reusable editorial page shell and decision aids for knowledge articles."""
from html import escape

from components import breadcrumb, btn, icon, link, pic, sym

HERO_SIZES = '(min-width: 1280px) 620px, (min-width: 900px) 48vw, 94vw'


def knowledge_intro(title, crumbs, intro, image, alt, caption, actions):
    primary, secondary = actions
    return f'''<div class="knowledge-sheet">
  <div class="container">
    <div class="knowledge-crumbs">{breadcrumb(crumbs)}</div>
    <header class="knowledge-hero">
      <div class="knowledge-hero__copy">
        <h1 id="art-h1" class="h1">{title}</h1>
        <p class="knowledge-hero__lead">{escape(intro)}</p>
        <div class="knowledge-actions">{btn(*primary, size="lg", icon_name="down")}{link(*secondary, arrow="down")}</div>
      </div>
      <figure class="knowledge-plate">
        <div class="knowledge-plate__media">{pic(image, alt, HERO_SIZES, eager=True)}</div>
        <figcaption><span>{escape(caption[0])}</span><span>{escape(caption[1])}</span></figcaption>
      </figure>
    </header>
  </div>
</div>'''


def knowledge_takeaway(title, items):
    points = ''.join(
        f'<div><dt>{escape(label)}</dt><dd>{escape(text)}</dd></div>' for label, text in items
    )
    return f'''<section class="knowledge-takeaway" aria-labelledby="knowledge-takeaway-title">
  <div class="container">
    <h2 class="h3" id="knowledge-takeaway-title">{escape(title)}</h2>
    <dl>{points}</dl>
  </div>
</section>'''


def knowledge_article(header, takeaway, sections, sources):
    toc = ''.join(f'<li><a href="#{id_}">{escape(label)}</a></li>' for id_, label, _ in sections)
    contents = ''.join(html for _, _, html in sections)
    citations = ''.join(f'<li>{link(escape(label), url)}</li>' for label, url in sources)
    return f'''<article class="knowledge-article" aria-labelledby="art-h1">
  {header}
  {takeaway}
  <div class="container knowledge-layout">
    <aside class="knowledge-rail" aria-label="Artikelnavigatie">
      <div class="knowledge-rail__sticky">
        <nav class="knowledge-toc" aria-label="In dit artikel" data-scrollspy="145">
          <p>In dit artikel</p><ol>{toc}</ol>
        </nav>
        <div class="knowledge-share">
          <button class="share-btn" type="button" data-share>{icon("share")}<span>Artikel delen</span></button>
          <p class="share-status" data-share-status role="status"></p>
        </div>
      </div>
    </aside>
    <div class="knowledge-content">
      {contents}
      <details class="knowledge-sources">
        <summary>Technische bronnen {icon("chev-down")}</summary>
        <ul>{citations}</ul>
      </details>
    </div>
  </div>
</article>'''


def knowledge_section(id_, title, content):
    return f'''<section class="knowledge-section" aria-labelledby="{id_}">
      <h2 class="h2" id="{id_}" tabindex="-1">{title}</h2>
      {content}
    </section>'''


def knowledge_comparison(caption, headings, rows):
    headers = ''.join(f'<th scope="col" role="columnheader">{escape(label)}</th>' for label in headings)
    body = []
    for criterion, *cells in rows:
        data = ''.join(
            f'<td role="cell"><span class="knowledge-mobile-label" aria-hidden="true">{escape(label)}</span>{escape(text)}</td>'
            for label, text in zip(headings[1:], cells, strict=True)
        )
        body.append(f'<tr role="row"><th scope="row" role="rowheader">{escape(criterion)}</th>{data}</tr>')
    return f'''<table class="knowledge-table" role="table">
      <caption class="visually-hidden">{escape(caption)}</caption>
      <thead role="rowgroup"><tr role="row">{headers}</tr></thead>
      <tbody role="rowgroup">{''.join(body)}</tbody>
    </table>'''


def knowledge_scenarios(cases):
    return '<div class="knowledge-scenarios">' + ''.join(
        f'<details name="knowledge-situation"{" open" if i == 0 else ""}>'
        f'<summary><span>{escape(situation)}</span>{icon("chev-down")}</summary>'
        f'<p><strong>{escape(direction)}</strong> {escape(reason)}</p></details>'
        for i, (situation, direction, reason) in enumerate(cases)
    ) + '</div>'


def knowledge_flow(title, stages, air_first, caption):
    nodes = ''.join(
        f'<li><span class="knowledge-flow__node">{sym(symbol)}</span><span>{escape(label)}</span></li>'
        for symbol, label in stages
    )
    return f'''<figure class="knowledge-flow" aria-label="{escape(title)}">
      <ol class="knowledge-flow__stages{" knowledge-flow__stages--air-first" if air_first else ""}">{nodes}</ol>
      <figcaption>{escape(caption)}</figcaption>
    </figure>'''
