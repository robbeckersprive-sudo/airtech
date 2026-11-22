/* Site signature (review concepts, Nov 20): one line that runs through every page and ties the content blocks together.
   html[data-sig="a"]  "Hartlijn"   a drawing's centre axis in the left margin: dash-dot hairline, orthogonal turn off the
                                    hero's tab rule, a datum point + leader + vertical label per section.
   html[data-sig="b"]  "Stroomlijn" a streamline: peels off the tab rule in one long curve, runs down the margin and swings
                                    in to touch every section head; a granule rides the drawn tip with a short fading tail.
   Geometry is measured from the DOM (hero tab rule, content edge, section heads, dark bands) and redrawn on resize.
   Scroll draws the line to ~62% of the viewport (the same tip as the hero/process motion). Reduced motion: fully drawn. */
(function () {
  'use strict';
  var L = function (k, nl, v) { var s = (window.ATI18N || {})[k] || nl; return v ? s.replace(/\{(\w+)\}/g, function (_, n) { return v[n]; }) : s; };
  var root = document.documentElement, V = root.getAttribute('data-sig');
  if (!V || !document.querySelector('main')) return;
  var NS = 'http://www.w3.org/2000/svg';
  // Every width (Nov 20: the user wants the animations on phones too). Below 1100px the line runs in the 22px page
  // margin; mobile.css drops the vertical labels and leaders there, the axis, datum points and progress stay.
  var wide = window.matchMedia('all');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var el = function (tag, attrs, parent) {
    var n = document.createElementNS(NS, tag);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n);
    return n;
  };
  var docY = function (r) { return r.top + window.scrollY; };

  var svg = el('svg', { 'class': 'sig sig--' + V, 'aria-hidden': 'true', focusable: 'false' });
  var defs = el('defs', {}, svg);
  var mLight = el('mask', { id: 'sig-m-light', maskUnits: 'userSpaceOnUse' }, defs);
  var mDark = el('mask', { id: 'sig-m-dark', maskUnits: 'userSpaceOnUse' }, defs);
  var gLine = el('g', { 'class': 'sig__lines' }, svg);
  var base = el('path', { 'class': 'sig__base', mask: 'url(#sig-m-light)' }, gLine);
  var baseInv = el('path', { 'class': 'sig__base sig__base--inv', mask: 'url(#sig-m-dark)' }, gLine);
  var done = el('path', { 'class': 'sig__done' }, gLine);
  var heads = V === 'b' ? [240, 130, 56].map(function (s, i) { return { s: s, p: el('path', { 'class': 'sig__head sig__head--' + i }, gLine) }; }) : [];
  var gSt = el('g', { 'class': 'sig__stations' }, svg);
  var gran = V === 'b' ? el('circle', { 'class': 'sig__granule', r: 3.5 }, svg) : null;
  document.body.appendChild(svg);

  var total = 0, table = [], stations = [], nodes = [], startY = 0, endY = 0, tick = false;

  function contentLeft() {
    var c = document.querySelector('main section:not(.hero) .container') || document.querySelector('.container');
    var r = c.getBoundingClientRect(), cs = getComputedStyle(c);
    return r.left + parseFloat(cs.paddingLeft);
  }

  function headingOf(sec) {
    var id = sec.getAttribute('aria-labelledby'), h = id && document.getElementById(id);
    if (h && h.offsetParent && !h.classList.contains('visually-hidden')) return h;
    return $$('h2', sec).filter(function (x) { return x.offsetParent && x.getBoundingClientRect().height > 0; })[0] || null;
  }

  function labelOf(sec, h) {
    var t = sec.getAttribute('data-sig-label') || (h && h.getAttribute('data-sig-label'));
    if (!t && h) { var ln = h.querySelector('.ln__in'); t = (ln || h).textContent; }
    if (!t) t = sec.getAttribute('aria-label') || '';
    t = t.replace(/\s+/g, ' ').trim().replace(/[.:]$/, '');
    return t.length > 26 ? t.slice(0, 25).trim() + '…' : t;
  }

  /* origin: the hero's tab rule (home) or the bottom of the page hero */
  function origin(sx) {
    // home hero "Doorstroom": the line starts at the Proceslijn's datum mark and turns down into block 2
    var dsO = document.querySelector('[data-sig-origin]');
    if (dsO && dsO.offsetParent) {
      var orr = dsO.getBoundingClientRect(), oy = docY(orr) + orr.height / 2;
      var S0 = root.getAttribute('data-sig-start');
      return { x: orr.left + orr.width / 2, y: oy, bottom: oy - (S0 === 'source' ? 8 : 48), label: L('processLine', 'Proceslijn'), tabs: true };
    }
    var track = document.querySelector('[data-hero-track]'), tab = document.querySelector('.hero-tab');
    if (track && tab && tab.offsetParent) {
      var hero = track.querySelector('.hero');
      var heroTop = docY(track.getBoundingClientRect()) + track.offsetHeight - hero.offsetHeight;   // where the hero lands after the pin
      var tr = tab.getBoundingClientRect(), hr = hero.getBoundingClientRect();
      return { x: tr.left, y: heroTop + (tr.top - hr.top), bottom: heroTop + hero.offsetHeight, label: L('processLine', 'Proceslijn'), tabs: true };
    }
    // other templates: start under the page hero (the h1's block, plus a following media block without its own h2)
    var h1 = document.querySelector('main h1'), blk = h1 || document.querySelector('main > *');

    while (blk.parentElement && !/^(MAIN|ARTICLE)$/.test(blk.parentElement.tagName)) blk = blk.parentElement;
    // closed dialogs / templates take no space: skip them; a page subnav belongs to the opening (product pages)
    var nx = blk.nextElementSibling;
    while (nx && !nx.getBoundingClientRect().height && nx.nextElementSibling) nx = nx.nextElementSibling;
    if (nx && !nx.querySelector('h2') && nx.getBoundingClientRect().height > 0) blk = nx;
    var r = blk.getBoundingClientRect();
    var lab = h1 ? (h1.querySelector('.ln__in') || h1).textContent.trim() : '';
    // the datum sits clear of the opening's edge (its border / the subnav bar), never on it (Nov 22)
    return { x: sx, y: docY(r) + r.height + 36, label: lab.length > 20 ? lab.slice(0, 19) + '…' : lab, tabs: false };
  }

  function collect(o) {
    var main = document.querySelector('main');
    var secs = $$('section', main).filter(function (s) {
      return !s.closest('.hero-track') && !s.parentElement.closest('section') && docY(s.getBoundingClientRect()) > o.y + 40;
    });
    var list = secs.map(function (s) { return { sec: s, h: headingOf(s) }; });
    // long-read pages: the article's own h2s are stations too
    $$('main h2.h2[id]').forEach(function (h) {
      if (h.closest('section') || !h.offsetParent) return;
      list.push({ sec: h, h: h });
    });
    return list.map(function (it) {
      var h = it.h, r = (h || it.sec).getBoundingClientRect(), y;
      if (h) {
        var ln = h.querySelector('.ln');
        if (ln) { var lr = ln.getBoundingClientRect(); y = docY(lr) + lr.height / 2; }
        else { var lh = parseFloat(getComputedStyle(h).lineHeight) || 40; y = docY(r) + Math.min(lh, r.height) / 2; }
      } else y = docY(r) + 48;
      return { y: Math.round(y) + 0.5, x: Math.round(r.left), label: labelOf(it.sec, h), sec: it.sec };
    }).filter(function (s) { return s.y > o.y + 60; })
      .sort(function (a, b) { return a.y - b.y; })
      .filter(function (s, i, a) { return i === 0 || s.y - a[i - 1].y > 180; });
  }

  function darkBands() {
    return $$('main [data-theme="forest"]').filter(function (b) { return !b.parentElement.closest('[data-theme="forest"]'); })
      .map(function (b) { var r = b.getBoundingClientRect(); return { y0: docY(r), y1: docY(r) + r.height }; });
  }

  function layout() {
    var W = document.documentElement.clientWidth, H = document.documentElement.scrollHeight;
    if (!wide.matches) { svg.style.display = 'none'; nodes.forEach(function (n) { n.classList.add('is-on'); }); return; }
    svg.style.display = '';
    svg.setAttribute('width', W); svg.setAttribute('height', H); svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);

    var cl = contentLeft();
    var sx = Math.round(Math.max(cl - 48, cl * 0.5)) + 0.5;
    var o = origin(sx);
    stations = collect(o);
    if (!stations.length) { svg.style.display = 'none'; return; }
    var last = stations[stations.length - 1];
    // start concepts (review): html[data-sig-start] = origin | inlet | source; all start one grid step below the hero
    var S = root.getAttribute('data-sig-start');
    startY = Math.round(S && o.tabs ? o.bottom + (S === 'source' ? 8 : 48) : o.y) + 0.5;
    var fadeL = Math.round(Math.min(130, (stations[0].y - startY) * 0.55));
    endY = last.y + (V === 'a' ? 72 : 140);

    var d, R = 14;
    if (V === 'a' && S === 'inlet') {
      d = 'M0,' + startY + ' H' + (sx - R) + ' Q' + sx + ',' + startY + ' ' + sx + ',' + (startY + R) + ' V' + endY;
    } else if (V === 'a' && S) {
      d = 'M' + sx + ',' + startY + ' V' + endY;
    } else if (V === 'a') {
      d = o.tabs ? 'M' + Math.max(o.x, sx + R) + ',' + startY + ' H' + (sx + R) + ' Q' + sx + ',' + startY + ' ' + sx + ',' + (startY + R)
                 : 'M' + sx + ',' + startY;
      d += ' V' + endY;
    } else {
      d = o.tabs ? 'M' + (sx > o.x + 40 ? sx - 56 : o.x + 56) + ',' + startY + ' C' + (sx + 6) + ',' + startY + ' ' + sx + ',' + (startY + 4) + ' ' + sx + ',' + (startY + 64)
                 : 'M' + sx + ',' + startY;
      stations.forEach(function (s) {
        var bx = Math.max(s.x - 18, sx + 14), k = 70;
        s.bx = bx;
        d += ' V' + (s.y - k * 1.6) + ' C' + sx + ',' + (s.y - k * 0.7) + ' ' + bx + ',' + (s.y - k * 0.75) + ' ' + bx + ',' + s.y +
             ' C' + bx + ',' + (s.y + k * 0.75) + ' ' + sx + ',' + (s.y + k * 0.7) + ' ' + sx + ',' + (s.y + k * 1.6);
      });
      d += ' V' + endY;
    }
    [base, baseInv, done].forEach(function (p) { p.setAttribute('d', d); });
    heads.forEach(function (h) { h.p.setAttribute('d', d); });
    total = done.getTotalLength();
    table = [];
    // The production signature is a vertical line: its arc length is its y distance.
    // Avoid thousands of synchronous SVG geometry queries on every layout.
    if (V === 'a' && S && S !== 'inlet') table.push([startY, 0]);
    else for (var L = 0; L <= total; L += 6) table.push([done.getPointAtLength(L).y, L]);
    table.push([endY, total]);

    gLine.removeAttribute('mask');
    var old = defs.querySelector('#sig-m-fade'); if (old) old.parentNode.removeChild(old);
    old = defs.querySelector('#sig-fade'); if (old) old.parentNode.removeChild(old);
    if (V === 'a' && S === 'source') {
      var gr = el('linearGradient', { id: 'sig-fade', gradientUnits: 'userSpaceOnUse', x1: 0, y1: startY, x2: 0, y2: startY + fadeL }, defs);
      el('stop', { offset: 0, 'stop-color': '#000' }, gr); el('stop', { offset: 1, 'stop-color': '#fff' }, gr);
      var fm = el('mask', { id: 'sig-m-fade', maskUnits: 'userSpaceOnUse' }, defs);
      el('rect', { width: W, height: H, fill: 'url(#sig-fade)' }, fm);
      gLine.setAttribute('mask', 'url(#sig-m-fade)');
    }

    // dark bands: the base line inverts inside them
    var bands = darkBands();
    mLight.innerHTML = ''; mDark.innerHTML = '';
    el('rect', { width: W, height: H, fill: '#fff' }, mLight);
    bands.forEach(function (b) {
      el('rect', { x: 0, y: b.y0, width: W, height: b.y1 - b.y0, fill: '#000' }, mLight);
      el('rect', { x: 0, y: b.y0, width: W, height: b.y1 - b.y0, fill: '#fff' }, mDark);
    });
    var inBand = function (y) { return bands.some(function (b) { return y >= b.y0 && y <= b.y1; }); };

    // stations
    gSt.innerHTML = '';
    var all = [{ y: startY, x: o.x, label: o.label, origin: true }].concat(stations);
    all.forEach(function (s, i) {
      var g = el('g', { 'class': 'sig-st' + (s.origin ? ' sig-st--origin' : '') + (inBand(s.y) ? ' is-inv' : '') }, gSt);
      var no = (i + 1 < 10 ? '0' : '') + (i + 1);
      if (V === 'a') {
        if (!s.origin) {
          el('line', { 'class': 'sig-st__leader', x1: sx + 9, y1: s.y, x2: Math.max(s.x - 16, sx + 18), y2: s.y }, g);
          el('line', { 'class': 'sig-st__cross', x1: sx - 9, y1: s.y, x2: sx + 9, y2: s.y }, g);
          el('line', { 'class': 'sig-st__cross', x1: sx, y1: s.y - 9, x2: sx, y2: s.y + 9 }, g);
          el('circle', { 'class': 'sig-st__dot', cx: sx, cy: s.y, r: 4 }, g);
        }
        if (s.origin && S === 'origin') {          // datum / centre-of-gravity mark: ring with two opposite quarters filled
          var q = 6.5;
          el('line', { 'class': 'sig-st__cross', x1: sx - 14, y1: startY, x2: sx + 14, y2: startY }, g);
          el('line', { 'class': 'sig-st__cross', x1: sx, y1: startY - 14, x2: sx, y2: startY }, g);
          el('circle', { 'class': 'sig-st__datum', cx: sx, cy: startY, r: q }, g);
          el('path', { 'class': 'sig-st__quad', d: 'M' + sx + ',' + startY + ' h' + q + ' a' + q + ',' + q + ' 0 0 1 ' + (-q) + ',' + q + 'z' }, g);
          el('path', { 'class': 'sig-st__quad', d: 'M' + sx + ',' + startY + ' h' + (-q) + ' a' + q + ',' + q + ' 0 0 1 ' + q + ',' + (-q) + 'z' }, g);
        }
        if (s.origin && S === 'inlet') {           // flow arrow on the run in from the sheet edge (ISO 10628)
          var ax = Math.round(Math.max(sx * 0.45, sx - 160));
          el('path', { 'class': 'sig-st__arrow', d: 'M' + (ax - 4) + ',' + (startY - 4.5) + ' L' + (ax + 5) + ',' + startY + ' L' + (ax - 4) + ',' + (startY + 4.5) + 'z' }, g);
        }
        if (s.origin && S === 'source') {          // the H1's pulse dot, where the line becomes solid
          el('circle', { 'class': 'sig-st__ping', cx: sx, cy: startY + fadeL, r: 4 }, g);
          el('circle', { 'class': 'sig-st__src', cx: sx, cy: startY + fadeL, r: 3.5 }, g);
        }
        var ty = s.origin ? startY + (S === 'source' ? fadeL + 22 : S ? 28 : 34) : s.y + 22;
        // the label runs down the axis until the next station: fit it to that gap (number only when it is tight)
        var next = all[i + 1] ? all[i + 1].y - 22 : endY + 200;
        var fit = Math.floor((next - ty) / 7.6) - 5, lab = s.label.toUpperCase();
        if (lab.length > fit) lab = fit >= 6 ? lab.slice(0, fit - 1).trim() + '…' : '';
        var t = el('text', { 'class': 'sig-st__label', x: sx - 9, y: ty, transform: 'rotate(-90 ' + (sx - 9) + ' ' + ty + ')', 'text-anchor': 'end' }, g);
        t.textContent = lab ? no + ' — ' + lab : no;
      } else {
        if (!s.origin) {
          el('circle', { 'class': 'sig-st__ring', cx: s.bx, cy: s.y, r: 4.5 }, g);
          var tb = el('text', { 'class': 'sig-st__no', x: s.bx - 12, y: s.y + 3.5, 'text-anchor': 'end' }, g);
          tb.textContent = no;
        }
      }
      s.g = g;
    });
    stations = all;

    // content nodes (e.g. the two discipline nodes) light up when the tip passes them
    nodes = $$('[data-sig-node]').map(function (n) { var r = n.getBoundingClientRect(); n._sy = docY(r) + r.height / 2; return n; });
    draw();
  }

  function lengthAt(y) {
    if (y <= table[0][0]) return 0;
    if (V === 'a' && root.getAttribute('data-sig-start') === 'origin') return Math.min(total, y - startY);
    var lo = 0, hi = table.length - 1;
    while (hi - lo > 1) { var m = (lo + hi) >> 1; if (table[m][0] < y) lo = m; else hi = m; }
    // the first rows share one y (the run along the tab rule): take the last of them
    return table[hi][1];
  }

  function draw() {
    tick = false;
    if (!wide.matches || !total) return;
    var tip = reduce.matches ? Infinity : window.scrollY + window.innerHeight * 0.62;
    var L = tip === Infinity ? total : lengthAt(tip);
    if (L < 1) L = 0;
    done.style.strokeDasharray = L + ' ' + (total + 10);
    heads.forEach(function (h) {
      var s = Math.min(h.s, L);
      h.p.style.strokeDasharray = '0 ' + (L - s) + ' ' + s + ' ' + (total + 10);
      h.p.style.opacity = L > 0 && L < total - 2 ? '' : '0';
    });
    if (gran) {
      var on = !reduce.matches && L > 2 && L < total - 2;
      gran.style.opacity = on ? '' : '0';
      if (on) { var pt = done.getPointAtLength(L); gran.setAttribute('cx', pt.x); gran.setAttribute('cy', pt.y); }
    }
    var tipY = L >= total ? Infinity : done.getPointAtLength(L).y;
    stations.forEach(function (s) { s.g.classList.toggle('is-on', L > 0 && tipY >= s.y - 1); });
    nodes.forEach(function (n) { n.classList.toggle('is-on', tipY >= n._sy); });
  }

  var queued = false;
  function relayout() { if (queued) return; queued = true; requestAnimationFrame(function () { queued = false; layout(); }); }
  relayout();
  window.addEventListener('load', relayout);
  window.addEventListener('resize', relayout);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(relayout);
  if ('ResizeObserver' in window) new ResizeObserver(relayout).observe(document.body);
  wide.addEventListener('change', relayout);
  reduce.addEventListener('change', relayout);
  window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(draw); } }, { passive: true });
})();
