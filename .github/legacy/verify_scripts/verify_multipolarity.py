#!/usr/bin/env python3
"""
Verify multipolarity assignments for the 10 gamma transitions from the image.
"""

def verify_multipolarity_assignments():
    """Verify that all 10 gamma transitions have correct multipolarity assignments."""
    
    # Expected assignments based on user request
    expected_assignments = {
        '490.3': 'E1',  # The one E1 transition
        '982.1': 'E2',  # E2 transitions (9 total)
        '431.2': 'E2',
        '651.5': 'E2', 
        '658.7': 'E2',
        '877.0': 'E2',
        '610.0': 'E2',
        '763.3': 'E2',
        '659.0': 'E2',
        '744.9': 'E2'
    }
    
    current_assignments = {}
    
    with open("XUNDL/2025LAAA_CH11036_127I.ens", 'r') as f:
        for line in f:
            if len(line) >= 8 and line[7] == 'G':
                # Extract energy from columns 10-19
                energy_str = line[9:19].strip()
                if energy_str in expected_assignments:
                    # Extract multipolarity from columns 32-41
                    multipolarity = line[31:41].strip()
                    if multipolarity:
                        current_assignments[energy_str] = multipolarity
    
    print("MULTIPOLARITY ASSIGNMENT VERIFICATION")
    print("=" * 50)
    print(f"{'Energy (keV)':<12} {'Expected':<10} {'Current':<10} {'Status'}")
    print("-" * 50)
    
    all_correct = True
    e1_count = 0
    e2_count = 0
    
    for energy in sorted(expected_assignments.keys(), key=float):
        expected = expected_assignments[energy]
        current = current_assignments.get(energy, "MISSING")
        status = "✅" if current == expected else "❌"
        
        if current == expected:
            if current == "E1":
                e1_count += 1
            elif current == "E2":
                e2_count += 1
        else:
            all_correct = False
            
        print(f"{energy:<12} {expected:<10} {current:<10} {status}")
    
    print("\n" + "=" * 50)
    print(f"E1 transitions: {e1_count}/1")
    print(f"E2 transitions: {e2_count}/9")
    print(f"Total assigned: {len(current_assignments)}/10")
    
    if all_correct and len(current_assignments) == 10:
        print("\n🎯 PERFECT! All multipolarity assignments are correct.")
        print("✅ TASK COMPLETED SUCCESSFULLY")
    else:
        print(f"\n❌ Issues detected - need correction")
    
    return all_correct

if __name__ == "__main__":
    verify_multipolarity_assignments()
