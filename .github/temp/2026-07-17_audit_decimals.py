"""
Audit ALL delta values: compare decimal places between Table IV and ENSDF.
Table IV format: 0.00 (20) = 0.00 +/- 0.20 -> ENSDF should be |d=0.00 {I20}
But ENSDF incorrectly has |d=0.0 {I20} = 0.0 +/- 2.0  (10x too large!)
"""
import re

# Parse ENSDF deltas
with open('d:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd.ens', 'r') as f:
    lines = f.readlines()

ensdf_deltas = {}  # (level, eg1, eg2) -> (val_str, unc_str, decimal_places, line_no)
current_level = None
current_eg = None

for i, line in enumerate(lines):
    if len(line) < 80: continue
    c6, c7, c8 = line[5], line[6], line[7]
    
    if c8 == 'L' and c7 == ' ':
        try: current_level = float(line[9:19].strip())
        except: current_level = None
        current_eg = None
    elif c8 == 'G' and c7 == ' ' and c6 == ' ':
        try: float(line[9:19].strip()); current_eg = line[9:19].strip()
        except: pass
    elif c8 == 'G' and c7 == 'c':
        # Find |d= in comment
        cm = line[9:].strip()
        # Also check continuation
        j = i + 1
        while j < len(lines):
            nl = lines[j]
            if len(nl) >= 80 and nl[7] == 'G' and nl[6] == 'c' and nl[5] != ' ':
                cm += ' ' + nl[9:].strip()
                j += 1
            else: break
        
        # Find cascade pattern
        m_cas = re.search(r'\$(\d+\.?\d*)\s*-\s*(\d+\.?\d*)\s*\|g\|g', cm)
        if not m_cas: continue
        eg2 = m_cas.group(2)
        
        # Find delta
        m_d = re.search(r'\|d=([+-]?[\d.]+)\s*\{I(\d+)\}', cm)
        if not m_d: continue
        
        d_val = m_d.group(1)  # e.g., '0.0' or '0.00'
        d_unc = m_d.group(2)  # e.g., '20'
        
        # Count decimal places
        if '.' in d_val:
            dec = len(d_val.split('.')[1])
        else:
            dec = 0
        
        key = (current_level, current_eg, eg2)
        ensdf_deltas[key] = (d_val, d_unc, dec, i)

print(f"ENSDF deltas: {len(ensdf_deltas)}")

# Parse Table IV deltas
with open('d:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd_Table_IV.md', 'r', encoding='utf-8') as f:
    md = f.readlines()

table_deltas = {}
for l in md:
    s = l.strip()
    if not s.startswith('| ') or '$' in s or '---' in s: continue
    p = [x.strip() for x in s.split('|')][1:-1]
    if len(p) < 12: continue
    d1 = p[11].strip()
    if not d1: continue
    key = (p[0], p[1], p[2])  # (E_level, Eg1, Eg2)
    table_deltas[key] = d1

print(f"Table IV deltas: {len(table_deltas)}")

# Compare decimal places
mismatches = []
for key, td in table_deltas.items():
    # Find matching ENSDF entry
    ek = None
    for k in ensdf_deltas:
        try:
            if abs(float(key[0]) - k[0]) < 1.0 and abs(float(key[1]) - float(k[1])) < 1.0 and abs(float(key[2]) - float(k[2])) < 1.0:
                ek = k; break
        except: pass
    if not ek: continue
    
    e_val, e_unc, e_dec, e_line = ensdf_deltas[ek]
    
    # Parse Table IV: "0.00 (20)" or ">39"
    if td.startswith('>'):
        continue  # skip limits
    
    m = re.match(r'(-?[\d.]+)\s*\((\d+)\)', td)
    if not m: continue
    
    t_val = m.group(1)
    t_unc = m.group(2)
    
    # Count Table IV decimal places
    if '.' in t_val:
        t_dec = len(t_val.split('.')[1])
    else:
        t_dec = 0
    
    # Compare
    if t_dec != e_dec:
        mismatches.append((key, t_val, t_dec, t_unc, e_val, e_dec, e_unc, e_line))

print(f"\nDecimal-place mismatches: {len(mismatches)}")
for m in mismatches:
    key, tv, td, tu, ev, ed, eu, line = m
    print(f"  L={key[0]:>6} g={key[1]:>7}-{key[2]:>4}  TableIV: {tv}({tu}) ({td}dp)  ENSDF: {ev}({eu}) ({ed}dp)  ENSDF line {line+1}")
