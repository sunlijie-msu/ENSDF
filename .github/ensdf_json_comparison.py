import json
import re

# Load JSON data
with open('1984CA14_final_corrected.json', 'r') as f:
    json_data = json.load(f)

# Read ENSDF file
with open('../new/S35_ng_resonances.ens', 'r') as f:
    ensdf_lines = f.readlines()

# Extract L-record data from ENSDF file
ensdf_levels = []
for line in ensdf_lines:
    if len(line) >= 8 and line[7] == 'L':
        # Extract energy from cols 10-19
        energy_str = line[9:19].strip()
        # Extract J-pi from cols 23-39  
        jp_str = line[22:39].strip() if len(line) > 39 else ""
        # Extract L-transfer from cols 56-64
        l_transfer_str = line[55:65].strip() if len(line) > 65 else ""
        # Extract En(lab) from cols 65-74 (S field in ENSDF)
        en_lab_str = line[64:74].strip() if len(line) > 74 else ""
        
        ensdf_levels.append({
            'raw_line': line.rstrip(),
            'energy': energy_str,
            'jp': jp_str if jp_str else None,
            'l_transfer': l_transfer_str if l_transfer_str else None,
            'en_lab': en_lab_str
        })

print(f"Found {len(ensdf_levels)} L-records in ENSDF file")
print(f"Found {len(json_data)} entries in JSON file")

# Compare and find matches
matches = []
discrepancies = []

for i, json_entry in enumerate(json_data):
    json_energy = json_entry['En_keV']
    json_jp = json_entry.get('Jp')
    json_l_transfer = json_entry.get('l_transfer')
    
    # Find corresponding ENSDF level by En(lab) match
    ensdf_match = None
    for ensdf_level in ensdf_levels:
        # Try to match with En(lab) field
        ensdf_en_lab = ensdf_level['en_lab']
        
        # Clean up energy strings for comparison
        json_en_clean = json_energy.replace('(', '').replace(')', '').strip()
        if json_en_clean.startswith('(') and json_en_clean.endswith(')'):
            json_en_clean = json_en_clean[1:-1]
        
        ensdf_en_clean = ensdf_en_lab.replace('(', '').replace(')', '').strip()
        
        # Try exact match first
        if json_en_clean == ensdf_en_clean:
            ensdf_match = ensdf_level
            break
        
        # Try approximate match for entries like "34.03" vs "34.03(1)"
        json_base = json_en_clean.split('(')[0] if '(' in json_en_clean else json_en_clean
        ensdf_base = ensdf_en_clean.split('(')[0] if '(' in ensdf_en_clean else ensdf_en_clean
        
        if json_base == ensdf_base:
            ensdf_match = ensdf_level
            break
    
    if ensdf_match:
        # Compare Jp assignments
        ensdf_jp = ensdf_match['jp']
        jp_match = (json_jp == ensdf_jp)
        
        # Compare l-transfer assignments
        ensdf_l = ensdf_match['l_transfer'] 
        # Convert ENSDF format [2] to JSON format l = 2
        if ensdf_l and ensdf_l.startswith('[') and ensdf_l.endswith(']'):
            ensdf_l_converted = f"l = {ensdf_l[1:-1]}"
        else:
            ensdf_l_converted = ensdf_l
            
        l_transfer_match = (json_l_transfer == ensdf_l_converted)
        
        match_info = {
            'json_index': i,
            'json_energy': json_energy,
            'ensdf_energy': ensdf_match['energy'],
            'ensdf_en_lab': ensdf_match['en_lab'],
            'json_jp': json_jp,
            'ensdf_jp': ensdf_jp,
            'jp_match': jp_match,
            'json_l_transfer': json_l_transfer,
            'ensdf_l_transfer': ensdf_l,
            'ensdf_l_converted': ensdf_l_converted,
            'l_transfer_match': l_transfer_match,
            'ensdf_line': ensdf_match['raw_line']
        }
        
        matches.append(match_info)
        
        # Track discrepancies
        if not jp_match or not l_transfer_match:
            discrepancies.append(match_info)
    else:
        print(f"No ENSDF match found for JSON entry: {json_energy}")

print(f"\nMatched {len(matches)} entries")
print(f"Found {len(discrepancies)} discrepancies")

# Show discrepancies
print("\n=== DISCREPANCIES FOUND ===")
for disc in discrepancies:
    en = disc['json_energy']
    print(f"\nEnergy: {en} (ENSDF En(lab): {disc['ensdf_en_lab']})")
    
    if not disc['jp_match']:
        print(f"  Jp MISMATCH: JSON='{disc['json_jp']}' vs ENSDF='{disc['ensdf_jp']}'")
    
    if not disc['l_transfer_match']:
        print(f"  L-transfer MISMATCH: JSON='{disc['json_l_transfer']}' vs ENSDF='{disc['ensdf_l_transfer']}'")
    
    print(f"  ENSDF line: {disc['ensdf_line']}")

# Summary statistics
jp_discrepancies = sum(1 for d in discrepancies if not d['jp_match'])
l_transfer_discrepancies = sum(1 for d in discrepancies if not d['l_transfer_match'])

print(f"\n=== SUMMARY ===")
print(f"Total matches: {len(matches)}")
print(f"Jp discrepancies: {jp_discrepancies}")
print(f"L-transfer discrepancies: {l_transfer_discrepancies}")
print(f"Total discrepancies: {len(discrepancies)}")

# Count missing assignments
json_jp_count = sum(1 for entry in json_data if entry.get('Jp'))
json_l_count = sum(1 for entry in json_data if entry.get('l_transfer'))
ensdf_jp_count = sum(1 for match in matches if match['ensdf_jp'])
ensdf_l_count = sum(1 for match in matches if match['ensdf_l_transfer'])

print(f"\nJSON data has {json_jp_count} Jp assignments and {json_l_count} l-transfer assignments")
print(f"ENSDF data has {ensdf_jp_count} Jp assignments and {ensdf_l_count} l-transfer assignments")

# Save detailed comparison for review
with open('ensdf_json_comparison.txt', 'w') as f:
    f.write("ENSDF vs JSON Comparison\n")
    f.write("=" * 50 + "\n\n")
    
    for match in matches:
        f.write(f"Energy: {match['json_energy']} (ENSDF: {match['ensdf_en_lab']})\n")
        f.write(f"  JSON Jp: {match['json_jp']}\n")
        f.write(f"  ENSDF Jp: {match['ensdf_jp']}\n")
        f.write(f"  JSON l-transfer: {match['json_l_transfer']}\n")
        f.write(f"  ENSDF l-transfer: {match['ensdf_l_transfer']}\n")
        f.write(f"  Jp match: {match['jp_match']}\n")
        f.write(f"  L-transfer match: {match['l_transfer_match']}\n")
        f.write(f"  ENSDF line: {match['ensdf_line']}\n")
        f.write("-" * 40 + "\n")

print("\nDetailed comparison saved to 'ensdf_json_comparison.txt'")
