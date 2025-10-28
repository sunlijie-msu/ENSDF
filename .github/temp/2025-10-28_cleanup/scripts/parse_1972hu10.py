import re
from pathlib import Path

# Read 1972Hu10.ens
with open('d:/X/ND/ENSDF/A35/Cl35/raw/1972HU10.ens', 'r') as f:
    hu10_lines = f.readlines()

# Read Cl35_34s_p_g.ens
with open('d:/X/ND/ENSDF/A35/Cl35/new/Cl35_34s_p_g.ens', 'r') as f:
    cl35_lines = f.readlines()

# Find starting point in 1972Hu10.ens (L 7066.4)
start_idx = None
for i, line in enumerate(hu10_lines):
    if 'L 7066.4' in line and '716.0' in line:
        start_idx = i
        break

if start_idx is None:
    print('ERROR: Could not find L 7066.4 in 1972Hu10.ens')
    exit(1)

print(f'Found L 7066.4 at line {start_idx + 1} in 1972Hu10.ens')

# Parse levels and gammas from 1972Hu10.ens starting from L 7066.4
levels_data = []
current_level = None

for i in range(start_idx, len(hu10_lines)):
    line = hu10_lines[i]
    
    # Check if it's an L-record
    if len(line) > 8 and line[7] == 'L' and line[5:7] == '  ':
        if current_level is not None:
            levels_data.append(current_level)
        
        # Extract level energy
        energy_str = line[9:19].strip()
        try:
            energy = float(energy_str)
        except:
            energy = energy_str
        
        current_level = {
            'energy': energy,
            'energy_str': energy_str,
            'line_num': i + 1,
            'gammas': []
        }
    
    # Check if it's a G-record
    elif len(line) > 8 and line[7] == 'G' and line[5:7] == '  ' and current_level is not None:
        # Extract gamma energy and RI
        gamma_energy_str = line[9:19].strip()
        ri_str = line[21:29].strip()
        dri_str = line[29:31].strip()
        
        if ri_str:  # Only if RI is present
            current_level['gammas'].append({
                'energy': gamma_energy_str,
                'ri': ri_str,
                'dri': dri_str,
                'line_num': i + 1
            })

# Add last level
if current_level is not None:
    levels_data.append(current_level)

total_gammas = sum(len(level['gammas']) for level in levels_data)
print(f'\nParsed {len(levels_data)} levels from 1972Hu10.ens')
print(f'Total gammas with RI values: {total_gammas}')

# Save to temp file for inspection
Path('.github/temp').mkdir(parents=True, exist_ok=True)
with open('.github/temp/1972hu10_parsed_data.txt', 'w') as f:
    f.write(f'Parsed {len(levels_data)} levels from 1972Hu10.ens\n')
    f.write(f'Total gammas: {total_gammas}\n\n')
    
    for level in levels_data:
        f.write(f'L {level["energy_str"]} (line {level["line_num"]}) - {len(level["gammas"])} gammas\n')
        for gamma in level['gammas']:
            f.write(f'  G {gamma["energy"]:10s}  RI={gamma["ri"]:7s}  DRI={gamma["dri"]:3s} (line {gamma["line_num"]})\n')
        f.write('\n')

print(f'\nSaved parsed data to .github/temp/1972hu10_parsed_data.txt')

# Now verify each RI in Cl35_34s_p_g.ens
print('\n' + '='*80)
print('VERIFICATION PHASE: Checking each RI in Cl35_34s_p_g.ens')
print('='*80)

discrepancies = []

for level in levels_data:
    level_energy = level['energy_str']
    
    # Search for this level in Cl35_34s_p_g.ens
    # Need to handle slight energy differences (7066.4 vs 7066.2)
    level_found = False
    cl35_level_line = None
    
    # Try exact match first
    for i, line in enumerate(cl35_lines):
        if f'L {level_energy}' in line and line[7] == 'L':
            level_found = True
            cl35_level_line = i
            break
    
    # If not found, try with small tolerance
    if not level_found:
        try:
            target_energy = float(level_energy)
            for i, line in enumerate(cl35_lines):
                if len(line) > 19 and line[7] == 'L' and line[5:7] == '  ':
                    try:
                        cl35_energy = float(line[9:19].strip())
                        if abs(cl35_energy - target_energy) < 0.5:  # 0.5 keV tolerance
                            level_found = True
                            cl35_level_line = i
                            cl35_level_energy_str = line[9:19].strip()
                            print(f'\nLevel match with energy difference: 1972Hu10 L {level_energy} -> Cl35 L {cl35_level_energy_str}')
                            break
                    except:
                        pass
        except:
            pass
    
    if not level_found:
        discrepancies.append({
            'type': 'MISSING_LEVEL',
            'level': level_energy,
            'message': f'Level L {level_energy} from 1972Hu10 NOT FOUND in Cl35_34s_p_g.ens'
        })
        print(f'\n❌ Level L {level_energy} NOT FOUND in Cl35_34s_p_g.ens')
        continue
    
    # Now check each gamma for this level
    print(f'\n✓ Checking level L {level_energy} ({len(level["gammas"])} gammas)')
    
    for gamma in level['gammas']:
        gamma_energy = gamma['energy']
        ri_1972 = gamma['ri']
        dri_1972 = gamma['dri']
        
        # Search for this gamma in Cl35_34s_p_g.ens near this level
        # Look in next 100 lines after the level
        gamma_found = False
        ri_in_comment = False
        
        for i in range(cl35_level_line, min(cl35_level_line + 100, len(cl35_lines))):
            line = cl35_lines[i]
            
            # Stop if we hit next level
            if i > cl35_level_line and len(line) > 8 and line[7] == 'L' and line[5:7] == '  ':
                break
            
            # Check if this is a gamma with matching energy
            if len(line) > 19 and line[7] == 'G' and line[5:7] == '  ':
                cl35_gamma_energy = line[9:19].strip()
                # Remove decimal points for comparison
                gamma_compare = gamma_energy.replace('.', '')
                cl35_compare = cl35_gamma_energy.replace('.', '')
                
                if gamma_compare == cl35_compare or gamma_energy == cl35_gamma_energy:
                    gamma_found = True
                    
                    # Check comment lines following this gamma
                    for j in range(i+1, min(i+3, len(cl35_lines))):
                        comment_line = cl35_lines[j]
                        if 'cG' in comment_line and '1972Hu10' in comment_line:
                            # Found 1972Hu10 citation
                            # Extract RI value from comment
                            # Pattern: "Other: XX.X {In} from 1972Hu10" or "RI$from 1972Hu10"
                            if 'Other:' in comment_line:
                                # Extract RI from "Other: XX.X {In}"
                                match = re.search(r'Other:\s+([\d.]+)\s+\{I(\d+)\}\s+(?:from\s+)?(?:\()?1972Hu10', comment_line)
                                if match:
                                    ri_cl35 = match.group(1)
                                    dri_cl35 = match.group(2)
                                    
                                    if ri_1972 != ri_cl35:
                                        discrepancies.append({
                                            'type': 'RI_MISMATCH',
                                            'level': level_energy,
                                            'gamma': gamma_energy,
                                            'ri_1972': ri_1972,
                                            'ri_cl35': ri_cl35,
                                            'dri_1972': dri_1972,
                                            'dri_cl35': dri_cl35,
                                            'message': f'G {gamma_energy}: RI mismatch - 1972Hu10={ri_1972} vs Cl35={ri_cl35}'
                                        })
                                        print(f'  ❌ G {gamma_energy}: RI MISMATCH - 1972Hu10={ri_1972}({dri_1972}) vs Cl35={ri_cl35}({dri_cl35})')
                                    elif dri_1972 != dri_cl35:
                                        discrepancies.append({
                                            'type': 'DRI_MISMATCH',
                                            'level': level_energy,
                                            'gamma': gamma_energy,
                                            'ri_1972': ri_1972,
                                            'ri_cl35': ri_cl35,
                                            'dri_1972': dri_1972,
                                            'dri_cl35': dri_cl35,
                                            'message': f'G {gamma_energy}: DRI mismatch - 1972Hu10={dri_1972} vs Cl35={dri_cl35}'
                                        })
                                        print(f'  ⚠️  G {gamma_energy}: DRI MISMATCH - 1972Hu10={dri_1972} vs Cl35={dri_cl35} (RI matches: {ri_1972})')
                                    else:
                                        print(f'  ✓ G {gamma_energy}: {ri_1972}({dri_1972}) - MATCHES')
                                    ri_in_comment = True
                                    break
                            elif 'RI$from 1972Hu10' in comment_line:
                                # This means RI should be in G-record field, not comment
                                # Need to check G-record RI field
                                cl35_ri_field = line[21:29].strip()
                                cl35_dri_field = line[29:31].strip()
                                
                                if ri_1972 != cl35_ri_field:
                                    discrepancies.append({
                                        'type': 'RI_MISMATCH',
                                        'level': level_energy,
                                        'gamma': gamma_energy,
                                        'ri_1972': ri_1972,
                                        'ri_cl35': cl35_ri_field,
                                        'dri_1972': dri_1972,
                                        'dri_cl35': cl35_dri_field,
                                        'message': f'G {gamma_energy}: RI mismatch in G-record - 1972Hu10={ri_1972} vs Cl35={cl35_ri_field}'
                                    })
                                    print(f'  ❌ G {gamma_energy}: RI MISMATCH in G-record - 1972Hu10={ri_1972}({dri_1972}) vs Cl35={cl35_ri_field}({cl35_dri_field})')
                                elif dri_1972 != cl35_dri_field:
                                    discrepancies.append({
                                        'type': 'DRI_MISMATCH',
                                        'level': level_energy,
                                        'gamma': gamma_energy,
                                        'ri_1972': ri_1972,
                                        'ri_cl35': cl35_ri_field,
                                        'dri_1972': dri_1972,
                                        'dri_cl35': cl35_dri_field,
                                        'message': f'G {gamma_energy}: DRI mismatch in G-record - 1972Hu10={dri_1972} vs Cl35={cl35_dri_field}'
                                    })
                                    print(f'  ⚠️  G {gamma_energy}: DRI MISMATCH in G-record - 1972Hu10={dri_1972} vs Cl35={cl35_dri_field} (RI matches: {ri_1972})')
                                else:
                                    print(f'  ✓ G {gamma_energy}: {ri_1972}({dri_1972}) in G-record - MATCHES')
                                ri_in_comment = True
                                break
                    break
        
        if not gamma_found:
            discrepancies.append({
                'type': 'MISSING_GAMMA',
                'level': level_energy,
                'gamma': gamma_energy,
                'ri_1972': ri_1972,
                'dri_1972': dri_1972,
                'message': f'G {gamma_energy} NOT FOUND in Cl35_34s_p_g.ens for level L {level_energy}'
            })
            print(f'  ❌ G {gamma_energy}: NOT FOUND in Cl35_34s_p_g.ens')
        elif not ri_in_comment:
            discrepancies.append({
                'type': 'MISSING_RI_CITATION',
                'level': level_energy,
                'gamma': gamma_energy,
                'ri_1972': ri_1972,
                'dri_1972': dri_1972,
                'message': f'G {gamma_energy}: Gamma found but NO 1972Hu10 RI citation in comments'
            })
            print(f'  ❌ G {gamma_energy}: Gamma found but NO 1972Hu10 RI CITATION')

# Summary
print('\n' + '='*80)
print('VERIFICATION SUMMARY')
print('='*80)
print(f'Total levels checked: {len(levels_data)}')
print(f'Total gammas checked: {total_gammas}')
print(f'Total discrepancies found: {len(discrepancies)}')

# Save discrepancies report
with open('.github/temp/1972hu10_verification_report.txt', 'w') as f:
    f.write('1972HU10 RI VERIFICATION REPORT\n')
    f.write('='*80 + '\n\n')
    f.write(f'Total levels checked: {len(levels_data)}\n')
    f.write(f'Total gammas checked: {total_gammas}\n')
    f.write(f'Total discrepancies found: {len(discrepancies)}\n\n')
    
    if discrepancies:
        f.write('DISCREPANCIES:\n')
        f.write('-'*80 + '\n\n')
        
        for disc in discrepancies:
            f.write(f'Type: {disc["type"]}\n')
            f.write(f'Level: L {disc["level"]}\n')
            if 'gamma' in disc:
                f.write(f'Gamma: G {disc["gamma"]}\n')
            if 'ri_1972' in disc:
                f.write(f'1972Hu10 RI: {disc["ri_1972"]}({disc["dri_1972"]})\n')
            if 'ri_cl35' in disc:
                f.write(f'Cl35_34s_p_g RI: {disc["ri_cl35"]}({disc["dri_cl35"]})\n')
            f.write(f'Message: {disc["message"]}\n')
            f.write('\n')
    else:
        f.write('✓ NO DISCREPANCIES FOUND - All RI values match!\n')

print(f'\nDetailed report saved to .github/temp/1972hu10_verification_report.txt')
