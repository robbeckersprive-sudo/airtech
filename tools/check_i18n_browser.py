"""Headless check of the multilingual build (Meertaligheid), Python Playwright + a local Playwright Chromium.

    python tools/check_i18n_browser.py [--out DIR]

Starts src/serve.py on a free port, then for nl / en / de renders home, a category, a product and a knowledge page
at 1440x900 and 390x844: no console errors, no page errors, no failed same-origin requests, <html lang> correct,
window.ATI18N present. On every page the header language switcher (desktop rail; mobile: Tekenblad menu) is clicked
for each other language and must land on the equivalent page. --out writes a screenshot per page. Exit 1 on failure.
"""
import glob
import os
import socket
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
import i18n  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

PAGES = ['index.html', 'componenten-cyclonen.html', 'cycloonafscheider.html', 'kennis-druk-of-vacuumtransport.html']


def chromium():
    exe = os.environ.get('FOLDER_CHROMIUM')
    if exe:
        return exe
    base = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'ms-playwright')
    found = sorted(glob.glob(os.path.join(base, 'chromium-*', 'chrome-win*', 'chrome.exe')))
    return found[-1] if found else None


def free_port():
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


def url_path(nl, code):
    return '/' + i18n.DIR[code] + i18n.filename(nl, code)


def main():
    out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None
    if out:
        os.makedirs(out, exist_ok=True)
    port = free_port()
    server = subprocess.Popen([sys.executable, os.path.join(ROOT, 'src', 'serve.py'), ROOT, str(port)],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=os.path.join(ROOT, 'src'))
    base = f'http://127.0.0.1:{port}'
    problems = []
    try:
        for _ in range(50):
            try:
                socket.create_connection(('127.0.0.1', port), 0.2).close()
                break
            except OSError:
                time.sleep(0.1)
        with sync_playwright() as pw:
            browser = pw.chromium.launch(executable_path=chromium())
            for name, view, mobile in (('desktop', {'width': 1440, 'height': 900}, False),
                                       ('mobile', {'width': 390, 'height': 844}, True)):
                ctx = browser.new_context(viewport=view, is_mobile=mobile, has_touch=mobile)
                page = ctx.new_page()
                errors = []
                page.on('console', lambda m: errors.append('console: ' + m.text) if m.type == 'error' else None)
                page.on('pageerror', lambda e: errors.append('pageerror: ' + str(e)))
                # ERR_ABORTED = request cancelled by the next navigation (switcher clicks), not a missing file
                page.on('requestfailed', lambda r: errors.append(f'requestfailed: {r.url} {r.failure}')
                        if r.url.startswith(base) and 'ERR_ABORTED' not in (r.failure or '') else None)
                page.on('response', lambda r: errors.append(f'HTTP {r.status}: {r.url}')
                        if r.url.startswith(base) and r.status >= 400 else None)
                for nl in PAGES:
                    for code in i18n.LANGS:
                        errors.clear()
                        target = url_path(nl, code)
                        page.goto(base + target, wait_until='networkidle')
                        page.wait_for_timeout(600)
                        lang = page.evaluate('document.documentElement.lang')
                        has_strings = page.evaluate('!!(window.ATI18N && window.ATI18N.locale)')
                        label = f'[{name}] {target}'
                        if lang != i18n.HTML_LANG[code]:
                            problems.append(f'{label}: lang={lang}')
                        if not has_strings:
                            problems.append(f'{label}: window.ATI18N missing')
                        if out:
                            page.screenshot(path=os.path.join(out, f'{name}-{code}-{i18n.filename(nl, code)}.png'))
                        problems.extend(f'{label}: {e}' for e in errors)
                        # language switcher -> equivalent page in each other language
                        for other in i18n.LANGS:
                            if other == code:
                                continue
                            page.goto(base + target, wait_until='domcontentloaded')
                            if mobile:
                                page.click('[data-hx-burger]')
                                page.wait_for_timeout(900)
                                link = page.locator(f'.lsw--sheet a[hreflang="{other}"]')
                            else:
                                link = page.locator(f'.lsw--rail a[hreflang="{other}"]')
                            link.click()
                            page.wait_for_load_state('domcontentloaded')
                            want = url_path(nl, other)
                            got = page.evaluate('location.pathname')
                            if got != want and not (want.endswith('/index.html') and got == want[:-10]):
                                problems.append(f'{label}: switcher {other} -> {got} (expected {want})')
                ctx.close()
            browser.close()
    finally:
        server.terminate()
    for p in problems:
        print(p)
    print(f'{len(PAGES) * len(i18n.LANGS)} pages x 2 viewports, switcher to every other language: {len(problems)} problem(s)')
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
