import re, math
data=open(r'd:\X\ND\ENSDF\A34\S34\new\S34_31p_a_pg.ens',encoding='utf-8-sig',newline='').read()
lines=data.split('\r\n')
if lines and lines[-1]=='': lines=lines[:-1]
def is_cG(l): return len(l)>8 and l[6:7]=='c' and l[7:8]=='G'
def is_cont(l): return len(l)>8 and l[6:7]!=' ' and l[7:8]=='G' and l[6:7] in '23456789' and l[6:7].isdigit()
def is_dataG(l): return len(l)==80 and l[5:6]==' ' and l[6:7]!='c' and l[7:8]=='G'

def parse_Iunc(s):
    # returns absolute sigma for value string & {In}
    pass

val_re=re.compile(r'(\d+\.?\d*)\s*\{I\+?(\d+)-(\d+)\}|\{I(\d+)\}|(\d+\.?\d*)\s*\{I(\d+)\}')
# simpler two patterns

def extract_vals(text):
    vals=[]
    # asym
    for m in re.finditer(r'(\d+\.?\d*)\s*\{I\+(\d+)-(\d+)\}', text):
        v=float(m.group(1)); 
        # uncertainty in last digit: need decimal place. use string
        vals.append((m.group(1), m.group(2), m.group(3)))
    for m in re.finditer(r'(\d+\.?\d*)\s*\{I(\d+)\}', text):
        vals.append((m.group(1), m.group(2), m.group(2)))
    return vals

def unc_from(vstr, dstr):
    # d = uncertainty in last digits of vstr
    if '.' in vstr:
        dec=len(vstr.split('.')[1])
    else:
        dec=0
    return int(dstr)/ (10.0**dec)

results=[]
for i,l in enumerate(lines,1):
    if l.startswith(' 34S  cG RI$weighted average'):
        j=i-2
        while j>=0 and not is_dataG(lines[j]): j-=1
        g=lines[j]
        ri_txt=g[22:29].strip(); dri_txt=g[29:31].strip()
        # collect text: first cG line + its continuations (2cG..)
        block=l
        k=i  # next index
        while k<len(lines) and is_cont(lines[k]):
            block += ' '+lines[k].strip(); k+=1
        text=block
        # strip trailing '.' 
        pairs=extract_vals(text)
        # determine unit scaling: if value has decimal places they differ per item but usually same scale; compute sigma via vstr decimals
        items=[]
        # re-extract with decimals properly
        for m in re.finditer(r'(\d+\.?\d*)\s*\{I\+(\d+)-(\d+)\}', text):
            v=float(m.group(1)); items.append((v,unc_from(m.group(1),m.group(2)),unc_from(m.group(1),m.group(3))))
        for m in re.finditer(r'(\d+\.?\d*)\s*\{I(\d+)\}', text):
            v=float(m.group(1)); items.append((v,unc_from(m.group(1),m.group(2)),None))
        # dedupe? none
        results.append((j+1,g[9:19].strip(),ri_txt,dri_txt,text,items))
print('n weighted avg comments:',len(results))
def fmt_num(x):
    # format to match field int-ish
    return x

for (ln,E,rif,drif,text,items) in results:
    n=len(items)
    if n==0:
        print(f'L{ln} E={E} NO ITEMS parsed: {text}'); continue
    # weighted mean of items using first sigma (sym)
    sw=0.0; swx=0.0
    for (v,s,sa) in items:
        sig=s if sa is None else (s+sa)/2.0
        w=1.0/(sig*sig); sw+=w; swx+=w*v
    mean=swx/sw
    sig_int=1.0/math.sqrt(sw)
    chi2=sum((1.0/((s if sa is None else (s+sa)/2.0)**2))*(v-mean)**2 for (v,s,sa) in items)
    if n>1:
        chi2r=chi2/(n-1)
    else:
        chi2r=0
    sig=sig_int*math.sqrt(chi2r) if (n>1 and chi2r>1) else sig_int
    # round like ENSDF: 2 sig figs if leading 10-34 else 1; here uncertainty given field DRI
    print(f'L{ln} E={E} field={rif}({drif}) items={[(v,s) for (v,s,_) in items]}')
    print(f'    mean={mean:.3f} sig_int={sig_int:.3f} chi2r={chi2r:.3f} sig_used={sig:.3f}')
    # compare to field
    rf=float(rif); df=float(drif) if drif not in ('LT','GT','LE','GE','') else None
    diff=abs(mean-rf)
    print(f'    |mean-field|={diff:.3f} (allow ~ <= max(sig_used,df, rounding0.5*fielddec))')
