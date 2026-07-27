"""Cross-check S34_n_g_n_n_resonances.ens vs 2018MuZY_34S.md."""
import re

# ====== PARSE MARKDOWN ======
with open(r'A34\S34\raw\2018MuZY_34S.md', 'r', encoding='utf-8') as f:
    md = f.read()

# Extract table rows: lines starting with | and containing numbers
md_rows = []
in_table = False
for line in md.split('\n'):
    line = line.strip()
    if 'E_0' in line and 'keV' in line:
        in_table = True
        continue
    if in_table and line.startswith('|') and '---' not in line:
        if 'Footnotes' in line:
            break
        md_rows.append(line)

# Parse each table row
# Format: | E0 | J | l | Gamma | Gamma_n | Gamma_g | Gamma_n0 | Gamma_n1 | gGnGg/G | Gamma_a |
def parse_cell(cell):
    """Parse a table cell, return (value_str, is_limit, is_tentative)."""
    c = cell.strip()
    if c == '':
        return ('', False, False)
    # Check for footnotes like ^a, ^b
    c = re.sub(r'\^[a-z]', '', c)
    # Check for tentative (parentheses)
    is_tent = c.startswith('(') and c.endswith(')')
    if is_tent:
        c = c[1:-1]
    is_lt = c.startswith('<')
    is_ge = c.startswith('≥') or c.startswith('≥')
    is_gt = c.startswith('>')
    c_clean = c.lstrip('<≥>').strip()
    return (c_clean, is_lt or is_ge or is_gt, is_tent)

md_levels = []
for row in md_rows:
    cells = [c.strip() for c in row.split('|')]
    # Remove empty first/last from split
    cells = [c for c in cells if c]
    if len(cells) < 3:
        continue
    
    e0_str = cells[0]
    # Strip markdown formatting: $...$ for math, ^ for superscript, ** for bold
    e0_str = re.sub(r'\$', '', e0_str)
    e0_str = re.sub(r'\^[a-z]', '', e0_str)
    e0_str = re.sub(r'\*\*', '', e0_str)
    e0_str = e0_str.strip()
    if e0_str in ('', '-', '—'):
        continue
    
    e0_val = float(e0_str)
    j_val = cells[1].strip() if len(cells) > 1 else ''
    l_val = cells[2].strip() if len(cells) > 2 else ''
    gamma_str = cells[3].strip() if len(cells) > 3 else ''
    gn_str = cells[4].strip() if len(cells) > 4 else ''
    gg_str = cells[5].strip() if len(cells) > 5 else ''
    gn0_str = cells[6].strip() if len(cells) > 6 else ''
    gn1_str = cells[7].strip() if len(cells) > 7 else ''
    ggn_str = cells[8].strip() if len(cells) > 8 else ''
    ga_str = cells[9].strip() if len(cells) > 9 else ''
    
    md_levels.append({
        'e0': e0_val,
        'j': j_val,
        'l': l_val,
        'gamma': gamma_str,
        'gn': gn_str,
        'gg': gg_str,
        'gn0': gn0_str,
        'gn1': gn1_str,
        'ggn': ggn_str,
        'ga': ga_str,
    })

print(f"Parsed {len(md_levels)} MD levels")

# ====== PARSE ENSDF ======
with open(r'A34\S34\new\S34_n_g_n_n_resonances.ens', 'r') as f:
    ens_lines = f.readlines()

ens_levels = []
current_l = None

for i, line in enumerate(ens_lines):
    if len(line) < 10: continue
    
    # L-record: col8='L', col9=' ', NOT cL comment
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
        
        e_val = float(e_str) if e_str else 0.0
        
        current_l = {
            'line': i+1,
            'e_exc': e_val,
            'de': de_str,
            'j': j_str,
            't': t_str,
            'dt': dt_str,
            'l': l_str,
            's': s_str.strip(),  # E_n(lab) in keV
            'q': q_str,
            'cl_comments': [],
            'ens_text': line.rstrip()
        }
        continue
    
    # Collect cL comments
    if current_l is not None and len(line) > 7 and line[6] == 'c' and line[7] == 'L':
        current_l['cl_comments'].append(line.rstrip())

if current_l is not None:
    ens_levels.append(current_l)

# Parse cL comments for each level to extract values
def parse_ens_comments(ens_l):
    """Extract Gamma_n, Gamma_g, gGnGg/G, Gamma_a from cL comments."""
    info = {'ggn': '', 'gn': '', 'gg': '', 'ga': '', 'gamma': ''}
    
    for cl in ens_l['cl_comments']:
        # gGnGg/G
        m = re.search(r'g\|G\{-n\}\|G\{-\|g\}/\|G=([\d.]+(?:\s+\{I[\d+-]+\})?)', cl)
        if not m:
            m = re.search(r'g\|G\{-n\}\|G\{-\|g\}/\|G\s*=\s*([\d.]+)', cl)
        if m:
            info['ggn'] = m.group(1).strip()
        
        # Gamma_n
        m = re.search(r'\|G\{-n\}=([\d.]+(?:\s*(?:EV|KEV|MEV))?\s*(?:\{I[\d+-]+\})?)', cl)
        if m:
            info['gn'] = m.group(1).strip()
        
        # Gamma_g
        m = re.search(r'\|G\|g=([\d.]+(?:\s*(?:EV|KEV|MEV))?\s*(?:\{I[\d+-]+\})?)', cl)
        if not m:
            m = re.search(r'\|G\{\|g\}=([\d.]+(?:\s*(?:EV|KEV|MEV))?\s*(?:\{I[\d+-]+\})?)', cl)
        if m:
            info['gg'] = m.group(1).strip()
        
        # Gamma_a
        m = re.search(r'\|G\{-\|a\}=([\d.]+(?:\s*(?:EV|KEV|MEV))?\s*(?:\{I[\d+-]+\})?)', cl)
        if m:
            info['ga'] = m.group(1).strip()
        
        # Gamma (total)
        m = re.search(r'\|G\|g=([\d.]+)', cl)
    
    # T field = Gamma total
    if ens_l['t']:
        info['gamma'] = ens_l['t'].strip()
    
    return info

# ====== MATCH AND COMPARE ======
print(f"Parsed {len(ens_levels)} ENSDF levels")
print("\n" + "="*75)
print("CROSS-CHECK: S34_n_g_n_n_resonances.ens vs 2018MuZY_34S.md")
print("="*75)

errors = 0
warnings = 0
matched_md = set()

for md_l in md_levels:
    e0 = md_l['e0']
    
    # Match by S field (E_n lab in keV)
    best_ens = None
    best_diff = 999
    for el in ens_levels:
        try:
            s_val = float(el['s'])
        except ValueError:
            continue
        d = abs(s_val - e0)
        if d < best_diff:
            best_diff = d
            best_ens = el
    
    if best_ens is None or best_diff > 0.2:
        print(f"\nE0={e0} keV: NO ENSDF MATCH (best diff={best_diff:.2f})")
        errors += 1
        continue
    
    matched_md.add(id(best_ens))
    el = best_ens
    info = parse_ens_comments(el)
    
    has_error = False
    
    # Compare J
    md_j = md_l['j'].replace(' ', '')
    ens_j = el['j'].replace(' ', '')
    if md_j and ens_j and md_j != ens_j:
        # Special case: ≥1 vs GE 1
        if not ('GE' in ens_j and md_j.startswith('≥')):
            print(f"\nE0={e0} keV (ENS line {el['line']}):")
            print(f"  J MISMATCH: MD='{md_l['j']}' vs ENS='{el['j']}'")
            has_error = True
            errors += 1
    
    # Compare l
    md_l_val = md_l['l'].strip('()')
    ens_l_val = el['l'].strip('()')
    if md_l_val and ens_l_val and md_l_val != ens_l_val:
        print(f"\nE0={e0} keV (ENS line {el['line']}):")
        print(f"  L MISMATCH: MD='{md_l['l']}' vs ENS='{el['l']}'")
        has_error = True
        errors += 1
    
    # Compare Gamma (total width)
    md_gamma = md_l['gamma']
    ens_gamma = info['gamma']
    if md_gamma and ens_gamma:
        # Extract numeric value for comparison
        md_g_val = re.search(r'([\d.]+)', md_gamma)
        ens_g_val = re.search(r'([\d.]+)', ens_gamma)
        if md_g_val and ens_g_val:
            md_g = float(md_g_val.group(1))
            ens_g = float(ens_g_val.group(1))
            if abs(md_g - ens_g) > max(md_g, ens_g) * 0.02:
                if not has_error:
                    print(f"\nE0={e0} keV (ENS line {el['line']}):")
                print(f"  Gamma MISMATCH: MD={md_gamma} vs ENS={ens_gamma}")
                has_error = True
                errors += 1
    
    # Compare gGnGg/G
    md_ggn = md_l['ggn']
    ens_ggn = info['ggn']
    if md_ggn and ens_ggn:
        md_g_val = re.search(r'([\d.]+)', md_ggn)
        ens_g_val = re.search(r'([\d.]+)', ens_ggn)
        if md_g_val and ens_g_val:
            md_g = float(md_g_val.group(1))
            ens_g = float(ens_g_val.group(1))
            if abs(md_g - ens_g) > max(md_g, ens_g) * 0.02:
                if not has_error:
                    print(f"\nE0={e0} keV (ENS line {el['line']}):")
                print(f"  gGnGg/G MISMATCH: MD={md_ggn} vs ENS={ens_ggn}")
                has_error = True
                errors += 1
    
    # Compare Gamma_n
    md_gn = md_l['gn']
    ens_gn = info['gn']
    if md_gn and ens_gn:
        # Handle special: ^a prefix on 2gGamma_n
        md_gn_clean = re.sub(r'\^[a-z]', '', md_gn)
        if md_gn_clean != ens_gn:
            md_v = re.search(r'([\d.]+)', md_gn_clean)
            ens_v = re.search(r'([\d.]+)', ens_gn)
            if md_v and ens_v:
                if float(md_v.group(1)) != float(ens_v.group(1)):
                    if not has_error:
                        print(f"\nE0={e0} keV (ENS line {el['line']}):")
                    print(f"  Gn MISMATCH: MD='{md_gn}' vs ENS='{ens_gn}'")
                    has_error = True
                    errors += 1
    
    # Compare Gamma_g
    md_gg = md_l['gg']
    ens_gg = info['gg']
    if md_gg and ens_gg:
        md_v = re.search(r'([\d.]+)', md_gg)
        ens_v = re.search(r'([\d.]+)', ens_gg)
        if md_v and ens_v:
            if abs(float(md_v.group(1)) - float(ens_v.group(1))) > 0.02:
                if not has_error:
                    print(f"\nE0={e0} keV (ENS line {el['line']}):")
                print(f"  Gg MISMATCH: MD='{md_gg}' vs ENS='{ens_gg}'")
                has_error = True
                errors += 1
    
    # Compare Gamma_a
    md_ga = md_l['ga']
    ens_ga = info['ga']
    if md_ga or ens_ga:
        if bool(md_ga) != bool(ens_ga):
            if not has_error:
                print(f"\nE0={e0} keV (ENS line {el['line']}):")
            print(f"  Ga PRESENCE MISMATCH: MD='{md_ga}' vs ENS='{ens_ga}'")
            has_error = True
            errors += 1
        elif md_ga:
            md_v = re.search(r'([\d.]+)', md_ga)
            ens_v = re.search(r'([\d.]+)', ens_ga)
            if md_v and ens_v:
                if abs(float(md_v.group(1)) - float(ens_v.group(1))) > 0.05:
                    if not has_error:
                        print(f"\nE0={e0} keV (ENS line {el['line']}):")
                    print(f"  Ga MISMATCH: MD='{md_ga}' vs ENS='{ens_ga}'")
                    has_error = True
                    errors += 1

# Check for ENSDF-only levels
ens_only_count = 0
for el in ens_levels:
    if id(el) not in matched_md:
        # Check if it's the fictitious level
        is_fictitious = any('fictitious' in c for c in el['cl_comments'])
        if not is_fictitious:
            ens_only_count += 1
            s_val = el['s'].strip()
            if s_val:
                print(f"\nENS ONLY: Line {el['line']}, E_n(lab)={s_val} keV, J={el['j']}")

print(f"\n{'='*75}")
print(f"SUMMARY: Errors={errors}, Warnings={warnings}")
print(f"MD levels: {len(md_levels)}, ENSDF levels: {len(ens_levels)}")
print(f"ENSDF-only (non-fictitious): {ens_only_count}")
