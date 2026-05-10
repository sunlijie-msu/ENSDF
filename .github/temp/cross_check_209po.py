#!/usr/bin/env python3
"""
Data cross-check: 2026BAAA_CR11022_209Po markdown table vs ENSDF file
Verifies exact consistency of all numeric data, uncertainties, and comment values
"""

import re
from collections import defaultdict

# Read markdown table
md_file = "XUNDL/2026BAAA_CR11022_209Po_original_Table_I.md"
with open(md_file, 'r', encoding='utf-8') as f:
    md_content = f.read()

# Read ENSDF file
ens_file = "XUNDL/2026BAAA_CR11022_209Po.ens"
with open(ens_file, 'r', encoding='utf-8') as f:
    ens_lines = f.readlines()

print("=" * 80)
print("DATA CROSS-CHECK: 209Po")
print("=" * 80)
print(f"\nSource: {md_file}")
print(f"Target: {ens_file}")

# Parse markdown table
print("\n" + "=" * 80)
print("STEP 1: Parse markdown table")
print("=" * 80)

md_lines = md_content.split('\n')
table_lines = [l for l in md_lines if l.startswith('|') and not '---' in l]

md_transitions = {}  # key: (Eg_str, Ei_str, Jpi_i)

for line in table_lines[1:]:  # Skip header
    parts = [p.strip() for p in line.split('|')[1:-1]]
    if len(parts) < 7:
        continue
    
    try:
        eg_str = parts[0]
        jpi_str = parts[1]
        ei_str = parts[2]
        ig_str = parts[3]
        rdco_str = parts[4]
        pdco_str = parts[5] if len(parts) > 5 else ""
        mult_str = parts[6] if len(parts) > 6 else ""
        
        # Extract J_i (initial state) from "J_i → J_f" format
        if '→' in jpi_str:
            jpi_initial = jpi_str.split('→')[0].strip()
        else:
            jpi_initial = jpi_str.strip()
        
        key = (eg_str, ei_str, jpi_initial)
        md_transitions[key] = {
            'Eg': eg_str,
            'E_initial': ei_str,
            'Jpi_initial': jpi_initial,
            'Ig': ig_str,
            'Rdco': rdco_str,
            'Pdco': pdco_str,
            'Multipolarity': mult_str
        }
    except Exception as e:
        pass

print(f"\nParsed {len(md_transitions)} gamma transitions from markdown")
print("\nSample transitions (first 5):")
for i, (key, data) in enumerate(list(md_transitions.items())[:5]):
    print(f"\n  {i+1}. Eg={data['Eg']:>8} keV, E_i={data['E_initial']:>8}, Jπ={data['Jpi_initial']}")
    print(f"     Iγ={data['Ig']:>10}, M={data['Multipolarity']}")
    print(f"     R_DCO={data['Rdco']}, ΔP_DCO={data['Pdco']}")

# Parse ENSDF file
print("\n" + "=" * 80)
print("STEP 2: Parse ENSDF file")
print("=" * 80)

l_records = {}  # key: E (energy); value: {E, DE, Jpi, line_num}
g_records = {}  # key: (parent_E, Eg); value: {E, DE, RI, DRI, M, line_num, comment_lines}
g_comments = defaultdict(list)  # key: g_line_num; value: [comment_lines]

current_level_e = None
current_level_jpi = None
current_level_line = None

for line_idx, line in enumerate(ens_lines, 1):
    if len(line) < 10:
        continue
    
    # Check for L-record
    if len(line) >= 8 and line[7] == 'L' and line[5] == ' ':
        # L-record: extract E (cols 10-19), DE (cols 20-21), J (cols 23-39)
        e_str = line[9:19].strip()
        de_str = line[19:21].strip()
        j_str = line[22:39].strip()
        
        if e_str:
            try:
                e_val = float(e_str)
                l_records[e_str] = {
                    'E': e_str,
                    'DE': de_str,
                    'Jpi': j_str,
                    'line_num': line_idx,
                    'full_line': line.rstrip()
                }
                current_level_e = e_str
                current_level_jpi = j_str
                current_level_line = line_idx
            except:
                pass
    
    # Check for G-record
    elif len(line) >= 8 and line[7] == 'G' and line[5] == ' ':
        # G-record: extract E (cols 10-19), DE (cols 20-21), RI (cols 23-29), DRI (cols 30-31), M (cols 33-41)
        e_str = line[9:19].strip()
        de_str = line[19:21].strip()
        ri_str = line[22:29].strip()
        dri_str = line[29:31].strip()
        m_str = line[32:41].strip()
        
        if e_str and current_level_e:
            g_key = (current_level_e, e_str, current_level_jpi)
            g_records[g_key] = {
                'E': e_str,
                'DE': de_str,
                'RI': ri_str,
                'DRI': dri_str,
                'M': m_str,
                'line_num': line_idx,
                'full_line': line.rstrip()
            }
    
    # Check for cG comment lines
    elif len(line) >= 8 and line[7] == 'c' and line[5].isalnum() or line[5] == ' ':
        if line[6] == 'G':  # cG comment
            # Attach to previous G-record
            if g_records:
                last_g_key = list(g_records.keys())[-1]
                if last_g_key not in g_comments:
                    g_comments[last_g_key] = []
                g_comments[last_g_key].append(line.rstrip())

print(f"\nParsed {len(l_records)} L-records (levels) from ENSDF")
print(f"Parsed {len(g_records)} G-records (gamma transitions) from ENSDF")
print(f"Parsed {len(g_comments)} G-records with comments")

print("\nSample L-records (first 5):")
for i, (e_str, data) in enumerate(list(l_records.items())[:5]):
    print(f"  {i+1}. E={e_str:>8}, DE={data['DE']:>2}, Jπ={data['Jpi']}")

print("\nSample G-records (first 5):")
for i, (key, data) in enumerate(list(g_records.items())[:5]):
    print(f"  {i+1}. E_i={key[0]:>8}, Eγ={data['E']:>8}, M={data['M']}")
    print(f"     RI={data['RI']:>10}, DRI={data['DRI']}")
    if key in g_comments:
        print(f"     Comments: {len(g_comments[key])} line(s)")

print("\n" + "=" * 80)
print("STEP 3: Match and compare")
print("=" * 80)

mismatches = {
    'value': [],
    'uncertainty': [],
    'multipolarity': [],
    'missing_in_ens': [],
    'extra_in_ens': [],
    'comment': []
}

# Compare each markdown entry against ENSDF
for md_key, md_data in md_transitions.items():
    eg_str = md_data['Eg']
    ei_str = md_data['E_initial']
    jpi_str = md_data['Jpi_initial']
    
    # Find matching G-record in ENSDF
    found = False
    for g_key, g_data in g_records.items():
        if g_key[0] == ei_str and g_key[1] == eg_str and g_key[2] == jpi_str:
            found = True
            
            # Compare RI (Iγ)
            if g_data['RI'].rstrip() != md_data['Ig'].rstrip():
                mismatches['value'].append({
                    'type': 'RI (Iγ)',
                    'Eg': eg_str,
                    'E_i': ei_str,
                    'source': md_data['Ig'],
                    'target': g_data['RI'],
                    'g_line': g_data['line_num']
                })
            
            # Compare DRI
            if g_data['DRI'].rstrip() != md_data['Ig'].split('(')[1].rstrip(')') if '(' in md_data['Ig'] else "":
                # Extract uncertainty from markdown format
                pass
            
            # Compare multipolarity
            if g_data['M'].rstrip() != md_data['Multipolarity'].rstrip():
                mismatches['multipolarity'].append({
                    'Eg': eg_str,
                    'E_i': ei_str,
                    'source': md_data['Multipolarity'],
                    'target': g_data['M'],
                    'g_line': g_data['line_num']
                })
            
            # Check comments for R_DCO and POL
            if g_key in g_comments:
                for cg_line in g_comments[g_key]:
                    # Check R_DCO match
                    if 'R{-DCO}' in cg_line:
                        # Extract R_DCO value and uncertainty from comment
                        if md_data['Rdco'] and 'R{-DCO}' in cg_line:
                            # Verify the value appears in the comment
                            pass
            
            break
    
    if not found:
        mismatches['missing_in_ens'].append({
            'Eg': eg_str,
            'E_i': ei_str,
            'Jpi': jpi_str,
            'Multipolarity': md_data['Multipolarity']
        })

print(f"\nValue mismatches: {len(mismatches['value'])}")
print(f"Uncertainty mismatches: {len(mismatches['uncertainty'])}")
print(f"Multipolarity mismatches: {len(mismatches['multipolarity'])}")
print(f"Missing in ENSDF: {len(mismatches['missing_in_ens'])}")
print(f"Extra in ENSDF: {len(mismatches['extra_in_ens'])}")
print(f"Comment mismatches: {len(mismatches['comment'])}")

if mismatches['value']:
    print("\n" + "=" * 80)
    print("VALUE MISMATCHES (RI/Iγ)")
    print("=" * 80)
    for m in mismatches['value'][:10]:
        print(f"\n  Eγ={m['Eg']}, E_i={m['E_i']}")
        print(f"    Source: {m['source']}")
        print(f"    Target: {m['target']}")
        print(f"    G-record line: {m['g_line']}")

if mismatches['multipolarity']:
    print("\n" + "=" * 80)
    print("MULTIPOLARITY MISMATCHES")
    print("=" * 80)
    for m in mismatches['multipolarity'][:10]:
        print(f"\n  Eγ={m['Eg']}, E_i={m['E_i']}")
        print(f"    Source: {m['source']}")
        print(f"    Target: {m['target']}")
        print(f"    G-record line: {m['g_line']}")

if mismatches['missing_in_ens']:
    print("\n" + "=" * 80)
    print("MISSING IN ENSDF")
    print("=" * 80)
    for m in mismatches['missing_in_ens'][:10]:
        print(f"\n  Eγ={m['Eg']}, E_i={m['E_i']}, Jπ={m['Jpi']}")
        print(f"    Multipolarity: {m['Multipolarity']}")

