#!/usr/bin/env python3
"""
Detailed side-by-side comparison of placement table vs original 2012DI06 data
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

def detailed_comparison(original_data, placement_data):
    """Show detailed side-by-side comparison"""
    
    print("DETAILED SIDE-BY-SIDE COMPARISON:")
    print("=" * 120)
    print(f"{'EG_2025':<8} {'EG_2012':<8} {'Field':<6} {'Placement':<25} {'Original':<25} {'Match':<6}")
    print("-" * 120)
    
    differences = []
    
    # Sort by 2025 energy for systematic check
    for eg_2025 in sorted(placement_data.keys()):
        placement = placement_data[eg_2025]
        eg_2012 = placement['eg_2012']
        
        if eg_2012 in original_data:
            orig = original_data[eg_2012]
            
            # Compare each field
            fields_to_check = [
                ('ELI', placement['eli'], orig['eli']),
                ('JI', placement['ji'], orig['ji']),
                ('ELF', placement['elf'], orig['elf']),
                ('JF', placement['jf'], orig['jf']),
                ('RI', placement['ri_2012'], orig['ri'])
            ]
            
            for field_name, placement_val, original_val in fields_to_check:
                if field_name in ['ELI', 'ELF']:
                    # Numerical comparison
                    match = abs(placement_val - original_val) < 0.01
                    if not match:
                        differences.append(f"{eg_2025} keV: {field_name} {placement_val} ≠ {original_val}")
                        print(f"{eg_2025:<8.1f} {eg_2012:<8.1f} {field_name:<6} {placement_val:<25} {original_val:<25} {'❌':<6}")
                else:
                    # String comparison
                    match = str(placement_val) == str(original_val)
                    if not match:
                        # Check if it's just parentheses or formatting difference
                        if field_name in ['JI', 'JF']:
                            clean_p = str(placement_val).replace('(', '').replace(')', '')
                            clean_o = str(original_val).replace('(', '').replace(')', '')
                            if clean_p == clean_o:
                                match = True  # Just parentheses difference
                        
                        if not match:
                            differences.append(f"{eg_2025} keV: {field_name} '{placement_val}' ≠ '{original_val}'")
                            print(f"{eg_2025:<8.1f} {eg_2012:<8.1f} {field_name:<6} {str(placement_val):<25} {str(original_val):<25} {'❌':<6}")
        else:
            differences.append(f"{eg_2025} keV: EG_2012 {eg_2012} not found in original data")
            print(f"{eg_2025:<8.1f} {eg_2012:<8.1f} {'ALL':<6} {'PRESENT':<25} {'NOT FOUND':<25} {'❌':<6}")
    
    print("-" * 120)
    print(f"Total differences found: {len(differences)}")
    
    if differences:
        print("\nSUMMARY OF DIFFERENCES:")
        for diff in differences:
            print(f"  • {diff}")
    else:
        print("\n✅ All fields match perfectly!")
    
    return differences

def show_sample_entries(original_data, placement_data):
    """Show first few entries for verification"""
    print("\nSAMPLE VERIFICATION (first 5 gammas):")
    print("=" * 80)
    
    count = 0
    for eg_2025 in sorted(placement_data.keys()):
        if count >= 5:
            break
        
        placement = placement_data[eg_2025]
        eg_2012 = placement['eg_2012']
        
        print(f"\n{count+1}. 2025LAAA Gamma: {eg_2025} keV")
        print(f"   Placement: ELI={placement['eli']}, JI='{placement['ji']}', ELF={placement['elf']}, JF='{placement['jf']}', EG={eg_2012}, RI='{placement['ri_2012']}'")
        
        if eg_2012 in original_data:
            orig = original_data[eg_2012]
            print(f"   Original:  ELI={orig['eli']}, JI='{orig['ji']}', ELF={orig['elf']}, JF='{orig['jf']}', EG={orig['eg']}, RI='{orig['ri']}'")
        else:
            print(f"   Original:  NOT FOUND!")
        
        count += 1

if __name__ == "__main__":
    original_file = "XUNDL/2012DI06_127I_all_gamma_transitions.xundl"
    placement_file = "XUNDL/2025LAAA_vs_2012DI06.ens"
    
    print(f"Loading data files...")
    original_data = parse_original_2012di06(original_file)
    placement_data = parse_placement_table(placement_file)
    
    print(f"Original data: {len(original_data)} transitions")
    print(f"Placement data: {len(placement_data)} gammas")
    print()
    
    differences = detailed_comparison(original_data, placement_data)
    show_sample_entries(original_data, placement_data)
