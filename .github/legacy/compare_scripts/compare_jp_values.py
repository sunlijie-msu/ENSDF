import json
import re
import sys

def extract_jp_from_ensdf(file_path):
    """
    Extracts J-π values from an ENSDF file.
    Returns a dictionary with energy as key and J-π as value.
    """
    jp_data = {}
    with open(file_path, 'r') as f:
        for line in f:
            if len(line) >= 80 and line[7] == 'L' and line[6] == ' ':
                try:
                    energy_str = line[9:19].strip()
                    jp_str = line[22:39].strip()
                    
                    if energy_str and jp_str:
                        energy = float(energy_str)
                        jp_data[energy] = jp_str
                except (ValueError, IndexError):
                    continue
    return jp_data

def extract_jp_from_json(json_file_path):
    """
    Extracts J-π values from the structured JSON data.
    """
    jp_data = {}
    
    # Try different encodings
    for encoding in ['utf-16', 'utf-8', 'utf-8-sig']:
        try:
            with open(json_file_path, 'r', encoding=encoding) as f:
                data = json.load(f)
            break
        except (UnicodeError, UnicodeDecodeError):
            continue
    else:
        print(f"Could not decode {json_file_path} with any standard encoding")
        return jp_data
    
    # Handle structured JSON format
    if 'levels' in data:
        for level in data['levels']:
            energy = level.get('energy_keV')
            jp = level.get('j_pi')
            if energy is not None and jp is not None:
                jp_data[float(energy)] = jp
    else:
        # Handle the original flat format if it exists
        for energy_str, level_info in data.items():
            if isinstance(level_info, dict):
                original_line = level_info.get('original_line', '')
                if len(original_line) >= 80:
                    jp_str = original_line[22:39].strip()
                    if jp_str:
                        try:
                            energy = float(energy_str)
                            jp_data[energy] = jp_str
                        except ValueError:
                            continue
    
    return jp_data

def compare_jp_data(se09_ens_data, se09_json_data, adopted_data):
    """
    Compare J-π data across the three sources and report discrepancies.
    """
    print("=== J-π Value Transfer Analysis ===")
    print()
    
    # First check: Are all J-π values from 2019Se09.json transferred to 2019SE09.ens?
    print("1. Checking transfer from 2019Se09.json to 2019SE09.ens:")
    print("-" * 60)
    
    json_missing_in_ens = []
    for energy, jp in se09_json_data.items():
        if energy not in se09_ens_data:
            json_missing_in_ens.append((energy, jp))
        elif se09_ens_data[energy] != jp:
            print(f"  MISMATCH at {energy} keV: JSON='{jp}' vs ENS='{se09_ens_data[energy]}'")
    
    if json_missing_in_ens:
        print("  J-π values in JSON but missing in ENS:")
        for energy, jp in json_missing_in_ens:
            print(f"    {energy} keV: {jp}")
    else:
        print("  ✓ All J-π values from JSON are present in ENS file")
    
    print()
    
    # Second check: Are all J-π values from 2019SE09.ens transferred to adopted file?
    print("2. Checking transfer from 2019SE09.ens to Cl35_32s_a_p.ens:")
    print("-" * 60)
    
    # Find levels with 'K' flag in adopted file (these should come from 2019Se09)
    k_flag_levels = []
    with open('d:\\X\\ND\\ENSDF\\A35\\Cl35\\new\\Cl35_32s_a_p.ens', 'r') as f:
        for line_num, line in enumerate(f, 1):
            if len(line) >= 80 and line[7] == 'L' and line[6] == ' ':
                flag = line[76:77].strip()
                if flag == 'K':
                    energy_str = line[9:19].strip()
                    jp_str = line[22:39].strip()
                    if energy_str:
                        try:
                            energy = float(energy_str)
                            k_flag_levels.append((energy, jp_str, line_num))
                        except ValueError:
                            continue
    
    print(f"  Found {len(k_flag_levels)} levels with 'K' flag in adopted file")
    print()
    
    # Check if J-π values are properly transferred for K-flag levels
    missing_jp = []
    mismatched_jp = []
    
    for energy, adopted_jp, line_num in k_flag_levels:
        # Find closest match in 2019SE09.ens data
        closest_energy = None
        min_diff = float('inf')
        for se09_energy in se09_ens_data.keys():
            diff = abs(energy - se09_energy)
            if diff < min_diff:
                min_diff = diff
                closest_energy = se09_energy
        
        if closest_energy and min_diff <= 5.0:  # Within 5 keV tolerance
            se09_jp = se09_ens_data[closest_energy]
            if not adopted_jp and se09_jp:
                missing_jp.append((energy, se09_jp, line_num))
            elif adopted_jp != se09_jp and se09_jp:
                mismatched_jp.append((energy, adopted_jp, se09_jp, line_num))
    
    if missing_jp:
        print("  Missing J-π values in adopted file (should be transferred from 2019Se09):")
        for energy, se09_jp, line_num in missing_jp:
            print(f"    Line {line_num}: {energy} keV missing J-π '{se09_jp}'")
    
    if mismatched_jp:
        print("  Mismatched J-π values:")
        for energy, adopted_jp, se09_jp, line_num in mismatched_jp:
            print(f"    Line {line_num}: {energy} keV: Adopted='{adopted_jp}' vs 2019Se09='{se09_jp}'")
    
    if not missing_jp and not mismatched_jp:
        print("  ✓ All J-π values from 2019Se09 are properly transferred to adopted file")
    
    print()
    
    # Summary of all J-π values in 2019SE09.ens
    print("3. Summary of all J-π values in 2019SE09.ens:")
    print("-" * 60)
    jp_count = 0
    for energy, jp in sorted(se09_ens_data.items()):
        if jp:
            print(f"  {energy:8.1f} keV: {jp}")
            jp_count += 1
    
    print(f"\n  Total J-π assignments in 2019SE09.ens: {jp_count}")
    
    return missing_jp, mismatched_jp

if __name__ == "__main__":
    # Extract J-π data from all sources
    se09_ens_data = extract_jp_from_ensdf('d:\\X\\ND\\ENSDF\\A35\\Cl35\\temp\\2019SE09.ens')
    se09_json_data = extract_jp_from_json('d:\\X\\ND\\ENSDF\\A35\\Cl35\\temp\\2019SE09.json')
    adopted_data = extract_jp_from_ensdf('d:\\X\\ND\\ENSDF\\A35\\Cl35\\new\\Cl35_32s_a_p.ens')
    
    missing_jp, mismatched_jp = compare_jp_data(se09_ens_data, se09_json_data, adopted_data)
    
    # Return appropriate exit code
    if missing_jp or mismatched_jp:
        sys.exit(1)
    else:
        sys.exit(0)