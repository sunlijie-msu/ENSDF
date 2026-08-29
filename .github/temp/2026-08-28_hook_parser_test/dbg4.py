path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
ls = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n').split('\n')
for i in [264, 265, 266, 332, 333, 334]:
    print(i + 1, 'len', len(ls[i]), '|', repr(ls[i]))
