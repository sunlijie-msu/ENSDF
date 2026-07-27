"""15% spot check for resonance data."""
import re, random
random.seed(42)

with open(r'A34\S34\raw\2018MuZY_34S.md','r',encoding='utf-8') as f: md=f.read()
with open(r'A34\S34\new\S34_n_g_n_n_resonances.ens','r') as f: ens=f.read()

md_data = {}
for line in md.split('\n'):
    if not line.strip().startswith('|') or '---' in line: continue
    cells = [c.strip() for c in line.split('|')]
    if cells and cells[0]=='': cells=cells[1:]
    if cells and cells[-1]=='': cells=cells[:-1]
    if len(cells)<3: continue
    e0s = re.sub(r'[\$\^a-z\*]','',cells[0]).strip()
    if e0s in ('','-','—'): continue
    try:
        e0=float(e0s)
        md_data[e0] = {'j':cells[1],'l':cells[2],'G':cells[3],'Gn':cells[4],
                       'Gg':cells[5],'ggn':cells[8],'Ga':cells[9]}
    except: pass

ens_data = {}
cur_s = None; cur_s_f = None
for line in ens.split('\n'):
    if len(line)>70 and line[7]=='L' and line[8]==' ' and line[6]!='c':
        cur_s = line[64:74].strip()
        try: cur_s_f = float(cur_s)
        except: cur_s_f = None; cur_s = None
        if cur_s_f: ens_data[cur_s_f] = {'j':line[22:39].strip(),'l':line[55:64].strip(),
                                          'T':line[39:49].strip(),'cL':[]}
    if cur_s_f is not None and len(line)>7 and line[6]=='c' and line[7]=='L':
        ens_data[cur_s_f]['cL'].append(line.rstrip())

keys = sorted([k for k in md_data if k in ens_data])
picked = random.sample(keys, min(7,len(keys)))

print('Spot check (15% = 7/44):')
for e0 in sorted(picked):
    m = md_data[e0]; e = ens_data[e0]
    cl_text = ' | '.join(e['cL'])
    
    errors = []
    mj = m['j'].replace(' ','').replace('$','').replace('\\','').replace('\u2265','GE')
    ej = e['j'].replace(' ','').rstrip('+-')
    if mj and ej and mj != ej:
        errors.append('J: MD=' + m['j'] + ' vs ENS=' + e['j'])
    
    ml = m['l'].strip('()'); el = e['l'].strip('()')
    if ml and el and ml != el:
        errors.append('L: MD=' + m['l'] + ' vs ENS=' + e['l'])
    
    for field, md_key, ens_pat in [
        ('Gn','Gn',r'\|G\{-n\}\s*=\s*([\d.]+)'),
        ('Gg','Gg',r'\|G\|g\s*=\s*([\d.]+)'),
        ('ggn','ggn',r'g\|G.*?/\|G\s*=\s*([\d.]+)'),
        ('Ga','Ga',r'\|G\{-\|a\}\s*=\s*([\d.]+)'),
    ]:
        md_val = m[md_key]
        if md_val and md_val not in ('','-'):
            m2 = re.match(r'([\d.]+)', md_val.replace('(',' ').replace(')',''))
            if m2:
                mdv = float(m2.group(1))
                pm = re.search(ens_pat, cl_text)
                if pm:
                    ensv = float(pm.group(1))
                    if abs(mdv-ensv) > max(mdv,ensv)*0.015:
                        errors.append(field + ': MD=' + str(md_val) + ' vs ENS=' + str(pm.group(1)))
    
    status = 'OK' if not errors else 'FAIL: ' + '; '.join(errors)
    print('  E0=' + str(e0) + ': ' + status)
