"""
Apply all 35 Ep comment reformatting replacements.
Reads replacements.json created by build_replacements.py.
Outputs a Python apply script that uses the data.
Also prints exact trailing space counts for IDE tool use.
"""
import json

with open(r'd:\X\ND\ENSDF\.github\temp\replacements.json', 'r', encoding='ascii') as f:
    reps = json.load(f)

content = open(r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens', 'rb').read().decode('ascii')

print(f'=== Applying {len(reps)} replacements ===')
for i, r in enumerate(reps):
    old = r['old']
    new = r['new']
    if old not in content:
        print(f'[{i:02d}] ERROR: old string NOT FOUND')
        continue
    content = content.replace(old, new, 1)
    print(f'[{i:02d}] OK')

# Verify no double replacements
remaining_old = sum(1 for r in reps if r['old'] in content)
print(f'\nRemaining old strings in content: {remaining_old} (should be 0)')

# Write result back
with open(r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens', 'wb') as f:
    f.write(content.encode('ascii'))
print('Written to file.')
