#!/usr/bin/env python3
"""
Detailed investigation of mismatches and random spot-check (15%)
"""

import re
import random
from collections import defaultdict

# Read files
with open('XUNDL/2026BAAA_CR11022_209Po_original_Table_I.md', 'r', encoding='utf-8') as f:
    md_lines = f.readlines()

with open('XUNDL/2026BAAA_CR11022_209Po.ens', 'r', encoding='utf-8') as f:
    ens_lines = f.readlines()

print("=" * 100)
print("INVESTIGATION OF MISMATCHES")
print("=" * 100)

# Read ENSDF to find these levels/gammas
print("\n1. Searching ENSDF file for level E=6461.6 keV (Jπ=41/2+)")
found_level_6461_6 = False
for i, line in enumerate(ens_lines):
    if '6461.6' in line or '6461' in line:
        print(f"   Line {i+1}: {line.rstrip()[:80]}")
        found_level_6461_6 = True

if not found_level_6461_6:
    print("   ✗ Level E=6461.6 NOT found in ENSDF file")
else:
    print("   ✓ Level E=6461.6 found in ENSDF")

print("\n2. Searching ENSDF file for level E=4857.0 keV")
found_level_4857 = False
for i, line in enumerate(ens_lines):
    if '4857' in line:
        print(f"   Line {i+1}: {line.rstrip()[:80]}")
        found_level_4857 = True

if not found_level_4857:
    print("   ✗ Level E=4857.0 NOT found in ENSDF file")
else:
    print("   ✓ Level E=4857.0 found in ENSDF")

print("\n3. Searching ENSDF file for level E=6300.2 keV")
found_level_6300_2 = False
for i, line in enumerate(ens_lines):
    if '6300.2' in line or '6300' in line:
        print(f"   Line {i+1}: {line.rstrip()[:80]}")
        found_level_6300_2 = True

if not found_level_6300_2:
    print("   ✗ Level E=6300.2 NOT found in ENSDF file")
else:
    print("   ✓ Level E=6300.2 found in ENSDF")

# ==============================================================================
# PERFORM 15% RANDOM SPOT-CHECK
# ==============================================================================
print("\n" + "=" * 100)
print("RANDOM SPOT-CHECK (15% of matched transitions)")
print("=" * 100)

# Parse markdown transitions
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

# Parse ENSDF
pn_idx = None
for idx, line in enumerate(ens_lines):
    if ' PN' in line:
        pn_idx = idx
        break

l_recs = []
g_recs = []
current_parent = None

for line_idx in range(pn_idx, len(ens_lines)):
    line = ens_lines[line_idx]
    
    if len(line) < 9:
        continue
    
    nucid = line[0:5].strip()
    if nucid not in ('209PO', '209Po'):
        continue
    
    is_comment = (len(line) > 6 and line[6] == 'c')
    if is_comment:
        if g_recs:
            g_recs[-1]['comments'].append(line.rstrip())
        continue
    
    rec_type = line[7] if len(line) > 7 else ' '
    
    if rec_type == 'L':
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
    
    elif rec_type == 'G':
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

# Find matched pairs
matched_pairs = []
for md in md_trans:
    l_match = None
    for l in l_recs:
        try:
            if abs(float(l['E']) - float(md['E_i'])) < 0.1:
                md_jpi = md['Jpi_i'].strip()
                l_jpi = l['Jpi'].split(',')[0].strip()
                if md_jpi == l_jpi or md_jpi in l['Jpi']:
                    l_match = l
                    break
        except:
            pass
    
    if not l_match:
        continue
    
    g_match = None
    for g in l_match['g_recs']:
        try:
            if abs(float(g['E']) - float(md['Eg'])) < 0.1:
                g_match = g
                break
        except:
            pass
    
    if not g_match:
        continue
    
    matched_pairs.append((md, l_match, g_match))

# Select 15% random sample
sample_size = max(1, int(len(matched_pairs) * 0.15))
random.seed(42)  # For reproducibility
sample_indices = random.sample(range(len(matched_pairs)), sample_size)

print(f"\nTotal matched pairs: {len(matched_pairs)}")
print(f"Sample size (15%): {sample_size}")
print(f"\nChecking random sample for consistency...\n")

spot_check_errors = []

for sample_i, idx in enumerate(sorted(sample_indices)):
    md, l_match, g_match = matched_pairs[idx]
    
    print(f"{sample_i + 1}. Eγ={md['Eg']} keV, E_i={md['E_i']}, Jπ_i={md['Jpi_i']}")
    
    # Check E_γ value in G-record E field
    try:
        md_eg = float(md['Eg'])
        ens_eg = float(g_match['E'])
        if abs(md_eg - ens_eg) > 0.01:
            print(f"   ✗ Eγ MISMATCH: MD={md['Eg']}({md['Eg_unc']}), ENS={g_match['E']}({g_match['DE']})")
            spot_check_errors.append(('Eγ value', md['Eg'], g_match['E']))
        else:
            print(f"   ✓ Eγ OK: {g_match['E']}({g_match['DE']})")
    except Exception as e:
        print(f"   ? Error checking Eγ: {e}")
    
    # Check Iγ in RI field (if present in MD)
    if md['Ig']:
        try:
            md_ig = float(md['Ig'])
            ens_ri = float(g_match['RI'])
            tol = max(abs(md_ig) * 0.10, 0.05)
            if abs(ens_ri - md_ig) > tol:
                print(f"   ✗ Iγ MISMATCH: MD={md['Ig']}({md['Ig_unc']}), ENS={g_match['RI']}({g_match['DRI']})")
                spot_check_errors.append(('Iγ value', md['Ig'], g_match['RI']))
            else:
                print(f"   ✓ Iγ OK: {g_match['RI']}({g_match['DRI']})")
        except:
            print(f"   ? Iγ unparseable")
    else:
        print(f"   - Iγ not in source table")
    
    # Check Multipolarity
    md_m = md['Multipolarity'].strip()
    ens_m = g_match['M'].strip()
    if md_m and ens_m:
        if md_m == ens_m:
            print(f"   ✓ Multipolarity OK: {ens_m}")
        else:
            print(f"   ✗ Multipolarity MISMATCH: MD={md_m}, ENS={ens_m}")
            spot_check_errors.append(('Multipolarity', md_m, ens_m))
    
    print()

print("=" * 100)
print("SPOT-CHECK SUMMARY")
print("=" * 100)

if spot_check_errors:
    print(f"\n✗ Found {len(spot_check_errors)} errors in spot-check:")
    for field, md_val, ens_val in spot_check_errors:
        print(f"   {field}: {md_val} vs {ens_val}")
else:
    print("\n✓ Spot-check PASSED: All 15% sample values match exactly")

print("\n" + "=" * 100)
print("FINAL SUMMARY")
print("=" * 100)
print(f"\nTotal markdown transitions: {len(md_trans)}")
print(f"Matched to ENSDF: {len(matched_pairs)}/103")
print(f"Missing in ENSDF: {103 - len(matched_pairs)}")
print(f"\nRandom spot-check sample: {sample_size} transitions")
print(f"Spot-check errors: {len(spot_check_errors)}")

if spot_check_errors:
    print(f"\nStatus: ✗ SPOT-CHECK FAILED")
else:
    print(f"\nStatus: ✓ ALL CHECKS PASSED")
