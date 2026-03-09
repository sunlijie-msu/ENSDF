"""Verify all Other: values in adp by tracing them to mrg source.
For every cG RI$from line with Other: in adp,
locate the corresponding G record in mrg and validate the exact value."""

import re

ADP_FILE = r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02_1983WA27.adp'
MRG_FILE = r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02_1983WA27.mrg'

def find_prev_G_energy(adp_lines, cg_idx):
    """Find preceding G record energy (return str)."""
    for i in range(cg_idx - 1, max(cg_idx - 15, -1), -1):
        l = adp_lines[i]
        if len(l) >= 8 and l[7] == 'G':
            return l[9:19].strip()
    return None

def extract_other_value(cg_line):
    """Extract the Other: substring (e.g., '<1.7' or '100 {I5}')."""
    # Format: '. Other: VALUE'
    match = re.search(r'\. Other: ([^()]+)\s*\(', cg_line)
    if match:
        return match.group(1).strip()
    return None

def build_mrg_lookup(mrg_lines):
    """Build list of GAMMA blocks with full info: [(adopted_E, dataset_A_info, dataset_B_info)]
       where *_info = {'E': energy, 'RI': ri, 'DRI': dri} or None if no entry"""
    result = []
    current_e = None
    current_A = None
    current_B = None
    
    for ml in mrg_lines:
        l = ml.rstrip('\n')
        if l.startswith(' GAMMA-'):
            if current_e is not None:
                result.append((current_e, current_A, current_B))
            current_e = None
            current_A = None
            current_B = None
            idx = l.find(' 34CL  G')
            if idx >= 0:
                try:
                    current_e = float(l[idx+9:idx+19].strip())
                except:
                    pass
        elif l.startswith(' LEVEL') or l.startswith('-----'):
            if current_e is not None:
                result.append((current_e, current_A, current_B))
            current_e = None
            current_A = None
            current_B = None
        elif current_e is not None and len(l) > 69:
            # Check for dataset G record
            if len(l) > 47 and l[39:47] == ' 34CL  G':
                tag = l[22:35] if len(l) > 35 else ''
                e_str = l[48:58].strip() if len(l) > 57 else ''
                ri = l[60:68].strip() if len(l) > 67 else ''
                dri = l[68:70].strip() if len(l) > 69 else ''
                try:
                    e = float(e_str)
                except:
                    e = None
                
                if '--->A' in tag:
                    current_A = {'E': e, 'RI': ri, 'DRI': dri}
                elif '--->B' in tag:
                    current_B = {'E': e, 'RI': ri, 'DRI': dri}
    
    if current_e is not None:
        result.append((current_e, current_A, current_B))
    return result

def format_expected(ri, dri):
    """Format expected Other: value."""
    if not ri:
        return None
    if dri == 'LT':
        return f'<{ri}'
    elif dri == 'GT':
        return f'>{ri}'
    elif dri:
        return f'{ri} {{I{dri}}}'
    else:
        return ri

adp_lines = open(ADP_FILE, encoding='utf-8').readlines()
mrg_lines = open(MRG_FILE, encoding='utf-8').readlines()
mrg_lookup = build_mrg_lookup(mrg_lines)

print(f"Parsed {len(mrg_lookup)} GAMMA blocks from mrg\n")

# Collect all cG RI$from with Other: lines, filter L <= 6136
other_lines = []
for i, line in enumerate(adp_lines):
    if ('cG RI$from 1977Da02' in line or 'cG RI$from 1983Wa27' in line) and 'Other' in line:
        # Find preceding L record to check if L <= 6136
        l_energy = None
        for j in range(i - 1, max(i - 20, -1), -1):
            if adp_lines[j].strip().startswith('34CL  L'):
                try:
                    l_energy = float(adp_lines[j][9:19].strip())
                    break
                except:
                    pass
        if l_energy is not None and l_energy <= 6136:
            other_lines.append((i + 1, l_energy, line))

print(f"Checking {len(other_lines)} 'Other:' lines (L <= 6136)\n")

pass_count = fail_count = 0
failures = []

for (lnum, l_energy, cg_line) in other_lines:
    g_energy_str = find_prev_G_energy(adp_lines, lnum - 1)
    if g_energy_str is None:
        print(f"WARN L{lnum}: No preceding G record found")
        continue
    
    try:
        g_energy = float(g_energy_str)
    except:
        print(f"WARN L{lnum}: Could not parse G energy '{g_energy_str}'")
        continue
    
    # Determine source and other dataset
    if 'from 1977Da02' in cg_line:
        source_letter = 'A'
        other_letter = 'B'
        other_name = '1983Wa27'
    else:
        source_letter = 'B'
        other_letter = 'A'
        other_name = '1977Da02'
    
    # Find the GAMMA block with the closest gamma energy (from either dataset)
    best_block = None
    best_diff = 2.0
    
    for (adopted_e, info_A, info_B) in mrg_lookup:
        source_info = info_A if source_letter == 'A' else info_B
        other_info = info_A if other_letter == 'A' else info_B
        
        # Check source dataset
        if source_info and source_info['E'] is not None:
            diff = abs(source_info['E'] - g_energy)
            if diff < best_diff:
                best_diff = diff
                best_block = (adopted_e, info_A, info_B)
        
        # Check other dataset
        if other_info and other_info['E'] is not None:
            diff = abs(other_info['E'] - g_energy)
            if diff < best_diff:
                best_diff = diff
                best_block = (adopted_e, info_A, info_B)
    
    if best_block is None or best_diff >= 2.0:
        print(f"FAIL L{lnum} G{g_energy}: No mrg block with matching gamma (closest diff={best_diff:.2f})")
        fail_count += 1
        failures.append((lnum, g_energy, 'no_close_mrg', cg_line.rstrip()))
        continue
    
    adopted_e, info_A, info_B = best_block
    other_info = info_A if other_letter == 'A' else info_B
    
    if other_info is None or other_info['RI'] == '':
        print(f"FAIL L{lnum} G{g_energy}: Other dataset has no RI measurement in best mrg block")
        fail_count += 1
        failures.append((lnum, g_energy, 'other_no_ri', cg_line.rstrip()))
        continue
    
    ri, dri = other_info['RI'], other_info['DRI']
    expected = format_expected(ri, dri)
    if expected is None:
        print(f"FAIL L{lnum} G{g_energy}: Expected no measurement but Other: present")
        fail_count += 1
        failures.append((lnum, g_energy, 'unexpected_other', cg_line.rstrip()))
        continue
    
    actual = extract_other_value(cg_line)
    if actual is None:
        print(f"FAIL L{lnum} G{g_energy}: Could not extract Other: value from adp")
        fail_count += 1
        failures.append((lnum, g_energy, 'extraction_failure', cg_line.rstrip()))
        continue
    
    # EXACT comparison
    if actual == expected:
        pass_count += 1
        # print(f"PASS L{lnum} G{g_energy}: {expected}")
    else:
        print(f"FAIL L{lnum} G{g_energy}: ADP value mismatch")
        print(f"  ADP:      '{actual}'")
        print(f"  Expected: '{expected}' (mrg: ri='{ri}', dri='{dri}')")
        fail_count += 1
        failures.append((lnum, g_energy, 'value_mismatch', cg_line.rstrip(), actual, expected, ri, dri))

print(f"\n{'='*70}")
print(f"SUMMARY: {pass_count} PASS, {fail_count} FAIL")
if fail_count == 0:
    print("ALL CHECKS PASSED ✓")
else:
    print(f"\nFAILURES REQUIRING CORRECTION:")
    for f in failures:
        if len(f) == 4:
            lnum, ge, reason, line = f
            print(f"  L{lnum} ({reason}): {line}")
        else:
            lnum, ge, reason, line, actual, expected, ri, dri = f
            print(f"  L{lnum} (value_mismatch): {line}")
            print(f"    Change '{actual}' → '{expected}'")
