"""Cross-check S34 resonance - fixed column parsing and units."""
import re

# ====== PARSE MARKDOWN ======
with open(r'A34\S34\raw\2018MuZY_34S.md', 'r', encoding='utf-8') as f:
    md = f.read()

md_rows = []
in_table = False
for line in md.split('\n'):
    line = line.strip()
    if 'E_0' in line and 'keV' in line:
        in_table = True
        continue
    if in_table and line.startswith('|') and '---' not in line:
        if 'Footnotes' in line: break
        md_rows.append(line)

md_levels = []
for row in md_rows:
    # Split but keep empty cells: preserve exact column structure
    cells = [c.strip() for c in row.split('|')]
    # Remove first and last empty from split
    if cells and cells[0] == '': cells = cells[1:]
    if cells and cells[-1] == '': cells = cells[:-1]
    
    if len(cells) < 3: continue
    
    e0_str = cells[0]
    e0_str = re.sub(r'[\$\^a-z\*]', '', e0_str).strip()
    if e0_str in ('', '-', '—'): continue
    
    e0_val = float(e0_str)
    
    # Columns: 0=E0, 1=J, 2=l, 3=Gamma, 4=Gamma_n, 5=Gamma_g, 6=Gamma_n0, 7=Gamma_n1, 8=gGnGg/G, 9=Gamma_a
    def cell(n):
        return cells[n] if n < len(cells) else ''
    
    md_levels.append({
        'e0': e0_val,
        'j': cell(1),
        'l': cell(2),
        'gamma': cell(3),
        'gn': cell(4),
        'gg': cell(5),
        'gn0': cell(6),
        'gn1': cell(7),
        'ggn': cell(8),
        'ga': cell(9),
    })

print(f"Parsed {len(md_levels)} MD levels")

# ====== PARSE ENSDF ======
with open(r'A34\S34\new\S34_n_g_n_n_resonances.ens', 'r') as f:
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
        j_str = line[22:39].strip()
        t_str = line[39:49].strip()
        dt_str = line[49:55].strip()
        l_str = line[55:64].strip()
        s_str = line[64:74].strip()
        q_str = line[79]
        
        current_l = {
            'line': i+1, 'e_exc': float(e_str) if e_str else 0,
            'j': j_str, 't': t_str, 'dt': dt_str,
            'l': l_str, 's': s_str.strip(), 'q': q_str,
            'cl_comments': [], 'ens_text': line.rstrip()
        }
        continue
    
    if current_l is not None and len(line) > 7 and line[6] == 'c' and line[7] == 'L':
        current_l['cl_comments'].append(line.rstrip())

if current_l is not None:
    ens_levels.append(current_l)

def parse_ens_comments(ens_l):
    """Extract values from cL comments with unit awareness."""
    info = {'ggn': '', 'gn': '', 'gg': '', 'ga': '', 'ggn_unc': '', 'gn_unc': '', 'gg_unc': '', 'ga_unc': ''}
    
    for cl in ens_l['cl_comments']:
        # gGnGg/G: "g|G{-n}|G{-|g}/|G=0.086 {I6}"
        m = re.search(r'g\|G\{-n\}\|G\{-\|g\}/\|G\s*=\s*([\d.]+)\s*(?:\{I([\d+-]+)\})?', cl)
        if m:
            info['ggn'] = m.group(1)
            if m.group(2): info['ggn_unc'] = m.group(2)
        
        # Gamma_n: "|G{-n}=75.0 EV 8" or with {I} notation
        m = re.search(r'\|G\{-n\}\s*=\s*([\d.]+)\s*(EV|KEV|MEV)?\s*(\d+)?(?:\s*\{I([\d+-]+)\})?', cl)
        if m:
            info['gn'] = m.group(1)
            info['gn_unit'] = m.group(2) if m.group(2) else ''
            info['gn_unc'] = m.group(3) if m.group(3) else ''
        
        # Gamma_g: "|G|g=0.21 EV 5"
        m = re.search(r'\|G\|g\s*=\s*([\d.]+)\s*(EV|KEV|MEV)?\s*(\d+)?(?:\s*\{I([\d+-]+)\})?', cl)
        if not m:
            m = re.search(r'\|G\{\|g\}\s*=\s*([\d.]+)\s*(EV|KEV|MEV)?\s*(\d+)?', cl)
        if m:
            info['gg'] = m.group(1)
            info['gg_unit'] = m.group(2) if m.group(2) else ''
            info['gg_unc'] = m.group(3) if m.group(3) else ''
        
        # Gamma_a: "|G{-|a}=41 EV 5"
        m = re.search(r'\|G\{-\|a\}\s*=\s*([\d.]+)\s*(EV|KEV|MEV)?\s*(\d+)?(?:\s*\{I([\d+-]+)\})?', cl)
        if m:
            info['ga'] = m.group(1)
            info['ga_unit'] = m.group(2) if m.group(2) else ''
            info['ga_unc'] = m.group(3) if m.group(3) else ''
    
    # Extract T field (total width)
    t_text = ens_l['t'].strip()
    dt_text = ens_l['dt'].strip()
    if t_text:
        # Find unit in T field
        m = re.match(r'([\d.]+)\s*(EV|KEV|MEV)?', t_text)
        if m:
            info['gamma_val'] = m.group(1)
            info['gamma_unit'] = m.group(2) if m.group(2) else 'EV'
            info['gamma_unc'] = dt_text if dt_text and dt_text not in ('LT', 'GT', 'LE', 'GE') else ''
            info['gamma_limit'] = dt_text if dt_text in ('LT', 'GT', 'LE', 'GE') else ''
    return info

def to_ev(val_str, unit_str):
    """Convert value+unit to eV."""
    try:
        v = float(val_str)
    except: return None
    if unit_str in ('KEV', 'keV'):
        return v * 1000
    elif unit_str in ('MEV', 'meV'):
        return v * 1e6
    return v

# ====== COMPARE ======
print("\n" + "="*75)
print("CROSS-CHECK: S34_n_g_n_n_resonances.ens vs 2018MuZY_34S.md")
print("="*75)

errors = 0
matched_ens = set()

for md_l in md_levels:
    e0 = md_l['e0']
    
    best_ens = None
    best_diff = 999
    for el in ens_levels:
        try: s_val = float(el['s'])
        except: continue
        d = abs(s_val - e0)
        if d < best_diff: best_diff, best_ens = d, el
    
    if best_ens is None or best_diff > 0.2:
        print(f"E0={e0} keV: NO MATCH (diff={best_diff:.2f})")
        errors += 1
        continue
    
    matched_ens.add(id(best_ens))
    el = best_ens
    info = parse_ens_comments(el)
    
    has_err = False
    def report(msg):
        nonlocal has_err
        if not has_err:
            print(f"\nE0={e0} keV (ENS line {el['line']}, S={el['s']}):")
        print(f"  {msg}")
        # can't use nonlocal at module level, use list
    
    # Compare J (strip parity from ENSDF for comparison)
    md_j = md_l['j'].replace(' ', '').replace('$','').replace('\\','')
    # Handle ≥ → GE
    md_j = md_j.replace('≥', 'GE').replace('≥', 'GE')
    ens_j = el['j'].replace(' ', '')
    # Strip parity suffix from ENSDF J for MD comparison
    ens_j_no_parity = ens_j.rstrip('+-')
    if md_j and ens_j_no_parity and md_j != ens_j_no_parity:
        report(f"J MISMATCH: MD='{md_l['j']}' vs ENS='{el['j']}'")
        errors += 1
    
    # Compare l
    md_l_val = md_l['l'].strip('()')
    ens_l_val = el['l'].strip('()')
    if md_l_val and ens_l_val and md_l_val != ens_l_val:
        report(f"L MISMATCH: MD='{md_l['l']}' vs ENS='{el['l']}'")
        errors += 1
    
    # Compare Gamma (total width): MD is always in eV
    md_gamma = md_l['gamma']
    if md_gamma:
        md_g_match = re.match(r'([<\>\u2264\u2265]*)\s*([\d.]+)\s*(?:\(([\d.]+)\))?', md_gamma)
        if md_g_match:
            md_g_val = float(md_g_match.group(2))
            md_g_unc = md_g_match.group(3)
            
            ens_g_val = to_ev(info.get('gamma_val',''), info.get('gamma_unit','EV'))
            
            if ens_g_val:
                if abs(md_g_val - ens_g_val) > max(md_g_val, ens_g_val) * 0.015:
                    report(f"Gamma MISMATCH: MD={md_gamma} eV vs ENS={info.get('gamma_val','')} {info.get('gamma_unit','EV')}")
                    errors += 1
    
    # Compare Gamma_n
    md_gn = md_l['gn']
    if md_gn:
        md_gn_clean = re.sub(r'\^[a-z]', '', md_gn)
        md_gn_match = re.match(r'([\d.]+)\s*(?:\(([\d.]+)\))?', md_gn_clean)
        if md_gn_match:
            md_gn_val = float(md_gn_match.group(1))
            ens_gn_val = to_ev(info.get('gn',''), info.get('gn_unit','EV'))
            if ens_gn_val and abs(md_gn_val - ens_gn_val) > max(md_gn_val, ens_gn_val) * 0.015:
                report(f"Gn MISMATCH: MD={md_gn} eV vs ENS={info.get('gn','')} {info.get('gn_unit','EV')}")
                errors += 1
    
    # Compare Gamma_g
    md_gg = md_l['gg']
    if md_gg:
        md_gg_match = re.match(r'([\d.]+)\s*(?:\(([\d.]+)\))?', md_gg)
        if md_gg_match:
            md_gg_val = float(md_gg_match.group(1))
            ens_gg_val = to_ev(info.get('gg',''), info.get('gg_unit','EV'))
            if ens_gg_val and abs(md_gg_val - ens_gg_val) > max(md_gg_val, ens_gg_val) * 0.015:
                report(f"Gg MISMATCH: MD={md_gg} eV vs ENS={info.get('gg','')} {info.get('gg_unit','EV')}")
                errors += 1
    
    # Compare gGnGg/G
    md_ggn = md_l['ggn']
    if md_ggn:
        md_ggn_match = re.match(r'([\d.]+)\s*(?:\(([\d.]+)\))?', md_ggn)
        if md_ggn_match:
            md_ggn_val = float(md_ggn_match.group(1))
            ens_ggn_val = float(info['ggn']) if info['ggn'] else None
            if ens_ggn_val and abs(md_ggn_val - ens_ggn_val) > max(md_ggn_val, ens_ggn_val) * 0.015:
                report(f"gGnGg/G MISMATCH: MD={md_ggn} vs ENS={info['ggn']}")
                errors += 1
    
    # Compare Gamma_a
    md_ga = md_l['ga']
    ens_ga = info['ga']
    if md_ga or ens_ga:
        has_md_ga = bool(md_ga and md_ga not in ('', '-'))
        has_ens_ga = bool(ens_ga)
        if has_md_ga != has_ens_ga:
            report(f"Ga PRESENCE: MD='{md_ga}' vs ENS='{ens_ga}'")
            errors += 1
        elif has_md_ga:
            md_ga_match = re.match(r'([\d.]+)\s*(?:\(([\d.]+)\))?', md_ga)
            if md_ga_match:
                md_ga_val = float(md_ga_match.group(1))
                ens_ga_val = to_ev(ens_ga, info.get('ga_unit','EV'))
                if ens_ga_val and abs(md_ga_val - ens_ga_val) > max(md_ga_val, ens_ga_val) * 0.015:
                    report(f"Ga MISMATCH: MD={md_ga} eV vs ENS={ens_ga} {info.get('ga_unit','EV')}")
                    errors += 1

# ENSDF-only
ens_only = 0
for el in ens_levels:
    if id(el) not in matched_ens:
        is_fict = any('fictitious' in c for c in el['cl_comments'])
        if not is_fict:
            ens_only += 1
            print(f"\nENS ONLY: Line {el['line']}, S={el['s']}, J={el['j']}")

print(f"\n{'='*75}")
print(f"Errors: {errors}  |  MD: {len(md_levels)}  ENS: {len(ens_levels)}  ENS-only: {ens_only}")
