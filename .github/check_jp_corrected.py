import re

def check_jp_transfer_corrected():
    """
    CORRECTED: Check J-π transfer from 2019SE09.ens to Cl35_32s_a_p.ens
    Now checks ALL levels that reference 2019Se09, not just K-flagged ones
    """
    # Extract J-π from 2019SE09.ens
    se09_jp_data = {}
    with open('d:\\X\\ND\\ENSDF\\A35\\Cl35\\temp\\2019SE09.ens', 'r') as f:
        for line in f:
            if len(line) >= 80 and line[7] == 'L' and line[6] == ' ':
                try:
                    energy_str = line[9:19].strip()
                    jp_str = line[22:39].strip()
                    
                    if energy_str and jp_str:
                        energy = float(energy_str)
                        se09_jp_data[energy] = jp_str
                except (ValueError, IndexError):
                    continue
    
    print(f"Found {len(se09_jp_data)} J-π assignments in 2019SE09.ens")
    
    # Extract ALL levels that reference 2019Se09 (K flag OR comments mention 2019Se09)
    se09_referenced_levels = []
    
    with open('d:\\X\\ND\\ENSDF\\A35\\Cl35\\new\\Cl35_32s_a_p.ens', 'r') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if this is an L-record
        if len(line) >= 80 and line[7] == 'L' and line[6] == ' ':
            energy_str = line[9:19].strip()
            jp_str = line[22:39].strip()
            flag = line[76:77].strip()
            
            if energy_str:
                try:
                    energy = float(energy_str)
                    line_num = i + 1
                    
                    # Check if this level references 2019Se09
                    references_se09 = False
                    
                    # Method 1: Check K flag
                    if flag == 'K':
                        references_se09 = True
                        reason = "K flag"
                    
                    # Method 2: Check following comment lines for 2019Se09 mention
                    if not references_se09:
                        j = i + 1
                        while j < len(lines):
                            next_line = lines[j]
                            # Check if this is a comment line for our level
                            if (len(next_line) >= 8 and 
                                next_line[0:5] == ' 35CL' and 
                                next_line[6:8] in ['cL', '2c', '3c', '4c', '5c']):
                                if '2019Se09' in next_line:
                                    references_se09 = True
                                    reason = "comment mentions 2019Se09"
                                    break
                                j += 1
                            else:
                                break
                    
                    if references_se09:
                        se09_referenced_levels.append((energy, jp_str, line_num, reason))
                        
                except ValueError:
                    pass
        i += 1
    
    print(f"Found {len(se09_referenced_levels)} levels that reference 2019Se09 data")
    print()
    
    # Detailed comparison
    missing_jp = []
    transferred_jp = []
    mismatched_jp = []
    
    tolerance = 10.0  # keV - increased tolerance for better matching
    
    for adopted_energy, adopted_jp, line_num, reason in se09_referenced_levels:
        # Find corresponding level in 2019SE09.ens
        closest_se09_energy = None
        min_diff = float('inf')
        
        for se09_energy in se09_jp_data.keys():
            diff = abs(adopted_energy - se09_energy)
            if diff < min_diff:
                min_diff = diff
                closest_se09_energy = se09_energy
        
        if closest_se09_energy and min_diff <= tolerance:
            se09_jp = se09_jp_data[closest_se09_energy]
            
            if not adopted_jp and se09_jp:
                missing_jp.append((adopted_energy, se09_jp, line_num, reason, closest_se09_energy))
            elif adopted_jp and se09_jp:
                if adopted_jp == se09_jp:
                    transferred_jp.append((adopted_energy, adopted_jp, line_num, reason))
                else:
                    mismatched_jp.append((adopted_energy, adopted_jp, se09_jp, line_num, reason))
    
    print("=== CORRECTED TRANSFER ANALYSIS RESULTS ===")
    print()
    
    print(f"Successfully transferred J-π values: {len(transferred_jp)}")
    if transferred_jp:
        for energy, jp, line_num, reason in transferred_jp:
            print(f"  Line {line_num:3d}: {energy:8.1f} keV → {jp} ({reason})")
    
    print()
    print(f"🚨 MISSING J-π values (should be transferred): {len(missing_jp)}")
    if missing_jp:
        for energy, se09_jp, line_num, reason, se09_energy in missing_jp:
            print(f"  Line {line_num:3d}: {energy:8.1f} keV should have J-π '{se09_jp}' from {se09_energy} keV ({reason})")
    
    print()
    print(f"Mismatched J-π values: {len(mismatched_jp)}")
    if mismatched_jp:
        for energy, adopted_jp, se09_jp, line_num, reason in mismatched_jp:
            print(f"  Line {line_num:3d}: {energy:8.1f} keV - Adopted: '{adopted_jp}' vs 2019Se09: '{se09_jp}' ({reason})")
    
    print()
    print("=== ALL LEVELS REFERENCING 2019Se09 DATA ===")
    for energy, jp, line_num, reason in se09_referenced_levels:
        jp_status = jp if jp else "NO J-π"
        print(f"  Line {line_num:3d}: {energy:8.1f} keV → {jp_status} ({reason})")
    
    print()
    print("=== ALL J-π VALUES IN 2019SE09.ens ===")
    for energy, jp in sorted(se09_jp_data.items()):
        print(f"  {energy:8.1f} keV: {jp}")
    
    return missing_jp, mismatched_jp, se09_referenced_levels

if __name__ == "__main__":
    missing, mismatched, referenced = check_jp_transfer_corrected()
    
    if missing:
        print(f"\n🚨 CRITICAL ISSUE: {len(missing)} J-π values are missing from the adopted file!")
        print("These should be added to maintain data integrity.")
    else:
        print("\n✅ All J-π values properly transferred.")