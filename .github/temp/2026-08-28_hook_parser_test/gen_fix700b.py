path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
t = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n')

def pad(content, total=80):
    return content + ' ' * (total - len(content))

repls = []
for v, gline in [('700', ' 34S   G 8076'), ('750', ' 34S   G 8338')]:
    old_cl = ' 34S  cL $1965Mc07 states that |g intensities = %s from this resonance to{+34}S' % v
    old_c2 = ' 34S 2cL levels higher than 3304 keV.'
    new_cl = pad(' 34S  cL $1965Mc07 states that |g intensities = %s from this resonance to' % v)
    new_c2 = pad(' 34S 2cL {+34}S levels higher than 3304 keV.')
    # find old lines exact
    old_lines = None
    for i in range(len(t.split('\n')) - 2):
        ls = t.split('\n')
        if ls[i] == old_cl and ls[i + 1] == old_c2 and ls[i + 2].startswith(gline):
            old_lines = (ls[i], ls[i + 1], ls[i + 2])
            idx = i + 1
            break
    if old_lines is None:
        print(v, 'OLD NOT FOUND')
        continue
    old = old_lines[0] + '\n' + old_lines[1] + '\n' + old_lines[2]
    new = new_cl + '\n' + new_c2 + '\n' + old_lines[2]
    print(v, 'idx', idx, 'match', old in t, 'oldlens', len(old_lines[0]), len(old_lines[1]), 'newlens', len(new_cl), len(new_c2))
    print('  old cL:', repr(old_lines[0]))
    print('  old c2:', repr(old_lines[1]))
    print('  new cL:', repr(new_cl))
    print('  new c2:', repr(new_c2))
    repls.append((old, new))
