path = r'd:\X\ND\ENSDF\A34\S34\new\S34_33s_d_p.ens'
b = open(path, 'rb').read()
t = b.decode('utf-8').replace('\r\n', '\n')
ls = t.split('\n')
print('CRLF:', b.count(b'\r\n'), 'nonascii:', sum(1 for x in b if x > 127), 'lines:', len(ls))
print('over80:', [(i+1, len(x)) for i, x in enumerate(ls) if len(x) > 80])
print('non-80/0:', [(i+1, len(x)) for i, x in enumerate(ls) if len(x) not in (80,0)][:8])

print()
print('=== general flag comments ===')
for i, x in enumerate(ls):
    if 'E(B)$' in x or 'E(C)$' in x or 'E(V)$' in x:
        print(f'  line {i+1}: {x.rstrip()}')
print('E(B)$:', sum(1 for x in ls if 'E(B)$' in x),
      'E(C)$:', sum(1 for x in ls if 'E(C)$' in x),
      'E(V)$:', sum(1 for x in ls if 'E(V)$' in x))

print()
print('=== redundant E$ comments remaining (should be 0 for simple) ===')
simple = [x.rstrip() for x in ls if 'cL E$from 1963Br05' in x or 'cL E$from 1972Cr08' in x]
va21 = [x.rstrip() for x in ls if 'level measured by 1971Va21' in x]
print('  "E$from 1963Br05" simple:', len([s for s in simple if 'Other:' not in s]))
print('  "E$from 1972Cr08" simple:', len([s for s in simple if 'weak' not in s]))
print('  "level measured by 1971Va21":', len(va21))
print()
print('=== kept comments (should be present) ===')
for m in ['observed by 1972Cr08', 'Other: 7388', 'weak, from 1972Cr08', 'weighted average of']:
    print(f'  {m!r}: {sum(1 for x in ls if m in x)}')
print()
print('=== L/S/S-other comments intact on flagged levels? ===')
for lev in ['2122', '5326', '3915', '7398', '6128']:
    for i, x in enumerate(ls):
        if x.startswith(' 34S   L ' + lev + ' '):
            print(f'  L {lev}:')
            for j in range(i+1, min(i+4, len(ls))):
                if ls[j].startswith(' 34S  c'):
                    print(f'    {ls[j].rstrip()[:60]}')
            break
