/* Beheer (owner environment): login, first-login welcome, kiosk settings with live preview, start on one or two screens.
   Server side: api/beheer.py (src/beheer_auth.py). Player: assets/js/kiosk.js. Settings stay on this device (localStorage). */
(function () {
  'use strict';
  var uiLang = document.documentElement.lang || 'nl';
  function K(s) { return (window.KI && window.KI[s]) || s; }
  function page(kind, lang) { return kind + (lang === 'nl' ? '' : '-' + lang) + '.html'; }
  var store = { getItem: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } }, setItem: function (k, v) { try { localStorage.setItem(k, v); return true; } catch (e) { return false; } }, removeItem: function (k) { try { localStorage.removeItem(k); } catch (e) {} } };
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var CFG = 'at-kiosk-cfg', WELCOMED = 'at-beheer-welcomed', PASS = 'at-kiosk-pass';
  var views = { login: $('[data-view="login"]'), welcome: $('[data-view="welcome"]'), dash: $('[data-view="dash"]') };
  var kioskDoc = null, sheets = null, screens = null, popup = null, requests = {}, revision = 0, starting = false, previewPaused = false;

  function show(name) {
    Object.keys(views).forEach(function (k) { views[k].hidden = k !== name; });
    $('[data-user]').hidden = name === 'login';
    if (name !== 'dash') { clearTimeout(timer); stopPreview(); }
    if (name === 'dash') { refresh(); $('#bh-main').focus({ preventScroll: true }); }
    if (name === 'login') { stopPreview(); setTimeout(function () { $('#bh-mail').focus(); }, 30); }
  }
  function api(action, extra) {
    var body = Object.assign({ action: action }, extra || {});
    return fetch('api/beheer', { method: 'POST', headers: { 'Content-Type': 'application/json' }, credentials: 'same-origin', body: JSON.stringify(body) })
      .then(function (r) { return r.json().then(function (j) { j.status = r.status; return j; }); });
  }
  function signedIn(mail) {
    $('[data-user-mail]').textContent = mail || '';
    show(store.getItem(WELCOMED) ? 'dash' : 'welcome');
  }

  /* ---------- login ---------- */
  var MESSAGES = {
    wrong: K('E-mailadres of wachtwoord klopt niet.'),
    too_many: K('Te veel pogingen. Probeer het over 15 minuten opnieuw.'),
    not_configured: K('De login is nog niet ingericht. Zet de omgevingsvariabelen voor Beheer in Vercel (zie DEPLOYMENT.md).'),
    invalid: K('Vul uw e-mailadres en wachtwoord in.'),
    network: K('Geen verbinding met de server. Controleer het netwerk en probeer het opnieuw.')
  };
  $('[data-login]').addEventListener('submit', function (e) {
    e.preventDefault();
    var f = e.target, err = $('[data-login-error]'), btn = f.querySelector('button[type="submit"]');
    if (!f.email.validity.valid || !f.email.value.trim() || !f.password.value) { err.textContent = MESSAGES.invalid; err.hidden = false; (f.email.validity.valid && f.email.value ? f.password : f.email).focus(); return; }
    btn.disabled = true; f.setAttribute('aria-busy', 'true'); err.hidden = true;
    api('login', { email: f.email.value, password: f.password.value, remember: f.remember.checked })
      .then(function (j) {
        if (j.ok) { store.setItem(PASS, String(j.expires * 1000)); f.password.value = ''; signedIn(j.email); }
        else { err.textContent = MESSAGES[j.code] || MESSAGES.wrong; err.hidden = false; f.password.select(); }
      })
      .catch(function () { err.textContent = MESSAGES.network; err.hidden = false; })
      .then(function () { btn.disabled = false; f.removeAttribute('aria-busy'); });
  });
  $('[data-logout]').addEventListener('click', function () {
    store.removeItem(PASS);
    api('logout').catch(function () {}).then(function () { show('login'); });
  });

  /* ---------- welcome: the handover moment ---------- */
  $('[data-today]').textContent = new Date().toLocaleDateString(uiLang, { day: 'numeric', month: 'long', year: 'numeric' });
  $('[data-welcome-done]').addEventListener('click', function () {
    var w = views.welcome;
    w.classList.add('is-leaving');
    store.setItem(WELCOMED, '1');
    setTimeout(function () { w.classList.remove('is-leaving'); show('dash'); }, 850);
  });
  $('[data-welcome-replay]').addEventListener('click', function () { show('welcome'); $('[data-welcome-done]').focus(); });

  /* ---------- settings ---------- */
  var form = $('[data-settings]');
  function readForm() {
    var all = $$('input[name="groups"]', form), on = all.filter(function (i) { return i.checked; }).map(function (i) { return i.value; });
    return {
      layout: form.layout.value, groups: on.length === all.length ? null : on, projects: form.projects.checked, steps: form.steps.checked,
      tempo: +form.tempo.value, lang: form.elements.namedItem('lang').value
    };
  }
  function writeForm(c) {
    if (!c || typeof c !== 'object') return;
    $$('input[name="layout"]', form).forEach(function (i) { i.checked = i.value === (c.layout === '1' ? '1' : '2'); });
    $$('input[name="groups"]', form).forEach(function (i) { i.checked = !Array.isArray(c.groups) || c.groups.indexOf(i.value) >= 0; });
    $$('input[name="lang"]', form).forEach(function (i) { i.checked = i.value === (['nl', 'en', 'de'].indexOf(c.lang) >= 0 ? c.lang : uiLang); });
    form.projects.checked = c.projects !== false; form.steps.checked = c.steps !== false;
    $$('input[name="tempo"]', form).forEach(function (i) { i.checked = +i.value === (c.tempo === 1.3 ? 1.3 : 1); });
  }
    // Language is part of the saved presentation configuration.
  function query(c, role, preview) {
    var q = new URLSearchParams({ role: role });
    if (c.groups) q.set('g', c.groups.join(','));
    if (!c.projects) q.set('p', '0');
    if (!c.steps) q.set('w', '0');
    if (c.tempo !== 1) q.set('tempo', c.tempo);
    if (preview) q.set('preview', '1');
    return page('kiosk', c.lang) + '?' + q.toString();
  }
  writeForm({ layout: '2', lang: uiLang });
  try { writeForm(JSON.parse(store.getItem(CFG) || 'null')); } catch (e) { /* first visit */ }
  var timer = null;
  form.addEventListener('change', function () {
    var groups = $$('input[name="groups"]:checked', form);
    if (!groups.length) { $$('input[name="groups"]', form)[0].checked = true; $('[data-save-status]').textContent = K('Eén component blijft geselecteerd.'); }   // never an empty presentation
    var saved = store.setItem(CFG, JSON.stringify(readForm()));
    $('[data-save-status]').textContent = K(saved ? 'Instellingen bewaard op dit apparaat.' : 'Opslaan lukt niet. De instellingen gelden alleen zolang deze pagina open is.');
    clearTimeout(timer); timer = setTimeout(refresh, 250);
  });

  /* ---------- live preview ---------- */
  function loadKiosk(lang) {
    if (requests[lang]) return requests[lang];
    requests[lang] = fetch(page('kiosk', lang), { credentials: 'same-origin', signal: AbortSignal.timeout(15000) }).then(function (r) {
      if (!r.ok) throw new Error('kiosk ' + r.status);
      return r.text();
    }).then(function (html) {
      var doc = new DOMParser().parseFromString(html, 'text/html');
      if (!doc.querySelector('.ks-sheets') || !doc.querySelector('[data-kiosk-root]')) throw new Error('Invalid kiosk document');
      return { doc: doc, sheets: document.importNode(doc.querySelector('.ks-sheets'), true) };
    }).catch(function (e) { delete requests[lang]; throw e; });
    return requests[lang];
  }
  var ro = new ResizeObserver(function (entries) {
    entries.forEach(function (e) { e.target.style.setProperty('--s', (e.contentRect.width / 1920).toFixed(4)); });
  });
  function stopPreview() { revision++; ro.disconnect(); $('[data-preview]').innerHTML = ''; }
  function refresh() {
    if (views.dash.hidden || !$('[data-host]').hidden) return;
    var c = readForm(), box = $('[data-preview]'), roles = c.layout === '2' ? ['a', 'b'] : ['s'];
    stopPreview();
    var current = revision;
    $('[data-preview-error]').hidden = true;
    $('[data-loop-meta]').textContent = K('Voorbeeld laden…');
    roles.forEach(function (r) {
      var s = document.createElement('div'); s.className = 'bh-screen';
      var f = document.createElement('iframe'); f.src = query(c, r, true); f.title = K('Voorbeeld scherm ') + r.toUpperCase(); f.tabIndex = -1; f.loading = 'eager'; f.setAttribute('aria-hidden', 'true');
      f.addEventListener('load', function () { if (previewPaused) f.contentWindow.postMessage({ type: 'at-preview-pause', paused: true }, location.origin); });
      var tag = document.createElement('span'); tag.className = 'bh-screen__tag'; tag.textContent = r === 's' ? K('ÉÉN SCHERM') : K('SCHERM ') + r.toUpperCase();
      s.appendChild(f); s.appendChild(tag); box.appendChild(s); ro.observe(s);
    });
    $('[data-screens-set]').hidden = c.layout !== '2';
    $('[data-b-link]').value = new URL(query(c, 'b'), location.href).href;
    loadKiosk(c.lang).then(function (data) {
      if (current !== revision) return;
      var p = AtKiosk.plan(data.sheets, c), seconds = Math.round(p.length), m = Math.floor(seconds / 60), s = seconds % 60;
      $('[data-loop-meta]').textContent = p.count + K(' bladen · één ronde ') + m + ':' + (s < 10 ? '0' : '') + s;
    }).catch(function () { if (current !== revision) return; $('[data-loop-meta]').textContent = ''; var err = $('[data-preview-error]'); err.hidden = false; err.textContent = K('De presentatie kon niet worden geladen. Controleer de verbinding en probeer opnieuw.'); });
  }
  $('[data-b-copy]').addEventListener('click', function () {
    var i = $('[data-b-link]'); i.select();
    (navigator.clipboard ? navigator.clipboard.writeText(i.value) : Promise.reject()).then(function () {
      $('[data-b-copy]').textContent = K('Gekopieerd');
      setTimeout(function () { $('[data-b-copy]').textContent = K('Kopieer'); }, 1600);
    }).catch(function () { document.execCommand('copy'); });
  });

  $('[data-preview-pause]').addEventListener('click', function () {
    previewPaused = !previewPaused; this.textContent = K(previewPaused ? 'Voorbeeld hervatten' : 'Voorbeeld pauzeren'); this.setAttribute('aria-pressed', String(previewPaused));
    $$('[data-preview] iframe').forEach(function (f) { f.contentWindow.postMessage({ type: 'at-preview-pause', paused: previewPaused }, location.origin); });
  });

  /* ---------- screens (Window Management API, Chrome/Edge) ---------- */
  var text = $('[data-screens-text]'), list = $('[data-screens]');
  function screenName(s, i) { return (s.label || K('Scherm ') + (i + 1)) + ' · ' + s.width + ' × ' + s.height + (s.isPrimary ? K(' · hoofdscherm') : ''); }
  function renderScreens() {
    list.innerHTML = '';
    screens.screens.forEach(function (s, i) {
      var li = document.createElement('li'), role = s === screens.a ? 'A' : s === screens.b ? 'B' : '–';
      li.className = role === 'B' ? 'is-b' : '';
      li.innerHTML = '<b>' + role + '</b><span></span><select aria-label="' + K('Rol van dit scherm') + '"><option value="">' + K('Niet gebruiken') + '</option><option value="a">' + K('Scherm A (links)') + '</option><option value="b">' + K('Scherm B (rechts)') + '</option></select>';
      li.querySelector('span').textContent = screenName(s, i);
      var sel = li.querySelector('select'); sel.value = role === '–' ? '' : role.toLowerCase();
      sel.addEventListener('change', function () {
        if (sel.value === 'a') { if (screens.b === s) screens.b = screens.a; screens.a = s; }
        else if (sel.value === 'b') { if (screens.a === s) screens.a = screens.b; screens.b = s; }
        else { if (screens.a === s) screens.a = null; if (screens.b === s) screens.b = null; }
        renderScreens();
      });
      list.appendChild(li);
    });
    list.hidden = false;
  }
  $('[data-screens-find]').addEventListener('click', function () {
    if (!('getScreenDetails' in window)) {
      text.textContent = K('Deze browser kan schermen niet automatisch plaatsen. Gebruik Chrome of Edge, of sleep scherm B na de start zelf naar het tweede scherm.');
      return;
    }
    window.getScreenDetails().then(function (d) {
      var others = d.screens.filter(function (s) { return s !== d.currentScreen; });
      screens = { screens: d.screens, a: d.currentScreen, b: others[0] || null };
      text.textContent = others.length ? K('Gevonden. Controleer welk scherm links (A) en rechts (B) staat.') : K('Er is maar één scherm gevonden. Sluit het tweede scherm aan (uitbreiden, niet dupliceren) en zoek opnieuw.');
      renderScreens();
    }).catch(function () {
      text.textContent = K('Geen toestemming om schermen te zoeken. Sta "Vensterbeheer" toe via het slotje in de adresbalk en probeer het opnieuw.');
    });
  });

  /* ---------- start ---------- */
  var host = $('[data-host]'), hint = $('[data-start-hint]'), HINT = hint.textContent;
  function fullscreen(el, screen) {
    if (!el.requestFullscreen) return Promise.resolve();
    return el.requestFullscreen(screen ? { screen: screen } : undefined).catch(function () { return el.requestFullscreen().catch(function () {}); });
  }
  $('[data-start]').addEventListener('click', function () {
    if (starting) return;
    starting = true;
    var btn = $('[data-start]'), original = btn.textContent; btn.disabled = true; btn.textContent = K('Kiosk voorbereiden…');
    var c = readForm(), two = c.layout === '2', role = two ? 'a' : 's';
    host.hidden = false; host.textContent = K('Kiosk voorbereiden…');
    // fullscreen first: with window-management permission Chrome then allows the companion popup on the other screen
    var fs = fullscreen(host, two && screens && screens.a);
    if (two) {
      var b = screens && screens.b, feat = b
        ? 'popup,left=' + b.availLeft + ',top=' + b.availTop + ',width=' + b.availWidth + ',height=' + b.availHeight
        : 'popup,width=1280,height=720';
      popup = window.open(query(c, 'b'), 'at-kiosk-b', feat);
      hint.textContent = popup ? (b ? K('Scherm B staat open op het tweede scherm: klik daar één keer om het volledig te vullen.') : K('Sleep het venster van scherm B naar het tweede scherm en klik erop om het volledig te vullen.'))
        : K('De browser blokkeerde scherm B. Sta pop-ups toe voor deze site en start opnieuw.');
    }
    stopPreview();
    Promise.all([loadKiosk(c.lang), fs]).then(function (results) {
      kioskDoc = results[0].doc; sheets = results[0].sheets;
      host.innerHTML = '';
      var root = document.importNode(kioskDoc.querySelector('[data-kiosk-root]'), true);
      root.lang = c.lang; host.appendChild(root);
      AtKiosk.mount(root, sheets, { role: role, t0: 0, groups: c.groups, projects: c.projects, steps: c.steps, tempo: c.tempo, lang: c.lang }, function () {
        host.hidden = true; host.innerHTML = '';
        if (document.fullscreenElement) document.exitFullscreen().catch(function () {});
        if (popup && !popup.closed) popup.close();
        setTimeout(function () { hint.textContent = HINT; }, 8000);
        refresh(); $('#bh-main').focus({ preventScroll: true });
      });
    }).catch(function () {
      host.hidden = true; host.innerHTML = '';
      if (popup && !popup.closed) popup.close();
      if (document.fullscreenElement) document.exitFullscreen().catch(function () {});
      var err = $('[data-preview-error]'); err.hidden = false; err.textContent = K('De presentatie kon niet worden geladen. Controleer de verbinding en probeer opnieuw.');
      refresh(); err.hidden = false;
    }).finally(function () { starting = false; btn.disabled = false; btn.textContent = original; });
  });

  $$('.bh-languages a').forEach(function (a) { if (a.lang === uiLang) a.setAttribute('aria-current', 'page'); });

  /* ---------- boot ---------- */
  api('status').then(function (j) {
    if (j.ok) { store.setItem(PASS, String(j.expires * 1000)); signedIn(j.email); }
    else {
      show('login');
      if (j.code === 'not_configured') { var err = $('[data-login-error]'); err.textContent = MESSAGES.not_configured; err.hidden = false; }
    }
  }).catch(function () {
    if (+store.getItem(PASS) > Date.now()) signedIn('');          // offline at the fair, recent login on this device
    else { show('login'); var err = $('[data-login-error]'); err.textContent = MESSAGES.network; err.hidden = false; }
  });
  var offline = $('[data-offline-status]');
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('kiosk-sw.js').then(function (registration) {
      var pending = registration.installing || registration.waiting;
      if (!pending || pending.state === 'activated') return navigator.serviceWorker.ready;
      return new Promise(function (resolve, reject) {
        function changed() {
          if (pending.state === 'activated') { pending.removeEventListener('statechange', changed); resolve(navigator.serviceWorker.ready); }
          else if (pending.state === 'redundant') { pending.removeEventListener('statechange', changed); reject(new Error('Offline installation failed')); }
        }
        pending.addEventListener('statechange', changed); changed();
      });
    }).then(function (registration) {
      var channel = new MessageChannel();
      channel.port1.onmessage = function (e) { offline.textContent = K(e.data.ready ? 'Gereed voor offline gebruik.' : 'Offline nog niet gereed. Houd verbinding en vernieuw deze pagina.'); channel.port1.close(); };
      registration.active.postMessage({ type: 'kiosk-cache-status' }, [channel.port2]);
    }).catch(function () { offline.textContent = K('Offline gebruik is niet beschikbaar in deze browser.'); });
  } else offline.textContent = K('Offline gebruik is niet beschikbaar in deze browser.');
})();
