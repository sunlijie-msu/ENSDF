p='d:/X/ND/ENSDF/XUNDL/B_E2_CL10995.ens'
with open(p,'r',encoding='utf-8') as f:
    lines=f.readlines()
bad=[(i+1,len(l.rstrip('\n'))) for i,l in enumerate(lines) if len(l.rstrip('\n'))!=80]
print('Total lines:',len(lines))
if bad:
    print('Lines not 80 chars:')
    for i,l in bad:
        print(i,l)
else:
    print('All lines are exactly 80 characters')
for i in [1,3,5,10,15]:
    if i<=len(lines):
        print(f'Line {i} len={len(lines[i-1].rstrip())}:',repr(lines[i-1].rstrip()))
