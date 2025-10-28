import re
from pathlib import Path

def normalize_energy(energy_str):
    """Normalize energy string for comparison"""
    try:
        return float(energy_str)
    except:
        return energy_str

def energies_match(e1_str, e2_str, tolerance=0.5):
    """Check if two energies match within tolerance"""
    try:
        e1 = float(e1_str)
        e2 = float(e2_str)
        return abs(e1 - e2) < tolerance
    except:
        # If conversion fails, try string match
        return e1_str.replace('.', '').replace(' ', '') == e2_str.replace('.', '').replace(' ', '')

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
        
        current_level = {
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

# Now verify each RI in Cl35_34s_p_g.ens
print('\n' + '='*80)
print('VERIFICATION PHASE: Checking each RI in Cl35_34s_p_g.ens')
print('='*80)

discrepancies = []
matches = []

for level in levels_data:
    level_energy = level['energy_str']
    
    # Search for this level in Cl35_34s_p_g.ens with energy tolerance
    level_found = False
    cl35_level_line = None
    cl35_level_energy_str = level_energy
    
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
                        if abs(cl35_energy - target_energy) > 0.05:
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
        print(f'\n❌ Level L {level_energy} NOT FOUND in Cl35_34s_p_g.ens ({len(level["gammas"])} gammas)')
        continue
    
    # Now check each gamma for this level
    print(f'\n✓ Level L {level_energy} (Cl35: L {cl35_level_energy_str}) - checking {len(level["gammas"])} gammas')
    
    for gamma in level['gammas']:
        gamma_energy = gamma['energy']
        ri_1972 = gamma['ri']
        dri_1972 = gamma['dri']
        
        # Search for this gamma in Cl35_34s_p_g.ens near this level
        # Look in next 150 lines after the level
        gamma_found = False
        ri_in_comment = False
        cl35_gamma_energy = None
        
        for i in range(cl35_level_line, min(cl35_level_line + 150, len(cl35_lines))):
            line = cl35_lines[i]
            
            # Stop if we hit next level
            if i > cl35_level_line and len(line) > 8 and line[7] == 'L' and line[5:7] == '  ':
                break
            
            # Check if this is a gamma with matching energy
            if len(line) > 19 and line[7] == 'G' and line[5:7] == '  ':
                cl35_gamma_energy = line[9:19].strip()
                
                if energies_match(gamma_energy, cl35_gamma_energy):
                    gamma_found = True
                    
                    # Check comment lines following this gamma
                    for j in range(i+1, min(i+3, len(cl35_lines))):
                        comment_line = cl35_lines[j]
                        
                        # Stop if we hit another G-record or L-record
                        if len(comment_line) > 8 and comment_line[7] in 'GL' and comment_line[5:7] == '  ':
                            break
                        
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
                                            'gamma_cl35': cl35_gamma_energy,
                                            'ri_1972': ri_1972,
                                            'ri_cl35': ri_cl35,
                                            'dri_1972': dri_1972,
                                            'dri_cl35': dri_cl35,
                                            'message': f'G {gamma_energy}(Cl35:{cl35_gamma_energy}): RI mismatch - 1972Hu10={ri_1972}({dri_1972}) vs Cl35={ri_cl35}({dri_cl35})'
                                        })
                                        print(f'  ❌ G {gamma_energy}(Cl35:{cl35_gamma_energy}): RI MISMATCH - 1972Hu10={ri_1972}({dri_1972}) vs Cl35={ri_cl35}({dri_cl35})')
                                    elif dri_1972 != dri_cl35:
                                        discrepancies.append({
                                            'type': 'DRI_MISMATCH',
                                            'level': level_energy,
                                            'gamma': gamma_energy,
                                            'gamma_cl35': cl35_gamma_energy,
                                            'ri_1972': ri_1972,
                                            'ri_cl35': ri_cl35,
                                            'dri_1972': dri_1972,
                                            'dri_cl35': dri_cl35,
                                            'message': f'G {gamma_energy}(Cl35:{cl35_gamma_energy}): DRI mismatch - 1972Hu10={dri_1972} vs Cl35={dri_cl35} (RI matches: {ri_1972})'
                                        })
                                        print(f'  ⚠️  G {gamma_energy}(Cl35:{cl35_gamma_energy}): DRI MISMATCH - 1972Hu10={dri_1972} vs Cl35={dri_cl35} (RI matches: {ri_1972})')
                                    else:
                                        matches.append({
                                            'level': level_energy,
                                            'gamma': gamma_energy,
                                            'gamma_cl35': cl35_gamma_energy,
                                            'ri': ri_1972,
                                            'dri': dri_1972
                                        })
                                        print(f'  ✓ G {gamma_energy}(Cl35:{cl35_gamma_energy}): {ri_1972}({dri_1972}) - MATCHES')
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
                                        'gamma_cl35': cl35_gamma_energy,
                                        'ri_1972': ri_1972,
                                        'ri_cl35': cl35_ri_field,
                                        'dri_1972': dri_1972,
                                        'dri_cl35': cl35_dri_field,
                                        'message': f'G {gamma_energy}(Cl35:{cl35_gamma_energy}): RI mismatch in G-record - 1972Hu10={ri_1972}({dri_1972}) vs Cl35={cl35_ri_field}({cl35_dri_field})'
                                    })
                                    print(f'  ❌ G {gamma_energy}(Cl35:{cl35_gamma_energy}): RI MISMATCH in G-record - 1972Hu10={ri_1972}({dri_1972}) vs Cl35={cl35_ri_field}({cl35_dri_field})')
                                elif dri_1972 != cl35_dri_field:
                                    discrepancies.append({
                                        'type': 'DRI_MISMATCH',
                                        'level': level_energy,
                                        'gamma': gamma_energy,
                                        'gamma_cl35': cl35_gamma_energy,
                                        'ri_1972': ri_1972,
                                        'ri_cl35': cl35_ri_field,
                                        'dri_1972': dri_1972,
                                        'dri_cl35': cl35_dri_field,
                                        'message': f'G {gamma_energy}(Cl35:{cl35_gamma_energy}): DRI mismatch in G-record - 1972Hu10={dri_1972} vs Cl35={cl35_dri_field} (RI matches: {ri_1972})'
                                    })
                                    print(f'  ⚠️  G {gamma_energy}(Cl35:{cl35_gamma_energy}): DRI MISMATCH in G-record - 1972Hu10={dri_1972} vs Cl35={cl35_dri_field} (RI matches: {ri_1972})')
                                else:
                                    matches.append({
                                        'level': level_energy,
                                        'gamma': gamma_energy,
                                        'gamma_cl35': cl35_gamma_energy,
                                        'ri': ri_1972,
                                        'dri': dri_1972
                                    })
                                    print(f'  ✓ G {gamma_energy}(Cl35:{cl35_gamma_energy}): {ri_1972}({dri_1972}) in G-record - MATCHES')
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
                'gamma_cl35': cl35_gamma_energy,
                'ri_1972': ri_1972,
                'dri_1972': dri_1972,
                'message': f'G {gamma_energy}(Cl35:{cl35_gamma_energy}): Gamma found but NO 1972Hu10 RI citation in comments'
            })
            print(f'  ❌ G {gamma_energy}(Cl35:{cl35_gamma_energy}): Gamma found but NO 1972Hu10 RI CITATION')

# Summary
print('\n' + '='*80)
print('VERIFICATION SUMMARY')
print('='*80)
print(f'Total levels checked: {len(levels_data)}')
print(f'Total gammas checked: {total_gammas}')
print(f'Matches found: {len(matches)}')
print(f'Discrepancies found: {len(discrepancies)}')

# Categorize discrepancies
missing_levels = [d for d in discrepancies if d['type'] == 'MISSING_LEVEL']
missing_gammas = [d for d in discrepancies if d['type'] == 'MISSING_GAMMA']
missing_citations = [d for d in discrepancies if d['type'] == 'MISSING_RI_CITATION']
ri_mismatches = [d for d in discrepancies if d['type'] == 'RI_MISMATCH']
dri_mismatches = [d for d in discrepancies if d['type'] == 'DRI_MISMATCH']

print(f'\nBreakdown:')
print(f'  - Missing levels: {len(missing_levels)}')
print(f'  - Missing gammas: {len(missing_gammas)}')
print(f'  - Missing RI citations: {len(missing_citations)}')
print(f'  - RI value mismatches: {len(ri_mismatches)}')
print(f'  - DRI value mismatches: {len(dri_mismatches)}')

# Save discrepancies report
with open('.github/temp/1972hu10_verification_report_v2.txt', 'w') as f:
    f.write('1972HU10 RI VERIFICATION REPORT (IMPROVED)\n')
    f.write('='*80 + '\n\n')
    f.write(f'Total levels checked: {len(levels_data)}\n')
    f.write(f'Total gammas checked: {total_gammas}\n')
    f.write(f'Matches found: {len(matches)}\n')
    f.write(f'Discrepancies found: {len(discrepancies)}\n\n')
    
    f.write(f'Breakdown:\n')
    f.write(f'  - Missing levels: {len(missing_levels)}\n')
    f.write(f'  - Missing gammas: {len(missing_gammas)}\n')
    f.write(f'  - Missing RI citations: {len(missing_citations)}\n')
    f.write(f'  - RI value mismatches: {len(ri_mismatches)}\n')
    f.write(f'  - DRI value mismatches: {len(dri_mismatches)}\n\n')
    
    if discrepancies:
        f.write('DISCREPANCIES:\n')
        f.write('-'*80 + '\n\n')
        
        # Group by type
        if missing_levels:
            f.write(f'### MISSING LEVELS ({len(missing_levels)}) ###\n\n')
            for disc in missing_levels:
                f.write(f'Level: L {disc["level"]} - {len([g for l in levels_data if l["energy_str"] == disc["level"] for g in l["gammas"]])} gammas missing\n')
            f.write('\n')
        
        if missing_gammas:
            f.write(f'### MISSING GAMMAS ({len(missing_gammas)}) ###\n\n')
            for disc in missing_gammas:
                f.write(f'Level L {disc["level"]}, Gamma G {disc["gamma"]}: RI={disc["ri_1972"]}({disc["dri_1972"]})\n')
            f.write('\n')
        
        if missing_citations:
            f.write(f'### MISSING RI CITATIONS ({len(missing_citations)}) ###\n\n')
            for disc in missing_citations:
                f.write(f'Level L {disc["level"]}, Gamma G {disc["gamma"]}(Cl35:{disc["gamma_cl35"]}): RI={disc["ri_1972"]}({disc["dri_1972"]})\n')
            f.write('\n')
        
        if ri_mismatches:
            f.write(f'### RI VALUE MISMATCHES ({len(ri_mismatches)}) ###\n\n')
            for disc in ri_mismatches:
                f.write(f'Level L {disc["level"]}, Gamma G {disc["gamma"]}(Cl35:{disc["gamma_cl35"]})\n')
                f.write(f'  1972Hu10: RI={disc["ri_1972"]}({disc["dri_1972"]})\n')
                f.write(f'  Cl35:     RI={disc["ri_cl35"]}({disc["dri_cl35"]})\n\n')
        
        if dri_mismatches:
            f.write(f'### DRI VALUE MISMATCHES ({len(dri_mismatches)}) ###\n\n')
            for disc in dri_mismatches:
                f.write(f'Level L {disc["level"]}, Gamma G {disc["gamma"]}(Cl35:{disc["gamma_cl35"]})\n')
                f.write(f'  1972Hu10: RI={disc["ri_1972"]}({disc["dri_1972"]})\n')
                f.write(f'  Cl35:     RI={disc["ri_cl35"]}({disc["dri_cl35"]})\n\n')
    else:
        f.write('✓ NO DISCREPANCIES FOUND - All RI values match!\n')

print(f'\nDetailed report saved to .github/temp/1972hu10_verification_report_v2.txt')
