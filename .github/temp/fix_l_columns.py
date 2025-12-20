import os

def fix_ensdf_columns(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if len(line) >= 8 and line[7] == 'L' and line[0:5].strip() == '34CL':
            # Standardize NUCID to " 34CL" (Col 1-5)
            nucid = " 34CL"
            
            # Extract fields based on current (possibly shifted) positions
            # We use lstrip() on fields to find the actual content
            
            # Energy (10-19)
            energy_field = line[9:19]
            # DE (20-21)
            de_field = line[19:21]
            
            # Jpi (23-39)
            jpi_field = line[22:39].strip()
            
            # L-transfer (56-64)
            # The tool says it's at 57, so we look around there
            l_trans_field = line[55:64].strip()
            
            # S-strength (65-74)
            s_strength_field = line[64:74].strip()
            
            # DS (75-76)
            ds_field = line[74:76].strip()
            
            # Comment Flag (77)
            flag = line[76] if len(line) > 76 else " "
            
            # Logic to move uncertainty from S to DS if DS is empty
            # Example: S="0.0118", DS="8 " -> S="0.0118", DS="8 " (already correct)
            # Example: S="0.230     8", DS="  " -> S="0.230    ", DS="8 "
            if not ds_field and " " in s_strength_field:
                parts = s_strength_field.split()
                if len(parts) == 2:
                    s_strength_field = parts[0]
                    ds_field = parts[1]
            
            # Reconstruct the line with exact column positions
            # Col 1-5: NUCID
            # Col 6: Blank
            # Col 7: Blank
            # Col 8: L
            # Col 9: Blank
            # Col 10-19: Energy (Left-justified)
            # Col 20-21: DE (Left-justified)
            # Col 22: Space
            # Col 23-39: Jpi (Left-justified)
            # Col 40-49: T1/2 (Blank for this file mostly)
            # Col 50-55: DT (Blank)
            # Col 56-64: L (Left-justified)
            # Col 65-74: S (Left-justified)
            # Col 75-76: DS (Left-justified)
            # Col 77: Flag
            # Col 78-79: MS
            # Col 80: Q
            
            new_line = list(" " * 80)
            new_line[0:5] = list(nucid.ljust(5))
            new_line[7] = 'L'
            
            # Energy
            energy_val = energy_field.strip()
            new_line[9:9+len(energy_val)] = list(energy_val)
            
            # DE
            de_val = de_field.strip()
            new_line[19:19+len(de_val)] = list(de_val)
            
            # Jpi
            if jpi_field:
                new_line[22:22+len(jpi_field)] = list(jpi_field)
            
            # L-transfer
            if l_trans_field:
                new_line[55:55+len(l_trans_field)] = list(l_trans_field)
                
            # S-strength
            if s_strength_field:
                new_line[64:64+len(s_strength_field)] = list(s_strength_field)
                
            # DS
            if ds_field:
                new_line[74:74+len(ds_field)] = list(ds_field)
                
            # Flag
            new_line[76] = flag
            
            new_lines.append("".join(new_line) + "\n")
        else:
            new_lines.append(line)

    with open(file_path, 'w') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    fix_ensdf_columns(r"d:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_3he_d.ens")
