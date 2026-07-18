"""
Update ENSDF cG comment lines to match Table IV angular correlation data.
Handles:
  A) Fix A-value uncertainties  
  B) Add missing delta (mixing ratio) values
"""
import re

with open('d:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd.ens', 'r') as f:
    lines = f.readlines()

# Build Table IV lookup
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

# Parse ENSDF and build list of edits
# Each edit: (line_index, action, detail)
edits = []

level = None; g_eg = None
for i, line in enumerate(lines):
    if len(line) < 80: continue
    c6 = line[5]; c7 = line[6]; c8 = line[7]
    
    if c8 == 'L' and c7 == ' ':
        try: level = float(line[9:19].strip())
        except: level = None
        g_eg = None
    elif c8 == 'G' and c7 == ' ' and c6 == ' ':
        try: float(line[9:19].strip()); g_eg = line[9:19].strip()
        except: pass
    elif c8 == 'G' and c7 == 'c':
        if 'A{-0}' not in line and 'A{-2}' not in line: continue
        if not level or not g_eg: continue
        
        cm_text = line[9:].strip()
        m_cascade = re.search(r'\$(\d+\.?\d*)\s*-\s*(\d+\.?\d*)\s*\|g\|g', cm_text)
        if not m_cascade: continue
        eg2 = m_cascade.group(2)
        
        # Find Table IV match
        tkey = None
        for k in tb:
            try:
                if abs(float(k[0]) - level) < 1.0 and abs(float(k[1]) - float(g_eg)) < 1.0 and abs(float(k[2]) - float(eg2)) < 1.0:
                    tkey = k; break
            except: pass
        if not tkey: continue
        trow = tb[tkey]
        
        # ---- CATEGORY A: Fix uncertainties ----
        for aname, idx in [('A0',0), ('A2',2), ('A4',4)]:
            tv = trow[aname].strip()
            if not tv: continue
            m = re.match(r'(-?[\d.]+)\s*\((\d+)\)', tv)
            if not m: continue
            tv_v, tv_u = m.group(1), m.group(2)
            
            pattern = r'(A\{-'+str(idx)+r'\}=)(-?[\d.]+)(\s*\{I)(\d+)(\})'
            m2 = re.search(pattern, line)
            if not m2: continue
            ev_v, ev_u = m2.group(2), m2.group(4)
            
            if tv_v == ev_v and tv_u != ev_u:
                old = m2.group(0)
                new = m2.group(1) + ev_v + m2.group(3) + tv_u + m2.group(5)
                edits.append((i, 'fix_unc', old, new, f'{aname}={tv_v} ({ev_u}->{tv_u})'))
        
        # ---- CATEGORY B: Add missing deltas ----
        td = trow['d1'].strip()
        if not td: continue
        
        # Check if delta already exists in this cascade's comments
        has_delta = False
        delta_text = ''
        
        # Check main cG line and its continuations
        combined = cm_text
        j = i + 1
        while j < len(lines):
            nl = lines[j]
            if len(nl) >= 80 and nl[7] == 'G' and nl[6] == 'c' and nl[5] != ' ':
                combined += ' ' + nl[9:].strip()
                j += 1
            else:
                break
        
        if '|d=' in combined:
            # Delta exists, check if it matches Table IV
            dm = re.search(r'\|d=([+-]?[\d.]+(?:\s*[<>GL]?[T]?\s*)?)\s*(?:\{I(\d+)\})?', combined)
            if dm:
                dv = dm.group(1).strip()
                du = dm.group(2) if dm.lastindex and dm.lastindex >= 2 else ''
                
                # Build ENSDF delta string
                if du:
                    e_delta_str = f'|d={dv} {{I{du}}}'
                else:
                    e_delta_str = f'|d={dv}'
                
                # Build Table IV delta string
                if td.startswith('>'):
                    t_delta_str = f'|d={td}'
                else:
                    mt = re.match(r'(-?[\d.]+)\s*\((\d+)\)', td)
                    if mt:
                        sign = '+' if float(mt.group(1)) >= 0 else ''
                        t_delta_str = f'|d={sign}{mt.group(1)} {{I{mt.group(2)}}}'
                    else:
                        t_delta_str = f'|d={td}'
                
                if e_delta_str != t_delta_str:
                    # Need to fix delta value
                    edits.append((i, 'fix_delta', e_delta_str, t_delta_str, f'delta {e_delta_str}->{t_delta_str}'))
        else:
            # Delta missing - need to add
            if td.startswith('>'):
                new_delta = f'|d={td}'
            else:
                mt = re.match(r'(-?[\d.]+)\s*\((\d+)\)', td)
                if mt:
                    sign = '+' if float(mt.group(1)) >= 0 else ''
                    new_delta = f'|d={sign}{mt.group(1)} {{I{mt.group(2)}}}'
                else:
                    new_delta = f'|d={td}'
            edits.append((i, 'add_delta', '', new_delta, f'add {new_delta}'))

print(f"Total edits: {len(edits)}")
unc_fixes = [e for e in edits if e[1] == 'fix_unc']
delta_adds = [e for e in edits if e[1] == 'add_delta']
delta_fixes = [e for e in edits if e[1] == 'fix_delta']
print(f"  fix_unc: {len(unc_fixes)}")
print(f"  add_delta: {len(delta_adds)}")
print(f"  fix_delta: {len(delta_fixes)}")

# Apply edits to ENSDF lines
# Build a map: line_index -> list of edits
from collections import defaultdict
edit_map = defaultdict(list)
for e in edits:
    edit_map[e[0]].append(e)

# Process edits
output = []
i = 0
while i < len(lines):
    line = lines[i]
    
    if i in edit_map:
        line_edits = edit_map[i]
        
        # Handle fix_unc: modify the A-value uncertainty inline
        unc_fix_applied = False
        for e in line_edits:
            if e[1] == 'fix_unc':
                old_str, new_str = e[2], e[3]
                if old_str in line:
                    line = line.replace(old_str, new_str)
                    unc_fix_applied = True
        
        # Handle add_delta and fix_delta: modify/add delta in comment section
        delta_edits = [e for e in line_edits if e[1] in ('add_delta', 'fix_delta')]
        
        if delta_edits:
            # Find the last continuation line for this cG block
            last_cont_idx = i
            j = i + 1
            while j < len(lines):
                nl = lines[j]
                if len(nl) >= 80 and nl[7] == 'G' and nl[6] == 'c' and nl[5] != ' ':
                    last_cont_idx = j
                    j += 1
                else:
                    break
            
            # For add_delta: append to last continuation, or create new 2cG line
            for de in delta_edits:
                if de[1] == 'add_delta':
                    new_delta = de[3]
                    # Check if there's a continuation line we can append to
                    if last_cont_idx > i:
                        # Modify last continuation line to include delta
                        cont_line = lines[last_cont_idx]
                        # Find the end of the text content and append
                        # Strip trailing space and newline
                        stripped = cont_line.rstrip()
                        # Check if line has room (before col 80)
                        if len(stripped) + len(', ' + new_delta) <= 80:
                            # Append to this continuation line
                            new_cont = stripped + ', ' + new_delta
                            # Pad to 80 chars
                            new_cont = new_cont.ljust(80)
                            # Store edit for later
                            edit_map[last_cont_idx] = edit_map.get(last_cont_idx, []) + [('replace', new_cont)]
                        else:
                            # Need new continuation line
                            # Generate next continuation number
                            # Count existing continuations
                            cont_num = 2
                            for jj in range(i+1, last_cont_idx+1):
                                c_digit = lines[jj][5]
                                if c_digit.isdigit():
                                    cont_num = max(cont_num, int(c_digit) + 1)
                            # Build new continuation line
                            nucid = line[0:5]
                            prefix = f'{nucid}{cont_num}cG '
                            content = new_delta
                            new_line = (prefix + content).ljust(80) + '\n'
                            edit_map[i] = edit_map.get(i, []) + [('add_after', new_line, last_cont_idx)]
                    else:
                        # No continuation, create 2cG
                        # Check if cG line has room before col 80
                        stripped = line.rstrip()
                        if len(stripped) + len(', ' + new_delta) <= 80:
                            new_line = stripped + ', ' + new_delta
                            new_line = new_line.ljust(80) + '\n'
                            line = new_line
                        else:
                            # Need continuation
                            nucid = line[0:5]
                            new_line = f'{nucid}2cG {new_delta}'.ljust(80) + '\n'
                            edit_map[i] = edit_map.get(i, []) + [('add_after', new_line, i)]
                
                elif de[1] == 'fix_delta':
                    old_delta, new_delta = de[2], de[3]
                    # Replace in the appropriate continuation line
                    for jj in range(i, last_cont_idx + 1):
                        if jj == i:
                            cl = line
                        else:
                            cl = lines[jj]
                        if old_delta in cl:
                            new_cl = cl.replace(old_delta, new_delta)
                            if jj == i:
                                line = new_cl
                            else:
                                edit_map[jj] = edit_map.get(jj, []) + [('replace', new_cl)]
                            break
        
        output.append(line)
    else:
        output.append(line)
    
    i += 1

# Second pass: apply any pending edits from edit_map
# Actually, the above approach is getting too complex for inline editing.
# Let me use a simpler approach: write the edits to a log and do them manually via replace_string_in_file.

# For now, just print the edits that need to be made
print("\n\n=== EDITS TO APPLY (by line number) ===")
for e in sorted(edits, key=lambda x: x[0]):
    line_no, action, old, new, desc = e
    print(f"L{line_no+1}: [{action}] {desc}")
    if old:
        print(f"    OLD: {old}")
    if new:
        print(f"    NEW: {new}")
