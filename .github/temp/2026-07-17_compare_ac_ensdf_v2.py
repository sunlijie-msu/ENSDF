"""
Compare angular correlation data between Table IV and ENSDF.
ENSDF format: col 0-4=NUCID, col 5=continuation, col 6=c-flag, col 7=record type
cG line: col 6='c', col 7='G'
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
    if '$' in s or '---' in s: continue
    parts = [p.strip() for p in s.split('|')]
    parts = parts[1:-1]
    if len(parts) < 12: continue
    try:
        table_rows.append({
            'E_level': parts[0], 'Eg1': parts[1], 'Eg2': parts[2],
            'A0': parts[3], 'A2': parts[4], 'A4': parts[5],
            'E2': parts[6], 'E3': parts[7],
            'J1': parts[8], 'J2': parts[9], 'J3': parts[10],
            'delta': parts[11]
        })
    except:
        pass

print(f"Table IV rows: {len(table_rows)}")

# ============================================================
# PARSE ENSDF
# ============================================================
with open('d:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd.ens', 'r') as f:
    lines = f.readlines()

# First pass: find level energies
levels = {}  # line_idx -> (energy, line)
for i, line in enumerate(lines):
    if len(line) < 80: continue
    # Col 7 (0-idx) = record type, Col 6 = must be blank for data records
    if line[7] == 'L' and line[6] == ' ':
        e_str = line[9:19].strip()
        if e_str:
            try:
                e_val = float(e_str)
                levels[i] = e_val
            except:
                pass

print(f"ENSDF L-records: {len(levels)}")

# Second pass: find G-records with cG comments
# Strategy: scan lines, track current level
ensdf_entries = []
current_level_e = None
current_g_eg = None
current_g_line_idx = None

i = 0
while i < len(lines):
    line = lines[i]
    if len(line) < 80:
        i += 1
        continue
    
    rt = line[7]  # record type at col 8
    cf = line[6]  # comment flag at col 7 (space or 'c')
    
    # L record
    if rt == 'L' and cf == ' ':
        e_str = line[9:19].strip()
        if e_str:
            try:
                current_level_e = float(e_str)
                current_g_eg = None
                current_g_line_idx = None
            except:
                pass
    
    # G record
    elif rt == 'G' and cf == ' ':
        eg_str = line[9:19].strip()
        if eg_str:
            try:
                current_g_eg = eg_str
                current_g_line_idx = i
            except:
                pass
    
    # cG comment line (col 6='c', col 7='G')
    elif rt == 'G' and cf == 'c':
        # This is a comment on the current G-record
        comment_text = line[9:].strip()
        
        # Collect continuation lines (2cG, 3cG, etc.)
        full_comment = comment_text
        j = i + 1
        while j < len(lines):
            nl = lines[j]
            if len(nl) >= 80 and nl[7] == 'G' and nl[6] == 'c':
                # Check if it's continuation: col 5 should not be blank
                # Actually, 2cG: col 5='2', col 6='c', col 7='G'
                # But regular cG: col 5=' ', col 6='c', col 7='G'
                if nl[5] != ' ':  # continuation
                    full_comment += ' ' + nl[9:].strip()
                    j += 1
                else:
                    break  # next cG for next gamma
            else:
                break
        
        # Check if this cG contains angular correlation data
        if 'A{-0}' in full_comment or 'A{-2}' in full_comment:
            # Extract $XXX-YYY pattern
            m_cascade = re.search(r'\$(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*\|g\|g', full_comment)
            if m_cascade and current_level_e is not None and current_g_eg is not None:
                eg_from_comment = m_cascade.group(1)
                eg2 = m_cascade.group(2)
                
                # Parse A values and delta
                a0 = None; a2 = None; a4 = None; delta = None
                
                m = re.search(r'A\{-0\}=([\d.]+)\s*\{I(\d+)\}', full_comment)
                if m:
                    a0 = (m.group(1), m.group(2))
                
                m = re.search(r'A\{-2\}=(-?[\d.]+)\s*\{I(\d+)\}', full_comment)
                if m:
                    a2 = (m.group(1), m.group(2))
                
                m = re.search(r'A\{-4\}=(-?[\d.]+)\s*\{I(\d+)\}', full_comment)
                if m:
                    a4 = (m.group(1), m.group(2))
                
                # Mixing ratio: |d=... in ENSDF
                m = re.search(r'\|d=([+-]?[\d.]+(?:\s*[<>GL]?[T]?\s*)?)\s*(?:\{I(\d+)\})?', full_comment)
                if m:
                    dv = m.group(1).strip()
                    du = m.group(2) if m.lastindex and m.lastindex >= 2 else None
                    delta = (dv, du)
                
                ensdf_entries.append({
                    'level': current_level_e,
                    'eg1': current_g_eg,
                    'eg2': eg2,
                    'A0': a0, 'A2': a2, 'A4': a4,
                    'delta': delta,
                    'line_idx': i,
                    'full_comment': full_comment
                })
        
        i = j - 1  # -1 because i += 1 at end of loop
    i += 1

print(f"ENSDF angular correlation entries: {len(ensdf_entries)}")

# ============================================================
# COMPARE
# ============================================================
print("\n=== DISCREPANCIES ===")

def parse_tv(t_str):
    """Parse '0.8860 (6)' -> ('0.8860', '6')"""
    m = re.match(r'(-?[\d.]+)\s*\((\d+)\)', t_str.strip())
    if m:
        return m.group(1), m.group(2)
    return None, None

def parse_tv_or_limit(t_str):
    """Handle '>39' or '0.006 (6)'"""
    t_str = t_str.strip()
    if t_str.startswith('>'):
        return '>' + t_str[1:].strip(), None
    if t_str.startswith('<'):
        return '<' + t_str[1:].strip(), None
    return parse_tv(t_str)

diffs = []
for tr in table_rows:
    e_level = tr['E_level']
    eg1 = tr['Eg1']
    eg2 = tr['Eg2']
    
    # Find matching ENSDF entry
    match = None
    for ee in ensdf_entries:
        if abs(float(e_level) - ee['level']) < 0.2:
            # Check gamma energies
            if abs(float(eg1) - float(ee['eg1'])) < 0.2 and abs(float(eg2) - float(ee['eg2'])) < 0.2:
                match = ee
                break
    
    if match is None:
        # Check if this cascade even has angular correlation data in Table IV
        if tr['A0'] or tr['A2'] or tr['A4']:
            diffs.append(('MISSING_ENSDF', tr, None))
        continue
    
    # Compare A values
    for field, t_str, e_tuple in [('A0', tr['A0'], match['A0']),
                                    ('A2', tr['A2'], match['A2']),
                                    ('A4', tr['A4'], match['A4'])]:
        if not t_str or not t_str.strip():
            continue
        tv, tu = parse_tv(t_str)
        if e_tuple is None:
            diffs.append(('MISSING_FIELD', f"L={e_level} g={eg1}-{eg2}", field, t_str, 'NONE', match['line_idx']))
            continue
        ev, eu = e_tuple
        if tv != ev or tu != eu:
            e_str = f"{ev} ({eu})" if eu else ev
            diffs.append(('VALUE', f"L={e_level} g={eg1}-{eg2}", field, t_str, e_str, match['line_idx']))
    
    # Compare delta
    t_delta = tr['delta'].strip() if tr['delta'] else ''
    if t_delta:
        tv, tu = parse_tv_or_limit(t_delta)
        if match['delta'] is None:
            if tv:
                diffs.append(('MISSING_DELTA', f"L={e_level} g={eg1}-{eg2}", 'delta', t_delta, 'NONE', match['line_idx']))
        else:
            ev, eu = match['delta']
            # Normalize delta comparison
            e_str = f"{ev} ({eu})" if eu else ev
            if t_delta != e_str:
                # Check if values match numerically
                try:
                    if tv and tv.startswith('>'):
                        if ev.startswith('>'):
                            if abs(float(tv[1:]) - float(ev[1:])) > 0.1:
                                diffs.append(('VALUE', f"L={e_level} g={eg1}-{eg2}", 'delta', t_delta, e_str, match['line_idx']))
                    elif tv and ev:
                        if abs(float(tv) - float(ev)) > 0.001:
                            diffs.append(('VALUE', f"L={e_level} g={eg1}-{eg2}", 'delta', t_delta, e_str, match['line_idx']))
                except:
                    diffs.append(('VALUE', f"L={e_level} g={eg1}-{eg2}", 'delta', t_delta, e_str, match['line_idx']))

# Also check ENSDF entries NOT in Table IV
table_keys = set()
for tr in table_rows:
    table_keys.add((tr['E_level'], tr['Eg1'], tr['Eg2']))

for ee in ensdf_entries:
    key = (str(int(ee['level'])) if ee['level'] == int(ee['level']) else str(ee['level']), 
           ee['eg1'], ee['eg2'])
    if key not in table_keys:
        # Try float matching
        found = False
        for tk in table_keys:
            try:
                if abs(float(tk[0]) - ee['level']) < 0.2 and abs(float(tk[1]) - float(ee['eg1'])) < 0.2 and abs(float(tk[2]) - float(ee['eg2'])) < 0.2:
                    found = True
                    break
            except:
                pass
        if not found:
            print(f"  ENSDF-only: L={ee['level']} g={ee['eg1']}-{ee['eg2']}")

print(f"\nDiscrepancies: {len(diffs)}")
for d in diffs[:40]:
    if d[0] == 'VALUE':
        _, key, field, t_val, e_val, line = d
        print(f"  {key} {field}: TableIV={t_val} ENSDF={e_val}  (ENSDF line {line+1})")
    elif d[0] == 'MISSING_FIELD':
        _, key, field, t_val, e_val, line = d
        print(f"  {key} {field}: TableIV={t_val} ENSDF=MISSING  (ENSDF line {line+1})")
    elif d[0] == 'MISSING_DELTA':
        _, key, field, t_val, e_val, line = d
        print(f"  {key} {field}: TableIV={t_val} ENSDF=MISSING  (ENSDF line {line+1})")
    elif d[0] == 'MISSING_ENSDF':
        _, tr, _ = d
        print(f"  MISSING_ENSDF: L={tr['E_level']} g={tr['Eg1']}-{tr['Eg2']} A0={tr['A0']} A2={tr['A2']} A4={tr['A4']}")
