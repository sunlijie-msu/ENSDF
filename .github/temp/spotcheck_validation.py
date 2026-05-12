#!/usr/bin/env python3
"""
Spot-check validation: 15% random sample of updated table rows.
"""

import random
import re
from typing import Optional, Tuple

def extract_j_value(jpi_str: str) -> Optional[float]:
    jpi_clean = jpi_str.strip().replace('$', '').replace('(', '').replace(')', '').replace(' ', '')
    match = re.match(r'(\d+)/(\d+)', jpi_clean)
    if match:
        num, denom = int(match.group(1)), int(match.group(2))
        return num / denom
    return None

def calc_delta_j(jpi_i: str, jpi_f: str) -> Optional[float]:
    ji = extract_j_value(jpi_i)
    jf = extract_j_value(jpi_f)
    if ji is not None and jf is not None:
        return abs(ji - jf)
    return None

def extract_rdco_and_gate(rdco_str: str) -> Tuple[Optional[float], Optional[str]]:
    if '–' in rdco_str or not rdco_str.strip():
        return None, None
    match = re.search(r'([\d.]+)', rdco_str)
    if match:
        value = float(match.group(1))
        gate = 'd' if '[d]' in rdco_str else ('q' if '[q]' in rdco_str else None)
        return value, gate
    return None, None

def extract_pol(pol_str: str) -> Optional[float]:
    if '–' in pol_str or not pol_str.strip():
        return None
    match = re.search(r'(-?[\d.]+)', pol_str)
    if match:
        return float(match.group(1))
    return None

def classify_dco_expected(rdco_val: Optional[float], gate: Optional[str], dj: Optional[float], 
                         ji: Optional[float], jf: Optional[float]) -> str:
    """
    Reimplement expected DCO classification with correct thresholds.
    
    From 2026BaAA comment:
    - R_DCO(Q)≈1.0 for stretched quadrupole (ΔJ=2) or unstretched dipole (ΔJ=0)
    - R_DCO(Q)≈0.76 for stretched dipole (ΔJ=1)
    - R_DCO(D)≈1.0 for stretched dipole (ΔJ=1)
    - R_DCO(D)≈1.33 for stretched quadrupole (ΔJ=2) or unstretched dipole (ΔJ=0)
    """
    if rdco_val is None:
        return "–"
    if ji is not None and jf is not None and abs(ji - jf) < 0.01:
        return "ΔJ=0"
    
    if gate == 'q':  # Gate on stretched quadrupole
        if 0.90 <= rdco_val <= 1.10:  # ~1.0
            return "Q"
        elif 0.68 <= rdco_val <= 0.84:  # ~0.76
            return "D"
        else:
            return "Mixed"
    elif gate == 'd':  # Gate on stretched dipole
        if 0.90 <= rdco_val <= 1.10:  # ~1.0
            return "D"
        elif 1.20 <= rdco_val <= 1.50:  # ~1.33
            return "Q"
        else:
            return "Mixed"
    
    return "Mixed"

# Read the updated table
with open(r'd:\X\ND\ENSDF\XUNDL\2026BAAA_CR11022_209Po_original_Table_I.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find data rows (skip header, title, separator)
data_rows = []
for i, line in enumerate(lines):
    if i > 2 and line.strip().startswith('|') and '–' not in line.split('|')[1][:1]:
        data_rows.append((i, line.strip()))

# Sample 15% of rows
sample_size = max(1, len(data_rows) // 7)  # ~15% for ~120 rows = ~17 rows
random.seed(42)  # Deterministic for reproducibility
sample_indices = sorted(random.sample(range(len(data_rows)), sample_size))

print(f"Total data rows: {len(data_rows)}")
print(f"Sample size (15%): {sample_size}")
print(f"\nSpot-check validation results:")
print("=" * 150)
print(f"{'Line':<5} | {'E_γ':<8} | {'R_DCO':<12} | {'POL':<8} | {'DCO Expected':<12} | {'DCO Actual':<12} | {'Status':<10}")
print("-" * 150)

errors = 0
for sample_idx in sample_indices:
    line_num, line = data_rows[sample_idx]
    
    # Parse row
    parts = [p.strip() for p in line.split('|')[1:-1]]
    if len(parts) < 9:
        continue
    
    eg = parts[0]
    jpis = parts[1]
    rdco_str = parts[4]
    pol_str = parts[5]
    dco_actual = parts[7]
    
    # Extract data
    if '\\to' in jpis:
        ji_str, jf_str = jpis.split('\\to')
    else:
        ji_str = jf_str = jpis
    
    ji = extract_j_value(ji_str)
    jf = extract_j_value(jf_str)
    dj = calc_delta_j(ji_str, jf_str)
    rdco_val, gate = extract_rdco_and_gate(rdco_str)
    pol_val = extract_pol(pol_str)
    
    # Calculate expected
    dco_expected = classify_dco_expected(rdco_val, gate, dj, ji, jf)
    
    # Check match
    status = "✓ PASS" if dco_expected == dco_actual else "✗ FAIL"
    if dco_expected != dco_actual:
        errors += 1
    
    rdco_display = f"{rdco_val} [{gate}]" if rdco_val else "–"
    pol_display = f"{pol_val:.2f}" if pol_val else "–"
    
    print(f"{line_num:<5} | {eg:<8} | {rdco_display:<12} | {pol_display:<8} | {dco_expected:<12} | {dco_actual:<12} | {status:<10}")

print("=" * 150)
print(f"\nValidation Summary:")
print(f"  Rows checked: {sample_size}")
print(f"  Errors found: {errors}")
if errors == 0:
    print(f"  Status: ✓ All spot checks PASSED - DCO analysis is correct!")
else:
    print(f"  Status: ✗ FAILURES detected - review analysis logic")
