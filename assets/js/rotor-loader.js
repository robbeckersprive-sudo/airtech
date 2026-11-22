/* Load the 3D renderer only when its sheet is requested; the photo and SVG remain immediately available. */
(function () {
  var script = document.currentScript;
  var host = document.querySelector('[data-rotor3d]');
  if (!host || !script) return;
  var slide = host.closest('.ds-slide'), loaded = false;
  function load() {
    if (loaded || !slide.classList.contains('is-on')) return;
    loaded = true;
    var renderer = document.createElement('script');
    renderer.src = script.dataset.rotorSrc;
    renderer.onerror = function () { loaded = false; };
    document.head.appendChild(renderer);
  }
  new MutationObserver(load).observe(slide, { attributes: true, attributeFilter: ['class'] });
  load();
})();
