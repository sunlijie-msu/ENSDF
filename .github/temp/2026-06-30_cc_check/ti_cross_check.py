"""
TI Cross-Check: Table III (source MD) vs ENSDF E-records (target)
Matches level energy within 0.5 keV, checks TI value, uncertainty, decimal places.
"""
import re, random

# ====== PARSE TABLE III (Source) ======
md = open('XUNDL/2026OSAA_CT11035_152Gd_Table_III.md', encoding='utf-8').read().splitlines()
src = []
for line in md:
    s = line.strip()
    if not s.startswith('|'): continue
    cells = [c.strip() for c in s.strip('|').split('|')]
    if len(cells) < 6: continue
    if cells[0].startswith('$E_x$'): continue
    if re.fullmatch(r'[-:\s]*', ''.join(cells)): continue
    
    ei_m = re.match(r'([\d\.]+)', cells[0])
    ei = ei_m.group(1) if ei_m else ''
    jpi = cells[1]
    ti_raw = cells[4]
    
    def parse_vu(s):
        s = s.strip()
        if not s: return (None, None)
        s = s.replace('$','').replace('\\times','').replace('\\','').replace('{','').replace('}','')
        s = s.replace('\u00d7','').replace('\u2212','-')
        s = re.sub(r'10\s*\^\s*([\-\d]+)', r'E\1', s)
        s = re.sub(r'10\s*([\-\d]+)', r'E\1', s)
        s = re.sub(r'(\d)\s*[xX]\s*10\^?([\-\d]+)', r'\1E\2', s)
        m = re.match(r'([\d\.Ee\-\+]+)\s*\(([\d\.]+)\)', s)
        if m: return (m.group(1), m.group(2))
        m = re.match(r'([\d\.Ee\-\+]+)', s)
        if m: return (m.group(1), '')
        return (None, None)
    
    ti_val, ti_unc = parse_vu(ti_raw)
    src.append({'ei': ei, 'jpi': jpi, 'ti_val': ti_val, 'ti_unc': ti_unc, 'ti_raw': ti_raw})

print('Source (T3) rows: {}'.format(len(src)))

# ====== PARSE ENSDF E-records ======
ens = open('XUNDL/2026OSAA_CT11035_152Gd.ens', encoding='utf-8').read().splitlines()
tgt = []
cur_ei = None
for ln, line in enumerate(ens, 1):
    if len(line) < 10: continue
    if line[5] == ' ' and line[6] == ' ' and line[7] == 'L':
        cur_ei = line[9:19].strip()
        continue
    if line[5] == ' ' and line[6] == ' ' and line[7] == 'E':
        ti = line[64:74].strip()
        dti = line[74:76].strip()
        tgt.append({'ei': cur_ei, 'ti': ti, 'dti': dti, 'ln': ln})

print('Target (ENS) E-records: {}'.format(len(tgt)))

# ====== UTILITIES ======
def match_ei(e1, e2):
    try: return abs(float(e1) - float(e2)) < 0.5
    except: return False

def nv(s):
    if not s: return None
    try: return float(s.replace('E','e').replace('e','e'))
    except: return None

def decimals(s):
    s = s.strip()
    if 'E' in s or 'e' in s:
        m = re.match(r'([\d\.]+)[Ee]', s)
        if m: s = m.group(1)
    if '.' in s: return len(s.split('.')[1])
    return 0

# ====== CROSS-CHECK ======
report = []
val_m = 0; unc_m = 0; dp_m = 0; full_match = 0; no_match_src = 0

for si, s in enumerate(src):
    found = False
    for t in tgt:
        if match_ei(s['ei'], t['ei']):
            found = True
            issues = []
            sv, su = s['ti_val'], s['ti_unc']
            tv, tu = t['ti'], t['dti']
            
            nsv, ntv = nv(sv), nv(tv)
            if nsv and ntv:
                if abs(ntv) > 1e-30:
                    rd = abs(nsv-ntv)/abs(ntv)
                else:
                    rd = abs(nsv-ntv)
                if rd > 0.005:
                    issues.append('VALUE: src={} tgt={}'.format(sv, tv))
                    val_m += 1
            elif sv != tv:
                issues.append('VALUE_STR: src={} tgt={}'.format(sv, tv))
                val_m += 1
            
            if su and tu and su != tu:
                issues.append('UNC: src={} tgt={}'.format(su, tu))
                unc_m += 1
            elif su and not tu:
                issues.append('UNC_MISS: src has unc={}'.format(su))
                unc_m += 1
            elif not su and tu:
                issues.append('UNC_EXTRA: tgt has unc={}'.format(tu))
                unc_m += 1
            
            sd = decimals(sv) if sv else 0
            td = decimals(tv) if tv else 0
            if sd != td:
                issues.append('DEC_PLACES: src={}dp tgt={}dp'.format(sd, td))
                dp_m += 1
            
            status = 'MATCH' if not issues else '; '.join(issues)
            report.append((si+1, s, t, status))
            if not issues:
                full_match += 1
            break
    if not found:
        no_match_src += 1
        report.append((si+1, s, None, 'NO_MATCH'))

print('\n=== CROSS-CHECK SUMMARY ===')
print('Full MATCH: {}'.format(full_match))
print('Value mismatches: {}'.format(val_m))
print('Uncertainty mismatches: {}'.format(unc_m))
print('Decimal place mismatches: {}'.format(dp_m))
print('No-match source: {}'.format(no_match_src))

# ====== DETAILED MISMATCHES ======
print('\n=== MISMATCH DETAILS ===')
mismatches = [r for r in report if r[3] != 'MATCH']
if mismatches:
    for idx, s, t, status in mismatches:
        if t:
            print('  #{}: Ei={}, Src={}, Tgt TI={}, DTI={}, Ln={}'.format(idx, s['ei'], s['ti_raw'], t['ti'], t['dti'], t['ln']))
            print('       {}'.format(status))
        else:
            print('  #{}: Ei={}, NO_MATCH'.format(idx, s['ei']))
else:
    print('  None. All TI values match perfectly.')

# ====== 15% SPOT CHECK ======
print('\n=== 15% SPOT CHECK ===')
matched_pairs = [(s,t) for _,s,t,st in report if t and st == 'MATCH']
random.seed(20260701150)
k = max(1, (15*len(matched_pairs)+99)//100)
sample = random.sample(matched_pairs, min(k, len(matched_pairs)))
spot_fail = 0
for s, t in sample:
    sv, su = s['ti_val'], s['ti_unc']
    tv, tu = t['ti'], t['dti']
    ok = True
    nsv, ntv = nv(sv), nv(tv)
    if nsv and ntv:
        if abs(ntv) > 1e-30 and abs(nsv-ntv)/abs(ntv) > 0.005:
            ok = False
    elif sv != tv:
        ok = False
    if su and tu and su != tu:
        ok = False
    if not ok:
        spot_fail += 1
        print('  FAIL: Ei={}, src={}({}) vs tgt={}({})'.format(s['ei'], sv, su, tv, tu))
print('Sample: {}, Failures: {}, Seed: 20260701150'.format(len(sample), spot_fail))
