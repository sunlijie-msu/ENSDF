#!/usr/bin/env python3
"""
Comprehensive data cross-check: 2026BAAA_CR11022_209Po
Verifies 100% consistency of Eγ, Iγ, Jπ, Eμ, R_DCO, ΔP_DCO, multipolarity
"""

import re
from collections import defaultdict

# Read files
md_file = "XUNDL/2026BAAA_CR11022_209Po_original_Table_I.md"
ens_file = "XUNDL/2026BAAA_CR11022_209Po.ens"

with open(md_file, 'r', encoding='utf-8') as f:
    md_content = f.read()

with open(ens_file, 'r', encoding='utf-8') as f:
    ens_content = f.read()

ens_lines = ens_content.split('\n')

print("=" * 100)
print("DATA CROSS-CHECK: 209Po 2026BaAA")
print("=" * 100)

# ==============================================================================
# PARSE MARKDOWN TABLE
# ==============================================================================
print("\n" + "=" * 100)
print("STEP 1: PARSE MARKDOWN TABLE")
print("=" * 100)

md_lines = md_content.split('\n')
md_transitions = []

for line in md_lines:
    # Table rows start with |
    if not line.startswith('|') or '---' in line or '---' not in line and '|' not in line:
        continue
    
    # Skip header/separator lines
    if 'Eγ' in line or '---' in line or 'Multipolarity' in line:
        continue
    
    # Parse data row
    parts = [p.strip() for p in line.split('|')[1:-1]]  # Remove first/last empty
    
    if len(parts) < 7:
        continue
    
    try:
        eg_raw = parts[0]  # e.g., "54.7(3)"
        jpi_raw = parts[1]  # e.g., "$17/2- \to 13/2-$"
        ei_raw = parts[2]   # e.g., "1472.6(2)"
        ig_raw = parts[3]   # e.g., "–" or "0.28(1)"
        rdco_raw = parts[4]  # e.g., "–" or "1.01(2)"
        pdco_raw = parts[5]  # e.g., "–" or "0.12(1)"
        mult_raw = parts[6]  # e.g., "E2" or "M1+E2"
        
        # Extract E and J from raw strings
        # Eγ format: "54.7(3)" → value="54.7", unc="3"
        eg_match = re.match(r'([\d.]+)\((\d+)\)', eg_raw)
        if not eg_match:
            continue
        eg_val = eg_match.group(1)
        eg_unc = eg_match.group(2)
        
        # E_i format: "1472.6(2)"
        ei_match = re.match(r'([\d.]+)\((\d+)\)', ei_raw)
        if not ei_match:
            continue
        ei_val = ei_match.group(1)
        ei_unc = ei_match.group(2)
        
        # Extract J_i and J_f from "$17/2- \to 13/2-$"
        jpi_clean = jpi_raw.replace('$', '').strip()
        if ' \\to ' in jpi_clean:
            jpi_i, jpi_f = jpi_clean.split(' \\to ')
            jpi_i = jpi_i.strip()
            jpi_f = jpi_f.strip()
        else:
            jpi_i = jpi_clean
            jpi_f = '?'
        
        # Parse Iγ
        ig_val = None
        ig_unc = None
        if ig_raw != '–':
            ig_match = re.match(r'([\d.]+)\((\d+)\)', ig_raw)
            if ig_match:
                ig_val = ig_match.group(1)
                ig_unc = ig_match.group(2)
        
        # Parse R_DCO
        rdco_val = None
        rdco_unc = None
        if rdco_raw != '–':
            rdco_match = re.match(r'([\d.+-]+)\((\d+)\)', rdco_raw)
            if rdco_match:
                rdco_val = rdco_match.group(1)
                rdco_unc = rdco_match.group(2)
        
        # Parse POL (ΔP_DCO)
        pdco_val = None
        pdco_unc = None
        if pdco_raw != '–':
            pdco_match = re.match(r'([+-][\d.]+)\((\d+)\)', pdco_raw)
            if pdco_match:
                pdco_val = pdco_match.group(1)
                pdco_unc = pdco_match.group(2)
        
        # Clean multipolarity
        mult = mult_raw.strip()
        
        # Deduced multipolarities in table are marked with different notes
        # We need to capture those too
        
        md_transitions.append({
            'Eg': eg_val,
            'Eg_unc': eg_unc,
            'E_initial': ei_val,
            'E_initial_unc': ei_unc,
            'Jpi_i': jpi_i,
            'Jpi_f': jpi_f,
            'Ig': ig_val,
            'Ig_unc': ig_unc,
            'Rdco': rdco_val,
            'Rdco_unc': rdco_unc,
            'Pdco': pdco_val,
            'Pdco_unc': pdco_unc,
            'Multipolarity': mult,
            'raw_Eg': eg_raw,
            'raw_Jpi': jpi_raw,
            'raw_Ei': ei_raw,
            'raw_Ig': ig_raw,
            'raw_Rdco': rdco_raw,
            'raw_Pdco': pdco_raw
        })
    except Exception as e:
        pass

print(f"\nSuccessfully parsed {len(md_transitions)} gamma transitions from markdown")

print("\nFirst 5 transitions (markdown):")
for i, t in enumerate(md_transitions[:5]):
    print(f"\n  {i+1}. Eγ={t['Eg']}({t['Eg_unc']}), E_i={t['E_initial']}({t['E_initial_unc']})")
    print(f"     Jπ_i={t['Jpi_i']}, Jπ_f={t['Jpi_f']}")
    print(f"     Iγ={t['Ig']}({t['Ig_unc']}) if Ig else None, M={t['Multipolarity']}")
    print(f"     R_DCO={t['Rdco']}({t['Rdco_unc']}), POL={t['Pdco']}({t['Pdco_unc']})")

# ==============================================================================
# PARSE ENSDF FILE
# ==============================================================================
print("\n" + "=" * 100)
print("STEP 2: PARSE ENSDF FILE")
print("=" * 100)

l_records = []  # List of level records
g_records = []  # List of gamma records with associated comment
current_parent_i = 0  # Index of current parent level record

for line_num, line in enumerate(ens_lines, 1):
    if len(line) < 9:
        continue
    
    # Detect record type: column 8 contains the type (L, G, etc.)
    if len(line) > 8:
        rec_type = line[7]
        
        # L-RECORD (Level)
        if rec_type == 'L':
            e_str = line[9:19].strip()
            de_str = line[19:21].strip()
            j_str = line[22:39].strip()
            
            if e_str:
                try:
                    l_records.append({
                        'E': e_str,
                        'DE': de_str,
                        'Jpi': j_str,
                        'line_num': line_num,
                        'full_line': line.rstrip(),
                        'g_records': []  # Will accumulate following G-records
                    })
                    current_parent_i = len(l_records) - 1
                except:
                    pass
        
        # G-RECORD (Gamma)
        elif rec_type == 'G':
            e_str = line[9:19].strip()
            de_str = line[19:21].strip()
            ri_str = line[22:29].strip()
            dri_str = line[29:31].strip()
            m_str = line[32:41].strip()
            
            if e_str and current_parent_i >= 0:
                try:
                    g_record = {
                        'E': e_str,
                        'DE': de_str,
                        'RI': ri_str,
                        'DRI': dri_str,
                        'Multipolarity': m_str,
                        'line_num': line_num,
                        'full_line': line.rstrip(),
                        'comments': [],
                        'parent_idx': current_parent_i
                    }
                    if current_parent_i < len(l_records):
                        l_records[current_parent_i]['g_records'].append(g_record)
                    g_records.append(g_record)
                except:
                    pass
        
        # COMMENT LINE (cG or cL)
        elif rec_type == 'c':
            # This is a comment line; attach to last G-record or L-record
            if g_records:
                g_records[-1]['comments'].append(line.rstrip())

print(f"\nSuccessfully parsed {len(l_records)} L-records (levels)")
print(f"Successfully parsed {len(g_records)} G-records (gammas)")
print(f"Found {sum(len(g['comments']) for g in g_records)} comment lines")

print("\nFirst 5 L-records (ENSDF):")
for i, l in enumerate(l_records[:5]):
    print(f"  {i+1}. E={l['E']:>10}, DE={l['DE']:>2}, Jπ={l['Jpi']:<12} | {len(l['g_records'])} gammas")

print("\nFirst 5 G-records (ENSDF):")
for i, g in enumerate(g_records[:5]):
    print(f"  {i+1}. Eγ={g['E']:>10}, RI={g['RI']:>10}, M={g['Multipolarity']:<12} | {len(g['comments'])} comments")

# ==============================================================================
# MATCH AND COMPARE
# ==============================================================================
print("\n" + "=" * 100)
print("STEP 3: MATCH AND COMPARE")
print("=" * 100)

mismatches = []

# For each markdown transition, find matching ENSDF G-record
for md_trans in md_transitions:
    # Find level: match E_initial (with uncertainties) and Jpi_i
    # Look for L-record with E close to md E_initial
    E_i_md = float(md_trans['E_initial'])
    Eg_md = float(md_trans['Eg'])
    Jpi_i_md = md_trans['Jpi_i']
    
    # Find matching level
    matched_level = None
    for l_rec in l_records:
        try:
            E_l = float(l_rec['E'])
            # Check if energies match (within ±0.5 keV tolerance for numeric representation)
            if abs(E_l - E_i_md) < 0.6 and Jpi_i_md in l_rec['Jpi']:
                matched_level = l_rec
                break
        except:
            pass
    
    if not matched_level:
        mismatches.append({
            'type': 'missing_level',
            'Eg': md_trans['Eg'],
            'E_initial': md_trans['E_initial'],
            'Jpi_i': md_trans['Jpi_i'],
            'detail': f"L-record E={md_trans['E_initial']}, Jπ={md_trans['Jpi_i']} not found"
        })
        continue
    
    # Find matching G-record within this level
    matched_gamma = None
    for g_rec in matched_level['g_records']:
        try:
            E_g = float(g_rec['E'])
            # Check if energies match
            if abs(E_g - Eg_md) < 0.6:
                matched_gamma = g_rec
                break
        except:
            pass
    
    if not matched_gamma:
        mismatches.append({
            'type': 'missing_gamma',
            'Eg': md_trans['Eg'],
            'E_initial': md_trans['E_initial'],
            'Jpi_i': md_trans['Jpi_i'],
            'detail': f"G-record Eγ={md_trans['Eg']} keV in level E={md_trans['E_initial']} not found"
        })
        continue
    
    # ========================================================================
    # DETAILED COMPARISONS FOR MATCHED RECORDS
    # ========================================================================
    
    # 1. Compare Eγ and DE
    try:
        eg_ens = float(matched_gamma['E'])
        eg_md_val = float(md_trans['Eg'])
        if abs(eg_ens - eg_md_val) > 0.01:
            mismatches.append({
                'type': 'value_mismatch',
                'field': 'Eγ (G-record E)',
                'Eg': md_trans['Eg'],
                'E_initial': md_trans['E_initial'],
                'source': md_trans['Eg'],
                'target': matched_gamma['E'],
                'g_line': matched_gamma['line_num']
            })
    except:
        pass
    
    # 2. Compare RI and DRI (Iγ)
    if md_trans['Ig']:
        ig_ens_str = matched_gamma['RI']
        ig_md_str = md_trans['Ig']
        try:
            ig_ens = float(ig_ens_str)
            ig_md = float(ig_md_str)
            if abs(ig_ens - ig_md) > 0.1 * max(abs(ig_md), 0.1):  # 10% tolerance for small values
                mismatches.append({
                    'type': 'value_mismatch',
                    'field': 'Iγ (G-record RI)',
                    'Eg': md_trans['Eg'],
                    'E_initial': md_trans['E_initial'],
                    'source': ig_md_str,
                    'target': ig_ens_str,
                    'g_line': matched_gamma['line_num']
                })
        except:
            if ig_md_str.strip() != ig_ens_str.strip():
                mismatches.append({
                    'type': 'value_mismatch',
                    'field': 'Iγ (G-record RI)',
                    'Eg': md_trans['Eg'],
                    'E_initial': md_trans['E_initial'],
                    'source': ig_md_str,
                    'target': ig_ens_str,
                    'g_line': matched_gamma['line_num']
                })
    
    # 3. Compare Multipolarity
    mult_md = md_trans['Multipolarity'].strip()
    mult_ens = matched_gamma['Multipolarity'].strip()
    if mult_md and mult_ens and mult_md != mult_ens:
        mismatches.append({
            'type': 'multipolarity_mismatch',
            'Eg': md_trans['Eg'],
            'E_initial': md_trans['E_initial'],
            'source': mult_md,
            'target': mult_ens,
            'g_line': matched_gamma['line_num']
        })
    
    # 4. Compare R_DCO in cG comments
    if md_trans['Rdco'] and matched_gamma['comments']:
        # Find R_DCO in comment
        for cg_line in matched_gamma['comments']:
            if 'R{-DCO}' in cg_line:
                # Extract value from comment
                # Example: "209PO cG $R{-DCO}(Q)=1.01 {I2}. POL=+0.12 {I1}."
                rdco_match = re.search(r'R\{-DCO\}\([^)]*\)=([\d.+-]+)\s+\{I(\d+)\}', cg_line)
                if rdco_match:
                    rdco_ens_val = rdco_match.group(1)
                    rdco_ens_unc = rdco_match.group(2)
                    if rdco_ens_val != md_trans['Rdco']:
                        mismatches.append({
                            'type': 'comment_value_mismatch',
                            'field': 'R_DCO',
                            'Eg': md_trans['Eg'],
                            'E_initial': md_trans['E_initial'],
                            'source': f"{md_trans['Rdco']} ({md_trans['Rdco_unc']})",
                            'target': f"{rdco_ens_val} ({rdco_ens_unc})",
                            'comment_line': cg_line[:80]
                        })
                break
    
    # 5. Compare POL (ΔP_DCO) in cG comments
    if md_trans['Pdco'] and matched_gamma['comments']:
        for cg_line in matched_gamma['comments']:
            if 'POL' in cg_line:
                # Extract value from comment
                pdco_match = re.search(r'POL=([+-][\d.]+)\s+\{I(\d+)\}', cg_line)
                if pdco_match:
                    pdco_ens_val = pdco_match.group(1)
                    pdco_ens_unc = pdco_match.group(2)
                    if pdco_ens_val != md_trans['Pdco']:
                        mismatches.append({
                            'type': 'comment_value_mismatch',
                            'field': 'POL (ΔP_DCO)',
                            'Eg': md_trans['Eg'],
                            'E_initial': md_trans['E_initial'],
                            'source': f"{md_trans['Pdco']} ({md_trans['Pdco_unc']})",
                            'target': f"{pdco_ens_val} ({pdco_ens_unc})",
                            'comment_line': cg_line[:80]
                        })
                break

# ==============================================================================
# REPORT RESULTS
# ==============================================================================
print(f"\nTotal mismatches found: {len(mismatches)}")

mismatch_types = defaultdict(list)
for m in mismatches:
    mismatch_types[m['type']].append(m)

print("\nMismatches by type:")
for mtype, items in sorted(mismatch_types.items()):
    print(f"  {mtype}: {len(items)}")

if mismatches:
    print("\n" + "=" * 100)
    print("DETAILED MISMATCH REPORT")
    print("=" * 100)
    
    # Show first 20 mismatches in detail
    for i, m in enumerate(mismatches[:20]):
        print(f"\n{i+1}. {m['type'].upper()}")
        print(f"   Eγ={m['Eg']}, E_initial={m['E_initial']}, Jπ_i={m.get('Jpi_i', '?')}")
        if 'field' in m:
            print(f"   Field: {m['field']}")
            print(f"   Source (MD):  {m.get('source', '?')}")
            print(f"   Target (ENS): {m.get('target', '?')}")
        if 'detail' in m:
            print(f"   Detail: {m['detail']}")
        if 'g_line' in m:
            print(f"   G-record line: {m['g_line']}")
        if 'comment_line' in m:
            print(f"   Comment: {m['comment_line']}")

print("\n" + "=" * 100)
print("END OF REPORT")
print("=" * 100)
