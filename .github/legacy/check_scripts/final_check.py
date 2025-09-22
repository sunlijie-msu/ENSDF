import re

def simple_final_check():
    """
    Simple final check without Unicode symbols
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
    
    print(f"2019SE09.ens has {len(se09_jp_data)} J-π assignments")
    
    # Check adopted file for levels that reference 2019Se09
    missing_count = 0
    exact_match_count = 0
    mismatch_count = 0
    
    with open('d:\\X\\ND\\ENSDF\\A35\\Cl35\\new\\Cl35_32s_a_p.ens', 'r') as f:
        lines = f.readlines()
    
    tolerance = 10.0
    
    for i, line in enumerate(lines):
        if len(line) >= 80 and line[7] == 'L' and line[6] == ' ':
            energy_str = line[9:19].strip()
            jp_str = line[22:39].strip()
            flag = line[76:77].strip()
            
            if energy_str:
                try:
                    energy = float(energy_str)
                    line_num = i + 1
                    
                    # Check if references 2019Se09
                    references_se09 = False
                    if flag == 'K':
                        references_se09 = True
                    else:
                        # Check comments
                        j = i + 1
                        while j < len(lines):
                            next_line = lines[j]
                            if (len(next_line) >= 8 and 
                                next_line[0:5] == ' 35CL' and 
                                next_line[6:8] in ['cL', '2c', '3c', '4c', '5c']):
                                if '2019Se09' in next_line:
                                    references_se09 = True
                                    break
                                j += 1
                            else:
                                break
                    
                    if references_se09:
                        # Find matching 2019Se09 level
                        closest_se09_energy = None
                        min_diff = float('inf')
                        
                        for se09_energy in se09_jp_data.keys():
                            diff = abs(energy - se09_energy)
                            if diff < min_diff:
                                min_diff = diff
                                closest_se09_energy = se09_energy
                        
                        if closest_se09_energy and min_diff <= tolerance:
                            se09_jp = se09_jp_data[closest_se09_energy]
                            
                            if not jp_str:
                                missing_count += 1
                                print(f"MISSING: Line {line_num} - {energy} keV should have '{se09_jp}'")
                            elif jp_str == se09_jp:
                                exact_match_count += 1
                            else:
                                mismatch_count += 1
                                print(f"MISMATCH: Line {line_num} - {energy} keV has '{jp_str}' vs '{se09_jp}'")
                
                except ValueError:
                    pass
    
    print(f"\nFINAL RESULTS:")
    print(f"  Exact matches: {exact_match_count}")
    print(f"  Mismatches: {mismatch_count}")
    print(f"  Missing: {missing_count}")
    
    if missing_count == 0 and mismatch_count == 0:
        print(f"\nSUCCESS: All J-π values exactly match 2019Se09!")
        print(f"Total of {exact_match_count} J-π values properly transferred with exact formatting.")
    else:
        print(f"\nISSUES REMAIN: {missing_count + mismatch_count} problems found.")

if __name__ == "__main__":
    simple_final_check()