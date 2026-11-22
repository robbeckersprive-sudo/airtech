/* Airtechnic "Flow" — real-time 3D rotor for the hero's dosing sheet (Nov 22).
   Based on the supplied package "doseersluis-3d-pakket" (main.js: geometry, lighting and the fit on the 1536x1024
   housing photo; Three.js 0.180.0, MIT). Changes for the site:
   - lives in the hero's 3:2 stage box ([data-rotor3d]); photo, canvas and front-rim SVG share that box;
   - speed follows the hero instrument (slide data-mode a = Laag 4 rpm, b = Hoog 12 rpm), eased;
   - runs only while the sheet is shown, on screen, not paused (hero .is-paused), tab visible, no reduced motion;
   - builds lazily the first time the sheet is shown; without WebGL the existing picture stays (no empty machine);
   - granules: an instanced set per pocket that fills under the inlet (top), rides down full and empties over the
     outlet (bottom).
   Build: see tools/rotor3d/README.txt. Output: assets/js/rotor3d.js */
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const FIT = Object.freeze({ cx: 816, cy: 494, radius: 266, ratio: 219 / 266, roll: 2.28, depth: 106 });
const RPM = { a: 4, b: 12 };
const host = document.querySelector('[data-rotor3d]');
if (host) init();

function init() {
  const box = host.closest('.ds-box'), slide = host.closest('.ds-slide'), hero = host.closest('[data-ds]');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  let renderer, scene, camera, rotor, grains, raf = 0, last, angle = 0, rpm = 0, built = false, failed = false, onScreen = true;
  const POCKETS = 8, PER = 46, dummy = new THREE.Object3D(), fills = new Array(POCKETS).fill(-1), slots = [];

  const shown = () => slide.classList.contains('is-on') || slide.classList.contains('is-leaving');
  const runs = () => built && !failed && shown() && onScreen && !document.hidden && !reduce.matches && !hero.classList.contains('is-paused');

  function fail() {
    failed = true; cancelAnimationFrame(raf);
    box.classList.remove('has-rotor3d');
  }
  function cylinder(radius, depth, material, z, parent, segments = 128) {
    const g = new THREE.CylinderGeometry(radius, radius, depth, segments, 1, false); g.rotateX(Math.PI / 2);
    const m = new THREE.Mesh(g, material); m.position.z = z; m.castShadow = m.receiveShadow = true; parent.add(m); return m;
  }
  function marksTexture() {
    const c = document.createElement('canvas'); c.width = c.height = 512;
    const ctx = c.getContext('2d'), px = ctx.createImageData(512, 512);
    for (let y = 0; y < 512; y++) for (let x = 0; x < 512; x++) {
      const r = Math.hypot(x - 255.5, y - 255.5), h = Math.sin(x * 12.9898 + y * 78.233) * 43758.5453, n = h - Math.floor(h);
      const v = Math.round(140 + 15 * Math.sin(r * 4.3) + 5 * (n - .5)), i = (y * 512 + x) * 4;
      px.data[i] = px.data[i + 1] = px.data[i + 2] = v; px.data[i + 3] = 255;
    }
    ctx.putImageData(px, 0, 0);
    const t = new THREE.CanvasTexture(c); t.anisotropy = Math.min(renderer.capabilities.getMaxAnisotropy(), 8); return t;
  }
  function build() {
    if (built || failed) return;
    try {
      renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true, powerPreference: 'high-performance' });
    } catch (e) { fail(); return; }
    renderer.setClearColor(0x000000, 0);
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
    renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.domElement.setAttribute('aria-hidden', 'true');
    renderer.domElement.addEventListener('webglcontextlost', e => { e.preventDefault(); fail(); });
    host.appendChild(renderer.domElement);

    scene = new THREE.Scene();
    camera = new THREE.OrthographicCamera(-768, 768, 512, -512, 1, 3000); camera.position.set(0, 0, 1400);
    const env = new RoomEnvironment(), pmrem = new THREE.PMREMGenerator(renderer);
    scene.environment = pmrem.fromScene(env, .045).texture; scene.environmentIntensity = 1.7; env.dispose(); pmrem.dispose();
    scene.add(new THREE.HemisphereLight(0xe8f0f6, 0x444a51, .45));
    const key = new THREE.DirectionalLight(0xfff9ef, 2.2); key.position.set(-550, 650, 900); key.target.position.set(48, 18, -45);
    key.castShadow = true; key.shadow.mapSize.set(2048, 2048);
    Object.assign(key.shadow.camera, { left: -430, right: 430, top: 430, bottom: -430, near: 100, far: 2000 });
    key.shadow.bias = -.0003; key.shadow.normalBias = .35; scene.add(key, key.target);
    const fill = new THREE.DirectionalLight(0xdce9f5, 1.4); fill.position.set(600, -50, 600); scene.add(fill);

    const pose = new THREE.Group();
    pose.position.set(FIT.cx - 768, 512 - FIT.cy, 0);
    pose.rotation.set(0, -Math.acos(FIT.ratio), THREE.MathUtils.degToRad(FIT.roll), 'ZYX');
    scene.add(pose);
    const marks = marksTexture();
    const metal = new THREE.MeshStandardMaterial({ color: 0xa8adb0, metalness: .96, roughness: .28 });
    const machined = new THREE.MeshPhysicalMaterial({ color: 0xc6c9cc, metalness: 1, roughness: .34, roughnessMap: marks, bumpMap: marks, bumpScale: .14 });
    const pocketMat = new THREE.MeshPhysicalMaterial({ color: 0x74797e, metalness: .95, roughness: .55, roughnessMap: marks, bumpMap: marks, bumpScale: .12 });
    const screwMat = new THREE.MeshStandardMaterial({ color: 0x9ba0a4, metalness: 1, roughness: .27 });
    const dark = new THREE.MeshStandardMaterial({ color: 0x171b20, metalness: .5, roughness: .55 });

    const barrelG = new THREE.CylinderGeometry(269, 269, FIT.depth + 8, 160, 1, true); barrelG.rotateX(Math.PI / 2);
    const barrel = new THREE.Mesh(barrelG, new THREE.MeshStandardMaterial({ color: 0x535b63, metalness: .8, roughness: .43, side: THREE.BackSide }));
    barrel.position.z = -FIT.depth / 2; barrel.receiveShadow = true; pose.add(barrel);
    cylinder(269, 3, dark, -FIT.depth - 6, pose);

    rotor = new THREE.Group(); pose.add(rotor);
    cylinder(264, 4, pocketMat, -FIT.depth, rotor);
    cylinder(55, FIT.depth, metal, -FIT.depth / 2, rotor);
    for (let i = 0; i < 8; i++) {
      const a = i * Math.PI / 4;
      const vane = new THREE.Mesh(new THREE.BoxGeometry(211, 3.8, FIT.depth), metal);
      vane.position.set(Math.cos(a) * 158.5, Math.sin(a) * 158.5, -FIT.depth / 2); vane.rotation.z = a;
      vane.castShadow = vane.receiveShadow = true; rotor.add(vane);
      const edge = new THREE.Mesh(new THREE.CylinderGeometry(1.45, 1.45, 211, 8), machined);
      edge.rotation.z = a - Math.PI / 2; edge.position.set(Math.cos(a) * 158.5, Math.sin(a) * 158.5, .15); rotor.add(edge);
    }
    cylinder(67, 12, metal, -2, rotor); cylinder(62, 3, machined, 5, rotor); cylinder(45, .65, machined, 6.8, rotor);
    for (const r of [45.2, 61.5]) { const ring = new THREE.Mesh(new THREE.TorusGeometry(r, .42, 8, 128), dark); ring.position.z = 7.2; rotor.add(ring); }
    for (let i = 0; i < 6; i++) {
      const a = i * Math.PI / 3 + Math.PI / 6, s = new THREE.Group(); s.position.set(Math.cos(a) * 53, Math.sin(a) * 53, 7); rotor.add(s);
      cylinder(6.2, 1.6, dark, 0, s, 32); cylinder(5.5, 2, screwMat, 1, s, 32); cylinder(2.8, .25, dark, 2.12, s, 6).rotation.z = a;
    }

    // granules: PER per pocket, packed from the pocket floor (outer rim) inwards, inside the pocket's depth
    let seed = 11; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
    const gold = new THREE.MeshStandardMaterial({ color: 0xb5761a, metalness: .05, roughness: .5, envMapIntensity: .55 });
    grains = new THREE.InstancedMesh(new THREE.SphereGeometry(7.2, 14, 10), gold, POCKETS * PER);
    grains.castShadow = grains.receiveShadow = true; grains.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
    for (let k = 0; k < POCKETS; k++) {
      const mid = k * Math.PI / 4 + Math.PI / 8, list = [];
      for (let j = 0; j < PER; j++) {
        const r = 248 - Math.pow(rnd(), .8) * 170, half = (Math.PI / 8) * (1 - 14 / r) * .92, a = mid + (rnd() * 2 - 1) * half;
        list.push({ x: Math.cos(a) * r, y: Math.sin(a) * r, z: -FIT.depth + 10 + rnd() * (FIT.depth - 22), s: .8 + rnd() * .45, r });
      }
      list.sort((p, q) => q.r - p.r);                 // outer grains first: a pocket fills from its rim
      slots.push(list);
    }
    rotor.add(grains);
    setFills(true);

    new ResizeObserver(() => { renderer.setSize(host.clientWidth, host.clientHeight, false); render(); }).observe(host);
    renderer.setSize(host.clientWidth, host.clientHeight, false);
    built = true; box.classList.add('has-rotor3d');
    render(); kick();
  }

  // fill state per pocket from its position: fills under the inlet (top), full on the way down, empties over the outlet
  function fillAt(t) {                                   // t: 0 at the top, increasing in the direction of motion
    t = ((t % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI);
    if (t < .45) return t / .45;
    if (t < Math.PI - .2) return 1;
    if (t < Math.PI + .45) return 1 - (t - (Math.PI - .2)) / .65;
    return 0;
  }
  function setFills(force) {
    let dirty = false;
    for (let k = 0; k < POCKETS; k++) {
      const world = k * Math.PI / 4 + Math.PI / 8 + angle;   // pocket centre in the pose frame (+y = up)
      const n = Math.round(fillAt(Math.PI / 2 - world) * PER);
      if (!force && n === fills[k]) continue;
      fills[k] = n; dirty = true;
      slots[k].forEach((p, j) => {
        dummy.position.set(p.x, p.y, p.z); dummy.scale.setScalar(j < n ? p.s : 0); dummy.updateMatrix();
        grains.setMatrixAt(k * PER + j, dummy.matrix);
      });
    }
    if (dirty) grains.instanceMatrix.needsUpdate = true;
  }
  function render() { if (renderer && rotor && !failed) { rotor.rotation.z = angle; setFills(false); renderer.render(scene, camera); } }
  function frame(time) {
    raf = 0;
    if (!runs()) { last = undefined; return; }
    const dt = last === undefined ? 0 : Math.min((time - last) / 1000, .05); last = time;
    const target = RPM[slide.getAttribute('data-mode')] || RPM.a;
    rpm += (target - rpm) * (1 - Math.exp(-dt * 2.2));
    angle = (angle - dt * rpm * Math.PI / 30) % (2 * Math.PI);
    render();
    raf = requestAnimationFrame(frame);
  }
  function kick() { if (!raf && runs()) raf = requestAnimationFrame(frame); }

  // build lazily when the sheet is first shown; keep in step with the hero
  const watch = new MutationObserver(() => { if (shown()) build(); kick(); });
  watch.observe(slide, { attributes: true, attributeFilter: ['class', 'data-mode'] });
  watch.observe(hero, { attributes: true, attributeFilter: ['class'] });
  if ('IntersectionObserver' in window) new IntersectionObserver(e => { onScreen = e[0].isIntersecting; kick(); }).observe(hero);
  document.addEventListener('visibilitychange', kick);
  if (shown()) build();
  window.rotor3d = { state: () => ({ built, failed, rpm, angle, fills: fills.slice(), running: runs() }) };
}
