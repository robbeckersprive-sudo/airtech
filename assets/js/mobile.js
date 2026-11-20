/* Airtechnic Solutions — mobile layer (Nov 20). Vanilla, no dependencies; styles in assets/css/mobile.css.
   1. Full-screen menu "Tekenblad": drawn down behind a scan line, numbered index, drill-in panes, focus kept inside.
   2. Home hero: swipe between the five sheets (uses the slide tabs, so site.js stays the one source of truth).
   3. Breadcrumbs: one scrollable line, scrolled so the current page shows.
   4. Contact dock: call + "Stel uw vraag" in thumb reach once the hero is gone; steps aside for the contact
      section, the footer, the menu and the on-screen keyboard. */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  var phone = window.matchMedia('(max-width: 759px)');

  /* ---------- 1. Menu ---------- */
  var hx = $('[data-site-header]');
  var burger = hx && $('[data-hx-burger]', hx);
  var menu = hx && $('[data-hx-sheet]', hx);
  var menuApi = { isOpen: function () { return false; } };
  if (burger && menu) {
    var root = $('[data-mnav-pane="root"]', menu);
    var outside = function () { return [$('main'), $('footer'), $('.skip-link'), $('[data-mdock]')].filter(Boolean); };
    var isOpen = false, closeT = 0, opener = null;
    var CLOSE_MS = 520;

    var setOutsideInert = function (on) {
      outside().forEach(function (el) { if (on) el.setAttribute('inert', ''); else el.removeAttribute('inert'); });
    };
    var showPane = function (key, focus) {
      var target = key === 'root' ? root : $('#mnav-' + key, menu);
      if (!target) return;
      menu.setAttribute('data-pane', key);
      $$('[data-mnav-pane]', menu).forEach(function (p) {
        var on = p === target;
        if (on) { p.hidden = false; p.removeAttribute('inert'); }
        else {
          p.setAttribute('inert', '');
          if (p !== root) setTimeout(function () { if (menu.getAttribute('data-pane') !== p.getAttribute('data-mnav-pane')) p.hidden = true; }, 600);
        }
      });
      $$('[data-mnav-open]', menu).forEach(function (b) { b.setAttribute('aria-expanded', String(b.getAttribute('data-mnav-open') === key)); });
      $('.mnav__body', menu).scrollTop = 0;
      if (focus) setTimeout(function () { focus.focus({ preventScroll: true }); }, reduce.matches ? 0 : 320);
    };
    var open = function () {
      if (isOpen) return;
      isOpen = true;
      clearTimeout(closeT);
      var bar = $('.hxb-bar', hx);
      if (bar) menu.style.setProperty('--mnav-top', Math.round(bar.getBoundingClientRect().bottom) + 'px');
      menu.hidden = false;
      menu.classList.remove('is-closing');
      showPane('root');
      void menu.offsetWidth;   // commit the closed state so the open state transitions
      requestAnimationFrame(function () { menu.classList.add('is-open'); });
      hx.classList.add('is-mnav');
      document.body.classList.add('hx-lock');
      burger.setAttribute('aria-expanded', 'true');
      burger.setAttribute('aria-label', 'Menu sluiten');
      setOutsideInert(true);
      var first = $('.mnav__item', menu);
      if (first) setTimeout(function () { first.focus({ preventScroll: true }); }, reduce.matches ? 0 : 420);
    };
    var close = function (instant, keepFocus) {
      if (!isOpen) return;
      isOpen = false;
      menu.classList.remove('is-open');
      burger.setAttribute('aria-expanded', 'false');
      burger.setAttribute('aria-label', 'Menu openen');
      setOutsideInert(false);
      var done = function () {
        menu.hidden = true; menu.classList.remove('is-closing'); menu.style.viewTransitionName = '';
        hx.classList.remove('is-mnav');
        document.body.classList.remove('hx-lock');
        showPane('root');
      };
      if (instant || reduce.matches) { done(); }
      else { menu.classList.add('is-closing'); closeT = setTimeout(done, CLOSE_MS); document.body.classList.remove('hx-lock'); }
      if (!keepFocus) burger.focus({ preventScroll: true });
    };
    menuApi.isOpen = function () { return isOpen; };

    burger.addEventListener('click', function () { if (isOpen) close(); else open(); });
    $$('[data-mnav-open]', menu).forEach(function (b) {
      b.addEventListener('click', function () {
        opener = b;
        var key = b.getAttribute('data-mnav-open');
        showPane(key, $('#mnav-' + key + ' [data-mnav-back]', menu));
      });
    });
    $$('[data-mnav-back]', menu).forEach(function (b) {
      b.addEventListener('click', function () { showPane('root', opener); });
    });
    // same-page anchors close the menu first; other pages leave it open so it can lift away in the page transition
    $$('a[href]', menu).forEach(function (a) {
      a.addEventListener('click', function () {
        var samePage = a.pathname === location.pathname && a.hash;
        if (samePage || !('onpagereveal' in window)) close(true, true);
      });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape' || !isOpen) return;
      if (menu.getAttribute('data-pane') && menu.getAttribute('data-pane') !== 'root') showPane('root', opener);
      else close();
    });
    window.matchMedia('(min-width: 1040px)').addEventListener('change', function (m) { if (m.matches) close(true, true); });
    // back/forward cache brings the page back as it was left: with the menu open
    window.addEventListener('pageshow', function (e) { if (e.persisted && isOpen) close(true, true); });
  }

  /* ---------- 2. Home hero: swipe between sheets ---------- */
  var hero = $('[data-hero-slides]');
  if (hero) {
    var tabs = $$('[data-tab]', hero);
    var sx = 0, sy = 0, st = 0, tracking = false;
    hero.addEventListener('touchstart', function (e) {
      if (e.touches.length !== 1) { tracking = false; return; }
      tracking = true; sx = e.touches[0].clientX; sy = e.touches[0].clientY; st = Date.now();
    }, { passive: true });
    hero.addEventListener('touchend', function (e) {
      if (!tracking || !tabs.length) return;
      tracking = false;
      var t = e.changedTouches[0], dx = t.clientX - sx, dy = t.clientY - sy;
      if (Math.abs(dx) < 48 || Math.abs(dx) < Math.abs(dy) * 1.4 || Date.now() - st > 800) return;
      var cur = tabs.findIndex(function (b) { return b.hasAttribute('aria-current'); });
      var next = (cur + (dx < 0 ? 1 : -1) + tabs.length) % tabs.length;
      hero.classList.add('is-swiped');
      tabs[next].click();
    }, { passive: true });
  }

  /* ---------- 3. Breadcrumbs: show the current page ---------- */
  var crumbs = function () {
    if (!phone.matches) return;
    $$('.breadcrumb').forEach(function (ol) { ol.scrollLeft = ol.scrollWidth; });
  };
  crumbs();
  phone.addEventListener('change', crumbs);

  /* ---------- 4. Contact dock ---------- */
  var tel = menu && $('.mnav__quick a[href^="tel:"]', menu);
  var ctaIcon = menu && $('.mnav__cta .btn__icon', menu);
  if (tel && ctaIcon && !document.documentElement.classList.contains('no-dock')) {
    var contact = document.getElementById('contact');
    var dock = document.createElement('div');
    dock.className = 'mdock';
    dock.setAttribute('data-mdock', '');
    dock.setAttribute('role', 'region');
    dock.setAttribute('aria-label', 'Snel contact');
    dock.innerHTML =
      '<a class="mdock__call" href="' + tel.getAttribute('href') + '" aria-label="Bel Airtechnic Solutions">' + $('svg', tel).outerHTML + '</a>' +
      '<a class="mdock__cta" href="' + (contact ? '#contact' : 'index.html#contact') + '"><span>Stel uw vraag</span>' + ctaIcon.outerHTML + '</a>';
    document.body.appendChild(dock);
    var blockers = new Set();
    var typing = false;
    var update = function () {
      var show = phone.matches && window.scrollY > window.innerHeight * 0.85 && !blockers.size && !typing && !menuApi.isOpen();
      dock.classList.toggle('is-on', show);
      if (show) { dock.removeAttribute('inert'); dock.removeAttribute('aria-hidden'); }
      else { dock.setAttribute('inert', ''); dock.setAttribute('aria-hidden', 'true'); }
    };
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { if (en.isIntersecting) blockers.add(en.target); else blockers.delete(en.target); });
        update();
      }, { rootMargin: '0px 0px -10% 0px' });
      [contact, $('footer'), $('.mnav__foot')].forEach(function (el) { if (el) io.observe(el); });
    }
    document.addEventListener('focusin', function (e) { typing = !!(e.target.matches && e.target.matches('input, textarea, select')); update(); });
    document.addEventListener('focusout', function () { typing = false; setTimeout(update, 50); });
    var ticking = false;
    window.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () { ticking = false; update(); });
    }, { passive: true });
    phone.addEventListener('change', update);
    if (burger) burger.addEventListener('click', function () { setTimeout(update, 0); });
    update();
  }
})();
