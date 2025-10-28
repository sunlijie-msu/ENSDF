#!/usr/bin/env python3
"""
Create precise mapping of which gammas need RI additions.
For each of the 10 target Exi levels, match their gammas in Cl35_34s_p_g.ens
to the RI values from 2001VO24.ens
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

# 2. Parse Cl35_34s_p_g.ens: Find the 10 target Exi levels and their gammas
cl35_data = {}
with open('A35/Cl35/new/Cl35_34s_p_g.ens') as f:
    lines = f.readlines()
    current_exi = None
    current_exi_line = None
    for i, line in enumerate(lines):
        if len(line) > 8 and line[7:8] == 'L':
            e_str = line[9:19].strip()
            try:
                current_exi = float(e_str)
                current_exi_line = i + 1
                # Check if this is one of our target Exi levels (within 2 keV)
                for target_exi in vo24_data.keys():
                    if abs(current_exi - target_exi) < 2.0:
                        cl35_data[current_exi] = {'line': current_exi_line, 'gammas': []}
                        break
            except:
                current_exi = None
        elif current_exi is not None and current_exi in cl35_data and len(line) > 8 and line[7:8] == 'G':
            eg_str = line[9:19].strip()
            ri_str = line[22:29].strip()
            try:
                eg = float(eg_str)
                has_ri = ri_str and ri_str not in ['', 'B', 'V', 'S']
                # Check if this G-record has a cG RI$ comment
                has_cg_ri = False
                for j in range(i+1, min(i+5, len(lines))):
                    if 'cG' in lines[j][6:9] and 'RI$' in lines[j]:
                        has_cg_ri = True
                        break
                
                cl35_data[current_exi]['gammas'].append({
                    'line': i+1,
                    'eg': eg,
                    'ri_field': ri_str,
                    'has_cg_ri': has_cg_ri
                })
            except:
                pass

print("\nCl35_34s_p_g.ens matching Exi levels found:")
for exi in sorted(cl35_data.keys()):
    print(f"  Exi {exi} @ line {cl35_data[exi]['line']}: {len(cl35_data[exi]['gammas'])} gammas")

# 3. Match gammas between 2001VO24 and Cl35 for each level
print("\n" + "="*70)
print("MATCHING GAMMAS AND RI VALUES:")
print("="*70)

all_additions = []

for vo24_exi in sorted(vo24_data.keys()):
    # Find corresponding Cl35 Exi
    cl35_exi = None
    for ce in cl35_data.keys():
        if abs(ce - vo24_exi) < 2.0:
            cl35_exi = ce
            break
    
    if cl35_exi is None:
        print(f"\n❌ Exi {vo24_exi} from 2001VO24 not matched in Cl35!")
        continue
    
    print(f"\nExi {vo24_exi} (2001VO24) <-> Exi {cl35_exi} (Cl35 @ line {cl35_data[cl35_exi]['line']}):")
    print(f"  2001VO24: {len(vo24_data[vo24_exi])} gammas")
    print(f"  Cl35: {len(cl35_data[cl35_exi]['gammas'])} gammas")
    
    vo24_gammas = sorted(vo24_data[vo24_exi], key=lambda x: x[0])
    cl35_gammas = sorted(cl35_data[cl35_exi]['gammas'], key=lambda x: x['eg'])
    
    # Match gammas by energy (within 1 keV tolerance)
    matched = 0
    missing_ri = []
    
    for eg_vo24, ri_vo24 in vo24_gammas:
        # Find matching gamma in Cl35
        found = False
        for g in cl35_gammas:
            if abs(g['eg'] - eg_vo24) < 1.0:  # 1 keV tolerance
                found = True
                if g['has_cg_ri']:
                    print(f"    ✓ Eg {g['eg']:8.1f} (line {g['line']:4d}): has cG RI$ (RI${ri_vo24})")
                    matched += 1
                else:
                    print(f"    ⚠ Eg {g['eg']:8.1f} (line {g['line']:4d}): NEEDS RI${ri_vo24}")
                    missing_ri.append((g['line'], ri_vo24, g['eg']))
                    all_additions.append((g['line'], ri_vo24))
                break
        
        if not found:
            print(f"    ❌ Eg {eg_vo24:8.1f}: NOT found in Cl35")
    
    print(f"  Summary: {matched} have cG RI$, {len(missing_ri)} need RI$ added")

print("\n" + "="*70)
print("FINAL INSERTION PLAN (insert from BOTTOM to TOP to preserve line numbers):")
print("="*70)
print(f"Total additions needed: {len(all_additions)}")
print()

# Sort by line number in descending order (for bottom-to-top insertion)
all_additions_sorted = sorted(all_additions, key=lambda x: x[0], reverse=True)

for i, (line_num, ri_val) in enumerate(all_additions_sorted, 1):
    print(f"{i:2d}. After line {line_num}: Insert cG RI${ri_val} {{2001Vo24}}")

print(f"\n✅ Ready for insertion!")
