"""Cross-check S34_35cl_d_3he.ens vs 1969PU03.csv for S-values."""
import csv, re, io

# ====== PARSE CSV ======
csv_text = open(r'A34\S34\raw\1969PU03.csv', 'r', encoding='utf-8-sig').read()
reader = csv.reader(io.StringIO(csv_text))
header = next(reader)
print(f"CSV header: {header}")

csv_levels = []
for row in reader:
    if not row or row[0].strip() == '': continue
    # Columns: Level No., Ex (MeV), lp, Jpi, Pickup Particle, C2S
    lvl_no = row[0].strip()
    ex_str = row[1].strip()
    if ex_str in ('—', '', '-'): continue
    
    # Parse energy: may have ± uncertainty
    ex_val = None
    ex_unc = ''
    if '±' in ex_str:
        parts = ex_str.split('±')
        ex_val = float(parts[0])
        ex_unc = parts[1]
    else:
        ex_val = float(ex_str)
    
    lp = row[2].strip()
    jpi = row[3].strip()
    pickup = row[4].strip()
    c2s = row[5].strip() if len(row) > 5 else ''
    
    # Parse C2S: may have multiple values, may have parentheses for tentative
    c2s_values = []
    for v in c2s.split(','):
        v = v.strip()
        if v and v not in ('—', '', '-'):
            c2s_values.append(v)
    
    csv_levels.append({
        'lvl_no': lvl_no,
        'ex_mev': ex_val,
        'ex_unc': ex_unc,
        'lp': lp,
        'jpi': jpi,
        'pickup': pickup,
        'c2s': c2s_values
    })

print(f"\nParsed {len(csv_levels)} CSV levels:")
for l in csv_levels:
    print(f"  Lvl {l['lvl_no']}: E={l['ex_mev']}±{l['ex_unc']} MeV, L={l['lp']}, J={l['jpi']}, pickup={l['pickup']}, C2S={l['c2s']}")

# ====== PARSE ENSDF ======
with open(r'A34\S34\new\S34_35cl_d_3he.ens', 'r') as f:
    ens_lines = f.readlines()

ens_levels = []
current_l = None

for i, line in enumerate(ens_lines):
    if len(line) < 10: continue
    
    # L-record: col8='L', col9=' ', NOT comment
    if line[7] == 'L' and line[8] == ' ' and line[6] != 'c':
        if current_l is not None:
            ens_levels.append(current_l)
        
        e_str = line[9:19].strip()
        de_str = line[19:21].strip()
        j_str = line[22:39].strip()
        l_str = line[55:64].strip()
        s_str = line[64:74].strip()
        ds_str = line[74:76].strip()
        
        e_val = float(e_str) if e_str else 0.0
        de_val = de_str if de_str else ''
        l_val = l_str if l_str else ''
        
        # Parse S: may be combined like "0.38+0.56"
        s_values = []
        if s_str:
            # Split by + for combined S values
            parts = re.split(r'\+', s_str)
            for p in parts:
                p = p.strip()
                if p:
                    try:
                        s_values.append(float(p))
                    except ValueError:
                        s_values.append(p)
        
        current_l = {
            'line': i+1,
            'e_kev': e_val,
            'de_kev': de_val,
            'jpi': j_str,
            'l': l_val,
            's': s_values,
            'ds': ds_str,
            's_text': s_str,
            'cl_comments': []
        }
        continue
    
    # Collect cL comments for this level
    if current_l is not None and line[6] == 'c' and line[7] == 'L':
        current_l['cl_comments'].append(line.rstrip())

if current_l is not None:
    ens_levels.append(current_l)

print(f"\nParsed {len(ens_levels)} ENSDF levels:")
for l in ens_levels:
    print(f"  Line {l['line']}: E={l['e_kev']}±{l['de_kev']} keV, L={l['l']}, S={l['s']}")

# ====== MATCH AND COMPARE ======
print("\n" + "="*70)
print("CROSS-CHECK REPORT: S34_35cl_d_3he.ens vs 1969PU03.csv")
print("="*70)

def match_csv_to_ens(csv_l):
    """Match CSV level (MeV) to ENSDF level (keV)."""
    csv_kev = csv_l['ex_mev'] * 1000
    csv_unc_kev = 0
    if csv_l['ex_unc']:
        try:
            csv_unc_kev = float(csv_l['ex_unc']) * 1000
        except: pass
    
    best = None
    best_diff = 999
    for el in ens_levels:
        d = abs(csv_kev - el['e_kev'])
        if d < best_diff:
            best_diff = d
            best = el
    
    tolerance = max(30, csv_unc_kev * 3) if csv_unc_kev else 30
    if best_diff <= tolerance:
        return best, best_diff
    return None, best_diff

errors = 0
warnings = 0

for csv_l in csv_levels:
    ens_l, diff = match_csv_to_ens(csv_l)
    csv_kev = csv_l['ex_mev'] * 1000
    
    if ens_l is None:
        print(f"\nCSV Lvl {csv_l['lvl_no']} E={csv_kev:.0f} keV: NO ENSDF MATCH (best diff={diff:.0f} keV)")
        errors += 1
        continue
    
    print(f"\nCSV Lvl {csv_l['lvl_no']} E={csv_kev:.0f} keV -> ENSDF Line {ens_l['line']} E={ens_l['e_kev']:.0f} keV (diff={diff:.0f} keV)")
    print(f"  CSV: L={csv_l['lp']}, pickup={csv_l['pickup']}, C2S={csv_l['c2s']}")
    print(f"  ENS: L={ens_l['l']}, S={ens_l['s']}, S_text='{ens_l['s_text']}'")
    
    # Compare S values
    csv_s_vals = []
    for v in csv_l['c2s']:
        # Remove parentheses for comparison, note tentative
        is_tent = v.startswith('(') and v.endswith(')')
        v_clean = v.strip('()')
        try:
            csv_s_vals.append((float(v_clean), is_tent))
        except ValueError:
            csv_s_vals.append((v_clean, is_tent))
    
    ens_s_vals = []
    for v in ens_l['s']:
        if isinstance(v, (int, float)):
            ens_s_vals.append(v)
        else:
            ens_s_vals.append(v)
    
    # Compare S values
    n_csv = len(csv_s_vals)
    n_ens = len(ens_s_vals)
    
    if n_csv != n_ens:
        print(f"  ** S COUNT MISMATCH: CSV={n_csv} vs ENS={n_ens}")
        errors += 1
    
    for j in range(min(n_csv, n_ens)):
        csv_s, csv_tent = csv_s_vals[j]
        ens_s = ens_s_vals[j]
        
        if isinstance(csv_s, float) and isinstance(ens_s, float):
            ratio = ens_s / csv_s if csv_s != 0 else 999
            if abs(ratio - 1.0) > 0.005:
                print(f"  ** S-VALUE MISMATCH [{j}]: CSV C2S={csv_s} vs ENS S={ens_s} (ratio={ratio:.3f})")
                errors += 1
        elif csv_s != ens_s:
            print(f"  ** S-VALUE MISMATCH [{j}]: CSV='{csv_s}' vs ENS='{ens_s}'")
            errors += 1
    
    # Compare L values
    # CSV lp may be like "0+2" (two L values), ENS l may be like "0+2"
    csv_lp = csv_l['lp'].replace(' ', '')
    ens_lp = ens_l['l'].replace(' ', '')
    if csv_lp and ens_lp and csv_lp != ens_lp:
        print(f"  ** L MISMATCH: CSV L={csv_l['lp']} vs ENS L={ens_l['l']}")
        errors += 1
    
    # Compare pickup vs cL comment
    pickup_csv = csv_l['pickup']
    has_pickup_comment = any('Pickup proton' in c for c in ens_l['cl_comments'])
    if pickup_csv and pickup_csv != '—' and not has_pickup_comment:
        print(f"  ** PICKUP COMMENT MISSING: CSV pickup='{pickup_csv}'")
        warnings += 1

# Check for ENSDF levels not in CSV
print(f"\n--- ENSDF-only levels ---")
matched_ens = set()
for csv_l in csv_levels:
    ens_l, _ = match_csv_to_ens(csv_l)
    if ens_l:
        matched_ens.add(ens_l['line'])

for el in ens_levels:
    if el['line'] not in matched_ens:
        print(f"  ENS Line {el['line']}: E={el['e_kev']} keV, S={el['s']} — NO CSV MATCH")
        # Check if from 1968Wi20
        has_wi20 = any('1968Wi20' in c for c in el['cl_comments'])
        if has_wi20:
            print(f"    (from 1968Wi20 — expected)")

print(f"\n{'='*70}")
print(f"SUMMARY: Errors={errors}, Warnings={warnings}")
