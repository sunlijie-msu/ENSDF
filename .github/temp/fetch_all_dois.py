import urllib.request
import json
import re
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_A(a):
    results = {}
    url = f"https://api.crossref.org/works?query.title=Nuclear+Data+Sheets+for+A%3D{a}&select=DOI,title,author,volume,published-print,page&rows=15"
    req = urllib.request.Request(url, headers={'User-Agent': 'mailto:ensdf_admin@example.com'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read())
                items = data.get('message', {}).get('items', [])
                
                valid_items = []
                for item in items:
                    titles = item.get('title', [])
                    if not titles: continue
                    t = titles[0].lower()
                    if f"a = {a}" in t or f"a={a}" in t:
                        if "update" not in t and "symbols" not in t and "abbreviations" not in t:
                            valid_items.append(item)
                
                if valid_items:
                    def get_year(itm):
                        try:
                            # Prefer print year, fallback to any available year
                            return itm.get('published-print', {}).get('date-parts', [[0]])[0][0]
                        except:
                            return 0
                    
                    valid_items.sort(key=get_year, reverse=True)
                    best = valid_items[0]
                    
                    authors_list = best.get('author', [])
                    auth_str = "None"
                    if authors_list:
                        authors = []
                        for au in authors_list:
                            name = au.get('given','') + " " + au.get('family','')
                            authors.append(name.strip())
                        if len(authors) > 3:
                            auth_str = authors[0] + " et al."
                        else:
                            auth_str = ", ".join(authors)
                    
                    vol = best.get('volume', '?')
                    page = best.get('page', '?')
                    year = get_year(best)
                    doi = best.get('DOI', '?')
                    
                    return (a, vol, page, year, doi, auth_str, "NDS")
        except Exception as e:
            time.sleep(2)
            continue
            
    # Try Nuclear Physics A for light masses if not found
    if a < 25:
        url2 = f"https://api.crossref.org/works?query.title=Energy+levels+of+light+nuclei+A%3D{a}&select=DOI,title,author,volume,published-print,page&rows=10"
        req2 = urllib.request.Request(url2, headers={'User-Agent': 'mailto:ensdf_admin@example.com'})
        for attempt in range(2):
            try:
                with urllib.request.urlopen(req2, timeout=10) as response:
                    data = json.loads(response.read())
                    items = data.get('message', {}).get('items', [])
                    valid_items = []
                    for item in items:
                        titles = item.get('title', [])
                        if not titles: continue
                        t = titles[0].lower()
                        if f"a = {a}" in t or f"a={a}" in t or ("a =" in t and str(a) in t):
                            if "update" not in t:
                                valid_items.append(item)
                    if valid_items:
                        def get_year(itm):
                            try:
                                return itm.get('published-print', {}).get('date-parts', [[0]])[0][0]
                            except:
                                return 0
                        valid_items.sort(key=get_year, reverse=True)
                        best = valid_items[0]
                        authors_list = best.get('author', [])
                        auth_str = "None"
                        if authors_list:
                            authors = [au.get('given','') + " " + au.get('family','') for au in authors_list]
                            if len(authors) > 3:
                                auth_str = authors[0].strip() + " et al."
                            else:
                                auth_str = ", ".join(a.strip() for a in authors)
                        return (a, best.get('volume', '?'), best.get('page', '?'), get_year(best), best.get('DOI', '?'), auth_str, "NPA")
            except:
                time.sleep(1)
                
    return (a, "NOT FOUND", "", 0, "", "", "")

# Load existing
out_file = '.github/temp/mass_dois.json'
results = {}
if os.path.exists(out_file):
    try:
        with open(out_file, 'r') as f:
            js = json.load(f)
            results = {int(k): v for k, v in js.items()}
    except:
        pass

missing = [a for a in range(1, 300) if a not in results or results[a][1] == 'ERROR']

print(f"Fetching {len(missing)} records...")
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {executor.submit(fetch_A, a): a for a in missing}
    for i, future in enumerate(as_completed(futures)):
        r = future.result()
        a = r[0]
        results[a] = list(r[1:])
        if i % 10 == 0:
            with open(out_file, 'w') as f:
                json.dump(results, f)
            print(f"Processed {i+1}/{len(missing)}...")

with open(out_file, 'w') as f:
    json.dump(results, f)
print("Finished fetching!")
