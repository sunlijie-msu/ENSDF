import json
import re

# Load JSON data
with open('1984CA14_final_corrected.json', 'r') as f:
    json_data = json.load(f)

# Read ENSDF file and extract L-records
with open('../new/S35_ng_resonances.ens', 'r') as f:
    ensdf_lines = f.readlines()

ensdf_levels = []
for line_num, line in enumerate(ensdf_lines):
    if len(line) >= 8 and line[7] == 'L':
        # ENSDF L-record format:
        # Cols 1-5: NUCID, 6: blank, 7: blank, 8: L, 9: blank
        # Cols 10-19: Energy (level energy)
        # Cols 20-21: DE (energy uncertainty)
        # Cols 23-39: J-π (spin-parity)
        # Cols 40-49: T (half-life)
        # Cols 56-64: L (L-transfer)
        # Cols 65-74: S (En(lab) - neutron lab energy)
        
        energy_str = line[9:19].strip()
        jp_str = line[22:39].strip() if len(line) > 39 else ""
        l_transfer_str = line[55:65].strip() if len(line) > 65 else ""
        en_lab_str = line[64:74].strip() if len(line) > 74 else ""
        
        ensdf_levels.append({
            'line_num': line_num + 1,
            'raw_line': line.rstrip(),
            'energy': energy_str,
            'jp': jp_str if jp_str else None,
            'l_transfer': l_transfer_str if l_transfer_str else None,
            'en_lab': en_lab_str
        })

print(f"Found {len(ensdf_levels)} L-records in ENSDF file")
print(f"Found {len(json_data)} entries in JSON file")

# Create matching function
def normalize_energy(energy_str):
    """Normalize energy string for comparison"""
    if not energy_str:
        return ""
    # Remove parentheses and spaces
    clean = energy_str.replace('(', '').replace(')', '').strip()
    return clean

# Find matches between JSON and ENSDF
matches = []
unmatched_json = []

for i, json_entry in enumerate(json_data):
    json_energy = json_entry['En_keV']
    json_jp = json_entry.get('Jp')
    json_l_transfer = json_entry.get('l_transfer')
    
    # Normalize JSON energy for matching
    json_en_norm = normalize_energy(json_energy)
    
    # Find corresponding ENSDF level by En(lab) match
    ensdf_match = None
    for ensdf_level in ensdf_levels:
        ensdf_en_lab = ensdf_level['en_lab']
        ensdf_en_norm = normalize_energy(ensdf_en_lab)
        
        # Try exact match
        if json_en_norm == ensdf_en_norm:
            ensdf_match = ensdf_level
            break
        
        # Try base match (before uncertainty)
        json_base = json_en_norm.split('(')[0] if '(' in json_energy else json_en_norm
        ensdf_base = ensdf_en_norm.split('(')[0] if '(' in ensdf_en_lab else ensdf_en_norm
        
        if json_base == ensdf_base:
            ensdf_match = ensdf_level
            break
    
    if ensdf_match:
        # Convert ENSDF L-transfer format to compare with JSON
        ensdf_l_raw = ensdf_match['l_transfer']
        ensdf_l_converted = None
        
        if ensdf_l_raw:
            if ensdf_l_raw.startswith('[') and ensdf_l_raw.endswith(']'):
                # Format like [2] -> l = 2
                l_val = ensdf_l_raw[1:-1]
                if l_val == '1':
                    ensdf_l_converted = "l = 1,2 (D)"  # Default assumption
                elif l_val == '2':
                    ensdf_l_converted = "l = 2 (E)"
                else:
                    ensdf_l_converted = f"l = {l_val}"
            else:
                ensdf_l_converted = ensdf_l_raw
        
        match_info = {
            'json_index': i,
            'json_energy': json_energy,
            'ensdf_line_num': ensdf_match['line_num'],
            'ensdf_en_lab': ensdf_match['en_lab'],
            'json_jp': json_jp,
            'ensdf_jp': ensdf_match['jp'],
            'json_l_transfer': json_l_transfer,
            'ensdf_l_transfer': ensdf_l_raw,
            'ensdf_l_converted': ensdf_l_converted,
            'raw_line': ensdf_match['raw_line']
        }
        
        matches.append(match_info)
    else:
        unmatched_json.append({
            'index': i,
            'energy': json_energy,
            'jp': json_jp,
            'l_transfer': json_l_transfer
        })

print(f"\nMatched {len(matches)} entries")
print(f"Unmatched JSON entries: {len(unmatched_json)}")

# Analyze discrepancies
jp_updates_needed = []
l_transfer_updates_needed = []

for match in matches:
    # Check if Jp needs update
    if match['json_jp'] and not match['ensdf_jp']:
        jp_updates_needed.append(match)
    elif match['json_jp'] != match['ensdf_jp']:
        jp_updates_needed.append(match)
    
    # Check if l-transfer needs update  
    if match['json_l_transfer'] and not match['ensdf_l_transfer']:
        l_transfer_updates_needed.append(match)
    elif match['json_l_transfer'] != match['ensdf_l_converted']:
        l_transfer_updates_needed.append(match)

print(f"\n=== UPDATE REQUIREMENTS ===")
print(f"Jp updates needed: {len(jp_updates_needed)}")
print(f"L-transfer updates needed: {len(l_transfer_updates_needed)}")

# Show first few updates needed
print(f"\n=== FIRST 10 Jp UPDATES NEEDED ===")
for i, update in enumerate(jp_updates_needed[:10]):
    print(f"{i+1}. Line {update['ensdf_line_num']}: {update['json_energy']}")
    print(f"   Current ENSDF Jp: '{update['ensdf_jp']}'")
    print(f"   JSON Jp: '{update['json_jp']}'")
    print(f"   ENSDF line: {update['raw_line']}")
    print()

print(f"\n=== FIRST 10 L-TRANSFER UPDATES NEEDED ===")
for i, update in enumerate(l_transfer_updates_needed[:10]):
    print(f"{i+1}. Line {update['ensdf_line_num']}: {update['json_energy']}")
    print(f"   Current ENSDF L: '{update['ensdf_l_transfer']}'")
    print(f"   JSON L-transfer: '{update['json_l_transfer']}'")
    print(f"   ENSDF line: {update['raw_line']}")
    print()

# Save update lists for processing
with open('jp_updates_needed.json', 'w') as f:
    json.dump(jp_updates_needed, f, indent=2)

with open('l_transfer_updates_needed.json', 'w') as f:
    json.dump(l_transfer_updates_needed, f, indent=2)

print(f"Update lists saved to jp_updates_needed.json and l_transfer_updates_needed.json")
