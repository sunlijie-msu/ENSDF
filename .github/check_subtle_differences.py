#!/usr/bin/env python3
"""
Check for subtle numerical differences between placement table and original 2012DI06 data
"""

def check_specific_entries():
    """Check specific entries that might have subtle differences"""
    
    print("CHECKING SPECIFIC ENTRIES FOR SUBTLE DIFFERENCES:")
    print("=" * 80)
    
    # Check 653.1 keV gamma specifically
    print("1. 653.1 keV gamma:")
    print("   Original 2012DI06: 4641.6(5) | (31/2-) | 3988.5(5) | (27/2-) | 653.1(5) |")
    print("   Placement table:   4641.60 | (31/2-)  |  3988.50 | (27/2-)  |    653.1 |              |    653.1")
    print("   ELI difference: 4641.60 vs 4641.6 → 0.00 (within rounding)")
    print("   ELF difference: 3988.50 vs 3988.5 → 0.00 (within rounding)")
    print("   This is just decimal formatting difference - numerically identical")
    print()
    
    # Check a few more problematic entries
    problematic_gammas = [274.4, 380.0, 409.9, 806.0, 806.5, 834.2]
    
    with open("XUNDL/2012DI06_127I_all_gamma_transitions.xundl", 'r') as f:
        original_lines = f.readlines()
    
    with open("XUNDL/2025LAAA_vs_2012DI06.ens", 'r') as f:
        placement_lines = f.readlines()
    
    for gamma in problematic_gammas:
        print(f"{gamma} keV gamma:")
        
        # Find in original data
        orig_found = False
        for line in original_lines:
            if f" {gamma}(" in line or f" {gamma} " in line:
                print(f"   Original: {line.strip()}")
                orig_found = True
                break
        
        if not orig_found:
            print(f"   Original: NOT FOUND")
        
        # Find in placement table
        place_found = False
        for line in placement_lines:
            if f"{gamma}" in line and '|' in line and 'keV' not in line:
                print(f"   Placement: {line.strip()}")
                place_found = True
                break
        
        if not place_found:
            print(f"   Placement: NOT FOUND")
        
        print()

def check_evidence_points_in_data():
    """Re-check the 14 evidence points against actual file data"""
    
    print("RE-CHECKING 14 EVIDENCE POINTS AGAINST ACTUAL DATA:")
    print("=" * 80)
    
    # Load placement data
    placements = {}
    with open("XUNDL/2025LAAA_vs_2012DI06.ens", 'r') as f:
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
                    eg_2025 = parts[6].strip()
                    
                    if eg_2025 != 'TBD' and eg_2025:
                        energy = float(eg_2025)
                        placements[energy] = {
                            'eli': eli,
                            'ji': ji,
                            'elf': elf,
                            'jf': jf
                        }
                except (ValueError, IndexError):
                    continue
    
    # Check evidence points
    evidence_checks = [
        (274.4, "31/2-", "29/2-", "274.4gamma must from 31/2- to 29/2-"),
        (653.1, "31/2-", None, "653.1gamma must from 31/2-, same initial level as 274.4"),
        (806.0, "13/2+", "9/2+", "806.0gamma must from 13/2+ to 9/2+"),
        (806.5, "17/2+", "13/2+", "806.5gamma must from 17/2+ to 13/2+"),
        (187.5, "23/2-", "21/2+", "187.5gamma must from 23/2- to 21/2+"),
        (431.2, "23/2-", None, "431.2 must from same 23/2- level as 187.5"),
        (188.0, "19/2-", "17/2+", "188.0gamma must from 19/2- to 17/2+"),
        (651.5, "19/2-", None, "651.5 must from same 19/2- level as 188.0"),
        (431.5, "21/2+", "19/2+", "431.5gamma must from 21/2+ to 19/2+"),
        (651.0, "9/2+", "5/2+", "651.0gamma must from 9/2+ to ground state 5/2+"),
        (834.2, "13/2+", "11/2+", "834.2gamma must from 13/2+ to 11/2+"),
        (380.0, "29/2-", "27/2-", "380.0gamma must from 29/2- to 27/2-"),
        (409.9, "29/2-", None, "409.9 must from same 29/2- level as 380.0")
    ]
    
    for energy, expected_ji, expected_jf, description in evidence_checks:
        if energy in placements:
            p = placements[energy]
            
            ji_ok = expected_ji in p['ji'] if expected_ji else True
            jf_ok = expected_jf in p['jf'] if expected_jf else True
            
            if ji_ok and jf_ok:
                print(f"✅ {energy} keV: {p['ji']} → {p['jf']} - {description}")
            else:
                print(f"❌ {energy} keV: {p['ji']} → {p['jf']} - FAILS: {description}")
        else:
            print(f"❌ {energy} keV: NOT FOUND - FAILS: {description}")

if __name__ == "__main__":
    check_specific_entries()
    print()
    check_evidence_points_in_data()
