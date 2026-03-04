import json

with open('.github/temp/exact_dois.json', 'r') as f:
    d = json.load(f)
with open('.github/temp/nndc_citations.json', 'r') as f:
    n = json.load(f)

print("In NNDC but not in exact_dois:")
print([k for k in n if k not in d])

print("Missing from 1 to 299 in exact_dois:")
print([k for k in range(1, 300) if str(k) not in d])
