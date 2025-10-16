#!/usr/bin/env python3
"""Debug L-record values in file"""

# Simple debug to check L-record values
with open('2001VO24.ens', 'r') as f:
    ens_lines = f.readlines()

print('L-records in file:')
for i, line in enumerate(ens_lines):
    if len(line) >= 19:
        type_field = line[7:8]
        if type_field == 'L':
            energy_field = line[9:19].strip()
            try:
                energy_val = float(energy_field)
                print(f'  Line {i+1}: Energy field="{energy_field}" -> {energy_val:.3f} MeV ({energy_val*1000:.0f} keV)')
            except:
                print(f'  Line {i+1}: Could not parse "{energy_field}"')
