"""Quick reachability test for the 7 newly added DOIs."""
import urllib.request
import time

new_dois = [
    (76,  'https://doi.org/10.1016/j.nds.2024.02.002'),
    (77,  'https://doi.org/10.1016/j.nds.2012.05.001'),
    (101, 'https://doi.org/10.1006/ndsh.1998.0001'),
    (108, 'https://doi.org/10.1006/ndsh.2000.0017'),
    (117, 'https://doi.org/10.1006/ndsh.2002.0007'),
    (165, 'https://doi.org/10.1016/j.nds.2006.05.002'),
    (224, 'https://doi.org/10.1016/j.nds.2015.11.003'),
]

print('Reachability test for 7 new DOIs:')
all_pass = True
for a, doi in new_dois:
    try:
        req = urllib.request.Request(doi, headers={'User-Agent': 'mailto:admin@example.com'})
        with urllib.request.urlopen(req, timeout=15) as r:
            code = r.getcode()
            print(f'  A={a:4d}: PASS (HTTP {code}) {doi}')
    except urllib.error.HTTPError as e:
        print(f'  A={a:4d}: HTTP ERROR {e.code} {doi}')
        all_pass = False
    except Exception as e:
        print(f'  A={a:4d}: FAIL ({type(e).__name__}) {doi}')
        all_pass = False
    time.sleep(0.3)

print()
print('Result:', 'ALL PASS' if all_pass else 'FAILURES DETECTED')
