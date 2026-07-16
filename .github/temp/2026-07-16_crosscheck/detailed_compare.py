import re
import json

# === Parse Source (revised.md) - fixed to handle asterisks ===
source_data = []

with open(r'XUNDL\2026MAAA_CT11001_141Sm_Table_I_revised.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for line in lines:
    line = line.strip()
    if not line.startswith('|') or '---' in line or 'E_x' in line:
        continue
    parts = [p.strip() for p in line.split('|')]
    if len(parts) < 9:
        continue
    try:
        float(parts[1].split('(')[0])
    except:
        continue
    
    # Clean asterisk from Eg field
    eg = parts[3].replace('*', '').replace('\u2217', '').strip()
    intensity = parts[4]
    
    source_data.append({
        'Ex': parts[1], 'Jpi': parts[2], 'Eg': eg, 'Intensity': intensity,
        'RDCO': parts[5], 'Rtheta': parts[6], 'P': parts[7], 'Assignment': parts[8]
    })

# === Parse Target (ENSDF) ===
with open(r'XUNDL\2026MAAA_CT11001_141Sm.ens', 'r', encoding='utf-8') as f:
    ens_lines = f.readlines()

levels = []
current_level = None
current_gamma = None

for line in ens_lines:
    line = line.rstrip('\n')
    if len(line) < 80:
        line = line.ljust(80)
    
    record_type = line[7:8]
    col6 = line[5:6]
    
    if record_type == 'L' and col6 == ' ':
        if current_level is not None:
            levels.append(current_level)
        
        current_level = {
            'line': line, 
            'E': line[9:19].strip(),
            'DE': line[19:21].strip(),
            'J': line[22:39].strip(),
            'T': line[39:49].strip(),
            'DT': line[49:55].strip(),
            'Q': line[79:80].strip(),
            'MS': line[77:79].strip(),
            'gammas': [],
            'cL_comments': []
        }
        current_gamma = None
    
    elif record_type == 'G' and col6 == ' ':
        current_gamma = {
            'line': line,
            'E': line[9:19].strip(),
            'DE': line[19:21].strip(),
            'RI': line[22:29].strip(),
            'DRI': line[29:31].strip(),
            'M': line[32:41].strip(),
            'MR': line[41:49].strip(),
            'DMR': line[49:55].strip(),
            'Q': line[79:80].strip(),
            'C': line[76:77].strip(),
            'c_comments': []
        }
        if current_level is not None:
            current_level['gammas'].append(current_gamma)
    
    elif record_type == 'c' and line[6:7] == 'G':
        if current_gamma is not None:
            current_gamma['c_comments'].append(line)
    
    elif record_type == 'c' and line[6:7] == 'L':
        if current_level is not None:
            current_level['cL_comments'].append(line)
    
    elif record_type == 'c' and line[6:7] == 'c' and line[7:8] == 'G':
        if current_gamma is not None:
            current_gamma['c_comments'].append(line)
    
    elif record_type == 'c' and line[6:7] == 'c' and line[7:8] == 'L':
        if current_level is not None:
            current_level['cL_comments'].append(line)

if current_level is not None:
    levels.append(current_level)

# === DETAILED COMPARISON ===
print("=" * 80)
print("DETAILED MISMATCH REPORT")
print("=" * 80)

# Parse source uncertainty notation
def parse_unc(text):
    """Parse '123.4(12)' -> (123.4, '12')"""
    match = re.match(r'([0-9]+\.?[0-9]*)\s*\(([0-9]+)\)', text)
    if match:
        return float(match.group(1)), match.group(2)
    return None, None

# For ENSDF fields, parse E and DE
def ens_to_display(e_val, de_val):
    """Convert ENSDF fields to display notation like '123.4(12)'"""
    if not e_val:
        return ''
    if not de_val:
        return e_val
    return f"{e_val}({de_val})"

mismatches = []

for si, src in enumerate(source_data):
    src_ex_val, src_ex_unc = parse_unc(src['Ex'])
    src_eg_val, src_eg_unc = parse_unc(src['Eg'])
    src_int_val, src_int_unc = parse_unc(src['Intensity'])
    
    # Find matching level
    matched_level = None
    for lv in levels:
        try:
            lv_e = float(lv['E'])
        except:
            continue
        if src_ex_val is not None and abs(lv_e - src_ex_val) < 1.0:
            matched_level = lv
            break
    
    if matched_level is None:
        mismatches.append("LEVEL NOT FOUND: Source Ex=" + src['Ex'])
        continue
    
    lv = matched_level
    
    # Compare Level Energy
    lv_e_display = ens_to_display(lv['E'], lv['DE'])
    if lv_e_display != src['Ex']:
        mismatches.append("L" + str(si) + " Ex MISMATCH: source=" + src['Ex'] + " vs target=" + lv_e_display + " (L-record E=" + lv['E'] + " DE=" + lv['DE'] + ")")
    
    # Compare Jpi
    if lv['J'] != src['Jpi']:
        mismatches.append("L" + str(si) + " Jpi MISMATCH: source=" + src['Jpi'] + " vs target=" + lv['J'])
    
    # Find matching gamma
    matched_gamma = None
    for g in lv['gammas']:
        try:
            g_e = float(g['E'])
        except:
            continue
        if src_eg_val is not None and abs(g_e - src_eg_val) < 0.2:
            matched_gamma = g
            break
    
    if matched_gamma is None:
        mismatches.append("L" + str(si) + " GAMMA NOT FOUND: Ex=" + src['Ex'] + " Eg=" + src['Eg'])
        continue
    
    g = matched_gamma
    
    # Compare Gamma Energy
    g_e_display = ens_to_display(g['E'], g['DE'])
    if g_e_display != src['Eg']:
        mismatches.append("L" + str(si) + " Eg MISMATCH: source=" + src['Eg'] + " vs target=" + g_e_display)
    
    # Compare Intensity
    g_ri_display = ens_to_display(g['RI'], g['DRI'])
    if g_ri_display != src['Intensity']:
        mismatches.append("L" + str(si) + " Intensity MISMATCH: source=" + src['Intensity'] + " vs target=" + g_ri_display + " (RI=" + g['RI'] + " DRI=" + g['DRI'] + ")")
    
    # Compare Multipolarity
    # Source uses Q, D+Q notation; target may use (M1+E2), (E2), Q, etc.
    src_mult = src['Assignment']
    tgt_mult = g['M']
    
    # Map source to expected ENSDF:
    # Q -> Q or (E2) or E2
    # D+Q -> (M1+E2) or M1+E2
    mult_match = False
    if src_mult == 'Q' and (tgt_mult == 'Q' or tgt_mult == '(E2)' or tgt_mult == 'E2'):
        mult_match = True
    elif src_mult == 'D+Q' and (tgt_mult == '(M1+E2)' or tgt_mult == 'M1+E2'):
        mult_match = True
    elif src_mult == tgt_mult:
        mult_match = True
    
    if not mult_match:
        mismatches.append("L" + str(si) + " Mult MISMATCH: source=" + src_mult + " vs target=" + tgt_mult)
    
    # Compare comments: RDCO, Rtheta, P
    cg_text = ' '.join(g['c_comments']).strip()
    
    if src['RDCO']:
        expected_rdco = "R{-DCO}=" + src['RDCO']
        if expected_rdco not in cg_text:
            mismatches.append("L" + str(si) + " RDCO COMMENT MISMATCH: expected=" + expected_rdco + " not found in: " + cg_text[:100])
    
    if src['Rtheta']:
        expected_rtheta = "R{-ADO}=" + src['Rtheta']
        if expected_rtheta not in cg_text:
            mismatches.append("L" + str(si) + " Rtheta COMMENT MISMATCH: expected=" + expected_rtheta + " not found in: " + cg_text[:100])
    
    if src['P']:
        expected_p = "POL=" + src['P']
        if expected_p not in cg_text:
            mismatches.append("L" + str(si) + " P COMMENT MISMATCH: expected=" + expected_p + " not found in: " + cg_text[:100])

print(f"\nTotal mismatches found: {len(mismatches)}")
for m in mismatches:
    print(f"  {m}")
