import json

with open('1984CA14_final_corrected.json', 'r') as f:
    data = json.load(f)

# Check the specific problematic entries
problem_entries = ['463.9(4)', '490.5(6)', '510.02(4)']

print('Current JSON data for problematic entries:')
for entry in data:
    if entry['En_keV'] in problem_entries:
        en = entry['En_keV']
        jp = entry.get('Jp')
        lt = entry.get('l_transfer')
        print(f'  {en}: Jp="{jp}", l_transfer="{lt}"')

print()
print('According to user corrections, should be:')
print('  463.9(4): Jp=null, l_transfer="l = 1,2 (D)"')
print('  490.5(6): Jp=null, l_transfer=null')  
print('  510.02(4): Jp="1/2- (B)", l_transfer=null')

print()
print('CRITICAL ERRORS DETECTED:')
print('The JSON extraction has systematic errors and mismatched data!')
print('Task must be stopped and JSON re-extracted carefully from PNG images!')
