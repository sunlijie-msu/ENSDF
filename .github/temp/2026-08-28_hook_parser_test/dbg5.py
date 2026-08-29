path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
ls = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n').split('\n')
for i in [264, 265, 332, 333]:
    print(i + 1, 'len', len(ls[i]), 'sp', len(ls[i]) - len(ls[i].rstrip()), '|', repr(ls[i]))
