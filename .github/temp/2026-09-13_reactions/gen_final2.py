"""Emit minimal unique FULL-LINE anchors for every comment line still lacking a
target nucleus, writing results to .github/temp (never into the data tree).

Usage: python gen_final2.py FILE OUT
Print format per block:
### BLOCK <lastline> (occurs N)
OLD <line1>\\n<line2>...
NEW <line1>\\n<line2>...
Spaces are rendered as '.' so trailing padding survives transcription.
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

need = []
for i, ln in enumerate(lines):
    base = ln.rstrip()
    if fix(base) != base:
        need.append(i)

spans = []
for i in need:
    chosen = None
    for k in range(1, 7):
        s = i - k + 1
        if s < 0:
            break
        if raw.count('\n'.join(lines[s:i + 1])) == 1:
            chosen = (s, i)
            break
    if chosen is None:
        chosen = (max(0, i - 5), i)
    spans.append(chosen)

spans.sort()
merged = []
for s, e in spans:
    if merged and s <= merged[-1][1] + 1:
        merged[-1][1] = max(merged[-1][1], e)
    else:
        merged.append([s, e])

blocks = []
for s, e in merged:
    while s > 0 and raw.count('\n'.join(lines[s:e + 1])) != 1:
        s -= 1
    cnt = raw.count('\n'.join(lines[s:e + 1]))
    fixme = []
    for ln in lines[s:e + 1]:
        base = ln.rstrip()
        fixme.append(fix(base) if fix(base) != base else ln)
    blocks.append((e + 1, cnt, '\n'.join(lines[s:e + 1]), '\n'.join(fixme)))

with open(out, 'w', encoding='utf-8') as fh:
    for last, cnt, old, new in blocks:
        fh.write('### BLOCK ends-at-line %d (occurs %d)\n' % (last, cnt))
        fh.write('OLD ' + old.replace(' ', '.') + '\n')
        fh.write('NEW ' + new.replace(' ', '.') + '\n')

print('remaining lines: %d  blocks: %d  non-unique: %d'
      % (len(need), len(blocks), sum(1 for b in blocks if b[1] != 1)))
