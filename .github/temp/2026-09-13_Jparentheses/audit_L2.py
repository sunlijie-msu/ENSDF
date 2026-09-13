import sys

path = sys.argv[1]
lines = open(path, encoding='utf-8').read().splitlines()
print('DATA L-RECORDS ONLY (col6=blank, col7=blank, col8=L)')
print('line  len  nucid(1-5)  c22   col8  J(23-39)   Jstart Jend  cols40+ blank  parenthesized')
n = 0
for i, l in enumerate(lines, 1):
    if len(l) >= 9 and l[5] == ' ' and l[6] == ' ' and l[7] == 'L':
        n += 1
        j = l[22:39].rstrip()
        tail_blank = (l[39:].strip() == '') if len(l) > 39 else True
        par = j.startswith('(') and j.endswith(')')
        print('{:>4}  {:>3}  [{}]  {!r:>4}  {}     {:<10}  {:>5}  {:>4}  {!s:<14}  {}'.format(
            i, len(l), l[0:5], l[21] if len(l) > 21 else '', l[7], j, 23, 22 + len(j), tail_blank, par))
print('TOTAL data L-records:', n)
print()
print('Any char at/after col 40 in a data L-record:')
for i, l in enumerate(lines, 1):
    if len(l) >= 9 and l[5] == ' ' and l[6] == ' ' and l[7] == 'L':
        seg = l[39:]
        if seg.strip():
            print('  line {}: {!r}'.format(i, seg))
print('  (none printed above = all blank)')
print()
print('Non-80-char lines (all records, excluding final blank):')
for i, l in enumerate(lines, 1):
    if len(l) != 80:
        print('  line {}: len={} {!r}'.format(i, len(l), l))
