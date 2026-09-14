"""Emit context anchors for the duplicate comment lines, with padding rendered as
middle dots so it can be counted reliably and converted back to spaces.

Usage: python gen_dup.py FILE
Writes dup_anchors.txt with:
### target <n>  pad_before_each_newline
OLD (dots = spaces)
NEW (dots = spaces)
"""
import re
import sys

path = sys.argv[1]
out = '.github/temp/2026-09-13_reactions/dup_anchors.txt'

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


def dots(s):
    return s.replace(' ', '.')


res = []
for i, ln in enumerate(lines, 1):
    t = ln.rstrip()
    new = fix(t)
    if new == t or raw.count(t) == 1:
        continue
    first = i
    while True:
        body = lines[first - 1:i]
        old = '\n'.join(body[:-1] + [body[-1].rstrip()])
        if raw.count(old) == 1:
            break
        if first == 1:
            break
        first -= 1
    body = lines[first - 1:i]
    old = '\n'.join(body[:-1] + [body[-1].rstrip()])
    parts = []
    for k, l2 in enumerate(body):
        tt = l2.rstrip() if k == len(body) - 1 else l2
        parts.append(fix(tt))
    newblock = '\n'.join(parts)
    pads = [len(b) - len(b.rstrip()) for b in body[:-1]]
    res.append((i, first, raw.count(old), dots(old), dots(newblock), pads))

with open(out, 'w', encoding='utf-8') as fh:
    for i, first, occ, o, n, pads in res:
        fh.write('### target %d  anchor %d-%d  occurs %d  pads %s\n' % (i, first, i, occ, pads))
        fh.write('OLD %s\n' % o)
        fh.write('NEW %s\n' % n)
print('anchors: %d' % len(res))
