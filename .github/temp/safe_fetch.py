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
    # Generic NDS/NP
    if "NDS" in cit: return 'Nuclear Data Sheets', cit, '', ''
    if "NP A" in cit or "NP " in cit: return 'Nuclear Physics A', cit, '', ''
    return None, None, None, None

def fetch_worker(a_str, raw_cit):
    try:
        res_parse = parse_cit(raw_cit)
        if not res_parse or res_parse[0] is None:
            return a_str, {'a': int(a_str), 'citation': raw_cit, 'doi': '', 'authors': 'Parse Error'}
            
        journal, vol, page, year = res_parse
        if journal == 'ENSDF':
            return a_str, {'a': int(a_str), 'citation': 'Continuous internal ENSDF', 'doi': '', 'authors': 'Internal NNDC/ENSDF Evaluation'}
            
        bib_query = f"{journal} {vol} {page} {year}".replace(' ', '+')
        url = f"https://api.crossref.org/works?query.bibliographic={bib_query}&rows=2"
        req = urllib.request.Request(url, headers={'User-Agent': 'mailto:ensdf_system_admin@example.com'})
        
        doi = ''
        authors_str = 'None'
        for _ in range(3):
            try:
                resp = urllib.request.urlopen(req, timeout=10)
                cdata = json.loads(resp.read())
                items = cdata.get('message', {}).get('items', [])
                if items:
                    best = items[0]
                    doi = best.get('DOI', '')
                    authors_list = best.get('author', [])
                    if authors_list:
                        auth_names = [(au.get('given','') + ' ' + au.get('family','')).strip() for au in authors_list][:4]
                        if len(auth_names) > 3:
                            authors_str = auth_names[0] + ' et al.'
                        else:
                            authors_str = ', '.join(auth_names)
                break
            except Exception as e:
                time.sleep(2)

        return a_str, {
            'a': int(a_str),
            'citation': f"{journal} {vol}, {page} ({year})" if page else f"{journal} - {vol}",
            'doi': doi,
            'authors': authors_str
        }
    except Exception as e:
        return a_str, {'a': int(a_str), 'citation': raw_cit, 'doi': '', 'authors': f'Error {e}'}

def main():
    with open('.github/temp/nndc_citations.json') as f:
        data = json.load(f)

    # Load existing to not refetch
    results = {}
    if os.path.exists('.github/temp/exact_dois.json'):
        with open('.github/temp/exact_dois.json') as f:
            try:
                results = json.load(f)
            except:
                pass

    for a in range(1, 300):
        if str(a) not in data:
            if str(a) not in results:
                results[str(a)] = {'a': a, 'citation': 'Not evaluated', 'doi': '', 'authors': ''}

    jobs = {k: v for k, v in data.items() if k not in results or not results[k].get('doi') or results[k].get('authors') == 'Parse Error'}
    print(f"Items to fetch: {len(jobs)}")
    
    # Sequential fetch with save to avoid getting banned or losing context
    for i, (k, v) in enumerate(jobs.items()):
        
        _, res = fetch_worker(k, v)
        results[k] = res
        
        if i % 10 == 0:
            with open('.github/temp/exact_dois.json', 'w') as f:
                json.dump(results, f, indent=2)
            print(f"Done {i}/{len(jobs)}")
            time.sleep(1) # Rate limit protection

    with open('.github/temp/exact_dois.json', 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == '__main__':
    main()
