"""For each distinct comment text still lacking a target nucleus, report how many
distinct FULL lines (padding included) exist and what their padding counts are.

Usage: python padcheck.py FILE
"""
import re
import sys
from collections import Counter

RULES = [
    (r'(?<=[ $])(\(\|a,\|g\),\(\|a,n\))', '{+30}Si'),
    (r'(?<=[ $])(\(\|a,\|g\))', '{+30}Si'),
    (r'(?<=[ $])(\(\|a,n\))', '{+30}Si'),
    (r'(?<=[ $])(\(\|a,\|a\'\))', '{+34}S'),
    (r'(?<=[ $])(\(\|a,p\|g\))', '{+31}P'),
    (r'(?<=[ $])(\(n,\|g\),\(n,n\))', '{+33}S'),
    (r'(?<=[ $])(\(n,\|g\))', '{+33}S'),
    (r'(?<=[ $])(\(n,n\))', '{+33}S'),
    (r'(?<=[ $])(\(\{\+16\}O,\|a2p\|g\))', '{+24}Mg'),
    (r'(?<=[ $])(\(\{\+36\}S,\{\+34\}S\|g\))', '{+208}Pb'),
    (r'(?<=[ $])(\(p,p\),\(p,p\'\),\(pol p,p\'\))', '{+34}S'),
    (r'(?<=[ $])(\(p,p\'\|g\))', '{+34}S'),
    (r'(?<=[ $])(\(p,p\'\))', '{+34}S'),
    (r'(?<=[ $])(\(p,p\))', '{+34}S'),
    (r'(?<=[ $])(\(pol p,p\'\))', '{+34}S'),
    (r'(?<=[ $])(\(t,p\))', '{+32}S'),
    (r'(?<=[ $])(\(d,p\))', '{+33}S'),
    (r'(?<=[ $])(\(d,\{\+3\}He\))', '{+35}Cl'),
    (r'(?<=[ $])(\(pol \|g,\|g\'\))', '{+34}S'),
    (r'(?<=[ $])(\(\|g,\|g\'\))', '{+34}S'),
    (r'(?<=[ $])(\(e,e\'\))', '{+34}S'),
]


def fix(line):
    new = line
    for frag, prefix in RULES:
        new = re.sub(frag, lambda m, p=prefix: p + m.group(1), new)
    return new


raw = open(sys.argv[1], 'r', encoding='utf-8', errors='replace').read().replace('\r\n', '\n')

forms = {}
for ln in raw.split('\n'):
    base = ln.rstrip()
    if base and fix(base) != base:
        forms.setdefault(base, Counter())[len(ln) - len(base)] += 1

for base, c in sorted(forms.items(), key=lambda kv: -sum(kv[1].values())):
    print('N %-3d distinct_forms %-3d pads %s | %s'
          % (sum(c.values()), len(c), dict(c), base))
