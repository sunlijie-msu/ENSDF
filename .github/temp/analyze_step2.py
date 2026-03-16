"""
Analyze Step 2: Map 1971HY02.ens RI data to Cl34_33s_p_g.ens G-records.
ENSDF format: col6=CONT, col7=BLANK(data) or 'c'(comment), col8=TYPE.
Data G-record: col7=blank. cG comment: col7='c'.
"""

# Parse 1971HY02.ens
hy02 = {}
with open(r'A34\Cl34\raw\1971HY02.ens') as f:
    lines = [l.rstrip('\n') for l in f.readlines()]
ei = None
for line in lines:
    if len(line) < 8: continue
    if line[5]==' ' and line[6]==' ' and line[7]=='L':
        try: ei = float(line[9:19].strip())
        except: ei = None
    elif line[5]==' ' and line[6]==' ' and line[7]=='G' and ei is not None:
        eg_str = line[9:19].strip()
        ri = line[22:29].strip()
        dri = line[29:31].strip()
        try: hy02[(ei, float(eg_str))] = {'ri': ri, 'dri': dri, 'eg_str': eg_str}
        except: pass
print(f'1971HY02: {len(hy02)} G-records')

# Parse Cl34_33s_p_g.ens
with open(r'A34\Cl34\new\Cl34_33s_p_g.ens') as f:
    src = [l.rstrip('\n') for l in f.readlines()]
print(f'Src file: {len(src)} lines')

src_map = {}
ei = None
last_g_key = None
for i, line in enumerate(src):
    if len(line) < 8: continue
    c6,c7,c8 = line[5],line[6],line[7]
    if c6==' ' and c7==' ' and c8=='L':
        try: ei = float(line[9:19].strip())
        except: ei = None
        last_g_key = None
    elif c6==' ' and c7==' ' and c8=='G' and ei is not None:
        eg_str = line[9:19].strip()
        try:
            eg = float(eg_str)
            key = (ei, eg)
            src_map[key] = {'lineno': i+1, 'eg_str': eg_str, 'cg_ri_lines': []}
            last_g_key = key
        except: pass
    elif c7=='c' and c8=='G' and last_g_key is not None:
        body = line[8:]
        if 'RI$' in body:
            src_map[last_g_key]['cg_ri_lines'].append((i+1, line))
    elif c6.isdigit() and c7=='c' and c8=='G' and last_g_key is not None:
        body = line[8:]
        if 'RI$' in body:
            src_map[last_g_key]['cg_ri_lines'].append((i+1, line))
print(f'Src G-records: {len(src_map)}')

# Match and report
found, notfound, need_avg, add_only = 0, 0, 0, 0
na_list = []
for key in sorted(hy02.keys()):
    ei_k, eg_k = key
    v = hy02[key]
    ri, dri = v['ri'], v['dri']
    if dri == 'LT': cat = 'LT'
    elif dri == '': cat = 'NO_DRI'
    else: cat = 'NEED_AVG'
    
    match = None
    best_diff = 9999
    for sk in src_map:
        if abs(sk[0]-ei_k)<0.1:
            diff = abs(sk[1]-eg_k)
            if diff < 2.0 and diff < best_diff:
                best_diff = diff
                match = sk
    
    if match:
        found += 1
        sm = src_map[match]
        existing = sm['cg_ri_lines']
        if cat=='NEED_AVG': need_avg+=1; na_list.append((key,match,sm,v))
        else: add_only+=1
        print(f'MATCH  Ei={ei_k:8.2f} Eg={eg_k:9.4f}  RI={ri:<8} DRI=[{dri:<2}]  cat={cat}  srcL={sm["lineno"]}')
        for lno,ltxt in existing:
            print(f'  existing cG RI$ L{lno}: {ltxt.strip()[:90]}')
    else:
        notfound += 1
        print(f'MISS   Ei={ei_k:8.2f} Eg={eg_k:9.4f}  RI={ri:<8} DRI=[{dri:<2}]  cat={cat}')

print(f'\nSUMMARY: found={found}, notfound={notfound}, need_avg={need_avg}, add_only={add_only}')
