"""Validate the kiosk's three languages, templates and offline image inventory.
Run after python src/kiosk_page.py. No browser or external dependencies required.
"""
from pathlib import Path
import json
import re
import sys
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import i18n
import kiosk_page
SITE_ROOT = ROOT / 'dist' if '--dist' in sys.argv else ROOT

class Assets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = set()
        self.templates = 0
        self.faces = 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'template' and 'data-sheet' in attrs:
            self.templates += 1
        if 'data-face' in attrs:
            self.faces += 1
        for key in ('src', 'srcset', 'href'):
            if key in attrs:
                self.urls.add(attrs[key].split('?')[0].split('#')[0])

extra = json.loads((ROOT / 'src/kiosk_strings.json').read_text(encoding='utf-8'))
source = kiosk_page.kiosk_html(kiosk_page.sheets()) + kiosk_page.beheer_html()
errors = []
for code in ('en', 'de'):
    i18n.catalog(code).update({i18n.norm(k): v[code == 'de'] for k, v in extra.items()})
    i18n.localize_html(source, code)
    errors += [f'{code}: missing translation: {key}' for key in i18n.MISSES[code]]
worker = (SITE_ROOT / 'kiosk-sw.js').read_text(encoding='utf-8')
cache_urls = set(json.loads(re.search(r'const URLS = (\[.*?\]);', worker, re.S)[1]))
for code in ('nl', 'en', 'de'):
    suffix = '' if code == 'nl' else '-' + code
    for kind in ('kiosk', 'beheer'):
        name = f'{kind}{suffix}.html'
        html = (SITE_ROOT / name).read_text(encoding='utf-8')
        assert f'<html lang="{code}">' in html
        parser = Assets(); parser.feed(html)
        for url in parser.urls:
            if not url or url.startswith(('https:', 'http:', 'mailto:', 'tel:', 'data:')):
                continue
            if not (SITE_ROOT / url).is_file():
                errors.append(f'{name}: missing asset {url}')
            if url.startswith(('images/', 'assets/')) and url not in cache_urls:
                errors.append(f'{name}: asset not cached {url}')
        if kind == 'kiosk':
            assert parser.templates >= 15 and parser.faces == parser.templates * 3
            print(f'{code}: {parser.templates} sheets, {parser.faces} faces, assets present and cached')
for url in cache_urls:
    if not (SITE_ROOT / url).is_file():
        errors.append(f'Offline cache: missing {url}')
if errors:
    print('\n'.join(errors)); sys.exit(1)
print(f'PASS: complete kiosk translations; {len(cache_urls)} offline files verified.')
