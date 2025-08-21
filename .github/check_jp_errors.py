# Check specific ENSDF entries against JSON reference
import json

# Expected values from JSON (without classification codes)
expected = {
    '118.30': '3/2-',
    '298.70': '1/2+', 
    '317.51': '3/2-',
    '355.41': '1/2+',
    '396.14': '1/2-',
    '435.4': '3/2-',
    '469.85': '1/2+',
    '510.02': '1/2-',
    '641.93': '3/2-',
    '798.65': '3/2-',
    '813.8': '1/2-',
    '836.27': '1/2+',
    '850.94': '3/2+',
    '893.17': '3/2-',
    '935.78': '3/2-',
    '997.9': '3/2-',
    '1017.7': '3/2-',
    '1140.0': '1/2-',
    '1237.0': '1/2-',
    '1275.1': '1/2-',
    '1308.2': '3/2-',
    '1314.5': '5/2+',
    '1325.7': '(1/2-)',
    '1388.0': '3/2-',
    '1447.2': '3/2-'
}

# Read ENSDF file
with open('A35/S35/new/S35_ng_resonances.ens', 'r') as f:
    lines = f.readlines()

print('Checking ENSDF vs Expected Jp assignments:')
errors = []
corrects = []

for energy, expected_jp in expected.items():
    found = False
    for i, line in enumerate(lines):
        if line.startswith(' 35S   L ') and energy in line:
            # Extract Jp field (columns 23-39, 0-indexed: 22-38)
            current_jp = line[22:39].strip()
            if current_jp != expected_jp:
                errors.append(f'Energy {energy}: ENSDF has "{current_jp}", should be "{expected_jp}"')
                print(f'❌ {energy}: "{current_jp}" → should be "{expected_jp}"')
            else:
                corrects.append(energy)
                print(f'✅ {energy}: "{current_jp}" (correct)')
            found = True
            break
    if not found:
        print(f'⚠️  {energy}: not found in ENSDF')

print(f'\n=== SUMMARY ===')
print(f'Total entries checked: {len(expected)}')
print(f'Correct: {len(corrects)}')
print(f'Errors found: {len(errors)}')
print(f'\nERROR LIST:')
for error in errors:
    print(error)
