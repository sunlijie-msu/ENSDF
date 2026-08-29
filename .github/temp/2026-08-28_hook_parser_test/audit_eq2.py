import re
path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
b = open(path, 'rb').read()
t = b.decode('utf-8').replace('\r\n', '\n')
ls = t.split('\n')
print('CRLF:', b.count(b'\r\n'), 'nonascii:', sum(1 for x in b if x > 127), 'lines:', len(ls))
print('over80:', [(i + 1, len(x)) for i, x in enumerate(ls) if len(x) > 80])
print()
print('=== intensity blocks ===')
for i, x in enumerate(ls):
    if '1965Mc07 states that' in x:
        print(i + 1, 'len', len(x), 'sp', len(x) - len(x.rstrip()), '|', x.rstrip())
        print(i + 2, 'len', len(ls[i + 1]), 'sp', len(ls[i + 1]) - len(ls[i + 1].rstrip()), '|', ls[i + 1].rstrip())
print()
print('=== scan rule1: `=\s[0-9]` (extra space after =, symbol context) ===')
hits = 0
for i, x in enumerate(ls):
    for m in re.finditer(r'=\s[0-9]', x):
        # report context
        start = max(0, m.start() - 20)
        print(i + 1, '...' + x[start:m.end() + 3] + '...')
        hits += 1
        break
print('rule1 hits:', hits)
print()
print('=== all `=` usages in comments ===')
for i, x in enumerate(ls):
    if '=' in x and (x.startswith(' 34S  c') or x.startswith(' 34S 2c') or x.startswith(' 34S 3c')):
        print(i + 1, repr(x.rstrip()))
