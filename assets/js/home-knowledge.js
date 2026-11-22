/* Airtechnic "Flow" — home blocks 6 "Vraagbaak" and 7 "Vragen" (src/home_knowledge.py). */
(function () {
  'use strict';
  /* FAQ index (.fq) arrival: also used on category pages, where the kennis block does not exist */
  var fqs = document.querySelectorAll('.fq');
  if (fqs.length) {
    if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      var fio = new IntersectionObserver(function (en) {
        en.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); fio.unobserve(e.target); } });
      }, { rootMargin: '0px 0px -15% 0px' });
      fqs.forEach(function (s) { fio.observe(s); });
    } else fqs.forEach(function (s) { s.classList.add('is-in'); });
  }
  var root = document.querySelector('[data-kq-root]');
  if (!root) return;
  var $$ = function (s, c) { return Array.prototype.slice.call((c || root).querySelectorAll(s)); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)');
  var rows = $$('.kq-row'), chips = $$('[data-kq-topic]'), empty = root.querySelector('[data-kq-empty]');

  /* topic chips filter the index (rows fold away, the rest close up) */
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      var t = c.getAttribute('data-kq-topic'), n = 0;
      chips.forEach(function (o) { o.setAttribute('aria-pressed', String(o === c)); });
      rows.forEach(function (r) {
        var on = t === 'all' || r.getAttribute('data-topic') === t;
        r.classList.toggle('is-out', !on);
        r.querySelector('a').tabIndex = on ? 0 : -1;
        if (on) { r.style.setProperty('--k', n); n++; }
      });
      if (empty) empty.hidden = n > 0;
    });
  });

  /* preview plate: sits in the quiet side column, level with the hovered row, and glides from row to row */
  var side = root.querySelector('.kq-side'), prev = root.querySelector('[data-kq-prev]'), imgs = $$('[data-kq-img]', prev), raf = 0, tx = 0, ty = 0, x = 0, y = 0, live = false;
  function loop() {
    x += (tx - x) * (reduce.matches ? 1 : .18); y += (ty - y) * (reduce.matches ? 1 : .18);
    prev.style.transform = 'translate3d(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px,0)';
    raf = live && (Math.abs(tx - x) > .3 || Math.abs(ty - y) > .3) ? requestAnimationFrame(loop) : 0;
  }
  $$('[data-kq]').forEach(function (a) {
    a.addEventListener('pointerenter', function () {
      if (!fine.matches) return;
      var i = a.getAttribute('data-kq');
      imgs.forEach(function (im) { im.classList.toggle('is-on', im.getAttribute('data-kq-img') === i); });
      // level with the row, but never over the side column's own text; no room left = no preview
      var sr = side.getBoundingClientRect(), rr = a.getBoundingClientRect(), ph = prev.offsetHeight || 225;
      var lo = sr.bottom + 28, hi = window.innerHeight - ph - 24;
      if (lo > hi) { live = false; prev.classList.remove('is-on'); return; }
      tx = sr.left; ty = Math.max(lo, Math.min(hi, rr.top + rr.height / 2 - ph / 2));
      if (!live) { x = tx; y = ty + 24; }
      live = true; prev.classList.add('is-on');
      if (!raf) raf = requestAnimationFrame(loop);
    });
  });
  var list = root.querySelector('[data-kq-list]');
  list.addEventListener('pointerleave', function () { live = false; prev.classList.remove('is-on'); });
  window.addEventListener('scroll', function () { if (live) { live = false; prev.classList.remove('is-on'); } }, { passive: true });

  /* arrival */
  if ('IntersectionObserver' in window && !reduce.matches) {
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -15% 0px' });
    document.querySelectorAll('[data-kq-root]').forEach(function (s) { io.observe(s); });
  } else document.querySelectorAll('[data-kq-root]').forEach(function (s) { s.classList.add('is-in'); });
})();
