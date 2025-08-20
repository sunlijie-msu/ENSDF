import json

# Load both files
with open('1984CA14_systematic_extraction.json', 'r') as f:
    systematic_data = json.load(f)

with open('1984CA14_final_corrected.json', 'r') as f:
    final_data = json.load(f)

print('=== FILE COMPARISON ===')
print(f'1984CA14_systematic_extraction.json:')
print(f'  Type: {type(systematic_data)}')
if isinstance(systematic_data, dict):
    print(f'  Keys: {list(systematic_data.keys())}')
    if 'resonances' in systematic_data:
        print(f'  Resonances count: {len(systematic_data["resonances"])}')
elif isinstance(systematic_data, list):
    print(f'  Array length: {len(systematic_data)}')

print(f'\n1984CA14_final_corrected.json:')
print(f'  Type: {type(final_data)}')
print(f'  Array length: {len(final_data)}')

# Check if systematic_data has the same structure as final_data
if isinstance(systematic_data, dict) and 'resonances' in systematic_data:
    print('\n=== STRUCTURE ANALYSIS ===')
    print('systematic_extraction.json contains resonance data with different structure')
    print('final_corrected.json contains tabular energy data')
    print('\nThese appear to be different data sets!')
    
    # Show a sample resonance entry
    print('\nSample from systematic_extraction (resonance format):')
    if len(systematic_data['resonances']) > 0:
        sample = systematic_data['resonances'][0]
        for key, value in sample.items():
            print(f'  {key}: {value}')
    
    print('\nSample from final_corrected (table format):')
    if len(final_data) > 0:
        sample = final_data[0]
        for key, value in sample.items():
            print(f'  {key}: {value}')
    
elif isinstance(systematic_data, list):
    print('\n=== DIRECT COMPARISON ===')
    print('Both files are arrays - comparing content...')
    
    # Compare lengths
    if len(systematic_data) != len(final_data):
        print(f'Length mismatch: systematic={len(systematic_data)}, final={len(final_data)}')
    else:
        print(f'Both have {len(final_data)} entries')
        
        # Compare key fields for first few entries
        mismatches = []
        for i in range(min(5, len(final_data))):
            sys_entry = systematic_data[i] if i < len(systematic_data) else None
            fin_entry = final_data[i]
            
            if sys_entry:
                # Compare key fields
                sys_en = sys_entry.get('En_keV')
                fin_en = fin_entry.get('En_keV')
                sys_jp = sys_entry.get('Jp')
                fin_jp = fin_entry.get('Jp')
                
                if sys_en != fin_en or sys_jp != fin_jp:
                    mismatches.append(f'Entry {i}: systematic=({sys_en}, {sys_jp}), final=({fin_en}, {fin_jp})')
        
        if mismatches:
            print('Differences found:')
            for mismatch in mismatches:
                print(f'  {mismatch}')
        else:
            print('First 5 entries match perfectly')

print('\n=== RECOMMENDATION ===')
if isinstance(systematic_data, dict) and 'resonances' in systematic_data:
    print('The systematic_extraction.json contains resonance data (different format)')
    print('The final_corrected.json contains the PNG table data we need')
    print('RECOMMENDATION: Use 1984CA14_final_corrected.json as the final version')
elif isinstance(systematic_data, list) and len(systematic_data) == len(final_data):
    print('Both files are table format - need detailed comparison')
else:
    print('Files have different structures - manual review needed')
