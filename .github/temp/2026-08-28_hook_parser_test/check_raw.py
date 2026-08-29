path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
b = open(path, 'rb').read()
t = b.decode('utf-8').replace('\r\n', '\n')
ls = t.split('\n')
print('total lines:', len(ls))
print('all lines with len!=80:')
for i, x in enumerate(ls):
    if len(x) != 80:
        print('  1-based', i + 1, 'len', len(x), 'repr', repr(x))
print()
print('=== raw region 298-345 (1-based) ===')
for i in range(297, 345):
    print(i + 1, repr(ls[i]))
