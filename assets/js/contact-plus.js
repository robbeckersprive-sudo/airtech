/* Airtechnic "Flow" — contact block extras (components.contact, styles in top.css "CONTACT").
   site.js keeps the form logic (validation, submit, feedback); this file adds:
   - topic chips (ARIA radiogroup) that drive the existing <select data-contact-topic> and fire its change event;
   - "Liever teruggebeld" brings the phone field forward;
   - message helpers ("+ Product", ...) that start a line in the message for the visitor to complete;
   - the progress line over the card (Vraag, Naam, E-mail);
   - the way there: any link to #contact (header CTA, hero, "Vraag technisch advies", ?aanvraag=topic#contact) no longer
     races the whole page past. A steel sheet slides up, the page jumps behind it, the sheet lifts off the form and
     focus lands in it. Close by: a short smooth scroll. Reduced motion: an instant jump. */
(function () {
  'use strict';
  var L = function (k, nl, v) { var s = (window.ATI18N || {})[k] || nl; return v ? s.replace(/\{(\w+)\}/g, function (_, n) { return v[n]; }) : s; };
  var section = document.getElementById('contact');
  if (!section) return;
  var form = section.querySelector('[data-form]'), select = section.querySelector('[data-contact-topic]');
  var group = section.querySelector('[data-ct-chips]');
  var chips = group ? Array.prototype.slice.call(group.querySelectorAll('[data-ct-topic]')) : [];
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');

  /* ---------- topic chips ---------- */
  var telLabel = section.querySelector('label[for="f-telefoon"]'), telText = telLabel ? telLabel.textContent : '';
  function mode() {
    var cb = !!select && select.value === 'terugbellen';
    section.classList.toggle('is-callback', cb);
    if (telLabel) telLabel.textContent = cb ? L('callback', 'Telefoon, wij bellen u') : telText;
  }
  function syncChips() {
    chips.forEach(function (c) {
      var on = c.getAttribute('data-ct-topic') === select.value;
      c.setAttribute('aria-checked', String(on)); c.tabIndex = on ? 0 : -1;
    });
    mode();
  }
  function setTopic(key) {
    if (!select || !Array.prototype.some.call(select.options, function (o) { return o.value === key; })) return;
    select.value = key;
    select.dispatchEvent(new Event('change', { bubbles: true }));
    syncChips();
  }
  if (select && chips.length > 1) {
    group.hidden = false;
    select.classList.add('ct-select--chips');
    select.setAttribute('aria-hidden', 'true'); select.tabIndex = -1;
    syncChips();
    chips.forEach(function (c, i) {
      c.addEventListener('click', function () { setTopic(c.getAttribute('data-ct-topic')); });
      c.addEventListener('keydown', function (e) {
        var d = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? 1 : e.key === 'ArrowLeft' || e.key === 'ArrowUp' ? -1 : 0;
        if (!d) return;
        e.preventDefault(); var n = chips[(i + d + chips.length) % chips.length]; setTopic(n.getAttribute('data-ct-topic')); n.focus();
      });
    });
    select.addEventListener('change', syncChips);
    if (form) form.addEventListener('reset', function () { setTimeout(syncChips, 0); });
  }

  /* ---------- message helpers ---------- */
  var helpers = section.querySelector('[data-ct-helpers]'), msg = form && form.elements.vraagstuk;
  if (helpers && msg) {
    helpers.hidden = false;
    helpers.addEventListener('click', function (e) {
      var b = e.target.closest('[data-ct-add]'); if (!b) return;
      var add = b.getAttribute('data-ct-add'), v = msg.value.replace(/\s+$/, '');
      if (v.indexOf(add.trim()) > -1) { msg.focus(); return; }
      msg.value = (v ? v + '\n' : '') + add;
      msg.focus(); msg.setSelectionRange(msg.value.length, msg.value.length);
      msg.dispatchEvent(new Event('input', { bubbles: true }));
      b.classList.add('is-used');
    });
  }

  /* ---------- progress line ---------- */
  var steps = Array.prototype.slice.call(section.querySelectorAll('[data-ct-step]')), fill = section.querySelector('[data-ct-fill]');
  function progress() {
    var done = 0;
    steps.forEach(function (li) {
      var f = form && form.elements[li.getAttribute('data-ct-step')];
      var ok = !!(f && f.value.trim() && (f.type !== 'email' || f.checkValidity()));
      li.classList.toggle('is-done', ok); if (ok) done++;
    });
    if (fill) fill.style.width = (done / Math.max(1, steps.length) * 100) + '%';
    section.classList.toggle('is-ready', done === steps.length);
  }
  if (form) { form.addEventListener('input', progress); form.addEventListener('reset', function () { setTimeout(progress, 0); }); }
  progress();

  /* ---------- the way there ---------- */
  var veil = null, busy = false;
  function sheet() {
    if (veil) return veil;
    veil = document.createElement('div');
    veil.className = 'ct-veil'; veil.setAttribute('aria-hidden', 'true');
    veil.innerHTML = '<span class="ct-veil__label"><i></i>' + L('toForm', 'Naar het contactformulier') + '</span>';
    document.body.appendChild(veil);
    return veil;
  }
  function land() {
    var target = section.querySelector('.ct-card') || section;
    var head = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--header-h')) || 72;
    var y = target.getBoundingClientRect().top + window.scrollY - head - 24;
    window.scrollTo({ top: Math.max(0, y), behavior: 'instant' });
  }
  function focusForm() {
    var first = group && !group.hidden ? group.querySelector('[aria-checked="true"]') : msg;
    if (first) first.focus({ preventScroll: true });
  }
  function go(topic) {
    if (topic) setTopic(topic);
    if (history.replaceState) history.replaceState(null, '', location.pathname + location.search.replace(/[?&]aanvraag=[^&]*/, '').replace(/^&/, '?') + '#contact');
    var dist = Math.abs(section.getBoundingClientRect().top);
    if (reduce.matches) { land(); focusForm(); return; }
    if (dist < window.innerHeight * 1.2) {                   // close by: a short glide is calmer than a curtain
      var head = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--header-h')) || 72;
      window.scrollTo({ top: (section.querySelector('.ct-card') || section).getBoundingClientRect().top + window.scrollY - head - 24, behavior: 'smooth' });
      setTimeout(focusForm, 700); return;
    }
    if (busy) return; busy = true;
    var v = sheet();
    v.classList.remove('is-out'); void v.offsetWidth; v.classList.add('is-in');
    setTimeout(function () {
      land();
      section.classList.add('is-arrived');
      v.classList.add('is-out');
      setTimeout(function () { v.classList.remove('is-in', 'is-out'); busy = false; focusForm(); }, 620);
      setTimeout(function () { section.classList.remove('is-arrived'); }, 1600);
    }, 460);
  }
  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest('a[href*="#contact"]'); if (!a || a.target === '_blank' || section.contains(a)) return;
    var url = new URL(a.getAttribute('href'), location.href);
    if (url.hash !== '#contact' || url.origin !== location.origin) return;
    // every page with its own contact block keeps the visitor there (header CTA used to jump to the home page)
    e.preventDefault(); e.stopImmediatePropagation();   // runs in the capture phase, before site.js' smooth scroll
    var topic = url.searchParams.get('aanvraag');
    // from the open mobile menu: close it first (it locks the page scroll), then go
    var burger = document.querySelector('[data-hx-burger][aria-expanded="true"]');
    if (burger) { burger.click(); setTimeout(function () { go(topic); }, 80); } else go(topic);
  }, true);
  // arriving with ?aanvraag=...#contact from another page: pick the topic
  var q = new URLSearchParams(location.search).get('aanvraag');
  if (q) setTopic(q);
})();
