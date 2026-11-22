/* Airtechnic "Flow" — product section nav as a reading line (Nov 22, component-detail.css "STICKY NAV").
   - .is-stuck once the bar sticks under the header (compact, frosted, shadow);
   - one pill glides to the current station (site.js scrollspy sets aria-current);
   - the line is drawn as separate segments in the free space BETWEEN the stations (never under a label); each segment
     fills red as you read from one section to the next, with a granule riding the head of the active one;
     stations already read get a filled dot. */
(function () {
  'use strict';
  var nav = document.querySelector('.detail-nav');
  if (!nav) return;
  var list = nav.querySelector('.subnav__list'), links = Array.prototype.slice.call(list.querySelectorAll('a'));
  var secs = links.map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); });
  var pill = document.createElement('span'); pill.className = 'dn-pill'; pill.setAttribute('aria-hidden', 'true');
  list.prepend(pill);
  var segs = links.slice(1).map(function () {
    var s = document.createElement('span'); s.className = 'dn-seg'; s.setAttribute('aria-hidden', 'true');
    s.innerHTML = '<b class="dn-seg__fill"></b><i class="dn-seg__head"></i>';
    list.prepend(s); return s;
  });
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)'), tick = false, GAP = 10;

  function box(a) { var lr = list.getBoundingClientRect(), r = a.getBoundingClientRect(); return { l: r.left - lr.left + list.scrollLeft, r: r.right - lr.left + list.scrollLeft, w: r.width }; }
  function frame() {
    tick = false;
    var top = parseFloat(getComputedStyle(nav).top) || 0;
    nav.classList.toggle('is-stuck', nav.getBoundingClientRect().top <= top + 1 && window.scrollY > 40);
    // reading position in "stations": i + f
    var line = nav.getBoundingClientRect().bottom + 40, i = 0, f = 0;
    secs.forEach(function (s, k) { if (s && s.getBoundingClientRect().top <= line) i = k; });
    var s = secs[i], next = secs[i + 1];
    if (s && next) { var a = s.getBoundingClientRect().top, b = next.getBoundingClientRect().top; f = Math.min(1, Math.max(0, (line - a) / Math.max(1, b - a))); }
    var pos = i + f, boxes = links.map(box);
    segs.forEach(function (seg, k) {
      var from = boxes[k].r + GAP, to = boxes[k + 1].l - GAP, w = Math.max(0, to - from), q = Math.min(1, Math.max(0, pos - k));
      seg.style.left = from + 'px'; seg.style.width = w + 'px';
      seg.style.setProperty('--q', q.toFixed(3));
      seg.classList.toggle('is-live', q > 0 && q < 1);
    });
    links.forEach(function (l, k) { l.classList.toggle('is-read', k < i); });
    var cur = links.filter(function (l) { return l.hasAttribute('aria-current'); })[0] || links[i];
    var cb = box(cur);
    pill.style.width = cb.w + 'px';
    pill.style.transform = 'translateX(' + cb.l + 'px)';
    list.classList.add('has-pill');
  }
  function req() { if (!tick) { tick = true; requestAnimationFrame(frame); } }
  window.addEventListener('scroll', req, { passive: true });
  window.addEventListener('resize', req);
  list.addEventListener('scroll', req, { passive: true });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(req);
  frame();
  new MutationObserver(function () {
    var cur = list.querySelector('a[aria-current]');
    if (cur && list.scrollWidth > list.clientWidth) list.scrollTo({ left: cur.offsetLeft - (list.clientWidth - cur.offsetWidth) / 2, behavior: reduce.matches ? 'auto' : 'smooth' });
    req();
  }).observe(list, { attributes: true, subtree: true, attributeFilter: ['aria-current'] });
})();
