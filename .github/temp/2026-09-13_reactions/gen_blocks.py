"""Emit unique block anchors for all lines needing a target nucleus in comment text.

Usage: python gen_blocks.py FILE > blocks.txt
Each block is a maximal run of lines needing change, extended backwards until its
text is unique in the file. Interior lines are emitted exactly as they appear
(including their padding); the last line of a block is emitted without trailing
padding. Print format:

BLOCK <first>-<last> OCC <n>
OLD>>>
<old text>
<<<END
NEW>>>
<new text>
<<<END
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


def fix(line):
    new = line
    for frag, prefix in RULES:
        new = re.sub(frag, lambda m, p=prefix: p + m.group(1), new)
    return new


raw = open(path, 'r', encoding='utf-8', errors='replace').read()
lines = raw.split('\n')
need = [i for i, ln in enumerate(lines, 1) if fix(ln.rstrip()) != ln.rstrip()]

blocks = []
cur = [need[0]]
for x in need[1:]:
    if x == cur[-1] + 1:
        cur.append(x)
    else:
        blocks.append(cur)
        cur = [x]
blocks.append(cur)

out = []
for b in blocks:
    first, last = b[0], b[-1]
    extended = False
    while True:
        body = lines[first - 1:last]
        old = '\n'.join(body[:-1] + [body[-1].rstrip()])
        if raw.count(old) == 1 or first == 1:
            break
        first -= 1
        extended = True
    body = lines[first - 1:last]
    old = '\n'.join(body[:-1] + [body[-1].rstrip()])
    parts = []
    for k, ln in enumerate(body):
        t = ln.rstrip() if k == len(body) - 1 else ln
        parts.append(fix(t))
    new = '\n'.join(parts)
    out.append((b[0], b[-1], first, raw.count(old), old, new, extended))

with open(sys.argv[2] if len(sys.argv) > 2 else '.github/temp/2026-09-13_reactions/blocks.txt', 'w', encoding='utf-8') as fh:
    for lo, hi, first, occ, old, new, ext in out:
        fh.write('BLOCK %d-%d (anchor from %d) OCC %d%s\n' % (lo, hi, first, occ, ' EXTENDED' if ext else ''))
        fh.write('OLD>>>\n%s\n<<<END\n' % old)
        fh.write('NEW>>>\n%s\n<<<END\n' % new)
print('blocks: %d  change-lines: %d' % (len(out), len(need)))
