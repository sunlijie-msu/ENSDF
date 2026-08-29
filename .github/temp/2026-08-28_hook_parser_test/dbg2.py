path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
t = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n')

c1300 = ' 34S  cL $1965Mc07 states that |g intensities =1300 from this resonance to      '
c2 = ' 34S 2cL {+34}S levels higher than 3304 keV.' + ' ' * 33
gl = ' 34S   G 7915'
print('c1300 in t:', c1300 in t)
print('c2 in t:', c2 in t)
print('c1300\\n in t:', (c1300 + '\n') in t)
print('c1300\\n+c2 in t:', (c1300 + '\n' + c2) in t)
print('c1300\\n+c2\\n in t:', (c1300 + '\n' + c2 + '\n') in t)
print('full in t:', (c1300 + '\n' + c2 + '\n' + gl) in t)
# find line 212 raw
ls = t.split('\n')
for i in range(210, 215):
    print(i + 1, repr(ls[i]))
