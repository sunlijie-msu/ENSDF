import json
import urllib.request
from urllib.parse import quote_plus

queries = {
    223: "Nuclear Data Sheets 93 846 2001",
    260: "Nuclear Data Sheets 87 301 1999",
    264: "Nuclear Data Sheets 87 309 1999",
    237: "Nuclear Data Sheets 107 3323 2006",
    242: "Nuclear Data Sheets 186 261 2022",
    24: "Nuclear Data Sheets 186 2 2022",
    65: "Nuclear Data Sheets 202 59 2025",
}

for a, q in queries.items():
    url = f"https://api.crossref.org/works?query.bibliographic={quote_plus(q)}&rows=12&select=DOI,title,container-title,volume,page,published-print,issued"
    req = urllib.request.Request(url, headers={'User-Agent':'mailto:ensdf_admin@example.com'})
    with urllib.request.urlopen(req, timeout=30) as r:
        items = json.loads(r.read().decode('utf-8')).get('message',{}).get('items',[])

    print(f"\n=== A={a} | query={q} ===")
    for i, it in enumerate(items[:10], start=1):
        title = (it.get('title') or [''])[0]
        jour = (it.get('container-title') or [''])[0]
        vol = str(it.get('volume',''))
        page = str(it.get('page',''))
        doi = it.get('DOI','')
        year = ''
        for key in ('published-print','issued'):
            dp = (it.get(key) or {}).get('date-parts',[])
            if dp and dp[0]:
                year = str(dp[0][0]); break
        print(f"{i:02d}. DOI={doi} | {jour} | v{vol} p{page} y{year} | {title}")
