"""Search Crossref for new 2026 NDS papers: NDS 209 vol."""
import urllib.request, json, time

def crossref_search(query):
    url = f"https://api.crossref.org/works?query={urllib.parse.quote(query)}&rows=3&filter=container-title:Nuclear%20Data%20Sheets"
    import urllib.parse
    req = urllib.request.Request(url, headers={'User-Agent': 'ENSDF-check/1.0 (mailto:test@test.com)'})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def crossref_volume_page(vol, page):
    """Find NDS paper by volume and first page."""
    import urllib.parse
    url = (f"https://api.crossref.org/works"
           f"?query.bibliographic=Nuclear+Data+Sheets+{vol}"
           f"&rows=20"
           f"&filter=container-title:Nuclear+Data+Sheets,volume:{vol}")
    req = urllib.request.Request(url, headers={'User-Agent': 'ENSDF-check/1.0 (mailto:test@test.com)'})
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
    for item in data['message']['items']:
        pages = item.get('page', '')
        if str(page) in pages.split('-')[0]:
            return item
    return None

import urllib.parse

# Search for NDS 209, 409 (2026) - A=216
print("=== Searching NDS 209, 409 (2026) - A=216 ===")
result = crossref_volume_page(209, 409)
if result:
    doi = result.get('DOI', '')
    title = result.get('title', [''])[0]
    authors = result.get('author', [])
    author_str = ', '.join(f"{a.get('given','').strip()} {a.get('family','').strip()}".strip() for a in authors)
    print(f"  DOI: {doi}")
    print(f"  Title: {title}")
    print(f"  Authors: {author_str}")
    print(f"  Page: {result.get('page', '')}")
else:
    print("  NOT FOUND via volume/page filter")

time.sleep(1)

# Search for NDS 209, 499 (2026) - A=261, 265
print()
print("=== Searching NDS 209, 499 (2026) - A=261, 265 ===")
result2 = crossref_volume_page(209, 499)
if result2:
    doi = result2.get('DOI', '')
    title = result2.get('title', [''])[0]
    authors = result2.get('author', [])
    author_str = ', '.join(f"{a.get('given','').strip()} {a.get('family','').strip()}".strip() for a in authors)
    print(f"  DOI: {doi}")
    print(f"  Title: {title}")
    print(f"  Authors: {author_str}")
    print(f"  Page: {result2.get('page', '')}")
else:
    print("  NOT FOUND via volume/page filter")
    # Fallback: search by title
    time.sleep(1)
    url = "https://api.crossref.org/works?query=Nuclear+Data+Sheets+A%3D261&rows=5&filter=container-title:Nuclear+Data+Sheets"
    req = urllib.request.Request(url, headers={'User-Agent': 'ENSDF-check/1.0 (mailto:test@test.com)'})
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
    for item in data['message']['items']:
        v = item.get('volume','')
        p = item.get('page','')
        y = item.get('published',{}).get('date-parts',[[0]])[0][0]
        print(f"  Candidate: vol={v} page={p} year={y} doi={item.get('DOI','')} title={item.get('title',[''])[0][:60]}")
