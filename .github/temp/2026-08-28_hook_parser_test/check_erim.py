path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
t = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n')
ls = t.split('\n')
print('=== all cG E,RI,M$from 1965Mc07 lines ===')
for i, x in enumerate(ls):
    if 'cG E,RI,M$from 1965Mc07' in x:
        print('line', i + 1, repr(x))
print()
print('=== all cG E,RI$from 1965Mc07 lines ===')
for i, x in enumerate(ls):
    if 'cG E,RI$from 1965Mc07' in x:
        print('line', i + 1, repr(x))
print()
print('=== context around W gammas 9329-9583 ===')
for i in range(283, 347):
    print(i + 1, repr(ls[i]))
