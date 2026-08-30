import subprocess, re

PY = r'C:\Users\sun\AppData\Local\Programs\Python\Python311\python.exe'
AVG = r'd:\X\ND\ENSDF\.github\scripts\Java_Average.py'
ENS = r'd:\X\ND\ENSDF\A34\S34\new\S34_33s_d_p.ens'

# parse current file: map level -> (E, DE)
t = open(ENS, encoding='utf-8', newline='').read().replace('\r\n', '\n')
ls = t.split('\n')
levels = {}
for x in ls:
    if x.startswith(' 34S   L '):
        levels[x[9:19].strip()] = x[19:21].strip()

# weighted-average comments: find level that precedes each comment
cur = None
wavg = []  # (level, comment)
for x in ls:
    if x.startswith(' 34S   L '):
        cur = x[9:19].strip()
    elif 'weighted average of:' in x:
        wavg.append((cur, x))

print(f'weighted-average levels in file: {len(wavg)}')
print(f"{'level':8} {'file(E DE)':12} {'java':14} {'method':14} match")
allok = True
for lev, comment in wavg:
    fe, fde = lev, levels.get(lev, '?')
    # extract input pairs from comment
    pairs = re.findall(r'(\d+\.?\d*)\s*\{I(\d+)\}\s*\((\d{4}[A-Za-z]{2}\d{2})\)', comment)
    args = []
    for v, u, ref in pairs:
        args += [v, u]
    r = subprocess.run([PY, AVG] + args, capture_output=True, text=True)
    out = r.stdout + r.stderr
    m = re.search(r'suggested adopted result:\s*([\d.]+)\((\d+)\)', out)
    meth = re.search(r'\((Weighted-Of-All|Unweighted[^)]*)\)', out)
    if not m:
        print(f'  {lev:8} {fe+" "+fde:12} ??? no result')
        continue
    cv, cu = m.group(1), m.group(2)
    # normalize decimal compare
    def norm(val, unc):
        v = float(val)
        return v, int(unc)
    fv = float(fe); cw = float(cv)
    tol = 10**(-len(cv.split('.')[-1])) if '.' in cv else 1.0
    same_val = abs(fv - cw) <= tol
    same_unc = (fde == cu) or (fde == str(int(cu)))
    ok = same_val and same_unc
    allok = allok and ok
    print(f'  {lev:8} {fe+" "+fde:12} {cv+"("+cu+")":14} {(meth.group(1) if meth else "?"):14} {"OK" if ok else "MISMATCH"}')
print()
print('ALL MATCH:', allok)
