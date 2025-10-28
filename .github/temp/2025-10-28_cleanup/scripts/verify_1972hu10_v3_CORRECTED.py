#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORRECTED VERSION 3: Verify 1972Hu10 RI citations in Cl35_34s_p_g.ens
FIXED BUG: Now correctly detects "Others: XX (ref), XX.X {In} (1972Hu10)" pattern
"""

import re
import sys

def normalize_energy(energy_str):
    """Convert energy string to float, handling various formats"""
    try:
        # Remove leading/trailing whitespace
        energy_str = energy_str.strip()
        # Remove any non-numeric characters except decimal point
        energy_str = re.sub(r'[^\d.]', '', energy_str)
        if energy_str:
            return float(energy_str)
    except:
        pass
    return None

def energies_match(e1_str, e2_str, tolerance=0.5):
    """Check if two energies match within tolerance"""
    e1 = normalize_energy(e1_str)
    e2 = normalize_energy(e2_str)
    if e1 is None or e2 is None:
        return False
    return abs(e1 - e2) <= tolerance

def extract_ri_from_1972hu10_comment(comment_block):
    """
    Extract RI value from 1972Hu10 citation in comment.
    Handles multiple patterns:
    1. "Other: XX.X {In} from 1972Hu10"
    2. "Other: XX.X {In} (1972Hu10)"
    3. "Others: XX (ref1), XX.X {In} (1972Hu10)" - 1972Hu10 as secondary citation
    """
    if '1972Hu10' not in comment_block and '1972hu10' not in comment_block.lower():
        return None, None
    
    # Look for pattern: number + {In} + (1972Hu10) or from 1972Hu10
    # This handles both primary and secondary citations
    pattern = r'(\d+\.?\d*)\s*\{[Ii](\d+)\}\s*(?:from\s*)?\(1972Hu10\)'
    match = re.search(pattern, comment_block, re.IGNORECASE)
    
    if match:
        ri = match.group(1)
        dri = match.group(2)
        return ri, dri
    
    return None, None

# Read 1972HU10.ens and parse from L 7066.4 onwards
print("=" * 80)
print("CORRECTED VERIFICATION: 1972Hu10 RI values in Cl35_34s_p_g.ens")
print("=" * 80)

file_1972 = r"d:\X\ND\ENSDF\A35\Cl35\raw\1972HU10.ens"
file_cl35 = r"d:\X\ND\ENSDF\A35\Cl35\new\Cl35_34s_p_g.ens"

# Parse 1972HU10.ens starting from L 7066.4
with open(file_1972, 'r', encoding='latin-1') as f:
    lines_1972 = f.readlines()

# Find starting line with L 7066.4
start_idx = None
for i, line in enumerate(lines_1972):
    if len(line) >= 19 and line[7:8] == 'L':
        energy_str = line[9:19].strip()
        if energies_match(energy_str, "7066.4", tolerance=0.1):
            start_idx = i
            print(f"Found L 7066.4 at line {i+1} in 1972Hu10.ens")
            break

if start_idx is None:
    print("ERROR: Could not find L 7066.4 in 1972Hu10.ens")
    sys.exit(1)

# Parse all levels and gammas from 1972HU10
levels_1972 = []
current_level = None

for i in range(start_idx, len(lines_1972)):
    line = lines_1972[i]
    if len(line) < 8:
        continue
    
    record_type = line[7:8]
    
    if record_type == 'L':
        # New level
        energy_str = line[9:19].strip()
        if energy_str:
            current_level = {
                'energy': energy_str,
                'line': i + 1,
                'gammas': []
            }
            levels_1972.append(current_level)
    
    elif record_type == 'G' and current_level is not None:
        # Gamma transition
        energy_str = line[9:19].strip()
        ri_str = line[21:29].strip()
        dri_str = line[29:31].strip()
        
        if ri_str:  # Only include gammas with RI values
            current_level['gammas'].append({
                'energy': energy_str,
                'ri': ri_str,
                'dri': dri_str,
                'line': i + 1
            })

print(f"Parsed {len(levels_1972)} levels from 1972Hu10.ens")
total_gammas = sum(len(level['gammas']) for level in levels_1972)
print(f"Total gammas with RI values: {total_gammas}")
print()

# Read Cl35_34s_p_g.ens
with open(file_cl35, 'r', encoding='latin-1') as f:
    lines_cl35 = f.readlines()

# Verify each level and gamma
matches = []
discrepancies = []

print("VERIFICATION RESULTS:")
print("=" * 80)

for level_1972 in levels_1972:
    level_energy = level_1972['energy']
    
    # Find matching level in Cl35 (with tolerance)
    cl35_level_idx = None
    cl35_level_energy = None
    
    for i, line in enumerate(lines_cl35):
        if len(line) >= 19 and line[7:8] == 'L':
            energy_str = line[9:19].strip()
            if energies_match(energy_str, level_energy, tolerance=0.5):
                cl35_level_idx = i
                cl35_level_energy = energy_str
                break
    
    if cl35_level_idx is None:
        # Level not found in Cl35
        discrepancies.append({
            'type': 'MISSING_LEVEL',
            'level': level_energy,
            'num_gammas': len(level_1972['gammas']),
            'message': f'L {level_energy}: NOT FOUND in Cl35_34s_p_g.ens ({len(level_1972["gammas"])} gammas with RI values)'
        })
        print(f'❌ Level L {level_energy}: NOT FOUND in Cl35_34s_p_g.ens ({len(level_1972["gammas"])} gammas)')
        continue
    
    # Level found - check gammas
    print(f'✓ Level L {level_energy} (Cl35: L {cl35_level_energy}) - checking {len(level_1972["gammas"])} gammas')
    
    for gamma_1972 in level_1972['gammas']:
        gamma_energy = gamma_1972['energy']
        ri_1972 = gamma_1972['ri']
        dri_1972 = gamma_1972['dri']
        
        # Find matching gamma in Cl35 (starting from level line)
        gamma_found = False
        cl35_gamma_energy = None
        
        for i in range(cl35_level_idx + 1, len(lines_cl35)):
            line = lines_cl35[i]
            
            # Stop at next level
            if len(line) >= 19 and line[7:8] == 'L':
                break
            
            # Check for G-record
            if len(line) >= 19 and line[7:8] == 'G':
                energy_str = line[9:19].strip()
                if energies_match(energy_str, gamma_energy, tolerance=0.5):
                    gamma_found = True
                    cl35_gamma_energy = energy_str
                    
                    # Now search for following cG comment lines
                    citation_found = False
                    ri_cl35 = None
                    dri_cl35 = None
                    
                    # Collect all following comment lines
                    comment_block = ""
                    for j in range(i + 1, min(i + 10, len(lines_cl35))):
                        comment_line = lines_cl35[j]
                        if len(comment_line) >= 8:
                            if comment_line[7:9] in ['cG', '2c', '3c', '4c', '5c']:
                                comment_block += comment_line
                            else:
                                break
                    
                    # Check if 1972Hu10 is cited
                    ri_cl35, dri_cl35 = extract_ri_from_1972hu10_comment(comment_block)
                    
                    if ri_cl35 is not None:
                        citation_found = True
                        
                        # Compare RI values
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
                    else:
                        # Gamma found but no 1972Hu10 citation
                        discrepancies.append({
                            'type': 'MISSING_RI_CITATION',
                            'level': level_energy,
                            'gamma': gamma_energy,
                            'gamma_cl35': cl35_gamma_energy,
                            'ri_1972': ri_1972,
                            'dri_1972': dri_1972,
                            'message': f'G {gamma_energy}(Cl35:{cl35_gamma_energy}): Gamma found but NO 1972Hu10 RI CITATION (1972Hu10 has RI={ri_1972}({dri_1972}))'
                        })
                        print(f'  ❌ G {gamma_energy}(Cl35:{cl35_gamma_energy}): Gamma found but NO 1972Hu10 RI CITATION')
                    
                    break
        
        if not gamma_found:
            # Gamma not found in Cl35
            discrepancies.append({
                'type': 'MISSING_GAMMA',
                'level': level_energy,
                'gamma': gamma_energy,
                'ri_1972': ri_1972,
                'dri_1972': dri_1972,
                'message': f'G {gamma_energy}: NOT FOUND in Cl35_34s_p_g.ens (1972Hu10 has RI={ri_1972}({dri_1972}))'
            })
            print(f'  ❌ G {gamma_energy}: NOT FOUND in Cl35_34s_p_g.ens')

# Print summary
print()
print("=" * 80)
print("VERIFICATION SUMMARY:")
print("=" * 80)
print(f"Total levels checked: {len(levels_1972)}")
print(f"Total gammas checked: {total_gammas}")
print(f"Matches found: {len(matches)}")
print(f"Discrepancies found: {len(discrepancies)}")
print()

# Categorize discrepancies
missing_levels = [d for d in discrepancies if d['type'] == 'MISSING_LEVEL']
missing_gammas = [d for d in discrepancies if d['type'] == 'MISSING_GAMMA']
missing_citations = [d for d in discrepancies if d['type'] == 'MISSING_RI_CITATION']
ri_mismatches = [d for d in discrepancies if d['type'] == 'RI_MISMATCH']
dri_mismatches = [d for d in discrepancies if d['type'] == 'DRI_MISMATCH']

print("Breakdown:")
print(f"  - Missing levels: {len(missing_levels)}")
print(f"  - Missing gammas: {len(missing_gammas)}")
print(f"  - Missing RI citations: {len(missing_citations)}")
print(f"  - RI value mismatches: {len(ri_mismatches)}")
print(f"  - DRI value mismatches: {len(dri_mismatches)}")
print()

# Save detailed report
output_file = r".github/temp/1972hu10_verification_report_v3_CORRECTED.txt"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("CORRECTED VERIFICATION REPORT: 1972Hu10 RI Citations in Cl35_34s_p_g.ens\n")
    f.write("=" * 80 + "\n\n")
    
    f.write("SUMMARY:\n")
    f.write(f"Total levels checked: {len(levels_1972)}\n")
    f.write(f"Total gammas checked: {total_gammas}\n")
    f.write(f"Matches found: {len(matches)}\n")
    f.write(f"Discrepancies found: {len(discrepancies)}\n\n")
    
    f.write("Breakdown:\n")
    f.write(f"  - Missing levels: {len(missing_levels)}\n")
    f.write(f"  - Missing gammas: {len(missing_gammas)}\n")
    f.write(f"  - Missing RI citations: {len(missing_citations)}\n")
    f.write(f"  - RI value mismatches: {len(ri_mismatches)}\n")
    f.write(f"  - DRI value mismatches: {len(dri_mismatches)}\n\n")
    
    f.write("=" * 80 + "\n")
    f.write("DETAILED FINDINGS:\n")
    f.write("=" * 80 + "\n\n")
    
    if missing_levels:
        f.write(f"1. MISSING LEVELS ({len(missing_levels)} levels):\n")
        f.write("-" * 80 + "\n")
        for d in missing_levels:
            f.write(f"  L {d['level']}: NOT in Cl35_34s_p_g.ens ({d['num_gammas']} gammas)\n")
        f.write("\n")
    
    if missing_gammas:
        f.write(f"2. MISSING GAMMAS ({len(missing_gammas)} gammas):\n")
        f.write("-" * 80 + "\n")
        for d in missing_gammas:
            f.write(f"  L {d['level']}, G {d['gamma']}: RI={d['ri_1972']}({d['dri_1972']}) - NOT in Cl35\n")
        f.write("\n")
    
    if missing_citations:
        f.write(f"3. MISSING RI CITATIONS ({len(missing_citations)} gammas):\n")
        f.write("-" * 80 + "\n")
        for d in missing_citations:
            f.write(f"  L {d['level']}, G {d['gamma']} (Cl35:{d['gamma_cl35']}): ")
            f.write(f"RI={d['ri_1972']}({d['dri_1972']}) - NO 1972Hu10 citation\n")
        f.write("\n")
    
    if ri_mismatches:
        f.write(f"4. RI VALUE MISMATCHES ({len(ri_mismatches)} gammas):\n")
        f.write("-" * 80 + "\n")
        for d in ri_mismatches:
            f.write(f"  L {d['level']}, G {d['gamma']} (Cl35:{d['gamma_cl35']}): ")
            f.write(f"1972Hu10={d['ri_1972']}({d['dri_1972']}) vs Cl35={d['ri_cl35']}({d['dri_cl35']})\n")
        f.write("\n")
    
    if dri_mismatches:
        f.write(f"5. DRI VALUE MISMATCHES ({len(dri_mismatches)} gammas):\n")
        f.write("-" * 80 + "\n")
        for d in dri_mismatches:
            f.write(f"  L {d['level']}, G {d['gamma']} (Cl35:{d['gamma_cl35']}): ")
            f.write(f"1972Hu10 DRI={d['dri_1972']} vs Cl35 DRI={d['dri_cl35']} (RI matches: {d['ri_1972']})\n")
        f.write("\n")
    
    if matches:
        f.write(f"6. SUCCESSFUL MATCHES ({len(matches)} gammas):\n")
        f.write("-" * 80 + "\n")
        for m in matches:
            f.write(f"  L {m['level']}, G {m['gamma']} (Cl35:{m['gamma_cl35']}): {m['ri']}({m['dri']}) ✓\n")
        f.write("\n")

print(f"Detailed report saved to {output_file}")
print()
print("=" * 80)
print("CORRECTED VERIFICATION COMPLETE")
print("=" * 80)
