"""Print exact L-record lines (repr + length) and locate J-π field content.

Usage: python list_L.py FILE
"""
import sys

path = sys.argv[1]
with open(path, 'r', encoding='utf-8', errors='replace') as fh:
    lines = fh.read().split('\n')

print('total lines: %d' % len(lines))
for i, l in enumerate(lines, 1):
    if len(l) > 7 and l[7] == 'L' and l[6] == ' ':
        j = l[22:39]
        stripped = j.rstrip()
        print('%3d len=%2d J=%r start=23 endcol=%d trailing=%d' % (
            i, len(l), stripped, 22 + len(stripped),
            len(l) - (22 + len(stripped)) if len(l) > 23 else -1))
        print('    RAW>>>%s<<<' % l)
