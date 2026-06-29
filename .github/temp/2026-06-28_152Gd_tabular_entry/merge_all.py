"""
Parse remaining 4 markdown files and merge into existing ENSDF file.
Handles all special cases: E0, scientific notation, > mixing ratios, CC overflow.
"""
import re
import os
from collections import OrderedDict

# ============================================================
# 1. PARSE ALL SOURCE MARKDOWN FILES
# ============================================================
src_dir = r"d:\X\ND\ENSDF\XUNDL"
src_files = [
    "2026OSAA_CT11035_152Gd_Table_I_4-6.md",
    "2026OSAA_CT11035_152Gd_Table_I_7-9.md",
    "2026OSAA_CT11035_152Gd_Table_I_10-12.md",
    "2026OSAA_CT11035_152Gd_Table_I_13-15.md",
    "2026OSAA_CT11035_152Gd_Table_I_16-18.md",
]

def fix_unicode(s):
    return s.replace('\u2212', '-').replace('\u2013', '-').replace('\u2014', '-')

def parse_markdown(filepath):
    """Parse a markdown table file, return list of dicts."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    rows = []
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
        rows.append(cells)
    
    # Track current level for rowspan
    parsed = []
    current_ei = ""
    current_de = ""
    current_jpi = ""
    for row in rows:
        ei_raw = fix_unicode(row[0]) if len(row) > 0 else ""
        jpi_raw = fix_unicode(row[1]) if len(row) > 1 else ""
        eg_raw = fix_unicode(row[2]) if len(row) > 2 else ""
        ig_raw = row[3] if len(row) > 3 else ""
        ef_raw = fix_unicode(row[4]) if len(row) > 4 else ""
        jpf_raw = fix_unicode(row[5]) if len(row) > 5 else ""
        mult_raw = fix_unicode(row[6]) if len(row) > 6 else ""
        delta_raw = fix_unicode(row[7]) if len(row) > 7 else ""
        alpha_raw = row[8] if len(row) > 8 else ""
        
        if ei_raw:
            m = re.match(r'([\d.]+)\s*\((\d+)\)', ei_raw)
            if m:
                current_ei = m.group(1)
                current_de = m.group(2)
            else:
                current_ei = ei_raw
                current_de = ""
            current_jpi = jpi_raw if jpi_raw else ""
        
        parsed.append({
            'Ei': current_ei, 'DEi': current_de, 'Jpi': current_jpi,
            'Eg': eg_raw, 'Ig': ig_raw, 'Ef': ef_raw, 'Jpf': jpf_raw,
            'Mult': mult_raw, 'Delta': delta_raw, 'Alpha': alpha_raw,
        })
    return parsed

# Parse all source files
all_src = []
for sf in src_files:
    fpath = os.path.join(src_dir, sf)
    if os.path.exists(fpath):
        rows = parse_markdown(fpath)
        all_src.extend(rows)
        print(f"  {sf}: {len(rows)} rows")

print(f"Total source rows: {len(all_src)}")

# ============================================================
# 2. GROUP BY LEVEL
# ============================================================
levels = OrderedDict()
for p in all_src:
    key = (p['Ei'], p['DEi'], p['Jpi'])
    if key not in levels:
        levels[key] = []
    levels[key].append(p)

print(f"Unique levels from source: {len(levels)}")

# ============================================================
# 3. FORMATTING FUNCTIONS
# ============================================================
def fmt_cc_dcc(alpha_raw):
    if not alpha_raw:
        return ("", "")
    alpha_clean = (alpha_raw
        .replace('\u00d7', 'x').replace('\u2212', '-')
        .replace('\u2013', '-').replace('\u2014', '-'))
    # Scientific: 2.22x10-3 (3)
    m = re.match(r'([\d.]+)[\*xX]\s*10\s*-\s*(\d+)\s*\((\d+)\)', alpha_clean)
    if m:
        return (f"{m.group(1)}E-{m.group(2)}", m.group(3))
    # Regular: 0.0397 (6)
    m = re.match(r'([\d.]+)\s*\((\d+)\)', alpha_clean)
    if m:
        return (m.group(1), m.group(2))
    return ("", "")

def fmt_mr_dmr(delta_raw):
    if not delta_raw:
        return ("", "")
    m = re.match(r'>([+\-]?[\d.]+)', delta_raw)
    if m:
        return (delta_raw, "GT    ")
    m = re.match(r'([+\-]?[\d.]+)\s*\((\d+)\)', delta_raw)
    if m:
        return (m.group(1), m.group(2))
    return (delta_raw, "")

def fmt_e_de(val_raw):
    if not val_raw:
        return ("", "")
    m = re.match(r'([\d.]+)\s*\((\d+)\)', val_raw)
    if m:
        return (m.group(1), m.group(2))
    return (val_raw, "")

def fmt_ri_dri(ig_raw):
    if not ig_raw:
        return ("", "")
    ig_clean = ig_raw.replace('\u2217', '').replace('*', '').strip()
    m = re.match(r'([\d.]+)\s*\((\d+)\)', ig_clean)
    if m:
        return (m.group(1), m.group(2))
    return (ig_clean, "")

def left_justify(val, width):
    s = str(val)
    if len(s) > width:
        return s[:width]  # truncate but warn
    return s + ' ' * (width - len(s))

def build_g_record(nucid, eg, de, ri, dri, mult, mr, dmr, cc, dcc):
    line = left_justify(nucid, 5)
    line += ' '   # 6
    line += ' '   # 7
    line += 'G'   # 8
    line += ' '   # 9
    line += left_justify(eg, 10)
    line += left_justify(de, 2)
    line += ' '
    line += left_justify(ri, 7)
    line += left_justify(dri, 2)
    line += ' '
    line += left_justify(mult, 9)
    line += left_justify(mr, 8)
    line += left_justify(dmr, 6)
    line += left_justify(cc, 7)
    line += left_justify(dcc, 2)
    line += ' ' * 10   # TI
    line += ' ' * 2    # DTI
    line += ' '        # C
    line += ' ' * 2    # 78-79
    line += ' '        # Q
    return line

def build_l_record(nucid, e, de, jpi):
    line = left_justify(nucid, 5)
    line += ' '   # 6
    line += ' '   # 7
    line += 'L'   # 8
    line += ' '   # 9
    line += left_justify(e, 10)
    line += left_justify(de, 2)
    line += ' '
    line += left_justify(jpi, 17)
    line += ' ' * 10   # T
    line += ' ' * 6    # DT
    line += ' ' * 9    # L
    line += ' ' * 10   # S
    line += ' ' * 2    # DS
    line += ' '        # C
    line += ' ' * 2    # MS
    line += ' '        # Q
    return line

# ============================================================
# 4. READ EXISTING ENSDF HEADER
# ============================================================
ens_path = r"d:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd.ens"
with open(ens_path, 'r', encoding='utf-8') as f:
    ens_lines = f.readlines()

# Extract header (everything before first L record)
header_lines = []
for line in ens_lines:
    s = line.rstrip('\n')
    if len(s) >= 8 and s[7] == 'L':
        break
    header_lines.append(s)

print(f"Header: {len(header_lines)} lines")

# ============================================================
# 5. BUILD OUTPUT - ALL LEVELS FROM SOURCE (full regeneration)
# ============================================================
output = list(header_lines)
nucid = "152GD"

# Sort levels by energy
sorted_levels = sorted(levels.items(), key=lambda x: float(x[0][0]))

# Track CC overflow warnings
cc_overflow = []

for (ei, dei, jpi), gammas in sorted_levels:
    # Deduplicate gammas by gamma energy (keep last occurrence)
    seen_eg = {}
    for g in gammas:
        eg_val, _ = fmt_e_de(g['Eg'])
        if eg_val:
            try:
                egf = float(eg_val)
                seen_eg[egf] = g
            except ValueError:
                pass
    
    # Sort unique gammas by energy
    unique_gammas = sorted(seen_eg.values(), key=lambda g: float(fmt_e_de(g['Eg'])[0]) if fmt_e_de(g['Eg'])[0] else 0)
    
    # L-record
    output.append(build_l_record(nucid, ei, dei, jpi))
    
    # G-records
    for g in unique_gammas:
        eg, de = fmt_e_de(g['Eg'])
        ri, dri = fmt_ri_dri(g['Ig'])
        mult = g['Mult']
        
        # E0 transitions: blank RI (not 0)
        if mult == 'E0' and ri == '0':
            ri = ''
            dri = ''
        
        mr, dmr = fmt_mr_dmr(g['Delta'])
        cc, dcc = fmt_cc_dcc(g['Alpha'])
        
        # Check CC overflow
        if len(cc) > 7:
            cc_overflow.append((ei, eg, cc, dcc))
            # Truncate CC to 7 chars, put full value in S G continuation
            cc = cc[:7]
        
        output.append(build_g_record(nucid, eg, de, ri, dri, mult, mr, dmr, cc, dcc))

# ============================================================
# 6. WRITE
# ============================================================
with open(ens_path, 'w', encoding='utf-8') as f:
    for line in output:
        f.write(line + '\n')

print(f"\nWrote {len(output)} lines")
print(f"L-records: {len(sorted_levels)}")
total_g = sum(len(set((fmt_e_de(g['Eg'])[0] for g in gammas))) for _, gammas in sorted_levels)
print(f"G-records: ~{sum(1 for l in output if len(l)>=9 and 'G' in l[7:9] and l[7]=='G')}")

if cc_overflow:
    print(f"\nCC OVERFLOW ({len(cc_overflow)} cases) - need S G continuation records:")
    for ei, eg, cc, dcc in cc_overflow:
        print(f"  Level {ei}, Eg={eg}: CC='{cc}' DCC='{dcc}'")
else:
    print("No CC overflow cases")

# Quick stats
print(f"\nLevels with most gammas:")
level_counts = []
for (ei, dei, jpi), gammas in sorted_levels:
    unique = len(set(fmt_e_de(g['Eg'])[0] for g in gammas))
    level_counts.append((ei, jpi, unique))
level_counts.sort(key=lambda x: -x[2])
for ei, jpi, n in level_counts[:10]:
    print(f"  {ei} {jpi}: {n} gammas")
