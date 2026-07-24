"""Build compact cL format: $(cfg1). N=v1, v2. (cfg2) N=v3, v4.  and apply edits."""
import re, json

with open(r'A34\S34\new\S34_32s_t_p.ens', 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

config_data = {
    0: [("(d{-3/2}){+2}", "100", "100"), ("(s{-1/2}){+2}", "13.8", "13.0")],
    2128: [("(d{-3/2}){+2}", "11.8", "11.5"), ("d{-3/2},s{-1/2}", "1.62", "1.52")],
    3308: [("(d{-3/2}){+2}", "9.12", "8.79"), ("d{-3/2},s{-1/2}", "1.18", "1.12")],
    3915: [("(d{-3/2}){+2}", "3.62", "3.33"), ("(s{-1/2}){+2}", "0.48", "0.42"), ("(f{-7/2}){+2}", "1.75", "2.18")],
    4121: [("(d{-3/2}){+2}", "4.50", "4.24"), ("d{-3/2},s{-1/2}", "0.59", "0.53"), ("(f{-7/2}){+2}", "2.25", "2.61")],
    4623: [("d{-3/2},f{-7/2}", "33.8", "33.3"), ("d{-3/2},p{-3/2}", "2.62", "2.67")],
    4690: [("(f{-7/2}){+2}", "2.00", "1.88"), ("d{-3/2},f{-7/2}", "0.48", "0.48")],
    4888: [("(d{-3/2}){+2}", "3.50", "3.30"), ("(f{-7/2}){+2}", "1.88", "1.88")],
    5225: [("(d{-3/2}){+2}", "5.38", "4.85"), ("(f{-7/2}){+2}", "3.38", "3.64"), ("(p{-3/2}){+2}", "0.29", "0.28")],
    5679: [("d{-3/2},p{-3/2}", "3.25", "3.18"), ("d{-3/2},f{-7/2}", "2.12", "2.18")],
    5759: [("d{-3/2},p{-3/2}", "9.38", "8.18")],
    5859: [("(f{-7/2}){+2}", "15.0", "")],
    6008: [("(f{-7/2}){+2}", "33.75", "33.33"), ("(p{-3/2}){+2}", "3.75", "3.03")],
    6128: [("(f{-7/2}){+2}", "7.75", "7.88")],
    6179: [("d{-3/2},p{-3/2}", "0.22", "0.21"), ("d{-3/2},f{-7/2}", "3.12", "2.73")],
    6349: [("d{-3/2},p{-3/2}", "6.38", "5.76")],
    6828: [("(f{-7/2}){+2}", "4.25", "4.55"), ("(p{-3/2}){+2}", "0.36", "")],
    7112: [("d{-3/2},f{-7/2}", "11.25", "10.00"), ("d{-3/2},p{-3/2}", "0.78", "0.67"), ("(f{-7/2}){+2}", "6.50", "6.67"), ("(p{-3/2}){+2}", "0.62", "0.55")],
    7245: [("d{-3/2},f{-7/2}", "22.50", "20.61"), ("d{-3/2},p{-3/2}", "1.62", "1.52")],
    7621: [("d{-3/2},f{-7/2}", "23.75", "23.03"), ("d{-3/2},p{-3/2}", "1.88", "1.61")],
    7739: [("(f{-7/2}){+2}", "4.75", "5.15"), ("(p{-3/2}){+2}", "0.48", "0.39")],
    7801: [("((f{-7/2}){+2}", "20.62", "")],
    8025: [("(p{-3/2}){+2}", "0.56", "")],
    8255: [("(f{-7/2}){+2}", "5.12", "5.15"), ("(p{-3/2}){+2}", "0.49", "0.36"), ("d{-3/2},p{-3/2}", "0.62", "0.52"), ("d{-3/2},f{-7/2}", "8.75", "4.24")],
    8293: [("(f{-7/2}){+2}", "4.75", "4.85"), ("d{-3/2},f{-7/2}", "1.12", "1.30")],
    8383: [("d{-3/2},p{-3/2}", "8.38", "")],
    8418: [("(f{-7/2}){+2}", "11.25", "")],
    8496: [("d{-3/2},p{-3/2}", "12.25", "")],
}

def build_compact(rows):
    """Build compact comment lines: each config as 'cfg. N=v1, v2.'"""
    chunks = []
    for cfg, sii, siip in rows:
        if siip:
            chunks.append(f"{cfg}. N={sii}, {siip}.")
        else:
            chunks.append(f"{cfg}. N={sii}.")
    
    # Split into lines (~65 chars per cL text line)
    lines = []
    current = ""
    for chunk in chunks:
        if not current:
            current = "$" + chunk
        else:
            test = current + " " + chunk
            if len(test) <= 72:
                current = test
            else:
                lines.append(current)
                current = "$" + chunk
    if current:
        lines.append(current)
    return lines

# Find L indices
l_map = {}
for i, line in enumerate(lines):
    if len(line) >= 19 and line[7] == 'L' and line[8] == ' ':
        e_str = line[9:19].strip()
        if e_str:
            try:
                e_int = int(round(float(e_str)))
                if e_int in config_data:
                    l_map[e_int] = i
            except ValueError:
                pass

# Determine if level already has cL comments
def has_cl_comment(l_idx):
    """Check if next line after L is a cL comment block we added."""
    for k in range(l_idx+1, min(l_idx+10, len(lines))):
        nxt = lines[k]
        if len(nxt) < 8: break
        # Our cL: col7='c', and text contains N=
        if nxt[6:8] in (' c', '2c', '3c', '4c', '5c') and 'N=' in nxt:
            return True
        # Existing cL (Doublet etc): col7='c'
        if nxt[7] == 'c':
            # Not ours if no N=
            if 'N=' not in nxt:
                return False  # existing cL, not ours
            return True
        # L or G record: stop
        if nxt[7] in ('L', 'G', 'B', 'E', 'A', 'D', 'P', 'N'):
            return False
    return False

def find_cl_range(l_idx):
    """Find range of cL comment lines after L-record (our added ones). Returns (start, end) or None."""
    start = None
    end = l_idx
    for k in range(l_idx+1, min(l_idx+10, len(lines))):
        nxt = lines[k]
        if len(nxt) < 8: break
        if nxt[6:8] in (' c', '2c', '3c', '4c', '5c') and ('N=' in nxt or '|s{-rel}' in nxt):
            if start is None:
                start = k
            end = k
        else:
            break
    if start is not None:
        return (start, end)
    return None

# Build replacements
replacements = []
for e_kev in sorted(config_data.keys()):
    if e_kev not in l_map: continue
    l_idx = l_map[e_kev]
    l_line = lines[l_idx]
    
    compact = build_compact(config_data[e_kev])
    
    # Build cL lines
    cl_lines = []
    for j, txt in enumerate(compact):
        if j == 0:
            prefix = "cL "
        elif j < 9:
            prefix = f"{j+1}cL"
        else:
            prefix = f"{chr(ord('a')+j-9)}cL"
        line = f" 34S {prefix}{txt}"
        line = line.ljust(80)
        cl_lines.append(line)
    
    # Check if we need to replace existing cL or insert new
    cl_range = find_cl_range(l_idx)
    
    if cl_range:
        # Replace existing cL block
        old_start = cl_range[0]
        old_end = cl_range[1]
        # Build old string: L-line + old cL lines + next line after cL
        old_lines = [l_line]
        for k in range(old_start, old_end + 1):
            old_lines.append(lines[k])
        # Add next line as context
        next_after = old_end + 1
        if next_after < len(lines):
            old_lines.append(lines[next_after])
            new_lines = [l_line] + cl_lines + [lines[next_after]]
        else:
            new_lines = [l_line] + cl_lines
        
        old_str = '\n'.join(old_lines)
        new_str = '\n'.join(new_lines)
        replacements.append((e_kev, 'replace', old_str, new_str))
    else:
        # Insert new cL after L-record
        next_line = lines[l_idx + 1] if l_idx + 1 < len(lines) else ''
        old_str = l_line + '\n' + next_line
        new_str = l_line + '\n' + '\n'.join(cl_lines) + '\n' + next_line
        replacements.append((e_kev, 'insert', old_str, new_str))

print(f"Total replacements: {len(replacements)}")
for e, op, old, new in replacements:
    cl_count = new.count('N=')
    print(f"  E={e} ({op}): {cl_count} configs, old_len={len(old)}, new_len={len(new)}")
