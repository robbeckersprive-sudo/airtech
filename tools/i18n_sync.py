"""Maintain the content catalogues src/locales/<lang>.json (Meertaligheid, see README).

    python tools/i18n_sync.py status                 counts per language (after `python src/build.py`)
    python tools/i18n_sync.py export DIR [SIZE]      write the untranslated segments as numbered batches
                                                     (DIR/batch-NN.tsv: id <TAB> Dutch segment)
    python tools/i18n_sync.py import FILE...         merge translations: JSON {id: [en, de]} next to its batch
    python tools/i18n_sync.py check                  validate catalogues (tags, placeholders, [TBD] markers)
    python tools/i18n_sync.py prune                  drop entries no page uses any more (needs a full build)

The build writes src/locales/missing-<lang>.json for segments without a translation (Dutch is used as fallback).
Exit code 1 from `check` when a translation changes the inline markup or drops a [TBD] marker.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
import i18n  # noqa: E402

TARGETS = [c for c in i18n.LANGS if c != i18n.DEFAULT]
TAG = re.compile(r'<(/?)([a-zA-Z][\w-]*)([^>]*)>')


def load(code):
    file = os.path.join(i18n.LOCALES, f'{code}.json')
    if not os.path.exists(file):
        return {}
    with open(file, encoding='utf-8') as f:
        return json.load(f)


def save(code, data):
    os.makedirs(i18n.LOCALES, exist_ok=True)
    with open(os.path.join(i18n.LOCALES, f'{code}.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(dict(sorted(data.items(), key=lambda kv: kv[0].lower())), f, ensure_ascii=False, indent=1)
        f.write('\n')


def missing(code):
    file = os.path.join(i18n.LOCALES, f'missing-{code}.json')
    if not os.path.exists(file):
        return {}
    with open(file, encoding='utf-8') as f:
        return json.load(f)


def tags(s):
    """Inline markup signature: tag names with their attributes, order-insensitive."""
    return sorted((m.group(1), m.group(2).lower(), m.group(3).strip()) for m in TAG.finditer(s))


def problems(nl, tx):
    out = []
    if tags(nl) != tags(tx):
        out.append('inline markup differs')
    for marker in re.findall(r'\[TBD[^\]]*\]', nl):
        if marker not in tx:
            out.append(f'marker {marker} missing')
    for ph in re.findall(r'\{\w+\}', nl):
        if ph not in tx:
            out.append(f'placeholder {ph} missing')
    return out


def cmd_status():
    for code in TARGETS:
        print(f'{code}: {len(load(code))} entries, {len(missing(code))} missing in the last build')


def cmd_export(folder, size=200):
    os.makedirs(folder, exist_ok=True)
    keys = list(dict.fromkeys(k for code in TARGETS for k in missing(code)))
    for n, start in enumerate(range(0, len(keys), size), 1):
        batch = {f'{n:02d}-{i:03d}': k for i, k in enumerate(keys[start:start + size])}
        with open(os.path.join(folder, f'batch-{n:02d}.json'), 'w', encoding='utf-8', newline='\n') as f:
            json.dump(batch, f, ensure_ascii=False, indent=0)
        with open(os.path.join(folder, f'batch-{n:02d}.tsv'), 'w', encoding='utf-8', newline='\n') as f:
            f.writelines(f'{i}\t{k}\n' for i, k in batch.items())
    print(f'{len(keys)} segments in {-(-len(keys) // size)} batches -> {folder}')


def cmd_import(files):
    cats = {code: load(code) for code in TARGETS}
    bad = 0
    for file in files:
        with open(file, encoding='utf-8') as f:
            tx = json.load(f)
        batch_file = os.path.join(os.path.dirname(file), 'batch-' + os.path.basename(file).split('-')[1][:2] + '.json')
        with open(batch_file, encoding='utf-8') as f:
            source = json.load(f)
        for key, values in tx.items():
            nl = source[key]
            for code, value in zip(TARGETS, values):
                issues = problems(nl, value)
                if issues:
                    bad += 1
                    print(f'{key} [{code}] {", ".join(issues)}\n  nl: {nl}\n  {code}: {value}')
                cats[code][nl] = value
    for code, data in cats.items():
        save(code, data)
    print(f'imported {len(files)} file(s); {bad} issue(s)')
    return 1 if bad else 0


def cmd_check():
    bad = 0
    for code in TARGETS:
        for nl, value in load(code).items():
            for issue in problems(nl, value):
                bad += 1
                print(f'[{code}] {issue}: {nl[:90]}')
    print(f'{bad} issue(s)')
    return 1 if bad else 0


def cmd_prune():
    """Remove entries that no page uses any more: rebuild with recording, then keep the used keys only."""
    import build
    used = {code: set() for code in TARGETS}
    original = i18n.tr

    def spy(text, code=None, record=True):
        code = code or i18n.lang()
        if code in used and text:
            used[code].add(i18n.norm(text))
        return original(text, code, record)

    i18n.tr = spy
    build.main()
    for code in TARGETS:
        data = load(code)
        keep = {k: v for k, v in data.items() if i18n.norm(k) in used[code]}
        print(f'{code}: {len(data) - len(keep)} unused entries removed')
        save(code, keep)


if __name__ == '__main__':
    args = sys.argv[1:] or ['status']
    if args[0] == 'export':
        cmd_export(args[1], int(args[2]) if len(args) > 2 else 200)
    elif args[0] == 'import':
        sys.exit(cmd_import(args[1:]))
    elif args[0] == 'check':
        sys.exit(cmd_check())
    elif args[0] == 'prune':
        cmd_prune()
    else:
        cmd_status()
