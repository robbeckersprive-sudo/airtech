/* Airtechnic Solutions — page transitions "Nieuw blad" (Nov 20).
   Cross-document View Transitions, so a plain multi-page site moves like one piece of paper being laid over another:
   - forward: the next page slides up over the current one like a fresh drawing sheet (red top edge, the old sheet
     sinks back and darkens); back: the current sheet slides away and reveals the previous one;
   - the picture of a tapped card (catalog sheet, product tile, menu tile, card) flies into the hero plate of the
     page it opens (shared element "vt-media");
   - from the full-screen menu: the menu lifts away as its own layer and uncovers the new page.
   The animation itself is CSS (mobile.css, "PAGE TRANSITIONS"). This file only names the layers and the direction.
   Loaded without defer in <head>, because pagereveal fires at the first render. No-op where unsupported or under
   prefers-reduced-motion (the CSS opt-in sits in a no-preference media query). */
(function () {
  'use strict';
  if (!('onpagereveal' in window)) return;
  var KEY = 'at-vt-media';
  var HERO_MEDIA = '.category-plate__photo, .detail-plate__image, .knowledge-plate__media, .about-hero__figure > picture, .project-hero__media, [data-vt-hero]';
  var lastLink = null;

  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    lastLink = a;
  }, true);

  var isBack = function (act) {
    return !!(act && act.navigationType === 'traverse' && act.from && act.entry && act.entry.index < act.from.index);
  };
  var inView = function (el) {
    var r = el.getBoundingClientRect();
    return r.width > 0 && r.bottom > 0 && r.top < window.innerHeight;
  };

  // old page: name what should travel
  window.addEventListener('pageswap', function (e) {
    var vt = e.viewTransition;
    if (!vt) return;
    var act = e.activation, dest = act && act.entry ? act.entry.url : '';
    var back = isBack(act);
    vt.types.add(back ? 'back' : 'forward');
    var menu = document.querySelector('.mnav.is-open');
    try {
      sessionStorage.removeItem(KEY);
      // the animation runs in the NEW document, so it learns about the open menu from here
      if (menu) { menu.style.viewTransitionName = 'mnav'; sessionStorage.setItem(KEY + '-menu', '1'); }
      else sessionStorage.removeItem(KEY + '-menu');
    } catch (err) { /* storage blocked */ }
    if (!back && lastLink && dest && lastLink.href === dest) {
      // the picture inside the link, or the one on the card the link belongs to
      var card = lastLink.closest('article, .card, .category-option, .project-card');
      var media = lastLink.querySelector('picture') || (card && card.querySelector('picture'));
      if (media && inView(media)) {
        media.style.viewTransitionName = 'vt-media';
        try { sessionStorage.setItem(KEY, dest.split('#')[0]); } catch (err) { /* no morph then */ }
      }
    }
  });

  // back/forward cache: an old page can come back with its names (or the open menu) still set
  window.addEventListener('pageshow', function (e) {
    if (!e.persisted) return;
    Array.prototype.forEach.call(document.querySelectorAll('[style*="view-transition-name"]'), function (el) { el.style.viewTransitionName = ''; });
  });

  // new page: direction + the hero plate that receives the card's picture
  window.addEventListener('pagereveal', function (e) {
    var vt = e.viewTransition;
    if (!vt) return;
    var act = window.navigation && window.navigation.activation;
    var back = isBack(act);
    vt.types.add(back ? 'back' : 'forward');
    var want = null;
    try {
      want = sessionStorage.getItem(KEY); sessionStorage.removeItem(KEY);
      if (sessionStorage.getItem(KEY + '-menu')) { vt.types.add('from-menu'); sessionStorage.removeItem(KEY + '-menu'); }
    } catch (err) { /* storage blocked */ }
    if (!back && want && want === location.href.split('#')[0]) {
      var hero = document.querySelector(HERO_MEDIA);
      if (hero && inView(hero)) {
        hero.style.viewTransitionName = 'vt-media';
        vt.types.add('morph');
        document.documentElement.classList.add('vt-morphed');
        vt.finished.finally(function () { hero.style.viewTransitionName = ''; });
      }
    }
  });
})();
