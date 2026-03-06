import json

with open('d:/X/ND/ENSDF/.github/temp/ka39_replace_pairs.json') as p:
    pairs = json.load(p)

with open('d:/X/ND/ENSDF/A34/Cl34/new/Cl34_33s_p_g.ens') as g:
    content = g.read()

ok = 0
fail = []
for pair in pairs:
    c = content.count(pair['old'])
    if c == 1:
        ok += 1
    else:
        fail.append((pair['ep'], c))

print('Total pairs:', len(pairs))
print('OK:', ok)
print('FAIL:', fail)
