import re
import json

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
    
    source_data.append({
        'Ex': parts[1], 'Jpi': parts[2], 'Eg': parts[3], 'Intensity': parts[4],
        'RDCO': parts[5], 'Rtheta': parts[6], 'P': parts[7], 'Assignment': parts[8]
    })

print('=== SOURCE DATA (revised.md) ===')
for i, d in enumerate(source_data):
    print(f"{i}: Ex={d['Ex']} Jpi={d['Jpi']} Eg={d['Eg']} I={d['Intensity']} RDCO={d['RDCO']} Rth={d['Rtheta']} P={d['P']} Mult={d['Assignment']}")

print("\n=== PARSING ENSDF TARGET ===")

# === Parse Target (ENSDF) ===
with open(r'XUNDL\2026MAAA_CT11001_141Sm.ens', 'r', encoding='utf-8') as f:
    ens_lines = f.readlines()

# Extract L-records and G-records with their c-comments
levels = []
current_level = None
current_gamma = None
current_c_comments = []

for line in ens_lines:
    line = line.rstrip('\n')
    if len(line) < 80:
        line = line.ljust(80)
    
    record_type = line[7:8]
    
    if record_type == 'L' and line[5:6] == ' ':
        # New level
        if current_level is not None:
            levels.append(current_level)
        
        e_str = line[9:19].strip()
        de_str = line[19:21].strip()
        j_str = line[22:39].strip()
        t_str = line[39:49].strip()
        dt_str = line[49:55].strip()
        q_str = line[79:80].strip()
        ms = line[77:79].strip()
        
        current_level = {
            'line': line, 'E': e_str, 'DE': de_str, 'J': j_str, 'T': t_str, 'DT': dt_str,
            'Q': q_str, 'MS': ms, 'gammas': [], 'c_comments': [], 'cL_comments': []
        }
        current_gamma = None
        current_c_comments = []
    
    elif record_type == 'G' and line[5:6] == ' ':
        e_str = line[9:19].strip()
        de_str = line[19:21].strip()
        ri_str = line[22:29].strip()
        dri_str = line[29:31].strip()
        m_str = line[32:41].strip()
        mr_str = line[41:49].strip()
        dmr_str = line[49:55].strip()
        q_str = line[79:80].strip()
        c_flag = line[76:77].strip()
        
        current_gamma = {
            'line': line, 'E': e_str, 'DE': de_str, 'RI': ri_str, 'DRI': dri_str,
            'M': m_str, 'MR': mr_str, 'DMR': dmr_str, 'Q': q_str, 'C': c_flag,
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
    
    elif line[6:7] == 'c' and line[7:8] == 'G':
        if current_gamma is not None:
            current_gamma['c_comments'].append(line)
    
    elif line[6:7] == 'c' and line[7:8] == 'L':
        if current_level is not None:
            current_level['cL_comments'].append(line)

if current_level is not None:
    levels.append(current_level)

print(f"Total levels: {len(levels)}")
print(f"Total gammas: {sum(len(lv['gammas']) for lv in levels)}")

# Match source data to target
print("\n=== MATCHING ===")

def extract_val_unc(text):
    """Extract value and uncertainty from text like '4482.0(6)' or '27.2(12)'"""
    match = re.match(r'([0-9]+\.?[0-9]*)\s*\(([0-9]+)\)', text)
    if match:
        return float(match.group(1)), int(match.group(2))
    return None, None

for si, src in enumerate(source_data):
    src_ex_val, src_ex_unc = extract_val_unc(src['Ex'])
    src_eg_val, src_eg_unc = extract_val_unc(src['Eg'])
    
    print(f"\n--- Source #{si}: Ex={src['Ex']} Eg={src['Eg']} Mult={src['Assignment']} ---")
    
    # Find matching level (within 1 keV tolerance since energies may be rounded)
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
        print(f"  NO MATCHING LEVEL FOUND for Ex={src['Ex']}")
        continue
    
    print(f"  Matched level: E={matched_level['E']} J={matched_level['J']}")
    
    # Find matching gamma
    matched_gamma = None
    for g in matched_level['gammas']:
        try:
            g_e = float(g['E'])
        except:
            continue
        if src_eg_val is not None and abs(g_e - src_eg_val) < 0.2:
            matched_gamma = g
            break
    
    if matched_gamma is None:
        print(f"  NO MATCHING GAMMA FOUND for Eg={src['Eg']}")
        continue
    
    print(f"  Matched gamma: E={matched_gamma['E']} RI={matched_gamma['RI']} M={matched_gamma['M']} C={matched_gamma['C']} Q={matched_gamma['Q']}")
    print(f"  cG comments: {matched_gamma['c_comments']}")
