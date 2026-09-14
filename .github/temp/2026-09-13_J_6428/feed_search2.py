"""Find gamma rays that can feed a target level (debug version).

Usage: python feed_search2.py FILE LEVEL_E [TOL]
"""
import sys

path = sys.argv[1]
target = float(sys.argv[2])
tol = float(sys.argv[3]) if len(sys.argv) > 3 else 1.2
print('ARGS: path=%r target=%r tol=%r' % (path, target, tol))

with open(path, 'r', encoding='utf-8', errors='replace') as fh:
    lines = fh.read().split('\n')

print('nlines=%d' % len(lines))

level = None
jpi = ''
hits = 0
for idx, ln in enumerate(lines):
    if len(ln) < 10:
        continue
    cont, com, typ = ln[5], ln[6], ln[7]   # col6=idx5, col7=idx6, col8=idx7
    if cont != ' ' or com != ' ':
        continue                            # skip continuation/comment records
    if typ == 'L':
        e_str = ln[9:19].strip()
        try:
            level = float(e_str)
        except ValueError:
            print('LEVEL-PARSE-FAIL idx=%d E=%r line=%r' % (idx, e_str, ln[:45]))
            level = None
            continue
        jpi = ln[22:39].strip()
    elif typ == 'G':
        if level is None or level <= target:
            continue
        try:
            e = float(ln[9:19])
        except ValueError:
            continue
        d = (level - target) - e
        if abs(d) <= tol:
            hits += 1
            print('MATCH line %5d  E_level=%10.3f Jpi=%-10s g=%9s ri=%-8s dE=%+6.3f' % (
                idx + 1, level, jpi, ln[9:19].strip(), ln[22:29].strip(), d))
print('TOTAL MATCHES: %d' % hits)
