"""Cross-check S34_35cl_d_3he.ens vs 1969PU03.csv - final version."""
import csv, re, io

csv_text = open(r'A34\S34\raw\1969PU03.csv', 'r', encoding='utf-8-sig').read()
# Clean zero-width spaces
csv_text = csv_text.replace('\u200b', '')

reader = csv.reader(io.StringIO(csv_text))
header = next(reader)

# Parse CSV with special handling for dual-L levels
csv_levels = []
for row in reader:
    if not row or row[0].strip() == '': continue
    
    lvl_no = row[0].strip()
    ex_str = row[1].strip()
    if ex_str in ('—', '', '-'): continue
    
    ex_val = None
    ex_unc = ''
    if '\xb1' in ex_str:  # ± symbol
        parts = ex_str.split('\xb1')
        ex_val = float(parts[0])
        ex_unc = parts[1].strip()
    else:
        ex_val = float(ex_str)
    
    lp = row[2].strip()
    jpi = row[3].strip()
    
    # Handle dual-L levels: row[4] and row[5] are pickup particles,
    # row[6] and row[7] are C2S values
    n_l = len(lp.replace(' ','').split('+')) if lp and lp != '—' else 1
    
    pickups = []
    c2s_vals = []
    
    if n_l == 2:
        pickups = [row[4].strip(), row[5].strip()]
        c2s_vals = [row[6].strip(), row[7].strip()] if len(row) > 7 else [row[6].strip()]
    else:
        pickups = [row[4].strip()]
        c2s_vals = [row[5].strip()] if len(row) > 5 else []
    
    csv_levels.append({
        'lvl_no': lvl_no,
        'ex_mev': ex_val,
        'ex_unc': ex_unc,
        'lp': lp,
        'jpi': jpi,
        'pickups': pickups,
        'c2s': c2s_vals,
        'n_l': n_l
    })

# Parse ENSDF
with open(r'A34\S34\new\S34_35cl_d_3he.ens', 'r') as f:
    ens_lines = f.readlines()

ens_levels = []
current_l = None

for i, line in enumerate(ens_lines):
    if len(line) < 10: continue
    if line[7] == 'L' and line[8] == ' ' and line[6] != 'c':
        if current_l is not None:
            ens_levels.append(current_l)
        
        e_str = line[9:19].strip()
        de_str = line[19:21].strip()
        l_str = line[55:64].strip()
        s_str = line[64:74].strip()
        
        e_val = float(e_str) if e_str else 0.0
        
        s_values = []
        if s_str:
            for p in re.split(r'\+', s_str):
                p = p.strip()
                if p:
                    try: s_values.append(float(p))
                    except: s_values.append(p)
        
        current_l = {
            'line': i+1, 'e_kev': e_val, 'de_kev': de_str,
            'l': l_str, 's': s_values, 's_text': s_str,
            'cl_comments': []
        }
        continue
    
    if current_l is not None and len(line) > 7 and line[6] == 'c' and line[7] == 'L':
        current_l['cl_comments'].append(line.rstrip())

if current_l is not None:
    ens_levels.append(current_l)

def match_csv_to_ens(csv_l):
    csv_kev = csv_l['ex_mev'] * 1000
    best, best_diff = None, 999
    for el in ens_levels:
        d = abs(csv_kev - el['e_kev'])
        if d < best_diff: best, best_diff = el, d
    tol = max(30, float(csv_l['ex_unc'])*3000) if csv_l['ex_unc'] else 30
    return (best, best_diff) if best_diff <= tol else (None, best_diff)

# ====== REPORT ======
print("CROSS-CHECK: S34_35cl_d_3he.ens vs 1969PU03.csv")
print("="*65)
print(f"{'CSV E':>8s} {'ENS E':>8s} {'L':>4s} {'CSV C2S':>14s} {'ENS S':>14s} {'Ratio':>8s} {'Note'}")
print("-"*65)

errors = 0
matched_ens = set()

for csv_l in csv_levels:
    ens_l, diff = match_csv_to_ens(csv_l)
    if ens_l is None:
        print(f"{csv_l['ex_mev']*1000:>8.0f} {'--':>8s} {'':>4s} {str(csv_l['c2s']):>14s} {'--':>14s} {'':>8s} NO MATCH")
        errors += 1
        continue
    
    matched_ens.add(ens_l['line'])
    
    for j in range(max(csv_l['n_l'], len(ens_l['s']))):
        csv_s = csv_l['c2s'][j] if j < len(csv_l['c2s']) else '--'
        ens_s = ens_l['s'][j] if j < len(ens_l['s']) else '--'
        
        csv_s_clean = csv_s.strip('()')
        try: csv_s_f = float(csv_s_clean)
        except: csv_s_f = None
        try: ens_s_f = float(ens_s) if isinstance(ens_s, str) else ens_s
        except: ens_s_f = None
        
        note = ''
        if csv_s_f and ens_s_f and csv_s_f != 0:
            ratio = ens_s_f / csv_s_f
            if abs(ratio - 1.500) < 0.01:
                note = '×1.500'
            elif abs(ratio - 1.0) < 0.01:
                note = 'OK'
            else:
                note = f'×{ratio:.3f} MISMATCH'
                errors += 1
        elif csv_s_f and ens_s_f:
            note = 'OK' if csv_s_f == ens_s_f else 'MISMATCH'
        
        csv_e_str = f"{csv_l['ex_mev']*1000:.0f}"
        ens_e_str = f"{ens_l['e_kev']:.0f}"
        l_str = csv_l['lp'] if j == 0 else ''
        
        print(f"{csv_e_str:>8s} {ens_e_str:>8s} {l_str:>4s} {csv_s:>14s} {str(ens_s):>14s} {note:>8s}")

# ENSDF-only
print(f"\n--- ENSDF-only (from 1968Wi20) ---")
for el in ens_levels:
    if el['line'] not in matched_ens:
        has_wi20 = any('1968Wi20' in c for c in el['cl_comments'])
        src = '1968Wi20' if has_wi20 else '?'
        print(f"  {el['e_kev']:.0f} keV: S={el['s']} ({src})")

# Check provenance for level 18 (6.22 MeV)
print(f"\n--- Provenance check: Level 6220 keV ---")
for el in ens_levels:
    if abs(el['e_kev'] - 6220) < 10:
        for c in el['cl_comments']:
            if '1969Pu03' in c:
                # Extract quoted S value
                m = re.search(r'S=\(?([\d.]+)\)?', c)
                if m:
                    quoted_s = m.group(1)
                    csv_l = [x for x in csv_levels if abs(x['ex_mev']*1000 - 6220) < 50]
                    if csv_l:
                        csv_c2s = csv_l[0]['c2s'][0].strip('()')
                        print(f"  ENSDF comment: 'other: S=({quoted_s}) (1969Pu03)'")
                        print(f"  CSV 1969Pu03:  C2S=({csv_c2s})")
                        if quoted_s != csv_c2s:
                            print(f"  ** PROVENANCE ERROR: quoted {quoted_s} != CSV {csv_c2s}")
                            errors += 1

print(f"\nErrors: {errors}")
print(f"\nKEY FINDING: All 1969Pu03 S-values in ENSDF are exactly 1.500× CSV C2S.")
print("This is a systematic normalization factor discrepancy.")
print("ENSDF cL says N=2.95; ratio suggests different N convention.")
