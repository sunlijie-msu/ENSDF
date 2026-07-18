import re
with open('d:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd.ens', 'r') as f:
    lines = f.readlines()

ac_entries = []
level = None
g_eg = None

for i, line in enumerate(lines):
    if len(line) < 80: continue
    c6 = line[5]; c7 = line[6]; c8 = line[7]
    
    if c8 == 'L' and c7 == ' ':
        e = line[9:19].strip()
        try: level = float(e)
        except: level = None
        g_eg = None
        continue
    
    if c8 == 'G' and c7 == ' ' and c6 == ' ':
        eg = line[9:19].strip()
        try:
            float(eg)
            g_eg = eg
        except: pass
        continue
    
    if c8 == 'G' and c7 == 'c':
        comment = line[9:].strip()
        if 'A{-0}' not in comment and 'A{-2}' not in comment:
            continue
        
        full = comment
        j = i + 1
        while j < len(lines):
            nl = lines[j]
            if len(nl) >= 80 and nl[7] == 'G' and nl[6] == 'c' and nl[5] != ' ':
                full += ' ' + nl[9:].strip()
                j += 1
            else:
                break
        
        m = re.search(r'\$(\d+\.?\d*)\s*-\s*(\d+\.?\d*)\s*\|g\|g', full)
        if m and level and g_eg:
            ac_entries.append({
                'level': level, 'eg1': g_eg, 'eg2': m.group(2),
                'comment': full, 'line': i
            })

print(f'AC entries: {len(ac_entries)}')
for e in ac_entries[:3]:
    print(f'  L={e["level"]:.1f} Eg1={e["eg1"]} Eg2={e["eg2"]}')
for e in ac_entries:
    try: float(e['eg1'])
    except: print(f'BAD eg1: {e["eg1"]!r}')

# Also check Table IV matching
with open('d:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd_Table_IV.md', 'r', encoding='utf-8') as f:
    md = f.readlines()

table = []
for l in md:
    s = l.strip()
    if not s.startswith('| '): continue
    if '$' in s or '---' in s: continue
    parts = [p.strip() for p in s.split('|')][1:-1]
    if len(parts) < 12: continue
    table.append({'E': parts[0], 'g1': parts[1], 'g2': parts[2],
                  'A0': parts[3], 'A2': parts[4], 'A4': parts[5], 'd1': parts[11]})

print(f'\nTable IV rows: {len(table)}')

# Match
matched = 0
unmatched_table = []
for tr in table:
    found = False
    for ee in ac_entries:
        if abs(float(tr['E']) - ee['level']) < 0.2:
            try:
                if abs(float(tr['g1']) - float(ee['eg1'])) < 0.2 and abs(float(tr['g2']) - float(ee['eg2'])) < 0.2:
                    found = True; matched += 1; break
            except: pass
    if not found:
        # Only flag if table row has A values
        if tr['A0'].strip() or tr['A2'].strip():
            unmatched_table.append(tr)

print(f'Matched: {matched}')
print(f'Unmatched (with AC data): {len(unmatched_table)}')
for tr in unmatched_table[:5]:
    print(f'  L={tr["E"]} g={tr["g1"]}-{tr["g2"]} A0={tr["A0"]} A2={tr["A2"]}')
