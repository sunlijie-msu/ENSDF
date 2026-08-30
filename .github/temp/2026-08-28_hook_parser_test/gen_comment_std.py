path = r'd:\X\ND\ENSDF\A34\S34\new\S34_33s_d_p.ens'
t = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n')
ls = t.split('\n')

def pad(s):
    return s + ' ' * (80 - len(s))

# find comment lines
for i, x in enumerate(ls):
    if 'E$from 1972Cr08.' in x:
        print('L7547 line', i+1, repr(x))
        print('  NEW', repr(pad(' 34S  cL E$from 1972Cr08')))
    if 'E$from 1963Br05. Other:' in x:
        print('L7398 line', i+1, repr(x))
        print('  NEW', repr(pad(' 34S  cL E$from 1963Br05; other: 7388 {I14} (1972Cr08)')))

# verify new lengths
print('len L7547 new:', len(pad(' 34S  cL E$from 1972Cr08')))
print('len L7398 new:', len(pad(' 34S  cL E$from 1963Br05; other: 7388 {I14} (1972Cr08)')))
# uniqueness of old comment lines
print('L7547 old unique:', t.count(' 34S  cL E$from 1972Cr08.') == 1)
print('L7398 old unique:', t.count(' 34S  cL E$from 1963Br05. Other: 7388 (1972Cr08).') == 1)
