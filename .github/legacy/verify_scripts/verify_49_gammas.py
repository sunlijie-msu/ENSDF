#!/usr/bin/env python3
"""
Verify that 2025LAAA_vs_2012DI06.ens contains all 49 gamma energies from the JSON file
with exact digit-by-digit accuracy.
"""
import json

def extract_json_gammas():
    """Extract all gamma energies from the JSON file."""
    with open("XUNDL/2025LAAA_CH11036_127I_gamma_energies.json", 'r') as f:
        data = json.load(f)
    
    gammas = []
    for transition in data['gamma_transitions']:
        energy = transition['energy']['value']
        gammas.append(energy)
    
    return sorted(gammas)

def extract_placement_table_gammas():
    """Extract all 2025LAAA gamma energies from the placement table."""
    gammas_2025 = []
    
    with open("XUNDL/2025LAAA_vs_2012DI06.ens", 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        if line.strip() and not line.startswith('=') and not line.startswith('-') and not line.startswith('FINAL') and '|' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 7:
                try:
                    eg_2025 = parts[6]
                    
                    if eg_2025 and eg_2025 != 'EG_2025':
                        gammas_2025.append(float(eg_2025))
                except (ValueError, IndexError):
                    continue
    
    return sorted(gammas_2025)

def main():
    print("Extracting gamma energies from JSON file...")
    json_gammas = extract_json_gammas()
    print(f"Found {len(json_gammas)} gamma energies in JSON")
    
    print("\nExtracting gamma energies from placement table...")
    placement_gammas = extract_placement_table_gammas()
    print(f"Found {len(placement_gammas)} gamma energies in placement table")
    
    print("\n" + "="*80)
    print("DIGIT-BY-DIGIT COMPARISON:")
    print("="*80)
    
    # Check if all JSON gammas are in placement table
    missing_from_placement = []
    for i, gamma in enumerate(json_gammas, 1):
        if gamma in placement_gammas:
            print(f"{i:2d}. ✅ {gamma:7.1f} keV - FOUND in placement table")
        else:
            print(f"{i:2d}. ❌ {gamma:7.1f} keV - MISSING from placement table")
            missing_from_placement.append(gamma)
    
    print("\n" + "="*80)
    print("EXTRA GAMMAS IN PLACEMENT TABLE (not in JSON):")
    print("="*80)
    
    extra_in_placement = []
    for gamma in placement_gammas:
        if gamma not in json_gammas:
            print(f"❌ {gamma:7.1f} keV - EXTRA in placement table")
            extra_in_placement.append(gamma)
    
    if not extra_in_placement:
        print("✅ No extra gammas found in placement table")
    
    print("\n" + "="*80)
    print("SUMMARY:")
    print("="*80)
    print(f"JSON file gamma count: {len(json_gammas)}")
    print(f"Placement table gamma count: {len(placement_gammas)}")
    print(f"Missing from placement: {len(missing_from_placement)}")
    print(f"Extra in placement: {len(extra_in_placement)}")
    
    if len(json_gammas) == len(placement_gammas) and not missing_from_placement and not extra_in_placement:
        print("✅ PERFECT MATCH: All 49 gamma energies are exactly present in placement table!")
    else:
        print("❌ MISMATCH: Placement table does not contain all JSON gamma energies!")
    
    print("\nDetailed lists:")
    print(f"Missing from placement: {missing_from_placement}")
    print(f"Extra in placement: {extra_in_placement}")

if __name__ == "__main__":
    main()
