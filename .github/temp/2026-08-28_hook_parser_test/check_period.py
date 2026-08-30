p = r'd:\X\ND\ENSDF\A34\A34_NDS2012.txt'
t = open(p, encoding='utf-8', newline='').read().replace('\r\n', '\n')
ls = t.split('\n')
es = [x.rstrip() for x in ls if 'cL E$from' in x]
print('E$from comments in 2012 NDS:', len(es))
for x in es[:10]:
    print('  ', repr(x[-55:]))
hasp = sum(1 for x in es if x.endswith('.'))
print('ending with period:', hasp, 'of', len(es))
