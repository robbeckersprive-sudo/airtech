"""Content review for the client: every Dutch text and photo of the live site in a few Word documents.

    python tools/content_review.py [--out docs/contentreview] [--base https://airtech-eta.vercel.app/]

Run after `python src/build.py`. Reads the built Dutch pages that a visitor can reach from index.html, plus the kiosk,
and writes to <out>/<date>-<hash>/:

    00-open-punten.docx         what Airtechnic must confirm: [TBD] markers, norms and claims, figures, references
    01..05-<part>.docx          all texts in reading order, one chapter per page, each text once (with a fixed ID)
    06-fotobijlage.docx         every photo once: thumbnail, pages, alt text, three checks
    manifest.json               ID -> Dutch text, kind, pages (for reading the corrections back in)

IDs (T0001 ...) are kept in <out>/ids.json, so a text keeps its ID across exports. The documents open with Track
Changes switched on; the client corrects the text column and uses comments for questions.
"""
from pathlib import Path
from html import unescape
import datetime, hashlib, io, json, re, sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import i18n  # noqa: E402

from docx import Document  # noqa: E402
from docx.enum.table import WD_TABLE_ALIGNMENT  # noqa: E402
from docx.enum.text import WD_COLOR_INDEX, WD_BREAK  # noqa: E402
from docx.oxml import OxmlElement  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
from docx.shared import Cm, Pt, RGBColor  # noqa: E402
from PIL import Image  # noqa: E402

ARG = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d  # noqa: E731
OUT = ROOT / ARG('--out', 'docs/contentreview')
BASE = ARG('--base', 'https://airtech-eta.vercel.app/')

GREY = RGBColor(0x80, 0x80, 0x80)
INK = RGBColor(0x1F, 0x23, 0x28)
RED = RGBColor(0xC8, 0x10, 0x2E)

# ------------------------------------------------------------------ pages
def live_pages():
    """Dutch pages reachable from index.html (the design variants and Beheer are not linked)."""
    seen, todo = [], ['index.html']
    while todo:
        p = todo.pop(0)
        if p in seen or not (ROOT / p).is_file():
            continue
        seen.append(p)
        todo += re.findall(r'href="([a-z0-9-]+\.html)', (ROOT / p).read_text(encoding='utf-8'))
    return seen


def html_of(page):
    return (ROOT / page).read_text(encoding='utf-8')


def parts(pages):
    """Five reading parts. Products follow the category page that links them first."""
    def has(p, *pre):
        return p.startswith(pre)
    A = [p for p in ('index.html', 'over-ons.html') if p in pages]
    C = sorted(p for p in pages if has(p, 'sectoren')) + sorted(p for p in pages if has(p, 'project'))
    C.sort(key=lambda p: (not p.startswith('sectoren.'), not p.startswith('sectoren'), p != 'projecten.html', p))
    D = sorted(p for p in pages if has(p, 'kennis'))
    D.sort(key=lambda p: p != 'kennisbank.html')
    B = sorted(p for p in pages if has(p, 'oplossingen'))
    if 'componenten.html' in pages:
        B.append('componenten.html')
    taken = set(A + B + C + D)
    for cat in sorted(p for p in pages if has(p, 'componenten-')):
        B.append(cat)
        taken.add(cat)
        for link in re.findall(r'href="([a-z0-9-]+\.html)', html_of(cat)):
            if link in pages and link not in taken:
                B.append(link)
                taken.add(link)
    B += sorted(p for p in pages if p not in taken and p not in B)
    return [('01', 'Algemeen en navigatie', A), ('02', 'Oplossingen en producten', B),
            ('03', 'Sectoren en projecten', C), ('04', 'Kennisbank', D), ('05', 'Kiosk (beursscherm)', ['kiosk.html'])]


# ------------------------------------------------------------------ segments
BLOCK_KIND = {'h1': 'H1', 'h2': 'H2', 'h3': 'H3', 'h4': 'H4', 'h5': 'H4', 'h6': 'H4', 'li': 'lijst', 'td': 'tabel',
              'th': 'tabel', 'dt': 'term', 'dd': 'tabel', 'figcaption': 'onderschrift', 'button': 'knop',
              'label': 'veld', 'legend': 'veld', 'summary': 'knop', 'blockquote': 'citaat', 'caption': 'tabel'}
SIGNIFICANT = re.compile(r'[A-Za-zÀ-ÖØ-öø-ÿ]{2}|\d')


def walk(html):
    """(segment, kind, in_main) in document order. Same run logic as the translation (i18n._walk), but with context
    and without honouring i18n:skip (those texts need a review as much as the rest)."""
    out = []

    def visit(el, stack):
        if el.name in i18n.NO_TEXT or el.name == 'head':
            return
        run = []

        def flush():
            if not run:
                return
            wrapper = i18n._strip_wrapper(run)
            if wrapper is not None:
                visit(wrapper, stack + [wrapper])
            else:
                text = i18n._text_of(run)
                plain = re.sub(r'<[^>]+>', '', text)
                shown = i18n.norm(unescape(plain))
                if SIGNIFICANT.search(shown) and len(shown) > 1 and not re.fullmatch(r'[\d\W]{1,4}', shown):
                    kind = 'tekst'
                    for a in reversed(stack):
                        if a.name in BLOCK_KIND:
                            kind = BLOCK_KIND[a.name]
                            break
                        if a.name == 'a' or 'btn' in a.cls or 'cta' in a.cls:
                            kind = 'knop'
                            break
                    out.append((i18n.norm(text), kind, any(a.name == 'main' for a in stack)))
            run.clear()

        for k in el.kids:
            if isinstance(k, tuple) and k[0] == '#c':
                flush()
            elif i18n._inline(k):
                run.append(k)
            else:
                flush()
                if isinstance(k, i18n._El):
                    visit(k, stack + [k])
        flush()

    root = i18n._parse(html)
    visit(root, [root])
    return out


def meta(html):
    t = re.search(r'<title>(.*?)</title>', html, re.S)
    d = re.search(r'<meta name="description" content="([^"]*)"', html)
    return (i18n.norm(t.group(1)) if t else ''), (i18n.norm(d.group(1)) if d else '')


def heading(html, page):
    h = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
    return i18n.norm(unescape(re.sub(r'<[^>]+>', ' ', h.group(1)))) if h else page


IMG_ATTR = re.compile(r'(?:src|srcset|data-src|data-srcset|content|href)="([^"]+)"|url\(([^)]+)\)')
VARIANT = re.compile(r'-(?:\d{2,4}w?|leeg-\d+)?(?=\.(?:avif|webp|jpe?g|png)$)')


def images(html):
    """[(base, alt)] for every raster image the page shows: <img>, <source>, CSS backgrounds, og:image."""
    found = {}
    for m in re.finditer(r'<img\b[^>]*>', html):
        tag = m.group()
        src = re.search(r'\ssrc="([^"]+)"', tag)
        alt = re.search(r'\salt="([^"]*)"', tag)
        if src:
            found.setdefault(base_of(src.group(1)), set()).add(i18n.norm(unescape(alt.group(1))) if alt else '')
    for m in IMG_ATTR.finditer(html):
        for part in (m.group(1) or m.group(2) or '').split(','):
            url = part.strip().strip('\'"').split(' ')[0]
            if re.search(r'^(?:images|assets|folders)/.*\.(?:avif|webp|jpe?g|png)$', url):
                found.setdefault(base_of(url), set())
    return found


def base_of(url):
    url = url.split('?')[0].split('#')[0]
    url = re.sub(r'-(\d{3,4})w?(?=\.\w+$)', '', url)
    return re.sub(r'\.(avif|webp|jpe?g|png)$', '', url)


def best_file(base):
    cands = [p for p in ROOT.glob(base + '*') if p.suffix.lower() in ('.webp', '.jpg', '.jpeg', '.png')
             and re.fullmatch(re.escape(Path(base).name) + r'(-\d{3,4}w?)?', p.stem)]
    if not cands:
        return None
    def size(p):
        m = re.search(r'-(\d{3,4})w?$', p.stem)
        return int(m.group(1)) if m else 9999
    small = [p for p in cands if size(p) <= 800]
    return max(small, key=size) if small else min(cands, key=size)


# ------------------------------------------------------------------ open points
CHECKS = [
    ('Te bevestigen', re.compile(r'TBD', re.I), 'Gemarkeerd als nog te bevestigen door Airtechnic.'),
    ('Normen en certificering', re.compile(r'\b(ATEX|EHEDG|FDA|ISO ?\d|NEN|EN ?\d{3,}|NFPA|CE-|2014/34|1999/92|richtlijn|'
                                           r'gecertificeerd|certificaat|certificering|conform|zone ?\d\d?)\b', re.I),
     'Verwijst naar een norm, richtlijn of certificering: klopt dit en mag Airtechnic dit zo stellen?'),
    ('Claims', re.compile(r'\b(garantie|gegarandeerd|uniek|marktleider|enige|altijd|nooit|100 ?%|food-grade|'
                          r'hygiënisch ontwerp|explosievrij|onderhoudsvrij|levenslang)\b', re.I),
     'Stellige bewering: kan Airtechnic dit waarmaken?'),
    ('Getallen en specificaties', re.compile(r'\d[\d.,]*\s?(?:–|-|tot)?\s?\d*[\d.,]*\s?(mm|cm|m³|m3|m/s|m|kW|W|bar|mbar|'
                                             r'Pa|kPa|°C|%|µm|μm|kg|ton|t/h|kg/h|l|liter|jaar|uur|min|rpm|dB)\b'),
     'Bevat een getal of maat: klopt de waarde?'),
]


# ------------------------------------------------------------------ docx helpers
def new_doc(title, subtitle, stamp):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    sec.left_margin = sec.right_margin = Cm(2)
    sec.top_margin, sec.bottom_margin = Cm(1.8), Cm(1.8)
    st = doc.styles['Normal']
    st.font.name, st.font.size = 'Calibri', Pt(10.5)
    st.element.rPr.rFonts.set(qn('w:eastAsia'), 'Calibri')
    for name, size in (('Title', 24), ('Heading 1', 16), ('Heading 2', 12.5), ('Heading 3', 11)):
        s = doc.styles[name]
        s.font.name, s.font.size, s.font.color.rgb = 'Calibri', Pt(size), INK
    # Track Changes on when the document opens
    settings = doc.settings.element
    tr = OxmlElement('w:trackRevisions')
    settings.insert(0, tr)
    # header / footer
    hp = sec.header.paragraphs[0]
    r = hp.add_run(f'Airtechnic · contentreview · {title} · versie {stamp}')
    r.font.size, r.font.color.rgb = Pt(8), GREY
    fp = sec.footer.paragraphs[0]
    r = fp.add_run('Pagina ')
    r.font.size, r.font.color.rgb = Pt(8), GREY
    field(fp, 'PAGE')
    doc.add_paragraph(title, style='Title')
    p = doc.add_paragraph(subtitle)
    p.runs[0].font.color.rgb = GREY
    return doc


def field(par, code):
    r = par.add_run()
    for tag, text in (('begin', None), (None, code), ('end', None)):
        if tag:
            e = OxmlElement('w:fldChar')
            e.set(qn('w:fldCharType'), tag)
        else:
            e = OxmlElement('w:instrText')
            e.set(qn('xml:space'), 'preserve')
            e.text = text
        r._r.append(e)
    r.font.size, r.font.color.rgb = Pt(8), GREY


def shade(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    s = OxmlElement('w:shd')
    s.set(qn('w:val'), 'clear')
    s.set(qn('w:color'), 'auto')
    s.set(qn('w:fill'), hex_fill)
    tcPr.append(s)


def borders(table, color='D9D9D9'):
    tblPr = table._tbl.tblPr
    b = OxmlElement('w:tblBorders')
    for side in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        e = OxmlElement(f'w:{side}')
        e.set(qn('w:val'), 'single' if side in ('insideH', 'top', 'bottom') else 'nil')
        e.set(qn('w:sz'), '4')
        e.set(qn('w:color'), color)
        b.append(e)
    tblPr.append(b)


def widths(table, cms):
    table.autofit = False
    for row in table.rows:
        for cell, w in zip(row.cells, cms):
            cell.width = Cm(w)


def no_split(row):
    trPr = row._tr.get_or_add_trPr()
    e = OxmlElement('w:cantSplit')
    trPr.append(e)


def repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    e = OxmlElement('w:tblHeader')
    trPr.append(e)


INLINE_TOK = re.compile(r'<(/?)(\w+)([^>]*)>|([^<]+)')


def rich(par, html, size=None, bold=False):
    """Inline HTML -> runs: strong/b bold, em/i italic, br line break, span.tbd highlighted, a underlined."""
    state = {'b': 0, 'i': 0, 'u': 0, 'tbd': 0}
    stack = []
    html = re.sub(r'</a>\s*(?=<a\b)', '</a> · ', html)      # adjacent links (menus) read as a list, not one word
    for m in INLINE_TOK.finditer(html):
        close, tag, attrs, text = m.groups()
        if text is not None:
            r = par.add_run(re.sub(r'\s+', ' ', unescape(text)).replace('­', ''))   # soft hyphens: site only
            r.bold = bold or bool(state['b'])
            r.italic = bool(state['i'])
            r.underline = bool(state['u'])
            if state['tbd'] or 'TBD' in text:
                r.font.highlight_color = WD_COLOR_INDEX.YELLOW
            if size:
                r.font.size = Pt(size)
            continue
        tag = tag.lower()
        if tag in ('br', 'wbr'):
            if tag == 'br':
                par.add_run().add_break()
            continue
        key = {'strong': 'b', 'b': 'b', 'em': 'i', 'i': 'i', 'a': 'u'}.get(tag)
        if tag == 'span' and 'tbd' in attrs:
            key = 'tbd'
        if close:
            if stack:
                k = stack.pop()
                if k:
                    state[k] -= 1
        else:
            stack.append(key)
            if key:
                state[key] += 1


KIND_SIZE = {'H1': 15, 'H2': 13, 'H3': 11.5, 'H4': 11}


def text_table(doc):
    t = doc.add_table(rows=0, cols=2)
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    borders(t)
    return t


def text_row(t, sid, kind, html):
    row = t.add_row()
    no_split(row)
    a, b = row.cells
    pa = a.paragraphs[0]
    r = pa.add_run(sid)
    r.font.size, r.font.color.rgb = Pt(7.5), GREY
    r = pa.add_run('\n' + kind)
    r.font.size, r.font.color.rgb = Pt(6.5), GREY
    shade(a, 'F4F4F4')
    if kind == 'lijst':
        b.paragraphs[0].add_run('•  ')
    rich(b.paragraphs[0], html, size=KIND_SIZE.get(kind), bold=kind in KIND_SIZE)
    widths(t, [1.6, 15.4])


def instructions(doc, extra=()):
    doc.add_heading('Zo werkt deze controle', level=1)
    for line in (
        'Wijzigingen bijhouden staat aan. Pas de tekst in de rechterkolom direct aan; Word laat zien wat er verandert.',
        'Heeft u een vraag of twijfel zonder concrete verbetering? Selecteer de tekst en kies Invoegen › Opmerking.',
        'Laat de grijze kolom met het nummer (T0001 …) staan: daarmee zetten wij elke correctie automatisch terug op de site.',
        'Elke tekst staat één keer in dit document, bij de eerste pagina waar hij voorkomt. Menu, voettekst en andere '
        'teksten die op elke pagina staan, vindt u in deel 01.',
        'Geel gemarkeerd = nog te bevestigen door Airtechnic. Die punten staan ook samen in "00 Open punten".',
        'Wilt u de tekst in de context zien? Onder elke paginatitel staat het adres van de testsite.',
        'Engels en Duits zijn vertaald vanuit het Nederlands en volgen na deze ronde; controleer nu alleen het Nederlands.',
        *extra):
        doc.add_paragraph(line, style='List Bullet')


# ------------------------------------------------------------------ main
def main():
    pages = live_pages()
    ids_file = OUT / 'ids.json'
    ids = json.loads(ids_file.read_text(encoding='utf-8')) if ids_file.is_file() else {}

    def sid(text):
        if text not in ids:
            ids[text] = f'T{len(ids) + 1:04d}'
        return ids[text]

    plan = parts(pages)
    data = {}                                   # page -> dict
    for _n, _t, group in plan:
        for page in group:
            html = html_of(page)
            data[page] = {'html': html, 'segs': walk(html), 'meta': meta(html), 'h1': heading(html, page),
                          'imgs': images(html)}

    # where each text occurs (for the manifest and the open points)
    where = {}
    for page, d in data.items():
        for text, _k, _m in d['segs']:
            where.setdefault(text, [])
            if page not in where[text]:
                where[text].append(page)
        for text in d['meta']:
            if text:
                where.setdefault(text, [])
                if page not in where[text]:
                    where[text].append(page)
    shared_count = {}
    for page, d in data.items():
        if page == 'kiosk.html':
            continue
        for text, _k, in_main in d['segs']:
            if not in_main:
                shared_count[text] = shared_count.get(text, 0) + 1

    manifest, shown = {}, set()
    stamp_src = json.dumps(sorted(where), ensure_ascii=False)
    stamp = datetime.date.today().isoformat() + '-' + hashlib.sha1(stamp_src.encode()).hexdigest()[:6]
    folder = OUT / stamp
    folder.mkdir(parents=True, exist_ok=True)

    def record(text, kind, page):
        i = sid(text)
        m = manifest.setdefault(i, {'nl': text, 'kind': kind, 'pages': where.get(text, [page])})
        return i, m

    summary = []
    for num, title, group in plan:
        doc = new_doc(f'{num} {title}', f'{len(group)} pagina\'s · alleen Nederlands · stand van de site op {stamp[:10]}', stamp)
        instructions(doc)
        n_texts = 0
        if num == '01':
            doc.add_page_break()
            doc.add_heading('Op elke pagina: menu, voettekst en vaste blokken', level=1)
            p = doc.add_paragraph('Deze teksten staan buiten de hoofdinhoud en komen op (bijna) alle pagina\'s terug.')
            p.runs[0].font.color.rgb = GREY
            t = text_table(doc)
            for page in pages:
                for text, kind, in_main in walk(html_of(page)):
                    if not in_main and text not in shown:
                        shown.add(text)
                        i, _ = record(text, kind, page)
                        text_row(t, i, kind, text)
                        n_texts += 1
        for page in group:
            d = data[page]
            doc.add_page_break()
            doc.add_heading(d['h1'] if page != 'kiosk.html' else 'Kiosk: teksten op het beursscherm', level=1)
            p = doc.add_paragraph()
            r = p.add_run(BASE + page)
            r.font.size, r.font.color.rgb = Pt(8.5), RED
            t = text_table(doc)
            title_, desc = d['meta']
            for text, kind in ((title_, 'titel'), (desc, 'zoek')):
                if text and text not in shown:
                    shown.add(text)
                    i, _ = record(text, kind, page)
                    text_row(t, i, kind, text)
                    n_texts += 1
            skipped = 0
            for text, kind, in_main in d['segs']:
                if not in_main and page != 'kiosk.html':
                    continue
                if text in shown:
                    skipped += 1
                    continue
                shown.add(text)
                i, _ = record(text, kind, page)
                text_row(t, i, kind, text)
                n_texts += 1
            if skipped:
                p = doc.add_paragraph(f'{skipped} tekst(en) van deze pagina staan al eerder in het document en zijn hier weggelaten.')
                p.runs[0].font.size, p.runs[0].font.color.rgb = Pt(8), GREY
        name = f'{num}-{re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")}.docx'
        doc.add_page_break()
        doc.add_paragraph('Legenda kolom: titel = paginatitel in de browser en Google · zoek = omschrijving in zoekresultaten · '
                          'H1–H4 = kop · knop = knop of link · veld = formulierveld · tabel = tabel of specificatie.').runs[0].font.size = Pt(8)
        doc.save(folder / name)
        summary.append((name, len(group), n_texts))

    # ---------------------------------------------------------------- open points
    doc = new_doc('00 Open punten', 'Wat Airtechnic moet bevestigen voordat de site live gaat', stamp)
    doc.add_heading('Zo werkt dit document', level=1)
    for line in ('Vul per punt de kolom "Antwoord" in: klopt, aanpassen naar …, of schrappen.',
                 'Elke tekst staat ook in het deel waar hij hoort; een antwoord hier is genoeg, wij verwerken het overal.',
                 'Wijzigingen bijhouden staat aan.'):
        doc.add_paragraph(line, style='List Bullet')
    doc.add_heading('Algemene vragen', level=1)
    general = [
        'Sectoren Chemie en Hout: is Airtechnic hier aantoonbaar actief? Zo niet, dan halen wij deze pagina\'s en kioskbladen weg.',
        'Uitvoeringen ATEX / food-grade: per product kan de site tonen of het in ATEX- of food-grade-uitvoering leverbaar is. '
        'Die lijst (docs/uitvoeringen-matrix.csv) is nog leeg en wordt pas getoond als Airtechnic hem invult.',
        'Contactgegevens (adres, telefoon, e-mail, KvK): kloppen ze zoals ze in de voettekst staan (deel 01)?',
    ]
    for p in pages:
        if p.startswith('project-'):
            general.append(f'Project "{data[p]["h1"]}": mag de klant (naam, foto\'s, gegevens) op de site genoemd worden?')
    t = doc.add_table(rows=1, cols=2)
    borders(t)
    for c, h in zip(t.rows[0].cells, ('Vraag', 'Antwoord')):
        c.paragraphs[0].add_run(h).bold = True
        shade(c, 'EDEDED')
    repeat_header(t.rows[0])
    for q in general:
        row = t.add_row()
        no_split(row)
        row.cells[0].paragraphs[0].add_run(q)
    widths(t, [11, 6])
    open_count = len(general)
    for cat, rx, why in CHECKS:
        hits = [(manifest_id, m) for manifest_id, m in manifest.items() if rx.search(re.sub(r'<[^>]+>', '', unescape(m['nl'])))]
        if cat == 'Getallen en specificaties':
            hits = [h for h in hits if h[1]['kind'] not in ('titel', 'zoek')]
        taken = getattr(main, 'taken', set())
        hits = [h for h in hits if h[0] not in taken]
        main.taken = taken | {h[0] for h in hits}
        if not hits:
            continue
        doc.add_page_break()
        doc.add_heading(f'{cat} ({len(hits)})', level=1)
        p = doc.add_paragraph(why)
        p.runs[0].font.color.rgb = GREY
        t = doc.add_table(rows=1, cols=4)
        borders(t)
        for c, h in zip(t.rows[0].cells, ('Nr.', 'Tekst', 'Pagina', 'Antwoord')):
            c.paragraphs[0].add_run(h).bold = True
            shade(c, 'EDEDED')
        repeat_header(t.rows[0])
        for i, m in sorted(hits, key=lambda h: h[0]):
            row = t.add_row()
            no_split(row)
            r = row.cells[0].paragraphs[0].add_run(i)
            r.font.size, r.font.color.rgb = Pt(7.5), GREY
            rich(row.cells[1].paragraphs[0], m['nl'], size=9.5)
            pg = m['pages']
            r = row.cells[2].paragraphs[0].add_run(', '.join(x[:-5] for x in pg[:3]) + (f' +{len(pg) - 3}' if len(pg) > 3 else ''))
            r.font.size = Pt(8)
        widths(t, [1.4, 9.2, 3.2, 3.2])
        open_count += len(hits)
    doc.save(folder / '00-open-punten.docx')
    summary.insert(0, ('00-open-punten.docx', '-', open_count))

    # ---------------------------------------------------------------- photos
    photos = {}
    for page, d in data.items():
        for base, alts in d['imgs'].items():
            e = photos.setdefault(base, {'pages': [], 'alts': set()})
            e['pages'].append(page)
            e['alts'] |= alts
    photos = {b: e for b, e in photos.items() if best_file(b)}
    doc = new_doc('06 Fotobijlage', f'{len(photos)} beelden · elk beeld één keer, met de pagina\'s waar het staat', stamp)
    doc.add_heading('Zo werkt deze bijlage', level=1)
    for line in ('Zet per beeld een kruisje (X) in de kolommen, of laat een opmerking achter.',
                 'Klopt = het beeld toont wat de tekst zegt (juist product, project of sector).',
                 'Rechten = Airtechnic mag dit beeld gebruiken (eigen foto, toestemming klant, of gekocht).',
                 'Personen/logo\'s = er staan geen herkenbare personen of klantlogo\'s op, of er is toestemming.',
                 'Alt-tekst = de beschrijving voor schermlezers en Google; corrigeer die gewoon in de tekst.'):
        doc.add_paragraph(line, style='List Bullet')
    doc.add_page_break()
    t = doc.add_table(rows=1, cols=4)
    borders(t)
    for c, h in zip(t.rows[0].cells, ('Beeld', 'Bestand, pagina\'s en alt-tekst', 'Klopt / Rechten / Personen', 'Opmerking')):
        c.paragraphs[0].add_run(h).bold = True
        shade(c, 'EDEDED')
    repeat_header(t.rows[0])
    order = {p: n for n, p in enumerate(pages + ['kiosk.html'])}
    for base, e in sorted(photos.items(), key=lambda kv: (min(order.get(p, 999) for p in kv[1]['pages']), kv[0])):
        row = t.add_row()
        no_split(row)
        img = Image.open(best_file(base)).convert('RGB')
        img.thumbnail((420, 300))
        buf = io.BytesIO()
        img.save(buf, 'JPEG', quality=78)
        buf.seek(0)
        row.cells[0].paragraphs[0].add_run().add_picture(buf, width=Cm(4.2))
        c = row.cells[1]
        r = c.paragraphs[0].add_run(Path(base).name)
        r.bold, r.font.size = True, Pt(8.5)
        pg = list(dict.fromkeys(e['pages']))
        r = c.add_paragraph().add_run('Op: ' + ', '.join(x[:-5] for x in pg[:6]) + (f' en {len(pg) - 6} andere' if len(pg) > 6 else ''))
        r.font.size, r.font.color.rgb = Pt(8), GREY
        alts = sorted(a for a in e['alts'] if a)
        if not alts:
            r = c.add_paragraph().add_run('Geen alt-tekst (decoratief beeld)')
            r.font.size, r.font.color.rgb, r.italic = Pt(8), GREY, True
        for a in alts:
            i, _ = record(a, 'alt', pg[0])
            p = c.add_paragraph()
            r = p.add_run(i + '  ')
            r.font.size, r.font.color.rgb = Pt(7.5), GREY
            r = p.add_run(a)
            r.font.size = Pt(9)
        p = row.cells[2].paragraphs[0]
        for label in ('[  ] Klopt', '[  ] Rechten', '[  ] Personen/logo\'s'):
            r = p.add_run(label + '\n')
            r.font.size = Pt(9)
        widths(t, [4.6, 6.4, 3.0, 3.0])
    doc.save(folder / '06-fotobijlage.docx')
    summary.append(('06-fotobijlage.docx', '-', len(photos)))

    # ---------------------------------------------------------------- manifest + ids
    (folder / 'manifest.json').write_text(json.dumps({'stamp': stamp, 'base': BASE, 'pages': pages + ['kiosk.html'],
                                                      'texts': manifest}, ensure_ascii=False, indent=1), encoding='utf-8')
    ids_file.write_text(json.dumps(ids, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'{folder}:{len(pages)} live pages + kiosk, {len(manifest)} texts, {len(photos)} photos')
    for name, n_pages, n in summary:
        print(f'  {name:42} pages {n_pages!s:>3}  items {n}')


if __name__ == '__main__':
    main()
