"""
Analyze CSV file to extract all limit values (<X) for proper LT marker handling
"""
import csv

limits = []
with open('A35/Cl35/temp/1976ME12_Branching_Ratios.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Handle spaces in header
        ep = row.get('Ep_keV') or row.get('Ep_keV ')
        ex = row.get('Ex_keV') or row.get(' Ex_keV')
        for col, val in row.items():
            if 'Ep_keV' not in col and 'Ex_keV' not in col and val and val.strip().startswith('<'):
                limits.append((ep, ex, col.strip(), val.strip()))

print(f'Total limit values found: {len(limits)}')
print()
print('Ep_keV | Ex_keV | Final_level_MeV | RI_value')
print('-' * 60)
for ep, ex, col, val in limits:
    print(f'{ep:<7}| {ex:<7}| {col:<16}| {val}')
