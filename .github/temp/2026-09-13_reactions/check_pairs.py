"""Audit every inserted target nucleus in the adopted file: collect each
(nucleus, reaction) pair that the mapping produced and count occurrences.

Usage: python check_pairs.py FILE
"""
import re
import sys
from collections import Counter

raw = open(sys.argv[1], 'r', encoding='utf-8', errors='replace').read()
lines = raw.replace('\r\n', '\n').split('\n')

pattern = re.compile(r'\{\+(\d+)\}([A-Z][a-z]?)\(([^)]*)\)')
counts = Counter()
for i, ln in enumerate(lines, 1):
    if len(ln) > 6 and ln[6] != ' ':          # comment line only
        for m in pattern.finditer(ln):
            counts[(m.group(1) + m.group(2), m.group(3))] += 1

print('distinct (nucleus, reaction) pairs in comment lines: %d' % len(counts))
for (nuc, rx), n in sorted(counts.items()):
    print('%-8s %-26s %d' % (nuc, '(' + rx + ')', n))
print('total occurrences: %d' % sum(counts.values()))
