import re
path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
t = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n')
ls = t.split('\n')
print('=== all intensity-comment blocks ===')
for i, x in enumerate(ls):
    if '1965Mc07 states that' in x:
        print(i + 1, repr(x))
        if i + 1 < len(ls):
            print(i + 2, repr(ls[i + 1]))
    if x.startswith(' 34S   G 7915') or x.startswith(' 34S   G 8076') or x.startswith(' 34S   G 8185') or x.startswith(' 34S   G 8240') or x.startswith(' 34S   G 8338'):
        print(i + 1, 'G:', repr(x))
print()
print('=== scan: = followed by space-digit (rule 1) ===')
for i, x in enumerate(ls):
    for m in re.finditer(r'=\s[0-9]', x):
        print(i + 1, repr(x))
        break
