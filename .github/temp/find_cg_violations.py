#!/usr/bin/env python3
"""
Scan ENSDF file for cG comment ordering violations.
Proper order: E$ < RI$ < M$ < MR$ < General$
Focus: Ensure RI before M and before MR
"""

import re

# Read file
with open('A35/Cl35/new/Cl35_34s_p_g.ens', 'r') as f:
    lines = f.readlines()

# Define cG identifier order
# E$=0, RI$=1, M$=2, MR$=3, General$=4
order_map = {
    'E': 0,
    'RI': 1,
    'M': 2,
    'MR': 3,
    'General': 4
}

violations = []
g_record_count = 0

i = 0
while i < len(lines):
    line = lines[i]
    # Look for G-records (actual gamma transitions)
    if line.startswith(' 35CL  G '):
        g_record_count += 1
        g_energy = line[10:19].strip()
        
        # Collect following cG lines for this G-record
        cg_blocks = []  # List of (line_idx, cG_line, identifiers)
        j = i + 1
        while j < len(lines) and lines[j].startswith(' 35CL cG'):
            cg_line = lines[j]
            # Extract main identifier (before $)
            match = re.search(r'cG\s+([^$]+)\$', cg_line)
            if match:
                id_text = match.group(1).strip()
                
                # Parse identifiers handling grouped comments (RI,M,MR etc)
                identifiers_in_line = []
                for part in id_text.split(','):
                    part = part.strip()
                    # Remove field modifiers like (K), (D), (H), (B)
                    part_clean = re.sub(r'\([A-Z]\)', '', part).strip()
                    if part_clean in order_map:
                        identifiers_in_line.append(part_clean)
                
                cg_blocks.append((j + 1, cg_line.strip(), id_text, identifiers_in_line))
            else:
                # General comment (just cG $)
                cg_blocks.append((j + 1, cg_line.strip(), '(General)', ['General']))
            
            j += 1
        
        # Check ordering within cG blocks for this G-record
        if len(cg_blocks) > 1:
            prev_max_order = -1
            for line_idx, cg_line_text, id_display, ids_list in cg_blocks:
                if not ids_list:
                    # General comment
                    ids_list = ['General']
                
                # Get max order for this cG line (in case of grouped comments)
                max_order = max(order_map.get(id_part, 4) for id_part in ids_list)
                
                # Check if ordering is violated
                if max_order < prev_max_order:
                    # Violation found
                    violations.append({
                        'g_idx': g_record_count,
                        'g_energy': g_energy,
                        'line_idx': line_idx,
                        'cg_line': cg_line_text[:60] + '...' if len(cg_line_text) > 60 else cg_line_text,
                        'id_display': id_display,
                        'ids_list': ids_list,
                        'max_order': max_order,
                        'prev_max_order': prev_max_order
                    })
                
                prev_max_order = max_order
        
        i = j
    else:
        i += 1

# Report violations
print(f'Total G-records scanned: {g_record_count}')
print(f'Total cG ordering violations found: {len(violations)}\n')

if violations:
    print('VIOLATIONS (showing first 50):')
    for v in violations[:50]:
        print(f"  Line {v['line_idx']:4d} (G#{v['g_idx']:3d}, E={v['g_energy']:>8s}): "
              f"{v['id_display']:20s} (order {v['max_order']} after {v['prev_max_order']})")
        print(f"           {v['cg_line']}")
else:
    print('No cG ordering violations detected!')
