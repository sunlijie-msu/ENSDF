import re, math
data=open(r'd:\X\ND\ENSDF\A34\S34\new\S34_31p_a_pg.ens',encoding='utf-8-sig',newline='').read()
lines=data.split('\r\n')
if lines and lines[-1]=='': lines=lines[:-1]
def is_cont(l):
    return len(l)>8 and l[6:7]=='c' and l[7:8]=='G' and l[5:6].isdigit()
def is_dataG(l): return len(l)==80 and l[5:6]==' ' and l[6:7]!='c' and l[7:8]=='G'
def unc_from(vstr, dstr):
    dec=len(vstr.split('.')[1]) if '.' in vstr else 0
    return int(dstr)/(10.0**dec)
results=[]
for i,l in enumerate(lines,1):
    if l.startswith(' 34S  cG RI$weighted average'):
        j=i-2
        while j>=0 and not is_dataG(lines[j]): j-=1
        g=lines[j]
        rif=g[22:29].strip(); drif=g[29:31].strip()
        block=l
        k=i
        while k<len(lines) and is_cont(lines[k]):
            block+=' '+lines[k].strip(); k+=1
        text=block
        items=[]
        for m in re.finditer(r'(\d+\.?\d*)\s*\{I\+(\d+)-(\d+)\}', text):
            items.append((float(m.group(1)),unc_from(m.group(1),m.group(2)),unc_from(m.group(1),m.group(3))))
        for m in re.finditer(r'(\d+\.?\d*)\s*\{I(\d+)\}', text):
            items.append((float(m.group(1)),unc_from(m.group(1),m.group(2)),None))
        results.append((j+1,g[9:19].strip(),rif,drif,text,items))
print('n=',len(results))
for (ln,E,rif,drif,text,items) in results:
    n=len(items)
    if n==0: print(f'L{ln} E={E} NO ITEMS: {text!r}'); continue
    sw=0.0; swx=0.0
    sigs=[]
    for (v,s,sa) in items:
        sig=s if sa is None else (s+sa)/2.0
        sigs.append(sig); w=1.0/(sig*sig); sw+=w; swx+=w*v
    mean=swx/sw; sig_int=1.0/math.sqrt(sw)
    chi2=sum((1.0/(sigs[t]**2))*(items[t][0]-mean)**2 for t in range(n))
    chi2r=chi2/(n-1) if n>1 else 0.0
    sig=sig_int*math.sqrt(chi2r) if (n>1 and chi2r>1) else sig_int
    print(f'L{ln} E={E} field={rif}({drif}) n={n} mean={mean:.3f} sigInt={sig_int:.3f} chi2r={chi2r:.3f} sig={sig:.3f} diff={abs(mean-float(rif)):.3f}')
    print('     raw:',text.replace("$","$ ")[:160])
