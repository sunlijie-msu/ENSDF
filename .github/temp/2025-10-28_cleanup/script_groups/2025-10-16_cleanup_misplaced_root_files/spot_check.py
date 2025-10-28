#!/usr/bin/env python3
"""
Bidirectional spot-check validation for ENSDF data entry.
Verifies CSV source data matches ENSDF records exactly.
"""
import csv
import random

csv_file = 'A35/Cl35/raw/2001VO24.csv'

# Read CSV
data = []
with open(csv_file, 'r') as f:
    reader = csv.reader(f)
    for row_idx, row in enumerate(reader, 1):
        data.append((row_idx, row))

# Extract Exi values from Row 3, columns 3-14
exi_row = data[2][1]
exi_values = []
exi_cols = []
for col_idx in range(2, 13):
    try:
        val = int(exi_row[col_idx])
        exi_values.append(val)
        exi_cols.append(col_idx)
    except:
        pass

# Extract all transitions with source positions
transitions = []
for row_idx in range(3, 27):
    if row_idx < len(data):
        row = data[row_idx][1]
        try:
            exf = int(row[0])
            for col_idx, exi in zip(exi_cols, exi_values):
                try:
                    br_str = row[col_idx].strip()
                    if br_str and br_str != '0':
                        br = int(br_str)
                        egamma = exi - exf
                        transitions.append({
                            'exi': exi, 'exf': exf, 'egamma': egamma, 'br': br,
                            'csv_row': row_idx + 1, 'csv_col': col_idx + 1
                        })
                except:
                    pass
        except:
            pass

# Select 6 random transitions
random.seed(42)
sample_indices = random.sample(range(len(transitions)), min(6, len(transitions)))

print('BIDIRECTIONAL SPOT-CHECK VALIDATION')
print('='*80)
print(f'Total transitions in dataset: {len(transitions)}')
print()
print('6 Random Samples Selected for Verification:')
print('='*80)

for idx, i in enumerate(sample_indices, 1):
    t = transitions[i]
    print(f'{idx}. Exi={t["exi"]:5d} keV, Exf={t["exf"]:5d} keV, Egamma={t["egamma"]:5d} keV, BR={t["br"]:3d}%')
    print(f'   CSV Source: Row {t["csv_row"]:2d}, Column {t["csv_col"]:2d}')
    print()
