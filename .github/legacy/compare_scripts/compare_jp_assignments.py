#!/usr/bin/env python3
"""
Compare J|π assignments between 1969Gr23 image, JSON data, and ENSDF file.
Created in .github folder as required.
"""

import json

def load_json_data():
    """Load data from both JSON files."""
    with open('A35/Cl35/temp/1969Gr23.json', 'r') as f:
        data_1969 = json.load(f)
    
    with open('A35/Cl35/temp/1970Mo01.json', 'r') as f:
        data_1970 = json.load(f)
    
    return data_1969, data_1970

def extract_jp_from_ensdf():
    """Extract J|π values from ENSDF S comments."""
    ensdf_jp = {}
    
    with open('A35/Cl35/new/Cl35_34s_3he_d.ens', 'r') as f:
        content = f.read()
    
    # Look for patterns like "for J|p=value" in 1969Gr23 lines
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if ' L ' in line[6:10] and line.strip():
            # Extract energy from L-record
            parts = line.split()
            if len(parts) >= 3:
                try:
                    energy = int(parts[2])
                    
                    # Look ahead for S comment lines
                    for j in range(i+1, min(i+10, len(lines))):
                        next_line = lines[j]
                        if 'for J|p=' in next_line and '1969Gr23' in next_line:
                            # Extract J|π from S comment
                            start = next_line.find('for J|p=') + 8
                            # Look for end markers
                            end_markers = [';', '.', ' in']
                            end = len(next_line)
                            for marker in end_markers:
                                marker_pos = next_line.find(marker, start)
                                if marker_pos != -1:
                                    end = min(end, marker_pos)
                            
                            jp = next_line[start:end].strip()
                            ensdf_jp[energy] = jp
                            break
                        elif ' L ' in next_line[6:10]:  # Hit next level
                            break
                except:
                    continue
    
    return ensdf_jp

def main():
    """Main comparison function."""
    print("J|π Assignment Comparison")
    print("=" * 60)
    
    # Load data
    data_1969, data_1970 = load_json_data()
    ensdf_jp = extract_jp_from_ensdf()
    
    print(f"{'Energy':>8} | {'1969Gr23 JSON':>15} | {'ENSDF Comment':>15} | {'Match?':>8}")
    print("-" * 60)
    
    for level in data_1969['levels']:
        energy_mev = level['excitation_energy_MeV']
        energy_kev = int(energy_mev * 1000)
        
        json_jp = level.get('spin_parity', 'null')
        ensdf_jp_val = ensdf_jp.get(energy_kev, 'not found')
        
        if json_jp == 'null' or json_jp is None:
            json_jp = 'null'
        
        match = "YES" if json_jp == ensdf_jp_val else "NO"
        
        print(f"{energy_kev:>8} | {json_jp:>15} | {ensdf_jp_val:>15} | {match:>8}")

if __name__ == "__main__":
    main()
