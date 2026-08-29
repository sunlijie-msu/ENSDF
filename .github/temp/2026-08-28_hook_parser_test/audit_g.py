path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
t = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n')
ls = t.split('\n')
for idx in [213, 300]:  # 0-based for lines 214, 301
    x = ls[idx]
    print('line', idx + 1, 'len', len(x), 'trail', len(x) - len(x.rstrip()), '| repr:', repr(x))
    print('  content:', repr(x.rstrip()))
