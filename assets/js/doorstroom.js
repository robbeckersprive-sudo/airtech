/* Airtechnic "Flow" — home hero "Doorstroom" (src/hero_doorstroom.py, styles in assets/css/top.css).
   Five sheets of one process line. The Proceslijn stations are the tabs; the play button's ring is the slide clock
   (CSS animation, its animationend advances). The clock holds while the visitor reads, hovers, focuses with the
   keyboard, plays with the tube or the regime instrument, while off-screen or in a hidden tab, and under reduced motion.
   The pause button stops everything that moves (WCAG 2.2.2): clock, granule canvas (.is-paused), SVG flows. */
(function () {
  'use strict';
  var root = document.querySelector('[data-ds]');
  if (!root) return;
  var $$ = function (s, c) { return Array.prototype.slice.call((c || root).querySelectorAll(s)); };
  var slides = $$('.ds-slide'), copies = $$('[data-ds-copy]'), mores = $$('[data-ds-more]'), tabs = $$('[data-ds-tab]');
  var play = root.querySelector('[data-ds-play]'), clock = root.querySelector('.ds-play__clock');
  var line = root.querySelector('[data-ds-line]'), fill = root.querySelector('[data-ds-fill]');
  var canvas = root.querySelector('canvas[data-granules]'), text = root.querySelector('.ds-text');
  var instruments = $$('[data-ds-instrument]');
  function instrumentFor(n) { return instruments.filter(function (m) { return +m.getAttribute('data-for') === n; })[0] || null; }
  var stage = root.querySelector('[data-ds-stage]');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  var current = 0, paused = false, engaged = false, visible = true, holds = {}, leaveTimer = 0;

  /* ---------- clock ---------- */
  function held() {
    for (var k in holds) if (holds[k]) return true;
    return paused || engaged || !visible || document.hidden || reduce.matches;
  }
  function syncClock() { root.classList.toggle('is-hold', held()); }
  function hold(key, on) { holds[key] = on; syncClock(); }
  function restartClock() {
    clock.style.animation = 'none';
    void clock.getBoundingClientRect();
    clock.style.animation = '';
    syncClock();
  }
  clock.addEventListener('animationend', function () { if (!held()) show((current + 1) % slides.length, true); });

  /* ---------- slides ---------- */
  function setOff(el, off) {
    if (off) { el.setAttribute('aria-hidden', 'true'); el.inert = true; }
    else { el.removeAttribute('aria-hidden'); el.inert = false; }
  }
  var sheetRequest = 0;
  function show(n, auto) {
    var request = ++sheetRequest;
    if (n === current) { restartClock(); return; }
    var prev = current, img = slides[n].querySelector('img');
    // A skipped inactive sheet must explicitly request its photo before decode can resolve.
    if (img) img.loading = 'eager';
    slides[n].querySelectorAll('img').forEach(function (image) { image.loading = 'eager'; });
    var ready = [];
    slides[n].querySelectorAll('image[data-sheet-href]').forEach(function (image) {
      var href = image.getAttribute('data-sheet-href');
      image.setAttribute('href', href);
      image.removeAttribute('data-sheet-href');
      var preload = new Image(); preload.src = href;
      if (preload.decode) ready.push(preload.decode().catch(function () {}));
    });
    var go = function () {
      if (request !== sheetRequest) return;
      if (auto && held()) return;
      current = n;
      clearTimeout(leaveTimer);
      slides.forEach(function (s, i) {
        s.hidden = i !== n && i !== prev;
        s.classList.toggle('is-on', i === n);
        s.classList.toggle('is-leaving', i === prev);
        setOff(s, i !== n);
      });
      root.classList.toggle('is-wiping', !reduce.matches);
      leaveTimer = setTimeout(function () {
        slides[prev].classList.remove('is-leaving'); slides[prev].hidden = true; root.classList.remove('is-wiping');
      }, reduce.matches ? 0 : 1500);
      copies.forEach(function (c, i) { c.classList.toggle('is-on', i === n); setOff(c, i !== n); });
      mores.forEach(function (m, i) { m.classList.toggle('is-on', i === n); setOff(m, i !== n); });
      tabs.forEach(function (t, i) { if (i === n) t.setAttribute('aria-current', 'true'); else t.removeAttribute('aria-current'); });
      root.setAttribute('data-sheet', String(n));
      instruments.forEach(function (m) { m.classList.toggle('is-for', m === instrumentFor(n)); });
      engaged = false;
      placeFill(); placeSpots(); restartClock(); kickRotor();
      root.dispatchEvent(new Event('hero-motion-change'));
    };
    if (img && img.decode) ready.push(img.decode().catch(function () {}));
    Promise.all(ready).then(go);
  }

  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { engaged = false; show(i); });
    t.addEventListener('keydown', function (e) {
      var k = e.key, n = k === 'ArrowRight' ? i + 1 : k === 'ArrowLeft' ? i - 1 : k === 'Home' ? 0 : k === 'End' ? tabs.length - 1 : null;
      if (n === null) return;
      e.preventDefault(); n = (n + tabs.length) % tabs.length; tabs[n].focus(); show(n);
    });
  });

  /* ---------- pause: everything that moves ---------- */
  function setPaused(on) {
    paused = on;
    root.classList.toggle('is-paused', on);
    play.setAttribute('aria-pressed', String(on));
    play.setAttribute('aria-label', on ? 'Animatie afspelen' : 'Animatie pauzeren');
    play.querySelector('[data-ds-icon-pause]').toggleAttribute('hidden', on);
    play.querySelector('[data-ds-icon-play]').toggleAttribute('hidden', !on);
    root.dispatchEvent(new Event('hero-motion-change'));   // site.js runs the SVG flows of the active sheet only
    syncClock(); kickRotor();
  }
  play.addEventListener('click', function () { setPaused(!paused); });

  /* ---------- holds ---------- */
  [text, line].concat(instruments).forEach(function (el, i) {
    if (!el) return;
    el.addEventListener('pointerenter', function (e) { if (e.pointerType !== 'touch') hold('h' + i, true); });
    el.addEventListener('pointerleave', function () { hold('h' + i, false); });
  });
  root.addEventListener('focusin', function (e) { hold('focus', e.target.matches(':focus-visible')); });
  root.addEventListener('focusout', function (e) { if (!e.relatedTarget || !root.contains(e.relatedTarget)) hold('focus', false); });
  if (canvas) new MutationObserver(function () { hold('tube', canvas.classList.contains('is-blowing')); })
    .observe(canvas, { attributes: true, attributeFilter: ['class'] });
  $$('[data-ds-spot]').forEach(function (s) {
    s.addEventListener('pointerenter', function () { hold('spot', true); });
    s.addEventListener('pointerleave', function () { hold('spot', false); });
  });
  document.addEventListener('visibilitychange', syncClock);
  if ('IntersectionObserver' in window) new IntersectionObserver(function (en) {
    visible = en[0].intersectionRatio > .35; syncClock(); kickRotor();
  }, { threshold: [0, .35, .6] }).observe(root);
  if (reduce.addEventListener) reduce.addEventListener('change', function () { setPaused(paused); });

  /* ---------- instruments: one per sheet that has two telling states (src/hero_modes.py) ----------
     A choice sets data-mode on its sheet (CSS shows flow group a or b); sheet 1 also drives the granule canvas.
     Choosing keeps the visitor on that sheet until they pick another station. */
  instruments.forEach(function (m) {
    var n = +m.getAttribute('data-for'), opts = $$('[data-ds-mode]', m), seg = m.querySelector('.ds-mode__seg');
    opts.forEach(function (b, bi) {
      b.addEventListener('click', function () {
        var mode = b.getAttribute('data-ds-mode');
        opts.forEach(function (o) { o.setAttribute('aria-pressed', String(o === b)); });
        $$('[data-ds-note]', m).forEach(function (p) { p.classList.toggle('is-on', p.getAttribute('data-ds-note') === mode); });
        seg.setAttribute('data-on', String(bi));
        slides[n].setAttribute('data-mode', mode);
        if (n === 0) { if (canvas) canvas.setAttribute('data-mode', mode); root.setAttribute('data-mode', mode); }
        engaged = true; syncClock(); kickRotor();
      });
    });
  });

  /* ---------- dosing sheet: the photographed rotor turns (unsquashed rotation, see hero_modes.dosing_modes) ----------
     The angle is integrated here so a speed change eases instead of jumping. Pockets fill under the inlet (top) and
     empty over the outlet (bottom) on the way down the right-hand side. */
  var rotorSvg = root.querySelector('[data-rotor]'), rotorSlide = rotorSvg && rotorSvg.closest('.ds-slide');
  var spin = rotorSvg && rotorSvg.querySelector('[data-rotor-spin]');
  var pockets = rotorSvg ? $$('[data-pocket]', rotorSvg).map(function (g) { return { el: g, a: +g.getAttribute('data-pocket'), o: -1 }; }) : [];
  var ang = 0, omega = 36, rotorRaf = 0, rotorLast = 0;
  function fillAt(phi) {                               // 0..360, clockwise from the top
    phi = ((phi % 360) + 360) % 360;
    if (phi < 14) return phi / 14;                     // filling under the inlet
    if (phi < 168) return 1;                           // carried down full
    if (phi < 196) return 1 - (phi - 168) / 28;        // emptying over the outlet
    return 0;
  }
  function drawRotor() {
    spin.setAttribute('transform', 'rotate(' + ang.toFixed(2) + ')');
    pockets.forEach(function (p) {
      var o = fillAt(p.a + ang);
      if (Math.abs(o - p.o) > .01) { p.o = o; p.el.setAttribute('opacity', o.toFixed(2)); }
    });
  }
  function rotorRuns() {
    return rotorSlide && (rotorSlide.classList.contains('is-on') || rotorSlide.classList.contains('is-leaving')) &&
      !paused && visible && !document.hidden && !reduce.matches;
  }
  function rotorFrame(now) {
    rotorRaf = 0;
    if (!rotorRuns()) { rotorLast = 0; return; }
    var dt = rotorLast ? Math.min((now - rotorLast) / 1000, .05) : 0;
    rotorLast = now;
    var target = rotorSlide.getAttribute('data-mode') === 'b' ? 112 : 36;   // degrees per second: ~3.2 s or 10 s per turn
    omega += (target - omega) * (1 - Math.exp(-dt * 1.8));
    ang = (ang + omega * dt) % 360;
    drawRotor();
    rotorRaf = requestAnimationFrame(rotorFrame);
  }
  function kickRotor() { if (spin && !rotorRaf && rotorRuns()) rotorRaf = requestAnimationFrame(rotorFrame); }
  if (spin) { drawRotor(); document.addEventListener('visibilitychange', kickRotor); }

  /* ---------- geometry: line fill to the active station, callouts clear of the type ---------- */
  function placeFill() {
    if (!fill || !tabs[current]) return;
    var lr = line.getBoundingClientRect(), node = tabs[current].querySelector('.ds-st__node').getBoundingClientRect();
    fill.style.width = Math.max(0, node.left + node.width / 2 - lr.left) + 'px';
  }
  function placeSpots() {
    var instrument = instrumentFor(current);
    var limit = text.getBoundingClientRect().right + 28, ir = instrument && instrument.offsetParent ? instrument.getBoundingClientRect() : null;
    var vw = document.documentElement.clientWidth, wide = window.matchMedia('(min-width: 900px) and (min-aspect-ratio: 6/5)').matches;
    var sr = stage.getBoundingClientRect(), fadeY = sr.bottom - (wide ? 140 : 70), topY = sr.top + (wide ? 120 : 50);   // not in the faded edges
    $$('[data-ds-spot]', slides[current]).forEach(function (s) {
      s.hidden = false;
      var r = s.getBoundingClientRect(), x = r.left, y = r.top;
      var inInstr = ir && x > ir.left - 30 && x < ir.right + 30 && y > ir.top - 30 && y < ir.bottom + 30;
      s.hidden = (wide && x < limit) || x < 16 || x > vw - 16 || inInstr || y > fadeY || y < topY;
      // the card opens towards the free side
      var cardW = 260;
      s.classList.toggle('is-r', wide ? x - cardW < limit : x < vw / 2);
    });
  }
  var rz = 0;
  function layout() { cancelAnimationFrame(rz); rz = requestAnimationFrame(function () { placeFill(); placeSpots(); }); }
  window.addEventListener('resize', layout);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(layout);
  window.addEventListener('load', layout);
  layout();

  /* ---------- touch: swipe the stage ---------- */
  var sx = null, sy = 0;
  stage.addEventListener('pointerdown', function (e) { if (e.pointerType === 'touch') { sx = e.clientX; sy = e.clientY; } });
  stage.addEventListener('pointerup', function (e) {
    if (sx === null) return;
    var dx = e.clientX - sx, dy = e.clientY - sy; sx = null;
    if (Math.abs(dx) > 48 && Math.abs(dx) > Math.abs(dy) * 1.4) show((current + (dx < 0 ? 1 : -1) + slides.length) % slides.length);
  });

  /* ---------- scroll: the sheet lifts off as block 2 arrives ---------- */
  var tick = false;
  function onScroll() {
    tick = false;
    var h = root.offsetHeight || 1, p = Math.min(1, Math.max(0, window.scrollY / h));
    root.style.setProperty('--sp', p.toFixed(4));
  }
  window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  root.classList.add('is-ready');
  setPaused(false);
  restartClock();
})();
