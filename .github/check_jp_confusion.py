import json

with open('1984CA14_final_corrected.json', 'r') as f:
    data = json.load(f)

print('Checking for misplaced l-transfer values in Jp field:')
misplaced_count = 0
for entry in data:
    jp = entry.get('Jp')
    if jp and ('l =' in str(jp) or 'l=' in str(jp)):
        en = entry['En_keV']
        l_transfer = entry.get('l_transfer')
        print(f'  {en}: Jp="{jp}" | l_transfer="{l_transfer}"')
        misplaced_count += 1

print(f'\nEntries with l-transfer in Jp field: {misplaced_count}')

print('\nChecking actual Jp assignments (spin-parity):')
actual_jp_count = 0
for entry in data:
    jp = entry.get('Jp')
    if jp and ('/' in str(jp) or '+' in str(jp) or '-' in str(jp)) and 'l =' not in str(jp):
        en = entry['En_keV']
        print(f'  {en}: {jp}')
        actual_jp_count += 1
        
print(f'\nActual Jp assignments: {actual_jp_count}')
