/* Airtechnic Solutions — "Flow" behaviour. Vanilla JS, no dependencies.
   Every module is opt-in through data attributes, so pages only pay for what they use. */
(function () {
  'use strict';
  var doc = document.documentElement;
  doc.classList.add('js');
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  var $ = function (sel, ctx) { return (ctx || document).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };

  /* ---------- Header "Doorsnede": scrolled state, drawers, ruler marker, figures, mobile sheet ---------- */
  var hx = $('[data-site-header]');
  if (hx) {
    var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
    var onHxScroll = function () { hx.classList.toggle('is-scrolled', window.scrollY > 8); };
    onHxScroll();
    window.addEventListener('scroll', onHxScroll, { passive: true });

    var tabs = $$('[data-hx-tab]', hx), panels = {};
    $$('[data-hx-panel]', hx).forEach(function (p) { panels[p.getAttribute('data-hx-panel')] = p; });
    var current = null, closeT = null, openT = null;
    var tabFor = function (key) { return tabs.filter(function (t) { return t.getAttribute('data-hx-tab') === key; })[0]; };

    var mk = $('.hxb-ruler__marker', hx), mkOn = false;
    var marker = function (el) {
      if (!mk) return;
      if (!el || !el.offsetWidth) { mk.hidden = true; mk.classList.remove('is-on'); mkOn = false; return; }
      mk.hidden = false;
      var rr = mk.parentNode.getBoundingClientRect(), r = el.getBoundingClientRect();
      mk.classList.toggle('no-anim', !mkOn);
      mk.style.setProperty('--mx', (r.left - rr.left + 16) + 'px');
      mk.style.setProperty('--mw', (r.width - 32) + 'px');
      mk.classList.add('is-on'); mkOn = true;
    };
    var restMarker = function () { marker(current ? tabFor(current) : $('.hxb-link.is-current', hx)); };

    var openPanel = function (key) {
      clearTimeout(closeT);
      if (current === key) return;
      var swap = !!current;
      Object.keys(panels).forEach(function (k) {
        var p = panels[k], on = k === key;
        p.classList.toggle('is-swap', swap);
        p.classList.toggle('is-on', on);
        if (on) p.removeAttribute('inert'); else p.setAttribute('inert', '');
      });
      tabs.forEach(function (t) { t.setAttribute('aria-expanded', String(t.getAttribute('data-hx-tab') === key)); });
      current = key;
      hx.classList.add('is-menu');
      marker(tabFor(key));
    };
    var closePanel = function () {
      if (!current) return;
      Object.keys(panels).forEach(function (k) { panels[k].classList.remove('is-on', 'is-swap'); panels[k].setAttribute('inert', ''); });
      tabs.forEach(function (t) { t.setAttribute('aria-expanded', 'false'); });
      hx.classList.remove('is-menu');
      current = null;
      restMarker();
    };
    tabs.forEach(function (t) {
      var key = t.getAttribute('data-hx-tab');
      t.addEventListener('click', function () { if (current === key) closePanel(); else openPanel(key); });
      if (finePointer) {
        t.addEventListener('pointerenter', function () { clearTimeout(openT); openT = setTimeout(function () { openPanel(key); }, current ? 0 : 90); });
        t.addEventListener('pointerleave', function () { clearTimeout(openT); });
      }
    });
    hx.querySelectorAll('[data-hx-panel] a').forEach(function (link) {
      link.addEventListener('click', closePanel);
    });
    if (finePointer) {
      hx.addEventListener('pointerleave', function () { closeT = setTimeout(closePanel, 260); });
      hx.addEventListener('pointerenter', function () { clearTimeout(closeT); });
      $$('.hxb-link:not([data-hx-tab])', hx).forEach(function (a) {
        a.addEventListener('pointerenter', function () { closeT = setTimeout(closePanel, 160); });
      });
    }
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && current) { var t = tabFor(current); closePanel(); if (t) t.focus(); }
    });
    hx.addEventListener('focusout', function (e) { if (current && !hx.contains(e.relatedTarget)) closePanel(); });
    document.addEventListener('click', function (e) { if (current && !hx.contains(e.target)) closePanel(); });

    if (mk) {
      $$('.hxb-link', hx).forEach(function (l) {
        l.addEventListener('pointerenter', function () { marker(l); });
        l.addEventListener('focus', function () { marker(l); });
      });
      $('.hxb-nav', hx).addEventListener('pointerleave', restMarker);
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(restMarker); else restMarker();
      window.addEventListener('resize', restMarker);
    }

    $$('[data-fig-frame]', hx).forEach(function (fig) {
      var links = $$('[data-fig]', fig.closest('[data-hx-panel]'));
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
      var start = links.filter(function (l) { return l.hasAttribute('aria-current'); })[0] || links[0];
      if (start) show(start);
    });

    // Burger + full-screen mobile menu: assets/js/mobile.js ("Tekenblad" menu, Nov 20).
  }

  /* ---------- Reveal on first entry (sections, split headings, staggered children) ---------- */
  $$('.cards-3, .cat-grid, .chips, .carousel__track, .steps__list, .checklist, .callouts, .hotspots, .contact__lines').forEach(function (c) {
    Array.prototype.forEach.call(c.children, function (ch, i) { ch.style.setProperty('--i', i); });
  });
  var reveals = $$('[data-reveal], [data-split]');
  if (reveals.length) {
    if (!('IntersectionObserver' in window) || reduceMotion.matches) {
      reveals.forEach(function (el) { el.classList.add('is-in'); });
    } else {
      var ro = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('is-in'); ro.unobserve(en.target); } });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
      reveals.forEach(function (el) { ro.observe(el); });
    }
  }

  /* ---------- Hero motion toggle ---------- */
  $$('[data-motion-toggle]').forEach(function (btn) {
    var scope = btn.closest('[data-motion-scope]');
    btn.addEventListener('click', function () {
      var paused = scope.classList.toggle('is-paused');
      btn.setAttribute('aria-pressed', String(paused));
      btn.querySelector('[data-label]').textContent = paused ? 'Animatie afspelen' : 'Animatie pauzeren';
      btn.querySelector('[data-icon-pause]').hidden = paused;
      btn.querySelector('[data-icon-play]').hidden = !paused;
      scope.dispatchEvent(new Event('hero-motion-change'));
    });
  });


  /* ---------- Scroll engine: progress bar, hero scroll-out, parallax, media expansion ---------- */
  var clamp01 = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; };
  var progressBar = $('[data-scroll-progress]');
  var hero = $('[data-hero]');
  var parallax = $$('[data-parallax]');
  var expand = $$('[data-expand]');
  var visible = new WeakMap();
  if ('IntersectionObserver' in window) {
    var vo = new IntersectionObserver(function (entries) { entries.forEach(function (en) { visible.set(en.target, en.isIntersecting); }); }, { rootMargin: '10% 0px' });
    parallax.concat(expand).forEach(function (el) { vo.observe(el); });
  }
  var frame = function () {
    var vh = window.innerHeight, y = window.scrollY;
    if (progressBar) progressBar.style.transform = 'scaleX(' + clamp01(y / Math.max(1, doc.scrollHeight - vh)).toFixed(4) + ')';
    if (reduceMotion.matches) return;
    if (hero && y < hero.offsetHeight * 1.2) hero.style.setProperty('--p', clamp01(y / hero.offsetHeight).toFixed(4));
    parallax.forEach(function (el) {
      if (visible.get(el) === false) return;
      var r = el.getBoundingClientRect();
      el.style.setProperty('--p', clamp01((vh - r.top) / (vh + r.height)).toFixed(4));
    });
    expand.forEach(function (el) {
      if (visible.get(el) === false) return;
      var r = el.getBoundingClientRect();
      el.style.setProperty('--p', clamp01((vh * .95 - r.top) / (vh * .7)).toFixed(4));
    });
  };
  var ticking = false;
  var requestFrame = function () { if (!ticking) { ticking = true; requestAnimationFrame(function () { frame(); ticking = false; }); } };
  window.addEventListener('scroll', requestFrame, { passive: true });
  window.addEventListener('resize', requestFrame);
  frame();

  /* ---------- Pointer micro-interactions (fine pointers only) ---------- */
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  if (finePointer) {
    $$('[data-spotlight]').forEach(function (el) {
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        el.style.setProperty('--mx', (e.clientX - r.left).toFixed(0) + 'px');
        el.style.setProperty('--my', (e.clientY - r.top).toFixed(0) + 'px');
      });
    });
    if (!reduceMotion.matches) {
      $$('[data-magnetic]').forEach(function (el) {
        el.addEventListener('pointermove', function (e) {
          var r = el.getBoundingClientRect();
          el.style.setProperty('--tx', (((e.clientX - r.left) / r.width - .5) * 10).toFixed(1) + 'px');
          el.style.setProperty('--ty', (((e.clientY - r.top) / r.height - .5) * 8).toFixed(1) + 'px');
        });
        el.addEventListener('pointerleave', function () { el.style.setProperty('--tx', '0px'); el.style.setProperty('--ty', '0px'); });
      });
    }
  }

  /* ---------- Hero: hotspot tour + pause the SVG flow when off-screen or reduced motion ---------- */
  if (hero) {
    var svgs = $$('svg[data-flow-svg]', hero);
    var isPaused = function () { return hero.classList.contains('is-paused'); };
    var setSvg = function (run) { svgs.forEach(function (s) { if (!s.pauseAnimations) return; var slide = s.closest("[data-slide]"); if (run && (!slide || slide.classList.contains("is-on"))) s.unpauseAnimations(); else s.pauseAnimations(); }); };
    var onScreen = true;
    var syncSvg = function () { setSvg(onScreen && !document.hidden && !reduceMotion.matches && !isPaused()); };
    syncSvg();
    hero.addEventListener('hero-motion-change', syncSvg);
    document.addEventListener('visibilitychange', syncSvg);
    reduceMotion.addEventListener('change', syncSvg);
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (en) { onScreen = en[0].isIntersecting; syncSvg(); }).observe(hero);
    }
    var spots = $$('.hotspot', hero);
    var spotsWrap = $('.hotspots', hero);
    var hold = false;
    var clearSpots = function () { spots.forEach(function (s) { s.classList.remove('is-active'); }); };
    if (spotsWrap) {
      spotsWrap.addEventListener('pointerenter', function () { hold = true; clearSpots(); });
      spotsWrap.addEventListener('pointerleave', function () { hold = false; });
      spotsWrap.addEventListener('focusin', function () { hold = true; clearSpots(); });
      spotsWrap.addEventListener('focusout', function () { hold = false; });
    }
    /* Hero "Tekenblad": pin progress, measured plate edge, hotspots clipped by the plate, title block */
    var track = $('[data-hero-track]');
    var plate = $('[data-plate]', hero);
    var disc = $('[data-plate-discipline]', hero);
    var setDiscipline = function (spot) {
      if (!disc || !spot) return;
      var t = $('strong', spot).textContent;
      if (disc.textContent === t) return;
      disc.textContent = t;
      disc.classList.remove('is-swap'); void disc.offsetWidth; disc.classList.add('is-swap');
    };
    if (track && plate) {
      var wideHero = window.matchMedia('(min-width: 720px) and (min-aspect-ratio: 6/5)');
      var typeEls = $$('.hero__eyebrow, .hero__title .ln__in, .hero__sub, .hero__actions > *', hero);
      var qTick = false, lastQ = -1;
      var measurePlate = function () {
        if (!wideHero.matches) return;
        var right = 0;
        var range = document.createRange();   // text extent, not the (wider) block boxes
        typeEls.forEach(function (el) { range.selectNodeContents(el); right = Math.max(right, range.getBoundingClientRect().right); });
        var vw = document.documentElement.clientWidth;
        var x = Math.min(Math.max(right + 64, vw * 0.42), vw * 0.6);
        var box = $('.hero__content', hero), bs = getComputedStyle(box);
        var ir = Math.max(vw - (box.getBoundingClientRect().right - parseFloat(bs.paddingRight)), 16);   // align with the content edge
        var iy = (parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--header-h')) || 72) + 44;
        var w = vw - x - ir, h = hero.offsetHeight - iy - 124;
        var extra = Math.max(h - w * 1.25, 0);       // never taller than 4:5: share the spare height above and below
        var ib = 124 + extra * 0.6;
        track.style.setProperty('--iy', Math.round(iy + extra * 0.4) + 'px');
        track.style.setProperty('--ix', Math.round(x) + 'px');
        track.style.setProperty('--ir', Math.round(ir) + 'px');
        track.style.setProperty('--ib', Math.round(ib) + 'px');
      };
      var clipSpots = function (q) {
        var pr = plate.getBoundingClientRect();
        spots.forEach(function (sp) {
          var d = $('.hotspot__dot', sp).getBoundingClientRect();
          var out = wideHero.matches && q > 0.5 && (d.left < pr.left || d.right > pr.right || d.top < pr.top || d.bottom > pr.bottom);
          if (out === sp.classList.contains('is-clipped')) return;
          sp.classList.toggle('is-clipped', out);
          sp.classList.remove('is-active');
          if (out) sp.setAttribute('inert', ''); else sp.removeAttribute('inert');
        });
      };
      var updatePlate = function () {
        qTick = false;
        var q;
        if (!wideHero.matches) q = 0;
        else if (reduceMotion.matches) q = 1;
        else {
          var r = track.getBoundingClientRect(), span = r.height - window.innerHeight;
          q = span > 0 ? clamp01(-r.top / span) : 1;
        }
        if (Math.abs(q - lastQ) < 0.0005) return;
        lastQ = q;
        var qe = q * q * (3 - 2 * q);   // smoothstep: the fold starts and lands softly
        track.style.setProperty('--q', q.toFixed(4));
        track.style.setProperty('--qe', qe.toFixed(4));
        clipSpots(q);
      };
      var reflow = function () { measurePlate(); lastQ = -1; updatePlate(); };
      reflow();
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(reflow);
      window.addEventListener('scroll', function () { if (!qTick) { qTick = true; requestAnimationFrame(updatePlate); } }, { passive: true });
      window.addEventListener('resize', reflow);
      wideHero.addEventListener('change', reflow);
      reduceMotion.addEventListener('change', reflow);
    }
    /* Hero slides: five photos share the stage. The active tab's fill line is the clock (CSS animation, paused by the
       pause button, hover/focus on the copy or the tabs, and off-screen); its animationend advances the slide.
       A photo wipes in from the equipment side behind a scan line, the statement swaps line by line, and the plate's
       title block follows (Discipline, Blad). Reduced motion: no autoplay, instant swaps via the tabs. */
    var slidesRoot = hero.hasAttribute('data-hero-slides') ? hero : null;
    var slideEls = $$('[data-slide]', hero);
    var cur = 0;
    var currentSpots = function () { return slidesRoot ? $$('.hotspot', slideEls[cur]) : spots; };
    var k = -1, tourTimer = 0;
    var tour = function () {
      var list = currentSpots();
      if (!list.length || hold || isPaused() || !onScreen || reduceMotion.matches) return;
      clearSpots();
      for (var n = 0; n < list.length; n++) {
        k = (k + 1) % list.length;
        var s = list[k];
        if (getComputedStyle(s).display !== 'none' && !s.classList.contains('is-clipped')) {
          s.classList.add('is-active');
          if (!slidesRoot) setDiscipline(s);
          return;
        }
      }
    };
    var startTour = function (delay) {
      clearTimeout(tourTimer); clearInterval(tourTimer); k = -1;
      tourTimer = setTimeout(function () { tour(); tourTimer = setInterval(tour, 3600); }, delay);
    };
    if (spots.length && !reduceMotion.matches) startTour(2800);

    if (slidesRoot && slideEls.length > 1) {
      var copies = $$('[data-copy]', hero), mores = $$('[data-more]', hero), tabs = $$('[data-tab]', hero);
      var heroSheetNumber = $('[data-plate-sheet]', hero);
      var WIPE = 1400, busy = false;
      var setOn = function (el, on) {
        el.classList.toggle('is-on', on);
        if (on) { el.removeAttribute('aria-hidden'); el.removeAttribute('inert'); }
        else { el.setAttribute('aria-hidden', 'true'); el.setAttribute('inert', ''); }
      };
      var KEY = 'airtechnic-hero-slide';   // returning visitors reopen the sheet they last saw (functional, no tracking)
      var go = function (next, opening) {
        next = (next + slideEls.length) % slideEls.length;
        if (next === cur || busy) return;
        var prev = cur, instant = reduceMotion.matches || !!opening;
        try { if (!Number.isInteger(previewSlide)) localStorage.setItem(KEY, String(next)); } catch (e) { /* storage blocked: sheet 1 next time */ }
        cur = next;
        clearSpots();
        // photo: the incoming slide wipes in over the outgoing one
        var a = slideEls[prev], b = slideEls[next];
        if (!instant) {
          busy = true;
          a.classList.add('is-leaving');
          b.classList.add('is-entering');
          setTimeout(function () { a.classList.remove('is-leaving'); b.classList.remove('is-entering'); busy = false; }, WIPE);
        }
        setOn(a, false); setOn(b, true);
        syncSvg();
        // statement: outgoing lines leave upwards, then reset below the mask while invisible
        var ca = copies[prev], cb = copies[next];
        if (!instant) {
          ca.classList.add('is-out');
          setTimeout(function () {
            ca.classList.add('no-anim'); ca.classList.remove('is-out'); void ca.offsetWidth; ca.classList.remove('no-anim');
          }, 900);
        }
        setOn(ca, false); setOn(cb, true);
        setOn(mores[prev], false); setOn(mores[next], true);
        // tabs + title block
        tabs.forEach(function (t, i) { if (i === next) t.setAttribute('aria-current', 'true'); else t.removeAttribute('aria-current'); });
        if (disc) {
          disc.innerHTML = cb.getAttribute('data-discipline');
          disc.classList.remove('is-swap'); void disc.offsetWidth; disc.classList.add('is-swap');
        }
        if (heroSheetNumber) heroSheetNumber.textContent = (next < 9 ? '0' : '') + (next + 1);
        if (!instant) startTour(1500);
        else if (opening) startTour(2800);
      };
      // reopen the last sheet without a wipe, before the copy reveal runs; its photo loads eagerly
      var saved = -1;
      try { saved = parseInt(localStorage.getItem(KEY), 10); } catch (e) { /* no storage */ }
      var preview = new URLSearchParams(location.search).get("preview");
      var previewSlide = { cycloon: 3, doseersluis: 4 }[preview];
      if (Number.isInteger(previewSlide)) saved = previewSlide;
      if (saved > 0 && saved < slideEls.length) {
        $$('img', slideEls[saved]).forEach(function (im) { im.loading = 'eager'; im.fetchPriority = 'high'; });
        go(saved, true);
      }
      tabs.forEach(function (t, i) {
        t.addEventListener('click', function () { go(i); });
        $('.hero-tab__fill', t).addEventListener('animationend', function () {
          if (!Number.isInteger(previewSlide) && !reduceMotion.matches && t.hasAttribute('aria-current')) go(cur + 1);
        });
      });
      // arrow keys move between the tab buttons
      $('.hero-tabs', hero).addEventListener('keydown', function (e) {
        var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (!d) return;
        e.preventDefault();
        var i = (tabs.indexOf(document.activeElement) + d + tabs.length) % tabs.length;
        tabs[i].focus(); go(i);
      });
      // hold the clock while the visitor reads, points at or tabs through the copy and the controls
      var holdZones = [$('.hero__inner', hero), $('.hero__bar', hero), $('.hotspots', slideEls[0])].filter(Boolean);
      // touch screens keep :hover after a tap, which would hold the clock for good: only real pointers count there
      var canHover = window.matchMedia('(hover: hover)');
      var setHold = function () {
        hero.classList.toggle('is-holding', holdZones.some(function (z) { return (canHover.matches && z.matches(':hover')) || !!z.querySelector(':focus-visible'); }));
      };
      holdZones.forEach(function (z) {
        ['pointerenter', 'pointerleave', 'focusin', 'focusout'].forEach(function (ev) { z.addEventListener(ev, function () { setTimeout(setHold, 0); }); });
      });
      $$('.hotspots', hero).forEach(function (z) {
        z.addEventListener('pointerenter', function (e) { if (e.pointerType !== 'touch') hero.classList.add('is-holding'); });
        z.addEventListener('pointerleave', function () { setTimeout(setHold, 0); });
      });
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (en) { hero.classList.toggle('is-offscreen', !en[0].isIntersecting); }, { threshold: 0.2 }).observe(hero);
      }
    }
  }

  /* ---------- Carousel (scroll-snap, buttons, keyboard, counter) ---------- */
  $$('[data-carousel]').forEach(function (root) {
    var track = $('[data-track]', root);
    var slides = $$('[data-slide]', track);
    var prevs = $$('[data-prev]', root), nexts = $$('[data-next]', root);
    var count = $('[data-count]', root);
    var step = function () { return slides[0].getBoundingClientRect().width + parseFloat(getComputedStyle(track).columnGap || 0); };
    var state = function () {
      var s = step();
      var first = Math.round(track.scrollLeft / s);
      var gap = parseFloat(getComputedStyle(track).columnGap || 0);
      var visible = Math.max(1, Math.floor((track.clientWidth + gap + 2) / s));
      var last = Math.min(slides.length, first + visible);
      return { first: first, last: last, visible: visible };
    };
    var update = function () {
      var st = state();
      if (count) count.textContent = (st.first + 1) + (st.last > st.first + 1 ? ' – ' + st.last : '') + ' van ' + slides.length;
      var atStart = track.scrollLeft <= 2;
      var atEnd = track.scrollLeft + track.clientWidth >= track.scrollWidth - 2;
      prevs.forEach(function (b) { b.disabled = atStart; });
      nexts.forEach(function (b) { b.disabled = atEnd; });
    };
    var go = function (dir) {
      var st = state();
      track.scrollTo({ left: Math.max(0, (st.first + dir * st.visible)) * step(), behavior: reduceMotion.matches ? 'auto' : 'smooth' });
    };
    prevs.forEach(function (b) { b.addEventListener('click', function () { go(-1); }); });
    nexts.forEach(function (b) { b.addEventListener('click', function () { go(1); }); });
    track.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); go(1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); go(-1); }
    });
    var t; track.addEventListener('scroll', function () { clearTimeout(t); t = setTimeout(update, 60); }, { passive: true });
    window.addEventListener('resize', update);
    update();
  });

  /* ---------- Tabs (horizontal or vertical; ARIA tabs pattern, automatic activation) ---------- */
  $$('[data-tabs]').forEach(function (root) {
    var tabs = $$('[role="tab"]', root);
    var vertical = root.getAttribute('data-tabs') === 'vertical';
    var activate = function (tab, focus) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute('aria-selected', String(on));
        t.tabIndex = on ? 0 : -1;
        var panel = document.getElementById(t.getAttribute('aria-controls'));
        if (!panel) return;
        if (panel.hasAttribute('data-crossfade')) { panel.classList.toggle('is-active', on); panel.setAttribute('aria-hidden', String(!on)); }
        else panel.hidden = !on;
      });
      if (focus) tab.focus();
      var list = tab.parentElement;
      list.style.setProperty('--tx', tab.offsetLeft + 'px');
      list.style.setProperty('--tw', tab.offsetWidth + 'px');
    };
    var placeSel = function () {
      var cur = tabs.filter(function (t) { return t.getAttribute('aria-selected') === 'true'; })[0];
      if (!cur) return;
      cur.parentElement.style.setProperty('--tx', cur.offsetLeft + 'px');
      cur.parentElement.style.setProperty('--tw', cur.offsetWidth + 'px');
    };
    placeSel();
    window.addEventListener('resize', placeSel);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(placeSel);
    tabs.forEach(function (tab, i) {
      tab.addEventListener('click', function () { activate(tab); });
      tab.addEventListener('keydown', function (e) {
        var next = vertical ? 'ArrowDown' : 'ArrowRight', prev = vertical ? 'ArrowUp' : 'ArrowLeft', idx = null;
        if (e.key === next) idx = (i + 1) % tabs.length;
        else if (e.key === prev) idx = (i - 1 + tabs.length) % tabs.length;
        else if (e.key === 'Home') idx = 0;
        else if (e.key === 'End') idx = tabs.length - 1;
        if (idx !== null) { e.preventDefault(); activate(tabs[idx], true); }
      });
    });
  });

  /* ---------- Scrollspy (article TOC, product sub-navigation) ---------- */
  $$('[data-scrollspy]').forEach(function (nav) {
    var links = $$('a[href^="#"]', nav);
    var map = links.map(function (a) { return { a: a, el: document.getElementById(a.getAttribute('href').slice(1)) }; }).filter(function (m) { return m.el; });
    if (!map.length) return;
    var offset = parseInt(nav.getAttribute('data-scrollspy'), 10) || 140;
    var setActive = function () {
      var current = map[0];
      map.forEach(function (m) { if (m.el.getBoundingClientRect().top - offset <= 0) current = m; });
      if (window.innerHeight + window.scrollY >= document.body.scrollHeight - 4) current = map[map.length - 1];
      map.forEach(function (m) { if (m === current) m.a.setAttribute('aria-current', 'true'); else m.a.removeAttribute('aria-current'); });
      if (nav.hasAttribute('data-scroll-into-view') && current.a.scrollIntoView && nav.scrollWidth > nav.clientWidth) {
        var list = current.a.parentElement.parentElement;
        list.scrollLeft = current.a.offsetLeft - 16;
      }
    };
    var ticking = false;
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(function () { setActive(); ticking = false; }); } }, { passive: true });
    setActive();
  });

  /* ---------- Share (Web Share API, fallback copy-link) ---------- */
  $$('[data-share]').forEach(function (btn) {
    var status = btn.parentElement.querySelector('[data-share-status]');
    btn.addEventListener('click', function () {
      var data = { title: document.title, url: location.href };
      if (navigator.share) { navigator.share(data).catch(function () {}); return; }
      var done = function (msg) { if (status) { status.textContent = msg; setTimeout(function () { status.textContent = ''; }, 3000); } };
      if (navigator.clipboard) navigator.clipboard.writeText(location.href).then(function () { done('Link gekopieerd.'); }, function () { done('Kopiëren niet gelukt.'); });
      else done(location.href);
    });
  });

  /* ---------- Client-side filtering (category) ---------- */
  $$('[data-filter]').forEach(function (form) {
    var grid = document.getElementById(form.getAttribute('data-filter'));
    var items = $$('[data-item]', grid);
    var q = $('[name="q"]', form), app = $('[name="toepassing"]', form), uit = $('[name="uitvoering"]', form);
    var status = document.getElementById(form.getAttribute('data-status'));
    var empty = document.getElementById(form.getAttribute('data-empty'));
    var apply = function () {
      var term = (q.value || '').trim().toLowerCase(), a = app.value, u = uit.value, n = 0;
      items.forEach(function (it) {
        var text = it.textContent.toLowerCase();
        var ok = (!term || text.indexOf(term) > -1) &&
          (!a || (' ' + it.dataset.toepassing + ' ').indexOf(' ' + a + ' ') > -1) &&
          (!u || it.dataset.uitvoering === u);
        it.hidden = !ok; if (ok) n++;
      });
      if (empty) empty.hidden = n > 0;
      var countText = n === 1 ? '1 oplossing gevonden' : n + ' oplossingen gevonden';
      if (status && status.textContent !== countText) status.textContent = countText;
    };
    form.addEventListener('input', apply);
    form.addEventListener('change', apply);
    form.addEventListener('submit', function (e) { e.preventDefault(); apply(); });
    var reset = function () { form.reset(); apply(); q.focus(); };
    $$('[data-reset]', form).forEach(function (button) { button.addEventListener('click', reset); });
    if (empty) $$('[data-reset]', empty).forEach(function (button) { button.addEventListener('click', reset); });
    apply();
  });

  /* ---------- Gallery + lightbox ---------- */
  $$('[data-gallery]').forEach(function (root) {
    var main = $('[data-gallery-main]', root);
    var thumbs = $$('[data-thumb]', root);
    var dialog = document.getElementById(root.getAttribute('data-gallery'));
    var stage = dialog && $('[data-lightbox-stage]', dialog);
    var counter = dialog && $('[data-lightbox-count]', dialog);
    var index = 0;
    var tmpl = function (i) { return document.getElementById(thumbs[i].getAttribute('data-thumb')).innerHTML; };
    var show = function (i, focus) {
      index = (i + thumbs.length) % thumbs.length;
      main.innerHTML = tmpl(index);
      var img = $('img', main); if (img) { img.loading = 'eager'; }
      thumbs.forEach(function (t, k) { if (k === index) t.setAttribute('aria-current', 'true'); else t.removeAttribute('aria-current'); });
      if (dialog && dialog.open) renderLightbox();
      if (focus) thumbs[index].focus();
    };
    var renderLightbox = function () {
      stage.innerHTML = tmpl(index);
      var img = $('img', stage); if (img) { img.loading = 'eager'; img.sizes = '94vw'; $$('source', stage).forEach(function (s) { s.sizes = '94vw'; }); }
      counter.textContent = 'Afbeelding ' + (index + 1) + ' van ' + thumbs.length;
    };
    thumbs.forEach(function (t, i) { t.addEventListener('click', function () { show(i); }); });
    if (dialog) {
      $('[data-zoom]', root).addEventListener('click', function () { renderLightbox(); dialog.showModal(); });
      $('[data-lightbox-close]', dialog).addEventListener('click', function () { dialog.close(); });
      $('[data-lightbox-prev]', dialog).addEventListener('click', function () { show(index - 1); });
      $('[data-lightbox-next]', dialog).addEventListener('click', function () { show(index + 1); });
      dialog.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowRight') { e.preventDefault(); show(index + 1); }
        if (e.key === 'ArrowLeft') { e.preventDefault(); show(index - 1); }
      });
      dialog.addEventListener('click', function (e) { if (e.target === dialog) dialog.close(); });
    }
  });

  /* ---------- Component cutaway ---------- */
  $$('[data-component-flow]').forEach(function (flow) {
    $$('button[data-step]', flow).forEach(function (marker) {
      var step = document.getElementById(marker.getAttribute('aria-controls'));
      var summary = $('summary', step);
      var sync = function () {
        marker.setAttribute('aria-expanded', String(step.open));
        marker.classList.toggle('is-current', step.open);
      };
      step.addEventListener('toggle', sync);
      marker.addEventListener('click', function () {
        step.open = true;
        summary.focus();
      });
      sync();
    });
  });

  /* ---------- Contact: page context, validation and submission ---------- */
  var MSG = {
    naam: 'Vul uw naam in.',
    email: 'Vul uw e-mailadres in.',
    emailFormat: 'Vul een geldig e-mailadres in, bijvoorbeeld naam@bedrijf.nl.',
    vraagstuk: 'Schrijf een kort bericht.'
  };
  $$('[data-form]').forEach(function (form) {
    var section = form.closest('#contact');
    var mailLink = section && $('.contact__lines a[href^="mailto:"]', section);
    if (!mailLink) return;

    var topic = $('[data-contact-topic]', form);
    var hint = $('[data-contact-hint]', form);
    var heading = $('#contact-form-title', form);
    var submit = $('button[type="submit"]', form);
    var feedback = $('[data-contact-feedback]', form);
    var legacyTopic = form.elements.product ? 'cycloonafscheider' : 'algemeen';
    var label = $('.btn__label', submit);
    var idleLabel = 'Verstuur uw aanvraag';
    var feedbackMessages = {
      rate_limited: 'Er zijn te veel aanvragen verstuurd. Probeer het over enkele minuten opnieuw.',
      invalid: 'Controleer uw gegevens en probeer het opnieuw.',
      unavailable: 'Versturen lukt op dit moment niet. Probeer het opnieuw of neem rechtstreeks contact met ons op.'
    };
    var fields = $$('[data-validate]', form);

    if (topic) {
      var defaultTopic = topic.value;
      var syncHint = function () {
        hint.textContent = topic.selectedOptions[0].dataset.hint;
      };
      var readTopic = function () {
        var key = new URLSearchParams(location.search).get('aanvraag');
        topic.value = Array.from(topic.options).some(function (option) {
          return option.value === key;
        }) ? key : defaultTopic;
        syncHint();
      };
      readTopic();
      topic.addEventListener('change', syncHint);
      window.addEventListener('popstate', readTopic);
    }
    label.textContent = idleLabel;

    document.addEventListener('click', function (event) {
      var link = event.target.closest('a[href]');
      if (!link || event.defaultPrevented || event.button !== 0 || event.ctrlKey ||
          event.metaKey || event.shiftKey || event.altKey || link.target || link.hasAttribute('download')) return;
      var url = new URL(link.href, location.href);
      if (url.origin !== location.origin || url.pathname !== location.pathname || url.hash !== '#contact') return;

      event.preventDefault();
      var next = new URL(location.href);
      var requestedTopic = url.searchParams.get('aanvraag');
      if (requestedTopic) next.searchParams.set('aanvraag', requestedTopic);
      else next.searchParams.delete('aanvraag');
      next.hash = 'contact';
      if (next.href !== location.href) history.pushState(null, '', next);
      if (topic) readTopic();
      else if (link.dataset.prefill) legacyTopic = 'cycloon-documentatie';
      if (heading) heading.focus({ preventScroll: true });
      (heading || section).scrollIntoView();
    });

    var validate = function (field) {
      var input = $('input, textarea', field);
      var err = $('.field__error', field);
      var value = input.value.trim();
      var msg = '';
      if (input.required && !value) msg = MSG[input.name];
      else if (input.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) msg = MSG.emailFormat;
      field.classList.toggle('has-error', !!msg);
      input.setAttribute('aria-invalid', String(!!msg));
      err.hidden = !msg;
      $('[data-msg]', err).textContent = msg;
      return !msg;
    };

    fields.forEach(function (field) {
      var input = $('input, textarea', field);
      input.addEventListener('blur', function () {
        if (input.value || field.classList.contains('has-error')) validate(field);
      });
      input.addEventListener('input', function () {
        if (field.classList.contains('has-error')) validate(field);
      });
    });

    form.addEventListener('submit', async function (event) {
      event.preventDefault();
      if (submit.disabled) return;
      if (feedback) feedback.textContent = '';
      var invalid = fields.filter(function (field) { return !validate(field); });
      if (invalid.length) { $('input, textarea', invalid[0]).focus(); return; }

      var data = Object.fromEntries(new FormData(form));
      var submitted = JSON.stringify(data);
      data.onderwerp = topic ? topic.value : legacyTopic;
      var endpoint = topic ? form.action : new URL('api/contact', location.href);
      submit.disabled = true;
      form.setAttribute('aria-busy', 'true');
      label.textContent = 'Bezig met versturen…';
      var message;
      try {
        var response = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify(data)
        });
        var result = await response.json();
        if (response.ok && result.ok === true && result.code === 'sent') {
          if (submitted === JSON.stringify(Object.fromEntries(new FormData(form)))) {
            form.reset();
            if (topic) { topic.value = data.onderwerp; syncHint(); }
          }
          message = 'Bedankt. Uw aanvraag is verstuurd.';
        } else {
          message = feedbackMessages[result.code] || feedbackMessages.unavailable;
        }
      } catch (error) {
        message = feedbackMessages.unavailable;
      } finally {
        form.removeAttribute('aria-busy');
        submit.disabled = false;
        label.textContent = idleLabel;
      }
      if (feedback) {
        feedback.textContent = message;
        feedback.focus();
      } else {
        var status = document.createElement('p');
        status.setAttribute('role', 'status');
        status.textContent = message;
        var oldStatus = $('[data-review-status]', form);
        if (oldStatus) oldStatus.replaceWith(status);
        else form.append(status);
        status.setAttribute('data-review-status', '');
      }
    });
    submit.disabled = false;
  });
  /* ---------- Home "Processchema": line from the hero plate into the two disciplines ---------- */
  var proc = $('[data-process]');
  if (proc) {
    // item hover/focus swaps the discipline's plate figure (same behaviour as the header drawers)
    $$('[data-disc]', proc).forEach(function (d) {
      var frame = $('[data-fig-frame]', d), links = $$('[data-fig]', d), cap = $('[data-fig-cap]', frame);
      var show = function (a) {
        var key = a.getAttribute('data-fig');
        links.forEach(function (l) { l.classList.toggle('is-on', l === a); });
        $$('[data-fig-img]', frame).forEach(function (im) {
          var on = im.getAttribute('data-fig-img') === key;
          im.classList.toggle('is-on', on);
          if (on) cap.textContent = im.getAttribute('data-cap');
        });
      };
      links.forEach(function (a) {
        a.addEventListener('pointerenter', function () { show(a); });
        a.addEventListener('focus', function () { show(a); });
      });
      if (links[0]) show(links[0]);
    });

    var pline = $('[data-process-line]', proc);
    var wideProc = window.matchMedia('(min-width: 960px)');
    var pTrack = $('[data-hero-track]');
    var heroPx = function (name, fallback) {
      var v = pTrack && parseFloat(pTrack.style.getPropertyValue(name));
      return isNaN(v) || !v ? fallback : v;
    };
    if (pline) {
      var pFlow = $$('[data-line-flow]', pline), pBase = $$('[data-line-base]', pline), pGran = $$('[data-line-granule]', pline);
      var pNodes = $$('[data-process-node]', proc), pLens = [0, 0], pEnds = [1, 1], pTick = false;
      var layoutLine = function () {
        if (!wideProc.matches) return;
        var sr = proc.getBoundingClientRect(), vw = document.documentElement.clientWidth;
        var x0 = heroPx('--ix', vw * 0.46) - sr.left;           // the hero plate's left edge
        var y0 = 10 - heroPx('--ib', 124);                       // its bottom-left corner sits --ib above this section
        var pts = pNodes.map(function (n) { var r = n.getBoundingClientRect(); return { x: r.left + r.width / 2 - sr.left, y: r.top + r.height / 2 - sr.top, h: r.height / 2 }; });
        var jy = Math.min(pts[0].y, pts[1].y) - 72, R = 18;
        pts.forEach(function (p, i) {
          var dir = p.x < x0 ? -1 : 1;
          var d = 'M' + x0 + ',' + y0 + ' V' + (jy - R) + ' Q' + x0 + ',' + jy + ' ' + (x0 + dir * R) + ',' + jy +
                  ' H' + (p.x - dir * R) + ' Q' + p.x + ',' + jy + ' ' + p.x + ',' + (jy + R) + ' V' + (p.y - p.h - 2);
          pBase[i].setAttribute('d', d); pFlow[i].setAttribute('d', d);
          pLens[i] = pFlow[i].getTotalLength(); pEnds[i] = p.y - p.h;
          pFlow[i].style.strokeDasharray = pLens[i] + ' ' + pLens[i];
        });
        drawLine();
      };
      var drawLine = function () {
        pTick = false;
        if (!wideProc.matches) return;
        var tip = window.innerHeight * 0.62 - proc.getBoundingClientRect().top;   // drawn tip at ~62% of the viewport
        pFlow.forEach(function (f, i) {
          var k = reduceMotion.matches ? 1 : clamp01(tip / pEnds[i]);
          var L = pLens[i] * k;
          f.style.strokeDashoffset = String(pLens[i] - L);
          var g = pGran[i], on = !reduceMotion.matches && k > 0.01 && k < 0.999;
          g.classList.toggle('is-on', on);
          if (on) { var pt = f.getPointAtLength(L); g.setAttribute('cx', pt.x); g.setAttribute('cy', pt.y); }
          pNodes[i].classList.toggle('is-on', k >= 0.999);
        });
      };
      layoutLine();
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { requestAnimationFrame(layoutLine); });
      window.addEventListener('load', layoutLine);
      window.addEventListener('resize', layoutLine);
      wideProc.addEventListener('change', layoutLine);
      reduceMotion.addEventListener('change', layoutLine);
      window.addEventListener('scroll', function () { if (!pTick) { pTick = true; requestAnimationFrame(drawLine); } }, { passive: true });
    }
  }

  /* ---------- Home "Catalogusbladen": registration marks open out as each sheet arrives ---------- */
  var catCells = $$('[data-catalog] .catalog__cell');
  var sectionLoader = 'IntersectionObserver' in window && new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      entry.target.querySelector('.sheet__img--sec img').loading = 'eager';
      sectionLoader.unobserve(entry.target);
    });
  }, { rootMargin: '400px' });
  catCells.forEach(function (cell) {
    var image = cell.querySelector('.sheet__img--sec img');
    var toggle = cell.querySelector('.sheet__toggle');
    if (!image || !toggle) return;
    if (sectionLoader) sectionLoader.observe(cell);
    else image.loading = "eager";
    function ready() {
      image.decode().then(function () { cell.classList.add('is-ready'); }).catch(function () {});
    }
    if (image.complete && image.naturalWidth) ready();
    else image.addEventListener('load', ready, { once: true });
    toggle.addEventListener('click', function () {
      toggle.setAttribute('aria-pressed', String(cell.classList.toggle('is-section')));
    });
  });
  if (catCells.length) {
    if (reduceMotion.matches || !('IntersectionObserver' in window)) catCells.forEach(function (c) { c.classList.add('is-in'); });
    else {
      var catIo = new IntersectionObserver(function (en) {
        en.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); catIo.unobserve(e.target); } });
      }, { rootMargin: '0px 0px -15% 0px' });
      catCells.forEach(function (c) { catIo.observe(c); });
    }
  }

})();
