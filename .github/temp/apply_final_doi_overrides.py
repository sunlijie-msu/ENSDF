import json

path = '.github/temp/exact_dois.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

overrides = {
    '223': {
        'doi': '10.1006/ndsh.2001.0016',
        'authors': 'E. Browne',
    },
    '260': {
        'doi': '10.1006/ndsh.1999.0021',
        'authors': 'C.W. Reich',
    },
    '264': {
        'doi': '10.1006/ndsh.1999.0021',
        'authors': 'C.W. Reich',
    },
}

for a, ov in overrides.items():
    if a in data:
        data[a]['doi'] = ov['doi']
        data[a]['authors'] = ov['authors']

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print('Applied overrides for:', ', '.join(sorted(overrides.keys(), key=int)))
