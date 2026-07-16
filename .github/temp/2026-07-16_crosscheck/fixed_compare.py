import re

# Parse source
source_data = []
with open(r'XUNDL\2026MAAA_CT11001_141Sm_Table_I_revised.md', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line.startswith('|') or '---' in line or 'E_x' in line:
            continue
        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 9:
            continue
        try:
            float(parts[1].split('(')[0])
        except: continue
        
        eg = parts[3]
        while eg and eg[-1] in '*\u2217\u00b7\u2022':
            eg = eg[:-1].strip()
        
        source_data.append({
            'Ex': parts[1], 'Jpi': parts[2], 'Eg': eg, 'Intensity': parts[4],
            'RDCO': parts[5], 'Rtheta': parts[6], 'P': parts[7], 'Assignment': parts[8]
        })

# Parse ENSDF - fixed cG/cL parsing
with open(r'XUNDL\2026MAAA_CT11001_141Sm.ens', 'r', encoding='utf-8') as f:
    ens_lines = [l.rstrip('\n') for l in f.readlines()]

# Pad lines to 80
ens_lines = [l + ' ' * (80 - len(l)) if len(l) < 80 else l for l in ens_lines]

levels = []
current_level = None
current_gamma = None

for line_idx, line in enumerate(ens_lines):
    # Column 6 = line[5] (continuation)
    # Column 7 = line[6] (comment flag 'c' or other)
    # Column 8 = line[7] (record type: L, G, etc.)
    col7 = line[6]   # comment identifier
    col8 = line[7]   # record type
    col6 = line[5]   # continuation
    
    if col8 == 'L' and col6 == ' ' and col7 == ' ':
        if current_level is not None:
            levels.append(current_level)
        current_level = {
            'line_idx': line_idx, 'line': line,
            'E': line[9:19].strip(), 'DE': line[19:21].strip(),
            'J': line[22:39].strip(), 'Q': line[79:80].strip(),
            'MS': line[77:79].strip(), 'gammas': [], 'cL_comments': []
        }
        current_gamma = None
    
    elif col8 == 'G' and col6 == ' ' and col7 == ' ':
        current_gamma = {
            'line_idx': line_idx, 'line': line,
            'E': line[9:19].strip(), 'DE': line[19:21].strip(),
            'RI': line[22:29].strip(), 'DRI': line[29:31].strip(),
            'M': line[32:41].strip(), 'Q': line[79:80].strip(),
            'C': line[76:77].strip(), 'c_comments': []
        }
        if current_level is not None:
            current_level['gammas'].append(current_gamma)
    
    elif col7 == 'c' and col8 == 'G':
        # cG or 2cG or 3cG line
        if current_gamma is not None:
            current_gamma['c_comments'].append(line)
    
    elif col7 == 'c' and col8 == 'L':
        if current_level is not None:
            current_level['cL_comments'].append(line)

if current_level is not None:
    levels.append(current_level)

def parse_unc(text):
    match = re.match(r'([0-9]+\.?[0-9]*)\s*\(([0-9]+)\)', text)
    if match: return float(match.group(1)), match.group(2)
    return None, None

def ens_display(e_val, de_val):
    if not e_val: return ''
    if not de_val: return e_val
    return e_val + '(' + de_val + ')'

def normalize_unc(text):
    return re.sub(r'\{I([+]?\d+(?:[-]\d+)?)\}', r'(\1)', text)

print("=" * 80)
print("FIXED PARSE - MISMATCH REPORT")
print("=" * 80)

mismatches = []

for si, src in enumerate(source_data):
    src_ex_val, src_ex_unc = parse_unc(src['Ex'])
    src_eg_val, src_eg_unc = parse_unc(src['Eg'])
    src_int_val, src_int_unc = parse_unc(src['Intensity'])
    
    matched_level = None
    for lv in levels:
        try:
            lv_e = float(lv['E'])
        except: continue
        if src_ex_val is not None and abs(lv_e - src_ex_val) < 1.0:
            matched_level = lv
            break
    
    if matched_level is None:
        mismatches.append("L" + str(si) + " LEVEL NOT FOUND: Ex=" + src['Ex'])
        continue
    
    lv = matched_level
    
    lv_e_disp = ens_display(lv['E'], lv['DE'])
    if lv_e_disp != src['Ex']:
        mismatches.append("L" + str(si) + " Ex: src=" + src['Ex'] + " vs ens=" + lv_e_disp)
    
    matched_gamma = None
    for g in lv['gammas']:
        try:
            g_e = float(g['E'])
        except: continue
        if src_eg_val is not None and abs(g_e - src_eg_val) < 0.2:
            matched_gamma = g
            break
    
    if matched_gamma is None:
        mismatches.append("L" + str(si) + " GAMMA NOT FOUND: Ex=" + src['Ex'] + " Eg=" + src['Eg'])
        continue
    
    g = matched_gamma
    
    g_e_disp = ens_display(g['E'], g['DE'])
    if g_e_disp != src['Eg']:
        mismatches.append("L" + str(si) + " Eg: src=" + src['Eg'] + " vs ens=" + g_e_disp)
    
    g_ri_disp = ens_display(g['RI'], g['DRI'])
    if g_ri_disp != src['Intensity']:
        mismatches.append("L" + str(si) + " I: src=" + src['Intensity'] + " vs ens=" + g_ri_disp)
    
    cg_text = ' '.join([normalize_unc(c) for c in g['c_comments']])
    
    if src['RDCO']:
        expected = "R{-DCO}=" + src['RDCO']
        if expected not in cg_text:
            mismatches.append("L" + str(si) + " RDCO: expected '" + expected + "' not in comments")
    
    if src['Rtheta']:
        expected = "R{-ADO}=" + src['Rtheta']
        if expected not in cg_text:
            mismatches.append("L" + str(si) + " Rtheta: expected '" + expected + "' not in comments")
    
    if src['P']:
        expected = "POL=" + src['P']
        if expected not in cg_text:
            mismatches.append("L" + str(si) + " POL: expected '" + expected + "' not in comments")

print("\nTotal mismatches: " + str(len(mismatches)))
for m in mismatches:
    print("  " + m)

# Also dump cG comments for first few to verify parsing
print("\n=== VERIFY: cG comments for first 3 matched gammas ===")
for si in range(min(3, len(source_data))):
    src = source_data[si]
    src_ex_val, _ = parse_unc(src['Ex'])
    src_eg_val, _ = parse_unc(src['Eg'])
    for lv in levels:
        try:
            if abs(float(lv['E']) - src_ex_val) < 1.0:
                for g in lv['gammas']:
                    try:
                        if abs(float(g['E']) - src_eg_val) < 0.2:
                            print("Source #" + str(si) + " (Ex=" + src['Ex'] + " Eg=" + src['Eg'] + "):")
                            print("  cG comments: " + str(g['c_comments']))
                    except:
                        pass
        except:
            pass
    print()
