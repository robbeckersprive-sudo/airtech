"""Shared helper for the template checks (Nov 27): strip blocks that are optional per page by design, so the
"identical structure" comparisons keep guarding the template while pages may differ in:
- the number of FAQ items (category / solution pages with an extra ATEX question): validated separately (count_faq)
- sector chips vs the neutral sentence on product pages (derived from sector_data.SECTORS[*]['components'])
- the confirmed "Uitvoeringen" row / labels / chip group (execution_data.CONFIRMED; empty by default)
- per-solution notes, "Toegepast in" chips and an extra knowledge link
Everything outside these blocks must still match tag for tag."""
import re

_OPTIONAL = [
    r'<details class="faq__item".*?</details>',
    r'<(div|p) class="detail-sectors">.*?</\1>',
    r'<tr data-executions="[^"]*">.*?</tr>',
    r'<ul class="cv-card__exec".*?</ul>',
    r'<div class="cv-chips cv-chips--exec".*?</div>',
    r'<p class="solution-note">.*?</p>',
    r'<p class="solution-applied">.*?</p><ul class="solution-applied__list">.*?</ul>',
    # content-dependent since the v2 templates (these made the checks fail at HEAD before Nov 27):
    r'<a class="link"[^>]*download="Productfolder[^"]*"[^>]*>.*?</a>',   # PDF exists only where rendered
]
_LIST_ITEMS = ('cv-card__tags', 'cv-tags')   # one <li> per application: count varies by item


def normalize(html):
    for pattern in _OPTIONAL:
        html = re.sub(pattern, '', html, flags=re.S)
    for cls in _LIST_ITEMS:
        html = re.sub(r'(<ul class="' + cls + r'"[^>]*>).*?(</ul>)', r'', html, flags=re.S)
    # link rows in heading areas may carry one extra onward link (category related head, solution FAQ side)
    html = re.sub(r'(<div class="cv-related__head">.*?</h2>).*?(</div>)', r'\1\2', html, flags=re.S)
    html = re.sub(r'(<h2 class="h2" id="vragen" tabindex="-1">.*?</h2>).*?(</div>)', r'\1\2', html, count=1, flags=re.S)
    return html


def count_faq(html):
    return html.count('<details class="faq__item"')
