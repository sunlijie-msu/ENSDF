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
    if len(line) >= 8 and line[7] == 'L' and line[0:5].strip():
        # Extract energy and Jπ from L-record
        energy_field = line[9:19].strip()  # Energy field (cols 10-19)
        jp_field = line[22:39].strip()     # Jπ field (cols 23-39)
        
        # Parse energy - get the laboratory energy from S field
        if line[64:74].strip():  # S field has lab energy
            lab_energy = line[64:74].strip()
            ensdf_levels[lab_energy] = {
                'jp': jp_field if jp_field else None,
                'line_num': line_num,
                'full_line': line.rstrip()
            }

print(f"Found {len(ensdf_levels)} ENSDF levels with lab energies")

# Compare with JSON data
discrepancies = []
matches = []

for json_entry in json_data:
    en_kev = json_entry['En_keV']
    json_jp = json_entry.get('Jp')
    json_lt = json_entry.get('l_transfer')
    
    # Handle parentheses in energy values
    en_clean = en_kev.replace('(', '').replace(')', '').strip()
    
    # Find matching ENSDF entry
    ensdf_match = None
    for ensdf_en, ensdf_data in ensdf_levels.items():
        if ensdf_en == en_kev or ensdf_en.replace('(', '').replace(')', '').strip() == en_clean:
            ensdf_match = ensdf_data
            break
    
    if ensdf_match:
        ensdf_jp = ensdf_match['jp']
        
        # Compare Jπ assignments
        if json_jp and ensdf_jp:
            # Both have Jπ - should match
            if json_jp != ensdf_jp:
                discrepancies.append({
                    'energy': en_kev,
                    'type': 'JP_MISMATCH',
                    'json_jp': json_jp,
                    'ensdf_jp': ensdf_jp,
                    'line_num': ensdf_match['line_num'],
                    'action': f'Change ENSDF from "{ensdf_jp}" to "{json_jp}"'
                })
            else:
                matches.append(en_kev)
        elif json_jp and not ensdf_jp:
            # JSON has Jπ, ENSDF doesn't - should add to ENSDF
            discrepancies.append({
                'energy': en_kev,
                'type': 'ENSDF_MISSING_JP',
                'json_jp': json_jp,
                'ensdf_jp': None,
                'line_num': ensdf_match['line_num'],
                'action': f'Add "{json_jp}" to ENSDF'
            })
        elif not json_jp and ensdf_jp:
            # ENSDF has Jπ, JSON doesn't - should remove from ENSDF
            discrepancies.append({
                'energy': en_kev,
                'type': 'ENSDF_EXTRA_JP',
                'json_jp': None,
                'ensdf_jp': ensdf_jp,
                'line_num': ensdf_match['line_num'],
                'action': f'Remove "{ensdf_jp}" from ENSDF'
            })
        else:
            # Both blank - OK
            matches.append(en_kev)
    else:
        print(f"⚠️  JSON energy {en_kev} not found in ENSDF")

print(f"\n📊 COMPARISON RESULTS:")
print(f"  Matches: {len(matches)}")
print(f"  Discrepancies: {len(discrepancies)}")

if discrepancies:
    print(f"\n❌ DISCREPANCIES FOUND ({len(discrepancies)}):")
    for i, disc in enumerate(discrepancies, 1):
        print(f"\n{i}. Energy {disc['energy']} (Line {disc['line_num']}):")
        print(f"   Type: {disc['type']}")
        print(f"   JSON Jπ: {disc['json_jp']}")
        print(f"   ENSDF Jπ: {disc['ensdf_jp']}")
        print(f"   Action: {disc['action']}")
else:
    print("\n✅ NO DISCREPANCIES - All Jπ assignments match!")

# Show some matches for verification
if matches:
    print(f"\n✅ SAMPLE MATCHES:")
    for en in matches[:10]:  # Show first 10 matches
        json_entry = next(e for e in json_data if e['En_keV'] == en)
        json_jp = json_entry.get('Jp')
        if json_jp:  # Only show non-null matches
            print(f"   {en}: {json_jp}")

# Create edit plan
if discrepancies:
    print(f"\n📝 EDIT PLAN:")
    print("The following ENSDF lines need to be updated:")
    for disc in discrepancies:
        print(f"  Line {disc['line_num']}: {disc['action']}")

print(f"\n🎯 NEXT STEPS:")
if discrepancies:
    print("  1. Apply the discrepancy corrections to ENSDF")
    print("  2. Ensure 80-column alignment after each edit")
    print("  3. Re-run validation tools")
else:
    print("  All Jπ assignments are consistent between JSON and ENSDF!")
