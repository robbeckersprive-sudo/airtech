/* Airtechnic "Flow" — component category template v2 (src/category_page.py, styles category-overview.css "TEMPLATE V2").
   Toepassing chips dim what does not fit (nothing disappears, so the comparison stays a comparison); the view switch
   shows the same uitvoeringen as cards or as a spec table. */
(function () {
  'use strict';
  var L = function (k, nl, v) { var s = (window.ATI18N || {})[k] || nl; return v ? s.replace(/\{(\w+)\}/g, function (_, n) { return v[n]; }) : s; };
  var root = document.querySelector('[data-cv]');
  if (!root) return;
  var $$ = function (s, c) { return Array.prototype.slice.call((c || root).querySelectorAll(s)); };
  var chips = $$('[data-cv-app]'), items = $$('[data-cv-item]'), count = root.querySelector('[data-cv-count]');
  var cards = root.querySelector('[data-cv-cards]'), table = root.querySelector('[data-cv-table]'), views = $$('[data-cv-view]');
  var total = $$('.cv-card').length;

  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      var app = c.getAttribute('data-cv-app');
      chips.forEach(function (o) { o.setAttribute('aria-pressed', String(o === c)); });
      var n = 0;
      items.forEach(function (it) {
        var fit = !app || (' ' + it.getAttribute('data-toepassing') + ' ').indexOf(' ' + app + ' ') > -1;
        it.classList.toggle('is-dim', !fit);
        if (fit && it.classList.contains('cv-card')) n++;
      });
      if (count) count.textContent = app ? L('countFit', '{n} van {total} uitvoeringen passen', { n: n, total: total })
        : L('countAll', '{n} van {total} uitvoeringen', { n: n, total: total });
    });
  });

  views.forEach(function (v) {
    v.addEventListener('click', function () {
      var t = v.getAttribute('data-cv-view') === 'table';
      views.forEach(function (o) { o.setAttribute('aria-pressed', String(o === v)); });
      cards.hidden = t; table.hidden = !t;
    });
  });

  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -12% 0px' });
    io.observe(root);
  } else root.classList.add('is-in');
})();
