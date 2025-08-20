import json

# Load the matched data
with open('matched_data.json', 'r') as f:
    matches = json.load(f)

# Read the current ENSDF file
with open('../new/S35_ng_resonances.ens', 'r') as f:
    ensdf_lines = f.readlines()

print("Starting systematic ENSDF updates...")

# Track all updates needed
jp_updates = []
l_transfer_updates = []

for match in matches:
    line_num = match['ensdf_line_num'] - 1  # Convert to 0-based indexing
    json_jp = match['json_jp']
    ensdf_jp = match['ensdf_jp']
    json_l = match['json_l_transfer']
    ensdf_l = match['ensdf_l_transfer']
    energy = match['json_energy']
    
    # Check if Jp update is needed
    if json_jp and ensdf_jp != json_jp:
        # Extract parity and other info from JSON
        if json_jp.endswith('- (A)') or json_jp.endswith('- (B)') or json_jp.endswith('- (C)'):
            new_jp = json_jp.split(' ')[0]  # Get just the "3/2-" part
        elif json_jp.endswith('+ (A)') or json_jp.endswith('+ (B)') or json_jp.endswith('+ (C)'):
            new_jp = json_jp.split(' ')[0]  # Get just the "1/2+" part
        elif json_jp.startswith('(') and json_jp.endswith(') (B)'):
            new_jp = json_jp.split(' ')[0]  # Get just the "(1/2-)" part
        else:
            new_jp = json_jp
            
        jp_updates.append({
            'line_num': line_num,
            'energy': energy,
            'current_jp': ensdf_jp,
            'new_jp': new_jp,
            'original_line': ensdf_lines[line_num].rstrip()
        })
    
    # Check if Jp needs to be added (ENSDF has None, JSON has value)
    elif json_jp and not ensdf_jp:
        if json_jp.endswith('- (B)'):
            new_jp = json_jp.split(' ')[0]  # Get just the "1/2-" part
        else:
            new_jp = json_jp.split(' ')[0] if ' ' in json_jp else json_jp
            
        jp_updates.append({
            'line_num': line_num,
            'energy': energy,
            'current_jp': '',
            'new_jp': new_jp,
            'original_line': ensdf_lines[line_num].rstrip()
        })

print(f"Found {len(jp_updates)} Jp updates to make")

# Show the updates that will be made
print("\n=== Jp UPDATES TO BE MADE ===")
for i, update in enumerate(jp_updates):
    print(f"{i+1}. Line {update['line_num']+1}: {update['energy']}")
    print(f"   '{update['current_jp']}' -> '{update['new_jp']}'")
    print(f"   {update['original_line']}")
    
    # Check if this is reasonable
    if len(update['new_jp']) > 10:
        print(f"   ⚠️  WARNING: New Jp seems too long: '{update['new_jp']}'")
    print()

# Save the update plan
with open('jp_update_plan.json', 'w') as f:
    json.dump(jp_updates, f, indent=2)

print(f"Update plan saved to jp_update_plan.json")
print(f"Ready to proceed with {len(jp_updates)} updates")
