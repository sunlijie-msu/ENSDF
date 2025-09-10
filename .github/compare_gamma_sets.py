import json

# Read 2025LAAA gamma energies
with open('XUNDL/2025LAAA_CH11036_127I_gamma_energies.json', 'r') as f:
    data = json.load(f)

laaa_gammas = set()
for gamma in data['gamma_transitions']:
    energy = gamma['energy']['value']
    laaa_gammas.add(energy)

print(f"2025LAAA contains {len(laaa_gammas)} gamma energies")

# Read ENSDF gamma records
ensdf_gammas = []
with open('XUNDL/2025LAAA_CH11036_127I.ens', 'r') as f:
    lines = f.readlines()

for line in lines:
    if line.startswith('127I   G'):
        energy_str = line[9:19].strip()
        if energy_str:
            try:
                energy = float(energy_str)
                ensdf_gammas.append(energy)
            except ValueError:
                continue

print(f"ENSDF file contains {len(ensdf_gammas)} gamma records")
print()

# Find gammas in ENSDF but not in 2025LAAA
extra_gammas = []
for gamma in ensdf_gammas:
    # Check if this gamma matches any 2025LAAA gamma (within 0.1 keV)
    found = False
    for laaa_gamma in laaa_gammas:
        if abs(gamma - laaa_gamma) < 0.1:
            found = True
            break
    if not found:
        extra_gammas.append(gamma)

if extra_gammas:
    print(f"EXTRA GAMMAS (should be removed): {len(extra_gammas)}")
    for i, gamma in enumerate(sorted(extra_gammas), 1):
        print(f"{i:2d}. {gamma:6.1f} keV")
else:
    print("No extra gammas found - all gammas match 2025LAAA dataset")

# Find 2025LAAA gammas missing from ENSDF
missing_gammas = []
for laaa_gamma in laaa_gammas:
    found = False
    for ensdf_gamma in ensdf_gammas:
        if abs(ensdf_gamma - laaa_gamma) < 0.1:
            found = True
            break
    if not found:
        missing_gammas.append(laaa_gamma)

if missing_gammas:
    print(f"\nMISSING GAMMAS (should be added): {len(missing_gammas)}")
    for i, gamma in enumerate(sorted(missing_gammas), 1):
        print(f"{i:2d}. {gamma:6.1f} keV")
else:
    print("\nNo missing gammas - all 2025LAAA gammas are present")
