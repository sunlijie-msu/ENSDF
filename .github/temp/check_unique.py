# -*- coding: utf-8 -*-
"""Check for duplicate old strings."""
import json

with open('.github/temp/replacements2.json', encoding='latin-1') as f:
    reps = json.load(f)

file_content = open('A34/Cl34/new/Cl34_33s_p_g.ens', encoding='latin-1').read()

for i, r in enumerate(reps):
    count = file_content.count(r['old'])
    if count != 1:
        print('WARNING: case %d G=%s appears %d times' % (i+1, r['g'], count))
    else:
        print('OK case %d (unique)' % (i+1))
