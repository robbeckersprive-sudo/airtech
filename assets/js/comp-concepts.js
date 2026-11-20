/* Block 3 variants A / B / C — review build; see tools/comp_concepts.py.
   A: entry line on the process axis + rail fill per station. B: plates open their registration marks on entry.
   C: section line A-A sweeps with scroll; picks switch the component. Reduced motion: finished states. */
(function () {
  'use strict';
  var sec = document.querySelector('[data-cx]');
  if (!sec) return;
  var kind = sec.getAttribute('data-cx');
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  var clamp01 = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; };
  var track = $('[data-hero-track]');
  var axisX = function () {   // the process axis: the hero plate's left edge
    var v = track && parseFloat(track.style.getPropertyValue('--ix'));
    return isNaN(v) || !v ? document.documentElement.clientWidth * 0.46 : v;
  };
  var tick = false, onFrame = [];
  var frame = function () { tick = false; onFrame.forEach(function (f) { f(); }); };
  window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(frame); } }, { passive: true });

  /* ---------- A ---------- */
  if (kind === 'a') {
    var wide = window.matchMedia('(min-width: 960px)');
    var entry = $('[data-cx-entry]', sec), base = $('.cxA-entry__base', entry), flow = $('.cxA-entry__flow', entry);
    var rail = $('[data-track]', sec), stations = $$('.cxA-st', sec), len = 1, endY = 1, entryDone = false;
    var layout = function () {
      if (!wide.matches) { entryDone = true; fill(); return; }
      var sr = sec.getBoundingClientRect(), node = $('.cxA-st__node', stations[0]).getBoundingClientRect();
      var x0 = axisX() - sr.left, nx = node.left + node.width / 2 - sr.left, ny = node.top + node.height / 2 - sr.top, R = 18;
      var dir = nx < x0 ? -1 : 1, jy = ny;
      var d = 'M' + x0 + ',0 V' + (jy - R) + ' Q' + x0 + ',' + jy + ' ' + (x0 + dir * R) + ',' + jy + ' H' + (nx - dir * (node.width / 2 + 2));
      base.setAttribute('d', d); flow.setAttribute('d', d);
      len = flow.getTotalLength(); endY = jy;
      flow.style.strokeDasharray = len + ' ' + len;
      draw();
    };
    var draw = function () {
      if (!wide.matches) return;
      var tip = window.innerHeight * 0.62 - sec.getBoundingClientRect().top;
      var k = reduce.matches ? 1 : clamp01(tip / endY);
      flow.style.strokeDashoffset = String(len * (1 - k));
      var done = k >= 0.999;
      if (done !== entryDone) { entryDone = done; fill(); }
    };
    // the rail fills station by station: everything up to the last fully visible station, once the line has arrived
    var fill = function () {
      var tr = rail.getBoundingClientRect(), last = -1;
      stations.forEach(function (s, i) { var r = s.getBoundingClientRect(); if (r.right <= tr.right + 4) last = i; });
      stations.forEach(function (s, i) {
        var on = entryDone && i <= last;
        s.classList.toggle('is-on', on);
        s.style.setProperty('--f', entryDone && i < last ? '1' : '0');
        s.style.transitionDelay = '0s';
        s.querySelector('.cxA-st__node').style.transitionDelay = (reduce.matches ? 0 : i * 90) + 'ms';
      });
    };
    rail.addEventListener('scroll', function () { requestAnimationFrame(fill); }, { passive: true });
    onFrame.push(draw);
    layout();
    window.addEventListener('resize', layout);
    window.addEventListener('load', layout);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { requestAnimationFrame(layout); });
    wide.addEventListener('change', layout);
  }

  /* ---------- B ---------- */
  if (kind === 'b') {
    var cells = $$('.cxB-cell', sec);
    if (reduce.matches || !('IntersectionObserver' in window)) cells.forEach(function (c) { c.classList.add('is-in'); });
    else {
      var io = new IntersectionObserver(function (en) {
        en.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
      }, { rootMargin: '0px 0px -15% 0px' });
      cells.forEach(function (c) { io.observe(c); });
    }
  }

  /* ---------- C ---------- */
  if (kind === 'c') {
    var plate = $('[data-cx-plate]', sec), picks = $$('[data-pick]', sec);
    var nameEl = $('[data-cx-name]', sec), viewEl = $('[data-cx-view]', sec), go = $('[data-cx-go]', sec), goName = $('[data-cx-goname]', sec);
    var select = function (btn) {
      var key = btn.getAttribute('data-pick'), layer = null;
      picks.forEach(function (b) { var on = b === btn; b.classList.toggle('is-on', on); b.setAttribute('aria-pressed', String(on)); });
      $$('[data-pick-layer]', plate).forEach(function (l) { var on = l.getAttribute('data-pick-layer') === key; l.classList.toggle('is-on', on); if (on) layer = l; });
      var hasSec = layer.classList.contains('has-sec');
      plate.classList.toggle('has-sec', hasSec);
      var name = btn.getAttribute('data-name').replace('&amp;', '&');
      nameEl.textContent = name; goName.textContent = name;
      viewEl.textContent = hasSec ? 'Doorsnede A–A' : 'Aanzicht';
      go.setAttribute('href', btn.getAttribute('data-href'));
    };
    picks.forEach(function (b) { b.addEventListener('click', function () { select(b); }); });
    select(picks.filter(function (b) { return b.classList.contains('is-on'); })[0] || picks[0]);
    // the section line sweeps in from the left edge and settles mid-plate as the plate scrolls into view
    var cut = function () {
      var r = plate.getBoundingClientRect(), vh = window.innerHeight;
      var k = reduce.matches ? 1 : clamp01((vh * 0.95 - r.top) / (vh * 0.6));
      var e = k * k * (3 - 2 * k);
      plate.style.setProperty('--cut', (e * 50).toFixed(2) + '%');
    };
    onFrame.push(cut);
    cut();
  }
})();
