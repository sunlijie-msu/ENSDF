p = r'd:\X\ND\ENSDF\A34\A34_NDS2012.txt'
t = open(p, encoding='utf-8', newline='').read().replace('\r\n', '\n')
ls = t.split('\n')
other = [x.rstrip() for x in ls if 'cL E$' in x and 'Other:' in x]
print('E$ ... Other: comments in 2012 NDS:', len(other))
for x in other[:10]:
    print('  ', repr(x[-60:]))
# also check 'other:' lowercase
other2 = [x.rstrip() for x in ls if 'cL E$' in x and 'other:' in x]
print('E$ ... other: (lowercase) comments:', len(other2))
for x in other2[:10]:
    print('  ', repr(x[-60:]))
