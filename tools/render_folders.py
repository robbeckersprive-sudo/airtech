"""Render product folders to PDF with headless Chromium, then check them.

Usage:  python tools/render_folders.py [slug ...]
Writes folders/<slug>.print.html (via src/folder_page.py) and folders/<slug>.pdf.

Check (the outside judge, PyMuPDF): 4 A4 pages, every font embedded, real (extractable) text,
no broken images, file under 2 MB. A failing check exits non-zero.
Needs: pip playwright (Chromium from %LOCALAPPDATA%/ms-playwright), PyMuPDF.
"""
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from folder_page import build_folders, FOLDER_SLUGS, OUT_DIR  # noqa: E402

MAX_BYTES = 2 * 1024 * 1024


def _chromium():
    """Use an already installed Playwright Chromium if the bundled revision is missing (no download)."""
    if os.environ.get('FOLDER_CHROMIUM'):
        return os.environ['FOLDER_CHROMIUM']
    import glob
    base = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'ms-playwright')
    found = sorted(glob.glob(os.path.join(base, 'chromium-*', 'chrome-win*', 'chrome.exe')),
                   key=lambda f: int(f.split('chromium-')[1].split(os.sep)[0]))
    return found[-1] if found else None


def render(paths):
    from playwright.sync_api import sync_playwright
    out = []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=_chromium())
        page = browser.new_page()
        for html in paths:
            t0 = time.perf_counter()
            page.goto('file:///' + html.replace('\\', '/'), wait_until='networkidle')
            page.evaluate('document.fonts.ready')
            broken = page.evaluate('[...document.images].filter(i => !i.complete || !i.naturalWidth).map(i => i.src)')
            pdf = html.replace('.print.html', '.pdf')
            page.pdf(path=pdf, format='A4', print_background=True, prefer_css_page_size=True, tagged=True, outline=True)
            out.append((pdf, broken, time.perf_counter() - t0))
        browser.close()
    return out


def check(pdf, broken):
    import fitz
    errors = []
    doc = fitz.open(pdf)
    if doc.page_count != 4:
        errors.append(f'{doc.page_count} pages, expected 4')
    for pg in doc:
        w, h = pg.rect.width * 25.4 / 72, pg.rect.height * 25.4 / 72
        if abs(w - 210) > 1 or abs(h - 297) > 1:
            errors.append(f'page {pg.number + 1} is {w:.0f}x{h:.0f} mm')
        if len(pg.get_text().strip()) < 200:
            errors.append(f'page {pg.number + 1} has almost no text')
    fonts = {f[3]: f[1] for pg in doc for f in pg.get_fonts(full=True)}
    unembedded = [name for name, ext in fonts.items() if ext in ('', 'n/a')]
    if unembedded:
        errors.append('fonts not embedded: ' + ', '.join(unembedded))
    size = os.path.getsize(pdf)
    if size > MAX_BYTES:
        errors.append(f'{size / 1024:.0f} KB > 2 MB')
    if broken:
        errors.append('broken images: ' + ', '.join(broken))
    return errors, size, sorted(fonts)


def main():
    slugs = sys.argv[1:] or FOLDER_SLUGS
    failed = False
    for pdf, broken, secs in render(build_folders(slugs)):
        errors, size, fonts = check(pdf, broken)
        print(f'{os.path.relpath(pdf, ROOT)}  {size / 1024:.0f} KB  {secs:.1f}s  fonts: {", ".join(fonts)}')
        for e in errors:
            print('  FAIL', e)
        failed |= bool(errors)
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
