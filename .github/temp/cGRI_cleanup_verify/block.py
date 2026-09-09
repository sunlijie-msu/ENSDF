data=open(r'd:\X\ND\ENSDF\A34\S34\new\S34_31p_a_pg.ens',encoding='utf-8-sig',newline='').read()
lines=data.split('\r\n')
if lines and lines[-1]=='': lines=lines[:-1]
from collections import Counter
flags=Counter()
for i,l in enumerate(lines,1):
    if len(l)>76 and l[7]=='G':
        f=l[76]
        flags[f]+=1
print('col77 flag distribution across G records:',dict(flags))
# For each of 22 Mo09 singles, show full block: G + subsequent comment lines until next data record (L/G/d)
mo=[i for i,l in enumerate(lines,1) if l.rstrip()==' 34S  cG RI$from 1970Mo09.']
for ci in mo:
    # block from G line (ci-1) forward until next G or L or d
    start=ci-1
    j=ci  # 0-based next line index+1
    block=[]
    # print lines from G to before next L/G/d/PN
    k=start
    print('=== G@%d (E=%s) ==='%(start,lines[start-1][9:19].strip()))
    while k<=len(lines):
        l=lines[k-1]
        if k==start or (len(l)>7 and l[5]==' ' and l[7] in 'LG' ) or l[5]=='d' or (len(l)>6 and l[6]=='P'):
            if k!=start:
                pass
        block.append((k,l.rstrip()))
        # stop at next data-ish record
        if k>start:
            # stop if next record is L or G (col8 L/G with col6 blank) or 'd' or PN
            if len(l)>7 and l[6]!=' ' and l[7]=='c':
                pass  # continuation comment
            elif len(l)>7 and l[5]==' ' and l[7]=='G':
                break
            elif len(l)>7 and l[5]==' ' and l[7]=='L':
                break
            elif l[5:6]=='d':
                break
        k+=1
    for (n,t) in block:
        print('   [%d] %s'%(n,t))
