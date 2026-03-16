#!/usr/bin/env python
"""
Find gamma rays matching missing A2/A4 transitions
"""
import re

with open(r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens') as f:
    lines = f.readlines()

# Expected gamma energies for missing transitions
missing_transitions = {
    'Ep1072_r_0_15': {'gamma_energy': 6215.20 - 150, 'desc': 'Ep=1072, r→0.15', 'A2': (-0.24, 23), 'A4': (-0.02, 25)},
    'Ep1072_r_0_66': {'gamma_energy': 6215.20 - 660, 'desc': 'Ep=1072, r→0.66', 'A2': (-0.04, 6), 'A4': (0.00, 8)},  # Note: 1072 r→0.66 should be different from existing 1072 r→0.66 at line 1383
    'Ep1165_r_2_37': {'gamma_energy': 6308.20 - 2370, 'desc': 'Ep=1165, r→2.37', 'A2': (0.02, 3), 'A4': (-0.06, 4)},
    'Ep1266_r_0': {'gamma_energy': 6409.20, 'desc': 'Ep=1266, r→0', 'A2': (-0.21, 13), 'A4': (-0.03, 15)},
    'Ep1266_r_0_15': {'gamma_energy': 6409.20 - 150, 'desc': 'Ep=1266, r→0.15', 'A2': (0.11, 13), 'A4': (0.00, 17)},
    'Ep1266_r_0_46': {'gamma_energy': 6409.20 - 460, 'desc': 'Ep=1266, r→0.46', 'A2': (-0.11, 16), 'A4': (0.09, 21)},
    'Ep1266_r_0_66': {'gamma_energy': 6409.20 - 660, 'desc': 'Ep=1266, r→0.66', 'A2': (-0.04, 6), 'A4': (0.00, 8)},
    'Ep1266_0_66_0': {'gamma_energy': 660, 'desc': 'Ep=1266, 0.66→0', 'A2': (0.31, 5), 'A4': (-0.07, 7)},
}

print('SEARCHING FOR GAMMA RAYS MATCHING MISSING TRANSITIONS')
print('=' * 120)

for key, trans_data in missing_transitions.items():
    target_gamma = trans_data['gamma_energy']
    desc = trans_data['desc']
    a2_val, a2_unc = trans_data['A2']
    a4_val, a4_unc = trans_data['A4']
    
    print()
    print('Target: %s (gamma ≈ %.1f keV)' % (desc, target_gamma))
    print('        A2=%+.2f±%d, A4=%+.2f±%d' % (a2_val, a2_unc, a4_val, a4_unc))
    print('-' * 120)
    
    found_gamma = []
    for i, line in enumerate(lines):
        if line[7] == 'G':  # G-record
            try:
                e_str = line[9:19].strip()
                if e_str:
                    e = float(e_str)
                    # Look for matching gamma energy (±50 keV tolerance)
                    if abs(e - target_gamma) < 50:
                        found_gamma.append((i, e, line))
            except:
                pass
    
    if found_gamma:
        for line_num, energy, line_content in found_gamma:
            print('Line %d: gamma=%.2f keV' % (line_num + 1, energy))
            # Check if it already has 1969Gr29 A2/A4
            if '1969Gr29' in line_content and 'A{-' in line_content:
                print('  ⚠️  Already has 1969Gr29 A2/A4 data')
            elif 'A{-' in line_content:
                print('  → Has A2/A4 but from different source')
            else:
                print('  → READY to add A2/A4 comment')
    else:
        print('❌ No matching gamma ray found')

print()
print('=' * 120)
