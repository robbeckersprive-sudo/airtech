"""Uitvoeringen (ATEX / food-grade): CSV matrix <-> execution_data.CONFIRMED.

    python tools/import_executions.py                 import docs/uitvoeringen-matrix.csv into CONFIRMED
    python tools/import_executions.py <file.csv>      import another file (e.g. a filled-in copy)
    python tools/import_executions.py --template      (re)write docs/uitvoeringen-matrix.csv from the data, all '?'
    python tools/import_executions.py --check         validate the CSV, change nothing

CSV columns: categorie, uitvoering, variant, atex, food, opmerking (UTF-8, comma separated).
Cell values for atex / food: 'ja' = confirmed by Airtechnic, 'nee' = not supplied, '?' or empty = unknown.
Only 'ja' ends up in CONFIRMED; everything else stays invisible on the site. After importing: python src/build.py.
"""
from pathlib import Path
import csv, re, sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from category_data import CATEGORIES
from cyclone_category_data import CYCLONES
from execution_data import EXECUTIONS

CSV_PATH = ROOT / 'docs' / 'uitvoeringen-matrix.csv'
DATA_PATH = ROOT / 'src' / 'execution_data.py'
COLUMNS = ['categorie', 'uitvoering', 'variant', *EXECUTIONS, 'opmerking']
VALUES = {'ja', 'nee', '?', ''}
CONTEXT = {
    'cyclonen': 'ATEX-uitvoeringen (aarding, ontlasting) en RVS-uitvoeringen voor food zijn bij fabrikanten gangbaar; bevestig leverbaarheid, categorie en materialen.',
    'blowers-ventilatoren': 'ATEX-uitvoeringen van ventilatoren en blowers zijn bij fabrikanten gangbaar; bevestig leverbaarheid, categorie en of het om de stof- of schone zijde gaat.',
    'filters': 'ATEX-uitvoeringen (o.a. antistatisch medium, ontlasting) en food-uitvoeringen zijn bij fabrikanten gangbaar; bevestig leverbaarheid, categorie en materialen.',
    'doseersluizen': 'ATEX-uitvoeringen van doseersluizen zijn bij fabrikanten gangbaar, soms ook als beproefde ontkoppeling; bevestig leverbaarheid en categorie.',
    'leidingwerk-koppelingen': 'Leidingwerk is meestal geen ATEX-apparatuur, wel moet het geaard en doorverbonden zijn. Food: RVS gangbaar; bevestig materiaal en afwerking.',
    'bigbag-stations': 'ATEX- en hygiënische uitvoeringen van big-bagstations zijn gangbaar; bevestig leverbaarheid, categorie en materialen.',
    'afsluiters': 'ATEX- en food-uitvoeringen van afsluiters zijn gangbaar; bevestig leverbaarheid, categorie en afdichtingsmaterialen.',
    'zeven': 'ATEX- en food-uitvoeringen van zeven zijn gangbaar; bevestig leverbaarheid en categorie.',
}


def catalogue():
    """(category, name, variant) for every uitvoering, in site order."""
    rows = [('cyclonen', it.name, it.variant) for it in CYCLONES['items']]
    for slug, data in CATEGORIES.items():
        rows += [(slug, it['name'], it['variant']) for it in data['items']]
    return rows


def write_template():
    CSV_PATH.parent.mkdir(exist_ok=True)
    with CSV_PATH.open('w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(COLUMNS)
        for cat, name, variant in catalogue():
            w.writerow([cat, name, variant, *('?' for _ in EXECUTIONS), CONTEXT.get(cat, '')])
    print(f'Wrote {CSV_PATH.relative_to(ROOT)} ({len(catalogue())} rows, all unknown).')


def read(path):
    known = {(c, v) for c, _n, v in catalogue()}
    confirmed, errors = set(), []
    with Path(path).open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        missing = [c for c in COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            sys.exit(f'Missing columns: {", ".join(missing)}')
        for line, row in enumerate(reader, 2):
            key = (row['categorie'].strip(), row['variant'].strip())
            if key not in known:
                errors.append(f'line {line}: unknown categorie/variant {key}')
                continue
            for ex in EXECUTIONS:
                value = (row[ex] or '').strip().lower()
                if value not in VALUES:
                    errors.append(f'line {line}: {ex}={row[ex]!r} (use ja, nee or ?)')
                elif value == 'ja':
                    confirmed.add((*key, ex))
    if errors:
        sys.exit('\n'.join(errors))
    return confirmed


def write_confirmed(confirmed):
    src = DATA_PATH.read_text(encoding='utf-8')
    body = ('CONFIRMED = frozenset()' if not confirmed else
            'CONFIRMED = frozenset({\n' + ''.join(f'    {t!r},\n' for t in sorted(confirmed)) + '})')
    new = re.sub(r'(# >>> CONFIRMED[^\n]*\n).*?(\n# <<< CONFIRMED)', lambda m: m.group(1) + body + m.group(2), src, flags=re.S)
    DATA_PATH.write_text(new, encoding='utf-8', newline='\n')
    print(f'CONFIRMED: {len(confirmed)} confirmed uitvoering(en) written to {DATA_PATH.relative_to(ROOT)}. Now run: python src/build.py')


if __name__ == '__main__':
    args = sys.argv[1:]
    if args[:1] == ['--template']:
        write_template()
    elif args[:1] == ['--check']:
        print(f'OK: {len(read(args[1] if len(args) > 1 else CSV_PATH))} confirmed in the CSV; nothing written.')
    else:
        write_confirmed(read(args[0] if args else CSV_PATH))
