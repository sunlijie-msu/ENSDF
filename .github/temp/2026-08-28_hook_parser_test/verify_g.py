path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
t = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n')
for content in [' 34S   G 7915         130', ' 34S   G 8185         56']:
    print(repr(content), 'count:', t.count(content), 'newlen80:', len(content) + 1 == 80 or True)
