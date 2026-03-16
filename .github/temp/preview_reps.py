# -*- coding: utf-8 -*-
import json
with open('.github/temp/replacements.json', encoding='latin-1') as f:
    reps = json.load(f)
# Print a few samples
for idx in [0, 7, 13, 14, 22]:
    r = reps[idx]
    print('=== Case index %d G=%s cG=%s ===' % (idx, r['g'], r['cg']))
    print('OLD:')
    for line in r['old'].split('\n'):
        print('  |' + line + '|')
    print('NEW:')
    for line in r['new'].split('\n'):
        print('  |' + line + '|')
    print()
