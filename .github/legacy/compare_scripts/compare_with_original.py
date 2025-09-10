#!/usr/bin/env python3
"""
Compare 2025LAAA_vs_2012DI06.ens placement table with original 2012DI06_127I_all_gamma_transitions.xundl
to identify any mismatches in ELI, JI, ELF, JF, EG_2012, RI_2012 data
"""

def parse_original_2012di06(filename):
    """Parse the original 2012DI06 data file"""
    transitions = {}
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    for line in lines[1:]:  # Skip header
        line = line.strip()
        if '|' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 6:
                try:
                    eli_str = parts[0]
                    ji = parts[1]
                    elf_str = parts[2]
                    jf = parts[3]
                    eg_str = parts[4]
                    ri = parts[5]
                    
                    # Extract numerical values
                    eli = float(eli_str.split('(')[0])
                    elf = float(elf_str.split('(')[0])
                    eg = float(eg_str.split('(')[0])
                    
                    # Use EG as key for matching
                    transitions[eg] = {
                        'eli': eli,
                        'ji': ji,
                        'elf': elf,
                        'jf': jf,
                        'eg': eg,
                        'ri': ri,
                        'eli_str': eli_str,
                        'elf_str': elf_str,
                        'eg_str': eg_str
                    }
                except (ValueError, IndexError):
                    continue
    
    return transitions

def parse_placement_table(filename):
    """Parse the placement table to extract gamma placements"""
    placements = {}
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        if '|' in line and 'keV' not in line and 'ELI' not in line and '---' not in line and 'FINAL' not in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 7:
                try:
                    eli = float(parts[0])
                    ji = parts[1].strip()
                    elf = float(parts[2])
                    jf = parts[3].strip()
                    eg_2012 = float(parts[4])
                    ri_2012 = parts[5].strip()
                    eg_2025 = parts[6].strip()
                    
                    if eg_2025 != 'TBD' and eg_2025:
                        energy_2025 = float(eg_2025)
                        placements[energy_2025] = {
                            'eli': eli,
                            'ji': ji,
                            'elf': elf,
                            'jf': jf,
                            'eg_2012': eg_2012,
                            'ri_2012': ri_2012,
                            'eg_2025': energy_2025
                        }
                except (ValueError, IndexError):
                    continue
    
    return placements

def find_mismatches(original_data, placement_data):
    """Find mismatches between original data and placement table"""
    
    print("COMPARING PLACEMENT TABLE WITH ORIGINAL 2012DI06 DATA:")
    print("=" * 80)
    print()
    
    mismatches = []
    
    for eg_2025, placement in placement_data.items():
        eg_2012 = placement['eg_2012']
        
        # Find corresponding entry in original data
        if eg_2012 in original_data:
            orig = original_data[eg_2012]
            
            # Check each field for mismatches
            errors_for_this_gamma = []
            
            # Check ELI
            if abs(placement['eli'] - orig['eli']) > 0.01:
                errors_for_this_gamma.append(f"ELI: {placement['eli']} ≠ {orig['eli']}")
            
            # Check JI (accounting for parentheses variations)
            if placement['ji'] != orig['ji']:
                # Check if it's just parentheses difference
                ji_clean = placement['ji'].replace('(', '').replace(')', '')
                orig_ji_clean = orig['ji'].replace('(', '').replace(')', '')
                if ji_clean != orig_ji_clean:
                    errors_for_this_gamma.append(f"JI: '{placement['ji']}' ≠ '{orig['ji']}'")
            
            # Check ELF
            if abs(placement['elf'] - orig['elf']) > 0.01:
                errors_for_this_gamma.append(f"ELF: {placement['elf']} ≠ {orig['elf']}")
            
            # Check JF (accounting for parentheses variations)
            if placement['jf'] != orig['jf']:
                # Check if it's just parentheses difference
                jf_clean = placement['jf'].replace('(', '').replace(')', '')
                orig_jf_clean = orig['jf'].replace('(', '').replace(')', '')
                if jf_clean != orig_jf_clean:
                    errors_for_this_gamma.append(f"JF: '{placement['jf']}' ≠ '{orig['jf']}'")
            
            # Check RI (allowing for formatting differences)
            if placement['ri_2012'] != orig['ri']:
                # Try to normalize both values for comparison
                try:
                    # Handle special cases like <=, >=, etc.
                    if '<=1.0' in orig['ri'] and 'LE' in placement['ri_2012']:
                        pass  # These might be equivalent
                    elif '>=17.0' in orig['ri'] and 'GE' in placement['ri_2012']:
                        pass  # These might be equivalent
                    elif orig['ri'] == '' and placement['ri_2012'] == '':
                        pass  # Both empty
                    else:
                        errors_for_this_gamma.append(f"RI: '{placement['ri_2012']}' ≠ '{orig['ri']}'")
                except:
                    errors_for_this_gamma.append(f"RI: '{placement['ri_2012']}' ≠ '{orig['ri']}'")
            
            if errors_for_this_gamma:
                mismatches.append({
                    'eg_2025': eg_2025,
                    'eg_2012': eg_2012,
                    'errors': errors_for_this_gamma,
                    'placement': placement,
                    'original': orig
                })
                
        else:
            mismatches.append({
                'eg_2025': eg_2025,
                'eg_2012': eg_2012,
                'errors': [f"EG_2012 {eg_2012} not found in original data!"],
                'placement': placement,
                'original': None
            })
    
    return mismatches

def report_mismatches(mismatches):
    """Report all mismatches in detail"""
    
    if not mismatches:
        print("✅ NO MISMATCHES FOUND!")
        print("All placement table entries match the original 2012DI06 data perfectly.")
        return
    
    print(f"❌ FOUND {len(mismatches)} GAMMA(S) WITH MISMATCHES:")
    print()
    
    for i, mismatch in enumerate(mismatches, 1):
        print(f"{i}. GAMMA {mismatch['eg_2025']} keV (mapped to 2012DI06 {mismatch['eg_2012']} keV):")
        
        for error in mismatch['errors']:
            print(f"   ❌ {error}")
        
        print(f"   Placement: ELI={mismatch['placement']['eli']}, JI='{mismatch['placement']['ji']}', ELF={mismatch['placement']['elf']}, JF='{mismatch['placement']['jf']}', RI='{mismatch['placement']['ri_2012']}'")
        
        if mismatch['original']:
            orig = mismatch['original']
            print(f"   Original:  ELI={orig['eli']}, JI='{orig['ji']}', ELF={orig['elf']}, JF='{orig['jf']}', RI='{orig['ri']}'")
        else:
            print(f"   Original:  NOT FOUND in 2012DI06 data!")
        
        print()

if __name__ == "__main__":
    original_file = "XUNDL/2012DI06_127I_all_gamma_transitions.xundl"
    placement_file = "XUNDL/2025LAAA_vs_2012DI06.ens"
    
    print(f"Loading original 2012DI06 data from {original_file}...")
    original_data = parse_original_2012di06(original_file)
    print(f"Found {len(original_data)} transitions in original data")
    
    print(f"Loading placement table from {placement_file}...")
    placement_data = parse_placement_table(placement_file)
    print(f"Found {len(placement_data)} gamma placements in table")
    print()
    
    mismatches = find_mismatches(original_data, placement_data)
    report_mismatches(mismatches)
    
    print("=" * 80)
    print(f"SUMMARY: {len(mismatches)} mismatches found out of {len(placement_data)} gamma placements")
