import re, math
data=open(r'd:\X\ND\ENSDF\A34\S34\new\S34_31p_a_pg.ens',encoding='utf-8-sig',newline='').read()
lines=data.split('\r\n')
if lines and lines[-1]=='': lines=lines[:-1]
def is_cont(l): return len(l)>8 and l[6:7]=='c' and l[7:8]=='G' and l[5:6].isdigit()
def is_dataG(l): return len(l)==80 and l[5:6]==' ' and l[6:7]!='c' and l[7:8]=='G'
def unc_from(vstr,dstr):
    dec=len(vstr.split('.')[1]) if '.' in vstr else 0
    return int(dstr)/(10.0**dec)
for i,l in enumerate(lines,1):
    if l.startswith(' 34S  cG RI$weighted average'):
        j=i-2
        while j>=0 and not is_dataG(lines[j]): j-=1
        g=lines[j]; rif=g[22:29].strip(); drif=g[29:31].strip()
        txt=l[9:]
        k=i
        while k<len(lines) and is_cont(lines[k]):
            txt+=' '+lines[k][9:].strip(); k+=1
        items=[]
        for m in re.finditer(r'(\d+\.?\d*)\s*\{I\+(\d+)-(\d+)\}',txt):
            items.append((float(m.group(1)),unc_from(m.group(1),m.group(2)),unc_from(m.group(1),m.group(3))))
        for m in re.finditer(r'(\d+\.?\d*)\s*\{I(\d+)\}',txt):
            items.append((float(m.group(1)),unc_from(m.group(1),m.group(2)),None))
        n=len(items)
        if n==0: print(f'L{j+1} E={g[9:19].strip():>8} field={rif}({drif}) NO ITEMS: {txt!r}'); continue
        sw=swx=0.0; sigs=[]
        for (v,s,sa) in items:
            sig=s if sa is None else (s+sa)/2.0; sigs.append(sig); w=1/(sig*sig); sw+=w; swx+=w*v
        mean=swx/sw; si=1/math.sqrt(sw)
        chi2=sum((items[t][0]-mean)**2/(sigs[t]**2) for t in range(n))
        c2r=chi2/(n-1) if n>1 else 0
        sig=si*math.sqrt(c2r) if n>1 and c2r>1 else si
        print(f'L{j+1} E={g[9:19].strip():>8} field={rif}({drif}) n={n} mean={mean:.4f} si={si:.3f} c2r={c2r:.3f} sig={sig:.3f} |d|={abs(mean-float(rif)):.3f}')
        print('     ', txt.strip())
