// Mobile text audit (Nov 22): node tools/mobile_text_audit.js [verbose] with the dev server on :5186; needs playwright-core and a Playwright Chromium (chromium-1169). Pass = all counters 0.
const { chromium } = require('playwright-core');
const path = require('path');
const PAGES = ['index.html', 'componenten.html', 'componenten-filters.html', 'patroonfilter.html', 'kennis-druk-of-vacuumtransport.html',
  'kennisbank.html', 'projecten.html', 'project-pet-recycling.html', 'over-ons.html', 'oplossingen-pneumatisch-transport.html'];
(async () => {
  const verbose = process.argv[2] === 'verbose';
  const b = await chromium.launch({ executablePath: path.join(process.env.LOCALAPPDATA, 'ms-playwright', 'chromium-1169', 'chrome-win', 'chrome.exe') });
  const tot = { clipped: 0, offscreen: 0, rowCut: 0, smallInput: 0, tiny: 0 };
  for (const w of [360, 390]) {
    const p = await b.newPage({ viewport: { width: w, height: 800 }, isMobile: true, hasTouch: true });
    for (const pg of PAGES) {
      await p.goto('http://localhost:5186/' + pg, { waitUntil: 'networkidle' });
      const H = await p.evaluate(() => document.body.scrollHeight);
      for (let y = 0; y < H; y += 700) { await p.evaluate(y => window.scrollTo(0, y), y); await p.waitForTimeout(60); }
      await p.waitForTimeout(400);
      const r = await p.evaluate(() => {
        const vw = document.documentElement.clientWidth, out = { clipped: [], offscreen: [], rowCut: [], smallInput: [], tiny: [] };
        const vis = e => { const cs = getComputedStyle(e); for (let a = e; a; a = a.parentElement) { if (getComputedStyle(a).clipPath === 'inset(50%)') return false; } return cs.visibility !== 'hidden' && cs.display !== 'none' && e.getClientRects().length && !e.closest('[hidden],[inert],[aria-hidden="true"],dialog:not([open]),.mnav,.sr-only,.visually-hidden,template'); };
        const label = e => (e.tagName + '.' + String(e.className).split(' ')[0] + ' "' + e.textContent.trim().slice(0, 30) + '"');
        const texts = [...document.querySelectorAll('main *, footer *')].filter(e => [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && vis(e));
        texts.forEach(e => {
          const r = e.getBoundingClientRect(); if (!r.width) return;
          const cs = getComputedStyle(e);
          if (parseFloat(cs.fontSize) < 11 && !/mono/i.test(cs.fontFamily)) out.tiny.push(label(e));
          if (cs.textOverflow === 'ellipsis' && e.scrollWidth > e.clientWidth + 1 && !e.title && !e.closest('[title]')) out.clipped.push('ellipsis-no-title ' + label(e));
          // walk up to the first clipping ancestor
          for (let a = e.parentElement; a && a !== document.body; a = a.parentElement) {
            const s = getComputedStyle(a), ox = s.overflowX;
            if (ox === 'visible') continue;
            const ar = a.getBoundingClientRect();
            const scroller = (ox === 'auto' || ox === 'scroll') && a.scrollWidth > a.clientWidth + 1;
            if (scroller) {
              const fade = (s.maskImage && s.maskImage !== 'none') || (s.webkitMaskImage && s.webkitMaskImage !== 'none');
              if (r.left < ar.right - 1 && r.right > ar.right + 1 && !fade) out.rowCut.push(label(e));
            } else if (r.right > ar.right + 1.5 || r.left < ar.left - 1.5) {
              if (!a.closest('.ds-stage,.cx-plate,.sx-insp,.wk-frame,.pd-stage,.mnav,.kq-prev')) out.clipped.push(label(e) + ' in ' + a.className.split(' ')[0]);
            }
            break;
          }
          if (r.right > vw + 1 && getComputedStyle(e).position !== 'fixed') {
            let inScroll = false;
            for (let a = e.parentElement; a; a = a.parentElement) { const ox = getComputedStyle(a).overflowX; if (ox === 'auto' || ox === 'scroll' || ox === 'hidden' || ox === 'clip') { inScroll = true; break; } }
            if (!inScroll) out.offscreen.push(label(e));
          }
        });
        document.querySelectorAll('input:not([type=hidden]):not([type=checkbox]):not([type=radio]), textarea, select').forEach(i => {
          if (vis(i) && parseFloat(getComputedStyle(i).fontSize) < 16) out.smallInput.push(i.id || i.name);
        });
        return out;
      });
      const n = k => r[k].length;
      Object.keys(tot).forEach(k => tot[k] += n(k));
      const line = Object.keys(tot).map(k => k + ':' + n(k)).join(' ');
      if (verbose || Object.keys(tot).some(k => n(k))) console.log(w, pg.padEnd(42), line, verbose ? JSON.stringify(Object.fromEntries(Object.keys(tot).map(k => [k, [...new Set(r[k])].slice(0, 4)]))) : '');
    }
    await p.close();
  }
  console.log('TOTAL', JSON.stringify(tot));
  await b.close();
})();
