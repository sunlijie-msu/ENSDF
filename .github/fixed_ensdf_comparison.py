import json
import re

# Load JSON data
with open('1984CA14_final_corrected.json', 'r') as f:
    json_data = json.load(f)

# Read ENSDF file and extract only actual L-records
with open('../new/S35_ng_resonances.ens', 'r') as f:
    ensdf_lines = f.readlines()

ensdf_levels = []
for line_num, line in enumerate(ensdf_lines):
    # Only process lines that are actual L-records (start with " 35S   L ")
    if (len(line) >= 8 and 
        line[0:5].strip() == "35S" and 
        line[7] == 'L' and 
        line[5:7] == "  "):
        
        # ENSDF L-record format:
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

print(f"Found {len(ensdf_levels)} actual L-records in ENSDF file")
print(f"Found {len(json_data)} entries in JSON file")

# Show first few ENSDF entries for verification
print(f"\nFirst 10 ENSDF L-records:")
for i, level in enumerate(ensdf_levels[:10]):
    print(f"{i+1}. Line {level['line_num']}: En(lab)={level['en_lab']}, Jp='{level['jp']}', L='{level['l_transfer']}'")

# Create matching function
def normalize_energy(energy_str):
    """Normalize energy string for comparison"""
    if not energy_str:
        return ""
    # Remove parentheses and spaces, handle special cases
    clean = energy_str.replace('(', '').replace(')', '').strip()
    if clean.startswith('(') and clean.endswith(')'):
        clean = clean[1:-1]
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
        json_base = json_energy.split('(')[0] if '(' in json_energy else json_energy
        ensdf_base = ensdf_en_lab.split('(')[0] if '(' in ensdf_en_lab else ensdf_en_lab
        
        if json_base.strip() == ensdf_base.strip():
            ensdf_match = ensdf_level
            break
    
    if ensdf_match:
        match_info = {
            'json_index': i,
            'json_energy': json_energy,
            'ensdf_line_num': ensdf_match['line_num'],
            'ensdf_en_lab': ensdf_match['en_lab'],
            'json_jp': json_jp,
            'ensdf_jp': ensdf_match['jp'],
            'json_l_transfer': json_l_transfer,
            'ensdf_l_transfer': ensdf_match['l_transfer'],
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

if len(unmatched_json) > 0:
    print(f"\nFirst 10 unmatched JSON entries:")
    for i, unmatched in enumerate(unmatched_json[:10]):
        print(f"{i+1}. {unmatched['energy']}")

# Analyze what updates are needed
jp_updates_needed = []
l_transfer_updates_needed = []

for match in matches:
    # Check if Jp needs update (JSON has value, ENSDF doesn't or they differ)
    if match['json_jp'] and not match['ensdf_jp']:
        jp_updates_needed.append(match)
    elif match['json_jp'] and match['ensdf_jp'] and match['json_jp'] != match['ensdf_jp']:
        jp_updates_needed.append(match)
    
    # Check if l-transfer needs update
    if match['json_l_transfer'] and not match['ensdf_l_transfer']:
        l_transfer_updates_needed.append(match)
    elif match['json_l_transfer'] and match['ensdf_l_transfer']:
        # Convert ENSDF format to compare
        ensdf_l = match['ensdf_l_transfer']
        json_l = match['json_l_transfer']
        
        # Simple conversion check
        if not (ensdf_l in json_l or json_l in ensdf_l):
            l_transfer_updates_needed.append(match)

print(f"\n=== UPDATE REQUIREMENTS ===")
print(f"Jp updates needed: {len(jp_updates_needed)}")
print(f"L-transfer updates needed: {len(l_transfer_updates_needed)}")

# Show updates needed
if jp_updates_needed:
    print(f"\n=== Jp UPDATES NEEDED ===")
    for i, update in enumerate(jp_updates_needed):
        print(f"{i+1}. Line {update['ensdf_line_num']}: {update['json_energy']}")
        print(f"   Current ENSDF Jp: '{update['ensdf_jp']}'")
        print(f"   JSON Jp: '{update['json_jp']}'")
        print(f"   ENSDF line: {update['raw_line']}")
        print()

if l_transfer_updates_needed:
    print(f"\n=== L-TRANSFER UPDATES NEEDED ===")
    for i, update in enumerate(l_transfer_updates_needed):
        print(f"{i+1}. Line {update['ensdf_line_num']}: {update['json_energy']}")
        print(f"   Current ENSDF L: '{update['ensdf_l_transfer']}'")
        print(f"   JSON L-transfer: '{update['json_l_transfer']}'")
        print(f"   ENSDF line: {update['raw_line']}")
        print()

# Save the matches for editing
with open('matched_data.json', 'w') as f:
    json.dump(matches, f, indent=2)

print(f"Matched data saved to matched_data.json for editing")
