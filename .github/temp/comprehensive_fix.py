import re

def fix_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        # Fix corrupted comment lines
        # If it looks like a comment but has 'L' at col 8
        if len(line) >= 10 and line[0:5].strip() == '34CL' and line[7] == 'L' and (line[9] == '$' or line[10] == '$' or '$' in line[8:15]):
            # It's a comment line
            nucid = " 34CL"
            # Find where the comment content starts (usually after $)
            dollar_idx = line.find('$')
            if dollar_idx != -1:
                # Reconstruct as cL comment
                # Standard format: " 34CL cL S$..."
                # We'll try to preserve the identifier (S, E, etc.)
                ident = line[8:dollar_idx].strip()
                content = line[dollar_idx:].strip()
                
                # Fix the C{+2}S issue if present
                content = content.replace("C  +2}", "C{+2}")
                content = content.replace("C +2}", "C{+2}")
                
                new_line = f"{nucid} cL {ident}{content}"
                # Pad to 80 if needed, but comments don't strictly need 80
                new_lines.append(new_line.ljust(80) + "\n")
                continue

        # Fix real L-records
        if len(line) >= 8 and line[7] == 'L' and line[0:5].strip() == '34CL':
            # Extract fields
            nucid = " 34CL"
            energy = line[9:19].strip()
            de = line[19:21].strip()
            jpi = line[22:39].strip()
            # T1/2 and DT are usually blank in this file
            t12 = line[39:49].strip()
            dt = line[49:55].strip()
            l_trans = line[55:64].strip()
            s_strength = line[64:74].strip()
            ds = line[74:76].strip()
            flag = line[76] if len(line) > 76 else " "
            
            # Logic to move uncertainty from S to DS if DS is empty
            if not ds and " " in s_strength:
                parts = s_strength.split()
                if len(parts) == 2:
                    s_strength = parts[0]
                    ds = parts[1]
            
            # Change .xxxx to 0.xxxx in S-field
            if s_strength.startswith('.'):
                s_strength = '0' + s_strength
            elif s_strength.startswith('+.'):
                s_strength = '+0' + s_strength[1:]
            elif s_strength.startswith('-.'):
                s_strength = '-0' + s_strength[1:]
            
            # Reconstruct line
            new_line = list(" " * 80)
            new_line[0:5] = list(nucid.ljust(5))
            new_line[7] = 'L'
            
            # Energy (10-19)
            if energy:
                new_line[9:9+len(energy)] = list(energy)
            # DE (20-21)
            if de:
                new_line[19:19+len(de)] = list(de)
            # Jpi (23-39)
            if jpi:
                new_line[22:22+len(jpi)] = list(jpi)
            # T1/2 (40-49)
            if t12:
                new_line[39:39+len(t12)] = list(t12)
            # DT (50-55)
            if dt:
                new_line[49:49+len(dt)] = list(dt)
            # L (56-64)
            if l_trans:
                new_line[55:55+len(l_trans)] = list(l_trans)
            # S (65-74)
            if s_strength:
                new_line[64:64+len(s_strength)] = list(s_strength)
            # DS (75-76)
            if ds:
                new_line[74:74+len(ds)] = list(ds)
            # Flag (77)
            new_line[76] = flag
            
            new_lines.append("".join(new_line) + "\n")
        else:
            # For other lines, just fix the C{+2}S issue if present
            line = line.replace("C  +2}", "C{+2}")
            line = line.replace("C +2}", "C{+2}")
            new_lines.append(line)

    with open(file_path, 'w') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    fix_file(r"d:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_3he_d.ens")
