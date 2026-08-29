path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
t = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n')
ls = t.split('\n')

def sp(n):
    return ' ' * n

for v, gval in [('700', ' 34S   G 8076         270'), ('750', ' 34S   G 8338         20')]:
    # old block (corrupted)
    old_cl = ' 34S  cL $1965Mc07 states that |g intensities = %s from this resonance to{+34}S' % v
    old_c2 = ' 34S 2cL levels higher than 3304 keV.'
    # find exact current lines
    for i in range(len(ls) - 2):
        if ls[i] == old_cl:
            o2 = ls[i + 1]
            og = ls[i + 2]
            break
    # new block
    ncl = ' 34S  cL $1965Mc07 states that |g intensities = %s from this resonance to' % v
    nc2 = ' 34S 2cL {+34}S levels higher than 3304 keV.'
    new_cl = ncl + sp(80 - len(ncl))
    new_c2 = nc2 + sp(80 - len(nc2))
    print('==== block', v, '====')
    print('OLD cL len', len(old_cl), ':', repr(old_cl))
    print('OLD c2 len', len(o2), ':', repr(o2))
    print('OLD G  len', len(og), ':', repr(og))
    print('NEW cL len', len(new_cl), ':', repr(new_cl))
    print('NEW c2 len', len(new_c2), ':', repr(new_c2))
    # validate uniqueness of 3-line block
    block = old_cl + '\n' + o2 + '\n' + og
    print('3-line block unique:', t.count(block) == 1)
    # validate 2-line (cL+c2) uniqueness
    block2 = old_cl + '\n' + o2
    print('2-line block unique:', t.count(block2) == 1)
