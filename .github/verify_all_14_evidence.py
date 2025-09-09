#!/usr/bin/env python3
"""
Comprehensive verification of all 14 user evidence points for 2025LAAA gamma placements
"""

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
    
    return placements

def verify_evidence_points(placements):
    """Verify all 14 evidence points from user"""
    
    print("VERIFYING ALL 14 USER EVIDENCE POINTS:")
    print("=" * 80)
    
    errors = []
    
    # Evidence 1: 274.4gamma must from 31/2- to 29/2-
    if 274.4 in placements:
        p = placements[274.4]
        if '31/2-' not in p['ji'] or '29/2-' not in p['jf']:
            errors.append(f"❌ Evidence 1: 274.4 keV has {p['ji']} → {p['jf']}, should be 31/2- → 29/2-")
        else:
            print("✅ Evidence 1: 274.4 keV correctly placed 31/2- → 29/2-")
    else:
        errors.append("❌ Evidence 1: 274.4 keV not found in placements")
    
    # Evidence 2: 653.1gamma must from 31/2-, same initial level as 274.4gamma
    if 653.1 in placements and 274.4 in placements:
        p1 = placements[274.4]
        p2 = placements[653.1]
        if abs(p1['eli'] - p2['eli']) > 0.1 or '31/2-' not in p2['ji']:
            errors.append(f"❌ Evidence 2: 653.1 keV from {p2['eli']} keV {p2['ji']}, should share 31/2- level with 274.4 from {p1['eli']} keV")
        else:
            print(f"✅ Evidence 2: 653.1 keV and 274.4 keV both from same 31/2- level at {p1['eli']} keV")
    else:
        errors.append("❌ Evidence 2: Cannot verify - missing 653.1 or 274.4 keV")
    
    # Evidence 3: 806.0gamma must from 13/2+ to 9/2+
    if 806.0 in placements:
        p = placements[806.0]
        if '13/2+' not in p['ji'] or '9/2+' not in p['jf']:
            errors.append(f"❌ Evidence 3: 806.0 keV has {p['ji']} → {p['jf']}, should be 13/2+ → 9/2+")
        else:
            print("✅ Evidence 3: 806.0 keV correctly placed 13/2+ → 9/2+")
    else:
        errors.append("❌ Evidence 3: 806.0 keV not found in placements")
    
    # Evidence 4: 806.5gamma must from 17/2+ to 13/2+
    if 806.5 in placements:
        p = placements[806.5]
        if '17/2+' not in p['ji'] or '13/2+' not in p['jf']:
            errors.append(f"❌ Evidence 4: 806.5 keV has {p['ji']} → {p['jf']}, should be 17/2+ → 13/2+")
        else:
            print("✅ Evidence 4: 806.5 keV correctly placed 17/2+ → 13/2+")
    else:
        errors.append("❌ Evidence 4: 806.5 keV not found in placements")
    
    # Evidence 5: 806.0 and 806.5 in cascade - 806.0's initial = 806.5's final
    if 806.0 in placements and 806.5 in placements:
        p1 = placements[806.0]  # 806.0
        p2 = placements[806.5]  # 806.5
        if abs(p1['eli'] - p2['elf']) > 0.1:
            errors.append(f"❌ Evidence 5: CASCADE BROKEN - 806.0 initial ({p1['eli']}) ≠ 806.5 final ({p2['elf']})")
        else:
            print(f"✅ Evidence 5: CASCADE CONFIRMED - 806.0 initial ({p1['eli']}) = 806.5 final ({p2['elf']})")
    else:
        errors.append("❌ Evidence 5: Cannot verify cascade - missing 806.0 or 806.5 keV")
    
    # Evidence 6: 187.5gamma must from 23/2- at around 2976.6 to 21/2+
    if 187.5 in placements:
        p = placements[187.5]
        if '23/2-' not in p['ji'] or '21/2+' not in p['jf'] or abs(p['eli'] - 2976.6) > 5:
            errors.append(f"❌ Evidence 6: 187.5 keV from {p['eli']} keV {p['ji']} → {p['jf']}, should be ~2976.6 keV 23/2- → 21/2+")
        else:
            print(f"✅ Evidence 6: 187.5 keV correctly placed from {p['eli']} keV 23/2- → 21/2+")
    else:
        errors.append("❌ Evidence 6: 187.5 keV not found in placements")
    
    # Evidence 7: 431.2 and 187.5 from same 23/2- level
    if 431.2 in placements and 187.5 in placements:
        p1 = placements[431.2]
        p2 = placements[187.5]
        if abs(p1['eli'] - p2['eli']) > 0.1 or '23/2-' not in p1['ji']:
            errors.append(f"❌ Evidence 7: 431.2 keV from {p1['eli']} keV {p1['ji']}, should share 23/2- level with 187.5 from {p2['eli']} keV")
        else:
            print(f"✅ Evidence 7: 431.2 keV and 187.5 keV both from same 23/2- level at {p1['eli']} keV")
    else:
        errors.append("❌ Evidence 7: Cannot verify - missing 431.2 or 187.5 keV")
    
    # Evidence 8: 188.0gamma must from 19/2- at around 2545.4 to 17/2+
    if 188.0 in placements:
        p = placements[188.0]
        if '19/2-' not in p['ji'] or '17/2+' not in p['jf'] or abs(p['eli'] - 2545.4) > 5:
            errors.append(f"❌ Evidence 8: 188.0 keV from {p['eli']} keV {p['ji']} → {p['jf']}, should be ~2545.4 keV 19/2- → 17/2+")
        else:
            print(f"✅ Evidence 8: 188.0 keV correctly placed from {p['eli']} keV 19/2- → 17/2+")
    else:
        errors.append("❌ Evidence 8: 188.0 keV not found in placements")
    
    # Evidence 9: 651.5 and 188.0 from same 19/2- level at around 2545.4
    if 651.5 in placements and 188.0 in placements:
        p1 = placements[651.5]
        p2 = placements[188.0]
        if abs(p1['eli'] - p2['eli']) > 0.1 or '19/2-' not in p1['ji']:
            errors.append(f"❌ Evidence 9: 651.5 keV from {p1['eli']} keV {p1['ji']}, should share 19/2- level with 188.0 from {p2['eli']} keV")
        else:
            print(f"✅ Evidence 9: 651.5 keV and 188.0 keV both from same 19/2- level at {p1['eli']} keV")
    else:
        errors.append("❌ Evidence 9: Cannot verify - missing 651.5 or 188.0 keV")
    
    # Evidence 10: 431.5gamma must from 21/2+ to 19/2+
    if 431.5 in placements:
        p = placements[431.5]
        if '21/2+' not in p['ji'] or '19/2+' not in p['jf']:
            errors.append(f"❌ Evidence 10: 431.5 keV has {p['ji']} → {p['jf']}, should be 21/2+ → 19/2+")
        else:
            print("✅ Evidence 10: 431.5 keV correctly placed 21/2+ → 19/2+")
    else:
        errors.append("❌ Evidence 10: 431.5 keV not found in placements")
    
    # Evidence 11: 651.0gamma must from 9/2+ to ground state 5/2+
    if 651.0 in placements:
        p = placements[651.0]
        if '9/2+' not in p['ji'] or '5/2+' not in p['jf'] or abs(p['elf'] - 0.0) > 0.1:
            errors.append(f"❌ Evidence 11: 651.0 keV from {p['eli']} keV {p['ji']} → {p['elf']} keV {p['jf']}, should be 9/2+ → ground state 5/2+")
        else:
            print(f"✅ Evidence 11: 651.0 keV correctly placed {p['ji']} → ground state {p['jf']}")
    else:
        errors.append("❌ Evidence 11: 651.0 keV not found in placements")
    
    # Evidence 12: 834.2gamma must from 13/2+ to 11/2+, same initial level as 244 and 806.0
    if 834.2 in placements:
        p = placements[834.2]
        if '13/2+' not in p['ji'] or '11/2+' not in p['jf']:
            errors.append(f"❌ Evidence 12a: 834.2 keV has {p['ji']} → {p['jf']}, should be 13/2+ → 11/2+")
        else:
            print("✅ Evidence 12a: 834.2 keV correctly placed 13/2+ → 11/2+")
            
        # Check if 834.2, 244.0, and 806.0 share same initial level
        if 244.0 in placements and 806.0 in placements:
            p1 = placements[834.2]
            p2 = placements[244.0]
            p3 = placements[806.0]
            if abs(p1['eli'] - p2['eli']) > 0.1 or abs(p1['eli'] - p3['eli']) > 0.1:
                errors.append(f"❌ Evidence 12b: 834.2 ({p1['eli']}), 244.0 ({p2['eli']}), 806.0 ({p3['eli']}) should share same 13/2+ initial level")
            else:
                print(f"✅ Evidence 12b: 834.2, 244.0, 806.0 all from same 13/2+ level at {p1['eli']} keV")
        else:
            errors.append("❌ Evidence 12b: Cannot verify level sharing - missing 244.0 or 806.0 keV")
    else:
        errors.append("❌ Evidence 12: 834.2 keV not found in placements")
    
    # Evidence 13: 380.0gamma must from 29/2- to 27/2-
    if 380.0 in placements:
        p = placements[380.0]
        if '29/2-' not in p['ji'] or '27/2-' not in p['jf']:
            errors.append(f"❌ Evidence 13: 380.0 keV has {p['ji']} → {p['jf']}, should be 29/2- → 27/2-")
        else:
            print("✅ Evidence 13: 380.0 keV correctly placed 29/2- → 27/2-")
    else:
        errors.append("❌ Evidence 13: 380.0 keV not found in placements")
    
    # Evidence 14: 409.9gamma must from 29/2-, same initial level as 380.0
    if 409.9 in placements and 380.0 in placements:
        p1 = placements[409.9]
        p2 = placements[380.0]
        if abs(p1['eli'] - p2['eli']) > 0.1 or '29/2-' not in p1['ji']:
            errors.append(f"❌ Evidence 14: 409.9 keV from {p1['eli']} keV {p1['ji']}, should share 29/2- level with 380.0 from {p2['eli']} keV")
        else:
            print(f"✅ Evidence 14: 409.9 keV and 380.0 keV both from same 29/2- level at {p1['eli']} keV")
    else:
        errors.append("❌ Evidence 14: Cannot verify - missing 409.9 or 380.0 keV")
    
    print("=" * 80)
    
    if errors:
        print(f"❌ VERIFICATION FAILED: {len(errors)} ERRORS FOUND")
        print()
        for error in errors:
            print(error)
        return False
    else:
        print("✅ ALL 14 EVIDENCE POINTS VERIFIED SUCCESSFULLY!")
        return True

if __name__ == "__main__":
    filename = "XUNDL/2025LAAA_vs_2012DI06.ens"
    placements = parse_placement_table(filename)
    
    print(f"Loaded {len(placements)} gamma placements from {filename}")
    print()
    
    success = verify_evidence_points(placements)
    
    if not success:
        print("\n🚨 CRITICAL: Placement table does not satisfy user requirements!")
        print("All 14 evidence points must be satisfied for accurate nuclear structure.")
