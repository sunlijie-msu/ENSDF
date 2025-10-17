#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FINAL CORRECTED VERSION: Verify 1972Hu10 RI citations in Cl35_34s_p_g.ens
CRITICAL FIX: Use Ep (S field) for matching resonance levels, NOT level energy
"""

import re
import sys

def normalize_energy(energy_str):
    """Convert energy string to float"""
    try:
        energy_str = energy_str.strip()
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

def extract_ep_from_s_field(line):
    """Extract Ep (proton energy) from S field (columns 22-39)"""
    if len(line) < 39:
        return None
    s_field = line[21:39].strip()
    # S field format: "Ep dEp" - extract first number
    match = re.match(r'(\d+\.?\d*)', s_field)
    if match:
        return match.group(1)
    return None

def is_data_record(line):
    """Check if line is a data record (not comment)"""
    if len(line) < 8:
        return False
    # CRITICAL: Index 5 (ENSDF column 6) must be ' ' for data, 'c' for comment
    # Index 7 (ENSDF column 8) must be 'L' or 'G' for data records
    return line[5] == ' ' and line[7] in ['L', 'G']

def extract_ri_from_1972hu10_comment(comment_block):
    """Extract RI value from 1972Hu10 citation in comment"""
    if '1972Hu10' not in comment_block and '1972hu10' not in comment_block.lower():
        return None, None
    
    # Pattern: number + {In} + (1972Hu10)
    pattern = r'(\d+\.?\d*)\s*\{[Ii](\d+)\}\s*\(1972Hu10\)'
    match = re.search(pattern, comment_block, re.IGNORECASE)
    
    if match:
        return match.group(1), match.group(2)
    
    return None, None

print("=" * 80)
print("FINAL CORRECTED VERIFICATION: 1972Hu10 RI values")
print("Using Ep (S field) for level matching")
print("=" * 80)

file_1972 = r"d:\X\ND\ENSDF\A35\Cl35\raw\1972HU10.ens"
file_cl35 = r"d:\X\ND\ENSDF\A35\Cl35\new\Cl35_34s_p_g.ens"

# Parse 1972HU10.ens starting from L 7066.4
with open(file_1972, 'r', encoding='latin-1') as f:
    lines_1972 = f.readlines()

# Find L 7066.4
start_idx = None
for i, line in enumerate(lines_1972):
    if is_data_record(line) and line[7] == 'L':
        energy = line[9:19].strip()
        if energies_match(energy, "7066.4", 0.1):
            start_idx = i
            print(f"Found L 7066.4 at line {i+1}")
            break

if not start_idx:
    print("ERROR: L 7066.4 not found")
    sys.exit(1)

# Parse all L-records and their G-records
levels_1972 = []
current_level = None

for i in range(start_idx, len(lines_1972)):
    line = lines_1972[i]
    
    if is_data_record(line):
        if line[7] == 'L':
            # New level
            energy = line[9:19].strip()
            ep = extract_ep_from_s_field(line)
            
            if energy:
                current_level = {
                    'energy': energy,
                    'ep': ep,
                    'line': i + 1,
                    'gammas': []
                }
                levels_1972.append(current_level)
        
        elif line[7] == 'G' and current_level:
            # Gamma
            gamma_energy = line[9:19].strip()
            ri = line[21:29].strip()
            dri = line[29:31].strip()
            
            if gamma_energy and ri:
                current_level['gammas'].append({
                    'energy': gamma_energy,
                    'ri': ri,
                    'dri': dri
                })

print(f"Parsed {len(levels_1972)} levels with Ep values")
total_gammas = sum(len(lv['gammas']) for lv in levels_1972)
print(f"Total gammas: {total_gammas}")
print()

# Read Cl35_34s_p_g.ens
with open(file_cl35, 'r', encoding='latin-1') as f:
    lines_cl35 = f.readlines()

# Verify
matches = []
discrepancies = []

for level_1972 in levels_1972:
    level_energy = level_1972['energy']
    ep_1972 = level_1972['ep']
    
    if not ep_1972:
        print(f"⚠️  L {level_energy}: No Ep in 1972Hu10 - skipping")
        continue
    
    # Find matching level by Ep (S field)
    cl35_level_idx = None
    cl35_level_energy = None
    
    for i, line in enumerate(lines_cl35):
        if is_data_record(line) and line[7] == 'L':
            ep_cl35 = extract_ep_from_s_field(line)
            if ep_cl35 and energies_match(ep_1972, ep_cl35, tolerance=3.0):
                cl35_level_idx = i
                cl35_level_energy = line[9:19].strip()
                break
    
    if not cl35_level_idx:
        discrepancies.append({
            'type': 'MISSING_LEVEL',
            'level': level_energy,
            'ep': ep_1972,
            'num_gammas': len(level_1972['gammas'])
        })
        print(f'❌ L {level_energy} (Ep={ep_1972}): NOT FOUND in Cl35')
        continue
    
    print(f'✓ L {level_energy} (1972: Ep={ep_1972}, Cl35: L {cl35_level_energy}) - {len(level_1972["gammas"])} gammas')
    
    # Check each gamma
    for gamma_1972 in level_1972['gammas']:
        gamma_energy = gamma_1972['energy']
        ri_1972 = gamma_1972['ri']
        dri_1972 = gamma_1972['dri']
        
        # Find matching gamma
        gamma_found = False
        cl35_gamma_energy = None
        
        for i in range(cl35_level_idx + 1, len(lines_cl35)):
            line = lines_cl35[i]
            
            # Stop at next level
            if is_data_record(line) and line[7] == 'L':
                break
            
            if is_data_record(line) and line[7] == 'G':
                energy_cl35 = line[9:19].strip()
                if energies_match(gamma_energy, energy_cl35, 2.0):
                    gamma_found = True
                    cl35_gamma_energy = energy_cl35
                    
                    # Collect comments
                    comment_block = ""
                    for j in range(i + 1, min(i + 15, len(lines_cl35))):
                        cline = lines_cl35[j]
                        if len(cline) >= 8 and cline[7:9] in ['cG', '2c', '3c', '4c', '5c']:
                            comment_block += cline
                        elif is_data_record(cline):
                            break
                    
                    # Check for 1972Hu10 citation
                    ri_cl35, dri_cl35 = extract_ri_from_1972hu10_comment(comment_block)
                    
                    if ri_cl35:
                        # Check match
                        if ri_1972 == ri_cl35 and dri_1972 == dri_cl35:
                            matches.append({
                                'level': level_energy,
                                'ep': ep_1972,
                                'gamma': gamma_energy,
                                'ri': ri_1972,
                                'dri': dri_1972
                            })
                            print(f'  ✓ G {gamma_energy}: {ri_1972}({dri_1972}) MATCHES')
                        else:
                            discrepancies.append({
                                'type': 'VALUE_MISMATCH',
                                'level': level_energy,
                                'ep': ep_1972,
                                'gamma': gamma_energy,
                                'ri_1972': ri_1972,
                                'dri_1972': dri_1972,
                                'ri_cl35': ri_cl35,
                                'dri_cl35': dri_cl35
                            })
                            print(f'  ❌ G {gamma_energy}: MISMATCH {ri_1972}({dri_1972}) vs {ri_cl35}({dri_cl35})')
                    else:
                        discrepancies.append({
                            'type': 'MISSING_CITATION',
                            'level': level_energy,
                            'ep': ep_1972,
                            'gamma': gamma_energy,
                            'ri_1972': ri_1972,
                            'dri_1972': dri_1972
                        })
                        print(f'  ❌ G {gamma_energy}: NO 1972Hu10 CITATION')
                    break
        
        if not gamma_found:
            discrepancies.append({
                'type': 'MISSING_GAMMA',
                'level': level_energy,
                'ep': ep_1972,
                'gamma': gamma_energy,
                'ri_1972': ri_1972,
                'dri_1972': dri_1972
            })
            print(f'  ❌ G {gamma_energy}: NOT FOUND')

# Summary
print()
print("=" * 80)
print("SUMMARY:")
print(f"Matches: {len(matches)}")
print(f"Discrepancies: {len(discrepancies)}")

missing_levels = [d for d in discrepancies if d['type'] == 'MISSING_LEVEL']
missing_gammas = [d for d in discrepancies if d['type'] == 'MISSING_GAMMA']
missing_citations = [d for d in discrepancies if d['type'] == 'MISSING_CITATION']
value_mismatches = [d for d in discrepancies if d['type'] == 'VALUE_MISMATCH']

print(f"  - Missing levels: {len(missing_levels)}")
print(f"  - Missing gammas: {len(missing_gammas)}")
print(f"  - Missing citations: {len(missing_citations)}")
print(f"  - Value mismatches: {len(value_mismatches)}")

# Save report
output = r".github/temp/1972hu10_FINAL_CORRECT_REPORT.txt"
with open(output, 'w', encoding='utf-8') as f:
    f.write("FINAL CORRECTED VERIFICATION REPORT\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"Matches: {len(matches)}\n")
    f.write(f"Discrepancies: {len(discrepancies)}\n\n")
    
    if missing_citations:
        f.write(f"MISSING CITATIONS ({len(missing_citations)}):\n")
        f.write("-" * 80 + "\n")
        for d in missing_citations:
            f.write(f"L {d['level']} (Ep={d['ep']}), G {d['gamma']}: RI={d['ri_1972']}({d['dri_1972']})\n")
        f.write("\n")
    
    if value_mismatches:
        f.write(f"VALUE MISMATCHES ({len(value_mismatches)}):\n")
        f.write("-" * 80 + "\n")
        for d in value_mismatches:
            f.write(f"L {d['level']} (Ep={d['ep']}), G {d['gamma']}: ")
            f.write(f"1972={d['ri_1972']}({d['dri_1972']}) vs Cl35={d['ri_cl35']}({d['dri_cl35']})\n")
        f.write("\n")
    
    if missing_gammas:
        f.write(f"MISSING GAMMAS ({len(missing_gammas)}):\n")
        f.write("-" * 80 + "\n")
        for d in missing_gammas:
            f.write(f"L {d['level']} (Ep={d['ep']}), G {d['gamma']}: RI={d['ri_1972']}({d['dri_1972']})\n")
        f.write("\n")
    
    if missing_levels:
        f.write(f"MISSING LEVELS ({len(missing_levels)}):\n")
        f.write("-" * 80 + "\n")
        for d in missing_levels:
            f.write(f"L {d['level']} (Ep={d['ep']}): {d['num_gammas']} gammas\n")

print(f"\nReport saved: {output}")
print("=" * 80)
