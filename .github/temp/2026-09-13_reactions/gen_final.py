"""Emit padding-free replacement anchors.

Usage: python gen_final.py FILE
Writes:
  single.txt   -- anchors that are entire trimmed comment lines (unique in file)
  dup.txt      -- lines whose trimmed text occurs more than once; these need a
                  multi-line anchor, printed with explicit pad counts.
"""
import re
import sys

path = sys.argv[1]
base_dir = '.github/temp/2026-09-13_reactions/'

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

singles, dups = [], []
for i, ln in enumerate(lines, 1):
    t = ln.rstrip()
    new = fix(t)
    if new == t:
        continue
    if raw.count(t) == 1:
        singles.append((i, t, new))
    else:
        dups.append((i, t, new, raw.count(t)))

with open(base_dir + 'single.txt', 'w', encoding='utf-8') as fh:
    for i, o, n in singles:
        fh.write('### %d\nOLD %s\nNEW %s\n' % (i, o, n))

with open(base_dir + 'dup.txt', 'w', encoding='utf-8') as fh:
    for i, t, n, c in dups:
        fh.write('### line %d  occurs %d  pad=%d\nOLD %s\nNEW %s\n' % (i, c, 80 - len(t), t, n))

print('single: %d   dup: %d' % (len(singles), len(dups)))
