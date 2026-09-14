"""Same as gen_pairs.py but also reports how many times each OLD text occurs in the
file, so pairs needing extra context can be identified.

Usage: python gen_pairs2.py FILE > pairs.txt
"""
import re
import sys

path = sys.argv[1]

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

raw = open(path, 'r', encoding='utf-8', errors='replace').read()
lines = raw.split('\n')
pairs = []
for i, ln in enumerate(lines, 1):
    orig = ln.rstrip()
    new = orig
    for frag, prefix in RULES:
        new = re.sub(frag, lambda m, p=prefix: p + m.group(1), new)
    if new != orig:
        pairs.append((i, orig, new, raw.count(orig)))

for i, a, b, c in pairs:
    print('LINE %d OCC %d' % (i, c))
    print('OLD %s' % a)
    print('NEW %s' % b)
print('PAIRS: %d   NEED_CONTEXT: %d' % (len(pairs), sum(1 for p in pairs if p[3] > 1)))
for i, a, b, c in pairs:
    if c > 1:
        print('DUP line %d occ %d: %s' % (i, c, a))
