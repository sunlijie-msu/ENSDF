"""List all comment lines containing bare (target-less) reaction notations.

Usage: python find_bare.py FILE [START] [END]
A notation is "bare" when it is preceded by a space instead of a nucleus symbol,
e.g. ' (|a,p|g)' vs the correct ' {+31}P(|a,p|g)'.
"""
import re
import sys

path = sys.argv[1]
lo = int(sys.argv[2]) if len(sys.argv) > 2 else 1
hi = int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 9

pats = [
    r' \(\|a,p\|g\)',
    r' \(n,\|g\)',
    r' \(n,n\)',
    r' \(\{\+16\}O,\|a2p\|g\)',
    r' \(\{\+36\}S,\{\+34\}S\|g\)',
    r' \(\{\+34\}S,\{\+34\}S\'\|g\)',
    r' \(p,p\'\|g\)',
    r' \(p,p\'\)',
    r' \(p,p\)',
    r' \(pol p,p\'\)',
    r' \(t,p\)',
    r' \(d,p\)',
    r' \(d,\{\+3\}He\)',
    r' \(\|g,\|g\'\)',
    r' \(pol \|g,\|g\'\)',
    r' \(e,e\'\)',
    r' \(\|a,\|g\)',
    r' \(\|a,n\)',
    r' \(\|a,\|a\'\)',
    r' \(\{\+35\}Cl,',
]
rx = re.compile('|'.join(pats))

lines = open(path, 'r', encoding='utf-8', errors='replace').read().split('\n')
n = 0
for i, ln in enumerate(lines, 1):
    if lo <= i <= hi and rx.search(ln):
        found = sorted(set(m.group(0).strip() for m in rx.finditer(ln)))
        n += 1
        print('%5d | %s' % (i, ln.rstrip()))
        print('      ^^ bare: %s' % '  '.join(found))
print('TOTAL LINES: %d' % n)
