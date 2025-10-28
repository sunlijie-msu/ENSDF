#!/usr/bin/env python3
"""
Verify ALL gamma energies in 2001VO24.ens
Calculate Efinal = Elevel - Egamma and verify against level scheme
"""

levels_info = []
current_level = None
lower_levels = set()

with open('A35/Cl35/raw/2001VO24.ens', 'r') as f:
    for line in f:
        # Check if L-record (column 7 = 'L')
        if len(line) >= 19 and line[7:8] == 'L':
            energy_str = line[9:19].strip()
            if energy_str:
                try:
                    energy = float(energy_str)
                    current_level = energy
                    lower_levels.add(energy)
                    levels_info.append({'level': energy, 'gammas': []})
                except:
                    pass
        # Check if G-record (column 7 = 'G')
        elif len(line) >= 29 and line[7:8] == 'G' and current_level is not None:
            egamma_str = line[9:19].strip()
            ri_str = line[22:29].strip()
            if egamma_str:
                try:
                    egamma = float(egamma_str)
                    ri = float(ri_str) if ri_str else 0
                    levels_info[-1]['gammas'].append({'egamma': egamma, 'ri': ri})
                except:
                    pass

print('VERIFICATION OF ALL GAMMA ENERGIES IN 2001VO24.ens')
print('=' * 90)
print(f'Lower Levels Available: {sorted(lower_levels)}\n')

# Track errors
errors = []

for item in levels_info:
    level = item['level']
    gammas = item['gammas']
    print(f'L {level:7.0f}')
    
    for g in gammas:
        egamma = g['egamma']
        ri = g['ri']
        efinal = level - egamma
        exists = efinal in lower_levels
        status = '✓' if exists else '✗ ERROR'
        
        if not exists:
            errors.append(f"L {level:.0f}: G {egamma:.0f} → E_final={efinal:.1f} NOT IN LEVEL SCHEME")
        
        print(f'  G {egamma:7.0f} RI={ri:3.0f}  →  E_final = {efinal:7.1f}  {status}')

print('\n' + '=' * 90)
if errors:
    print(f'\nERRORS FOUND ({len(errors)}):')
    for error in errors:
        print(f'  {error}')
else:
    print('NO ERRORS FOUND')
