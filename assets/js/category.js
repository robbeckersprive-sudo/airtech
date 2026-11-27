/* Airtechnic "Flow" — component category template v2 (src/category_page.py, styles category-overview.css "TEMPLATE V2").
   Toepassing chips dim what does not fit (nothing disappears, so the comparison stays a comparison); the view switch
   shows the same uitvoeringen as cards or as a spec table.
   Nov 27: an optional second group "Uitvoering" (ATEX / food-grade, [data-cv-exec]) combines with Toepassing using
   AND. It only exists when Airtechnic confirmed data (execution_data.CONFIRMED). The selection is kept in the URL
   (?toepassing=…&uitvoering=…) so a page can link to a filtered view. */
(function () {
  'use strict';
  var L = function (k, nl, v) { var s = (window.ATI18N || {})[k] || nl; return v ? s.replace(/\{(\w+)\}/g, function (_, n) { return v[n]; }) : s; };
  var root = document.querySelector('[data-cv]');
  if (!root) return;
  var $$ = function (s, c) { return Array.prototype.slice.call((c || root).querySelectorAll(s)); };
  var appChips = $$('[data-cv-app]'), execChips = $$('[data-cv-exec]'), items = $$('[data-cv-item]');
  var count = root.querySelector('[data-cv-count]');
  var cards = root.querySelector('[data-cv-cards]'), table = root.querySelector('[data-cv-table]'), views = $$('[data-cv-view]');
  var total = $$('.cv-card').length;
  var state = { app: '', exec: '' };
  var has = function (list, value) { return (' ' + (list || '') + ' ').indexOf(' ' + value + ' ') > -1; };
  var valid = function (chips, attr, value) { return chips.some(function (c) { return c.getAttribute(attr) === value; }) ? value : ''; };

  function apply(updateUrl) {
    appChips.forEach(function (o) { o.setAttribute('aria-pressed', String(o.getAttribute('data-cv-app') === state.app)); });
    execChips.forEach(function (o) { o.setAttribute('aria-pressed', String(o.getAttribute('data-cv-exec') === state.exec)); });
    var n = 0;
    items.forEach(function (it) {
      var fit = (!state.app || has(it.getAttribute('data-toepassing'), state.app)) &&
                (!state.exec || has(it.getAttribute('data-uitvoering'), state.exec));
      it.classList.toggle('is-dim', !fit);
      if (fit && it.classList.contains('cv-card')) n++;
    });
    if (count) count.textContent = (state.app || state.exec) ? L('countFit', '{n} van {total} uitvoeringen passen', { n: n, total: total })
      : L('countAll', '{n} van {total} uitvoeringen', { n: n, total: total });
    if (updateUrl && window.history && history.replaceState) {
      try {
        var url = new URL(location.href);
        ['toepassing', 'uitvoering'].forEach(function (k) { url.searchParams.delete(k); });
        if (state.app) url.searchParams.set('toepassing', state.app);
        if (state.exec) url.searchParams.set('uitvoering', state.exec);
        history.replaceState(history.state, '', url.pathname + url.search + url.hash);
      } catch (e) { /* URL API unavailable: filtering still works */ }
    }
  }

  appChips.forEach(function (c) {
    c.addEventListener('click', function () { state.app = c.getAttribute('data-cv-app'); apply(true); });
  });
  execChips.forEach(function (c) {
    c.addEventListener('click', function () { state.exec = c.getAttribute('data-cv-exec'); apply(true); });
  });

  // Deep link: ?toepassing=<value>&uitvoering=<value>; unknown values are ignored
  try {
    var q = new URLSearchParams(location.search);
    state.app = valid(appChips, 'data-cv-app', q.get('toepassing') || '');
    state.exec = valid(execChips, 'data-cv-exec', q.get('uitvoering') || '');
    if (state.app || state.exec) apply(false);
  } catch (e) { /* no URLSearchParams: start unfiltered */ }

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
