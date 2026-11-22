/* Airtechnic "Flow" — equal heights for names in card rows (Nov 22).
   Elements marked [data-eq] that share a visual row (same top of their card) get the height of the tallest one, so a
   name that wraps to two lines no longer pushes only its own card down. Each kind is grouped separately (by class).
   CSS also balances the line breaks (text-wrap: balance) and clamps at two lines. Recomputed on resize and fonts. */
(function () {
  'use strict';
  var els = Array.prototype.slice.call(document.querySelectorAll('[data-eq]'));
  if (!els.length) return;
  function run() {
    els.forEach(function (e) { e.style.minHeight = ''; });
    var groups = {};
    els.forEach(function (e) {
      if (!e.offsetParent) return;                                   // hidden (e.g. table view)
      var card = e.closest('li, article') || e.parentElement;
      var key = e.className + '|' + Math.round(card.getBoundingClientRect().top + window.scrollY);
      (groups[key] = groups[key] || []).push(e);
    });
    Object.keys(groups).forEach(function (k) {
      var g = groups[k];
      if (g.length < 2) return;
      var max = Math.max.apply(null, g.map(function (e) { return e.offsetHeight; }));
      g.forEach(function (e) { e.style.minHeight = max + 'px'; });
    });
  }
  var t = 0;
  function later() { clearTimeout(t); t = setTimeout(run, 120); }
  run();
  window.addEventListener('resize', later);
  window.addEventListener('load', run);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(run);
})();
