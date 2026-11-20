(() => {
  const controls = document.querySelector('.kb-controls');
  const search = document.querySelector('#kb-search');
  const topic = document.querySelector('#kb-topic');
  const reset = document.querySelector('#kb-reset');
  const count = document.querySelector('#kb-count');

  function normalize(text) {
    return text.toLocaleLowerCase('nl').normalize('NFD')
      .replace(/\p{M}|\u00ad/gu, '').replace(/[^\p{L}\p{N}]+/gu, ' ').trim();
  }

  const groups = Array.from(document.querySelectorAll('.kb-group'), section => {
    const heading = section.querySelector('h2');
    const cards = Array.from(section.querySelectorAll('.card'), card => {
      const snippet = document.createElement('p');
      snippet.className = 'kb-snippet';
      snippet.hidden = true;
      card.querySelector('.card__link').before(snippet);
      return {
        card,
        snippet,
        source: card.dataset.searchText.replace(/\u00ad/g, ''),
        text: normalize([heading.textContent, card.querySelector('h3').textContent,
          card.querySelector('.card__text').textContent, card.dataset.searchText].join(' '))
      };
    });
    return {section, id: heading.id, cards};
  });

  function showSnippet(item, terms) {
    const {source, snippet} = item;
    snippet.replaceChildren();
    snippet.hidden = true;
    if (!terms.length || item.card.hidden) return;

    // Map folded search characters back to the original spelling.
    let folded = '';
    const offsets = [];
    for (let index = 0; index < source.length;) {
      const character = String.fromCodePoint(source.codePointAt(index));
      const normalized = character.toLocaleLowerCase('nl').normalize('NFD').replace(/\p{M}/gu, '')
        .replace(/[^\p{L}\p{N}]/gu, ' ');
      for (const part of normalized) {
        folded += part;
        offsets.push({start: index, end: index + character.length});
      }
      index += character.length;
    }
    const ranges = [];
    for (const term of terms) {
      let position = folded.indexOf(term);
      while (position !== -1) {
        ranges.push({start: offsets[position].start, end: offsets[position + term.length - 1].end});
        position = folded.indexOf(term, position + term.length);
      }
    }
    if (!ranges.length) return;
    ranges.sort((a, b) => a.start - b.start);
    const merged = [];
    for (const range of ranges) {
      const previous = merged[merged.length - 1];
      if (previous && range.start <= previous.end) previous.end = Math.max(previous.end, range.end);
      else merged.push({...range});
    }

    let start = Math.max(0, merged[0].start - 65);
    while (start > 0 && start < merged[0].start && !/\s/.test(source[start - 1])) start++;
    let end = Math.min(source.length, Math.max(start + 230, merged[0].end));
    while (end < source.length && !/\s/.test(source[end])) end++;
    let cursor = start;
    if (start) snippet.append('… ');
    for (const range of merged) {
      if (range.start >= end) break;
      snippet.append(source.slice(cursor, range.start));
      const mark = document.createElement('mark');
      mark.textContent = source.slice(range.start, range.end);
      snippet.append(mark);
      cursor = range.end;
    }
    snippet.append(source.slice(cursor, end), end < source.length ? ' …' : '');
    snippet.hidden = false;
  }

  function render() {
    const terms = normalize(search.value).split(/\s+/).filter(Boolean);
    let matches = 0;
    for (const group of groups) {
      let visible = 0;
      for (const item of group.cards) {
        const {card, text} = item;
        card.hidden = Boolean(topic.value && topic.value !== group.id) || !terms.every(term => text.includes(term));
        showSnippet(item, terms);
        if (!card.hidden) visible++;
      }
      group.section.hidden = visible === 0;
      matches += visible;
    }
    count.textContent = matches ? (matches === 1 ? '1 artikel' : matches + ' artikelen')
      : 'Geen artikelen gevonden. Probeer een andere zoekterm of kies een ander onderwerp.';
    reset.hidden = !search.value && !topic.value;
  }

  function update() {
    render();
    const url = new URL(location.href);
    for (const [key, value] of [['q', search.value.trim()], ['onderwerp', topic.value]]) {
      if (value) url.searchParams.set(key, value);
      else url.searchParams.delete(key);
    }
    history.replaceState(history.state, '', url);
  }

  function restore() {
    const params = new URLSearchParams(location.search);
    search.value = params.get('q') || '';
    const selected = params.get('onderwerp');
    topic.value = groups.some(group => group.id === selected) ? selected : '';
    render();
  }

  search.addEventListener('input', update);
  topic.addEventListener('change', update);
  reset.addEventListener('click', () => {
    search.value = '';
    topic.value = '';
    update();
    search.focus();
  });
  window.addEventListener('pageshow', restore);
  window.addEventListener('popstate', restore);
  restore();
  document.querySelector('.kb-topics').hidden = true;
  controls.hidden = false;
})();
