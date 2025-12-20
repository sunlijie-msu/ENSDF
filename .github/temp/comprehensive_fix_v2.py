import re

def fix_file_v2(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        # Check if it's a line that should be a comment
        is_comment = False
        if len(line) >= 10 and line[0:5].strip() == '34CL' and line[7] == 'L':
            energy_part = line[9:19].strip()
            # If energy part is not a number and not empty, it's likely a comment
            if energy_part:
                try:
                    float(energy_part.replace('(', '').replace(')', ''))
                except ValueError:
                    is_comment = True
            else:
                # If energy is empty, check other fields
                # Real L-records with empty energy are rare in this file
                # but let's check if it has a Jpi or L-transfer in the right place
                jpi_part = line[22:39].strip()
                l_part = line[55:64].strip()
                if not jpi_part and not l_part:
                    is_comment = True

        if is_comment:
            nucid = " 34CL"
            content = line[8:].strip()
            # Fix the C{+2}S issue
            content = content.replace("C  +2}", "C{+2}")
            content = content.replace("C +2}", "C{+2}")
            content = content.replace("C{+2} S", "C{+2}S")
            
            new_line = f"{nucid} cL {content}"
            new_lines.append(new_line.ljust(80) + "\n")
            continue

        # Fix real L-records
        if len(line) >= 8 and line[7] == 'L' and line[0:5].strip() == '34CL':
            # Extract fields
            nucid = " 34CL"
            energy = line[9:19].strip()
            de = line[19:21].strip()
            jpi = line[22:39].strip()
            t12 = line[39:49].strip()
            dt = line[49:55].strip()
            l_trans = line[55:64].strip()
            s_strength = line[64:74].strip()
            ds = line[74:76].strip()
            flag = line[76] if len(line) > 76 else " "
            
            # Logic to move uncertainty from S to DS if DS is empty
            # BUT ONLY if it's a single value, not a sum like 0.123+0.456
            if not ds and " " in s_strength and "+" not in s_strength:
                parts = s_strength.split()
                if len(parts) == 2:
                    s_strength = parts[0]
                    ds = parts[1]
            
            # If it was incorrectly split (like 0.028+.01 and 6), rejoin it
            if "+" in s_strength and ds and ds.isdigit():
                # Check if the split happened at the end of a sum
                # e.g. S="0.028+.01", DS="6 " -> S="0.028+.016", DS=""
                if len(s_strength) < 10:
                    s_strength = (s_strength + ds)[:10]
                    ds = ""

            # Change .xxxx to 0.xxxx in S-field if it fits
            if s_strength.startswith('.') and len(s_strength) < 10:
                s_strength = '0' + s_strength
            elif s_strength.startswith('+.') and len(s_strength) < 10:
                s_strength = '+0' + s_strength[1:]
            elif s_strength.startswith('-.') and len(s_strength) < 10:
                s_strength = '-0' + s_strength[1:]
            
            # Reconstruct line
            new_line = list(" " * 80)
            new_line[0:5] = list(nucid.ljust(5))
            new_line[7] = 'L'
            
            if energy:
                new_line[9:9+len(energy)] = list(energy)
            if de:
                new_line[19:19+len(de)] = list(de)
            if jpi:
                new_line[22:22+len(jpi)] = list(jpi)
            if t12:
                new_line[39:39+len(t12)] = list(t12)
            if dt:
                new_line[49:49+len(dt)] = list(dt)
            if l_trans:
                new_line[55:55+len(l_trans)] = list(l_trans)
            if s_strength:
                new_line[64:64+len(s_strength)] = list(s_strength)
            if ds:
                new_line[74:74+len(ds)] = list(ds)
            new_line[76] = flag
            
            new_lines.append("".join(new_line) + "\n")
        else:
            # For other lines, fix C{+2}S
            line = line.replace("C  +2}", "C{+2}")
            line = line.replace("C +2}", "C{+2}")
            line = line.replace("C{+2} S", "C{+2}S")
            new_lines.append(line)

    with open(file_path, 'w') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    fix_file_v2(r"d:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_3he_d.ens")
