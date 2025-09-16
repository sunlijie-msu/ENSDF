import re

def strict_jp_match_verification():
    """
    STRICT verification - J-π values must match EXACTLY including parentheses
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
    print()
    
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
            
            if energy_str:
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
    
    print(f"Found {len(adopted_levels_with_jp)} levels that reference 2019Se09")
    print()
    
    # STRICT comparison - EXACT match required
    exact_matches = []
    mismatched = []
    missing_jp = []
    extra_jp = []
    
    tolerance = 10.0  # keV
    
    print("=== STRICT EXACT MATCH VERIFICATION ===")
    print()
    
    # Check all adopted levels that reference 2019Se09
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
            
            if not adopted_jp:  # Missing J-π in adopted
                missing_jp.append((adopted_energy, se09_jp, line_num, reason, closest_se09_energy))
            elif adopted_jp == se09_jp:  # EXACT match
                exact_matches.append((adopted_energy, adopted_jp, line_num, reason, closest_se09_energy))
            else:  # Mismatch (different J-π values)
                mismatched.append((adopted_energy, adopted_jp, se09_jp, line_num, reason, closest_se09_energy))
        else:
            if adopted_jp:  # Has J-π but no source
                extra_jp.append((adopted_energy, adopted_jp, line_num, reason))
    
    # Check for 2019Se09 J-π values that should be in adopted but aren't
    se09_levels_not_in_adopted = []
    for se09_energy, se09_jp in se09_jp_data.items():
        found_in_adopted = False
        for adopted_energy, adopted_jp, line_num, reason in adopted_levels_with_jp:
            if abs(se09_energy - adopted_energy) <= tolerance:
                found_in_adopted = True
                break
        if not found_in_adopted:
            se09_levels_not_in_adopted.append((se09_energy, se09_jp))
    
    print(f"✅ EXACT matches: {len(exact_matches)}")
    if exact_matches:
        for energy, jp, line_num, reason, se09_energy in exact_matches:
            print(f"  Line {line_num:3d}: {energy:8.1f} keV → '{jp}' ✓ (exactly matches {se09_energy} keV)")
    
    print()
    print(f"🚨 MISMATCHED J-π values (EXACT comparison): {len(mismatched)}")
    if mismatched:
        for energy, adopted_jp, se09_jp, line_num, reason, se09_energy in mismatched:
            print(f"  Line {line_num:3d}: {energy:8.1f} keV → Adopted: '{adopted_jp}' vs 2019Se09: '{se09_jp}' (from {se09_energy} keV)")
            print(f"           ISSUE: Parentheses or formatting mismatch!")
    
    print()
    print(f"❌ MISSING J-π values: {len(missing_jp)}")
    if missing_jp:
        for energy, se09_jp, line_num, reason, se09_energy in missing_jp:
            print(f"  Line {line_num:3d}: {energy:8.1f} keV should have J-π '{se09_jp}' from {se09_energy} keV")
    
    print()
    print(f"⚠️  EXTRA J-π values (no 2019Se09 source): {len(extra_jp)}")
    if extra_jp:
        for energy, jp, line_num, reason in extra_jp:
            print(f"  Line {line_num:3d}: {energy:8.1f} keV has J-π '{jp}' but no matching 2019Se09 source")
    
    print()
    print(f"🔍 2019Se09 levels not represented in adopted file: {len(se09_levels_not_in_adopted)}")
    if se09_levels_not_in_adopted:
        for energy, jp in se09_levels_not_in_adopted:
            print(f"  {energy:8.1f} keV → '{jp}' (no corresponding level in adopted file)")
    
    print()
    print("=== DETAILED J-π COMPARISON TABLE ===")
    print("Line | Adopted Energy | Adopted J-π     | 2019Se09 Energy | 2019Se09 J-π    | Status")
    print("-" * 85)
    
    for adopted_energy, adopted_jp, line_num, reason in sorted(adopted_levels_with_jp, key=lambda x: x[0]):
        closest_se09_energy = None
        min_diff = float('inf')
        
        for se09_energy in se09_jp_data.keys():
            diff = abs(adopted_energy - se09_energy)
            if diff < min_diff:
                min_diff = diff
                closest_se09_energy = se09_energy
        
        if closest_se09_energy and min_diff <= tolerance:
            se09_jp = se09_jp_data[closest_se09_energy]
            if not adopted_jp:
                status = "MISSING"
            elif adopted_jp == se09_jp:
                status = "EXACT ✓"
            else:
                status = "MISMATCH ❌"
            se09_energy_str = f"{closest_se09_energy:.1f}"
        else:
            se09_energy_str = "N/A"
            se09_jp = "N/A"
            status = "NO SOURCE"
        
        adopted_jp_display = adopted_jp if adopted_jp else "(empty)"
        print(f"{line_num:3d}  | {adopted_energy:13.1f} | {adopted_jp_display:15s} | {se09_energy_str:15s} | {se09_jp:15s} | {status}")
    
    return exact_matches, mismatched, missing_jp, extra_jp

if __name__ == "__main__":
    exact, mismatched, missing, extra = strict_jp_match_verification()
    
    total_issues = len(mismatched) + len(missing) + len(extra)
    
    if total_issues > 0:
        print(f"\n🚨 CRITICAL ISSUES FOUND: {total_issues} problems require correction!")
        print("The file needs to be revised to fix these discrepancies.")
    else:
        print(f"\n✅ PERFECT: All J-π values exactly match 2019Se09 sources.")