"""Emit minimal unique anchors for every comment line still lacking a target
nucleus. Prefers FORWARD context (following lines, right-trimmed) so that no
interior line padding has to be reproduced by hand; falls back to backward
context only when forward context is not enough.

Usage: python gen_final3.py FILE OUT
Format: ### BLOCK <start>-<end> (occurs N) / OLD ... / NEW ...
Interior spaces are rendered as '.' (only backward fallback blocks can contain
them). The final line of each block is right-trimmed, so the trailing padding of
the last line is never part of the replacement.
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


def needs(line):
    base = line.rstrip()
    return fix(base) != base


def render(text):
    return text.replace(' ', '.')


raw = open(path, 'r', encoding='utf-8', errors='replace').read().replace('\r\n', '\n')
lines = raw.split('\n')

need = [i for i, ln in enumerate(lines) if needs(ln)]


def anchor(s, e):
    blk = lines[s:e + 1]
    return '\n'.join(blk[:-1] + [blk[-1].rstrip()])


def interior_pad(s, e):
    return sum(len(ln) - len(ln.rstrip()) for ln in lines[s:e])


spans = []
for i in need:
    cands = []
    for f in range(0, 5):
        e = i + f
        if e >= len(lines):
            break
        if raw.count(anchor(i, e)) == 1:
            cands.append((i, e))
    for b in range(1, 8):
        s = i - b
        if s < 0:
            break
        if raw.count(anchor(s, i)) == 1:
            cands.append((s, i))
    if cands:
        cands.sort(key=lambda se: (interior_pad(*se), se[1] - se[0]))
        chosen = cands[0]
    else:
        chosen = (max(0, i - 8), i)
    spans.append(chosen)

spans.sort()
merged = []
for s, e in spans:
    if merged and s <= merged[-1][1] + 1:
        merged[-1][1] = max(merged[-1][1], e)
    else:
        merged.append([s, e])

blocks = []
bad = []
for s, e in merged:
    s0, e0 = s, e
    while raw.count(anchor(s, e)) != 1 and s > 0:
        s -= 1
    cnt = raw.count(anchor(s, e))
    if cnt != 1:
        bad.append((s0, e0, s, cnt, lines[e0].rstrip()))
    newlines = []
    for ln in lines[s:e + 1]:
        if needs(ln):
            newlines.append(fix(ln.rstrip()))
        else:
            newlines.append(ln if newlines else ln)
    newtxt = '\n'.join(newlines[:-1] + [newlines[-1].rstrip()]) if newlines else ''
    oldtxt = anchor(s, e)
    blocks.append((s + 1, e + 1, cnt, oldtxt, newtxt))

for s0, e0, s, cnt, txt in bad:
    print('BAD span %d-%d -> %d (occurs %d) : %s' % (s0, e0, s, cnt, txt[:70]))

with open(out, 'w', encoding='utf-8') as fh:
    for s, e, cnt, old, new in blocks:
        fh.write('### BLOCK %d-%d (occurs %d)\n' % (s, e, cnt))
        fh.write('OLD ' + render(old) + '\n')
        fh.write('NEW ' + render(new.replace(' ', '.')) + '\n')

print('remaining lines: %d  blocks: %d  non-unique: %d'
      % (len(need), len(blocks), sum(1 for b in blocks if b[2] != 1)))
