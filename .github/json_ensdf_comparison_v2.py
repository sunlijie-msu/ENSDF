import json
import re

# Load the corrected JSON data
with open('A35/S35/temp/1984CA14_final_corrected.json', 'r') as f:
    json_data = json.load(f)

# Read the ENSDF file
with open('A35/S35/new/S35_ng_resonances.ens', 'r') as f:
    ensdf_lines = f.readlines()

print("🔍 SYSTEMATIC JSON vs ENSDF Jπ COMPARISON")
print("=" * 70)

# Extract L-records from ENSDF with their Jπ assignments
ensdf_levels = {}
for line_num, line in enumerate(ensdf_lines, 1):
    if len(line) >= 8 and line[7] == 'L' and line[0:5].strip() == '35S':
        # Extract fields from L-record
        jp_field = line[22:39].strip()     # Jπ field (cols 23-39)
        s_field = line[64:74].strip()      # S field (lab energy, cols 65-74)
        
        if s_field:
            # Remove question mark and clean up
            lab_energy = s_field.replace('?', '').strip()
            ensdf_levels[lab_energy] = {
                'jp': jp_field if jp_field else None,
                'line_num': line_num,
                'full_line': line.rstrip()
            }

print(f"Found {len(ensdf_levels)} ENSDF levels with lab energies")

# Show sample ENSDF entries for debugging
print("\n🔍 Sample ENSDF entries:")
for i, (en, data) in enumerate(list(ensdf_levels.items())[:10]):
    print(f"  {en}: Jπ='{data['jp'] or 'None'}' (Line {data['line_num']})")

print("\n🔍 Sample JSON entries:")
for i, entry in enumerate(json_data[:10]):
    print(f"  {entry['En_keV']}: Jπ='{entry.get('Jp') or 'None'}', l_transfer='{entry.get('l_transfer') or 'None'}'")

# Create energy matching function
def find_ensdf_match(json_en_kev, ensdf_levels):
    """Find matching ENSDF entry by energy comparison"""
    for ensdf_en, ensdf_data in ensdf_levels.items():
        # Direct match (accounting for formatting differences)
        if json_en_kev == ensdf_en:
            return ensdf_data
        
        # Compare numerical values, handling uncertainty notation
        json_num = re.sub(r'\([^)]+\)', '', json_en_kev).strip()
        ensdf_num = re.sub(r'\([^)]+\)', '', ensdf_en).strip() 
        
        # Handle decimal precision differences (e.g., 34.03 vs 34.0)
        try:
            json_val = float(json_num)
            ensdf_val = float(ensdf_num)
            # Match if within 0.01 keV (accounting for rounding differences)
            if abs(json_val - ensdf_val) < 0.01:
                return ensdf_data
        except ValueError:
            continue
    
    return None

# Compare with JSON data
discrepancies = []
matches = []
not_found = []

for json_entry in json_data:
    en_kev = json_entry['En_keV']
    json_jp = json_entry.get('Jp')
    json_lt = json_entry.get('l_transfer')
    
    # Find matching ENSDF entry
    ensdf_match = find_ensdf_match(en_kev, ensdf_levels)
    
    if ensdf_match:
        ensdf_jp = ensdf_match['jp']
        
        # Determine expected Jπ based on JSON data
        expected_jp = None
        json_type = 'blank'
        
        if json_jp and json_jp != 'None':
            expected_jp = json_jp
            json_type = 'Jp'
        elif json_lt and json_lt != 'None' and 'l =' in str(json_lt):
            # l-transfer assignments should NOT appear as Jπ in ENSDF
            expected_jp = None
            json_type = 'l_transfer'
        
        # Compare Jπ assignments
        if expected_jp and ensdf_jp:
            # Both have Jπ - should match
            if expected_jp != ensdf_jp:
                discrepancies.append({
                    'energy': en_kev,
                    'type': 'JP_MISMATCH',
                    'expected_jp': expected_jp,
                    'ensdf_jp': ensdf_jp,
                    'line_num': ensdf_match['line_num'],
                    'action': f'Change ENSDF from "{ensdf_jp}" to "{expected_jp}"',
                    'json_type': json_type,
                    'full_line': ensdf_match['full_line']
                })
            else:
                matches.append(en_kev)
        elif expected_jp and not ensdf_jp:
            # JSON has Jπ, ENSDF doesn't - should add to ENSDF
            discrepancies.append({
                'energy': en_kev,
                'type': 'ENSDF_MISSING_JP',
                'expected_jp': expected_jp,
                'ensdf_jp': 'None',
                'line_num': ensdf_match['line_num'],
                'action': f'Add "{expected_jp}" to ENSDF',
                'json_type': json_type,
                'full_line': ensdf_match['full_line']
            })
        elif not expected_jp and ensdf_jp:
            # ENSDF has Jπ, JSON doesn't
            if json_lt and json_lt != 'None' and 'l =' in str(json_lt):
                discrepancies.append({
                    'energy': en_kev,
                    'type': 'ENSDF_HAS_JP_BUT_JSON_HAS_L_TRANSFER',
                    'expected_jp': 'None',
                    'ensdf_jp': ensdf_jp,
                    'line_num': ensdf_match['line_num'],
                    'action': f'Remove "{ensdf_jp}" from ENSDF (JSON has l_transfer: {json_lt})',
                    'json_type': json_type,
                    'full_line': ensdf_match['full_line']
                })
            else:
                # This might be OK - ENSDF could have additional information
                matches.append(en_kev)
        else:
            # Both blank - OK
            matches.append(en_kev)
    else:
        not_found.append(en_kev)

print(f"\n📊 COMPARISON RESULTS:")
print(f"  Matches: {len(matches)}")
print(f"  Discrepancies: {len(discrepancies)}")
print(f"  Not found in ENSDF: {len(not_found)}")

if discrepancies:
    print(f"\n❌ DISCREPANCIES FOUND ({len(discrepancies)}):")
    for i, disc in enumerate(discrepancies, 1):
        print(f"\n{i}. Energy {disc['energy']} (Line {disc['line_num']}):")
        print(f"   Type: {disc['type']}")
        print(f"   JSON type: {disc['json_type']}")
        print(f"   Expected Jπ: {disc['expected_jp']}")
        print(f"   ENSDF Jπ: {disc['ensdf_jp']}")
        print(f"   Action: {disc['action']}")
        print(f"   Current line: {disc['full_line']}")

if not_found:
    print(f"\n⚠️  ENERGIES NOT FOUND IN ENSDF ({len(not_found)}):")
    for en in not_found[:10]:  # Show first 10
        print(f"   {en}")
    if len(not_found) > 10:
        print(f"   ... and {len(not_found) - 10} more")

print(f"\n🎯 SUMMARY:")
if discrepancies:
    print(f"  Found {len(discrepancies)} Jπ discrepancies that need correction in ENSDF")
    print("  Each edit must maintain 80-column alignment")
else:
    print("  All Jπ assignments are consistent between JSON and ENSDF!")

if len(not_found) > 70:
    print(f"  Warning: {len(not_found)} JSON energies not found - may need energy tolerance adjustment")
