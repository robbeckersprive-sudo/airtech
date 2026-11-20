"""Reusable presentation for static component detail pages."""
from html import escape

from components import breadcrumb, btn, icon, link, pic

GALLERY_SIZES = '(min-width: 1240px) 620px, (min-width: 900px) 50vw, (min-width: 700px) 470px, 94vw'


def component_intro(name, crumbs, lead, facts, views, advice_url):
    """Render the page opening and the shared keyboard-enabled image viewer."""
    def view_picture(view, sizes, eager=False, decorative=False):
        style = view[3] if len(view) > 3 else ''
        return pic(view[1], '' if decorative else view[2], sizes, eager=eager, style=style)
    tabs = ''.join(
        f'<li><button class="detail-view" type="button" data-thumb="gal-{i}"'
        f'{' aria-current="true"' if i == 0 else ''}>'
        f'{view_picture(view, "72px", decorative=True)}<span>{escape(view[0])}</span></button></li>'
        for i, view in enumerate(views))
    templates = ''.join(
        f'<template id="gal-{i}">{view_picture(view, GALLERY_SIZES)}</template>'
        for i, view in enumerate(views))
    rows = ''.join(f'<div><dt>{escape(label)}</dt><dd>{escape(value)}</dd></div>' for label, value in facts)
    return f'''<div class="detail-sheet">
  <div class="container">
    <div class="detail-crumbs">{breadcrumb(crumbs)}</div>
    <section class="detail-intro" id="overzicht" aria-labelledby="prod-h1">
      <div class="detail-intro__copy">
        <h1 id="prod-h1" class="h1">{escape(name)}</h1>
        <p class="detail-intro__lead">{escape(lead)}</p>
        <div class="detail-intro__actions">{btn("Vraag technisch advies", advice_url, "lg")}{link("Bekijk de werking", "#werking", "down")}</div>
      </div>
      <div class="detail-gallery" data-gallery="lightbox">
        <figure class="detail-plate">
          <div class="detail-plate__image" data-gallery-main>{view_picture(views[0], GALLERY_SIZES, eager=True)}</div>
          <button class="zoom-btn" type="button" data-zoom aria-label="Vergroot afbeelding" aria-haspopup="dialog">{icon("zoom")}</button>
          <figcaption class="detail-plate__caption"><span>Productaanzichten</span><span>Voorbeeld op maat</span></figcaption>
        </figure>
        <ul class="detail-views" style="--views:{len(views)}" aria-label="Kies een productaanzicht">{tabs}</ul>
        {templates}
      </div>
      <dl class="detail-facts">{rows}</dl>
    </section>
  </div>
</div>
<dialog class="lightbox" id="lightbox" aria-label="Productafbeeldingen {escape(name)}">
  <div class="lightbox__inner">
    <div class="lightbox__bar"><span data-lightbox-count aria-live="polite"></span><button class="icon-btn" type="button" data-lightbox-close aria-label="Sluiten" autofocus>{icon("close")}</button></div>
    <div class="lightbox__stage" data-lightbox-stage></div>
    <div class="lightbox__nav"><button class="icon-btn" type="button" data-lightbox-prev aria-label="Vorige afbeelding">{icon("left")}</button><button class="icon-btn" type="button" data-lightbox-next aria-label="Volgende afbeelding">{icon("right")}</button></div>
  </div>
</dialog>'''


def component_nav(items):
    anchors = ''.join(f'<li><a href="#{section}">{escape(label)}</a></li>' for section, label in items)
    return f'''<nav class="subnav detail-nav" aria-label="Op deze pagina" data-scrollspy="162">
  <div class="container"><ul class="subnav__list">{anchors}</ul></div>
</nav>'''


def component_principle(title, intro, image, alt, steps, note, step_heading='Volg de lucht en de deeltjes'):
    """The markers use percentages of the original, uncropped cutaway."""
    markers = ''.join(
        f'<button type="button" class="detail-marker" data-step="{i}" style="--x:{x}%;--y:{y}%" '
        f'aria-label="Stap {i}. {escape(label)}" aria-controls="flow-step-{i}"><span>{i:02}</span></button>'
        for i, (label, _, x, y) in enumerate(steps, 1))
    explanations = [
        f'<details name="component-flow" id="flow-step-{i}" data-step="{i}"{" open" if i == 1 else ""}>'
        f'<summary><span class="detail-step__number" aria-hidden="true">{i:02}</span>'
        f'<span>{escape(label)}</span><span class="detail-step__icon" aria-hidden="true"></span></summary>'
        f'<p>{escape(text)}</p></details>'
        for i, (label, text, _, _) in enumerate(steps, 1)]
    return f'''<section class="section detail-section" id="werking" aria-labelledby="werking-title">
  <div class="container">
    <header class="detail-section__head">
      <h2 id="werking-title" class="h2">{title}</h2>
      <p>{escape(intro)}</p>
    </header>
    <div class="detail-flow" data-component-flow>
      <figure class="detail-flow__figure">
        <div class="detail-flow__canvas">
          <div class="detail-flow__image">
            {pic(image, alt, "(min-width: 900px) 340px, 60vw")}
            {markers}
          </div>
        </div>
        <figcaption><span>Doorsnede</span><span>Werkingsprincipe · niet op schaal</span></figcaption>
      </figure>
      <div class="detail-flow__body">
        <h3 class="h3">{escape(step_heading)}</h3>
        <ol class="detail-flow__steps">{''.join(f'<li>{item}</li>' for item in explanations)}</ol>
        <p class="detail-flow__note">{escape(note)}</p>
      </div>
    </div>
  </div>
</section>'''
