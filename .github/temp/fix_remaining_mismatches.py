import json
import re
import urllib.request
from urllib.parse import quote_plus

NNDC_PATH = '.github/temp/nndc_citations.json'
EXACT_PATH = '.github/temp/exact_dois.json'
VALID_PATH = '.github/temp/doi_metadata_validation.json'
REPORT_PATH = '.github/temp/fix_remaining_mismatches_report.json'

BAD_TITLE = ['symbols and abbreviations', 'editorial board', 'front cover', 'back cover', 'contents', 'index']


def norm(t):
    return re.sub(r'\s+', ' ', (t or '').strip())


def parse_cit(raw):
    raw = norm(raw)
    if raw == 'ENSDF':
        return {'kind': 'ENSDF', 'journal': 'ENSDF', 'vol': '', 'page': '', 'year': ''}

    m = re.search(r'NDS\s*(\d+)\s*,?\s*(\d+)\s*\(?\s*(\d{4})\s*\)?\.?', raw, re.IGNORECASE)
    if m:
        return {'kind': 'NDS', 'journal': 'Nuclear Data Sheets', 'vol': m.group(1), 'page': m.group(2), 'year': m.group(3)}

    m = re.search(r'NP\s*A?\s*(\d+)\s*,?\s*(\d+)\s*\(?\s*(\d{4})\s*\)?\.?', raw, re.IGNORECASE)
    if m:
        return {'kind': 'NPA', 'journal': 'Nuclear Physics A', 'vol': m.group(1), 'page': m.group(2), 'year': m.group(3)}

    m = re.search(r'NDS\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d{4})', raw, re.IGNORECASE)
    if m:
        return {'kind': 'NDS', 'journal': 'Nuclear Data Sheets', 'vol': m.group(1), 'page': m.group(2), 'year': m.group(3)}

    return {'kind': 'UNKNOWN', 'journal': raw, 'vol': '', 'page': '', 'year': ''}


def first_page(p):
    if not p:
        return ''
    return str(p).split('-')[0].strip()


def year_of(item):
    for key in ('published-print', 'published-online', 'issued'):
        val = item.get(key, {})
        parts = val.get('date-parts', []) if isinstance(val, dict) else []
        if parts and parts[0]:
            return str(parts[0][0])
    return ''


def title_of(item):
    t = item.get('title', [])
    return t[0] if t else ''


def journal_of(item):
    c = item.get('container-title', [])
    return c[0] if c else ''


def query_items(q):
    url = f"https://api.crossref.org/works?query.bibliographic={quote_plus(q)}&rows=40&select=DOI,title,author,container-title,volume,page,published-print,published-online,issued"
    req = urllib.request.Request(url, headers={'User-Agent': 'mailto:ensdf_admin@example.com'})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode('utf-8'))
    return data.get('message', {}).get('items', [])


def title_has_a(title, a):
    tl = title.lower().replace('\u202f', ' ')
    if re.search(rf'\ba\s*=\s*{a}\b', tl):
        return True
    # handle ranges like A = 16-17 or A = 13–15
    for m in re.finditer(r'\ba\s*=\s*(\d+)\s*[\-–]\s*(\d+)\b', tl):
        lo = int(m.group(1)); hi = int(m.group(2))
        if lo <= a <= hi:
            return True
    return False


def is_bad_title(title):
    tl = title.lower()
    return any(p in tl for p in BAD_TITLE)


def score(item, off, a):
    title = title_of(item)
    jour = journal_of(item).lower()
    vol = str(item.get('volume', '') or '')
    pg = first_page(item.get('page', ''))
    yr = year_of(item)

    if is_bad_title(title):
        return -9999

    s = 0
    if off['kind'] == 'NDS' and 'nuclear data sheets' in jour:
        s += 30
    if off['kind'] == 'NPA' and 'nuclear physics a' in jour:
        s += 30

    if vol == off['vol'] or off['vol'] in vol:
        s += 40
    else:
        s -= 40

    if pg == off['page']:
        s += 45
    else:
        s -= 35

    if yr == off['year']:
        s += 20

    if title_has_a(title, a):
        s += 40

    return s


def author_str(item):
    a = item.get('author', [])
    if not a:
        return 'None'
    names = []
    for au in a:
        nm = f"{au.get('given','')} {au.get('family','')}".strip()
        if nm:
            names.append(nm)
    if not names:
        return 'None'
    if len(names) > 3:
        return names[0] + ' et al.'
    return ', '.join(names)


def main():
    with open(NNDC_PATH, 'r', encoding='utf-8') as f:
        nndc = json.load(f)
    with open(EXACT_PATH, 'r', encoding='utf-8') as f:
        exact = json.load(f)
    with open(VALID_PATH, 'r', encoding='utf-8') as f:
        valid = json.load(f)

    target = set(valid['summary'].get('volume_mismatch', []))
    target.update(valid['summary'].get('year_mismatch', []))
    target.update(valid['summary'].get('page_mismatch', []))

    report = {'target': sorted(target), 'updated': [], 'unchanged': []}

    for a in sorted(target):
        a_str = str(a)
        if a_str not in nndc:
            continue

        off = parse_cit(nndc[a_str])
        if off['kind'] not in ('NDS', 'NPA'):
            continue

        q = f"{off['journal']} {off['vol']} {off['page']} {off['year']}"
        try:
            items = query_items(q)
        except Exception as e:
            report['unchanged'].append({'a': a, 'reason': f'query_error {e}'})
            continue

        scored = sorted([(score(it, off, a), it) for it in items], key=lambda x: x[0], reverse=True)
        if not scored or scored[0][0] < 60:
            report['unchanged'].append({'a': a, 'reason': 'no_confident_candidate'})
            continue

        best = scored[0][1]
        best_doi = best.get('DOI', '')
        old_doi = exact.get(a_str, {}).get('doi', '')

        if not best_doi or best_doi == old_doi:
            report['unchanged'].append({'a': a, 'reason': 'same_or_empty'})
            continue

        exact[a_str] = {
            'a': a,
            'citation': f"{off['journal']} {off['vol']}, {off['page']} ({off['year']})",
            'doi': best_doi,
            'authors': author_str(best)
        }

        report['updated'].append({'a': a, 'old_doi': old_doi, 'new_doi': best_doi, 'title': title_of(best), 'score': scored[0][0]})

    with open(EXACT_PATH, 'w', encoding='utf-8') as f:
        json.dump(exact, f, indent=2)
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    print('targets:', len(report['target']))
    print('updated:', len(report['updated']))
    print('unchanged:', len(report['unchanged']))


if __name__ == '__main__':
    main()
