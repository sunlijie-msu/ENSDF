# -*- coding: utf-8 -*-
"""Print all replacement pairs for multi_replace_string_in_file call."""
import json

with open('.github/temp/replacements2.json', encoding='latin-1') as f:
    reps = json.load(f)

for i, r in enumerate(reps):
    print('=== REP %02d ===' % i)
    print('OLD:')
    print(repr(r['old']))
    print('NEW:')
    print(repr(r['new']))
    print()
