/* Header concepts A / B / C — behaviour. Review build; see tools/header_concepts.py. */
(function () {
  'use strict';
  var hx = document.querySelector('[data-hx]');
  if (!hx) return;
  var kind = hx.getAttribute('data-hx');
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* ---------- scrolled / compact state ---------- */
  function onScroll() {
    var y = window.scrollY;
    hx.classList.toggle('is-scrolled', y > 8);
    hx.classList.toggle('is-compact', y > 56);
  }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---------- dropdown menus (A, B) ---------- */
  var tabs = $$('[data-hx-tab]', hx);
  var panels = {};
  $$('[data-hx-panel]', hx).forEach(function (p) { panels[p.getAttribute('data-hx-panel')] = p; });
  var stage = $('[data-hx-stage]', hx);
  var current = null, closeT = null, openT = null;

  function tabFor(key) { return tabs.filter(function (t) { return t.getAttribute('data-hx-tab') === key; })[0]; }

  function placeStage(key, first) {
    if (!stage) return;
    var p = panels[key], bar = $('[data-hxa]', hx), t = tabFor(key);
    var w = p.offsetWidth, h = p.offsetHeight;
    var bw = bar.clientWidth;
    var bl = bar.getBoundingClientRect().left, tr = t.getBoundingClientRect();
    var center = tr.left + tr.width / 2 - bl;
    var cs = getComputedStyle(bar), inset = parseFloat(cs.paddingLeft) - 24;   // panel text lines up with the logo
    var x = Math.max(Math.min(center - w / 2, bw - w - inset), inset);
    if (w > bw) x = (bw - w) / 2;
    var minX = 10 - bl, maxX = window.innerWidth - 10 - bl - w;   // keep inside the viewport
    x = Math.min(Math.max(x, minX), maxX);
    stage.classList.toggle('no-anim', !!first);
    stage.style.setProperty('--sw', w + 'px');
    stage.style.setProperty('--sh', h + 'px');
    stage.style.setProperty('--sx', x + 'px');
    stage.style.setProperty('--so', Math.round(center - x) + 'px');
  }

  function open(key) {
    clearTimeout(closeT);
    if (current === key) return;
    var prev = current;
    var order = Object.keys(panels);
    Object.keys(panels).forEach(function (k) {
      var p = panels[k], on = k === key;
      if (prev && !reduce) p.style.setProperty('--from', (order.indexOf(k) < order.indexOf(key) ? -40 : 40) + 'px');
      p.classList.toggle('is-on', on);
      if (on) p.removeAttribute('inert'); else p.setAttribute('inert', '');
    });
    tabs.forEach(function (t) { t.setAttribute('aria-expanded', String(t.getAttribute('data-hx-tab') === key)); });
    current = key;
    hx.classList.add('is-menu');
    if (stage) { placeStage(key, !prev); stage.classList.add('is-open'); }
    if (kind === 'b') {
      Object.keys(panels).forEach(function (k) { panels[k].classList.toggle('is-swap', !!prev); });
    }
  }

  function close() {
    if (!current) return;
    Object.keys(panels).forEach(function (k) { panels[k].classList.remove('is-on', 'is-swap'); panels[k].setAttribute('inert', ''); });
    tabs.forEach(function (t) { t.setAttribute('aria-expanded', 'false'); });
    if (stage) stage.classList.remove('is-open');
    hx.classList.remove('is-menu');
    current = null;
    marker(null);
  }

  tabs.forEach(function (t) {
    var key = t.getAttribute('data-hx-tab');
    t.addEventListener('click', function () { current === key ? close() : open(key); });
    if (finePointer) {
      t.addEventListener('pointerenter', function () { clearTimeout(openT); openT = setTimeout(function () { open(key); }, current ? 0 : 90); });
      t.addEventListener('pointerleave', function () { clearTimeout(openT); });
    }
  });
  if (tabs.length) {
    var zone = kind === 'a' ? $('[data-hxa]', hx) : hx;
    if (finePointer) {
      zone.addEventListener('pointerleave', function () { closeT = setTimeout(close, 260); });
      zone.addEventListener('pointerenter', function () { clearTimeout(closeT); });
      $$('.hxa-link:not([data-hx-tab]), .hxb-link:not([data-hx-tab])', hx).forEach(function (a) {
        a.addEventListener('pointerenter', function () { closeT = setTimeout(close, 160); });
      });
    }
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && current) { var t = tabFor(current); close(); t && t.focus(); }
    });
    hx.addEventListener('focusout', function (e) { if (current && !hx.contains(e.relatedTarget)) close(); });
    document.addEventListener('click', function (e) { if (current && !hx.contains(e.target)) close(); });
    window.addEventListener('resize', function () { if (current) placeStage(current, true); });
  }

  /* ---------- A: gliding hover pill ---------- */
  var pill = $('.hxa-pill', hx);
  if (pill) {
    var nav = $('.hxa-nav', hx), pillOn = false;
    var move = function (el) {
      var nr = nav.getBoundingClientRect(), r = el.getBoundingClientRect();
      pill.classList.toggle('no-anim', !pillOn);
      pill.style.setProperty('--px', (r.left - nr.left) + 'px');
      pill.style.setProperty('--pw', r.width + 'px');
      pill.classList.add('is-on'); pillOn = true;
    };
    $$('.hxa-link', hx).forEach(function (l) {
      l.addEventListener('pointerenter', function () { move(l); });
      l.addEventListener('focus', function () { move(l); });
    });
    nav.addEventListener('pointerleave', function () {
      var t = current && tabFor(current);
      if (t) move(t); else { pill.classList.remove('is-on'); pillOn = false; }
    });
  }

  /* ---------- B: ruler marker + figure swap ---------- */
  var mk = $('.hxb-ruler__marker', hx), mkOn = false;
  function marker(el) {
    if (!mk) return;
    if (!el) { mk.classList.remove('is-on'); mkOn = false; return; }
    var rr = mk.parentNode.getBoundingClientRect(), r = el.getBoundingClientRect();
    mk.classList.toggle('no-anim', !mkOn);
    mk.style.setProperty('--mx', (r.left - rr.left + 16) + 'px');
    mk.style.setProperty('--mw', (r.width - 32) + 'px');
    mk.classList.add('is-on'); mkOn = true;
  }
  if (mk) {
    $$('.hxb-link', hx).forEach(function (l) {
      l.addEventListener('pointerenter', function () { marker(l); });
      l.addEventListener('focus', function () { marker(l); });
    });
    $('.hxb-nav', hx).addEventListener('pointerleave', function () { marker(current ? tabFor(current) : null); });
  }
  $$('[data-fig-frame]', hx).forEach(function (fig) {
    var drawer = fig.closest('[data-hx-panel]');
    var links = $$('[data-fig]', drawer);
    var cap = $('[data-fig-cap]', fig), grp = $('[data-fig-grp]', fig);
    var show = function (a) {
      var key = a.getAttribute('data-fig');
      links.forEach(function (l) { l.classList.toggle('is-on', l === a); });
      $$('[data-fig-img]', fig).forEach(function (im) {
        var on = im.getAttribute('data-fig-img') === key;
        im.classList.toggle('is-on', on);
        if (on) { cap.textContent = im.getAttribute('data-cap').replace('&amp;', '&'); grp.textContent = im.getAttribute('data-grp'); }
      });
    };
    links.forEach(function (a) {
      a.addEventListener('pointerenter', function () { show(a); });
      a.addEventListener('focus', function () { show(a); });
    });
    if (links[0]) show(links[0]);
  });

  /* ---------- mobile sheet (A, B) ---------- */
  var burger = $('[data-hx-burger]', hx), sheet = $('[data-hx-sheet]', hx);
  if (burger && sheet) {
    var setSheet = function (on) {
      if (on) {
        var b = kind === 'a' ? $('[data-hxa]', hx).getBoundingClientRect().bottom + 8 : hx.getBoundingClientRect().bottom;
        sheet.style.setProperty('--sheet-top', Math.round(b) + 'px');
      }
      sheet.hidden = !on;
      burger.setAttribute('aria-expanded', String(on));
      burger.setAttribute('aria-label', on ? 'Menu sluiten' : 'Menu openen');
      document.body.classList.toggle('hx-lock', on);
      hx.classList.toggle('is-menu', on);
    };
    burger.addEventListener('click', function () { setSheet(sheet.hidden); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !sheet.hidden) { setSheet(false); burger.focus(); } });
    $$('a', sheet).forEach(function (a) { a.addEventListener('click', function () { setSheet(false); }); });
    window.matchMedia('(min-width: 1040px)').addEventListener('change', function (m) { if (m.matches) setSheet(false); });
  }

  /* ---------- C: full-screen index dialog ---------- */
  var dlg = $('[data-hxc-dialog]', hx);
  if (dlg) {
    var opener = $('[data-hxc-open]', hx);
    var openDlg = function () {
      var r = opener.getBoundingClientRect();
      dlg.style.setProperty('--ox', Math.round(r.left + r.width / 2) + 'px');
      dlg.style.setProperty('--oy', Math.round(r.top + r.height / 2) + 'px');
      dlg.classList.remove('is-closing');
      dlg.showModal();
      opener.setAttribute('aria-expanded', 'true');
      document.body.classList.add('hx-lock');
      requestAnimationFrame(function () { requestAnimationFrame(function () { dlg.classList.add('is-open'); }); });
    };
    var closeDlg = function () {
      if (!dlg.open) return;
      opener.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('hx-lock');
      if (reduce) { dlg.classList.remove('is-open'); dlg.close(); return; }
      dlg.classList.add('is-closing');
      dlg.classList.remove('is-open');
      var done = function (e) {
        if (e && (e.target !== dlg || e.propertyName !== 'clip-path')) return;
        dlg.removeEventListener('transitionend', done); clearTimeout(fb);
        if (!dlg.classList.contains('is-open')) dlg.close();
      };
      var fb = setTimeout(done, 800);
      dlg.addEventListener('transitionend', done);
    };
    opener.addEventListener('click', openDlg);
    $$('[data-hxc-close]', dlg).forEach(function (b) { b.addEventListener('click', closeDlg); });
    dlg.addEventListener('cancel', function (e) { e.preventDefault(); closeDlg(); });
    $$('a[href^="#"]', dlg).forEach(function (a) { a.addEventListener('click', closeDlg); });
    dlg.addEventListener('close', function () { opener.focus(); });

    // index -> peek panel
    var bigs = $$('[data-peek]', dlg), peeks = $$('[data-peek-panel]', dlg);
    var peek = function (key, a) {
      bigs.forEach(function (b) { b.classList.toggle('is-on', b === a); });
      peeks.forEach(function (p) {
        var on = p.getAttribute('data-peek-panel') === key;
        p.classList.toggle('is-on', on);
        if (on) p.removeAttribute('inert'); else p.setAttribute('inert', '');
      });
    };
    peek('default', null);
    bigs.forEach(function (b) {
      b.addEventListener('pointerenter', function () { peek(b.getAttribute('data-peek'), b); });
      b.addEventListener('focus', function () { peek(b.getAttribute('data-peek'), b); });
    });
  }

  /* ---------- C: live section label ---------- */
  var sec = $('[data-hxc-sec]', hx);
  if (sec && 'IntersectionObserver' in window) {
    var named = $$('main section').map(function (s) {
      var e = $('.eyebrow', s); return e ? { el: s, name: e.textContent.trim() } : null;
    }).filter(Boolean);
    var visible = new Map();
    var setLabel = function (name) {
      if (sec.textContent === name) return;
      hx.classList.toggle('has-sec', !!name);
      sec.textContent = name;
      sec.classList.remove('is-in'); void sec.offsetWidth; sec.classList.add('is-in');
    };
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { visible.set(en.target, en.isIntersecting); });
      var hit = named.filter(function (n) { return visible.get(n.el); }).pop();
      setLabel(hit ? hit.name : '');
    }, { rootMargin: '-35% 0px -60% 0px' });
    named.forEach(function (n) { io.observe(n.el); });
  }
})();
