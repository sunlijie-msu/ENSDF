import re
from collections import Counter

p = r"d:/X/ND/ENSDF/XUNDL/A58/Ni58/new/Ni58_adopted.ens"
L = open(p, encoding="utf-8", errors="replace").read().split("\n")

def g(l, a, b):
    return l.ljust(80)[a - 1:b]

MTOK = ['M1+E2', 'M1(+E2)', '(M1+E2)', '(M1(+E2))', 'E1+M2', 'E1(+M2)', '(E1+M2)', '(E1(+M2))',
        'E2+M1', 'E2(+M1)', '[M1]', '[E1]', '[E2]', '[M2]', '[M1,E2]', '(M1)', '(E1)', '(E2)',
        '(M2)', '(Q)', '(D)', 'D+Q', 'D(+Q)', 'M1', 'E1', 'E2', 'E3', 'M2', 'M3', 'E4', 'M4',
        'E0', 'D', 'Q']

def pm(line):
    sub = g(line, 31, 45)
    st = None
    for k, ch in enumerate(sub):
        if ch in "([EMDQ":
            st = k
            break
    if st is None:
        return ""
    sub = sub[st:]
    for t in sorted(MTOK, key=len, reverse=True):
        if sub.startswith(t):
            return t
    return ""

c = Counter(); n = 0
samples = {}
for line in L:
    t = line.ljust(80)
    if t[7] == 'G' and t[6] == ' ' and t[5] == ' ' and re.match(r'^[\d.]+', t[9:19].strip() or ''):
        m = pm(line); c[m] += 1; n += 1
        samples.setdefault(m, []).append(line[:60])
print('gammas', n)
for k, v in c.most_common(25):
    print(f'  {k!r:14} {v}')
print()
for k in ('', 'E', '0', 'T'):
    if k in samples:
        print('sample for', repr(k), ':', samples[k][:3])
