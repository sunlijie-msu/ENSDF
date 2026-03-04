import urllib.request
import json
import re
import os
import time

def main():
    url = 'https://www.nndc.bnl.gov/ensdf/EvaluationIndexServlet'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req).read().decode('utf-8')
    data = json.loads(response)
    
    mass_data = {}
    for item in data:
        if item.get('type') == 'MASS':
            a = item['a']
            cit = item['citation']
            mass_data[a] = cit
            
    with open('.github/temp/nndc_citations.json', 'w') as f:
        json.dump(mass_data, f, indent=2)

    print(f"Saved {len(mass_data)} mass citations.")
    
if __name__ == '__main__':
    main()
