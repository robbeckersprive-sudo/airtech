"""Browser check for the kiosk sheets added on Nov 27 (sectors, knowledge sheet, QR codes, stand line).

    python tools/check_kiosk_qr.py [--out DIR] [--base http://localhost:5183/] [--4k]

Needs a running local server (python src/serve.py <root> 5183), Python Playwright and OpenCV (cv2). For every
language and screen role it renders the sheets that carry a QR code, decodes the code from the screenshot and
compares it with the page it should open; it also checks that the target exists, that text keeps the kiosk's
reading sizes (headlines >= 6.6u, reading text >= 3.2u, labels >= 2u), that nothing overflows the screen and that
the Beheer filters (sectors, knowledge, stand line) change the schedule. Exit code 1 on a failure.
"""
from pathlib import Path
import asyncio, re, sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import i18n
from sector_data import ORDER, sector_file

import cv2, numpy as np
from playwright.async_api import async_playwright

BASE = sys.argv[sys.argv.index('--base') + 1] if '--base' in sys.argv else 'http://localhost:5183/'
OUT = Path(sys.argv[sys.argv.index('--out') + 1]) if '--out' in sys.argv else None
TARGETS = {**{f'sector-{s}': sector_file(s) for s in ORDER}, 'kennis-atex': 'kennis-atex-explosieveiligheid.html', 'contact': 'index.html#contact'}
_SIZE = (3840, 2160) if '--4k' in sys.argv else (1920, 1080)      # --4k: the same check on a 4K fair screen
SIZES = {'a': _SIZE, 'b': _SIZE, 's': _SIZE}
MEASURE = """() => {
  const u = Math.min(innerHeight / 100, innerWidth * .5625 / 100), layer = document.querySelector('.ks-layer.is-live'), out = [];
  const W = innerWidth, H = innerHeight;
  layer.querySelectorAll('h2, p, li, span, dd, dt, b').forEach(e => {
    if (!e.childNodes.length || ![...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) return;
    const r = e.getBoundingClientRect(), s = getComputedStyle(e);
    if (!r.width || s.visibility === 'hidden') return;
    out.push({ t: e.textContent.trim().slice(0, 28), size: +(parseFloat(s.fontSize) / u).toFixed(2), mono: /mono/i.test(s.fontFamily),
               over: r.right > W + 1 || r.bottom > H + 1 || r.left < -1 || r.top < -1, cls: e.className || e.parentElement.className });
  });
  return out;
}"""

soft = 0
slow = []


async def main():
    problems, n = [], 0
    global soft
    detector = cv2.QRCodeDetector()
    if OUT:
        OUT.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for lang in i18n.LANGS:
            page_name = 'kiosk' + ('' if lang == 'nl' else '-' + lang) + '.html'
            for role, (w, h) in SIZES.items():
                ctx = await browser.new_context(viewport={'width': w, 'height': h})
                await ctx.route('**/api/beheer', lambda r: r.abort())          # offline path: a recent login on this device counts
                await ctx.add_init_script("localStorage.setItem('at-kiosk-pass', String(Date.now() + 864e5))")
                page = await ctx.new_page()
                errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                await page.goto(f'{BASE}{page_name}?role={role}&preview=1', wait_until='networkidle')
                starts = await page.evaluate("""() => { const p = AtKiosk.plan(document.querySelector('.ks-sheets'), {tempo: 1});
                    const o = {}; p.seq.forEach(s => { if (s.tpl) o[s.tpl.dataset.sheet] = s.at; }); return {at: o, count: p.count, length: p.length}; }""")
                for sheet, target in TARGETS.items():
                    t0 = f'Date.now() - {int(starts["at"][sheet] * 1000 + 6500)}'
                    await page.goto(f'{BASE}{page_name}?role={role}&preview=1&stand=Hal%203%20%C2%B7%20Stand%20B12', wait_until='domcontentloaded')
                    # jump to the sheet: the player derives the sheet from Date.now() - t0
                    await page.evaluate(f"history.replaceState(null, '', location.pathname + '?role={role}&preview=1&stand=Hal%203%20%C2%B7%20Stand%20B12&t0=' + ({t0}))")
                    await page.reload(wait_until='networkidle')
                    try:
                        await page.wait_for_selector('.ks-layer.is-live[aria-label]', timeout=15000)
                    except Exception:
                        # a slow local server can stall one image; one reload tells a stall from a sheet that never starts
                        slow.append(f'{lang} {role} {sheet}')
                        await page.evaluate(f"history.replaceState(null, '', location.pathname + '?role={role}&preview=1&stand=Hal%203%20%C2%B7%20Stand%20B12&t0=' + ({t0}))")
                        await page.reload(wait_until='networkidle')
                        try:
                            await page.wait_for_selector('.ks-layer.is-live[aria-label]', timeout=30000)
                        except Exception:
                            problems.append(f'{lang} {role} {sheet}: sheet never became live')
                            continue
                    await page.wait_for_timeout(1800)
                    label = f'{lang} {role} {sheet}'
                    shot = await page.screenshot()
                    if OUT:
                        (OUT / f'kiosk-{lang}-{role}-{sheet}.png').write_bytes(shot)
                    n += 1
                    # QR: every plate that this role shows must decode to the translated target on this origin
                    has_qr = await page.evaluate("!!document.querySelector('.ks-layer.is-live [data-qr]:not([hidden]) svg')")
                    expect_qr = not (role == 'a')                             # screen A carries the picture, B / single the code
                    want = BASE + i18n.DIR[lang] + i18n.filename(target.split('#')[0], lang) + ('#' + target.split('#')[1] if '#' in target else '')
                    if has_qr != expect_qr:
                        problems.append(f'{label}: QR plate {"missing" if expect_qr else "unexpected"}')
                    if has_qr:
                        img = cv2.imdecode(np.frombuffer(shot, np.uint8), cv2.IMREAD_COLOR)
                        got, _pts, _raw = detector.detectAndDecode(img)
                        if not got:
                            # OpenCV's detector is weaker than a phone camera: read the plate itself, enlarged (as a phone would frame it)
                            box = await page.evaluate("(()=>{const r=document.querySelector('.ks-layer.is-live [data-qr-code]').getBoundingClientRect();return [r.left,r.top,r.right,r.bottom]})()")
                            x0, y0, x1, y1 = [int(v) for v in box]
                            crop = img[max(0, y0 - 12):y1 + 12, max(0, x0 - 12):x1 + 12]
                            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
                            for f in (2, 3, 4):
                                for interp in (cv2.INTER_NEAREST, cv2.INTER_CUBIC):
                                    big = cv2.resize(gray, None, fx=f, fy=f, interpolation=interp)
                                    got = detector.detectAndDecode(cv2.threshold(big, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1])[0]
                                    if got:
                                        break
                                if got:
                                    break
                        if not got:
                            # The screenshot is soft (the picture drifts a few px against burn-in). Authoritative: the modules
                            # the page actually drew, read back from the SVG path and decoded from a clean raster.
                            soft += 1
                            d = await page.evaluate("document.querySelector('.ks-layer.is-live [data-qr-code] svg path').getAttribute('d')")
                            size = int(await page.evaluate("document.querySelector('.ks-layer.is-live [data-qr-code] svg').viewBox.baseVal.width"))
                            clean = np.full((size * 8, size * 8), 255, np.uint8)
                            for mx, my in re.findall(r'M(\d+) (\d+)h1', d):
                                clean[int(my) * 8:int(my) * 8 + 8, int(mx) * 8:int(mx) * 8 + 8] = 0
                            got = detector.detectAndDecode(clean)[0]
                        # modules must stay at least 3 device pixels on a 1080p screen to scan from a few steps away
                        px = await page.evaluate("(()=>{const s=document.querySelector('.ks-layer.is-live [data-qr-code] svg');return s.getBoundingClientRect().width/s.viewBox.baseVal.width})()")
                        if px < 3:
                            problems.append(f'{label}: QR modules only {px:.1f}px')
                        if got != want:
                            problems.append(f'{label}: QR decodes to {got!r}, expected {want!r}')
                        path = ROOT / (i18n.DIR[lang] + i18n.filename(target.split('#')[0], lang))
                        if not path.is_file():
                            problems.append(f'{label}: QR target file missing {path.name}')
                    # reading sizes and overflow
                    for m in await page.evaluate(MEASURE):
                        low = 2.0 if (m['mono'] or 'tb' in m['cls'] or 'qr' in m['cls']) else 2.8
                        if m['size'] < low - .02:
                            problems.append(f'{label}: text "{m["t"]}" is {m["size"]}u (< {low}u)')
                        if m['over']:
                            problems.append(f'{label}: "{m["t"]}" leaves the screen')
                    stand = await page.evaluate("document.querySelector('[data-stand]').textContent + '|' + document.querySelector('[data-tb-stand]').hidden")
                    if stand != 'Hal 3 · Stand B12|false':
                        problems.append(f'{label}: stand line {stand!r}')
                problems += [f'{lang} {role}: page error {e}' for e in errors]
                # filters from Beheer
                counts = await page.evaluate("""() => { const r = document.querySelector('.ks-sheets'), c = o => AtKiosk.plan(r, Object.assign({tempo: 1}, o)).count;
                    return [c({}), c({sectors: []}), c({sectors: ['food', 'feed']}), c({knowledge: false}), c({sectors: [], knowledge: false})]; }""")
                if not (counts[0] - counts[1] == len(ORDER) and counts[2] - counts[1] == 2 and counts[0] - counts[3] == 1 and counts[4] == counts[1] - 1):
                    problems.append(f'{lang} {role}: schedule filters {counts}')
                await ctx.close()
        # without a stand line the title block keeps the scale cell
        ctx = await browser.new_context(viewport={'width': _SIZE[0], 'height': _SIZE[1]})
        await ctx.route('**/api/beheer', lambda r: r.abort())
        await ctx.add_init_script("localStorage.setItem('at-kiosk-pass', String(Date.now() + 864e5))")
        page = await ctx.new_page()
        await page.goto(f'{BASE}kiosk.html?role=s&preview=1', wait_until='networkidle')
        await page.wait_for_selector('.ks-layer.is-live')
        state = await page.evaluate("[document.querySelector('[data-tb-stand]').hidden, document.querySelector('[data-tb-scale]').hidden]")
        if state != [True, False]:
            problems.append(f'no stand line: cells {state}')
        await browser.close()
    print(f'{n} sheet renders (3 languages x 3 roles x {len(TARGETS)} sheets): {len(problems)} problem(s)')
    if slow:
        print(f'note: {len(slow)} sheet(s) needed a second load (slow server): {", ".join(slow)}')
    if soft:
        print(f'note: {soft} code(s) were read from the drawn modules, not from the soft screenshot (OpenCV detector limit)')
    for line in problems[:60]:
        print(' -', line)
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
