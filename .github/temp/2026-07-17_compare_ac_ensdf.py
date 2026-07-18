"""
Compare angular correlation data between Table IV markdown and ENSDF cG comment lines.
Flag discrepancies and report for fixing.
"""
import re

# ============================================================
# PARSE TABLE IV 
# ============================================================
with open('d:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd_Table_IV.md', 'r', encoding='utf-8') as f:
    md_lines = f.readlines()

table_rows = []
for l in md_lines:
    s = l.strip()
    if not s.startswith('| '): continue
    if '$' in s or '---' in s or ':' in s: continue
    parts = [p.strip() for p in s.split('|')]
    parts = parts[1:-1]
    if len(parts) < 12: continue
    try:
        # Parse Table IV row
        e_level = parts[0]       # E1
        eg1 = parts[1]           # Eg1
        eg2 = parts[2]           # Eg2
        a0 = parts[3]            # 0.8860 (6) format
        a2 = parts[4]
        a4 = parts[5]
        e2 = parts[6]            # E2 (intermediate level)
        e3 = parts[7]            # E3 (ground = 0)
        j1 = parts[8]            # J1
        j2 = parts[9]            # J2
        j3 = parts[10]           # J3
        d1 = parts[11]           # delta_1 (mixing ratio)
        
        table_rows.append({
            'E_level': e_level,
            'Eg1': eg1, 'Eg2': eg2,
            'A0': a0, 'A2': a2, 'A4': a4,
            'E2': e2, 'E3': e3,
            'J1': j1, 'J2': j2, 'J3': j3,
            'delta': d1
        })
    except:
        pass

print(f"Table IV rows parsed: {len(table_rows)}")

# Build lookup keyed by (E_level, Eg1, Eg2)
table_lookup = {}
for r in table_rows:
    key = (r['E_level'], r['Eg1'], r['Eg2'])
    table_lookup[key] = r

# ============================================================
# PARSE ENSDF FILE
# ============================================================
with open('d:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd.ens', 'r') as f:
    ensdf_lines = f.readlines()

# Find L-records (level energies), G-records (gamma energies), and cG comments
ensdf_data = []
current_level_e = None
current_gammas = []  # list of (eg, raw_line)

for i, line in enumerate(ensdf_lines):
    # Check record type at col 8 (0-indexed 7)
    if len(line) < 80:
        continue
    
    rectype = line[7] if len(line) > 7 else ''
    nucid = line[0:5]
    
    if rectype == 'L' and '152GD' in nucid:
        # Parse level energy from cols 10-19
        e_str = line[9:19].strip()
        if e_str:
            try:
                current_level_e = float(e_str)
                current_gammas = []
                # Store for each gamma that follows
            except:
                pass
    
    elif rectype == 'G' and '152GD' in nucid and current_level_e is not None:
        # Parse gamma energy
        eg_str = line[9:19].strip()
        if eg_str:
            try:
                eg = float(eg_str)
                # Store this G-record line index
                current_gammas.append({'eg': eg_str, 'line_idx': i, 'ensdf_line': line.rstrip()})
            except:
                pass
    
    elif rectype == 'c' and line[6] == 'G' and '152GD' in nucid:
        # cG comment line for angular correlation
        comment = line[9:].strip()
        # Check for A{-n}=value {Iunc} pattern
        if 'A{-0}' in line or 'A{-2}' in line or 'A{-4}' in line:
            # This cG belongs to the LAST G-record
            if current_gammas and current_level_e is not None:
                last_g = current_gammas[-1]
                if 'ag_comments' not in last_g:
                    last_g['ag_comments'] = []
                last_g['ag_comments'].append({
                    'line_idx': i,
                    'text': comment,
                    'full_line': line.rstrip()
                })
                # Also check for continuation (2cG, 3cG)
                last_g['ag_continuation'] = []
    elif rectype == '2' and len(line) > 7 and line[6] == 'c' and line[7] == 'G':
        # 2cG continuation
        comment = line[9:].strip()
        if current_gammas:
            last_g = current_gammas[-1]
            if 'ag_continuation' not in last_g:
                last_g['ag_continuation'] = []
            last_g['ag_continuation'].append({
                'line_idx': i,
                'text': comment,
                'full_line': line.rstrip()
            })
    elif rectype == '3' and len(line) > 7 and line[6] == 'c' and line[7] == 'G':
        # 3cG continuation
        comment = line[9:].strip()
        if current_gammas:
            last_g = current_gammas[-1]
            if 'ag_continuation' not in last_g:
                last_g['ag_continuation'] = []
            last_g['ag_continuation'].append({
                'line_idx': i,
                'text': comment,
                'full_line': line.rstrip()
            })

# Build ENSDF lookup by (level_energy, gamma1, gamma2)
# We need to match cascades - Table IV gives cascades as (E_level, Eg1, Eg2 referring to cascade Eg1-Eg2 from level E)
# In ENSDF, cG $XXX-YYY |g|g(|q) annotates gamma transitions. The convention:
# $Eg1-Eg2 |g|g(|q) A{-0}=... means the AC was measured for the cascade where Eg1 feeds from the level 
# and Eg2 is the subsequent transition

# Actually, looking at ENSDF more carefully:
# The cG notation "$271-344 |g|g(|q)" appears after G-record for gamma 271 from the 615 level
# This means the angular correlation was measured between the 271 gamma (feeding the 344 level) and the 344 gamma (ground state transition)
# So the cascade is: 615 level -> 271 (gamma1) -> 344 level -> 344 (gamma2) -> 0 ground

# Table IV gives: E_level=615, Eg1=271, Eg2=344
# This matches perfectly.

# Let me now build the lookup. For each G-record that has cG with A{-0}:
#   Level = current_level_e
#   Gamma1 = eg of this G-record  
#   Gamma2 = extracted from $XXX-YYY pattern in cG

ensdf_lookup = {}

for g in current_gammas:
    if 'ag_comments' not in g:
        continue
    
    # Get the gamma energy of this G-record
    eg1 = g['eg']
    
    for ag in g['ag_comments']:
        text = ag['full_line']
        # Extract $XXX-YYY |g|g(|q) pattern
        m = re.search(r'\$(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*\|g\|g', text)
        if not m:
            continue
        eg2 = m.group(2)  # the second gamma in the cascade
        
        # Parse A0, A2, A4 from the text
        # Combine main cG line + continuation lines
        combined = text
        for cont in g.get('ag_continuation', []):
            combined += ' ' + cont['full_line']
        
        a0 = None; a2 = None; a4 = None; delta = None
        
        m0 = re.search(r'A\{-0\}=([\d.]+(?:\s*[<>])?)\s*\{I(\d+)\}', combined)
        m2 = re.search(r'A\{-2\}=(-?[\d.]+)\s*\{I(\d+)\}', combined)
        m4 = re.search(r'A\{-4\}=(-?[\d.]+(?:\.[\d]+)?)\s*\{I(\d+)\}', combined)
        md = re.search(r'\|d=([+-]?[\d.]+(?:\s*[<>])?)\s*\{I(\d+)\}', combined)
        
        key = (current_level_e, eg1, eg2)
        
        ensdf_lookup[key] = {
            'level': current_level_e,
            'eg1': eg1, 'eg2': eg2,
            'A0_val': m0.group(1).strip() if m0 else None,
            'A0_unc': m0.group(2) if m0 else None,
            'A2_val': m2.group(1).strip() if m2 else None,
            'A2_unc': m2.group(2) if m2 else None,
            'A4_val': m4.group(1).strip() if m4 else None,
            'A4_unc': m4.group(2) if m4 else None,
            'delta_val': md.group(1).strip() if md else None,
            'delta_unc': md.group(2) if md else None,
            'line_idx': ag['line_idx'],
            'combined_text': combined
        }

print(f"ENSDF angular correlation entries: {len(ensdf_lookup)}")

# ============================================================
# COMPARE
# ============================================================
print("\n=== COMPARISON ===")

def parse_value_unc(s):
    """Parse '0.8860 (6)' into (0.8860, 0.0006)"""
    m = re.match(r'(-?[\d.]+)\s*\((\d+)\)', s.strip())
    if not m:
        return None, None
    val = float(m.group(1))
    unc = int(m.group(2))
    # Determine decimal places from the string representation
    if '.' in m.group(1):
        dec = len(m.group(1).split('.')[1])
    else:
        dec = 0
    return val, unc / (10**dec)

def ensdf_to_str(val, unc_str):
    """Convert ENSDF A{-0}=0.8860 {I6} format to '0.8860 (6)'"""
    if val is None or unc_str is None:
        return None
    return f"{val} ({unc_str})"

discrepancies = []
for key, tr in table_lookup.items():
    e_level, eg1, eg2 = key
    
    # Normalize keys for matching
    # Table IV has integer-like strings, ENSDF has floats
    # Try to match by rounding
    
    # Find best match in ENSDF
    best_match = None
    for ek, ev in ensdf_lookup.items():
        el, g1, g2 = ek
        # Allow small differences in energy
        try:
            te = float(e_level)
            ee = float(el)
            tg1 = float(eg1)
            eg1e = float(g1)
            tg2 = float(eg2)
            eg2e = float(g2)
            if abs(te - ee) < 0.1 and abs(tg1 - eg1e) < 0.1 and abs(tg2 - eg2e) < 0.1:
                best_match = ev
                break
        except:
            pass
    
    if best_match is None:
        # Try alternate cascade (eg1 ordering might differ)
        # Table IV row has Eγ1, Eγ2 — this is the cascade γ1-γ2 from level
        continue
    
    # Compare A0, A2, A4, delta
    for field, t_val, e_val, e_unc in [
        ('A0', tr['A0'], best_match.get('A0_val'), best_match.get('A0_unc')),
        ('A2', tr['A2'], best_match.get('A2_val'), best_match.get('A2_unc')),
        ('A4', tr['A4'], best_match.get('A4_val'), best_match.get('A4_unc')),
    ]:
        tv, tu = parse_value_unc(t_val)
        if tv is None:
            continue
        ev = float(e_val) if e_val else None
        eu = int(e_unc) if e_unc else None
        
        if ev is None:
            discrepancies.append((key, field, t_val, 'MISSING_IN_ENSDF', best_match['line_idx']))
            continue
        
        # Compare values
        if abs(tv - ev) > 0.0001 or (eu and tu and abs(tu - eu / (10**len(str(tv).split('.')[1] if '.' in str(tv) else 0))) > 0.00001):
            # Different!
            t_str = t_val
            e_str = ensdf_to_str(e_val, e_unc) if e_unc else str(e_val)
            if t_str != e_str:
                discrepancies.append((key, field, t_val, e_str if e_str else str(e_val), best_match['line_idx']))
    
    # Compare delta
    if tr['delta'] and tr['delta'].strip():
        t_ds = tr['delta'].strip()
        if t_ds.startswith('>'):
            # Limit comparison
            t_limit = float(t_ds[1:])
            e_dv = best_match.get('delta_val')
            if e_dv:
                if e_dv.startswith('>'):
                    e_limit = float(e_dv[1:].strip())
                    if abs(t_limit - e_limit) > 0.1:
                        discrepancies.append((key, 'delta', t_ds, best_match.get('delta_val', 'N/A'), best_match['line_idx']))
                else:
                    discrepancies.append((key, 'delta', t_ds, best_match.get('delta_val', 'N/A'), best_match['line_idx']))
        else:
            td_val, td_unc = parse_value_unc(t_ds) if '(' in t_ds else (float(t_ds), None)
            ed_val = float(best_match.get('delta_val', '999')) if best_match.get('delta_val') else None
            if td_val is not None and ed_val is not None:
                if abs(td_val - ed_val) > 0.001:
                    e_str = ensdf_to_str(best_match.get('delta_val'), best_match.get('delta_unc')) if best_match.get('delta_unc') else str(best_match.get('delta_val'))
                    discrepancies.append((key, 'delta', t_ds, e_str if e_str else 'N/A', best_match['line_idx']))

print(f"Total discrepancies found: {len(discrepancies)}")
for key, field, t_val, e_val, line_idx in discrepancies[:30]:
    print(f"  Level={key[0]} Eg1={key[1]} Eg2={key[2]} {field}: TableIV={t_val} ENSDF={e_val} (line {line_idx+1})")
