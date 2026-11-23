/* Airtechnic Solutions — UX polish pass (Nov 23). Styles in polish.css.
   1. Werkwijze on phones: numbered tabs, one step at a time, details folded, swipe between steps
   2. Knowledge list on phones: three questions, then "show all" */
(function () {
  'use strict';
  var lang = (document.documentElement.lang || 'nl').slice(0, 2);
  var T = {
    nl: { next: 'Volgende', all: 'Toon alle {n} vragen', steps: 'Stappen' },
    en: { next: 'Next', all: 'Show all {n} questions', steps: 'Steps' },
    de: { next: 'Weiter', all: 'Alle {n} Fragen zeigen', steps: 'Schritte' }
  }[lang] || null;
  if (!T) T = { next: 'Volgende', all: 'Toon alle {n} vragen', steps: 'Stappen' };
  var phone = window.matchMedia('(max-width: 899px)');
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---------- 1. Werkwijze stepper ---------- */
  var wk = document.querySelector('[data-wk]');
  if (wk) {
    var steps = $$('[data-wk-step]', wk), list = wk.querySelector('[data-wk-steps]');
    var tabs = document.createElement('div'), current = 0;
    tabs.className = 'wk-tabs';
    tabs.setAttribute('role', 'tablist');
    tabs.setAttribute('aria-label', T.steps);
    tabs.style.setProperty('--n', steps.length);
    steps.forEach(function (s, i) {
      var id = 'wk-step-' + i, name = (s.querySelector('.wk-name') || {}).textContent || '';
      s.id = s.id || id;
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'wk-tab'; b.id = 'wk-tab-' + i;
      b.setAttribute('role', 'tab'); b.setAttribute('aria-controls', s.id);
      b.innerHTML = (i < 9 ? '0' : '') + (i + 1) + '<small>' + name.charAt(0) + name.slice(1).toLowerCase() + '</small>';
      b.addEventListener('click', function () { show(i, true); });
      tabs.appendChild(b);
      // fold "Wat u krijgt / In deze fase" behind one control
      var cols = s.querySelector('.wk-cols');
      if (cols) {
        cols.id = cols.id || 'wk-cols-' + i;
        var more = document.createElement('button');
        more.type = 'button'; more.className = 'wk-more'; more.setAttribute('aria-controls', cols.id);
        more.textContent = $$('.wk-h4', cols).map(function (h) { return h.textContent; }).join(' · ');
        more.addEventListener('click', function () {
          var open = more.getAttribute('aria-expanded') === 'true';
          more.setAttribute('aria-expanded', String(!open)); cols.hidden = open;
        });
        cols.parentNode.insertBefore(more, cols);
      }
      if (i < steps.length - 1) {
        var nx = document.createElement('div'), nextName = (steps[i + 1].querySelector('.wk-name') || {}).textContent || '';
        nx.className = 'wk-next';
        nx.innerHTML = '<button type="button" class="link">' + T.next + ': ' + nextName.charAt(0) + nextName.slice(1).toLowerCase() + ' →</button>';
        nx.firstChild.style.cssText = 'border:0;cursor:pointer;font:inherit;font-weight:640';
        nx.firstChild.addEventListener('click', function () { show(i + 1, true, true); });
        s.appendChild(nx);
      }
    });
    list.parentNode.insertBefore(tabs, list);

    var show = function (i, user, scroll) {
      current = Math.max(0, Math.min(steps.length - 1, i));
      steps.forEach(function (s, k) {
        s.classList.toggle('is-tab', k === current);
        s.setAttribute('role', 'tabpanel'); s.setAttribute('aria-labelledby', 'wk-tab-' + k);
      });
      $$('.wk-tab', tabs).forEach(function (b, k) {
        b.setAttribute('aria-selected', String(k === current)); b.tabIndex = k === current ? 0 : -1;
        if (k === current && user) b.focus({ preventScroll: true });
      });
      if (scroll) tabs.scrollIntoView({ block: 'start', behavior: 'smooth' });
      window.dispatchEvent(new Event('scroll'));   // home-practice.js replots the sheet
    };
    tabs.addEventListener('keydown', function (e) {
      var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if (d) { e.preventDefault(); show(current + d, true); }
    });
    // horizontal swipe on the step switches tabs
    var sx = 0, sy = 0;
    list.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; sy = e.touches[0].clientY; }, { passive: true });
    list.addEventListener('touchend', function (e) {
      if (!wk.classList.contains('is-tabbed')) return;
      var dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy;
      if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.5) show(current + (dx < 0 ? 1 : -1));
    }, { passive: true });

    var mode = function () {
      var on = phone.matches;
      wk.classList.toggle('is-tabbed', on);
      $$('.wk-cols', wk).forEach(function (c) { c.hidden = on; });
      $$('.wk-more', wk).forEach(function (m) { m.hidden = !on; m.setAttribute('aria-expanded', 'false'); });
      $$('.wk-next', wk).forEach(function (m) { m.hidden = !on; });
      tabs.hidden = !on;
      if (on) show(current); else steps.forEach(function (s) { s.removeAttribute('role'); s.removeAttribute('aria-labelledby'); });
    };
    phone.addEventListener('change', mode);
    mode();
  }

  /* ---------- 2. Knowledge list: three, then "show all" ---------- */
  var kq = document.querySelector('[data-kq-root]');
  if (kq) {
    var small = window.matchMedia('(max-width: 759px)');
    var rows = $$('.kq-row', kq), listK = kq.querySelector('[data-kq-list]'), expanded = false;
    var btn = document.createElement('button');
    btn.type = 'button'; btn.className = 'kq-more';
    listK.parentNode.insertBefore(btn, listK.nextSibling);
    var clip = function () {
      var live = rows.filter(function (r) { return !r.classList.contains('is-out'); });
      var cut = small.matches && !expanded && live.length > 4;
      rows.forEach(function (r) { r.classList.remove('is-clip'); });
      if (cut) live.slice(3).forEach(function (r) { r.classList.add('is-clip'); });
      btn.classList.toggle('is-needed', cut);
      btn.textContent = T.all.replace('{n}', live.length);
    };
    btn.addEventListener('click', function () {
      expanded = true; clip();
      var first = rows.filter(function (r) { return !r.classList.contains('is-out'); })[3];
      if (first) first.querySelector('a').focus();
    });
    $$('[data-kq-topic]', kq).forEach(function (c) { c.addEventListener('click', function () { setTimeout(clip, 0); }); });
    small.addEventListener('change', clip);
    clip();
  }
})();
