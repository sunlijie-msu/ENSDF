"""
Add missing mixing ratio (|d=) values to ENSDF cG comment lines.
Matches each cascade against Table IV, adds delta where missing.
"""
import re

with open('d:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd.ens', 'r') as f:
    lines = f.readlines()

# Load Table IV
with open('d:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd_Table_IV.md', 'r', encoding='utf-8') as f:
    md = f.readlines()
tb = {}
for l in md:
    s = l.strip()
    if not s.startswith('| ') or '$' in s or '---' in s: continue
    p = [x.strip() for x in s.split('|')][1:-1]
    if len(p) < 12: continue
    key = (p[0], p[1], p[2])
    tb[key] = {'A0':p[3], 'A2':p[4], 'A4':p[5], 'd1':p[11]}

# Parse ENSDF and build delta additions map
# delta_adds: list of (insert_after_line_idx, new_line_text)
delta_adds = []

level = None; g_eg = None
i = 0
while i < len(lines):
    line = lines[i]
    if len(line) < 80:
        i += 1; continue
    c6 = line[5]; c7 = line[6]; c8 = line[7]
    
    if c8 == 'L' and c7 == ' ':
        try: level = float(line[9:19].strip())
        except: level = None
        g_eg = None
    elif c8 == 'G' and c7 == ' ' and c6 == ' ':
        try: float(line[9:19].strip()); g_eg = line[9:19].strip()
        except: pass
    elif c8 == 'G' and c7 == 'c':
        if 'A{-0}' not in line and 'A{-2}' not in line:
            i += 1; continue
        if not level or not g_eg:
            i += 1; continue
        
        cm_text = line[9:].strip()
        m_cascade = re.search(r'\$(\d+\.?\d*)\s*-\s*(\d+\.?\d*)\s*\|g\|g', cm_text)
        if not m_cascade:
            i += 1; continue
        eg2 = m_cascade.group(2)
        
        # Find Table IV match
        tkey = None
        for k in tb:
            try:
                if abs(float(k[0]) - level) < 1.0 and abs(float(k[1]) - float(g_eg)) < 1.0 and abs(float(k[2]) - float(eg2)) < 1.0:
                    tkey = k; break
            except: pass
        if not tkey:
            i += 1; continue
        trow = tb[tkey]
        td = trow['d1'].strip()
        if not td:
            i += 1; continue
        
        # Check if delta already in this cascade's comments (main + continuations)
        combined = cm_text
        last_cont_idx = i
        j = i + 1
        while j < len(lines):
            nl = lines[j]
            if len(nl) >= 80 and nl[7] == 'G' and nl[6] == 'c' and nl[5] != ' ':
                combined += ' ' + nl[9:].strip()
                last_cont_idx = j
                j += 1
            else:
                break
        
        if '|d=' in combined:
            # Already has delta, skip
            i += 1; continue
        
        # Build delta text
        if td.startswith('>'):
            delta_str = f'|d={td}'
        else:
            mt = re.match(r'(-?[\d.]+)\s*\((\d+)\)', td)
            if mt:
                sign = '+' if float(mt.group(1)) >= 0 else ''
                delta_str = f'|d={sign}{mt.group(1)} {{I{mt.group(2)}}}'
            else:
                delta_str = f'|d={td}'
        
        # Determine where to add delta
        last_line = lines[last_cont_idx]
        stripped = last_line.rstrip()
        
        text_to_add = ', ' + delta_str
        
        if len(stripped) + len(text_to_add) <= 80:
            # Can fit on same line
            # Pad with spaces to 80 chars
            new_content = stripped + text_to_add
            new_line = new_content.ljust(80) + '\n'
            lines[last_cont_idx] = new_line
        else:
            # Need new continuation line
            # Determine next available continuation number
            cont_nums = set()
            for jj in range(i, last_cont_idx + 1):
                c = lines[jj][5]
                if c.isdigit():
                    cont_nums.add(int(c))
            next_cont = max(cont_nums) + 1 if cont_nums else 2
            
            nucid = line[0:5]
            prefix = f'{nucid}{next_cont}cG '
            content = delta_str
            new_line = (prefix + content).ljust(80) + '\n'
            delta_adds.append((last_cont_idx, new_line))
        
        i = j  # Skip past continuation lines
        continue
    
    i += 1

print(f"Delta additions needed: {len(delta_adds)}")
for idx, nl in delta_adds[:5]:
    print(f"  After L{idx+1}: {nl.rstrip()}")

# Apply insertions (in reverse order to preserve indices)
for insert_idx, new_line in sorted(delta_adds, key=lambda x: -x[0]):
    lines.insert(insert_idx + 1, new_line)

print(f"Lines after insertion: {len(lines)}")

# Write back
with open('d:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd.ens', 'w') as f:
    f.writelines(lines)

print("Done. File updated.")
