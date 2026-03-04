import json
import os

in_file = '.github/temp/exact_dois.json'
out_file = 'ENSDF_Mass_Chain_Evaluations.md'

with open(in_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

lines = [
    '# ENSDF Mass Chain Evaluations',
    '',
    '| Mass Number | Citation (Volume, Page, Year) | DOI | Authors |',
    '|---|---|---|---|'
]

for a in range(1, 300):
    a_str = str(a)
    if a_str not in data or data[a_str]['citation'] == 'Not evaluated':
        lines.append(f"| {a} | Not evaluated |  |  |")
        continue
    
    item = data[a_str]
    cit = item['citation']
    doi = item['doi']
    authors = item['authors']
    
    doi_link = ''
    if doi:
        doi_link = f"[{doi}](https://doi.org/{doi})"
    
    lines.append(f"| {a} | {cit} | {doi_link} | {authors} |")

with open(out_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f"Created {out_file} with {len(lines)-4} rows.")
