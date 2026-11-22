/* Airtechnic "Flow" — hero granule flow.
   Draws granules flowing through the empty glass tube of the hero photo: a dense bed sliding along the tube floor
   (slow at the bottom, fast on top, with travelling dunes) and loose granules hopping through the air above it.
   Geometry comes from the markup: data-tube = cross-sections [[bottomWall, topWall], ...] and data-box = canvas box,
   both in px of the 1536x1024 photo. The front glass (walls + reflections, data-glass) is drawn over the granules.
   Respects the hero pause button, pauses off-screen, and draws one still frame under prefers-reduced-motion.
   Optional (Doorstroom hero): data-mode="dense|dilute" on the canvas switches the flow regime (eased), and a pointer
   over the tube blows an air pulse into it (bed bulges, granules are kicked up and sped up locally). */
(function () {
  'use strict';
  var cv = document.querySelector('canvas[data-granules]');
  if (!cv || !cv.getContext) return;
  var ctx = cv.getContext('2d');
  var hero = cv.closest('[data-hero]') || document.body;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  var SEC = JSON.parse(cv.getAttribute('data-tube'));
  var BOX = cv.getAttribute('data-box').split(',').map(Number);   // x0, y0, x1, y1
  var BW = BOX[2] - BOX[0], BH = BOX[3] - BOX[1];

  /* ---------- tube geometry: Catmull-Rom walls, re-sampled by arc length ---------- */
  function cr(pts, n) {
    var p = [pts[0]].concat(pts, [pts[pts.length - 1]]), out = [];
    for (var i = 1; i < p.length - 2; i++) {
      for (var k = 0; k < n; k++) {
        var t = k / n, t2 = t * t, t3 = t2 * t, q = [];
        for (var j = 0; j < 2; j++) {
          q[j] = .5 * (2 * p[i][j] + (-p[i - 1][j] + p[i + 1][j]) * t + (2 * p[i - 1][j] - 5 * p[i][j] + 4 * p[i + 1][j] - p[i + 2][j]) * t2 +
                       (-p[i - 1][j] + 3 * p[i][j] - 3 * p[i + 1][j] + p[i + 2][j]) * t3);
        }
        out.push(q);
      }
    }
    out.push(pts[pts.length - 1].slice());
    return out;
  }
  var bot = cr(SEC.map(function (s) { return s[0]; }), 30);
  var top = cr(SEC.map(function (s) { return s[1]; }), 30);
  var cum = [0], i;
  for (i = 1; i < bot.length; i++) {
    var mx = (bot[i][0] + top[i][0] - bot[i - 1][0] - top[i - 1][0]) / 2, my = (bot[i][1] + top[i][1] - bot[i - 1][1] - top[i - 1][1]) / 2;
    cum.push(cum[i - 1] + Math.sqrt(mx * mx + my * my));
  }
  var LEN = cum[cum.length - 1];
  var U = 260, BI = [], TI = [], j = 0;              // inner walls at uniform arc steps
  for (i = 0; i < U; i++) {
    var target = i / (U - 1) * LEN;
    while (j < cum.length - 2 && cum[j + 1] < target) j++;
    var f = (target - cum[j]) / ((cum[j + 1] - cum[j]) || 1);
    var bx = bot[j][0] + (bot[j + 1][0] - bot[j][0]) * f, by = bot[j][1] + (bot[j + 1][1] - bot[j][1]) * f;
    var tx = top[j][0] + (top[j + 1][0] - top[j][0]) * f, ty = top[j][1] + (top[j + 1][1] - top[j][1]) * f;
    var dx = tx - bx, dy = ty - by, dl = Math.sqrt(dx * dx + dy * dy) || 1;
    dx /= dl; dy /= dl;
    BI.push([bx + dx * 9, by + dy * 9]);             // granules rest on the inside of the glass
    TI.push([tx - dx * 7, ty - dy * 7]);
  }
  var CLIP = [];
  for (i = 0; i < U; i += 4) CLIP.push(BI[i]);
  CLIP.push(BI[U - 1]);
  for (i = U - 1; i >= 0; i -= 4) CLIP.push(TI[i]);
  CLIP.push(TI[0]);
  var P = [0, 0], A = [0, 0];
  function pos(u, v) {                                 // u: 0..1 along the tube, v: 0 floor .. 1 roof
    var x = Math.min(Math.max(u, 0), 1) * (U - 1), k = Math.min(x | 0, U - 2), g = x - k;
    var b0 = BI[k], b1 = BI[k + 1], t0 = TI[k], t1 = TI[k + 1];
    var px0 = b0[0] + (b1[0] - b0[0]) * g, py0 = b0[1] + (b1[1] - b0[1]) * g;
    var px1 = t0[0] + (t1[0] - t0[0]) * g, py1 = t0[1] + (t1[1] - t0[1]) * g;
    P[0] = px0 + (px1 - px0) * v; P[1] = py0 + (py1 - py0) * v;
    A[0] = b1[0] - b0[0]; A[1] = b1[1] - b0[1];      // local flow direction
    return P;
  }

  /* ---------- granule sprites (photo-matched shading, light from the top left) ----------
     Bed sprites carry a soft contact shadow below-right of the sphere (ambient occlusion between packed granules);
     airborne sprites are clean spheres. Sprite box 64 px, sphere radius 22 px centred at (28, 28). */
  var SPR = [], SPA = [], TINTS = [.7, .8, .9, 1, 1.08, 1.15], SC = 28, SR = 22, SS = 64;
  var STOPS = [[0, 255, 250, 226, 1], [.26, 250, 222, 130, 1], [.6, 232, 180, 64, 1], [.87, 204, 146, 38, 1], [1, 176, 122, 28, .5]];
  function makeSprite(k, ao) {
    var c = document.createElement('canvas'); c.width = c.height = SS;
    var g = c.getContext('2d');
    if (ao) {
      var sh = g.createRadialGradient(SC + 4, SC + 6, SR * .5, SC + 4, SC + 6, SR * 1.45);
      sh.addColorStop(0, 'rgba(58,32,4,.4)'); sh.addColorStop(1, 'rgba(58,32,4,0)');
      g.fillStyle = sh; g.fillRect(0, 0, SS, SS);
    }
    var gr = g.createRadialGradient(SC - 7, SC - 9, 1, SC, SC, SR);
    STOPS.forEach(function (s) {
      // darker granules shift to warm amber (shadowed side of the bed), not to olive
      var r = Math.min(255, s[1] * Math.pow(k, .8)), gg = Math.min(255, s[2] * Math.pow(k, 1.25)), b = Math.min(255, s[3] * Math.pow(k, 2.2));
      gr.addColorStop(s[0], 'rgba(' + (r | 0) + ',' + (gg | 0) + ',' + (b | 0) + ',' + s[4] + ')');
    });
    g.fillStyle = gr; g.beginPath(); g.arc(SC, SC, SR - .5, 0, Math.PI * 2); g.fill();
    return c;
  }
  TINTS.forEach(function (k) { SPR.push(makeSprite(k, true)); SPA.push(makeSprite(k, false)); });

  /* ---------- particles ---------- */
  var seed = 7;
  function rnd() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }
  var R = 5.4;                                         // granule radius in photo px (measured on the filled photo)
  var VTOP = 840 / LEN;                                // speed of the bed surface, tube lengths per second
  var EXPO = 1 / 110;                                  // motion-blur exposure (s): each granule is stretched along the
                                                       // flow by speed x EXPO, like a camera at a 180-degree shutter;
                                                       // without it rows moving > 1 pitch per frame strobe backwards
  function baseH(u) { return .56 - .1 * Math.max(0, (u - .3) / .7); }   // ~45-55% of the diameter, thinner where it climbs
  function dune(u, t) {                                // travelling dunes (dense-phase 'dune flow'), ~1 +/- .16
    return 1 + .11 * Math.sin(6.2832 * (2.1 * u - .7 * t)) + .05 * Math.sin(6.2832 * (5.3 * u - 1.6 * t) + 1.3);
  }
  var M = 0, MT = 0, J = 0, JT = 0, UJ = .5;          // regime (0 dense .. 1 dilute) and air pulse, eased
  function jet(u) { var x = (u - UJ) / .075; return J * Math.exp(-x * x); }
  function bedH(u, t) {                                // bed height as a fraction of the tube diameter
    return baseH(u) * dune(u, t) * (1 - .8 * M) + jet(u) * (.2 - .08 * M);
  }
  function mult(u) { return (1 + 1.9 * M) * (1 + .8 * jet(u)); }
  // Dense bed = packed rows (hexagonal offset, jittered) in two depth layers. Each row slides at its own speed
  // (shear: slow on the floor, fast on top), so rows pass each other without gaps or clumps.
  var bed = [], air = [], n, NR = 12, PER = Math.round(LEN / (1.72 * R));
  function sprite(b, z) { return SPR[Math.max(0, Math.min(5, Math.round((.32 * b + .5 * z + .18 * rnd()) * 5)))]; }
  for (var layer = 0; layer < 2; layer++) {
    for (var row = 0; row < NR; row++) {
      var b = (row + .5) / NR, rs = VTOP * (.2 + .8 * Math.pow(b, 1.25));
      for (n = 0; n < PER; n++) {
        var z = layer ? .6 + .4 * rnd() : .35 * rnd();
        bed.push({ u: (n + (row % 2) * .5 + layer * .27 + (rnd() - .5) * .5) / PER, b: b + (rnd() - .5) * .6 / NR, z: z,
          r: R * (.84 + .3 * rnd()) * (.86 + .24 * z), s: rs, sp: sprite(b, z), ph: rnd() * 6.28, w: 2 + rnd() * 3 });
      }
    }
  }
  for (n = 0; n < Math.round(PER * 1.2); n++) {         // loose top layer riding on the surface
    var zt = rnd();
    bed.push({ u: rnd(), b: .97 + rnd() * .14, z: zt, r: R * (.84 + .3 * rnd()), s: VTOP * (1 + rnd() * .15), sp: sprite(1, .5 + zt / 2),
      ph: rnd() * 6.28, w: 2 + rnd() * 3 });
  }
  bed.sort(function (p, q) { return p.z - q.z; });     // back to front
  function blur(p) { p.kx = 1 + p.s * LEN * EXPO / (2 * p.r); }
  bed.forEach(blur);
  function hop(p) { p.k = 1.5 + rnd() * 3.5; p.ph = rnd(); p.a = .18 + rnd() * .55; }
  for (n = 0; n < 330; n++) {                          // 95 always airborne; the rest only show in the dilute regime
    var q = { u: rnd(), r: R * (.75 + .3 * rnd()), s: VTOP * (1.5 + rnd() * 1.1), sp: SPA[3 + (rnd() * 3 | 0)],
      v0: .06 + .86 * rnd(), w0: 1 + rnd() * 2.5, ex: n >= 95 };
    hop(q); blur(q); air.push(q);
  }

  /* ---------- rendering ---------- */
  var glass = new Image(), glassOk = false;
  glass.onload = function () { glassOk = true; draw(); };
  glass.src = cv.getAttribute('data-glass');
  var scale = 1;
  function size() {
    var r = cv.getBoundingClientRect(), dpr = Math.min(window.devicePixelRatio || 1, 2);
    var w = Math.max(1, Math.round(r.width * dpr)), h = Math.max(1, Math.round(r.height * dpr));
    if (cv.width !== w || cv.height !== h) { cv.width = w; cv.height = h; }
    scale = w / BW;
  }
  var T = 0;
  function draw() {
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, cv.width, cv.height);
    ctx.setTransform(scale, 0, 0, scale, -BOX[0] * scale, -BOX[1] * scale);
    ctx.save();
    ctx.beginPath(); ctx.moveTo(CLIP[0][0], CLIP[0][1]);
    for (var c = 1; c < CLIP.length; c++) ctx.lineTo(CLIP[c][0], CLIP[c][1]);
    ctx.closePath(); ctx.clip();
    var k, p, h, v, f, an, cs, sn, ox = -BOX[0] * scale, oy = -BOX[1] * scale;
    // bed body: the packed mass behind the visible granules, so the bed never looks see-through
    ctx.beginPath();
    for (k = 0; k <= 64; k++) { pos(k / 64, 0); if (k) ctx.lineTo(P[0], P[1]); else ctx.moveTo(P[0], P[1]); }
    for (k = 64; k >= 0; k--) { pos(k / 64, bedH(k / 64, T) * .86); ctx.lineTo(P[0], P[1]); }
    ctx.closePath(); ctx.fillStyle = '#8E5E14'; ctx.globalAlpha = 1 - .9 * M; ctx.fill(); ctx.globalAlpha = 1;
    var km;
    for (k = 0; k < bed.length; k++) {
      p = bed[k]; h = bedH(p.u, T);
      if (M > .01 && (k % 3) && (k * .618) % 1 < M * 1.1) continue;   // dilute: the bed thins out gradually to a saltating layer
      km = Math.min(1 + (p.kx - 1) * mult(p.u), 2.4);
      v = p.b * h + .012 * Math.sin(T * p.w + p.ph);
      // compression wave travelling with the dunes: a displacement (not a velocity) field, so granules surge over a
      // crest and lag in a trough (~ +/-15% speed) without ever clumping or opening holes in the bed
      pos(p.u + .011 * p.b * Math.sin(6.2832 * (2.1 * p.u - .7 * T) - 1.2), Math.max(.015, v)); f = p.r / SR;
      if (km < 1.08) { ctx.setTransform(scale, 0, 0, scale, ox, oy); ctx.drawImage(p.sp, P[0] - SC * f, P[1] - SC * f, SS * f, SS * f); continue; }
      an = Math.atan2(A[1], A[0]); cs = Math.cos(an) * scale; sn = Math.sin(an) * scale;
      ctx.setTransform(cs, sn, -sn, cs, ox + P[0] * scale, oy + P[1] * scale);
      ctx.drawImage(p.sp, -SC * f * km, -SC * f, SS * f * km, SS * f);
    }
    for (k = 0; k < air.length; k++) {
      p = air[k];
      if (p.ex && M < .02) continue;
      h = bedH(p.u, T);
      var fr = (p.u * p.k + p.ph) % 1, jt = jet(p.u);
      v = h + (.9 - h) * Math.min(1, p.a * (1 + 1.3 * jt)) * Math.sin(Math.PI * fr);
      v = v * (1 - M) + (p.v0 + .035 * Math.sin(T * p.w0 * 2 + p.ph * 6)) * M;
      pos(p.u, v);
      an = Math.atan2(A[1], A[0]) - Math.cos(Math.PI * fr) * .5 * p.a * (1 - M); cs = Math.cos(an) * scale; sn = Math.sin(an) * scale;
      ctx.setTransform(cs, sn, -sn, cs, ox + P[0] * scale, oy + P[1] * scale);
      f = p.r / SR; km = Math.min(1 + (p.kx - 1) * mult(p.u), 2.6 - .4 * M);
      if (p.ex) ctx.globalAlpha = M;
      ctx.drawImage(p.sp, -SC * f * km, -SC * f, SS * f * km, SS * f);
      ctx.globalAlpha = 1;
    }
    ctx.setTransform(scale, 0, 0, scale, ox, oy);
    shade(0, .07); shade(1, .93);
    ctx.restore();
    if (glassOk) ctx.drawImage(glass, BOX[0], BOX[1], BW, BH);
  }
  function shade(u0, u1) {                             // darkness inside the steel flange, fading into the glass
    var a = pos(u0, .5).slice(), b = pos(u1, .5).slice(), gr = ctx.createLinearGradient(a[0], a[1], b[0], b[1]);
    gr.addColorStop(0, 'rgba(34,24,8,.55)'); gr.addColorStop(1, 'rgba(34,24,8,0)');
    ctx.beginPath();
    for (var k = 0; k <= 8; k++) { pos(u0 + (u1 - u0) * k / 8, -.05); if (k) ctx.lineTo(P[0], P[1]); else ctx.moveTo(P[0], P[1]); }
    for (k = 8; k >= 0; k--) { pos(u0 + (u1 - u0) * k / 8, 1.05); ctx.lineTo(P[0], P[1]); }
    ctx.closePath(); ctx.fillStyle = gr; ctx.fill();
  }
  function step(dt) {
    var k, p;
    var e = 1 - Math.exp(-dt * 2.6);
    M += (MT - M) * e; J += (JT - J) * (1 - Math.exp(-dt * (JT > J ? 7 : 2.2)));
    for (k = 0; k < bed.length; k++) { p = bed[k]; p.u += p.s * dt * mult(p.u); if (p.u > 1) p.u -= 1; }
    for (k = 0; k < air.length; k++) { p = air[k]; p.u += p.s * dt * mult(p.u) * (1 + .5 * M); if (p.u > 1) { p.u -= 1; hop(p); } }
    T += dt;
  }

  var onScreen = true, last = 0, raf = 0;
  var slide = cv.closest('[data-slide]');   // hero slides: only simulate while the pipe photo is (being) shown
  function shown() { return !slide || slide.classList.contains('is-on') || slide.classList.contains('is-leaving'); }
  function running() { return onScreen && shown() && !reduce.matches && !hero.classList.contains('is-paused') && !document.hidden; }
  function frame(now) {
    raf = 0;
    if (!running()) { last = 0; return; }
    var dt = last ? Math.min((now - last) / 1000, .05) : 0;
    last = now;
    step(dt); draw();
    raf = requestAnimationFrame(frame);
  }
  function kick() { if (!raf && running()) raf = requestAnimationFrame(frame); }

  /* regime (data-mode) and pointer air pulse */
  function readMode() { MT = cv.getAttribute('data-mode') === 'dilute' ? 1 : 0; if (!running()) { M = MT; draw(); } kick(); }
  readMode();
  new MutationObserver(readMode).observe(cv, { attributes: true, attributeFilter: ['data-mode'] });
  if (cv.hasAttribute('data-mode')) {
    var C = [];
    for (i = 0; i <= 80; i++) { pos(i / 80, .5); C.push([P[0], P[1]]); }
    hero.addEventListener('pointermove', function (e) {
      if (e.pointerType === 'touch') return;
      var r = cv.getBoundingClientRect(); if (!r.width) return;
      var x = BOX[0] + (e.clientX - r.left) / r.width * BW, y = BOX[1] + (e.clientY - r.top) / r.height * BH, best = 1e9, bu = 0;
      for (var c = 0; c < C.length; c++) { var dx = C[c][0] - x, dy = C[c][1] - y, d = dx * dx + dy * dy; if (d < best) { best = d; bu = c / 80; } }
      var on = best < 150 * 150;
      JT = on ? 1 : 0; if (on) UJ = bu;
      cv.classList.toggle('is-blowing', on);
      kick();
    }, { passive: true });
    hero.addEventListener('pointerleave', function () { JT = 0; cv.classList.remove('is-blowing'); });
  }

  size(); draw(); kick();
  if ('ResizeObserver' in window) new ResizeObserver(function () { size(); draw(); }).observe(cv);
  else window.addEventListener('resize', function () { size(); draw(); });
  if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { onScreen = en[0].isIntersecting; kick(); }).observe(cv);
  new MutationObserver(kick).observe(hero, { attributes: true, attributeFilter: ['class'] });
  if (slide) new MutationObserver(kick).observe(slide, { attributes: true, attributeFilter: ['class'] });
  document.addEventListener('visibilitychange', kick);
  if (reduce.addEventListener) reduce.addEventListener('change', function () { draw(); kick(); });
})();
