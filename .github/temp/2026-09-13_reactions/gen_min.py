"""Emit minimal unique (old, new) anchors for every comment line needing a target
nucleus, writing the result to .github/temp (never into the data tree).

Usage: python gen_min.py FILE OUT
Print format per pair:
### LINE <n>
OLD
<old anchor text>
NEW
<new anchor text>
"""
import re
import sys

path = sys.argv[1]
out = sys.argv[2]

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


raw = open(path, 'r', encoding='utf-8', errors='replace').read()
lines = raw.split('\n')

pairs = []
for i, ln in enumerate(lines, 1):
    base = ln.rstrip()
    new = fix(base)
    if new == base:
        continue
    # tight window: from the first change to the last change
    s = 0
    while s < len(base) and new[:s + 1].rstrip() == base[:s + 1].rstrip():
        s += 1
    # find first differing char index robustly
    a = b = None
    for k in range(len(base)):
        if k >= len(new) or base[k] != new[k]:
            a = k
            break
    if a is None:
        continue
    # last differing char (compare from the right)
    j = 1
    while j <= len(base) and j <= len(new) and base[len(base) - j] == new[len(new) - j]:
        j += 1
    b = len(base) - j + 1
    # extend left/right until unique in file
    L, R = a, b + 1
    while True:
        cand = base[L:R]
        if cand and raw.count(cand) == 1:
            break
        if L > 0:
            L -= 1
        elif R < len(base):
            R += 1
        else:
            break
    old = base[L:R]
    newtxt = new[L:R]
    if raw.count(old) != 1:
        # fall back to previous line tail + this line
        prev = lines[i - 2].rstrip()
        for k in range(1, len(prev) + 1):
            cand = prev[len(prev) - k:] + '\n' + base
            if raw.count(cand) == 1:
                old = cand
                newtxt = prev[len(prev) - k:] + '\n' + new
                break
    pairs.append((i, old, newtxt, raw.count(old)))

with open(out, 'w', encoding='utf-8') as fh:
    for i, o, n, c in pairs:
        fh.write('### LINE %d (occurrences %d)\nOLD %s\nNEW %s\n' % (i, c, o, n))
print('pairs: %d  non-unique: %d' % (len(pairs), sum(1 for p in pairs if p[3] != 1)))
