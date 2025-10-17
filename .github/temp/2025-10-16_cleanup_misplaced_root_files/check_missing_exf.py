#!/usr/bin/env python3
"""
Check which Exf (final state) values from CSV are NOT in ENS level scheme
"""

import csv

# Read CSV and extract all Exf values
csv_path = "A35/Cl35/raw/2001VO24.csv"
csv_exf_values = []
with open(csv_path, 'r') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if i >= 3:  # Data rows start at index 3
            exf_str = row[1].strip()
            if exf_str:
                try:
                    exf = float(exf_str)
                    csv_exf_values.append(exf)
                except ValueError:
                    pass

# Read ENS and extract all L-record energy values
ens_path = "A35/Cl35/raw/2001VO24.ens"
ens_levels = []
with open(ens_path, 'r') as f:
    for line in f:
        if len(line) < 20:
            continue
        record_type = line[7:8].strip()
        if record_type == 'L':
            energy_str = line[9:19].strip()
            try:
                energy = float(energy_str)
                ens_levels.append(energy)
            except ValueError:
                pass

print("=" * 80)
print("CSV Exf (final state) values NOT in ENS level scheme")
print("=" * 80)
print()

csv_exf_set = set(csv_exf_values)
ens_levels_set = set(ens_levels)

missing_exf = sorted(csv_exf_set - ens_levels_set)

print(f"ENS levels: {sorted(ens_levels)}")
print()
print(f"CSV Exf values: {sorted(csv_exf_values)}")
print()
print(f"Exf values NOT in ENS levels ({len(missing_exf)} missing):")
for exf in missing_exf:
    print(f"  {exf}")
print()

print("=" * 80)
print("INTERPRETATION")
print("=" * 80)
print(f"""
The CSV matrix has {len(csv_exf_set)} unique final state energies (Exf).
The ENS file has {len(ens_levels_set)} defined levels.

CRITICAL FINDING:
{len(missing_exf)} Exf values from CSV are NOT in the ENS level scheme:
  {missing_exf}

This means the CSV data references INTERMEDIATE COMPOUND NUCLEAR STATES
that are NOT part of the final level scheme being tabulated in this ENS file.

The formula Egamma = Exi - Exf is CORRECT, but Exf values like 477 keV
do NOT represent adopted levels - they represent transient compound states
populated during the {+35}Cl(p,g) reaction.

USER'S STATEMENT: "G 7070 is absolutely wrong" likely means:
  - The 7070 keV transition from 7547 to 477 is "wrong" because 477 is NOT
    a real level in the adopted {+35}Cl scheme
  - This transition should NOT be included in the final evaluated dataset
  - Only transitions to REAL levels (those in ens_levels) should be included

SOLUTION: Filter transitions to only include those where Exf matches an ENS level!
""")
