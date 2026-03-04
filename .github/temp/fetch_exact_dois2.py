import urllib.request
import urllib.parse
import json
import re
import os
import time

def parse_cit(cit):
    if cit.strip() == 'ENSDF': return 'ENSDF', '', '', ''
    m = re.match(r'NDS\s+(\d+)\s*[,]*\s*(\d+)\s*[,\(]?\s*(\d{4})\)?', cit)
    if m: return 'Nuclear Data Sheets', m.group(1), m.group(2), m.group(3)
    m = re.match(r'NP\s*(?:A)?\s*(\d+)\s*[,]*\s*(\d+)\s*\((\d{4})\)', cit)
    if m: return 'Nuclear Physics A', m.group(1), m.group(2), m.group(3)
    return None, None, None, None

def fetch_dois():
    with open('.github/temp/nndc_citations.json') as f:
        data = json.load(f)

    results = {}
    memo = {}

    for a in range(1, 300):
        a_str = str(a)
        if a_str not in data:
            results[a_str] = {'a': a, 'citation': 'Not evaluated', 'doi': '', 'authors': ''}
            continue

        raw_cit = data[a_str]
        res_parse = parse_cit(raw_cit)
        
        # If parse failed, mark as unparseable
        if not res_parse or res_parse[0] is None:
            results[a_str] = {'a': a, 'citation': raw_cit, 'doi': '', 'authors': 'Parse Error'}
            continue
            
        journal, vol, page, year = res_parse

        if journal == 'ENSDF':
            results[a_str] = {'a': a, 'citation': 'Continuous internal ENSDF', 'doi': '', 'authors': 'Internal'}
            continue
            
        key = f"{journal}_{vol}_{page}"
        if key in memo:
            results[a_str] = {
                'a': a,
                'citation': f"{journal} {vol}, {page} ({year})",
                'doi': memo[key]['doi'],
                'authors': memo[key]['authors']
            }
            continue
            
        bib_query = f"{journal} {vol} {page} {year}".replace(' ', '+')
        url = f"https://api.crossref.org/works?query.bibliographic={bib_query}&rows=3"
        req = urllib.request.Request(url, headers={'User-Agent': 'mailto:ensdf_admin@example.com'})
        
        doi = ""
        authors_str = "None"
        found = False
        
        for attempt in range(3):
            try:
                resp = urllib.request.urlopen(req, timeout=10)
                cdata = json.loads(resp.read())
                items = cdata.get('message', {}).get('items', [])
                if items:
                    best = items[0]
                    doi = best.get('DOI', '')
                    authors_list = best.get('author', [])
                    if authors_list:
                        auth_names = [(au.get('given','') + ' ' + au.get('family','')).strip() for au in authors_list]
                        if len(auth_names) > 3:
                            authors_str = auth_names[0] + " et al."
                        else:
                            authors_str = ", ".join(auth_names)
                    found = True
                break
            except Exception as e:
                time.sleep(1)

        memo[key] = {'doi': doi, 'authors': authors_str}
        results[a_str] = {
            'a': a,
            'citation': f"{journal} {vol}, {page} ({year})",
            'doi': doi,
            'authors': authors_str
        }
        
        print(f"A={a} -> DOI: {doi}")
        with open('.github/temp/exact_dois.json', 'w') as f:
            json.dump(results, f, indent=2)

if __name__ == '__main__':
    fetch_dois()
    print("Done!")
