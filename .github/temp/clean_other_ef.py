import re
import csv

# Parse L-record energies from 1977DA02.ens
ens_file = r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02.ens'
l_records = {}
with open(ens_file) as f:
    for line in f:
        if len(line) > 8 and line[7:8] == 'L':
            e_str = line[9:19].strip()
            try:
                e = float(e_str)
                l_records[e] = e_str
            except:
                pass

print(f"L-record energies found: {len(l_records)}")

# Create mapping from MeV to precise keV (nearest match)
def find_nearest_l_energy(mev_value):
    """Find the closest L-record energy to a MeV value"""
    kev_rough = mev_value * 1000
    closest = min(l_records.keys(), key=lambda x: abs(x - kev_rough))
    if abs(closest - kev_rough) < 50:  # Within 50 keV
        return closest
    return None

# Parse Unbound CSV and identify all unique "Other Ef" values
csv_file = r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02_Unbound_extracttable.csv'
other_ef_values = set()

with open(csv_file) as f:
    lines = f.readlines()

# Extract all MeV values from "Other Ef" column
for i, line in enumerate(lines[2:], start=3):
    parts = line.rstrip('\n').split(',')
    if len(parts) > 30 and parts[-1].strip():
        other_ef_raw = parts[-1].strip()
        # Extract all MeV values from pattern like "4.42(0.5)4.52(1)"
        matches = re.findall(r'(\d+\.\d+)\s*\(([^)]+)\)', other_ef_raw)
        for mev_str, ig_str in matches:
            mev = float(mev_str)
            other_ef_values.add(mev)

print(f"\nUnique MeV values in 'Other Ef' column: {sorted(other_ef_values)}")

# Build mapping
mev_mapping = {}
for mev in sorted(other_ef_values):
    precise_kev = find_nearest_l_energy(mev)
    mev_mapping[mev] = precise_kev
    status = "✓" if precise_kev else "✗ NO MATCH"
    print(f"  {mev:.2f} MeV ({mev*1000:.0f} keV rough) → {precise_kev} keV {status}")

# Now process the CSV and clean the "Other Ef" column
output_lines = []
for i, line in enumerate(lines):
    if i < 2:  # Keep header lines
        output_lines.append(line.rstrip('\n'))
    else:
        # Clean the row
        parts = line.rstrip('\n').split(',')
        if len(parts) > 30 and parts[-1].strip():
            other_ef_raw = parts[-1].strip()
            # Parse all (Ef_MeV(Ig)) pairs
            matches = re.findall(r'(\d+\.\d+)\s*\(([^)]+)\)', other_ef_raw)
            cleaned_pairs = []
            for mev_str, ig_str in matches:
                mev = float(mev_str)
                precise_kev = mev_mapping.get(mev)
                if precise_kev:
                    cleaned_pairs.append(f"{precise_kev:.1f}({ig_str})")
            
            if cleaned_pairs:
                parts[-1] = ', '.join(cleaned_pairs)
        
        output_lines.append(','.join(parts))

# Write cleaned CSV
output_file = csv_file
with open(output_file, 'w') as f:
    f.write('\n'.join(output_lines))

print(f"\n✓ Cleaned {output_file}")
print(f"  Total rows processed: {len(lines)-2}")

# Display sample cleaned rows
print("\nSample cleaned 'Other Ef' values:")
for i in range(2, min(10, len(output_lines))):
    parts = output_lines[i].split(',')
    if len(parts) > 30 and parts[-1].strip():
        ei = parts[1]
        other_ef = parts[-1]
        print(f"  Ei={ei}: {other_ef}")
