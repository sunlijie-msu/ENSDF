import json
import re
import time
import urllib.request
from urllib.parse import quote_plus

NNDC_PATH = '.github/temp/nndc_citations.json'
EXACT_PATH = '.github/temp/exact_dois.json'
VALID_PATH = '.github/temp/doi_metadata_validation.json'
REPORT_PATH = '.github/temp/repair_frontmatter_dois_report.json'

BAD_TITLE_PATTERNS = [
    'symbols and abbreviations',
    'editorial board',
    'front cover',
    'back cover',
    'contents',
    'index',
]

BAD_PAGE_TOKENS = {'ifc', 'ibc', 'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii'}


def norm(text):
    return re.sub(r'\s+', ' ', (text or '').strip())


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


def first_page(page):
    if not page:
        return ''
    return str(page).split('-')[0].strip()


def item_year(item):
    for key in ('published-print', 'published-online', 'issued'):
        val = item.get(key, {})
        dp = val.get('date-parts', []) if isinstance(val, dict) else []
        if dp and dp[0]:
            return str(dp[0][0])
    return ''


def item_title(item):
    t = item.get('title', [])
    return t[0] if t else ''


def item_journal(item):
    c = item.get('container-title', [])
    return c[0] if c else ''


def query_items(query):
    url = f"https://api.crossref.org/works?query.bibliographic={quote_plus(query)}&rows=25&select=DOI,title,author,container-title,volume,page,published-print,published-online,issued"
    req = urllib.request.Request(url, headers={'User-Agent': 'mailto:ensdf_admin@example.com'})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode('utf-8'))
    return data.get('message', {}).get('items', [])


def bad_title(title):
    tl = title.lower()
    return any(p in tl for p in BAD_TITLE_PATTERNS)


def bad_page_token(pg):
    return pg.lower() in BAD_PAGE_TOKENS


def score(item, off, a):
    title = item_title(item)
    title_l = title.lower()
    journal = item_journal(item).lower()
    vol = str(item.get('volume', '') or '')
    pg = first_page(item.get('page', ''))
    yr = item_year(item)

    if bad_title(title):
        return -9999

    if off['page'].isdigit() and pg and bad_page_token(pg):
        return -9999

    s = 0

    if off['kind'] == 'NDS' and 'nuclear data sheets' in journal:
        s += 30
    if off['kind'] == 'NPA' and 'nuclear physics a' in journal:
        s += 30

    if vol == off['vol']:
        s += 40
    elif off['vol'] in vol:
        s += 25

    if pg == off['page']:
        s += 50
    elif pg:
        s -= 20

    if yr == off['year']:
        s += 20

    if f'a = {a}' in title_l or f'a={a}' in title_l:
        s += 25

    # useful for classic light nuclei papers
    if off['kind'] == 'NPA' and ('energy levels of light nuclei' in title_l or 'levels of light nuclei' in title_l):
        s += 20

    return s


def authors_str(item):
    aa = item.get('author', [])
    if not aa:
        return 'None'
    names = []
    for au in aa:
        nm = f"{au.get('given', '')} {au.get('family', '')}".strip()
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

    target = set(valid.get('summary', {}).get('page_mismatch', []))
    target.update(valid.get('summary', {}).get('volume_mismatch', []))

    report = {'targets': sorted(target), 'fixed': [], 'unresolved': []}

    for a in sorted(target):
        a_str = str(a)
        if a_str not in nndc:
            continue

        off = parse_cit(nndc[a_str])
        if off['kind'] not in ('NDS', 'NPA'):
            continue

        old = exact.get(a_str, {'doi': '', 'authors': ''})
        old_doi = old.get('doi', '')

        query = f"{off['journal']} {off['vol']} {off['page']} {off['year']}"
        try:
            items = query_items(query)
        except Exception as e:
            report['unresolved'].append({'a': a, 'reason': f'query_error: {e}'})
            continue

        scored = sorted(((score(it, off, a), it) for it in items), key=lambda x: x[0], reverse=True)
        if not scored or scored[0][0] < 50:
            report['unresolved'].append({'a': a, 'reason': 'no_strong_candidate'})
            continue

        best = scored[0][1]
        new_doi = best.get('DOI', '')
        if not new_doi:
            report['unresolved'].append({'a': a, 'reason': 'empty_doi'})
            continue

        if new_doi != old_doi:
            exact[a_str] = {
                'a': a,
                'citation': f"{off['journal']} {off['vol']}, {off['page']} ({off['year']})",
                'doi': new_doi,
                'authors': authors_str(best),
            }
            report['fixed'].append({
                'a': a,
                'old_doi': old_doi,
                'new_doi': new_doi,
                'title': item_title(best),
                'score': scored[0][0],
            })

        time.sleep(0.25)

    with open(EXACT_PATH, 'w', encoding='utf-8') as f:
        json.dump(exact, f, indent=2)

    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    print('targets:', len(report['targets']))
    print('fixed:', len(report['fixed']))
    print('unresolved:', len(report['unresolved']))


if __name__ == '__main__':
    main()
