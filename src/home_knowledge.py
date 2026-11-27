"""Home blocks 6 and 7 (Nov 21). Styles appended to assets/css/home-blocks.css ("BLOCK 6" / "BLOCK 7"),
behaviour assets/js/home-knowledge.js.

Block 6 "Vraagbaak" — the knowledge articles are written as shop-floor questions, so the block shows all nine as an
editorial index (number, question, topic) instead of three cards. Topic chips filter the index; on a fine pointer a
preview plate of the article follows the cursor. Phones: rows with a thumbnail, chips scroll sideways.

Block 7 "Vragen" — the FAQ as a numbered index (one answer open at a time, `details name`), smooth opening where the
browser supports it, and a sticky "Staat uw vraag er niet bij?" card with the contact action and phone number.
Copy: article names / descriptions from knowledge_data; FAQ items from pages.home()."""
import re
from components import pic, icon, link, split_lines, faq, PHONE_TEL, PHONE_DISPLAY, EMAIL, _v
from knowledge_data import ARTICLES

TOPICS = [('lucht', 'Lucht &amp; filtratie'), ('transport', 'Transport &amp; dosering'), ('bulk', 'Scheiden &amp; lossen'),
          ('veiligheid', 'Veiligheid &amp; hygiëne')]
TOPIC_OF = {
    'wanneer-filters-vervangen': 'lucht', 'juiste-blower-selecteren': 'lucht', 'cycloon-als-voorafscheider': 'lucht',
    'silo-ontluchting-pneumatisch-vullen': 'lucht', 'slijtage-transportbochten': 'transport',
    'doorvalsluis-of-doorblaassluis': 'transport', 'controlezeef-of-fractioneerzeef': 'bulk',
    'bigbag-lossen-onregelmatige-productstroom': 'bulk', 'atex-explosieveiligheid': 'veiligheid',
}
# the comparison article lives on its own template (pages.artikel)
LEAD = ('Druk- of vacuümtransport?', 'kennis-druk-of-vacuumtransport.html', '01-hero-pijpleiding',
        'Vergelijk druk- en vacuümtransport voor poeders, granulaat en pellets.', 'transport')


def _first_sentence(text):
    text = re.sub(r'<[^>]+>', '', text)
    m = re.match(r'(.+?[.!?])(\s|$)', text)
    return m.group(1) if m else text


def kennis_block():
    entries = [LEAD] + [(v['name'], f'kennis-{k}.html', v['image'], _first_sentence(v['description']), TOPIC_OF.get(k, 'lucht'))
                        for k, v in ARTICLES.items()]
    label = dict(TOPICS)
    rows, previews = [], []
    for i, (name, href, img, desc, topic) in enumerate(entries):
        rows.append(f'''<li class="kq-row" data-topic="{topic}" style="--i:{i}"><a class="kq-link" href="{href}" data-kq="{i}">
          <span class="kq-no" aria-hidden="true">K.{i + 1:02d}</span>
          <span class="kq-txt"><span class="kq-q">{name}</span><span class="kq-d">{desc}</span></span>
          <span class="kq-topic">{label[topic]}</span>
          <span class="kq-thumb" aria-hidden="true">{pic(img, "", "72px")}</span>{icon("ur")}</a></li>''')
        previews.append(f'<span class="kq-prev__img" data-kq-img="{i}">{pic(img, "", "320px")}</span>')
    chips = (f'<button type="button" class="kq-chip" aria-pressed="true" data-kq-topic="all">Alles <small>{len(entries)}</small></button>'
             + ''.join(f'<button type="button" class="kq-chip" aria-pressed="false" data-kq-topic="{k}">{t} '
                       f'<small>{sum(1 for e in entries if e[4] == k)}</small></button>' for k, t in TOPICS))
    return f'''<section class="section--home kq" aria-labelledby="kennis-title" data-kq-root>
  <div class="container kq-in">
    <div class="kq-side">
      <h2 id="kennis-title" class="h2" data-split>{split_lines("Kennis die uw proces<br><em>verder brengt.</em>")}</h2>
      <p class="kq-intro">Praktische antwoorden op vragen uit de fabriekshal: van slijtende bochten tot een silo die niet ontlucht.</p>
      <div class="kq-chips" role="group" aria-label="Filter op onderwerp">{chips}</div>
      {link("Bekijk de volledige kennisbank", "kennisbank.html", "ur", "kq-all")}
    </div>
    <div class="kq-main">
      <ol class="kq-list" data-kq-list>{"".join(rows)}</ol>
      <p class="kq-empty" hidden data-kq-empty>Geen artikelen in dit onderwerp.</p>
    </div>
  </div>
  <div class="kq-prev" aria-hidden="true" data-kq-prev>{"".join(previews)}</div>
</section>'''


def faq_block(items, title="Veelgestelde vragen over<br><em>uw procesinstallatie.</em>", card=True, cls="section--home"):
    """Also used by category_page (card=False: the contact block follows right after)."""
    acc = faq(items, True).replace('<details class="faq__item"', '<details class="faq__item" name="faq-index"')
    card_html = (f'''<div class="fq-card">
        <p class="fq-card__k"><span class="fq-card__dot" aria-hidden="true"></span>Staat uw vraag er niet bij?</p>
        <p class="fq-card__t">Vertel ons wat u verwerkt en wat u wilt bereiken.</p>
        <a class="btn fq-card__btn" href="#contact"><span class="btn__label">Stel uw vraag</span><span class="btn__icon" aria-hidden="true">{icon("ur")}{icon("ur", "btn__icon-2")}</span></a>
        <p class="fq-card__alt"><a href="tel:{PHONE_TEL}">{icon("phone")}<span>{PHONE_DISPLAY}</span></a><a href="mailto:{EMAIL}">{icon("mail")}<span>{EMAIL}</span></a></p>
      </div>''' if card else '')
    return f'''<section class="{cls} fq" aria-labelledby="faq-title">
  <div class="container fq-in">
    <div class="fq-side">
      <h2 id="faq-title" class="h2" data-split>{split_lines(title)}</h2>
      {card_html}
    </div>
    <div class="fq-main">{acc}</div>
  </div>
</section>
<script src="{_v("assets/js/home-knowledge.js")}" defer></script>'''
