/* Block 2 variants A / B / C — review build; see tools/block_concepts.py.
   One passive scroll listener + rAF; reads the hero plate geometry (--ix / --ir on [data-hero-track]) so the block
   picks up exactly where the hero ended. Reduced motion: every variant renders its finished state. */
(function () {
  'use strict';
  var sec = document.querySelector('[data-blk]');
  if (!sec) return;
  var kind = sec.getAttribute('data-blk');
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  var wide = window.matchMedia('(min-width: 960px)');
  var clamp01 = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; };
  var track = $('[data-hero-track]');
  var heroVar = function (name, fallback) {
    var v = track && parseFloat(track.style.getPropertyValue(name));
    return isNaN(v) || !v ? fallback : v;
  };

  /* ---------- figure swap (A, B: per discipline; C: one plate for all rows) ---------- */
  var showFig = function (frame, key, link) {
    $$('[data-fig-img]', frame).forEach(function (im) {
      var on = im.getAttribute('data-fig-img') === key;
      im.classList.toggle('is-on', on);
      if (on) { var c = $('[data-fig-cap]', frame); if (c) c.textContent = im.getAttribute('data-cap'); }
    });
    if (link) {
      var pos = $('[data-fig-pos]', frame), row = link.closest('[data-row]');
      if (pos && row) pos.textContent = $('.blkC-pos', row).textContent;
    }
  };
  var setActive = function (links, a, frame) {
    links.forEach(function (l) { l.classList.toggle('is-on', l === a); var r = l.closest('[data-row]'); if (r) r.classList.toggle('is-on', l === a); });
    showFig(frame, a.getAttribute('data-fig'), a);
  };
  if (kind === 'c') {
    var frameC = $('[data-fig-frame]', sec), linksC = $$('[data-fig]', sec);
    linksC.forEach(function (a) {
      a.addEventListener('pointerenter', function () { setActive(linksC, a, frameC); });
      a.addEventListener('focus', function () { setActive(linksC, a, frameC); });
    });
    setActive(linksC, linksC[0], frameC);
    if ('IntersectionObserver' in window) {
      // the row crossing the middle of the screen drives the plate (works on touch, no hover needed)
      var mid = new IntersectionObserver(function (en) {
        en.forEach(function (e) { if (e.isIntersecting) setActive(linksC, $('[data-fig]', e.target), frameC); });
      }, { rootMargin: '-46% 0px -46% 0px' });
      var rows = $$('[data-row]', sec);
      rows.forEach(function (r) { mid.observe(r); });
      if (!reduce.matches) {
        rows.forEach(function (r) { r.style.setProperty('--rx', '0'); });
        var draw = new IntersectionObserver(function (en) {
          en.forEach(function (e) { if (e.isIntersecting) { e.target.style.setProperty('--rx', '1'); draw.unobserve(e.target); } });
        }, { rootMargin: '0px 0px -12% 0px' });
        rows.forEach(function (r, i) { r.style.transitionDelay = (i % 4) * 60 + 'ms'; draw.observe(r); });
      }
    }
  } else {
    $$('[data-disc]', sec).forEach(function (d) {
      var frame = $('[data-fig-frame]', d), links = $$('[data-fig]', d);
      links.forEach(function (a) {
        a.addEventListener('pointerenter', function () { setActive(links, a, frame); });
        a.addEventListener('focus', function () { setActive(links, a, frame); });
      });
      if (links[0]) setActive(links, links[0], frame);
    });
  }

  /* ---------- A: the process line ---------- */
  var line = $('[data-blk-line]', sec), base = [], flow = [], gran = [], nodes = [], lens = [0, 0], ends = [0, 0];
  if (line) {
    base = $$('[data-line-base]', line); flow = $$('[data-line-flow]', line); gran = $$('[data-line-granule]', line);
    nodes = $$('[data-blk-node]', sec);
  }
  var layoutLine = function () {
    if (!line || !wide.matches) return;
    var sr = sec.getBoundingClientRect(), vw = document.documentElement.clientWidth;
    var x0 = heroVar('--ix', vw * 0.46) - sr.left;           // drops from the hero plate's left edge
    var pts = nodes.map(function (n) { var r = n.getBoundingClientRect(); return { x: r.left + r.width / 2 - sr.left, y: r.top + r.height / 2 - sr.top, h: r.height / 2 }; });
    var jy = Math.min(pts[0].y, pts[1].y) - 72, R = 18;
    var y0 = 10 - heroVar('--ib', 124);                       // the hero plate's bottom-left corner sits --ib above us
    pts.forEach(function (p, i) {
      var dir = p.x < x0 ? -1 : 1;
      var d = 'M' + x0 + ',' + y0 + ' V' + (jy - R) + ' Q' + x0 + ',' + jy + ' ' + (x0 + dir * R) + ',' + jy +
              ' H' + (p.x - dir * R) + ' Q' + p.x + ',' + jy + ' ' + p.x + ',' + (jy + R) + ' V' + (p.y - p.h - 2);
      base[i].setAttribute('d', d); flow[i].setAttribute('d', d);
      lens[i] = flow[i].getTotalLength(); ends[i] = p.y - p.h;
      flow[i].style.strokeDasharray = lens[i] + ' ' + lens[i];
    });
  };
  var drawLine = function () {
    if (!line || !wide.matches) return;
    var sr = sec.getBoundingClientRect(), vh = window.innerHeight;
    var tip = vh * 0.62 - sr.top;                             // the drawn tip rides at ~62% of the viewport
    flow.forEach(function (f, i) {
      var k = reduce.matches ? 1 : clamp01(tip / ends[i]);
      var L = lens[i] * k;
      f.style.strokeDashoffset = String(lens[i] - L);
      var g = gran[i], on = !reduce.matches && k > 0.01 && k < 0.999;
      g.classList.toggle('is-on', on);
      if (on) { var pt = f.getPointAtLength(L); g.setAttribute('cx', pt.x); g.setAttribute('cy', pt.y); }
      nodes[i].classList.toggle('is-on', k >= 0.999);
    });
  };

  /* ---------- B: the split ---------- */
  var split = $('[data-blk-split]', sec);
  var layoutSplit = function () {
    if (!split) return;
    var f = $('.blkB-fig', split);
    split.style.setProperty('--fig-h', f.offsetHeight + 'px');
  };
  var drawSplit = function () {
    if (!split || !wide.matches) return;
    var r = split.getBoundingClientRect(), vh = window.innerHeight;
    var b = reduce.matches ? 1 : clamp01((vh * 0.9 - r.top) / (vh * 0.55));
    var e = b * b * (3 - 2 * b);
    split.style.setProperty('--b', e.toFixed(4));
  };

  /* ---------- C: plate in the hero plate's footprint ---------- */
  var layoutC = function () {
    if (kind !== 'c') return;
    var vw = document.documentElement.clientWidth;
    var w = vw - heroVar('--ix', vw * 0.46) - heroVar('--ir', 24);
    var grid = $('.blkC', sec);
    grid.style.setProperty('--plate-w', Math.round(Math.min(w, grid.clientWidth * 0.48)) + 'px');
  };

  var tick = false;
  var frame = function () { tick = false; drawLine(); drawSplit(); };
  var layout = function () { layoutC(); layoutSplit(); layoutLine(); frame(); };
  layout();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { requestAnimationFrame(layout); });
  window.addEventListener('load', layout);
  window.addEventListener('resize', layout);
  window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(frame); } }, { passive: true });
  reduce.addEventListener('change', layout);
})();
