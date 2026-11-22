"""Check the multilingual build (Meertaligheid): run after `python src/build.py`.

    python tools/check_i18n.py

1. Dutch remnants: visible text, readable attributes, <title>/meta and JSON-LD of every en/ and de/ page are scanned
   for Dutch function words and Dutch-only technical terms (names such as "Beek en Donk" are allowed).
2. hreflang: every localized page lists nl/en/de/x-default, all targets exist and list the same set back (reciprocal),
   canonical = its own hreflang URL, <html lang> and og:locale match the language.
3. Language switcher: header rail and mobile sheet link to the equivalent page in each language.
4. Links: every relative href/src/srcset in en/ and de/ resolves to an existing file (fragments and queries ignored).
Exit code 1 on any problem.
"""
import json
import os
import re
import sys
from html import unescape
from urllib.parse import urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
import i18n  # noqa: E402
from components import SITE  # noqa: E402
from i18n_slugs import SLUGS  # noqa: E402

# Words that only Dutch uses (as whole words, case-insensitive). Deliberately no words shared with EN/DE.
NL_WORDS = {
    'de', 'het', 'een', 'van', 'voor', 'met', 'uw', 'wij', 'onze', 'naar', 'niet', 'ook', 'bij', 'wordt', 'worden',
    'zijn', 'deze', 'dit', 'dat', 'hoe', 'welke', 'kunt', 'moet', 'gaat', 'tussen', 'waar', 'wanneer', 'u', 'je',
    'of', 'op', 'aan', 'uit', 'na', 'door', 'tot', 'over', 'nog', 'maar', 'geen', 'meer', 'zo', 'samen', 'ons',
    'bekijk', 'bespreek', 'vraag', 'stel', 'lees', 'ontdek', 'vergelijk', 'kies', 'deel', 'neem', 'geef',
    'luchttechniek', 'cycloon', 'cyclonen', 'zeef', 'zeven', 'sluis', 'doseersluis', 'leiding', 'leidingwerk',
    'afscheider', 'afsluiter', 'uitvoering', 'uitvoeringen', 'oplossing', 'oplossingen', 'componenten', 'kennisbank',
    'projecten', 'werkwijze', 'toepassing', 'toepassingen', 'stofafzuiging', 'transport', 'vacuümtransport',
    'druktransport', 'bedrijf', 'installatie', 'capaciteit', 'luchtdebiet', 'drukverschil', 'opvang', 'afvoer',
    'toevoer', 'trechter', 'bocht', 'koppeling', 'wissel', 'ventilatoren', 'blowers', 'filterzakken', 'patroon',
    'stof', 'lucht', 'product', 'productstroom', 'vrijblijvend', 'privacyverklaring', 'bel', 'mail', 'menu',
}
# Allowed inside text: proper names and the address.
ALLOW = ('Beek en Donk', 'Scherpenbeemd', 'Driessen Food Extrusion', 'Deurne', 'Coperion', 'Flexicon', 'Donaldson',
         'Russell Finex', 'Jenike', 'WAMGROUP', 'Gericke', 'DMN-WESTINGHOUSE', 'SHAPA', 'CAGI', 'Busch', 'VEGA', 'VDL',
         'Airtechnic MIX', 'Mineral Products Association', 'US EPA')
# Words that are Dutch but also correct English/German in context (checked per language).
SHARED = {
    'en': {'product', 'menu', 'mail', 'transport', 'blowers', 'of', 'over', 'door'},
    'de': {'menu', 'mail', 'transport', 'blowers', 'meer', 'ventilatoren', 'je'},
}

TEXT_ATTRS = re.compile(r'\s(?:alt|title|aria-label|placeholder|data-cap|data-grp|data-hint|data-ct-add|data-caption|'
                        r'data-label|data-sig-label)="([^"]*)"')
WORD = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+")

problems = []


def fail(msg):
    problems.append(msg)


def visible_text(html):
    body = re.sub(r'<script\b(?![^>]*ld\+json).*?</script>|<style\b.*?</style>', ' ', html, flags=re.S | re.I)
    body = re.sub(r'<nav class="lsw\b.*?</nav>', ' ', body, flags=re.S)   # language switcher: NL / EN / DE names
    body = re.sub(r'<link\b[^>]*>', ' ', body)
    attrs = ' '.join(unescape(a) for a in TEXT_ATTRS.findall(body))
    metas = ' '.join(unescape(m) for m in re.findall(r'<meta\s+(?:name|property)="(?:description|og:title|og:description)"\s+content="([^"]*)"', body))
    ld = []
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        def walk(o):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k in ('name', 'description', 'text', 'headline', 'category') and isinstance(v, str):
                        ld.append(v)
                    else:
                        walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(json.loads(block))
    text = re.sub(r'<script\b.*?</script>', ' ', body, flags=re.S)
    text = unescape(re.sub(r'<[^>]+>', ' ', text)).replace('­', '')
    return ' '.join((text, attrs, metas, ' '.join(ld)))


def dutch_hits(text, code):
    for name in ALLOW:
        text = text.replace(name, ' ')
    text = re.sub(r'\[TBD[^\]]*\]', ' ', text)
    shared = SHARED.get(code, set())
    hits = {}
    for w in WORD.findall(text):
        lw = w.lower()
        if lw in NL_WORDS and lw not in shared:
            hits[lw] = hits.get(lw, 0) + 1
    return hits


def page_file(nl, code):
    return os.path.join(ROOT, i18n.DIR[code] + i18n.filename(nl, code))


def check_page(nl, code):
    file = page_file(nl, code)
    if not os.path.exists(file):
        fail(f'[{code}] missing page {os.path.relpath(file, ROOT)}')
        return
    html = open(file, encoding='utf-8').read()
    rel = os.path.relpath(file, ROOT).replace('\\', '/')
    # lang + og:locale
    if f'<html lang="{i18n.HTML_LANG[code]}"' not in html:
        fail(f'{rel}: <html lang> is not "{code}"')
    if f'<meta property="og:locale" content="{i18n.LOCALE[code]}">' not in html:
        fail(f'{rel}: og:locale is not {i18n.LOCALE[code]}')
    # hreflang
    alts = dict(re.findall(r'<link rel="alternate" hreflang="([\w-]+)" href="([^"]+)">', html))
    want = {i18n.HTML_LANG[c]: f'{SITE}/{i18n.path(nl, c)}' for c in i18n.LANGS}
    want['x-default'] = f'{SITE}/{i18n.path(nl, i18n.DEFAULT)}'
    if alts != want:
        fail(f'{rel}: hreflang set differs: {alts}')
    canon = re.search(r'<link rel="canonical" href="([^"]+)">', html)
    if not canon or canon.group(1) != want[i18n.HTML_LANG[code]]:
        fail(f'{rel}: canonical {canon and canon.group(1)} != {want[i18n.HTML_LANG[code]]}')
    for c, url in alts.items():
        rest = url[len(SITE) + 1:]
        target = os.path.join(ROOT, rest + 'index.html' if (not rest or rest.endswith('/')) else rest)
        if not os.path.exists(target):
            fail(f'{rel}: hreflang {c} target missing: {url}')
    # language switcher (rail + sheet)
    for nav in re.findall(r'<nav class="lsw lsw--\w+"[^>]*>(.*?)</nav>', html, re.S):
        links = dict((c, h) for h, c in re.findall(r'<a href="([^"]+)" hreflang="(\w+)"', nav))
        for c in i18n.LANGS:
            href = links.get(c)
            expect = os.path.normpath(page_file(nl, c))
            got = os.path.normpath(os.path.join(os.path.dirname(file), href or ''))
            if got != expect:
                fail(f'{rel}: switcher {c} -> {href} (expected {os.path.relpath(expect, ROOT)})')
    if html.count('class="lsw lsw--') != 2:
        fail(f'{rel}: expected 2 language switchers (rail + menu)')
    # links
    if code != i18n.DEFAULT:
        for attr, value in re.findall(r'\s(href|src|action|data-rotor-src|data-sheet-href|data-glass)="([^"]*)"', html):
            check_link(rel, file, value)
        for value in re.findall(r'\s(?:srcset|imagesrcset)="([^"]*)"', html):
            for part in value.split(','):
                check_link(rel, file, part.strip().split(' ')[0])
        hits = dutch_hits(visible_text(html), code)
        if hits:
            fail(f'{rel}: Dutch words: ' + ', '.join(f'{w}×{n}' for w, n in sorted(hits.items(), key=lambda kv: -kv[1])))


def check_link(rel, file, value):
    if not value or value.startswith(('#', 'http:', 'https:', 'mailto:', 'tel:', 'data:', 'javascript:')):
        return
    path = urlsplit(value).path
    if not path:
        return
    target = os.path.normpath(os.path.join(os.path.dirname(file), unescape(path)))
    if path.startswith('/'):
        target = os.path.normpath(os.path.join(ROOT, path.lstrip('/')))
    if 'api' + os.sep + 'contact' in target:
        return                                          # serverless endpoint, not a file
    if not os.path.exists(target):
        fail(f'{rel}: broken link {value}')


def main():
    for nl in SLUGS:
        for code in i18n.LANGS:
            check_page(nl, code)
    for p in problems:
        print(p)
    pages = len(SLUGS) * len(i18n.LANGS)
    print(f'{pages} pages checked ({len(SLUGS)} per language): {len(problems)} problem(s)')
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
