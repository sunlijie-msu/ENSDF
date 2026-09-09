data=open(r'd:\X\ND\ENSDF\A34\S34\new\S34_31p_a_pg.ens',encoding='utf-8-sig',newline='').read()
lines=data.split('\r\n')
tg=set(['1175.2','3303.1','1945.5','4070.9','1986.9','4113.7','1318.8','2495.5','1571.9','2750.9','1587.9','4890.7','1000','1066'])
def isG(l): return len(l)>=19 and l[5:6]==' ' and l[7:8]=='G' and l[6:7]!='c'
for i,l in enumerate(lines):
    if isG(l) and l[9:19].strip() in tg:
        print('G LINE',i+1,repr(l))
        # collect following cG lines until next G or L or non-comment
        j=i+1
        while j<len(lines) and (lines[j][6:7]=='c' if len(lines[j])>6 else False):
            print('  cont',j+1,repr(lines[j]))
            j+=1
