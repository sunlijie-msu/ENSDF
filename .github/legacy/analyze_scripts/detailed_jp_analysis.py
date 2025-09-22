import json

def detailed_jp_analysis():
    """
    Detailed analysis of the missing J-π values.
    """
    # Load the JSON data
    with open('d:\\X\\ND\\ENSDF\\A35\\Cl35\\temp\\2019SE09.json', 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    # Extract levels with J-π from JSON
    json_jp_levels = []
    for level in json_data['levels']:
        energy = level.get('energy_keV')
        jp = level.get('j_pi')
        if energy is not None and jp is not None:
            json_jp_levels.append((energy, jp))
    
    print(f"Found {len(json_jp_levels)} levels with J-π in JSON file:")
    for energy, jp in sorted(json_jp_levels):
        print(f"  {energy:8.1f} keV: {jp}")
    
    print("\n" + "="*60)
    
    # Load ENS data
    ens_jp_levels = []
    with open('d:\\X\\ND\\ENSDF\\A35\\Cl35\\temp\\2019SE09.ens', 'r') as f:
        for line in f:
            if len(line) >= 80 and line[7] == 'L' and line[6] == ' ':
                try:
                    energy_str = line[9:19].strip()
                    jp_str = line[22:39].strip()
                    
                    if energy_str and jp_str:
                        energy = float(energy_str)
                        ens_jp_levels.append((energy, jp_str))
                except (ValueError, IndexError):
                    continue
    
    print(f"Found {len(ens_jp_levels)} levels with J-π in ENS file:")
    for energy, jp in sorted(ens_jp_levels):
        print(f"  {energy:8.1f} keV: {jp}")
    
    print("\n" + "="*60)
    print("MISSING TRANSFERS (in JSON but not in ENS):")
    
    # Check for missing transfers with tolerance
    tolerance = 5.0  # keV
    missing_count = 0
    
    for json_energy, json_jp in json_jp_levels:
        found_match = False
        for ens_energy, ens_jp in ens_jp_levels:
            if abs(json_energy - ens_energy) <= tolerance:
                found_match = True
                if json_jp != ens_jp:
                    print(f"  MISMATCH: {json_energy} keV - JSON: '{json_jp}' vs ENS: '{ens_jp}'")
                break
        
        if not found_match:
            missing_count += 1
            print(f"  MISSING: {json_energy:8.1f} keV with J-π '{json_jp}' not found in ENS")
    
    if missing_count == 0:
        print("  None - all J-π values are properly transferred!")
    
    print(f"\nTotal missing J-π transfers: {missing_count}")

if __name__ == "__main__":
    detailed_jp_analysis()