"""
Cross-check T$ comment values in adopted file against individual dataset T fields.
Extracts adopted L-records with their T$ comment blocks.
"""
import re

base = r'd:\X\ND\ENSDF\A34\Cl34\new'
adopted_file = f'{base}/Cl34_adopted.ens'

with open(adopted_file, 'r') as f:
    lines = f.readlines()

# Find starting line (L 1230.28)
start = None
for i, line in enumerate(lines):
    if '34CL  L 1230.28' in line:
        start = i
        break

print(f"=== Adopted L-records with T$ comments from line {start+1} ===\n")

i = start
while i < len(lines):
    raw = lines[i].rstrip('\n')
    
    # Check for L-record (col7=space, col8='L' in 0-indexed: raw[6]=' ', raw[7]='L')
    if len(raw) >= 8 and raw[5] == ' ' and raw[6] == ' ' and raw[7] == 'L':
        lrec_line = i + 1
        E_field = raw[9:19].strip() if len(raw) >= 19 else ''
        T_field = raw[39:49].strip() if len(raw) >= 49 else ''
        DT_field = raw[49:55].strip() if len(raw) >= 55 else ''
        
        # Look ahead for T$ comment
        j = i + 1
        t_comment_lines = []
        while j < len(lines):
            next_raw = lines[j].rstrip('\n')
            if len(next_raw) < 8:
                j += 1
                continue
            # Stop if we hit a new L-record
            if next_raw[5] == ' ' and next_raw[6] == ' ' and next_raw[7] == 'L':
                break
            # Collect T$ cL comment lines (first and continuations)
            if next_raw[5] == ' ' and next_raw[6:8] == 'cL' and 'T$' in next_raw:
                t_comment_lines.append((j+1, next_raw))
            elif t_comment_lines and len(next_raw) >= 8 and next_raw[6:8] == 'cL' and next_raw[5] in '23456789':
                # continuation of T$ block
                t_comment_lines.append((j+1, next_raw))
            j += 1
        
        if t_comment_lines:
            print(f"Line {lrec_line}: L E={E_field} T_adopted={T_field} DT={DT_field}")
            for tl, tr in t_comment_lines:
                print(f"  Line {tl}: {tr}")
            print()
    
    i += 1
