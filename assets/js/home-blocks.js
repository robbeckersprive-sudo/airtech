/* Airtechnic "Flow" — home blocks 2 "Processchema" and 3 "Röntgen" (src/home_blocks.py, assets/css/home-blocks.css). */
(function () {
  'use strict';
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)');

  /* arrival: lines draw, stations come in one by one (CSS on .is-in) */
  var arrive = $$('[data-sx], [data-cx]');
  if (!('IntersectionObserver' in window) || reduce.matches) arrive.forEach(function (s) { s.classList.add('is-in'); });
  else {
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -18% 0px' });
    arrive.forEach(function (s) { io.observe(s); });
  }

  /* ---------- block 2: a station fills the inspector plate ---------- */
  var sx = document.querySelector('[data-sx]');
  if (sx) {
    var nodes = $$('[data-sx-key]', sx), items = $$('[data-sx-item]', sx), last = null;
    var show = function (node) {
      if (node === last) return;
      last = node;
      var key = node.getAttribute('data-sx-key');
      nodes.forEach(function (n) { n.classList.toggle('is-on', n === node); });
      items.forEach(function (it) { it.classList.toggle('is-on', it.getAttribute('data-sx-item') === key); });
      sx.setAttribute('data-lane', node.closest('.sx-lane--air') ? 'air' : 'product');
    };
    nodes.forEach(function (n) {
      n.addEventListener('pointerenter', function () { if (fine.matches) show(n); });
      n.addEventListener('focus', function () { show(n); });
    });
    var start = $$('.sx-node.is-on', sx)[0];
    if (start) { last = null; show(start); }
  }

  /* ---------- block 3: the scan line ---------- */
  var cx = document.querySelector('[data-cx]');
  if (!cx) return;
  var cards = $$('[data-cx-card]', cx), deck = cx.querySelector('[data-cx-deck]');
  var dots = $$('[data-cx-dot]', cx), fill = cx.querySelector('[data-cx-fill]');
  var deckMode = window.matchMedia('(max-width: 899px)');
  var setX = function (card, x) { card.style.setProperty('--x', (Math.max(0, Math.min(1, x)) * 100).toFixed(2) + '%'); };

  cards.forEach(function (card) {
    var plate = card.querySelector('.cx-plate'), wipe = card.getAttribute('data-scan') === 'wipe';
    card.addEventListener('pointerenter', function (e) {
      if (e.pointerType === 'touch' || deckMode.matches) return;
      card.classList.add('is-scan');
      if (wipe) setX(card, 1);
    });
    card.addEventListener('pointermove', function (e) {
      if (e.pointerType === 'touch' || deckMode.matches || wipe) return;
      var r = plate.getBoundingClientRect();
      card.classList.add('is-live');                     // follow the pointer without easing
      setX(card, (e.clientX - r.left) / r.width);
    });
    card.addEventListener('pointerleave', function () {
      if (deckMode.matches) return;
      card.classList.remove('is-scan', 'is-live');
      setX(card, 0);
    });
    // keyboard: focusing a sheet opens it halfway
    card.addEventListener('focus', function () { if (!deckMode.matches) { card.classList.add('is-scan'); setX(card, wipe ? 1 : .5); } });
    card.addEventListener('blur', function () { if (!deckMode.matches) { card.classList.remove('is-scan'); setX(card, 0); } });
  });

  /* phones / tablets: a swipe deck; the swipe itself moves the scan line across the sheet in the middle */
  var ticking = false, active = -1;
  function onDeck() {
    ticking = false;
    if (!deckMode.matches) return;
    // vertical grids (componenten.html, data-cx-vertical): the page scroll moves the scan; decks: the sideways swipe
    var vertical = deck.hasAttribute('data-cx-vertical'), vh = window.innerHeight;
    var dr = deck.getBoundingClientRect(), mid = vertical ? vh * .5 : dr.left + dr.width / 2, best = 1e9;
    cards.forEach(function (card, i) {
      var r = card.getBoundingClientRect(), c = vertical ? r.top + r.height / 2 : r.left + r.width / 2;
      var d = (c - mid) / (vertical ? vh * .55 : r.width);   // -1 .. 1 around the middle
      var wipe = card.getAttribute('data-scan') === 'wipe';
      // centred sheet: half cut; arriving from the right it opens, leaving to the left it closes again
      var x = reduce.matches ? .5 : (wipe ? (Math.abs(d) < .25 ? 1 : 0) : .5 - d * .9);
      setX(card, x);
      card.classList.toggle('is-scan', Math.abs(d) < .6);
      if (Math.abs(d) < best) { best = Math.abs(d); active = i; }
    });
    dots.forEach(function (b, i) { b.classList.toggle('is-on', i === active); });
    if (fill && dots[active]) {
      var pr = fill.parentElement.getBoundingClientRect(), br = dots[active].getBoundingClientRect();
      fill.style.width = Math.max(0, br.left + br.width / 2 - pr.left) + 'px';
    }
  }
  (deck.hasAttribute('data-cx-vertical') ? window : deck).addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onDeck); } }, { passive: true });
  dots.forEach(function (b, i) {
    b.addEventListener('click', function () {
      var card = cards[i].parentElement;
      deck.scrollTo({ left: card.offsetLeft - (deck.clientWidth - card.offsetWidth) / 2, behavior: reduce.matches ? 'auto' : 'smooth' });
    });
  });
  function reset() {
    if (deckMode.matches) onDeck();
    else cards.forEach(function (c) { c.classList.remove('is-scan', 'is-live'); setX(c, 0); });
  }
  deckMode.addEventListener('change', reset);
  window.addEventListener('resize', function () { if (!ticking) { ticking = true; requestAnimationFrame(onDeck); } });
  window.addEventListener('load', reset);
  reset();
})();
