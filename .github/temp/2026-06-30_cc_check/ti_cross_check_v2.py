"""
TI Cross-Check v2: Table III (source MD) vs ENSDF E-records (target)
Fixed scientific notation parsing. Generates markdown report.
"""
import re, random, os

BASE = 'XUNDL/2026OSAA_CT11035_152Gd'

# ====== PARSE TABLE III ======
md = open(BASE + '_Table_III.md', encoding='utf-8').read().splitlines()
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
        """Parse value(uncertainty) from Table III cell, handling LaTeX and scientific notation."""
        s = s.strip().replace('$','')
        if not s: return (None, None)
        # Replace unicode
        s = s.replace('\u00d7','x').replace('\u2212','-').replace('\u2013','-').replace('\u2014','-')
        # Handle LaTeX \times 10^{n} -> E+n notation
        s = re.sub(r'\\times\s*10\s*\^\s*\{\s*([\-\d]+)\s*\}', r'E\1', s)
        # Handle ×10^n or x10^n with optional ^ (must have x/× prefix to avoid false matches)
        s = re.sub(r'[xX]\s*10\s*\^*\s*([\-\d]+)', r'E\1', s)
        # Now there should be no ×10 patterns left. Parse value(uncertainty).
        m = re.match(r'([\d\.Ee\-\+]+)\s*\(\s*([\d\.]+)\s*\)', s)
        if m: return (m.group(1), m.group(2))
        m = re.match(r'([\d\.Ee\-\+]+)', s)
        if m: return (m.group(1), '')
        return (None, None)
    
    ti_val, ti_unc = parse_vu(ti_raw)
    src.append({'ei': ei, 'jpi': jpi, 'ti_val': ti_val, 'ti_unc': ti_unc, 'ti_raw': ti_raw})

print('Source (T3) rows: {}'.format(len(src)))

# ====== PARSE ENSDF E-records ======
ens = open(BASE + '.ens', encoding='utf-8').read().splitlines()
tgt = []
cur_ei = None
for ln, line in enumerate(ens, 1):
    if len(line) < 10: continue
    if line[5] == ' ' and line[6] == ' ' and line[7] == 'L':
        cur_ei = line[9:19].strip()
        continue
    if line[5] == ' ' and line[6] == ' ' and line[7] == 'E':
        ib = line[22:29].strip()
        dib = line[29:31].strip()
        ie = line[31:39].strip()
        die = line[39:41].strip()
        ti = line[64:74].strip()
        dti = line[74:76].strip()
        tgt.append({'ei': cur_ei, 'ib': ib, 'dib': dib, 'ie': ie, 'die': die,
                     'ti': ti, 'dti': dti, 'ln': ln})

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

def fmt_ti(val, unc):
    """Format TI value with uncertainty for display."""
    if val is None: return '?'
    s = str(val)
    if unc:
        return '{}({})'.format(s, unc)
    return s

# ====== CROSS-CHECK ======
report_rows = []
val_m = 0; unc_m = 0; dp_m = 0; full_match = 0; no_match = 0

for si, s in enumerate(src):
    found = False
    for t in tgt:
        if match_ei(s['ei'], t['ei']):
            found = True
            issues = []
            sv, su = s['ti_val'], s['ti_unc']
            tv, tu = t['ti'], t['dti']
            
            # Value check
            nsv, ntv = nv(sv), nv(tv)
            if nsv is not None and ntv is not None:
                if abs(ntv) > 1e-30:
                    rd = abs(nsv-ntv)/abs(ntv)
                else:
                    rd = abs(nsv-ntv)
                if rd > 0.005:
                    issues.append('VAL')
                    val_m += 1
            elif sv != tv:
                issues.append('VAL')
                val_m += 1
            
            # Uncertainty check
            su_clean = su.strip() if su else ''
            tu_clean = tu.strip() if tu else ''
            if su_clean and tu_clean and su_clean != tu_clean:
                issues.append('UNC')
                unc_m += 1
            elif su_clean and not tu_clean:
                issues.append('UNC')
                unc_m += 1
            elif not su_clean and tu_clean:
                issues.append('UNC')
                unc_m += 1
            
            # Decimal places
            sd = decimals(sv) if sv else 0
            td = decimals(tv) if tv else 0
            if sd != td:
                issues.append('DP')
                dp_m += 1
            
            status = 'MATCH' if not issues else ','.join(issues)
            if status == 'MATCH':
                full_match += 1
            
            report_rows.append({
                'idx': si+1, 'ei': s['ei'], 'jpi': s['jpi'],
                'src_ti': sv, 'src_unc': su,
                'tgt_ti': tv, 'tgt_unc': tu,
                'status': status, 'ln': t['ln'],
                'src_raw': s['ti_raw']
            })
            break
    if not found:
        no_match += 1
        report_rows.append({
            'idx': si+1, 'ei': s['ei'], 'jpi': s['jpi'],
            'src_ti': s['ti_val'], 'src_unc': s['ti_unc'],
            'tgt_ti': None, 'tgt_unc': None,
            'status': 'NO_MATCH', 'ln': 0,
            'src_raw': s['ti_raw']
        })

print('\n=== SUMMARY ===')
print('Full MATCH: {}'.format(full_match))
print('Value mismatches: {}'.format(val_m))
print('Uncertainty mismatches: {}'.format(unc_m))
print('Decimal place mismatches: {}'.format(dp_m))
print('No-match source: {}'.format(no_match))

# ====== 15% SPOT CHECK ======
print('\n=== 15% SPOT CHECK ===')
matched = [r for r in report_rows if r['status'] == 'MATCH']
random.seed(20260701180)
k = max(1, (15*len(matched)+99)//100)
sample = random.sample(matched, min(k, len(matched)))
spot_fail = 0
for r in sample:
    sv, su = r['src_ti'], r['src_unc']
    tv, tu = r['tgt_ti'], r['tgt_unc']
    ok = True
    nsv, ntv = nv(sv), nv(tv)
    if nsv is not None and ntv is not None:
        if abs(ntv) > 1e-30 and abs(nsv-ntv)/abs(ntv) > 0.005:
            ok = False
    elif sv != tv:
        ok = False
    su_clean = su.strip() if su else ''
    tu_clean = tu.strip() if tu else ''
    if su_clean and tu_clean and su_clean != tu_clean:
        ok = False
    if not ok:
        spot_fail += 1
        print('  FAIL: Ei={}, src={}({}) vs tgt={}({})'.format(r['ei'], sv, su, tv, tu))
print('Seed: 20260701180, Sample: {}, Failures: {}'.format(len(sample), spot_fail))

# ====== MARKDOWN REPORT ======
md_report = []
md_report.append('# TI Cross-Check: Table III (MD) vs ENSDF E-records (ENS)')
md_report.append('')
md_report.append('## Task Configuration')
md_report.append('')
md_report.append('- Source: `XUNDL/2026OSAA_CT11035_152Gd_Table_III.md`')
md_report.append('- Target: `XUNDL/2026OSAA_CT11035_152Gd.ens`')
md_report.append('- Field mapping: MD $I_{tot}$ column → ENSDF E-record TI (col 65-74), DTI (col 75-76)')
md_report.append('- Matching: parent level energy within ±0.5 keV')
md_report.append('- Tolerance: 0.5% relative difference for TI value match')
md_report.append('- Spot-check: 15% random sample, seed=20260701180')
md_report.append('')
md_report.append('## Summary')
md_report.append('')
md_report.append('| Category | Count |')
md_report.append('| :--- | :--- |')
md_report.append('| Total source rows (T3) | {} |'.format(len(src)))
md_report.append('| Total target E-records (ENS) | {} |'.format(len(tgt)))
md_report.append('| Full MATCH | {} |'.format(full_match))
md_report.append('| TI Value mismatches | {} |'.format(val_m))
md_report.append('| DTI Uncertainty mismatches | {} |'.format(unc_m))
md_report.append('| Decimal place mismatches | {} |'.format(dp_m))
md_report.append('| No-match source rows | {} |'.format(no_match))
md_report.append('| 15% Spot-check failures | {}/{} |'.format(spot_fail, len(sample)))
md_report.append('')

# Mismatch details
mismatches = [r for r in report_rows if r['status'] != 'MATCH']
if mismatches:
    md_report.append('## Mismatch Details')
    md_report.append('')
    md_report.append('| # | E_x (keV) | J^π | T3 $I_{tot}$ | ENS TI | ENS DTI | Issues |')
    md_report.append('| :--- | :--- | :--- | :--- | :--- | :--- | :--- |')
    for r in mismatches:
        src_disp = fmt_ti(r['src_ti'], r['src_unc'])
        tgt_disp = r['tgt_ti'] if r['tgt_ti'] else '—'
        tgt_unc_disp = r['tgt_unc'] if r['tgt_unc'] else '—'
        md_report.append('| {} | {} | {} | {} | {} | {} | {} |'.format(
            r['idx'], r['ei'], r['jpi'], src_disp, tgt_disp, tgt_unc_disp, r['status']))

# Write report
report_path = BASE + '_TI_cross_check.md'
with open(report_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(md_report))
print('\nReport written to: {}'.format(report_path))
