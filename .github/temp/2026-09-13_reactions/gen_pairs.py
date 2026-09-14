"""Generate (old, new) line pairs inserting the correct target nucleus before bare
reaction notations in comment text, matching the XREF list in S34_adopted.ens.

Usage: python gen_pairs.py FILE > pairs.txt
Only comment lines are touched. Lines are printed trimmed (trailing pad preserved
by the caller because the trimmed text is a substring of the padded line).

Also reports any notation occurrence that is neither prefixed nor space/$-separated,
so nothing is silently missed.
"""
import re
import sys

path = sys.argv[1]

# (regex fragment, replacement prefix)  -- order matters: longer/compound first
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

lines = open(path, 'r', encoding='utf-8', errors='replace').read().split('\n')
pairs = []
unclassified = []
nrepl = 0
for i, ln in enumerate(lines, 1):
    if len(ln) > 7 and not (ln[6] in 'cC' or (ln[6] == 'd' and ln[7] == '')):
        pass
    is_comment = len(ln) > 7 and (ln[6] == 'c' or ln[6] in '0123456789dF' or ln[6] == 'S')
    orig = ln.rstrip()
    new = orig
    for frag, prefix in RULES:
        new, k = re.subn(frag, lambda m, p=prefix: p + m.group(1), new)
        nrepl += k
    if new != orig:
        pairs.append((i, orig, new))
    # unclassified occurrences: notation preceded by a char that is not ' ', '$' and not a nucleus
    for m in re.finditer(r'[A-Za-z0-9\)\}]?(\(\|a,p\|g\)|\(n,\|g\)|\(t,p\)|\(d,p\)|\(p,p\'\)|\(p,p\)|\(\|g,\|g\'\)|\(e,e\'\)|\(\|a,\|g\))', orig):
        pre = m.group(0)[:len(m.group(0)) - len(m.group(1))]
        if pre and pre not in ('{+31}P', '{+33}S', '{+32}S', '{+34}S', '{+30}Si', '{+35}Cl'):
            unclassified.append((i, m.group(0)))

for i, a, b in pairs:
    print('LINE %d' % i)
    print('OLD %s' % a)
    print('NEW %s' % b)
print('PAIRS: %d  REPLACEMENTS: %d' % (len(pairs), nrepl))
print('--- manually check these prefixed occurrences (should be valid nuclei) ---')
seen = set()
for i, s in unclassified:
    if s in seen:
        continue
    seen.add(s)
    print('  %5d %s' % (i, s))
