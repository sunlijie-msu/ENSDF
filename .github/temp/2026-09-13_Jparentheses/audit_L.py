import sys

path = sys.argv[1]
lines = open(path, encoding='utf-8').read().splitlines()
print('idx  len  c8  nucid  c22  J(23-39)          tail40_blank  Jstart  Jend')
for i, l in enumerate(lines, 1):
    rt = l[7] if len(l) > 7 else '?'
    if rt == 'L':
        j = l[22:39].rstrip()
        tail_blank = (l[39:].strip() == '') if len(l) > 39 else True
        print('{:>3}  {:>3}  {}   [{}]  {!r:>4}  {:<16}  {!s:<12}  {:>2}     {:>2}'.format(
            i, len(l), rt, l[0:5], l[21] if len(l) > 21 else '', j, tail_blank, 23, 22 + len(j)))

print('--- non-L records ---')
for i, l in enumerate(lines, 1):
    rt = l[7] if len(l) > 7 else '?'
    if rt != 'L':
        print('{:>3}  len={:>3}  c8={!r}  data={}'.format(i, len(l), rt, l[:40]))
