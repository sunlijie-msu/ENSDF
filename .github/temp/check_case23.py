# -*- coding: utf-8 -*-
"""Check case 23 specifically."""
import json

with open('.github/temp/replacements2.json', encoding='latin-1') as f:
    reps = json.load(f)

file_content = open('A34/Cl34/new/Cl34_33s_p_g.ens', encoding='latin-1').read()

r = reps[22]  # Case 23 (0-indexed)
print('Case 23 G=%s cG=%s' % (r['g'], r['cg']))
count = file_content.count(r['old'])
print('Count:', count)
print('OLD repr:', repr(r['old']))
