path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
t = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n')
ls = t.split('\n')

def pad(content, total=80):
    return content + ' ' * (total - len(content))

new_cl_700 = pad(' 34S  cL $1965Mc07 states that |g intensities = 700 from this resonance to')
new_cl_750 = pad(' 34S  cL $1965Mc07 states that |g intensities = 750 from this resonance to')
new_c2 = pad(' 34S 2cL {+34}S levels higher than 3304 keV.')
print('new cl700 len', len(new_cl_700), 'new cl750 len', len(new_cl_750), 'new c2 len', len(new_c2))
print('REPR new cl700:', repr(new_cl_700))
print('REPR new cl750:', repr(new_cl_750))
print('REPR new c2   :', repr(new_c2))
print()
for i, x in enumerate(ls):
    if 'intensities = 700' in x or 'intensities = 750' in x:
        print('cL', i + 1, repr(x))
        print('2cL', i + 2, repr(ls[i + 1]))
        print('G', i + 3, repr(ls[i + 2]))
        print()
