import json

# Load the current JSON file
with open('1984CA14_final_corrected.json', 'r') as f:
    data = json.load(f)

print(f"Processing {len(data)} entries...")

# Fix the systematic confusion between Jp and l_transfer fields
for entry in data:
    jp = entry.get('Jp')
    if jp and ('l =' in str(jp) or 'l=' in str(jp)):
        # This is actually an l-transfer value, move it to the correct field
        entry['l_transfer'] = jp
        entry['Jp'] = None
        print(f"Fixed {entry['En_keV']}: moved '{jp}' from Jp to l_transfer")

# Save the corrected JSON
with open('1984CA14_final_corrected.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\nCorrection completed!")

# Verify the fix
print("\nVerification - Entries with l-transfer values:")
l_transfer_count = 0
for entry in data:
    l_transfer = entry.get('l_transfer')
    if l_transfer:
        en = entry['En_keV']
        print(f"  {en}: l_transfer = {l_transfer}")
        l_transfer_count += 1

print(f"\nTotal entries with l_transfer: {l_transfer_count}")

print("\nVerification - Entries with Jp values:")
jp_count = 0
for entry in data:
    jp = entry.get('Jp')
    if jp:
        en = entry['En_keV']
        print(f"  {en}: Jp = {jp}")
        jp_count += 1

print(f"\nTotal entries with Jp: {jp_count}")
