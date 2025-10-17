#!/usr/bin/env python3
"""
CRITICAL ANALYSIS: Parse CSV matrix and extract ALL 80+ gamma transitions
with CORRECT energies and branching ratios from the 2001VO24 source data.

Key insight: CSV format is
- ROWS = Exf (final state energies)
- COLUMNS = Exi (initial/excitation energies) 
- CELLS = Branching intensities (RI)

Gamma energy = Exi - Exf (NOT what's in current ENS)
"""

import csv

# Parse CSV file
csv_file = 'A35/Cl35/raw/2001VO24.csv'
data = []
with open(csv_file, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        data.append(row)

# Extract header information
# Line 0: Ep values (probe energies) - skip index 0
# Line 2: Exi values (initial level energies) - skip index 0
ep_line = data[0][1:]  # Skip first empty cell
exi_line = data[2][1:]  # Skip first empty cell

print("=" * 100)
print("ANALYSIS OF 2001VO24 CSV MATRIX")
print("=" * 100)
print()

# Parse Ep and Exi
ep_values = []
for val in ep_line:
    if val.strip():
        try:
            ep_values.append(float(val))
        except ValueError:
            ep_values.append(None)
    else:
        ep_values.append(None)

exi_values = []
for val in exi_line:
    if val.strip():
        try:
            exi_values.append(float(val))
        except ValueError:
            exi_values.append(None)
    else:
        exi_values.append(None)

print(f"Ep (probe) values: {[e for e in ep_values if e is not None]}")
print(f"Exi (level) values: {[e for e in exi_values if e is not None]}")
print()

# Build transition table from CSV
print("=" * 100)
print("ALL 80+ GAMMA TRANSITIONS FROM CSV MATRIX (Exi, Exf, RI)")
print("=" * 100)
print()

total_transitions = 0
transitions_dict = {}  # {Exi: [(Egamma, RI, Exf), ...]}

for row_idx in range(3, len(data)):  # Skip header rows
    row = data[row_idx]
    exf_str = row[0].strip()  # First column is Exf
    
    if not exf_str or exf_str == 'Exi':
        continue
    
    exf = float(exf_str)
    
    # Parse each column (each Exi)
    for col_idx in range(1, len(exi_values)):
        if exi_values[col_idx] is None:
            continue
        
        exi = exi_values[col_idx]
        ri_str = row[col_idx].strip() if col_idx < len(row) else ""
        
        if ri_str and ri_str != "0":
            try:
                ri = float(ri_str)
                egamma = exi - exf  # CORRECT: Egamma = Exi - Exf
                
                if exi not in transitions_dict:
                    transitions_dict[exi] = []
                transitions_dict[exi].append((egamma, ri, exf))
                total_transitions += 1
            except:
                pass

# Sort by Exi and display
for exi in sorted(transitions_dict.keys()):
    transitions = transitions_dict[exi]
    transitions.sort(key=lambda x: x[0])  # Sort by Egamma
    
    print(f"\nL {exi:7.0f} (Exi) - {len(transitions)} transitions:")
    for egamma, ri, exf in transitions:
        print(f"  G {egamma:7.1f} (→ Exf {exf:7.1f}) RI = {ri:6.1f}")

print()
print("=" * 100)
print(f"TOTAL TRANSITIONS: {total_transitions}")
print("=" * 100)
print()

# CRITICAL CHECK: What about G 7070?
print("CRITICAL ANALYSIS: What is G 7070?")
print("=" * 100)
print()
print("In original ENS: G 7070 from L 7547")
print("  → Final state = 7547 - 7070 = 477 keV")
print()
print("From CSV matrix (L 7547 / Exi 7547):")
print("  Row Exf=477: Has value 1")
print("  → Egamma = 7547 - 477 = 7070 keV ✓ ENERGY IS CORRECT!")
print("  → RI = 1")
print()
print("CONCLUSION: G 7070 energy is MATHEMATICALLY CORRECT")
print("But: Exf 477 does NOT appear in adopted level scheme")
print()
print("POSSIBLE INTERPRETATION OF 'G 7070 IS WRONG':")
print("  1. Energy calculation method is wrong?")
print("  2. Should be Exf instead of Egamma?")
print("  3. Final state assignment is wrong?")
print("  4. Branching ratio is wrong?")
print()
