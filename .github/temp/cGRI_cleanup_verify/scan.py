import io
p=r'd:\X\ND\ENSDF\A34\S34\new\S34_31p_a_pg.ens'
lines=open(p,encoding='utf-8-sig').read().splitlines()
print('--- verify 5 converted lines ---')
for i in (134,213,294,313,392):
    print('[%d] %s'%(i,lines[i-1].rstrip()))
print('--- any RI$ comments w/ value repetition (no from/weighted/Other)? ---')
pref=' 34S  cG RI$'
found=0
for idx,l in enumerate(lines,1):
    if l.startswith(pref) and 'from' not in l and 'weighted' not in l and 'Other' not in l:
        print('[%d] KEEP? %s'%(idx,l.rstrip())); found+=1
print('repetition-comments remaining:',found)
c=sum(1 for l in lines if l.startswith(pref+'from'))
print('RI$from count=',c)
bad=[(i+1,len(l)) for i,l in enumerate(lines) if len(l)!=80]
print('non-80 lines:',bad)
