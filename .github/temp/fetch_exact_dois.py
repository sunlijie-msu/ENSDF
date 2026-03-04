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

    # Output list
    results = {}
    
    # Memoize to avoid duplicate fetches
    memo = {}

    for a in range(1, 300):
        a_str = str(a)
        if a_str not in data:
            results[a_str] = {
                'a': a,
                'citation': 'Not evaluated',
                'doi': '',
                'authors': ''
            }
            continue

        raw_cit = data[a_str]
        journal, vol, page, year = parse_cit(raw_cit)

        if journal == 'ENSDF':
            results[a_str] = {
                'a': a,
                'citation': 'Unpublished (Continuous ENSDF Update)',
                'doi': '',
                'authors': 'Internal NNDC/ENSDF Evaluation'
            }
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
            
        # We need to fetch from Crossref
        url = f"https://api.crossref.org/works?query.container-title={journal.replace(' ', '+')}&query.volume={vol}&query.page={page}&rows=3"
        req = urllib.request.Request(url, headers={'User-Agent': 'mailto:ensdf_admin@example.com'})
        
        found = False
        doi = ""
        authors_str = "None"
        
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    cdata = json.loads(resp.read())
                    items = cdata.get('message', {}).get('items', [])
                    if items:
                        best = items[0] # The most relevant one if query matches well
                        doi = best.get('DOI', '')
                        
                        authors_list = best.get('author', [])
                        if authors_list:
                            auth_names = []
                            for au in authors_list:
                                auth_names.append((au.get('given','') + " " + au.get('family','')).strip())
                            if len(auth_names) > 3:
                                authors_str = auth_names[0] + " et al."
                            else:
                                authors_str = ", ".join(auth_names)
                        found = True
                break
            except Exception as e:
                print(f"Error for A={a}: {e}")
                time.sleep(2)
        
        if not found:
            # Fallback to bibliographic query
            bib_query = f"{journal} {vol} {page} {year}"
            url2 = f"https://api.crossref.org/works?query.bibliographic={bib_query.replace(' ', '+')}&rows=3"
            req2 = urllib.request.Request(url2, headers={'User-Agent': 'mailto:ensdf_admin@example.com'})
            for attempt in range(2):
                try:
                    with urllib.request.urlopen(req2, timeout=10) as resp2:
                        cdata = json.loads(resp2.read())
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
        time.sleep(0.1) # Be nice to crossref API

    with open('.github/temp/exact_dois.json', 'w') as f:
        json.dump(results, f, indent=2)
        
if __name__ == '__main__':
    fetch_dois()
    print("Done!")
