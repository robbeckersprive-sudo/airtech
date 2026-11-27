/* Beurs Kiosk Modus — player (Nov 22). Pages: kiosk.html (standalone screen) and beheer.html (screen A after "Start").

   One clock, no network: every screen derives the current sheet from Date.now() and a shared start time t0, so two
   windows on one PC, or two devices with a synced clock, show the same sheet at the same moment. Roles: a = left
   screen, b = right screen, s = single screen. A sheet change is a red scan line that crosses screen A in the first
   half of the transition and screen B in the second half: one line over both screens.
   Within a sheet, CSS animations are offset by --late (seconds this screen joined after the sheet began), so a
   screen that opens late is still in step. */
(function () {
  'use strict';
  var uiLang = document.documentElement.lang || 'nl';
  function K(s) { return (window.KI && window.KI[s]) || s; }
  function page(kind, lang) { return kind + (lang === 'nl' ? '' : '-' + lang) + '.html'; }
  var store = { getItem: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } }, setItem: function (k, v) { try { localStorage.setItem(k, v); return true; } catch (e) { return false; } }, removeItem: function (k) { try { localStorage.removeItem(k); } catch (e) {} } };
  var T_SWEEP = 1.4;            // seconds for the scan line to cross all screens
  var PREBUILD = 8;             // seconds before a change the next sheet is built (images decode in time)

  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function ease(t) { return 1 - Math.pow(1 - t, 3); }

  /* ---------------------------------------------------------------- schedule */
  function plan(sheetsRoot, cfg) {
    var tpls = Array.prototype.slice.call(sheetsRoot.querySelectorAll('template[data-sheet]'));
    var seq = [], pool = [], tempo = cfg.tempo || 1;
    tpls.forEach(function (t) {
      var g = t.dataset.group;
      if (g && cfg.groups && cfg.groups.indexOf(g) < 0) return;
      if (t.dataset.sector && cfg.sectors && cfg.sectors.indexOf(t.dataset.sector) < 0) return;   // sectors: null = all, [] = none
      if (t.dataset.kind === 'knowledge' && cfg.knowledge === false) return;
      if (t.dataset.kind === 'steps' && cfg.steps === false) return;
      if (t.dataset.pool === 'project') {
        if (cfg.projects === false) return;
        if (!pool.length) seq.push({ slot: 0 }, { slot: 1 });
        pool.push(t);
        return;
      }
      seq.push({ tpl: t });
    });
    var cum = 0;
    seq.forEach(function (s) {
      var t = s.tpl || pool[0];
      s.dur = parseFloat(t.dataset.dur) * tempo;
      s.at = cum; cum += s.dur;
    });
    return { seq: seq, pool: pool, length: cum, count: seq.length };
  }

  function sheetAt(p, t) {               // t: ms since t0
    var L = p.length * 1000, n = Math.floor(t / L), r = t - n * L, k = 0;
    while (k < p.seq.length - 1 && p.seq[k + 1].at * 1000 <= r) k++;
    var s = p.seq[k], tpl = s.tpl || p.pool[(2 * n + s.slot) % p.pool.length];
    return { key: n + ':' + k, tpl: tpl, index: k, start: n * L + s.at * 1000, dur: s.dur, loopPos: r / L };
  }

  /* ---------------------------------------------------------------- granule flow over the panorama */
  // Measured on 01-proceslijn-panorama (7680 × 2160): heap surface (floor) and inner roof of both glass bends.
  var GLASS = [
    { floor: [[770, 1235], [1000, 1235], [1200, 1150], [1400, 1030], [1600, 985], [1650, 985]],
      roof: [[770, 1128], [1000, 1110], [1200, 1040], [1400, 928], [1600, 872], [1650, 872]] },
    { floor: [[6050, 985], [6200, 1000], [6400, 1110], [6600, 1205], [6800, 1240], [6940, 1240]],
      roof: [[6050, 872], [6200, 876], [6400, 950], [6600, 1080], [6800, 1118], [6940, 1118]] }
  ];
  var STEEL = [1650, 6050], PIPE_Y = [866, 964], IMG = [7680, 2160];
  var SPLIT = [.15, .85], PERIOD = 4.2, N = 240;
  function yAt(pts, x) {
    for (var i = 0; i < pts.length - 1; i++) {
      if (x <= pts[i + 1][0]) {
        var f = (x - pts[i][0]) / (pts[i + 1][0] - pts[i][0]);
        return pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f;
      }
    }
    return pts[pts.length - 1][1];
  }
  function rnd(i, k) { var x = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return x - Math.floor(x); }
  var GRAINS = [];
  for (var gi = 0; gi < N; gi++) GRAINS.push({ ph: rnd(gi, 1), v: .12 + rnd(gi, 2) * .78, r: 7 + rnd(gi, 3) * 7, sp: .9 + rnd(gi, 4) * .2, w: rnd(gi, 5) * 6.283 });

  function Flow(canvas, role) {
    this.c = canvas; this.ctx = canvas.getContext('2d'); this.role = role; this.map = null;
  }
  Flow.prototype.resize = function () {
    var r = this.c.getBoundingClientRect(), dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    if (!r.width) return;
    this.c.width = Math.round(r.width * dpr); this.c.height = Math.round(r.height * dpr);
    var W = r.width, H = r.height, s, ox, oy;
    if (this.role === 's') {          // contain, centred
      s = Math.min(W / IMG[0], H / IMG[1]); ox = (W - IMG[0] * s) / 2; oy = (H - IMG[1] * s) / 2;
    } else {                          // cover over a virtual canvas two screens wide
      s = Math.max(2 * W / IMG[0], H / IMG[1]); ox = (2 * W - IMG[0] * s) / 2; oy = (H - IMG[1] * s) / 2;
      if (this.role === 'b') ox -= W;
    }
    this.map = { s: s * dpr, ox: ox * dpr, oy: oy * dpr };
  };
  Flow.prototype.draw = function (now) {
    if (!this.map) this.resize();
    if (!this.map) return;
    var ctx = this.ctx, m = this.map, t = now / 1000;
    ctx.clearRect(0, 0, this.c.width, this.c.height);
    // a soft glint travels along the steel: the stream you cannot see, crossing the gap between the screens
    var gx = STEEL[0] + (STEEL[1] - STEEL[0]) * (((t / PERIOD) % 1 + 1) % 1);
    var X = m.ox + gx * m.s, y0 = m.oy + PIPE_Y[0] * m.s, y1 = m.oy + PIPE_Y[1] * m.s, gw = 900 * m.s;
    var g = ctx.createLinearGradient(X - gw, 0, X + gw * .25, 0);
    g.addColorStop(0, 'rgba(255,255,255,0)'); g.addColorStop(.8, 'rgba(255,255,255,.16)'); g.addColorStop(1, 'rgba(255,255,255,0)');
    ctx.globalCompositeOperation = 'lighter';
    ctx.fillStyle = g; ctx.fillRect(X - gw, y0, gw * 1.25, y1 - y0);
    ctx.globalCompositeOperation = 'source-over';
    for (var i = 0; i < N; i++) {
      var p = GRAINS[i], s = ((t * p.sp / PERIOD + p.ph) % 1 + 1) % 1, gl, u;
      if (s < SPLIT[0]) { gl = GLASS[0]; u = s / SPLIT[0]; }
      else if (s >= SPLIT[1]) { gl = GLASS[1]; u = (s - SPLIT[1]) / (1 - SPLIT[1]); }
      else continue;
      var xa = gl.floor[0][0], xb = gl.floor[gl.floor.length - 1][0], x = xa + (xb - xa) * u;
      var v = clamp(p.v + Math.sin(t * 3 + p.w) * .05, .06, .94);
      var fy = yAt(gl.floor, x), ry = yAt(gl.roof, x), y = fy + (ry - fy) * v;
      var dy = (yAt(gl.floor, x + 20) - fy) / 20, px = m.ox + x * m.s, py = m.oy + y * m.s, r = p.r * m.s;
      var len = 26 * m.s, nx = 1 / Math.sqrt(1 + dy * dy), ny = dy * nx;
      ctx.strokeStyle = 'rgba(217,164,65,.35)'; ctx.lineWidth = r * 1.3; ctx.lineCap = 'round';
      ctx.beginPath(); ctx.moveTo(px - nx * len, py - ny * len); ctx.lineTo(px, py); ctx.stroke();
      ctx.fillStyle = '#E2B04E'; ctx.beginPath(); ctx.arc(px, py, r, 0, 6.283); ctx.fill();
      ctx.fillStyle = 'rgba(255,240,200,.7)'; ctx.beginPath(); ctx.arc(px - r * .3, py - r * .35, r * .35, 0, 6.283); ctx.fill();
    }
  };

  /* ---------------------------------------------------------------- QR codes (Nov 27) */
  // Byte mode, error correction M, versions 1-10 (up to 213 bytes): enough for a site URL. Drawn at run time from
  // location.href, so the code points at the site this kiosk runs on (also offline) and never at a stale domain.
  // Algorithm after ISO/IEC 18004; checked by decoding rendered sheets (tools/check_kiosk_qr.py).
  var QR_ECC = [0, 10, 16, 26, 18, 24, 16, 18, 22, 22, 26], QR_BLOCKS = [0, 1, 1, 1, 2, 2, 4, 4, 4, 5, 5];
  function qrRaw(v) { var r = (16 * v + 128) * v + 64; if (v >= 2) { var n = Math.floor(v / 7) + 2; r -= (25 * n - 10) * n - 55; if (v >= 7) r -= 36; } return r; }
  function qrMul(x, y) { var z = 0; for (var i = 7; i >= 0; i--) { z = (z << 1) ^ ((z >>> 7) * 0x11D); z ^= ((y >>> i) & 1) * x; } return z & 255; }
  function qrMatrix(text) {
    var data = unescape(encodeURIComponent(text)).split('').map(function (c) { return c.charCodeAt(0); });
    var ver = 1, cap, i, j;
    for (;; ver++) {
      if (ver > 10) return null;
      cap = (Math.floor(qrRaw(ver) / 8) - QR_ECC[ver] * QR_BLOCKS[ver]) * 8;
      if (4 + (ver < 10 ? 8 : 16) + data.length * 8 <= cap) break;
    }
    var bits = [];
    function push(val, len) { for (var b = len - 1; b >= 0; b--) bits.push((val >>> b) & 1); }
    push(4, 4); push(data.length, ver < 10 ? 8 : 16); data.forEach(function (b) { push(b, 8); });
    push(0, Math.min(4, cap - bits.length)); push(0, (8 - bits.length % 8) % 8);
    for (var pad = 0xEC; bits.length < cap; pad ^= 0xEC ^ 0x11) push(pad, 8);
    var cw = [];
    for (i = 0; i < bits.length; i += 8) { var byte = 0; for (j = 0; j < 8; j++) byte = (byte << 1) | bits[i + j]; cw.push(byte); }
    // Reed-Solomon per block, then interleave
    var nb = QR_BLOCKS[ver], ecl = QR_ECC[ver], raw = Math.floor(qrRaw(ver) / 8), nshort = nb - raw % nb, shortLen = Math.floor(raw / nb);
    var div = [], root = 1;
    for (i = 0; i < ecl - 1; i++) div.push(0);
    div.push(1);
    for (i = 0; i < ecl; i++) { for (j = 0; j < ecl; j++) { div[j] = qrMul(div[j], root); if (j + 1 < ecl) div[j] ^= div[j + 1]; } root = qrMul(root, 2); }
    var blocks = [], k = 0;
    for (i = 0; i < nb; i++) {
      var dat = cw.slice(k, k + shortLen - ecl + (i < nshort ? 0 : 1)); k += dat.length;
      var rem = div.map(function () { return 0; });
      dat.forEach(function (b) { var f = b ^ rem.shift(); rem.push(0); div.forEach(function (c, x) { rem[x] ^= qrMul(c, f); }); });
      if (i < nshort) dat.push(0);
      blocks.push(dat.concat(rem));
    }
    var out = [];
    for (i = 0; i < blocks[0].length; i++) blocks.forEach(function (b, x) { if (i !== shortLen - ecl || x >= nshort) out.push(b[i]); });
    // function patterns
    var size = ver * 4 + 17, M = [], F = [];
    for (i = 0; i < size; i++) { M.push([]); F.push([]); for (j = 0; j < size; j++) { M[i].push(false); F[i].push(false); } }
    function set(x, y, d) { M[y][x] = d; F[y][x] = true; }
    for (i = 0; i < size; i++) { set(6, i, i % 2 === 0); set(i, 6, i % 2 === 0); }
    [[3, 3], [size - 4, 3], [3, size - 4]].forEach(function (c) {
      for (var dy = -4; dy <= 4; dy++) for (var dx = -4; dx <= 4; dx++) {
        var d = Math.max(Math.abs(dx), Math.abs(dy)), xx = c[0] + dx, yy = c[1] + dy;
        if (xx >= 0 && xx < size && yy >= 0 && yy < size) set(xx, yy, d !== 2 && d !== 4);
      }
    });
    if (ver > 1) {
      var na = Math.floor(ver / 7) + 2, step = Math.ceil((ver * 4 + 4) / (na * 2 - 2)) * 2, pos = [6];
      for (var ap = size - 7; pos.length < na; ap -= step) pos.splice(1, 0, ap);
      pos.forEach(function (ax, a) { pos.forEach(function (ay, b) {
        if ((a === 0 && b === 0) || (a === 0 && b === na - 1) || (a === na - 1 && b === 0)) return;
        for (var dy = -2; dy <= 2; dy++) for (var dx = -2; dx <= 2; dx++) set(ax + dx, ay + dy, Math.max(Math.abs(dx), Math.abs(dy)) !== 1);
      }); });
    }
    function format(mask) {
      var r = mask, b;                                   // error correction level M = 0b00
      for (b = 0; b < 10; b++) r = (r << 1) ^ ((r >>> 9) * 0x537);
      var fb = ((mask << 10) | r) ^ 0x5412;
      function bit(n) { return ((fb >>> n) & 1) !== 0; }
      for (b = 0; b <= 5; b++) set(8, b, bit(b));
      set(8, 7, bit(6)); set(8, 8, bit(7)); set(7, 8, bit(8));
      for (b = 9; b < 15; b++) set(14 - b, 8, bit(b));
      for (b = 0; b < 8; b++) set(size - 1 - b, 8, bit(b));
      for (b = 8; b < 15; b++) set(8, size - 15 + b, bit(b));
      set(8, size - 8, true);
    }
    format(0);
    if (ver >= 7) {
      var vr = ver;
      for (i = 0; i < 12; i++) vr = (vr << 1) ^ ((vr >>> 11) * 0x1F25);
      var vb = (ver << 12) | vr;
      for (i = 0; i < 18; i++) { var on = ((vb >>> i) & 1) !== 0, va = size - 11 + i % 3, vc = Math.floor(i / 3); set(va, vc, on); set(vc, va, on); }
    }
    // data: zigzag from the bottom right
    var n = 0;
    for (var right = size - 1; right >= 1; right -= 2) {
      if (right === 6) right = 5;
      for (var vert = 0; vert < size; vert++) for (j = 0; j < 2; j++) {
        var x = right - j, up = ((right + 1) & 2) === 0, y = up ? size - 1 - vert : vert;
        if (!F[y][x] && n < out.length * 8) { M[y][x] = ((out[n >>> 3] >>> (7 - (n & 7))) & 1) !== 0; n++; }
      }
    }
    // mask: the pattern with the lowest penalty (runs, 2x2 blocks, dark/light balance)
    function masked(mask, x, y) {
      switch (mask) {
        case 0: return (x + y) % 2 === 0; case 1: return y % 2 === 0; case 2: return x % 3 === 0; case 3: return (x + y) % 3 === 0;
        case 4: return (Math.floor(x / 3) + Math.floor(y / 2)) % 2 === 0; case 5: return x * y % 2 + x * y % 3 === 0;
        case 6: return (x * y % 2 + x * y % 3) % 2 === 0; default: return ((x + y) % 2 + x * y % 3) % 2 === 0;
      }
    }
    function apply(mask) { for (var y = 0; y < size; y++) for (var x = 0; x < size; x++) if (!F[y][x] && masked(mask, x, y)) M[y][x] = !M[y][x]; }
    function penalty() {
      var p = 0, dark = 0, x, y, run, col;
      for (y = 0; y < size; y++) {
        for (x = 0, run = 0, col = null; x < size; x++) { if (M[y][x] === col) { run++; if (run === 5) p += 3; else if (run > 5) p++; } else { col = M[y][x]; run = 1; } if (M[y][x]) dark++; }
        for (x = 0, run = 0, col = null; x < size; x++) { if (M[x][y] === col) { run++; if (run === 5) p += 3; else if (run > 5) p++; } else { col = M[x][y]; run = 1; } }
      }
      for (y = 0; y < size - 1; y++) for (x = 0; x < size - 1; x++) { var c = M[y][x]; if (c === M[y][x + 1] && c === M[y + 1][x] && c === M[y + 1][x + 1]) p += 3; }
      return p + Math.floor(Math.abs(dark * 20 - size * size * 10) / (size * size)) * 10;
    }
    var best = 0, bestP = Infinity;
    for (var mk = 0; mk < 8; mk++) { apply(mk); format(mk); var pen = penalty(); if (pen < bestP) { bestP = pen; best = mk; } apply(mk); }
    apply(best); format(best);
    return M;
  }
  function qrSvg(text) {
    var m = qrMatrix(text);
    if (!m) return '';
    var n = m.length, q = 4, d = '';
    for (var y = 0; y < n; y++) for (var x = 0; x < n; x++) if (m[y][x]) d += 'M' + (x + q) + ' ' + (y + q) + 'h1v1h-1z';
    return '<svg viewBox="0 0 ' + (n + 2 * q) + ' ' + (n + 2 * q) + '" shape-rendering="crispEdges" role="img" aria-label="QR"><rect width="100%" height="100%" fill="#fff"/><path d="' + d + '" fill="#08182A"/></svg>';
  }
  function drawQr(scope) {
    Array.prototype.forEach.call(scope.querySelectorAll('[data-qr]'), function (el) {
      var box = el.querySelector('[data-qr-code]'), svg = '';
      try { svg = qrSvg(new URL(el.dataset.qr, location.href).href.replace(/[?&](role|t0|g|p|w|k|sec|stand|tempo|preview)=[^&#]*/g, '')); } catch (e) { svg = ''; }
      if (svg && box) box.innerHTML = svg; else el.hidden = true;          // no code: no plate (never an empty frame)
    });
  }

  /* ---------------------------------------------------------------- player */
  function Player(root, sheetsRoot, cfg) {
    this.root = root; this.cfg = cfg; this.role = cfg.role || 's';
    this.stage = root.querySelector('[data-stage]');
    this.scan = root.querySelector('[data-scan]');
    this.progress = root.querySelector('[data-progress]');
    this.tbTitle = root.querySelector('[data-tb-title]');
    this.tbSheet = root.querySelector('[data-tb-sheet]');
    this.plan = plan(sheetsRoot, cfg);
    this.reduced = matchMedia('(prefers-reduced-motion: reduce)').matches; this.paused = false; this.lastDraw = 0;
    this.cur = null; this.next = null; this.old = null; this.flows = [];
    var role = this.role;
    Array.prototype.forEach.call(root.querySelectorAll('[data-tb]'), function (el) { el.hidden = el.dataset.tb.split(' ').indexOf(role) < 0; });
    // optional stand line from Beheer ("Hal 3 · Stand B12"): takes the place of the scale cell
    var stand = (cfg.stand || '').trim().slice(0, 40), standCell = root.querySelector('[data-tb-stand]'), scaleCell = root.querySelector('[data-tb-scale]');
    if (standCell) { standCell.hidden = !stand; standCell.querySelector('[data-stand]').textContent = stand; if (stand && scaleCell) scaleCell.hidden = true; }
    root.classList.add('is-running');
    var self = this;
    this.onResize = function () { self.width = root.clientWidth; self.flows.forEach(function (f) { f.flow.resize(); }); };
    this.onResize();
    window.addEventListener('resize', this.onResize);
    this.tick = this.tick.bind(this);
    this.raf = requestAnimationFrame(this.tick);
  }
  Player.prototype.build = function (sh) {
    var face = sh.tpl.content.querySelector('[data-face="' + this.role + '"]');
    var layer = document.createElement('section');
    layer.className = 'ks-layer is-next';
    layer.dataset.role = this.role;
    layer.setAttribute('aria-label', sh.tpl.dataset.title);
    layer.style.setProperty('--dur', sh.dur + 's');
    layer.appendChild(face.cloneNode(true));
    this.stage.appendChild(layer);
    drawQr(layer);
    var flows = [], role = this.role;
    Array.prototype.forEach.call(layer.querySelectorAll('[data-flow]'), function (c) { flows.push({ layer: layer, flow: new Flow(c, role) }); });
    this.flows = this.flows.concat(flows);
    var item = { key: sh.key, sh: sh, layer: layer, counts: layer.querySelectorAll('[data-count]'), ready: false };
    Promise.all(Array.prototype.map.call(layer.querySelectorAll('img'), function (img) {
      img.loading = 'eager';
      return img.decode().catch(function () {
        var pic = img.closest('picture'); if (pic) pic.querySelectorAll('source').forEach(function (s) { s.remove(); });
        return img.decode().catch(function () {});
      });
    })).then(function () { item.ready = true; });
    return item;
  };
  Player.prototype.drop = function (item) {
    if (!item) return;
    this.flows = this.flows.filter(function (f) { return f.layer !== item.layer; });
    item.layer.remove();
  };
  Player.prototype.show = function (item, now) {
    var late = (now - (this.cfg.t0 + item.sh.start)) / 1000;
    item.layer.querySelector('.ks-face').style.setProperty('--late', Math.max(0, late).toFixed(3) + 's');
    item.layer.classList.remove('is-next');
    item.layer.classList.add('is-live');
    if (this.old) { this.drop(this.old); this.old = null; }
    if (!this.reduced && late < T_SWEEP && this.cur) { item.layer.classList.add('is-in'); item.layer.style.setProperty('--x', '0px'); this.old = this.cur; }
    else { this.drop(this.cur); }
    this.cur = item;
    this.flows.forEach(function (f) { if (f.layer === item.layer) f.flow.resize(); });
    var idx = item.sh.index + 1, total = this.plan.count;
    if (this.tbTitle) this.tbTitle.textContent = item.sh.tpl.dataset.title;
    if (this.tbSheet) this.tbSheet.textContent = (idx < 10 ? '0' : '') + idx + ' / ' + (total < 10 ? '0' : '') + total;
  };
  Player.prototype.tick = function () {
    this.raf = requestAnimationFrame(this.tick);
    if (this.paused || document.hidden) return;
    var now = Date.now();
    if (now - this.lastDraw < (this.root.classList.contains('is-preview') ? 50 : 15)) return;
    this.lastDraw = now;
    var t = now - this.cfg.t0, sh = sheetAt(this.plan, t);
    if (!this.cur || this.cur.key !== sh.key) {
      var item = this.next && this.next.key === sh.key ? this.next : this.build(sh);
      if (this.next && this.next !== item) this.drop(this.next);
      this.next = item;
      if (!item.ready) return;
      this.next = null;
      this.show(item, now);
    }
    // prebuild the next sheet a few seconds before the change
    var endAt = this.cfg.t0 + sh.start + sh.dur * 1000;
    if (!this.next && endAt - now < PREBUILD * 1000) {
      var nsh = sheetAt(this.plan, endAt - this.cfg.t0 + 5);
      if (nsh.key !== sh.key) this.next = this.build(nsh);
    }
    // the sweep: global progress over all screens; A owns the first half, B the second
    var W = this.width, el = (now - (this.cfg.t0 + sh.start)) / 1000, p = clamp(el / T_SWEEP, 0, 1), lp;
    lp = this.role === 'a' ? clamp(p * 2, 0, 1) : this.role === 'b' ? clamp(p * 2 - 1, 0, 1) : p;
    lp = ease(lp);
    if (this.cur.layer.classList.contains('is-in')) {
      this.cur.layer.style.setProperty('--x', (lp * W).toFixed(1) + 'px');
      if (p >= 1) { this.cur.layer.classList.remove('is-in'); this.drop(this.old); this.old = null; }
    }
    var scanOn = p < 1 && lp > 0 && lp < 1 && this.old !== null;
    this.scan.classList.toggle('is-on', scanOn);
    if (scanOn) this.scan.style.setProperty('--scan-x', (lp * W).toFixed(1) + 'px');
    // loop progress line: also one line over both screens
    var lpos = sh.loopPos, pr = this.role === 'a' ? clamp(lpos * 2, 0, 1) : this.role === 'b' ? clamp(lpos * 2 - 1, 0, 1) : lpos;
    if (this.progress) this.progress.style.setProperty('--p', (pr * 100).toFixed(2) + '%');
    // burn-in care: the whole picture drifts a few pixels over minutes (identical on every screen)
    this.root.style.setProperty('--shift-x', (Math.sin(now / 97000) * 3).toFixed(2) + 'px');
    this.root.style.setProperty('--shift-y', (Math.cos(now / 131000) * 3).toFixed(2) + 'px');
    // count-ups (facts), timed from the sheet start
    var counts = this.cur.counts, inDelay = this.role === 'b' ? .95 : .35;
    for (var i = 0; i < counts.length; i++) {
      var c = counts[i], li = c.closest('li'), d = li ? parseFloat(li.style.getPropertyValue('--d')) || 0 : 0;
      var f = ease(clamp((el - inDelay - d - .2) / 1.6, 0, 1)), dec = +c.dataset.dec;
      var val = (parseFloat(c.dataset.count) * f).toLocaleString(this.cfg.lang || uiLang, { minimumFractionDigits: dec, maximumFractionDigits: dec });
      var txt = c.dataset.pre + val + c.dataset.suf;
      if (c.textContent !== txt) c.textContent = txt;
    }
    if (this.reduced) return;
    for (var k = 0; k < this.flows.length; k++) if (this.flows[k].layer === this.cur.layer || (this.old && this.flows[k].layer === this.old.layer)) this.flows[k].flow.draw(now);
  };
  Player.prototype.stop = function () {
    cancelAnimationFrame(this.raf);
    window.removeEventListener('resize', this.onResize);
    this.stage.innerHTML = '';
    this.root.classList.remove('is-running');
  };

  /* ---------------------------------------------------------------- shell: auth, fullscreen, wake lock, exit */
  var PASS = 'at-kiosk-pass';
  function checkSession() {
    return fetch('api/beheer', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{"action":"status"}', credentials: 'same-origin' })
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok && j.ok, code: j.code, expires: j.expires }; }); })
      .then(function (s) { if (s.ok) store.setItem(PASS, String(s.expires * 1000)); return s; })
      .catch(function () {                       // offline at the fair: a recent login on this device still counts
        return { ok: +store.getItem(PASS) > Date.now(), code: 'offline' };
      });
  }
  var lock = null;
  function wake() {
    if (!('wakeLock' in navigator) || document.visibilityState !== 'visible') return;
    navigator.wakeLock.request('screen').then(function (l) { lock = l; l.addEventListener('release', function () { if (lock === l) lock = null; }); }).catch(function () {});
  }
  function bindExit(root, onStop) {
    var dlg = root.querySelector('[data-exit]'), timer = null, stopped = false, previousFocus = null;
    var hadFullscreen = !!document.fullscreenElement;
    var chan = 'BroadcastChannel' in window ? new BroadcastChannel('at-kiosk') : null;
    function open() {
      if (stopped || !dlg.hidden) return;
      previousFocus = document.activeElement; dlg.hidden = false;
      root.classList.remove('is-running'); dlg.querySelector('[data-exit-no]').focus();
    }
    function close() {
      dlg.hidden = true; root.classList.add('is-running');
      if (previousFocus && previousFocus.isConnected) previousFocus.focus();
    }
    function cleanup() {
      clearTimeout(timer);
      document.removeEventListener('keydown', onKey);
      document.removeEventListener('visibilitychange', onVisibility);
      document.removeEventListener('fullscreenchange', onFullscreen);
      root.removeEventListener('pointerdown', onDown);
      ['pointerup', 'pointercancel', 'pointerleave'].forEach(function (n) { root.removeEventListener(n, cancelHold); });
      if (chan) chan.close();
      if (lock) { lock.release().catch(function () {}); lock = null; }
    }
    function stop(local) {
      if (stopped) return; stopped = true;
      if (chan && !local) chan.postMessage({ type: 'stop' });
      cleanup(); onStop();
    }
    function onKey(e) {
      if (e.key === 'Escape') { e.preventDefault(); if (dlg.hidden) open(); else close(); }
      if (e.key === 'Tab' && !dlg.hidden) {
        var first = dlg.querySelector('[data-exit-no]'), last = dlg.querySelector('[data-exit-yes]');
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    }
    function onDown(e) {
      var r = root.getBoundingClientRect();
      if (e.clientX - r.left > r.width * .12 || e.clientY - r.top > r.height * .12) return;
      cancelHold(); timer = setTimeout(open, 3000);
    }
    function cancelHold() { clearTimeout(timer); }
    function onVisibility() { if (!stopped && document.visibilityState === 'visible' && lock === null) wake(); }
    function onFullscreen() {
      if (document.fullscreenElement) hadFullscreen = true;
      else if (hadFullscreen) { hadFullscreen = false; open(); }
    }
    dlg.querySelector('[data-exit-no]').addEventListener('click', close);
    dlg.querySelector('[data-exit-yes]').addEventListener('click', function () { stop(false); });
    document.addEventListener('keydown', onKey);
    document.addEventListener('visibilitychange', onVisibility);
    document.addEventListener('fullscreenchange', onFullscreen);
    root.addEventListener('pointerdown', onDown);
    ['pointerup', 'pointercancel', 'pointerleave'].forEach(function (n) { root.addEventListener(n, cancelHold); });
    if (chan) chan.onmessage = function (m) { if (m.data && m.data.type === 'stop') stop(true); };
    return cleanup;
  }
  function nightlyReload() {          // a fresh start every night at 04:00 keeps a multi-day fair free of leaks
    var d = new Date(), n = new Date(d); n.setHours(4, 0, 0, 0); if (n <= d) n.setDate(n.getDate() + 1);
    setTimeout(function () { location.reload(); }, n - d);
  }

  function readCfg() {
    var q = new URLSearchParams(location.search);
    return {
      role: ['a', 'b', 's'].indexOf(q.get('role')) >= 0 ? q.get('role') : 's',
      t0: +q.get('t0') || 0,
      groups: q.get('g') ? q.get('g').split(',') : null,
      projects: q.get('p') !== '0', steps: q.get('w') !== '0',
      sectors: q.get('sec') === null ? null : q.get('sec') === '0' ? [] : q.get('sec').split(','),
      knowledge: q.get('k') !== '0', stand: q.get('stand') || '',
      tempo: [1, 1.3].indexOf(+q.get('tempo')) >= 0 ? +q.get('tempo') : 1, lang: uiLang, preview: q.get('preview') === '1'
    };
  }

  function boot() {
    var root = document.querySelector('[data-kiosk-root]'), sheets = document.querySelector('.ks-sheets'), cfg = readCfg();
    var gate = root.querySelector('[data-gate]'), player = null;
    if ('serviceWorker' in navigator && !cfg.preview) navigator.serviceWorker.register('kiosk-sw.js').catch(function () {});
    if (cfg.preview) root.classList.add('is-preview');
    checkSession().then(function (s) {
      if (!s.ok) {
        gate.hidden = false;
        gate.querySelector('[data-gate-title]').textContent = K('Eerst inloggen');
        gate.querySelector('[data-gate-text]').textContent = K('De kiosk start vanuit Beheer. Log in en kies daar "Start kiosk".');
        gate.querySelector('[data-gate-go]').hidden = true;
        gate.querySelector('[data-gate-login]').hidden = false;
        return;
      }
      player = new Player(root, sheets, cfg);
      if (cfg.preview) {
        window.addEventListener('message', function (e) { if (e.origin === location.origin && e.source === parent && e.data && e.data.type === 'at-preview-pause') { player.paused = !!e.data.paused; root.classList.toggle('is-paused', player.paused); } });
        return;
      }
      nightlyReload();
      bindExit(root, function () {
        if (player) player.stop();
        if (document.fullscreenElement) document.exitFullscreen().catch(function () {});
        window.close();                                  // popups (screen B) close; a normal tab goes back to Beheer
        setTimeout(function () { location.href = page('beheer', uiLang); }, 150);
      });
      if (!document.fullscreenElement) {
        gate.hidden = false;
        gate.querySelector('[data-gate-title]').textContent = cfg.role === 'b' ? K('Scherm B') : 'Kiosk';
        gate.querySelector('[data-gate-text]').textContent = K('Klik om dit scherm volledig te vullen. De presentatie loopt al gelijk met de andere schermen.');
        gate.querySelector('[data-gate-go]').addEventListener('click', function () {
          gate.hidden = true;
          (document.documentElement.requestFullscreen ? document.documentElement.requestFullscreen() : Promise.resolve()).catch(function () {});
          wake();
        });
        gate.querySelector('[data-gate-go]').focus();
      } else wake();
    });
  }

  /* inside Beheer: screen A plays in a fullscreen host on the same page */
  function mount(root, sheets, cfg, onStop) {
    var player = new Player(root, sheets, cfg);
    wake();
    bindExit(root, function () { player.stop(); if (onStop) onStop(); });
    return player;
  }

  window.AtKiosk = { boot: boot, mount: mount, plan: plan, checkSession: checkSession, qr: qrMatrix };
})();
