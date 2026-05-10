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
print("Source: 2026BAAA_CR11022_209Po_original_Table_I.md")
print("Target: 2026BAAA_CR11022_209Po.ens")
print("=" * 100)

# ==============================================================================
# PARSE MARKDOWN TABLE
# ==============================================================================
print("\n" + "=" * 100)
print("STEP 1: Parse Markdown Table")
print("=" * 100)

md_trans = []
for line_num, line in enumerate(md_lines, 1):
    # Skip non-data lines
    if not line.startswith('|'):
        continue
    if '---' in line or 'Eγ' in line:
        continue
    
    # Split by pipe
    parts = [p.strip() for p in line.split('|')[1:-1]]
    if len(parts) < 7:
        continue
    
    try:
        eg_raw = parts[0]         # "54.7(3)"
        jpi_raw = parts[1]         # "$17/2- \to 13/2-$"
        ei_raw = parts[2]          # "1472.6(2)"
        ig_raw = parts[3]          # "–" or "0.28(1)"
        rdco_raw = parts[4]        # "–" or "1.01(2)"
        pdco_raw = parts[5]        # "–" or "0.12(1)"
        mult_raw = parts[6]        # "E2" or "M1+E2"
        
        # Parse Eγ: "54.7(3)" → ("54.7", "3")
        m_eg = re.match(r'^([\d.]+)\((\d+)\)$', eg_raw)
        if not m_eg:
            continue
        eg_val, eg_unc = m_eg.groups()
        
        # Parse E_i: "1472.6(2)" → ("1472.6", "2")
        m_ei = re.match(r'^([\d.]+)\((\d+)\)$', ei_raw)
        if not m_ei:
            continue
        ei_val, ei_unc = m_ei.groups()
        
        # Parse Jπ: "$17/2- \to 13/2-$" → ("17/2-", "13/2-")
        jpi_clean = jpi_raw.replace('$', '').strip()
        if ' \\to ' in jpi_clean:
            jpi_parts = jpi_clean.split(' \\to ')
            jpi_i = jpi_parts[0].strip()
            jpi_f = jpi_parts[1].strip() if len(jpi_parts) > 1 else ''
        else:
            jpi_i = jpi_clean
            jpi_f = ''
        
        # Parse Iγ
        ig_val = ig_unc = None
        if ig_raw != '–':
            m_ig = re.match(r'^([\d.]+)\((\d+)\)$', ig_raw)
            if m_ig:
                ig_val, ig_unc = m_ig.groups()
        
        # Parse R_DCO: "1.01(2)" or "–"
        rdco_val = rdco_unc = None
        if rdco_raw != '–':
            m_rdco = re.match(r'^([\d.+-]+)\((\d+)\)$', rdco_raw)
            if m_rdco:
                rdco_val, rdco_unc = m_rdco.groups()
        
        # Parse POL (ΔP_DCO): "+0.12(1)" or "–"
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
    except Exception as e:
        pass

print(f"Parsed {len(md_trans)} gamma transitions from markdown table")
if md_trans:
    print("\nFirst 3 transitions:")
    for i, t in enumerate(md_trans[:3]):
        print(f"  {i+1}. Eγ={t['Eg']}({t['Eg_unc']}) keV, E_i={t['E_i']}({t['E_i_unc']}) keV")
        print(f"     Jπ: {t['Jpi_i']} → {t['Jpi_f']}")
        print(f"     Iγ={t['Ig']}({t['Ig_unc']}), M={t['Multipolarity']}")
        print(f"     R_DCO={t['Rdco']}({t['Rdco_unc']}), POL={t['Pdco']}({t['Pdco_unc']})")

# ==============================================================================
# PARSE ENSDF FILE
# ==============================================================================
print("\n" + "=" * 100)
print("STEP 2: Parse ENSDF File (starting from PN line)")
print("=" * 100)

# Find PN line (marks start of actual data)
pn_idx = None
for idx, line in enumerate(ens_lines):
    if ' PN' in line or line.strip().startswith('209PO PN'):
        pn_idx = idx
        break

if pn_idx is None:
    print("ERROR: PN line not found")
else:
    print(f"Found PN line at line {pn_idx + 1}")

# Parse L and G records starting from PN
l_recs = []
g_recs = []
current_parent = None

for line_idx in range(pn_idx if pn_idx else 0, len(ens_lines)):
    line = ens_lines[line_idx]
    
    if len(line) < 9:
        continue
    
    nucid = line[0:5].strip()
    if nucid != '209PO' and nucid != '209Po':
        continue
    
    cont = line[5]
    space1 = line[6]
    rec_type = line[7]
    
    if rec_type == 'L':
        # L-record
        e_str = line[9:19].strip()
        de_str = line[19:21].strip()
        jpi_str = line[22:39].strip()
        
        if e_str:
            l_recs.append({
                'E': e_str,
                'DE': de_str,
                'Jpi': jpi_str,
                'line_num': line_idx + 1,
                'g_recs': []
            })
            current_parent = len(l_recs) - 1
    
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
    
    elif rec_type == 'c':
        # Comment line - attach to last G-record
        if g_recs:
            g_recs[-1]['comments'].append(line.rstrip())

print(f"Parsed {len(l_recs)} L-records (levels)")
print(f"Parsed {len(g_recs)} G-records (gammas)")
print(f"Found {sum(len(g['comments']) for g in g_recs)} G-record comment lines")

if l_recs:
    print("\nFirst 3 L-records:")
    for i, l in enumerate(l_recs[:3]):
        print(f"  {i+1}. E={l['E']:>10}, DE={l['DE']:>3}, Jπ={l['Jpi']:<12} | {len(l['g_recs'])} gammas")

if g_recs:
    print("\nFirst 3 G-records:")
    for i, g in enumerate(g_recs[:3]):
        print(f"  {i+1}. Eγ={g['E']:>10}, RI={g['RI']:>10}, M={g['M']:<12} | {len(g['comments'])} comments")

# ==============================================================================
# MATCH AND COMPARE
# ==============================================================================
print("\n" + "=" * 100)
print("STEP 3: Match & Compare")
print("=" * 100)

mismatches = []

# Iterate markdown transitions
for md in md_trans:
    # Find matching L-record
    l_match = None
    for l in l_recs:
        try:
            if abs(float(l['E']) - float(md['E_i'])) < 0.1:
                # Check if Jπ matches
                md_jpi_clean = md['Jpi_i'].strip()
                l_jpi_clean = l['Jpi'].split(',')[0].strip()  # Use first Jπ if multiple
                if md_jpi_clean == l_jpi_clean or md_jpi_clean in l['Jpi']:
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
            'detail': f"No L-record found for E={md['E_i']}, Jπ={md['Jpi_i']}"
        })
        continue
    
    # Find matching G-record within this level
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
            'detail': f"No G-record Eγ={md['Eg']} found in level E={md['E_i']}"
        })
        continue
    
    # ====================================================================
    # Matched: Now compare field values
    # ====================================================================
    
    # 1. Compare Eγ value
    try:
        g_eg = float(g_match['E'])
        md_eg = float(md['Eg'])
        if abs(g_eg - md_eg) > 0.01:
            mismatches.append({
                'type': 'VALUE_MISMATCH',
                'field': 'Eγ',
                'Eg': md['Eg'],
                'E_i': md['E_i'],
                'source': f"{md['Eg']}({md['Eg_unc']})",
                'target': f"{g_match['E']}({g_match['DE']})",
                'line_num': g_match['line_num']
            })
    except:
        pass
    
    # 2. Compare Iγ (RI)
    if md['Ig']:
        try:
            md_ig = float(md['Ig'])
            ens_ri = float(g_match['RI'])
            # 10% relative tolerance
            tol = max(abs(md_ig) * 0.10, 0.05)
            if abs(ens_ri - md_ig) > tol:
                mismatches.append({
                    'type': 'VALUE_MISMATCH',
                    'field': 'Iγ (RI)',
                    'Eg': md['Eg'],
                    'E_i': md['E_i'],
                    'source': f"{md['Ig']}({md['Ig_unc']})",
                    'target': f"{g_match['RI']}({g_match['DRI']})",
                    'line_num': g_match['line_num']
                })
        except:
            pass
    
    # 3. Compare Multipolarity
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
    
    # 4. Compare R_DCO in comments
    if md['Rdco'] and g_match['comments']:
        for cg in g_match['comments']:
            # Pattern: R{-DCO}(Q)=1.01 {I2}
            m_rdco = re.search(r'R\{-DCO\}[^=]*=\s*([\d.+-]+)\s*\{I(\d+)\}', cg)
            if m_rdco:
                cg_rdco_val = m_rdco.group(1).strip()
                cg_rdco_unc = m_rdco.group(2).strip()
                if cg_rdco_val != md['Rdco']:
                    mismatches.append({
                        'type': 'COMMENT_VALUE_MISMATCH',
                        'field': 'R_DCO',
                        'Eg': md['Eg'],
                        'E_i': md['E_i'],
                        'source': f"{md['Rdco']}({md['Rdco_unc']})",
                        'target': f"{cg_rdco_val}({cg_rdco_unc})",
                        'comment_excerpt': cg[:60]
                    })
                break
    
    # 5. Compare POL in comments
    if md['Pdco'] and g_match['comments']:
        for cg in g_match['comments']:
            # Pattern: POL=+0.12 {I1}
            m_pol = re.search(r'POL\s*=\s*([+-][\d.]+)\s*\{I(\d+)\}', cg)
            if m_pol:
                cg_pol_val = m_pol.group(1).strip()
                cg_pol_unc = m_pol.group(2).strip()
                if cg_pol_val != md['Pdco']:
                    mismatches.append({
                        'type': 'COMMENT_VALUE_MISMATCH',
                        'field': 'POL',
                        'Eg': md['Eg'],
                        'E_i': md['E_i'],
                        'source': f"{md['Pdco']}({md['Pdco_unc']})",
                        'target': f"{cg_pol_val}({cg_pol_unc})",
                        'comment_excerpt': cg[:60]
                    })
                break

# ==============================================================================
# REPORT
# ==============================================================================
print(f"\nTotal mismatches found: {len(mismatches)}")

mtype_counts = defaultdict(int)
for m in mismatches:
    mtype_counts[m['type']] += 1

print("\nMismatch counts by type:")
for mtype in sorted(mtype_counts.keys()):
    print(f"  {mtype}: {mtype_counts[mtype]}")

if mismatches:
    print("\n" + "=" * 100)
    print("DETAILED MISMATCH LIST (first 30)")
    print("=" * 100)
    
    for i, m in enumerate(mismatches[:30], 1):
        print(f"\n{i}. [{m['type']}]")
        print(f"   Eγ={m['Eg']} keV, E_i={m['E_i']} keV, Jπ_i={m.get('Jpi_i', '?')}")
        if 'field' in m:
            print(f"   Field: {m['field']}")
            print(f"     Source (MD):  {m.get('source', '?')}")
            print(f"     Target (ENS): {m.get('target', '?')}")
        if 'detail' in m:
            print(f"   {m['detail']}")
        if 'line_num' in m:
            print(f"   ENS line: {m['line_num']}")
        if 'comment_excerpt' in m:
            print(f"   Comment: {m['comment_excerpt']}")

print("\n" + "=" * 100)
print(f"Total markdown transitions checked: {len(md_trans)}")
print(f"Total ENSDF L-records: {len(l_recs)}")
print(f"Total ENSDF G-records: {len(g_recs)}")
print("=" * 100)
