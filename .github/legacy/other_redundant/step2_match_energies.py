#!/usr/bin/env python3
"""
Step 2: List 2025LAAA gammas and match with close 2012DI06 energies
"""
import json

def step2_match_energies():
    # Load 2025LAAA gamma energies
    with open("XUNDL/2025LAAA_CH11036_127I_gamma_energies.json", "r") as f:
        data_2025 = json.load(f)
    
    gammas_2025 = []
    for gamma in data_2025["gamma_transitions"]:
        energy = gamma["energy"]["value"]
        status = gamma.get("status", "standard")
        gammas_2025.append((energy, status))
    
    # Close energy groups from 2012DI06 (from Step 1)
    close_groups_2012 = [
        (187.5, 188.0),
        (195.4, 195.8),
        (213.1, 213.5),
        (268.3, 269.0),
        (270.5, 271.3),
        (274.2, 274.5, 274.6),
        (289.9, 290.5),
        (348.6, 349.3),
        (357.3, 357.8),
        (370.5, 371.0),
        (409.0, 409.5),
        (431.0, 431.5),
        (466.8, 467.5),
        (518.5, 519.4),
        (651.0, 651.5),
        (655.7, 656.0),
        (658.5, 659.0),
        (761.0, 761.2),
        (805.9, 806.4),
        (833.5, 834.2)
    ]
    
    print("STEP 2: 2025LAAA GAMMA ENERGIES AND POTENTIAL MATCHES")
    print("=" * 80)
    print(f"Total 2025LAAA gamma energies: {len(gammas_2025)}")
    print()
    
    print("ALL 2025LAAA GAMMA ENERGIES:")
    print("-" * 40)
    for i, (energy, status) in enumerate(gammas_2025, 1):
        status_str = f" ({status})" if status != "standard" else ""
        print(f"{i:2d}. {energy:6.1f} keV{status_str}")
    print()
    
    print("POTENTIAL MATCHING ISSUES (2025LAAA energies that match close 2012DI06 groups):")
    print("=" * 80)
    
    matches_found = []
    
    for group in close_groups_2012:
        for energy_2025, status in gammas_2025:
            # Check if 2025LAAA energy is close to any energy in this group
            for energy_2012 in group:
                if abs(energy_2025 - energy_2012) < 1.0:
                    matches_found.append((energy_2025, status, group))
                    break
    
    # Remove duplicates and sort
    unique_matches = {}
    for energy_2025, status, group in matches_found:
        if energy_2025 not in unique_matches:
            unique_matches[energy_2025] = (status, group)
    
    if not unique_matches:
        print("No potential matching issues found.")
    else:
        for i, (energy_2025, (status, group)) in enumerate(sorted(unique_matches.items()), 1):
            print(f"\nISSUE {i}:")
            print(f"  2025LAAA: {energy_2025:6.1f} keV{' (' + status + ')' if status != 'standard' else ''}")
            print(f"  Matches close 2012DI06 group: {', '.join(f'{e:.1f}' for e in group)} keV")
            
            # Show which specific 2012DI06 energy is closest
            closest_2012 = min(group, key=lambda x: abs(x - energy_2025))
            diff = abs(energy_2025 - closest_2012)
            print(f"  Closest match: {closest_2012:.1f} keV (difference: {diff:.1f} keV)")
            
            # Check if it's an exact or near-exact match
            if diff < 0.2:
                print(f"  *** VERY CLOSE MATCH - likely same transition ***")
            elif diff < 0.5:
                print(f"  *** CLOSE MATCH - could be same transition ***")
            else:
                print(f"  *** POTENTIAL CONFUSION - different transitions ***")
    
    print("\n" + "=" * 80)
    print("CRITICAL QUESTIONS FOR MANUAL VERIFICATION:")
    print("=" * 80)
    
    critical_cases = []
    for energy_2025, (status, group) in sorted(unique_matches.items()):
        if len(group) > 2 or any(abs(energy_2025 - e) > 0.3 for e in group):
            critical_cases.append((energy_2025, status, group))
    
    if critical_cases:
        print("\nThese cases require J,π information to distinguish:")
        for i, (energy_2025, status, group) in enumerate(critical_cases, 1):
            print(f"\n{i}. {energy_2025:.1f} keV (2025LAAA)")
            print(f"   Could match: {', '.join(f'{e:.1f}' for e in group)} keV (2012DI06)")
            print(f"   NEED: Initial and final level J,π for proper assignment")
    
    return unique_matches

if __name__ == "__main__":
    step2_match_energies()
