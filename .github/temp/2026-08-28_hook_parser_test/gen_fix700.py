path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
ls = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n').split('\n')

def pad(content, total=80):
    return content + ' ' * (total - len(content))

# target structure (matches correct 1300/2600 blocks)
for v in ['700', '750']:
    cl = pad(' 34S  cL $1965Mc07 states that |g intensities = %s from this resonance to' % v)
    c2 = pad(' 34S 2cL {+34}S levels higher than 3304 keV.')
    print(v, 'cl len', len(cl), 'c2 len', len(c2))
    # find current broken lines
    for i, x in enumerate(ls):
        if 'intensities = %s from this resonance to' % v in x.replace(' ', '') or ('= %s from this resonance to' % v) in x:
            print('  idx', i + 1, repr(x))
            print('  nxt', repr(ls[i + 1]))
