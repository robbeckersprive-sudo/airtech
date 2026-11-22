/* Airtechnic "Flow" — home blocks 4 "Projectdossier" and 5 "Van tekening tot installatie" (src/home_practice.py). */
(function () {
  'use strict';
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  var clamp = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; };

  /* =================================================================== block 4: project dossier */
  var pd = document.querySelector('[data-pd]');
  if (pd) {
    var imgs = $$('[data-pd-img]', pd), copies = $$('[data-pd-copy]', pd), tabs = $$('[data-pd-tab]', pd);
    var count = pd.querySelector('[data-pd-count]'), cur = 0, timer = 0;
    var fmt = function (v, dec) { return v.toLocaleString('nl-NL', { minimumFractionDigits: dec, maximumFractionDigits: dec }); };
    // the hard facts count up as a project opens (the final text is already in the HTML)
    var countUp = function (copy) {
      $$('dd[data-count]', copy).forEach(function (dd, k) {
        var span = dd.querySelector('[data-pd-num]'), to = parseFloat(dd.getAttribute('data-count')), dec = +dd.getAttribute('data-dec');
        if (!span || reduce.matches) return;
        var end = span.textContent, t0 = 0, dur = 1100 + k * 150;
        var step = function (t) {
          if (!t0) t0 = t;
          var q = clamp((t - t0) / dur), e = 1 - Math.pow(1 - q, 3);
          span.textContent = q < 1 ? fmt(to * e, dec) : end;
          if (q < 1) requestAnimationFrame(step);
        };
        requestAnimationFrame(step);
      });
    };
    var show = function (n, focus) {
      if (n === cur) return;
      var prev = cur; cur = n;
      clearTimeout(timer);
      imgs.forEach(function (im, i) { im.classList.toggle('is-on', i === n); im.classList.toggle('is-leaving', i === prev); });
      pd.classList.toggle('is-wiping', !reduce.matches);
      timer = setTimeout(function () { imgs[prev].classList.remove('is-leaving'); pd.classList.remove('is-wiping'); }, reduce.matches ? 0 : 1400);
      copies.forEach(function (c, i) {
        var on = i === n;
        c.classList.toggle('is-on', on);
        if (on) { c.removeAttribute('aria-hidden'); c.inert = false; } else { c.setAttribute('aria-hidden', 'true'); c.inert = true; }
      });
      tabs.forEach(function (t, i) {
        t.setAttribute('aria-selected', String(i === n)); t.tabIndex = i === n ? 0 : -1;
      });
      if (focus) tabs[n].focus();
      if (count) count.textContent = (n < 9 ? '0' : '') + (n + 1);
      countUp(copies[n]);
      // keep the active thumbnail in view in the scrolling index (phones)
      var idx = tabs[n].parentElement;
      if (idx.scrollWidth > idx.clientWidth) idx.scrollTo({ left: tabs[n].offsetLeft - (idx.clientWidth - tabs[n].offsetWidth) / 2, behavior: reduce.matches ? 'auto' : 'smooth' });
    };
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { show(i); });
      t.addEventListener('keydown', function (e) {
        var k = e.key, m = k === 'ArrowRight' ? i + 1 : k === 'ArrowLeft' ? i - 1 : k === 'Home' ? 0 : k === 'End' ? tabs.length - 1 : null;
        if (m === null) return;
        e.preventDefault(); show((m + tabs.length) % tabs.length, true);
      });
    });
    // swipe the picture (touch)
    var stage = pd.querySelector('[data-pd-stage]'), sx = null, sy = 0;
    stage.addEventListener('pointerdown', function (e) { if (e.pointerType === 'touch') { sx = e.clientX; sy = e.clientY; } });
    stage.addEventListener('pointerup', function (e) {
      if (sx === null) return;
      var dx = e.clientX - sx, dy = e.clientY - sy; sx = null;
      if (Math.abs(dx) > 48 && Math.abs(dx) > Math.abs(dy) * 1.4) show((cur + (dx < 0 ? 1 : -1) + tabs.length) % tabs.length);
    });
    // first arrival: the facts of the opening project count up once
    if ('IntersectionObserver' in window) {
      var pio = new IntersectionObserver(function (en) {
        if (en[0].isIntersecting) { pd.classList.add('is-in'); countUp(copies[cur]); pio.disconnect(); }
      }, { rootMargin: '0px 0px -25% 0px' });
      pio.observe(pd);
    } else pd.classList.add('is-in');
  }

  /* =================================================================== block 5: drawing -> installation */
  var wk = document.querySelector('[data-wk]');
  if (!wk) return;
  var steps = $$('[data-wk-step]', wk), shots = $$('[data-wk-shot]', wk), labels = $$('[data-wk-label]', wk);
  var no = wk.querySelector('[data-wk-no]'), rail = wk.querySelector('[data-wk-rail]'), list = wk.querySelector('[data-wk-steps]');
  var wide = window.matchMedia('(min-width: 900px)');
  var active = -1, ticking = false;
  function frame() {
    ticking = false;
    var vh = window.innerHeight, line = vh * .5;
    // which step is under the reading line, and how far it has been read
    var idx = 0, local = 0;
    steps.forEach(function (s, i) {
      var r = s.getBoundingClientRect();
      if (r.top <= line) { idx = i; local = clamp((line - r.top) / Math.max(1, r.height * .62)); }
      // phones: every step plots its own sheet as it crosses the screen
      if (!wide.matches) {
        var m = s.querySelector('.wk-mshot'), mr = m.getBoundingClientRect();
        m.style.setProperty('--x', (reduce.matches ? 100 : clamp((vh * .86 - mr.top) / (vh * .55)) * 100).toFixed(1) + '%');
      }
    });
    if (reduce.matches) local = 1;
    wk.style.setProperty('--x', (local * 100).toFixed(1) + '%');
    wk.classList.toggle('is-plotting', local > .01 && local < .99);
    if (idx !== active) {
      active = idx;
      shots.forEach(function (sh, i) { sh.classList.toggle('is-on', i === idx); });
      labels.forEach(function (l, i) { l.classList.toggle('is-on', i === idx); });
      steps.forEach(function (s, i) { s.classList.toggle('is-on', i === idx); s.classList.toggle('is-done', i < idx); });
      if (no) no.textContent = (idx < 9 ? '0' : '') + (idx + 1);
    }
    // the rail fills down to the reading line
    var lr = list.getBoundingClientRect();
    if (rail) rail.style.height = (clamp((line - lr.top) / lr.height) * 100).toFixed(2) + '%';
  }
  var request = function () { if (!ticking) { ticking = true; requestAnimationFrame(frame); } };
  window.addEventListener('scroll', request, { passive: true });
  window.addEventListener('resize', request);
  wide.addEventListener('change', request);
  frame();
})();
