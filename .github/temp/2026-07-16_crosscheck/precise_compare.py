import re

# === Parse Source (revised.md) ===
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
    
    # Clean Eg: remove trailing asterisk (both ASCII * and Unicode variants)
    eg = parts[3]
    while eg and eg[-1] in '*\u2217\u00b7\u2022':
        eg = eg[:-1].strip()
    
    source_data.append({
        'Ex': parts[1], 'Jpi': parts[2], 'Eg': eg, 'Intensity': parts[4],
        'RDCO': parts[5], 'Rtheta': parts[6], 'P': parts[7], 'Assignment': parts[8]
    })

# === Parse ENSDF ===
with open(r'XUNDL\2026MAAA_CT11001_141Sm.ens', 'r', encoding='utf-8') as f:
    ens_lines = f.readlines()

levels = []
current_level = None
current_gamma = None

for line_idx, line in enumerate(ens_lines):
    line = line.rstrip('\n')
    if len(line) < 80:
        line = line.ljust(80)
    
    rt = line[7:8]
    c6 = line[5:6]
    
    if rt == 'L' and c6 == ' ':
        if current_level is not None:
            levels.append(current_level)
        current_level = {
            'line_idx': line_idx, 'line': line,
            'E': line[9:19].strip(), 'DE': line[19:21].strip(),
            'J': line[22:39].strip(), 'T': line[39:49].strip(),
            'DT': line[49:55].strip(), 'Q': line[79:80].strip(),
            'MS': line[77:79].strip(), 'gammas': [], 'cL_comments': []
        }
        current_gamma = None
    
    elif rt == 'G' and c6 == ' ':
        current_gamma = {
            'line_idx': line_idx, 'line': line,
            'E': line[9:19].strip(), 'DE': line[19:21].strip(),
            'RI': line[22:29].strip(), 'DRI': line[29:31].strip(),
            'M': line[32:41].strip(), 'MR': line[41:49].strip(),
            'DMR': line[49:55].strip(), 'Q': line[79:80].strip(),
            'C': line[76:77].strip(), 'c_comments': []
        }
        if current_level is not None:
            current_level['gammas'].append(current_gamma)
    
    elif line[7:8] == 'c' and line[6:7] == 'G':
        if current_gamma is not None:
            current_gamma['c_comments'].append(line)
    elif line[7:8] == 'c' and line[6:7] == 'L':
        if current_level is not None:
            current_level['cL_comments'].append(line)
    elif line[7:8] == 'c' and line[6:7].isdigit() and len(line) > 8 and line[8:9] == 'G':
        if current_gamma is not None:
            current_gamma['c_comments'].append(line)
    elif line[7:8] == 'c' and line[6:7].isdigit() and len(line) > 8 and line[8:9] == 'L':
        if current_level is not None:
            current_level['cL_comments'].append(line)

if current_level is not None:
    levels.append(current_level)

def parse_unc(text):
    match = re.match(r'([0-9]+\.?[0-9]*)\s*\(([0-9]+)\)', text)
    if match:
        return float(match.group(1)), match.group(2)
    return None, None

def ens_display(e_val, de_val):
    if not e_val: return ''
    if not de_val: return e_val
    return e_val + '(' + de_val + ')'

# Convert ENSDF {In} comment notation to (n) for comparison
def normalize_unc(text):
    """Convert {I5} -> (5), {I+10-11} -> (+10-11)"""
    return re.sub(r'\{I([+]?\d+(?:[-]\d+)?)\}', r'(\1)', text)

print("=" * 80)
print("PRECISE MISMATCH REPORT (ENSDF {In} notation normalized)")
print("=" * 80)

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
        except: continue
        if src_ex_val is not None and abs(lv_e - src_ex_val) < 1.0:
            matched_level = lv
            break
    
    if matched_level is None:
        mismatches.append("L" + str(si) + " LEVEL NOT FOUND: Ex=" + src['Ex'])
        continue
    
    lv = matched_level
    
    # Level Energy
    lv_e_disp = ens_display(lv['E'], lv['DE'])
    if lv_e_disp != src['Ex']:
        mismatches.append("L" + str(si) + " Ex: src=" + src['Ex'] + " vs ens=" + lv_e_disp + " (E=" + lv['E'] + " DE=" + lv['DE'] + ")")
    
    # Jpi - normalize Unicode minus to ASCII
    src_jpi = src['Jpi'].replace('\u2212', '-')
    if lv['J'] != src_jpi:
        mismatches.append("L" + str(si) + " Jpi: src=" + src_jpi + " vs ens=" + lv['J'])
    
    # Find gamma
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
    
    # Gamma Energy
    g_e_disp = ens_display(g['E'], g['DE'])
    if g_e_disp != src['Eg']:
        mismatches.append("L" + str(si) + " Eg: src=" + src['Eg'] + " vs ens=" + g_e_disp)
    
    # Intensity
    g_ri_disp = ens_display(g['RI'], g['DRI'])
    if g_ri_disp != src['Intensity']:
        mismatches.append("L" + str(si) + " I: src=" + src['Intensity'] + " vs ens=" + g_ri_disp + " (RI=" + g['RI'] + " DRI=" + g['DRI'] + ")")
    
    # Comments
    cg_text = ' '.join([normalize_unc(c) for c in g['c_comments']])
    
    if src['RDCO']:
        expected = "R{-DCO}=" + src['RDCO']
        if expected not in cg_text:
            mismatches.append("L" + str(si) + " RDCO missing: " + expected)
    
    if src['Rtheta']:
        expected = "R{-ADO}=" + src['Rtheta']
        if expected not in cg_text:
            mismatches.append("L" + str(si) + " Rtheta missing: " + expected)
    
    if src['P']:
        expected = "POL=" + src['P']
        if expected not in cg_text:
            mismatches.append("L" + str(si) + " POL missing: " + expected)

print("\nTotal mismatches: " + str(len(mismatches)))
for m in mismatches:
    print("  " + m)

print("\n=== Summary ===")
ex_mismatches = [m for m in mismatches if 'Ex:' in m]
jpi_mismatches = [m for m in mismatches if 'Jpi:' in m]
eg_mismatches = [m for m in mismatches if 'Eg:' in m]
int_mismatches = [m for m in mismatches if 'I:' in m]
comment_mismatches = [m for m in mismatches if 'missing' in m]
not_found = [m for m in mismatches if 'NOT FOUND' in m]

print("Level Energy mismatches: " + str(len(ex_mismatches)))
print("Jpi mismatches: " + str(len(jpi_mismatches)))
print("Gamma Energy mismatches: " + str(len(eg_mismatches)))
print("Intensity mismatches: " + str(len(int_mismatches)))
print("Comment mismatches: " + str(len(comment_mismatches)))
print("Not found: " + str(len(not_found)))
