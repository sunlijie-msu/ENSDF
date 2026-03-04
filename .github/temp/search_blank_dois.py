"""Search for most recent NDS/NSDD evaluations for blank-DOI entries."""
import urllib.request
import json
import time

def get_metadata(doi):
    url = f'https://api.crossref.org/works/{doi}'
    req = urllib.request.Request(url, headers={'User-Agent': 'mailto:admin@example.com'})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
            item = data.get('message', {})
            try:
                year = item.get('published-print', {}).get('date-parts', [[0]])[0][0]
            except:
                year = 0
            title = item.get('title', ['?'])[0]
            vol = item.get('volume', '?')
            page = item.get('page', '?')
            authors_list = item.get('author', [])
            authors = [(au.get('given', '') + ' ' + au.get('family', '')).strip() for au in authors_list]
            if len(authors) > 3:
                auth_str = ', '.join(authors[:3]) + ' et al.'
            else:
                auth_str = ', '.join(authors)
            return {'year': year, 'vol': vol, 'page': page, 'title': title, 'authors': auth_str}
    except Exception as e:
        return {'error': str(e)}

def search_mass(a, query, from_year=None):
    url = f'https://api.crossref.org/works?query.title={query}&select=DOI,title,author,volume,published-print,page&rows=15'
    if from_year:
        url += f'&filter=from-pub-date:{from_year}'
    req = urllib.request.Request(url, headers={'User-Agent': 'mailto:admin@example.com'})
    results = []
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
            for item in data.get('message', {}).get('items', []):
                title = item.get('title', [''])[0]
                tl = title.lower()
                # Filter: must reference this mass number
                if str(a) not in title:
                    continue
                if any(x in tl for x in ['erratum', 'symbols', 'abbreviation', 'update']):
                    continue
                # Must say A={a} or A = {a}
                if f'A={a}' not in title and f'A = {a}' not in title and f'A={a},' not in title:
                    continue
                try:
                    year = item.get('published-print', {}).get('date-parts', [[0]])[0][0]
                except:
                    year = 0
                vol = item.get('volume', '?')
                page = item.get('page', '?')
                doi = item.get('DOI', '')
                authors_list = item.get('author', [])
                authors = [(au.get('given', '') + ' ' + au.get('family', '')).strip() for au in authors_list]
                if len(authors) > 3:
                    auth_str = ', '.join(authors[:3]) + ' et al.'
                else:
                    auth_str = ', '.join(authors)
                results.append((year, vol, page, doi, auth_str, title[:80]))
    except Exception as e:
        results.append((0, '?', '?', '', f'ERROR: {e}', ''))
    results.sort(reverse=True)
    return results[:3]

# First, verify the user's A=76 DOI
print('=== A=76 (user-provided DOI verification) ===')
meta = get_metadata('10.1016/j.nds.2024.02.002')
print(f'  Title: {meta.get("title", "?")}')
print(f'  Vol: {meta.get("vol")} | Page: {meta.get("page")} | Year: {meta.get("year")}')
print(f'  Authors: {meta.get("authors")}')
print()
time.sleep(0.3)

# Search for others
searches = {
    2: ('energy+levels+light+nuclei+A%3D2', None),
    77: ('Nuclear+Data+Sheets+A%3D77', None),
    101: ('Nuclear+Data+Sheets+A%3D101', None),
    108: ('Nuclear+Data+Sheets+A%3D108', None),
    117: ('Nuclear+Data+Sheets+A%3D117', None),
}

for a, (query, from_year) in searches.items():
    print(f'=== A={a} ===')
    results = search_mass(a, query, from_year)
    if results:
        for r in results:
            print(f'  year={r[0]} vol={r[1]} page={r[2]} doi={r[3]}')
            print(f'    title={r[5]}')
            print(f'    authors={r[4]}')
    else:
        print('  NO RESULTS FOUND')
    time.sleep(0.4)

# Also try A=2 with an alternate query
print()
print('=== A=2 alternate search (NPA) ===')
url = 'https://api.crossref.org/works?query.title=energy+levels+light+nuclei&select=DOI,title,author,volume,published-print,page&rows=20'
req = urllib.request.Request(url, headers={'User-Agent': 'mailto:admin@example.com'})
try:
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
        for item in data.get('message', {}).get('items', []):
            title = item.get('title', [''])[0]
            tl = title.lower()
            if 'a = 2' in tl or 'a=2' in tl or '1, 2' in title or '1,2' in title:
                try:
                    year = item.get('published-print', {}).get('date-parts', [[0]])[0][0]
                except:
                    year = 0
                print(f'  year={year} doi={item.get("DOI","")} title={title[:80]}')
except Exception as e:
    print(f'Error: {e}')
