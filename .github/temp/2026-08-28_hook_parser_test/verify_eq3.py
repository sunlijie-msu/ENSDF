path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
t = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n')

for v in ['700', '2600', '750']:
    old = 'intensities =%s from this resonance to ' % v
    print(v, 'unique', old in t)

c1300 = ' 34S  cL $1965Mc07 states that |g intensities =1300 from this resonance to      '
n1300 = ' 34S  cL $1965Mc07 states that |g intensities = 1300 from this resonance to     '
c2 = ' 34S 2cL {+34}S levels higher than 3304 keV.' + ' ' * 36
for gl, gls in [('G7915', ' 34S   G 7915'), ('G8185', ' 34S   G 8185')]:
    old = c1300 + '\n' + c2 + '\n' + gls
    new = n1300 + '\n' + c2 + '\n' + gls
    print(gl, 'match', old in t, 'newcl_len', len(new.split('\n')[0]))
