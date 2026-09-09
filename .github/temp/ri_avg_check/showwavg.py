import re
data=open(r'd:\X\ND\ENSDF\A34\S34\new\S34_31p_a_pg.ens',encoding='utf-8-sig',newline='').read()
lines=data.split('\r\n')
tg=set(['1175.2','3303.1','1945.5','4070.9','1986.9','4113.7','1318.8','2495.5','1571.9','2750.9','1587.9','4890.7','1000','1066'])
def isG(l): return len(l)>=19 and l[5:6]==' ' and l[7:8]=='G' and l[6:7]!='c'
def iscG(l): return len(l)>=9 and l[6:7]=='c' and l[7:8]=='G'
for i,l in enumerate(lines):
    if isG(l) and l[9:19].strip() in tg:
        # gather contiguous comment block (cG or 2cG/3cG...)
        j=i+1; cb=[]
        while j<len(lines):
            x=lines[j]
            if iscG(x) or (len(x)>=9 and x[5:6].isdigit() and x[6:7]=='c' and x[7:8]=='G'):
                cb.append(x)
                j+=1
            else: break
        # print only lines with 'weighted average of' (full text joined across conts)
        text=''
        block_txt=''
        for x in cb:
            block_txt += x[9:].rstrip()+' '
        m=re.search(r'weighted average of(.*?)\.',block_txt)
        print(f'G{i+1} {l[9:19].strip():8s} field RI={l[22:29].strip()} DRI={l[29:31].strip()}')
        if m: print('   comment:',m.group(1).strip())
