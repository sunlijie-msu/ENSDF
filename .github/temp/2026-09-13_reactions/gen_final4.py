"""Emit minimal unique anchors (all lines right-trimmed) for every comment line
still lacking a target nucleus. Uniqueness is verified against a version of the
file in which trailing whitespace is stripped from every line, matching how the
editor's search string is compared.

Usage: python gen_final4.py FILE OUT
Format: ### BLOCK <start>-<end> (occurs N) / OLD ... / NEW ...
Spaces are rendered as '.' so the block can be transcribed unambiguously.
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


raw = open(path, 'r', encoding='utf-8', errors='replace').read().replace('\r\n', '\n')
lines = raw.split('\n')
trimmed = [ln.rstrip() for ln in lines]
norm = '\n'.join(trimmed)
need = [i for i, ln in enumerate(trimmed) if ln and fix(ln) != ln]


def block(s, e):
    return '\n'.join(trimmed[s:e + 1])


spans = []
for i in need:
    cands = []
    for f in range(0, 7):
        e = i + f
        if e >= len(lines):
            break
        if norm.count(block(i, e)) == 1:
            cands.append((i, e))
    for b in range(1, 8):
        s = i - b
        if s < 0:
            break
        if norm.count(block(s, i)) == 1:
            cands.append((s, i))
    if cands:
        cands.sort(key=lambda se: (se[1] - se[0] + 1, se[0]))
        spans.append(cands[0])
    else:
        spans.append((max(0, i - 10), i))

spans.sort()
merged = []
for s, e in spans:
    if merged and s <= merged[-1][1] + 1:
        merged[-1][1] = max(merged[-1][1], e)
    else:
        merged.append([s, e])

blocks = []
for s, e in merged:
    while norm.count(block(s, e)) != 1 and s > 0:
        s -= 1
    cnt = norm.count(block(s, e))
    old = block(s, e)
    new = '\n'.join(fix(ln) if fix(ln) != ln else ln for ln in trimmed[s:e + 1])
    blocks.append((s + 1, e + 1, cnt, old, new))

with open(out, 'w', encoding='utf-8') as fh:
    for s, e, cnt, old, new in blocks:
        fh.write('### BLOCK %d-%d (occurs %d)\n' % (s, e, cnt))
        fh.write('OLD ' + old.replace(' ', '.') + '\n')
        fh.write('NEW ' + new.replace(' ', '.') + '\n')

print('remaining lines: %d  blocks: %d  non-unique: %d'
      % (len(need), len(blocks), sum(1 for b in blocks if b[2] != 1)))
