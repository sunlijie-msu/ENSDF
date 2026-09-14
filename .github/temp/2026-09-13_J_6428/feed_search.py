"""Find gamma rays that can feed a target level in an ENSDF adopted file.

Usage: python feed_search.py FILE LEVEL_E [TOL]
Prints, for every level above LEVEL_E, any G record whose energy matches
(E_level - LEVEL_E) within TOL keV, plus the parent level J-pi.
"""
import sys

path, target = sys.argv[1], float(sys.argv[2])
tol = float(sys.argv[3]) if len(sys.argv) > 3 else 1.2

lines = open(path, 'r', encoding='utf-8', errors='replace').read().split('\n')
print('DIAG: lines=%d  L=%d  G=%d' % (
    len(lines),
    sum(1 for l in lines if len(l) > 7 and l[7] == 'L' and l[6] == ' '),
    sum(1 for l in lines if len(l) > 7 and l[7] == 'G' and l[6] == ' ')))
print('DIAG: lines containing 1353.46 -> %d' % sum(1 for l in lines if '1353.46' in l))
for i, l in enumerate(lines):
    if '1353.46' in l:
        print('DIAG: found at index %d; previous lines:' % i)
        for k in range(max(0, i - 4), i + 1):
            print('   [%d] len=%d col6=%r col8=%r %r' % (k, len(lines[k]), lines[k][6:7], lines[k][7:8], lines[k][:40]))
level = None
for i, l in enumerate(lines, 1):
    if len(l) < 10:
        continue
    if l[7] == 'L' and l[6] == ' ':
        try:
            level = float(l[9:19])
        except ValueError:
            level = None
            continue
        jpi = l[22:39].strip()
    elif l[7] == 'G' and l[6] == ' ' and level is not None and level > target:
        try:
            e = float(l[9:19])
        except ValueError:
            continue
        d = (level - target) - e
        if abs(d) <= tol:
            print('line %5d  E_level=%10.3f Jpi=%-10s  g=%9s ri=%-8s dE=%+6.3f' % (
                i, level, jpi, l[9:19].strip(), l[22:29].strip(), d))
