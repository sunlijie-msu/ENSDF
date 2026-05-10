#!/usr/bin/env python3
"""
Comprehensive data cross-check: 2026BAAA 209Po
Source: markdown table with gamma energies, intensities, J-pi, R_DCO, POL, multipolarities
Target: ENSDF file G-records and L-records with cG/cL comments
"""

import re
from collections import defaultdict

# Read files
md_file = "XUNDL/2026BAAA_CR11022_209Po_original_Table_I.md"
ens_file = "XUNDL/2026BAAA_CR11022_209Po.ens"

with open(md_file, 'r', encoding='utf-8') as f:
    md_lines = f.readlines()

with open(ens_file, 'r', encoding='utf-8') as f:
    ens_lines = f.readlines()

print("=" * 100)
print("DATA CROSS-CHECK: 209Po 2026BaAA")
print("=" * 100)

# ==============================================================================
# PARSE MARKDOWN TABLE
# ==============================================================================
print("\nSTEP 1: Parse Markdown Table")

md_trans = []
for line_num, line in enumerate(md_lines, 1):
    if not line.startswith('|'):
        continue
    if '---' in line or 'Eγ' in line:
        continue
    
    parts = [p.strip() for p in line.split('|')[1:-1]]
    if len(parts) < 7:
        continue
    
    try:
        eg_raw = parts[0]
        jpi_raw = parts[1]
        ei_raw = parts[2]
        ig_raw = parts[3]
        rdco_raw = parts[4]
        pdco_raw = parts[5]
        mult_raw = parts[6]
        
        m_eg = re.match(r'^([\d.]+)\((\d+)\)$', eg_raw)
        if not m_eg:
            continue
        eg_val, eg_unc = m_eg.groups()
        
        m_ei = re.match(r'^([\d.]+)\((\d+)\)$', ei_raw)
        if not m_ei:
            continue
        ei_val, ei_unc = m_ei.groups()
        
        jpi_clean = jpi_raw.replace('$', '').strip()
        if ' \\to ' in jpi_clean:
            jpi_parts = jpi_clean.split(' \\to ')
            jpi_i = jpi_parts[0].strip()
            jpi_f = jpi_parts[1].strip() if len(jpi_parts) > 1 else ''
        else:
            jpi_i = jpi_clean
            jpi_f = ''
        
        ig_val = ig_unc = None
        if ig_raw != '–':
            m_ig = re.match(r'^([\d.]+)\((\d+)\)$', ig_raw)
            if m_ig:
                ig_val, ig_unc = m_ig.groups()
        
        rdco_val = rdco_unc = None
        if rdco_raw != '–':
            m_rdco = re.match(r'^([\d.+-]+)\((\d+)\)$', rdco_raw)
            if m_rdco:
                rdco_val, rdco_unc = m_rdco.groups()
        
        pdco_val = pdco_unc = None
        if pdco_raw != '–':
            m_pdco = re.match(r'^([+-][\d.]+)\((\d+)\)$', pdco_raw)
            if m_pdco:
                pdco_val, pdco_unc = m_pdco.groups()
        
        md_trans.append({
            'Eg': eg_val,
            'Eg_unc': eg_unc,
            'E_i': ei_val,
            'E_i_unc': ei_unc,
            'Jpi_i': jpi_i,
            'Jpi_f': jpi_f,
            'Ig': ig_val,
            'Ig_unc': ig_unc,
            'Rdco': rdco_val,
            'Rdco_unc': rdco_unc,
            'Pdco': pdco_val,
            'Pdco_unc': pdco_unc,
            'Multipolarity': mult_raw.strip(),
            'md_line': line_num
        })
    except:
        pass

print(f"✓ Parsed {len(md_trans)} gamma transitions from markdown table")

# ==============================================================================
# PARSE ENSDF FILE
# ==============================================================================
print("STEP 2: Parse ENSDF File")

# Find PN line
pn_idx = None
for idx, line in enumerate(ens_lines):
    if ' PN' in line:
        pn_idx = idx
        break

if pn_idx is None:
    print("ERROR: PN line not found")
    exit(1)

print(f"✓ Found PN line at line {pn_idx + 1}")

# Parse data records
l_recs = []
g_recs = []
current_parent = None
last_data_rec_idx = None  # Index of last non-comment record

for line_idx in range(pn_idx, len(ens_lines)):
    line = ens_lines[line_idx]
    
    if len(line) < 9:
        continue
    
    # Check NUCID
    nucid = line[0:5].strip()
    if nucid not in ('209PO', '209Po'):
        continue
    
    # Columns (1-indexed):  1-5=NUCID, 6=CONT, 7=blank, 8=TYPE
    # 0-indexed:            0-4=NUCID, 5=CONT, 6=blank, 7=TYPE
    # For comments: 6=c (the comment indicator replaces the blank)
    
    cont = line[5] if len(line) > 5 else ' '
    
    # Check if this is a comment line (column 7 = 'c')
    is_comment = (len(line) > 6 and line[6] == 'c')
    
    if is_comment:
        # Comment line - attach to last data record (L or G)
        if g_recs:
            g_recs[-1]['comments'].append(line.rstrip())
        continue
    
    # Not a comment - it's a data record
    rec_type = line[7] if len(line) > 7 else ' '
    
    if rec_type == 'L':
        # L-record
        e_str = line[9:19].strip()
        de_str = line[19:21].strip()
        jpi_str = line[22:39].strip()
        
        if e_str:
            l_rec = {
                'E': e_str,
                'DE': de_str,
                'Jpi': jpi_str,
                'line_num': line_idx + 1,
                'g_recs': []
            }
            l_recs.append(l_rec)
            current_parent = len(l_recs) - 1
            last_data_rec_idx = line_idx
    
    elif rec_type == 'G':
        # G-record
        e_str = line[9:19].strip()
        de_str = line[19:21].strip()
        ri_str = line[22:29].strip()
        dri_str = line[29:31].strip()
        mult_str = line[32:41].strip()
        
        if e_str and current_parent is not None:
            g_rec = {
                'E': e_str,
                'DE': de_str,
                'RI': ri_str,
                'DRI': dri_str,
                'M': mult_str,
                'line_num': line_idx + 1,
                'comments': []
            }
            l_recs[current_parent]['g_recs'].append(g_rec)
            g_recs.append(g_rec)
            last_data_rec_idx = line_idx

print(f"✓ Parsed {len(l_recs)} L-records (levels)")
print(f"✓ Parsed {len(g_recs)} G-records (gammas)")

# Count comments
total_comments = sum(len(g['comments']) for g in g_recs)
print(f"✓ Found {total_comments} G-record comment lines")

# ==============================================================================
# MATCH AND COMPARE
# ==============================================================================
print("STEP 3: Match & Compare")

mismatches = []
matched_count = 0

for md in md_trans:
    # Find matching L-record
    l_match = None
    for l in l_recs:
        try:
            if abs(float(l['E']) - float(md['E_i'])) < 0.1:
                # Check Jπ - handle multiple values and substrings
                md_jpi = md['Jpi_i'].strip()
                l_jpi = l['Jpi'].split(',')[0].strip()
                if md_jpi == l_jpi or md_jpi in l['Jpi']:
                    l_match = l
                    break
        except:
            pass
    
    if not l_match:
        mismatches.append({
            'type': 'MISSING_LEVEL',
            'Eg': md['Eg'],
            'E_i': md['E_i'],
            'Jpi_i': md['Jpi_i'],
            'detail': f"No L-record for E={md['E_i']}, Jπ={md['Jpi_i']}"
        })
        continue
    
    # Find matching G-record
    g_match = None
    for g in l_match['g_recs']:
        try:
            if abs(float(g['E']) - float(md['Eg'])) < 0.1:
                g_match = g
                break
        except:
            pass
    
    if not g_match:
        mismatches.append({
            'type': 'MISSING_GAMMA',
            'Eg': md['Eg'],
            'E_i': md['E_i'],
            'Jpi_i': md['Jpi_i'],
            'detail': f"No G-record Eγ={md['Eg']} in level E={md['E_i']}"
        })
        continue
    
    matched_count += 1
    
    # ====================================================================
    # COMPARE MATCHED RECORDS
    # ====================================================================
    
    # 1. Multipolarity
    md_m = md['Multipolarity'].strip()
    ens_m = g_match['M'].strip()
    if md_m and ens_m and md_m != ens_m:
        mismatches.append({
            'type': 'MULTIPOLARITY_MISMATCH',
            'Eg': md['Eg'],
            'E_i': md['E_i'],
            'source': md_m,
            'target': ens_m,
            'line_num': g_match['line_num']
        })
    
    # 2. Iγ (RI)
    if md['Ig']:
        try:
            md_ig = float(md['Ig'])
            ens_ri = float(g_match['RI'])
            tol = max(abs(md_ig) * 0.10, 0.05)
            if abs(ens_ri - md_ig) > tol:
                mismatches.append({
                    'type': 'VALUE_MISMATCH',
                    'field': 'Iγ',
                    'Eg': md['Eg'],
                    'E_i': md['E_i'],
                    'source': f"{md['Ig']}({md['Ig_unc']})",
                    'target': f"{g_match['RI']}({g_match['DRI']})",
                    'line_num': g_match['line_num']
                })
        except:
            pass
    
    # 3. R_DCO in comments
    if md['Rdco'] and g_match['comments']:
        for cg_line in g_match['comments']:
            m_rdco = re.search(r'R\{-DCO\}[^=]*=\s*([\d.+-]+)\s*\{I(\d+)\}', cg_line)
            if m_rdco:
                cg_rdco_val = m_rdco.group(1).strip()
                cg_rdco_unc = m_rdco.group(2).strip()
                if cg_rdco_val != md['Rdco']:
                    mismatches.append({
                        'type': 'RDCO_MISMATCH',
                        'Eg': md['Eg'],
                        'E_i': md['E_i'],
                        'source': f"{md['Rdco']}({md['Rdco_unc']})",
                        'target': f"{cg_rdco_val}({cg_rdco_unc})",
                        'comment': cg_line[:60]
                    })
                break
    
    # 4. POL in comments
    if md['Pdco'] and g_match['comments']:
        for cg_line in g_match['comments']:
            m_pol = re.search(r'POL\s*=\s*([+-][\d.]+)\s*\{I(\d+)\}', cg_line)
            if m_pol:
                cg_pol_val = m_pol.group(1).strip()
                cg_pol_unc = m_pol.group(2).strip()
                if cg_pol_val != md['Pdco']:
                    mismatches.append({
                        'type': 'POL_MISMATCH',
                        'Eg': md['Eg'],
                        'E_i': md['E_i'],
                        'source': f"{md['Pdco']}({md['Pdco_unc']})",
                        'target': f"{cg_pol_val}({cg_pol_unc})",
                        'comment': cg_line[:60]
                    })
                break

# ==============================================================================
# REPORT
# ==============================================================================
print(f"\n{'=' * 100}")
print("RESULTS SUMMARY")
print(f"{'=' * 100}")

print(f"\nMarkdown table entries: {len(md_trans)}")
print(f"ENSDF L-records: {len(l_recs)}")
print(f"ENSDF G-records: {len(g_recs)}")
print(f"Successful matches: {matched_count}/{len(md_trans)}")
print(f"\nTotal mismatches: {len(mismatches)}")

mtype_counts = defaultdict(int)
for m in mismatches:
    mtype_counts[m['type']] += 1

if mtype_counts:
    print("\nMismatch breakdown:")
    for mtype in sorted(mtype_counts.keys()):
        print(f"  {mtype}: {mtype_counts[mtype]}")

if mismatches:
    print(f"\n{'=' * 100}")
    print("DETAILED MISMATCH LIST")
    print(f"{'=' * 100}")
    
    for i, m in enumerate(mismatches[:50], 1):
        print(f"\n{i:3d}. [{m['type']}]")
        print(f"     Eγ={m['Eg']} keV, E_i={m['E_i']} keV")
        if 'Jpi_i' in m:
            print(f"     Jπ_i={m.get('Jpi_i', '?')}")
        if 'detail' in m:
            print(f"     {m['detail']}")
        if 'field' in m:
            print(f"     {m['field']}: {m.get('source', '?')} vs {m.get('target', '?')}")
        if 'source' in m and 'field' not in m:
            print(f"     {m.get('source', '?')} vs {m.get('target', '?')}")
        if 'comment' in m:
            print(f"     Comment: {m['comment']}")

print(f"\n{'=' * 100}")
print("END OF REPORT")
print(f"{'=' * 100}")
