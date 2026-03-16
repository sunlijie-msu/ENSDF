# -*- coding: utf-8 -*-
import json
lines = open('A34/Cl34/new/Cl34_33s_p_g.ens', encoding='latin-1').read()
with open('.github/temp/replacements.json', encoding='latin-1') as f:
    replacements = json.load(f)
for i, r in enumerate(replacements):
    found = r['old'] in lines
    status = 'OK' if found else 'MISSING'
    if not found:
        print('%s case %d G=%s cG=%s' % (status, i+1, r['g'], r['cg']))
        print('OLD repr:', repr(r['old']))
        print()
print('Done.')
