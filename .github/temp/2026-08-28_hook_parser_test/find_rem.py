p = r'd:\X\ND\ENSDF\A34\S34\new\S34_33s_d_p.ens'
t = open(p, encoding='utf-8', newline='').read().replace('\r\n', '\n')
ls = t.split('\n')
hits = [x.rstrip() for x in ls if 'E$from 1972Cr08' in x]
print('lines containing E$from 1972Cr08:', len(hits))
for h in hits:
    print('  ', repr(h))
hits2 = [x.rstrip() for x in ls if 'E$from 1963Br05' in x]
print('lines containing E$from 1963Br05:', len(hits2))
for h in hits2:
    print('  ', repr(h))
