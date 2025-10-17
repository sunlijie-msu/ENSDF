#!/usr/bin/env python3
"""
CORRECTED: Properly collect gammas until next L-record (not just within same section)
"""

# 1. Parse 2001VO24.ens: 10 levels with their gammas and RI values
vo24_data = {}
with open('A35/Cl35/raw/2001VO24.ens') as f:
    current_exi = None
    for line in f:
        if len(line) > 8 and line[7:8] == 'L':
            e_str = line[9:19].strip()
            try:
                current_exi = float(e_str)
                vo24_data[current_exi] = []
            except:
                current_exi = None
        elif current_exi is not None and len(line) > 8 and line[7:8] == 'G':
            eg_str = line[9:19].strip()
            ri_str = line[22:29].strip()
            try:
                eg = float(eg_str)
                ri = int(ri_str.split()[0]) if ri_str and ri_str[0].isdigit() else None
                if ri is not None:
                    vo24_data[current_exi].append((eg, ri))
            except:
                pass

print("2001VO24.ens data:")
for exi in sorted(vo24_data.keys()):
    print(f"  Exi {exi}: {len(vo24_data[exi])} gammas")

# 2. Parse Cl35_34s_p_g.ens: For each target Exi, collect its gammas UNTIL next L-record
cl35_exi_gammas = {}  # Map from approximate Exi to list of gammas

with open('A35/Cl35/new/Cl35_34s_p_g.ens') as f:
    lines = f.readlines()

# First pass: find all L-record positions
l_records = []
for i, line in enumerate(lines):
    if len(line) > 8 and line[7:8] == 'L':
        e_str = line[9:19].strip()
        try:
            exi = float(e_str)
            l_records.append((i, exi))
        except:
            pass

print(f"\nFound {len(l_records)} L-records in Cl35_34s_p_g.ens")

# Second pass: for each L-record, collect its gammas
for idx, (l_line_num, exi) in enumerate(l_records):
    # Gammas follow this L-record until next L-record
    start_line = l_line_num + 1
    if idx + 1 < len(l_records):
        end_line = l_records[idx+1][0]
    else:
        end_line = len(lines)
    
    gammas = []
    for i in range(start_line, end_line):
        line = lines[i]
        if len(line) > 8 and line[7:8] == 'G':
            eg_str = line[9:19].strip()
            ri_str = line[22:29].strip()
            try:
                eg = float(eg_str)
                has_ri_field = ri_str and ri_str not in ['', 'B', 'V', 'S']
                
                # Check for cG RI$ comment
                has_cg_ri = False
                for j in range(i+1, min(i+5, end_line)):
                    if 'cG' in lines[j][6:9] and 'RI$' in lines[j]:
                        has_cg_ri = True
                        break
                
                gammas.append({
                    'line': i+1,
                    'eg': eg,
                    'ri_field': ri_str,
                    'has_cg_ri': has_cg_ri,
                    'has_ri_field': has_ri_field
                })
            except:
                pass
    
    if gammas:
        cl35_exi_gammas[exi] = gammas

print(f"Extracted gammas for {len(cl35_exi_gammas)} Exi levels in Cl35:")
for exi in sorted(cl35_exi_gammas.keys())[:5]:
    print(f"  Exi {exi}: {len(cl35_exi_gammas[exi])} gammas")
if len(cl35_exi_gammas) > 5:
    print(f"  ... and {len(cl35_exi_gammas)-5} more levels")

# 3. Match gammas and create insertion list
print("\n" + "="*70)
print("MATCHING GAMMAS AND RI VALUES:")
print("="*70)

all_additions = []

for vo24_exi in sorted(vo24_data.keys()):
    # Find closest Cl35 Exi
    cl35_exi = None
    min_diff = 999
    for ce in cl35_exi_gammas.keys():
        diff = abs(ce - vo24_exi)
        if diff < 2.0 and diff < min_diff:
            cl35_exi = ce
            min_diff = diff
    
    if cl35_exi is None:
        print(f"\n❌ Exi {vo24_exi} from 2001VO24 not matched in Cl35!")
        continue
    
    vo24_gammas = sorted(vo24_data[vo24_exi], key=lambda x: x[0])
    cl35_gammas = sorted(cl35_exi_gammas[cl35_exi], key=lambda x: x['eg'])
    
    print(f"\nExi {vo24_exi} (2001VO24) <-> Exi {cl35_exi} (Cl35):")
    print(f"  2001VO24: {len(vo24_gammas)} gammas, Cl35: {len(cl35_gammas)} gammas")
    
    matched_count = 0
    missing_count = 0
    
    for eg_vo24, ri_vo24 in vo24_gammas:
        found = False
        for g in cl35_gammas:
            if abs(g['eg'] - eg_vo24) < 1.0:
                found = True
                if g['has_cg_ri']:
                    matched_count += 1
                else:
                    print(f"    Need: Line {g['line']:4d} Eg {g['eg']:8.1f} → RI${ri_vo24}")
                    all_additions.append((g['line'], ri_vo24))
                    missing_count += 1
                break
        
        if not found:
            print(f"    NOT FOUND: Eg {eg_vo24:8.1f}")
    
    print(f"  Result: {matched_count} ✓, {missing_count} need adding, {len(vo24_gammas)-matched_count-missing_count} not in file")

print("\n" + "="*70)
print(f"TOTAL: {len(all_additions)} gammas need RI$ values")
print("="*70)

if len(all_additions) > 0:
    # Sort by line number (descending for bottom-to-top insertion)
    all_additions_sorted = sorted(set(all_additions), key=lambda x: x[0], reverse=True)
    print(f"\nInsertion order (BOTTOM to TOP):")
    for i, (line_num, ri_val) in enumerate(all_additions_sorted, 1):
        if i <= 5 or i > len(all_additions_sorted) - 5:
            print(f"  {i:2d}. After line {line_num}: Insert cG RI${ri_val} {{2001Vo24}}")
        elif i == 6:
            print(f"  ... ({len(all_additions_sorted)-10} more) ...")
