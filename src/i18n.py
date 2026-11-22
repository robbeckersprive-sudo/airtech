"""Meertaligheid (nl / en / de) for the Flow generator and anything else that renders Airtechnic text (kiosk).

Two kinds of tables, both per language:

* ``STRINGS`` (src/i18n_strings.py): keyed UI strings for the chrome every page shares: header, mobile menu,
  footer title block, contact block and form, buttons, aria-labels, ``SIG_LABELS`` and the texts the scripts in
  assets/js/ need (``js_strings()``). Use ``t('key')``.
* Content catalogues (src/locales/en.json, de.json): page content, keyed by the Dutch source segment (gettext
  style: the Dutch text is the msgid). The Dutch data modules stay the single source; ``localize_html()``
  translates a rendered Dutch fragment segment by segment. Use ``tr('Dutch text')`` for a single string.

Pages are written per language: Dutch at the root, English under en/, German under de/ (``SLUGS`` holds the
translated file names). ``components.page()`` calls ``localize_html()``, ``localize_jsonld()`` and
``rewrite_urls()`` when the active language is not Dutch. Missing catalogue entries fall back to Dutch and are
recorded in ``MISSES``; ``python tools/i18n_sync.py`` lists them so they can be translated.

Kiosk / other renderers::

    import i18n
    with i18n.use('de'):
        label = i18n.t('nav.solutions')          # keyed UI string
        text = i18n.tr('Pneumatisch transport')   # content string, Dutch msgid
        html = i18n.localize_html(dutch_fragment)
    i18n.js_strings('en')                         # dict for window.ATI18N
"""
import json
import os
import re
from contextlib import contextmanager
from html import escape, unescape

from i18n_strings import STRINGS
from i18n_slugs import SLUGS

LANGS = ('nl', 'en', 'de')
DEFAULT = 'nl'
NAMES = {'nl': 'Nederlands', 'en': 'English', 'de': 'Deutsch'}
LOCALE = {'nl': 'nl_NL', 'en': 'en_GB', 'de': 'de_DE'}
HTML_LANG = {'nl': 'nl', 'en': 'en', 'de': 'de'}
DIR = {'nl': '', 'en': 'en/', 'de': 'de/'}

SRC = os.path.dirname(os.path.abspath(__file__))
LOCALES = os.path.join(SRC, 'locales')

_state = {'lang': DEFAULT, 'page': None}
MISSES = {lang: {} for lang in LANGS}   # lang -> {msgid: first page it was seen on}


# ---------------------------------------------------------------- language context
def lang():
    return _state['lang']


def set_lang(code):
    if code not in LANGS:
        raise ValueError(f'unknown language {code!r}')
    _state['lang'] = code


@contextmanager
def use(code):
    prev = _state['lang']
    set_lang(code)
    try:
        yield
    finally:
        _state['lang'] = prev


def set_page(nl_filename):
    """The Dutch file name of the page being rendered (language switcher, hreflang, miss report)."""
    _state['page'] = nl_filename


def current_page():
    return _state['page']


# ---------------------------------------------------------------- keyed UI strings
def t(key, code=None, **fmt):
    entry = STRINGS[key]
    text = entry.get(code or lang()) or entry[DEFAULT]
    return text.format(**fmt) if fmt else text


def js_strings(code=None):
    """Strings for assets/js (window.ATI18N). Keys are the part after 'js.'."""
    code = code or lang()
    return {k[3:]: v.get(code) or v[DEFAULT] for k, v in STRINGS.items() if k.startswith('js.')}


# ---------------------------------------------------------------- URLs
def localized(nl_filename):
    return nl_filename in SLUGS


def filename(nl_filename, code=None):
    """File name of a page in a language, relative to that language's directory."""
    code = code or lang()
    if code == DEFAULT or nl_filename not in SLUGS:
        return nl_filename
    return SLUGS[nl_filename][code]


def path(nl_filename, code=None):
    """Site-root-relative path, e.g. 'de/komponenten-zyklone.html' ('' for the Dutch home)."""
    code = code or lang()
    if code != DEFAULT and nl_filename not in SLUGS:
        code = DEFAULT
    name = filename(nl_filename, code)
    if name == 'index.html':
        name = ''
    return DIR[code] + name


def href_from(nl_filename, target, source=None):
    """Relative href from a page in language `source` to page `nl_filename` in language `target`."""
    source = source or lang()
    up = '../' if source != DEFAULT else ''
    if target != DEFAULT and nl_filename not in SLUGS:
        nl_filename = 'index.html'
    name = filename(nl_filename, target)
    if target == source:
        return name
    return up + DIR[target] + name


_REVERSE = {}


def reverse(name, code):
    """Dutch file name for a translated file name (or None)."""
    if not _REVERSE:
        for nl, names in SLUGS.items():
            for c, n in names.items():
                _REVERSE[(c, n)] = nl
    return _REVERSE.get((code, name))


# ---------------------------------------------------------------- content catalogues
_CATALOG = {}


def catalog(code):
    if code not in _CATALOG:
        file = os.path.join(LOCALES, f'{code}.json')
        data = {}
        if os.path.exists(file):
            with open(file, encoding='utf-8') as f:
                data = json.load(f)
        _CATALOG[code] = {norm(k): v for k, v in data.items() if v}
    return _CATALOG[code]


def reload():
    _CATALOG.clear()


_WS = re.compile(r'\s+')
_LETTER = re.compile(r'[A-Za-zÀ-ÖØ-öø-ÿ]{2}')


def norm(s):
    return _WS.sub(' ', s).strip()


def tr(text, code=None, record=True):
    """Translate one Dutch segment (plain text or inline HTML). Unknown segments return the Dutch text."""
    code = code or lang()
    if code == DEFAULT or not text or not _LETTER.search(text):
        return text
    key = norm(text)
    found = catalog(code).get(key)
    if found is None:
        if _skip_text(key):
            return text
        if record:
            MISSES[code].setdefault(key, _state['page'])
        return text
    lead = text[:len(text) - len(text.lstrip())]
    trail = text[len(text.rstrip()):]
    return lead + found + trail


def tr_plain(text, code=None):
    """Translate a plain-text value (attribute, JSON-LD): tries the text as-is and in its HTML-escaped form."""
    code = code or lang()
    if code == DEFAULT or not text or not _LETTER.search(text):
        return text
    cat = catalog(code)
    key = norm(text)
    lead, trail = text[:len(text) - len(text.lstrip())], text[len(text.rstrip()):]
    if key in cat:
        return lead + cat[key] + trail
    esc = norm(escape(text, quote=False))
    if esc in cat:
        return lead + unescape(cat[esc]) + trail
    return tr(text, code)


def tr_title(title, code=None):
    """<title> and og:title: translate each ' | ' part separately."""
    return ' | '.join(tr(part, code) for part in title.split(' | '))


# Segments that are the same in every language: brand, names, codes, units, contact data.
_KEEP = re.compile(r'^(?:Airtechnic(?: Solutions(?: BV)?)?|Solids processing|LinkedIn|Rev\.|TBD|\[TBD[^\]]*\]|'
                   r'[\w.+-]+@[\w.-]+|\+?[\d ()+-]+|[A-Z]{1,4}[ .-]?\d[\w .-]*|[\d.,:×x /–-]+\s?[a-zA-Z³²°%/]{0,6})$')


def _skip_text(key):
    plain = re.sub(r'<[^>]+>', '', unescape(key)).strip()
    return not _LETTER.search(plain) or bool(_KEEP.match(plain))


# ---------------------------------------------------------------- HTML segmentation
_TOKEN = re.compile(r'<!--.*?-->|<script\b.*?</script>|<style\b.*?</style>|<[^>]+>|[^<]+', re.S | re.I)
_TAGNAME = re.compile(r'</?([a-zA-Z][\w:-]*)')
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}
# Phrasing elements that stay inside a translation segment (their tags are copied into the translation).
INLINE = {'em', 'strong', 'b', 'br', 'sup', 'sub', 'small', 'abbr', 'code', 'wbr', 'q', 'mark', 'a', 'time', 'cite', 'dfn'}
INLINE_SPAN = {'tbd'}          # <span class="tbd"> markers stay in the sentence
SKIP_START, SKIP_END = '<!--i18n:skip-->', '<!--/i18n:skip-->'
NO_TEXT = {'script', 'style', 'defs', 'pre'}

# Attributes whose value is shown or read out.
TEXT_ATTRS = ('alt', 'title', 'aria-label', 'placeholder', 'label', 'data-cap', 'data-grp', 'data-hint',
              'data-ct-add', 'data-caption', 'data-label', 'data-title', 'data-name', 'aria-roledescription', 'aria-valuetext')
_ATTR = re.compile(r'(\s)(' + '|'.join(re.escape(a) for a in TEXT_ATTRS) + r')="([^"]*)"')
_META = re.compile(r'(<meta\s+(?:name|property)="(?:description|og:title|og:description|og:image:alt|twitter:title|twitter:description)"\s+content=")([^"]*)(")')


class _El:
    __slots__ = ('name', 'open', 'close', 'kids', 'cls')

    def __init__(self, name, open_tok, cls=''):
        self.name, self.open, self.close, self.kids, self.cls = name, open_tok, '', [], cls


def _parse(html):
    root = _El('#root', '')
    stack = [root]
    for m in _TOKEN.finditer(html):
        tok = m.group()
        if tok.startswith('<'):
            if tok.startswith('<!--') or tok.lower().startswith(('<script', '<style', '<!doctype')):
                stack[-1].kids.append(tok if not tok.startswith('<!--') else ('#c', tok))
                continue
            nm = _TAGNAME.match(tok)
            if not nm:
                stack[-1].kids.append(('#t', tok))
                continue
            name = nm.group(1).lower()
            if tok.startswith('</'):
                # close the nearest matching element (generated HTML is well-formed)
                for i in range(len(stack) - 1, 0, -1):
                    if stack[i].name == name:
                        stack[i].close = tok
                        del stack[i:]
                        break
                continue
            cls = re.search(r'\sclass="([^"]*)"', tok)
            el = _El(name, tok, cls.group(1) if cls else '')
            stack[-1].kids.append(el)
            if name not in VOID and not tok.endswith('/>'):
                stack.append(el)
        else:
            stack[-1].kids.append(('#t', tok))
    return root


def _inline(node):
    if isinstance(node, str):
        return False                      # script/style/doctype
    if isinstance(node, tuple):
        return node[0] == '#t'            # comments break runs
    if node.name == 'span':
        if not (set(node.cls.split()) & INLINE_SPAN):
            return False
    elif node.name not in INLINE:
        return False
    return all(_inline(k) for k in node.kids)


def _ser(node):
    if isinstance(node, str):
        return node
    if isinstance(node, tuple):
        return node[1]
    return node.open + ''.join(_ser(k) for k in node.kids) + node.close


def _text_of(nodes):
    return ''.join(_ser(n) for n in nodes)


def _strip_wrapper(nodes):
    """A run that is one inline element around text: translate only the inside (keeps the catalogue small)."""
    core = [n for n in nodes if not (isinstance(n, tuple) and not n[1].strip())]
    if len(core) == 1 and isinstance(core[0], _El) and core[0].name in INLINE and core[0].kids:
        return core[0]
    return None


def segments(html):
    """Yield the translatable segments of an HTML fragment (for tools: extraction, checks)."""
    out = []
    _walk(_parse(html), lambda s: (out.append(s), s)[1], skip=[False])
    return out


def _walk(el, fn, skip):
    if el.name in NO_TEXT:
        return
    kids, run, new = el.kids, [], []

    def flush():
        if not run:
            return
        text = _text_of(run)
        wrapper = _strip_wrapper(run)
        if wrapper is not None and not skip[0]:
            _walk(wrapper, fn, skip)
            new.extend(run)
        elif not skip[0] and _LETTER.search(re.sub(r'<[^>]+>|&\w+;', '', text)):
            new.append(('#t', fn(text)))
        else:
            new.extend(run)
        run.clear()

    for k in kids:
        if isinstance(k, tuple) and k[0] == '#c':
            flush()
            if k[1] == SKIP_START:
                skip[0] = True
            elif k[1] == SKIP_END:
                skip[0] = False
            new.append(k)
        elif _inline(k):
            run.append(k)
        else:
            flush()
            if isinstance(k, _El):
                _walk(k, fn, skip)
            new.append(k)
    flush()
    el.kids = new


def _translate_attrs(html, code):
    def attr(m):
        return f'{m.group(1)}{m.group(2)}="{escape(tr_plain(unescape(m.group(3)), code))}"'

    def meta(m):
        return m.group(1) + escape(tr_plain(unescape(m.group(2)), code)) + m.group(3)

    def tag(m):
        tok = m.group()
        if tok.startswith(('<!--', '<script', '<style')):
            return tok
        tok = _ATTR.sub(attr, tok)
        return _META.sub(meta, tok) if tok.startswith('<meta') else tok

    return re.sub(r'<!--.*?-->|<script\b.*?</script>|<style\b.*?</style>|<[^>]+>', tag, html, flags=re.S | re.I)


def localize_html(html, code=None):
    """Translate a rendered Dutch fragment: text segments and readable attributes."""
    code = code or lang()
    if code == DEFAULT:
        return html
    root = _parse(html)
    _walk(root, lambda s: tr(s, code), skip=[False])
    out = _text_of(root.kids)
    # attributes too, except inside fragments that were rendered in the target language already (skip())
    parts = re.split(f'({re.escape(SKIP_START)}.*?{re.escape(SKIP_END)})', out, flags=re.S)
    return ''.join(p if p.startswith(SKIP_START) else _translate_attrs(p, code) for p in parts)


def skip(html):
    """Mark a fragment that is already rendered in the active language (keyed UI strings)."""
    return f'{SKIP_START}{html}{SKIP_END}'


# ---------------------------------------------------------------- JSON-LD
_LD_TEXT = {'name', 'description', 'text', 'headline', 'category', 'alternativeName', 'caption', 'about', 'keywords',
            'articleSection', 'abstract', 'disambiguatingDescription', 'slogan'}


def localize_jsonld(obj, site, code=None):
    code = code or lang()
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if k == 'inLanguage':
                out[k] = HTML_LANG[code]
            elif isinstance(v, str) and k in _LD_TEXT:
                out[k] = tr_plain(v, code)
            elif isinstance(v, str) and v.startswith(site + '/'):
                out[k] = localize_abs_url(v, site, code)
            else:
                out[k] = localize_jsonld(v, site, code)
        return out
    if isinstance(obj, list):
        return [localize_jsonld(v, site, code) for v in obj]
    return obj


def localize_abs_url(url, site, code=None):
    code = code or lang()
    rest = url[len(site) + 1:]
    name, sep, frag = rest.partition('#')
    if name == '':
        name = 'index.html'
    if '/' in name or not name.endswith(('.html', '.htm')):
        return url
    if name not in SLUGS:
        return url
    p = path(name, code)
    return f'{site}/{p}{sep}{frag}'


# ---------------------------------------------------------------- URL rewriting for en/ and de/
_ASSET = re.compile(r'(?<![\w/.:-])(assets|images|folders|api)/')
_HREF = re.compile(r'(\s(?:href|data-href|data-sheet-link)=")([a-z0-9][a-z0-9-]*\.html?)((?:\?[^"#]*)?(?:#[^"]*)?)"')


def rewrite_urls(html, code=None):
    """Relative URLs in a page that lives in en/ or de/: assets one level up, page links to the translated file."""
    code = code or lang()
    if code == DEFAULT:
        return html

    def page_link(m):
        name = m.group(2)
        if name in SLUGS:
            target = SLUGS[name][code]
        elif reverse(name, code):
            target = name                  # already translated (rewrite_urls is idempotent)
        else:
            target = '../' + name          # not translated (review pages): the Dutch original
        return f'{m.group(1)}{target}{m.group(3)}"'

    def tag(m):
        tok = m.group()
        if tok.startswith('<!--'):
            return tok
        if tok.lower().startswith(('<script', '<style')):
            # inline scripts / styles: only url(...) and src attributes
            head, sep, rest = tok.partition('>')
            return _ASSET.sub(r'../\1/', head) + sep + re.sub(r'url\((["\']?)(assets|images)/', r'url(\1../\2/', rest)
        tok = _ASSET.sub(r'../\1/', tok)
        return _HREF.sub(page_link, tok)

    return re.sub(r'<!--.*?-->|<script\b.*?</script>|<style\b.*?</style>|<[^>]+>', tag, html, flags=re.S | re.I)


# ---------------------------------------------------------------- head tags + switcher
def alternates(nl_filename, site):
    """hreflang links for a page (reciprocal: every language lists all three plus x-default)."""
    if not localized(nl_filename):
        return ''
    links = [f'<link rel="alternate" hreflang="{HTML_LANG[c]}" href="{site}/{path(nl_filename, c)}">' for c in LANGS]
    links.append(f'<link rel="alternate" hreflang="x-default" href="{site}/{path(nl_filename, DEFAULT)}">')
    return '\n'.join(links) + '\n'


def switcher_items(nl_filename=None, code=None):
    """[(code, label, href, current)] for the language switcher of the page being rendered."""
    code = code or lang()
    nl_filename = nl_filename or _state['page'] or 'index.html'
    return [(c, NAMES[c], href_from(nl_filename, c, code), c == code) for c in LANGS]


def unmark(html):
    return html.replace(SKIP_START, '').replace(SKIP_END, '')


# ---------------------------------------------------------------- headings: discretionary breaks per language
# Headings use `hyphens: manual` (site.css); long compounds get &shy; at their joints. Dutch: components.py.
HEADING_COMPOUNDS = {
    'en': {},
    'de': {
        'zellenradschleuse': 'zellenrad|schleuse', 'zellenradschleusen': 'zellenrad|schleusen',
        'zyklonabscheider': 'zyklon|abscheider', 'vorabscheider': 'vor|abscheider',
        'durchblasschleuse': 'durchblas|schleuse', 'durchfallschleuse': 'durchfall|schleuse',
        'drehkolbengebläse': 'drehkolben|gebläse', 'seitenkanalverdichter': 'seitenkanal|verdichter',
        'radialventilator': 'radial|ventilator', 'ventilatoreinheit': 'ventilator|einheit',
        'patronenfilter': 'patronen|filter', 'schlauchfilter': 'schlauch|filter', 'entlüftungsfilter': 'entlüftungs|filter',
        'filterelement': 'filter|element', 'filterelemente': 'filter|elemente', 'rohrleitungsteile': 'rohrleitungs|teile',
        'förderbogen': 'förder|bogen', 'förderbögen': 'förder|bögen', 'rohrkupplung': 'rohr|kupplung',
        'rohrweiche': 'rohr|weiche', 'entleerstation': 'entleer|station', 'befüllstation': 'befüll|station',
        'dosierstation': 'dosier|station', 'entleergestell': 'entleer|gestell', 'absperrklappe': 'absperr|klappe',
        'quetschventil': 'quetsch|ventil', 'vibrationssieb': 'vibrations|sieb', 'kontrollsieb': 'kontroll|sieb',
        'klassiersieb': 'klassier|sieb', 'trommelsieb': 'trommel|sieb', 'mehrdecksieb': 'mehrdeck|sieb',
        'förderabscheider': 'förder|abscheider', 'staubabsaugung': 'staub|absaugung', 'saugförderung': 'saug|förderung',
        'druckförderung': 'druck|förderung', 'förderleitung': 'förder|leitung', 'schüttgutverarbeitung': 'schüttgut|verarbeitung',
        'lufttechnik': 'luft|technik', 'inbetriebnahme': 'inbetrieb|nahme', 'siloentlüftung': 'silo|entlüftung',
        'abscheidegrad': 'abscheide|grad', 'filterauswahl': 'filter|auswahl', 'auswahlkriterien': 'auswahl|kriterien',
        'funktionsprinzip': 'funktions|prinzip', 'produktfluss': 'produkt|fluss', 'prozessanlage': 'prozess|anlage',
        'verschleißbild': 'verschleiß|bild', 'hochvakuumabsaugung': 'hochvakuum|absaugung', 'absperrorgane': 'absperr|organe',
        'absperrorgan': 'absperr|organ', 'anlagenplanung': 'anlagen|planung', 'projektvorgehen': 'projekt|vorgehen',
    },
}
_HEADING_RE = {}


def heading_breaks(match, code=None):
    code = code or lang()
    words = HEADING_COMPOUNDS.get(code) or {}
    if not words:
        return match.group()
    if code not in _HEADING_RE:
        _HEADING_RE[code] = re.compile('|'.join(sorted(map(re.escape, words), key=len, reverse=True)), re.IGNORECASE)
    rx = _HEADING_RE[code]

    def compound(word):
        text = word.group()
        parts, start = [], 0
        for chunk in words[text.lower()].split('|'):
            parts.append(text[start:start + len(chunk)])
            start += len(chunk)
        return '&shy;'.join(parts)

    return ''.join(part if part.startswith('<') else rx.sub(compound, part)
                   for part in re.split(r'(<[^>]+>)', match.group()))


# ---------------------------------------------------------------- units and numbers next to a unit
# Dutch writes "18.000 m³/u" and "≈ 1,1 t/u" (u = uur). English: 18,000 m³/h, 1.1 t/h; German: 18.000 m³/h, 1,1 t/h.
_UNIT = r'(?:m³|t|kg|l)/[uh]\b|kW\b|m\b'
_NUM_UNIT = re.compile(r'(?<![\d.,])(\d{1,3}(?:\.\d{3})+|\d+,\d{1,2})(?=(?:\s|&nbsp;|<small>|\u2009)*(?:' + _UNIT + r'))')
_PER_HOUR = re.compile(r'(?<=m³/|kg/)u\b|(?<=\bt/)u\b')


def localize_units(html, code=None):
    """Per-hour units and decimal/thousands separators of figures that carry a unit (text and attributes)."""
    code = code or lang()
    if code == DEFAULT:
        return html

    def num(m):
        v = m.group(1)
        return v.replace('.', '\x00').replace(',', '.').replace('\x00', ',') if code == 'en' else v

    parts = re.split(r'(<script\b.*?</script>|<style\b.*?</style>)', html, flags=re.S | re.I)
    out = []
    for p in parts:
        if p.lower().startswith(('<script', '<style')):
            out.append(p)
        else:
            out.append(_PER_HOUR.sub('h', _NUM_UNIT.sub(num, p)))
    return ''.join(out)


def finalize(html, code=None):
    """Last pass over a finished en/de page (build.py): URLs and units, also for markup added after page()."""
    code = code or lang()
    if code == DEFAULT:
        return html
    return localize_units(rewrite_urls(unmark(html), code), code)


def _check_slugs():
    seen = {}
    for nl, names in SLUGS.items():
        for c in ('en', 'de'):
            other = names[c]
            if other in SLUGS and other != nl:
                raise ValueError(f'{c} file name {other} of {nl} collides with a Dutch page')
            if (c, other) in seen:
                raise ValueError(f'duplicate {c} file name {other}')
            seen[(c, other)] = nl


_check_slugs()
