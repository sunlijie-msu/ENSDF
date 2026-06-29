"""
Spot-check validation: compare generated ENSDF records against source markdown.
Checks 15% random sample (~20 entries).
"""
import re
import random

# Read source
src_path = r"d:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Table_I_4-6.md"
with open(src_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Read ENSDF
ens_path = r"d:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd.ens"
with open(ens_path, 'r', encoding='utf-8') as f:
    ens_lines = f.readlines()

# Parse ENSDF records
ens_levels = {}  # energy -> {jpi, gammas: [{eg, de, ri, dri, mult, mr, dmr, cc, dcc}]}
current_level_e = None
for line in ens_lines:
    s = line.rstrip('\n')
    if len(s) < 80:
        continue
    if s[7] == 'L':
        e_str = s[9:19].strip()
        j_str = s[22:39].strip()
        if e_str:
            current_level_e = e_str
            ens_levels[current_level_e] = {'jpi': j_str, 'gammas': []}
    elif s[7] == 'G' and current_level_e:
        eg = s[9:19].strip()
        de = s[19:21].strip()
        ri = s[22:29].strip()
        dri = s[29:31].strip()
        mult = s[32:41].strip()
        mr = s[41:49].strip()
        dmr = s[49:55].strip()
        cc = s[55:62].strip()
        dcc = s[62:64].strip()
        ens_levels[current_level_e]['gammas'].append({
            'eg': eg, 'de': de, 'ri': ri, 'dri': dri,
            'mult': mult, 'mr': mr, 'dmr': dmr, 'cc': cc, 'dcc': dcc
        })

print(f"ENSDF levels: {len(ens_levels)}")
total_g = sum(len(v['gammas']) for v in ens_levels.values())
print(f"ENSDF gammas: {total_g}")

# Parse source markdown into same structure
lines = content.split('\n')
src_rows = []
for line in lines:
    line = line.strip()
    if not line.startswith('|'):
        continue
    if '$E_i$' in line or 'E_i$' in line:
        continue
    if ':---' in line:
        continue
    parts = line.split('|')
    if parts and parts[0] == '':
        parts = parts[1:]
    if parts and parts[-1] == '':
        parts = parts[:-1]
    cells = [c.strip() for c in parts]
    while len(cells) < 9:
        cells.append("")
    src_rows.append(cells)

# Build source structure
src_levels = {}
current_ei = None
for row in src_rows:
    ei_raw = row[0]
    jpi_raw = row[1]
    eg_raw = row[2]
    ig_raw = row[3]
    mult_raw = row[6]
    delta_raw = row[7] if len(row) > 7 else ""
    alpha_raw = row[8] if len(row) > 8 else ""
    
    if ei_raw:
        m = re.match(r'([\d.]+)\s*\((\d+)\)', ei_raw)
        if m:
            current_ei = m.group(1)
        else:
            current_ei = ei_raw
        if current_ei not in src_levels:
            src_levels[current_ei] = {'jpi': jpi_raw, 'gammas': []}
    
    # Parse gamma values
    m_eg = re.match(r'([\d.]+)\s*\((\d+)\)', eg_raw) if eg_raw else None
    eg_val = m_eg.group(1) if m_eg else eg_raw
    eg_unc = m_eg.group(2) if m_eg else ""
    
    ig_clean = ig_raw.replace('\u2217', '').replace('*', '').strip()
    m_ig = re.match(r'([\d.]+)\s*\((\d+)\)', ig_clean) if ig_clean else None
    ig_val = m_ig.group(1) if m_ig else ig_clean
    ig_unc = m_ig.group(2) if m_ig else ""
    
    # Alpha
    alpha_clean = alpha_raw.replace('\u00d7', 'x').replace('\u2212', '-')
    m_a = re.match(r'([\d.]+)[\*xX]\s*10\s*-\s*(\d+)\s*\((\d+)\)', alpha_clean)
    if m_a:
        cc_val = f"{m_a.group(1)}E-{m_a.group(2)}"
        cc_unc = m_a.group(3)
    else:
        m_a = re.match(r'([\d.]+)\s*\((\d+)\)', alpha_clean)
        if m_a:
            cc_val = m_a.group(1)
            cc_unc = m_a.group(2)
        else:
            cc_val = ""
            cc_unc = ""
    
    src_levels[current_ei]['gammas'].append({
        'eg': eg_val, 'de': eg_unc, 'ri': ig_val, 'dri': ig_unc,
        'mult': mult_raw, 'delta': delta_raw,
        'cc': cc_val, 'dcc': cc_unc
    })

print(f"Source levels: {len(src_levels)}")
total_src_g = sum(len(v['gammas']) for v in src_levels.values())
print(f"Source gammas: {total_src_g}")

# Map source Ei to ENSDF Ei (source may have different decimal places)
def find_matching_level(src_ei, ens_levels):
    """Find ENSDF level matching source energy."""
    src_f = float(src_ei)
    for ens_e in ens_levels:
        if abs(float(ens_e) - src_f) < 0.01:
            return ens_e
    return None

# Spot check: for each source level, check all gammas
errors = []
checked = 0
for src_ei, src_data in src_levels.items():
    ens_ei = find_matching_level(src_ei, ens_levels)
    if ens_ei is None:
        errors.append(f"Level {src_ei} not found in ENSDF")
        continue
    
    ens_data = ens_levels[ens_ei]
    
    # Match gammas by energy
    for sg in src_data['gammas']:
        matched = False
        for eg in ens_data['gammas']:
            try:
                if abs(float(eg['eg']) - float(sg['eg'])) < 0.005:
                    matched = True
                    checked += 1
                    # Check each field
                    if eg['de'] != sg['de']:
                        errors.append(f"  Eg={sg['eg']}: DE mismatch ENSDF='{eg['de']}' vs src='{sg['de']}'")
                    if eg['ri'] != sg['ri']:
                        errors.append(f"  Eg={sg['eg']}: RI mismatch ENSDF='{eg['ri']}' vs src='{sg['ri']}'")
                    if eg['dri'] != sg['dri']:
                        errors.append(f"  Eg={sg['eg']}: DRI mismatch ENSDF='{eg['dri']}' vs src='{sg['dri']}'")
                    if eg['mult'] != sg['mult']:
                        errors.append(f"  Eg={sg['eg']}: Mult mismatch ENSDF='{eg['mult']}' vs src='{sg['mult']}'")
                    if eg['cc'] != sg['cc']:
                        errors.append(f"  Eg={sg['eg']}: CC mismatch ENSDF='{eg['cc']}' vs src='{sg['cc']}'")
                    if eg['dcc'] != sg['dcc']:
                        errors.append(f"  Eg={sg['eg']}: DCC mismatch ENSDF='{eg['dcc']}' vs src='{sg['dcc']}'")
                    break
            except (ValueError, TypeError):
                pass
        if not matched:
            errors.append(f"  Gamma Eg={sg['eg']} from level {src_ei} not found in ENSDF")

print(f"\nChecked {checked} gamma entries")
print(f"Errors: {len(errors)}")
for e in errors[:30]:
    print(f"  {e}")
if len(errors) > 30:
    print(f"  ... and {len(errors)-30} more errors")

# Also check level Jpi
for src_ei, src_data in src_levels.items():
    ens_ei = find_matching_level(src_ei, ens_levels)
    if ens_ei:
        # Normalize Jpi comparison (Unicode minus to ASCII)
        src_jpi = src_data['jpi'].replace('\u2212', '-')
        ens_jpi = ens_levels[ens_ei]['jpi']
        if src_jpi and ens_jpi and src_jpi != ens_jpi:
            errors.append(f"Level {src_ei}: Jpi mismatch ENSDF='{ens_jpi}' vs src='{src_jpi}'")

print(f"\nTotal errors after Jpi check: {len(errors)}")
for e in errors[-10:]:
    print(f"  {e}")
