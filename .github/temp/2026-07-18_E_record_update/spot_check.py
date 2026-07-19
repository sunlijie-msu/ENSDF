"""15% spot-check: E-records vs Table III."""
import re, random
random.seed(20260718)

t3 = {}
with open('d:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd_Table_III.md','r',encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line.startswith('|') or '---' in line or 'TABLE' in line: continue
        parts = [p.strip() for p in line.split('|')]
        if len(parts)<8: continue
        ex=parts[1]; ib=parts[3]; ie=parts[4]; it=parts[5]
        m = re.match(r'([\d.]+)', ex)
        if m: t3[round(float(m.group(1)))] = (ex, ib, ie, it)

ensdf = {}
with open('d:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd.ens','r',encoding='utf-8') as f:
    lines = f.readlines()
cur = None
for i,l in enumerate(lines):
    if len(l)>=9 and l[5:6]==' ' and l[6:7]==' ' and l[7:8]=='L':
        e = l[9:19].strip()
        if e:
            try: cur = round(float(e))
            except: pass
    if len(l)>=9 and l[5:6]==' ' and l[6:7]==' ' and l[7:8]=='E':
        if cur is not None:
            ensdf[cur] = (l[22:29].strip(), l[31:39].strip(), l[64:74].strip(), i+1)

common = sorted(set(t3.keys()) & set(ensdf.keys()))
sample = random.sample(common, min(30, len(common)))
sample.sort()

def clean(v):
    return v.replace('*10','E').replace(u'\u2212','-').replace('(',' ').replace(')','').split()[0]

def pct_diff(a,b):
    if abs(a)+abs(b) < 1e-30: return 0
    return abs(a-b)/(abs(a)+abs(b)+1e-30)*200

print("SPOT-CHECK (15% of matched E-records):")
print("{:>5s}  {:>10s}  {:>10s}  {:>10s}  {:>10s}".format("Key","T3 IB","ENS IB","T3 IE","ENS IE"))
print("-"*55)
ok=0; bad=0
for key in sample:
    ex,ib,ie,it = t3[key]
    ibf,ief,itf,ln = ensdf[key]
    issues = []
    # Check IE (most important — present for all entries)
    if ie and ief:
        try:
            tv=float(clean(ie)); ev=float(ief)
            if pct_diff(tv,ev)>5:
                issues.append("IE:{}vs{}".format(ie,ief))
        except: issues.append("IE_parse")
    # Check TI
    if it and itf:
        try:
            tv=float(clean(it)); ev=float(itf.replace('E','e'))
            if pct_diff(tv,ev)>5:
                issues.append("TI:{}vs{}".format(it,itf))
        except: issues.append("TI_parse")
    # Check IB if present
    if ib and ibf:
        try:
            tv=float(clean(ib)); ev=float(ibf.replace('E','e'))
            if pct_diff(tv,ev)>5:
                issues.append("IB:{}vs{}".format(ib,ibf))
        except: issues.append("IB_parse")
    if issues:
        bad+=1
        print("{:5d}  {:>10s}  {:>10s}  {:>10s}  {:>10s}  FAIL: {}".format(key,ib[:10],ibf[:10],ie[:10],ief[:10],"; ".join(issues)))
    else:
        ok+=1

print("\nSpot-check: {} OK, {} FAIL out of {}".format(ok, bad, len(sample)))
