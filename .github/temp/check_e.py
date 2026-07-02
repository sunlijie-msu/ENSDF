lines = open('XUNDL/2026OSAA_CT11035_152Gd.ens', 'r').readlines()
cur = ''
for i, ln in enumerate(lines):
    if len(ln) < 76: continue
    if ln[5:8] == '  L':
        cur = ln[9:19].strip()
    if ln[5:8] == '  E' and cur in ['755.55', '1048.08']:
        ib = ln[22:29].strip()
        ie = ln[31:39].strip()
        ti = ln[64:74].strip()
        dti = ln[74:76].strip()
        print('E={} IB={} IE={} TI={} DTI={} Ln={}'.format(cur, ib, ie, ti, dti, i+1))
