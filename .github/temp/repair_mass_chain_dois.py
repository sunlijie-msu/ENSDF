import json
import re
import time
import urllib.request
from urllib.parse import quote_plus

NNDC_PATH = '.github/temp/nndc_citations.json'
EXACT_PATH = '.github/temp/exact_dois.json'
OUT_PATH = '.github/temp/exact_dois.json'
REPORT_PATH = '.github/temp/repair_mass_chain_dois_report.json'


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


def query_crossref_items(query, rows=12):
    url = f"https://api.crossref.org/works?query.bibliographic={quote_plus(query)}&rows={rows}&select=DOI,title,author,container-title,volume,page,published-print,published-online,issued"
    req = urllib.request.Request(url, headers={'User-Agent': 'mailto:ensdf_admin@example.com'})
    with urllib.request.urlopen(req, timeout=25) as r:
        data = json.loads(r.read().decode('utf-8'))
    return data.get('message', {}).get('items', [])


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


def score_item(item, off, a):
    title = item_title(item)
    title_l = title.lower()
    journal = item_journal(item).lower()
    volume = str(item.get('volume', '') or '')
    page = first_page(item.get('page', ''))
    year = item_year(item)

    if 'symbols and abbreviations' in title_l:
        return -9999
    if 'update' in title_l:
        return -9999

    score = 0

    if off['kind'] == 'NDS':
        if 'nuclear data sheets' in journal:
            score += 30
        if f'a = {a}' in title_l or f'a={a}' in title_l:
            score += 35
    elif off['kind'] == 'NPA':
        if 'nuclear physics a' in journal:
            score += 30
        if f'a = {a}' in title_l or f'a={a}' in title_l:
            score += 15

    if off['vol'] and volume == off['vol']:
        score += 40
    elif off['vol'] and off['vol'] in volume:
        score += 15

    if off['page'] and page == off['page']:
        score += 35

    if off['year'] and year == off['year']:
        score += 20

    # penalize clear mismatch
    if off['vol'] and volume and volume != off['vol'] and off['vol'] not in volume:
        score -= 35
    if off['year'] and year and year != off['year']:
        score -= 15

    return score


def authors_str(item):
    authors = item.get('author', [])
    if not authors:
        return 'None'
    names = []
    for au in authors:
        name = f"{au.get('given', '')} {au.get('family', '')}".strip()
        if name:
            names.append(name)
    if not names:
        return 'None'
    if len(names) > 3:
        return names[0] + ' et al.'
    return ', '.join(names)


def select_best(off, a):
    query = f"{off['journal']} {off['vol']} {off['page']} {off['year']}"
    items = query_crossref_items(query, rows=15)

    scored = []
    for item in items:
        scored.append((score_item(item, off, a), item))

    scored.sort(key=lambda x: x[0], reverse=True)
    if not scored or scored[0][0] < 40:
        return None, scored[:3]

    return scored[0][1], scored[:5]


def is_suspect(item, off):
    doi = (item.get('doi') or '').strip()
    if off['kind'] in ('NDS', 'NPA') and not doi:
        return True

    title = (item.get('title_check') or '').lower()
    if 'symbols and abbreviations' in title or 'update' in title:
        return True

    if item.get('vol_check') and off['vol'] and item['vol_check'] != off['vol']:
        return True

    if item.get('year_check') and off['year'] and item['year_check'] != off['year']:
        return True

    return False


def crossref_by_doi(doi):
    if not doi:
        return {'title': '', 'vol': '', 'year': ''}
    url = f"https://api.crossref.org/works/{doi}"
    req = urllib.request.Request(url, headers={'User-Agent': 'mailto:ensdf_admin@example.com'})
    with urllib.request.urlopen(req, timeout=20) as r:
        msg = json.loads(r.read().decode('utf-8')).get('message', {})
    return {
        'title': item_title(msg),
        'vol': str(msg.get('volume', '') or ''),
        'year': item_year(msg),
    }


def main():
    with open(NNDC_PATH, 'r', encoding='utf-8') as f:
        nndc = json.load(f)
    with open(EXACT_PATH, 'r', encoding='utf-8') as f:
        exact = json.load(f)

    report = {
        'checked': 0,
        'suspect': [],
        'repaired': [],
        'unresolved': []
    }

    for a_str in sorted(nndc.keys(), key=lambda x: int(x)):
        a = int(a_str)
        off = parse_cit(nndc[a_str])

        if off['kind'] == 'ENSDF':
            continue
        if off['kind'] == 'UNKNOWN':
            report['unresolved'].append({'a': a, 'reason': 'unknown_official_format', 'official': nndc[a_str]})
            continue

        cur = exact.get(a_str, {'a': a, 'citation': '', 'doi': '', 'authors': ''})
        doi = (cur.get('doi') or '').strip()

        vol_check = ''
        year_check = ''
        title_check = ''
        if doi:
            try:
                cr = crossref_by_doi(doi)
                vol_check = cr['vol']
                year_check = cr['year']
                title_check = cr['title']
            except Exception:
                pass

        probe = {
            'doi': doi,
            'vol_check': vol_check,
            'year_check': year_check,
            'title_check': title_check,
        }

        report['checked'] += 1

        if not is_suspect(probe, off):
            continue

        report['suspect'].append({'a': a, 'old_doi': doi, 'old_title': title_check})

        try:
            best, scored = select_best(off, a)
        except Exception as e:
            report['unresolved'].append({'a': a, 'reason': f'crossref_query_error: {e}'})
            time.sleep(0.5)
            continue

        if not best:
            report['unresolved'].append({'a': a, 'reason': 'no_confident_match'})
            time.sleep(0.5)
            continue

        new_doi = best.get('DOI', '')
        new_authors = authors_str(best)

        exact[a_str] = {
            'a': a,
            'citation': f"{off['journal']} {off['vol']}, {off['page']} ({off['year']})",
            'doi': new_doi,
            'authors': new_authors,
        }

        report['repaired'].append({
            'a': a,
            'old_doi': doi,
            'new_doi': new_doi,
            'new_title': item_title(best),
            'score': score_item(best, off, a),
        })

        if len(report['repaired']) % 5 == 0:
            with open(OUT_PATH, 'w', encoding='utf-8') as f:
                json.dump(exact, f, indent=2)

        time.sleep(0.4)

    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(exact, f, indent=2)

    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    print('checked:', report['checked'])
    print('suspect:', len(report['suspect']))
    print('repaired:', len(report['repaired']))
    print('unresolved:', len(report['unresolved']))


if __name__ == '__main__':
    main()
