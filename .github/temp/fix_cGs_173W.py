
def fix_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    new_lines = []
    changes = 0
    for line in lines:
        stripped = line.rstrip('\n').rstrip('\r')
        if not stripped.startswith('173W'): 
            # header or other lines
            new_lines.append(line)
            continue
            
        # Check length
        if len(stripped) != 80:
            # Pad or trim
            if len(stripped) < 80:
                fixed = f"{stripped:<80}"
            else:
                fixed = stripped[:80]
            
            new_lines.append(fixed + '\n')
            changes += 1
        else:
            new_lines.append(line)
            
    with open(filepath, 'w') as f:
        f.writelines(new_lines)
    
    print(f"Fixed {changes} lines in {filepath}")

fix_file(r"d:\X\ND\ENSDF\XUNDL\2026TAAA_CLR1074_173W.ens")
