import re

def verify_existing_jp_matches():
    """
    Verify that existing J-π values in Cl35_32s_a_p.ens actually match 2019SE09.ens
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
    
    # Extract levels with J-π values that reference 2019Se09 from adopted file
    adopted_levels_with_jp = []
    
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
            
            if energy_str and jp_str:  # Only check levels that HAVE J-π values
                try:
                    energy = float(energy_str)
                    line_num = i + 1
                    
                    # Check if this level references 2019Se09
                    references_se09 = False
                    reason = ""
                    
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
                        adopted_levels_with_jp.append((energy, jp_str, line_num, reason))
                        
                except ValueError:
                    pass
        i += 1
    
    print(f"Found {len(adopted_levels_with_jp)} levels with J-π values that reference 2019Se09")
    print()
    
    # Compare existing J-π values
    matching = []
    mismatched = []
    no_source_jp = []
    
    tolerance = 10.0  # keV
    
    for adopted_energy, adopted_jp, line_num, reason in adopted_levels_with_jp:
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
            
            if adopted_jp == se09_jp:
                matching.append((adopted_energy, adopted_jp, line_num, reason, closest_se09_energy))
            else:
                mismatched.append((adopted_energy, adopted_jp, se09_jp, line_num, reason, closest_se09_energy))
        else:
            no_source_jp.append((adopted_energy, adopted_jp, line_num, reason))
    
    print("=== VERIFICATION OF EXISTING J-π VALUES ===")
    print()
    
    print(f"✅ Correctly matching J-π values: {len(matching)}")
    if matching:
        for energy, jp, line_num, reason, se09_energy in matching:
            print(f"  Line {line_num:3d}: {energy:8.1f} keV → {jp} ✓ (matches {se09_energy} keV, {reason})")
    
    print()
    print(f"🚨 MISMATCHED J-π values: {len(mismatched)}")
    if mismatched:
        for energy, adopted_jp, se09_jp, line_num, reason, se09_energy in mismatched:
            print(f"  Line {line_num:3d}: {energy:8.1f} keV → Adopted: '{adopted_jp}' vs 2019Se09: '{se09_jp}' (from {se09_energy} keV, {reason})")
    
    print()
    print(f"⚠️  J-π values with no clear 2019Se09 source: {len(no_source_jp)}")
    if no_source_jp:
        for energy, jp, line_num, reason in no_source_jp:
            print(f"  Line {line_num:3d}: {energy:8.1f} keV → {jp} (no matching energy in 2019Se09, {reason})")
    
    print()
    print("=== DETAILED COMPARISON TABLE ===")
    print("Adopted Energy | Adopted J-π   | 2019Se09 Energy | 2019Se09 J-π  | Match | Line | Reason")
    print("-" * 95)
    
    all_comparisons = []
    for adopted_energy, adopted_jp, line_num, reason in adopted_levels_with_jp:
        closest_se09_energy = None
        min_diff = float('inf')
        
        for se09_energy in se09_jp_data.keys():
            diff = abs(adopted_energy - se09_energy)
            if diff < min_diff:
                min_diff = diff
                closest_se09_energy = se09_energy
        
        if closest_se09_energy and min_diff <= tolerance:
            se09_jp = se09_jp_data[closest_se09_energy]
            match_status = "YES" if adopted_jp == se09_jp else "NO"
            se09_energy_str = f"{closest_se09_energy:.1f}"
        else:
            se09_energy_str = "N/A"
            se09_jp = "N/A"
            match_status = "N/A"
        
        print(f"{adopted_energy:13.1f} | {adopted_jp:13s} | {se09_energy_str:15s} | {se09_jp:13s} | {match_status:5s} | {line_num:3d}  | {reason}")
    
    return matching, mismatched, no_source_jp

if __name__ == "__main__":
    matching, mismatched, no_source = verify_existing_jp_matches()
    
    if mismatched:
        print(f"\n🚨 CRITICAL ISSUE: {len(mismatched)} existing J-π values do NOT match 2019Se09!")
    else:
        print(f"\n✅ All existing J-π values properly match their 2019Se09 sources.")