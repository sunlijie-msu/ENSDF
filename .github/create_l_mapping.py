import json

# Load JSON reference data to get l-transfer values
with open('A35/S35/temp/1984CA14_final_corrected.json', 'r') as f:
    json_data = json.load(f)

# Convert to ENSDF L field format
l_transfer_map = {}
for entry in json_data:
    en = entry['En_keV'].split('(')[0]  # Remove uncertainty
    l_transfer = entry['l_transfer']
    
    if l_transfer:
        if 'l = 2' in l_transfer and 'l = 1,2' not in l_transfer:
            l_field = '2'
        elif 'l = 1,2' in l_transfer:
            l_field = '1,2'
        else:
            l_field = ''  # Unknown format, leave blank
    else:
        l_field = ''  # Blank
    
    if en:  # Skip empty energy values
        l_transfer_map[en] = l_field

print('L field values for ENSDF:')
for energy in sorted(l_transfer_map.keys(), key=lambda x: float(x) if x.replace('.','').isdigit() else 0):
    if l_transfer_map[energy]:
        print(f'{energy}: "{l_transfer_map[energy]}"')
    else:
        print(f'{energy}: (blank)')
        
# Also save to a file for reference
with open('l_transfer_mapping.txt', 'w') as f:
    for energy in sorted(l_transfer_map.keys(), key=lambda x: float(x) if x.replace('.','').isdigit() else 0):
        f.write(f'{energy}: {l_transfer_map[energy]}\n')
