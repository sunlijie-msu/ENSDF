import urllib.request, json, time, re

with open(r'd:\X\ND\ENSDF\.github\docs\NDS_by_ENSDF_Mass_Chains.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

dois = []
for line in lines:
    if '|' in line and 'doi.org/' in line:
        m = re.search(r'doi\.org/([^ |]+)', line)
        if m:
            doi = m.group(1).strip()
            a_m = re.search(r'\|\s*(\d+)\s*\|', line)
            a = a_m.group(1) if a_m else '?'
            dois.append((a, doi, line))

print(f'Found {len(dois)} DOIs to check.')
with open(r'd:\X\ND\ENSDF\.github\temp\verify_report.txt', 'w', encoding='utf-8') as out:
    for a, doi, line in dois: # Check ALL
        try:
            url = 'https://api.crossref.org/works/' + doi
            req = urllib.request.Request(url, headers={'User-Agent': 'ENSDF-AI-Agent/1.0 (mailto:test@example.com)'})
            resp = urllib.request.urlopen(req)
            data = json.loads(resp.read().decode('utf-8'))
            title = data['message'].get('title', [''])[0]
            authors = []
            for author in data['message'].get('author', []):
                authors.append(f"{author.get('given', '')} {author.get('family', '')}".strip())
            out.write(f'A={a}, DOI={doi}\n -> Ref Title: {title}\n -> CrossRef Authors: {", ".join(authors)}\n -> File Line: {line.strip()}\n\n')
        except Exception as e:
            out.write(f'A={a}, DOI={doi}: ERROR {e}\n\n')
        time.sleep(0.1)
