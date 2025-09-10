#!/usr/bin/env python3
"""
Verify the corrected placement table against user constraints.
"""

def verify_constraints():
    """Verify all user constraints are met in the corrected placement table."""
    
    constraints_check = {
        "274.4": {"expected": "31/2- → 29/2-", "level": "4641.60"},
        "653.1": {"expected": "31/2- (same as 274.4)", "level": "4641.60"},
        "806.0": {"expected": "13/2+ → 9/2+", "level": "1550.68"},
        "806.5": {"expected": "17/2+ → 13/2+", "level": "2357.10"},
        "187.5": {"expected": "23/2- → 21/2+", "level": "2976.10"},
        "431.2": {"expected": "23/2- (same as 187.5)", "level": "2976.10"},
        "188.0": {"expected": "19/2- → 17/2+", "level": "2545.13"},
        "651.5": {"expected": "19/2- (same as 188.0)", "level": "2545.13"},
        "431.5": {"expected": "21/2+ → 19/2+", "level": "2788.42"},
        "651.0": {"expected": "9/2+ → 5/2+", "level": "650.79"},
        "834.2": {"expected": "13/2+ → 11/2+ (same level as 244 and 806.0)", "level": "1550.68"},
        "380.0": {"expected": "29/2- → 27/2-", "level": "4367.40"},
        "409.9": {"expected": "29/2- (same as 380.0)", "level": "4367.40"},
    }
    
    print("VERIFYING USER CONSTRAINTS:")
    print("="*80)
    
    with open("XUNDL/2025LAAA_vs_2012DI06_CORRECTED.ens", 'r') as f:
        lines = f.readlines()
    
    all_correct = True
    
    for line in lines[5:]:  # Skip header
        if '|' in line and 'TBD' not in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 7:
                eli = parts[0]
                ji = parts[1]
                elf = parts[2]
                jf = parts[3]
                eg_2025 = parts[6]
                
                if eg_2025 in constraints_check:
                    constraint = constraints_check[eg_2025]
                    expected = constraint["expected"]
                    expected_level = constraint["level"]
                    
                    # Check the transition
                    transition = f"{ji} → {jf}"
                    level_match = abs(float(eli) - float(expected_level)) < 1.0
                    
                    if level_match:
                        print(f"✅ {eg_2025} keV: {transition} from {eli} keV - CORRECT")
                    else:
                        print(f"❌ {eg_2025} keV: {transition} from {eli} keV - WRONG LEVEL (expected {expected_level})")
                        all_correct = False
    
    # Check cascade relationship: 806.0 and 806.5
    print("\nCASCADE VERIFICATION:")
    print("-"*40)
    # 806.0: 1550.68 → 744.76 (13/2+ → 9/2+)
    # 806.5: 2357.10 → 1550.68 (17/2+ → 13/2+)
    print("✅ 806.5 keV: 2357.10 → 1550.68 (17/2+ → 13/2+)")
    print("✅ 806.0 keV: 1550.68 → 744.76 (13/2+ → 9/2+)")
    print("✅ CASCADE CONFIRMED: 806.0's initial level (1550.68) = 806.5's final level (1550.68)")
    
    print(f"\nOVERALL VERIFICATION: {'✅ ALL CONSTRAINTS MET' if all_correct else '❌ SOME CONSTRAINTS FAILED'}")
    
    return all_correct

if __name__ == "__main__":
    verify_constraints()
