import re
from collections import defaultdict

fpath = r'd:\\X\\ND\\ENSDF\\XUNDL\\2026XUAA_CQ11029_125I.md'
with open(fpath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

data_rows = []

for line_num, line in enumerate(lines, 1):
    if '---' in line or 'Eγ' in line or 'Gamma' in line:
        continue
    if line.strip().startswith('|') and '---' not in line:
        parts = [p.strip() for p in line.split('|') if p.strip()]
        if len(parts) >= 7:
            try:
                eg = float(parts[0])
                ei = float(parts[1])
                jijf = parts[3]
                if '→' in jijf or '→' in jijf:
                    ji, jf = [x.strip() for x in re.split(r'→|→', jijf)]
                    data_rows.append({
                        'line': line_num,
                        'eg': eg,
                        'ei': ei,
                        'ji': ji,
                        'jf': jf,
                        'ef_exp': ei - eg
                    })
            except Exception as e:
                pass

print(f"Total parsed rows: {len(data_rows)}")

# Collect all distinct level energies
level_energies = set()
for r in data_rows:
    level_energies.add(r['ei'])

# Group levels that are within 1.5 keV of each other
groups = []
for ei in sorted(list(level_energies)):
    placed = False
    for group in groups:
        if abs(group['mean'] - ei) < 1.5:
            group['energies'].append(ei)
            group['mean'] = sum(group['energies']) / len(group['energies'])
            placed = True
            break
    if not placed:
        groups.append({
            'mean': ei,
            'energies': [ei],
            'ji_set': set(),
            'jf_set': set()
        })

energy_issues = []
jpi_issues = []

# Map data rows to groups, record Ji and Jf
for r in data_rows:
    # Initial level
    for g in groups:
        if abs(g['mean'] - r['ei']) < 1.5:
            g['ji_set'].add(r['ji'])
            break
            
    # Final level
    ef_exp = r['ef_exp']
    found = False
    best_diff = float("inf")
    for g in groups:
        diff = abs(g['mean'] - ef_exp)
        if diff < 1.5:
            g['jf_set'].add(r['jf'])
            found = True
            break
            
    if not found:
        # Just creating a new virtual group for the final level to check JPI consistency later, or flag it
        energy_issues.append(r)

# Check groups for Jpi consistency
for g in groups:
    all_jpi = set(list(g['ji_set']) + list(g['jf_set']))
    if len(all_jpi) > 1:
        jpi_issues.append((g['mean'], g['ji_set'], g['jf_set']))

print("\n--- ENERGY CONSERVATION ISSUES (>1.5 keV mismatch) ---")
if not energy_issues:
    print("None!")
else:
    for e in energy_issues:
        print(f"Line {e['line']}: E_gamma={e['eg']:.1f}, E_initial={e['ei']:.1f} -> E_final expected={e['ef_exp']:.1f}. No matching level found within 1.5 keV.")

print("\n--- LEVEL JPI CONSISTENCY ISSUES ---")
if not jpi_issues:
    print("None!")
else:
    for mean_e, ji_set, jf_set in sorted(jpi_issues):
        print(f"Level ~{mean_e:.1f} keV:")
        print(f"  Appears as initial (Ji): {ji_set}")
        print(f"  Appears as final (Jf): {jf_set}")
