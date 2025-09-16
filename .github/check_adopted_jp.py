import re

def check_jp_transfer_to_adopted():
    """
    Check J-π transfer from 2019SE09.ens to Cl35_32s_a_p.ens
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
    
    # Extract levels with K flag from adopted file
    k_flag_levels = []
    with open('d:\\X\\ND\\ENSDF\\A35\\Cl35\\new\\Cl35_32s_a_p.ens', 'r') as f:
        for line_num, line in enumerate(f, 1):
            if len(line) >= 80 and line[7] == 'L' and line[6] == ' ':
                flag = line[76:77].strip()
                if flag == 'K':
                    energy_str = line[9:19].strip()
                    jp_str = line[22:39].strip()
                    if energy_str:
                        try:
                            energy = float(energy_str)
                            k_flag_levels.append((energy, jp_str, line_num))
                        except ValueError:
                            continue
    
    print(f"Found {len(k_flag_levels)} levels with 'K' flag in adopted file")
    print()
    
    # Detailed comparison
    missing_jp = []
    transferred_jp = []
    mismatched_jp = []
    
    tolerance = 5.0  # keV
    
    for adopted_energy, adopted_jp, line_num in k_flag_levels:
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
                missing_jp.append((adopted_energy, se09_jp, line_num))
            elif adopted_jp and se09_jp:
                if adopted_jp == se09_jp:
                    transferred_jp.append((adopted_energy, adopted_jp, line_num))
                else:
                    mismatched_jp.append((adopted_energy, adopted_jp, se09_jp, line_num))
    
    print("=== TRANSFER ANALYSIS RESULTS ===")
    print()
    
    print(f"Successfully transferred J-π values: {len(transferred_jp)}")
    if transferred_jp:
        for energy, jp, line_num in transferred_jp:
            print(f"  Line {line_num:3d}: {energy:8.1f} keV → {jp}")
    
    print()
    print(f"Missing J-π values (should be transferred): {len(missing_jp)}")
    if missing_jp:
        for energy, se09_jp, line_num in missing_jp:
            print(f"  Line {line_num:3d}: {energy:8.1f} keV should have J-π '{se09_jp}'")
    
    print()
    print(f"Mismatched J-π values: {len(mismatched_jp)}")
    if mismatched_jp:
        for energy, adopted_jp, se09_jp, line_num in mismatched_jp:
            print(f"  Line {line_num:3d}: {energy:8.1f} keV - Adopted: '{adopted_jp}' vs 2019Se09: '{se09_jp}'")
    
    print()
    print("=== SUMMARY OF ALL J-π VALUES IN 2019SE09.ens ===")
    for energy, jp in sorted(se09_jp_data.items()):
        print(f"  {energy:8.1f} keV: {jp}")
    
    return missing_jp, mismatched_jp

if __name__ == "__main__":
    missing, mismatched = check_jp_transfer_to_adopted()
    
    if missing or mismatched:
        print(f"\n⚠️  ISSUES FOUND: {len(missing)} missing, {len(mismatched)} mismatched")
    else:
        print(f"\n✅ ALL J-π VALUES PROPERLY TRANSFERRED")