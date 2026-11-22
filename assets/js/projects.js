/* Progressive enhancement: all cases and original image links work without JS. */
(() => {
  'use strict';
  const form = document.querySelector('[data-project-filters]');
  if (form) {
    const cards = [...document.querySelectorAll('[data-project]')];
    const count = document.querySelector('[data-project-count]');
    const empty = document.querySelector('[data-project-empty]');
    const reset = form.querySelector('[type="reset"]');
    const fields = ['q', 'sector', 'toepassing'];
    const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase(document.documentElement.lang || 'nl');
    const readURL = () => {
      const params = new URLSearchParams(location.search);
      fields.forEach(name => { form.elements[name].value = params.get(name) || ''; });
    };
    const update = (writeURL = true) => {
      const query = normalize(form.elements.q.value.trim());
      const sector = form.elements.sector.value;
      const category = form.elements.toepassing.value;
      let total = 0;
      cards.forEach(card => {
        const match = query.split(/\s+/).every(word => normalize(card.textContent).includes(word)) && (!sector || card.dataset.sector === sector) && (!category || card.dataset.category === category);
        card.hidden = !match;
        if (match) total++;
      });
      count.textContent = `${total} ${total === 1 ? 'project' : 'projecten'} gevonden`;
      empty.hidden = total !== 0;
      reset.hidden = !(query || sector || category);
      document.querySelector('[data-project-invitation]').hidden = !!(query || sector || category);
      if (writeURL) {
        const url = new URL(location.href);
        fields.forEach(name => {
          const value = form.elements[name].value.trim();
          value ? url.searchParams.set(name, value) : url.searchParams.delete(name);
        });
        history.replaceState(null, '', url);
      }
    };
    form.hidden = false;
    readURL(); update(false);
    form.addEventListener('submit', event => event.preventDefault());
    form.addEventListener('input', () => update());
    form.addEventListener('change', () => update());
    form.addEventListener('reset', () => { setTimeout(() => { update(); form.elements.q.focus(); }, 0); });
    document.querySelector('[data-project-reset]').addEventListener('click', () => form.reset());
    addEventListener('popstate', () => { readURL(); update(false); });
  }
  const dialog = document.querySelector('.project-lightbox');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  const photos = [...document.querySelectorAll('[data-project-photo]')];
  let current = 0;
  let opener;
  const show = index => {
    current = (index + photos.length) % photos.length;
    const photo = photos[current];
    const image = dialog.querySelector('[data-photo-image]');
    image.src = photo.href;
    image.alt = photo.dataset.caption;
    dialog.querySelector('[data-photo-caption]').textContent = photo.dataset.caption;
    dialog.querySelector('[data-photo-position]').textContent = `${current + 1} / ${photos.length}`;
  };
  photos.forEach((photo, index) => photo.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault(); opener = photo; show(index); dialog.showModal();
  }));
  dialog.querySelector('[data-photo-close]').addEventListener('click', () => dialog.close());
  dialog.querySelector('[data-photo-prev]').addEventListener('click', () => show(current - 1));
  dialog.querySelector('[data-photo-next]').addEventListener('click', () => show(current + 1));
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault(); show(current + (event.key === 'ArrowRight' ? 1 : -1));
    }
  });
  dialog.addEventListener('click', event => { if (event.target === dialog) {
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  }});
  dialog.addEventListener('close', () => opener?.focus());
})();
