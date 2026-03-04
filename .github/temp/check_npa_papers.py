import urllib.request, json
dois = [
    '10.1016/j.nuclphysa.2012.01.010',
    '10.1016/j.nuclphysa.2010.08.012',
]
for doi in dois:
    url = f'https://api.crossref.org/works/{doi}'
    req = urllib.request.Request(url, headers={'User-Agent': 'a@b.com'})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            item = json.loads(r.read()).get('message', {})
            title = item.get('title', ['?'])[0]
            vol = item.get('volume', '?')
            page = item.get('page', '?')
            try:
                year = item.get('published-print', {}).get('date-parts', [[0]])[0][0]
            except:
                year = 0
            authors = [(au.get('given', '') + ' ' + au.get('family', '')).strip() for au in item.get('author', [])]
            auth_str = ', '.join(authors)
            abstract = item.get('abstract', '')[:200] if item.get('abstract') else ''
            print(f'DOI: {doi}')
            print(f'  Title: {title}')
            print(f'  Vol: {vol} | Page: {page} | Year: {year}')
            print(f'  Authors: {auth_str}')
            print()
    except Exception as e:
        print(f'Error {doi}: {e}')
