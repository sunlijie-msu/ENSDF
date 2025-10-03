"""
Update L-record energies in 1972HU10.ens using Exi_revised values from CSV.
Directly replace Exi_original with Exi_revised without recalculating Sp.
"""

import re

# Read CSV and create mapping
exi_mapping = {}  # Maps Exi_original -> Exi_revised
ep_mapping = {}   # Maps Exi_original -> Ep_keV for verification

with open('A35/Cl35/temp/1972HU10_Branching_Ratios.csv', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Skip first 3 header lines
for line in lines[3:]:
    parts = line.strip().split(',')
    if len(parts) >= 3 and parts[0] and parts[1] and parts[2]:
        try:
            exi_rev = int(parts[0])
            ep = int(parts[1])
            exi_orig = int(parts[2])
            exi_mapping[exi_orig] = exi_rev
            ep_mapping[exi_orig] = ep
        except ValueError:
            continue

print(f"[INFO] Total mappings from CSV: {len(exi_mapping)}")
print(f"\n[INFO] Sample mappings (Exi_original -> Exi_revised):")
for i, (orig, rev) in enumerate(sorted(exi_mapping.items())[:10]):
    diff = rev - orig
    ep = ep_mapping[orig]
    print(f"  {orig:4} -> {rev:4} (diff={diff:+2} keV) [Ep={ep} keV]")

# Read the ENSDF file
with open('A35/Cl35/temp/1972HU10.ens', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Process L-records with S field (resonances from 1972Hu10)
updated_count = 0
not_found = []
output_lines = []

for i, line in enumerate(lines):
    # Check if this is an L-record with S field data
    if line[7:8] == 'L' and len(line) >= 75 and line[64:74].strip():
        # Extract current energy
        energy_str = line[9:19].strip()
        try:
            energy_float = float(energy_str)
            energy_int = int(round(energy_float))
            
            # Check if we have a mapping for this energy
            if energy_int in exi_mapping:
                exi_revised = exi_mapping[energy_int]
                ep_check = ep_mapping[energy_int]
                
                # Format the new energy (preserve decimal if original had it)
                if '.' in energy_str:
                    new_energy_str = f"{exi_revised}.0"
                else:
                    new_energy_str = str(exi_revised)
                
                # Replace energy in the line (columns 10-19, left-justified)
                new_line = line[:9] + f"{new_energy_str:<10}" + line[19:]
                output_lines.append(new_line)
                
                print(f"[UPDATE] Line {i+1}: {energy_int} -> {exi_revised} (Ep={ep_check})")
                updated_count += 1
            else:
                # Energy not in mapping - keep as is
                output_lines.append(line)
                not_found.append((i+1, energy_int))
        except ValueError:
            output_lines.append(line)
    else:
        output_lines.append(line)

# Write updated file
with open('A35/Cl35/temp/1972HU10_updated_exi.ens', 'w', encoding='utf-8') as f:
    f.writelines(output_lines)

print(f"\n[SUMMARY] Updated {updated_count} L-record energies")
print(f"[SUMMARY] Output file: A35/Cl35/temp/1972HU10_updated_exi.ens")

if not_found:
    print(f"\n[WARNING] {len(not_found)} L-records with Ep data not found in CSV mapping:")
    for line_num, energy in not_found[:10]:
        print(f"  Line {line_num}: Energy {energy} keV")
    if len(not_found) > 10:
        print(f"  ... and {len(not_found) - 10} more")
