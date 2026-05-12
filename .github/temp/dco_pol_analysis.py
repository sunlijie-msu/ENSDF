#!/usr/bin/env python3
"""
DCO and POL analysis for 209Po gamma transitions.
Applies DCO decision rules and POL multipolarity assignment.
"""

import re
from typing import Optional, Tuple

def extract_j_value(jpi_str: str) -> Optional[float]:
    """Extract J value from J-pi string like '17/2-' or '(41/2+)'"""
    jpi_clean = jpi_str.strip().replace('$', '').replace('(', '').replace(')', '')
    match = re.match(r'(\d+)/(\d+)', jpi_clean)
    if match:
        num, denom = int(match.group(1)), int(match.group(2))
        return num / denom
    return None

def extract_parity(jpi_str: str) -> Optional[str]:
    """Extract parity from J-pi string"""
    jpi_clean = jpi_str.strip().replace('$', '').replace('(', '').replace(')', '')
    if '+' in jpi_clean:
        return '+'
    elif '-' in jpi_clean:
        return '-'
    return None

def calc_delta_j(jpi_i: str, jpi_f: str) -> Optional[float]:
    """Calculate spin change |J_i - J_f|"""
    ji = extract_j_value(jpi_i)
    jf = extract_j_value(jpi_f)
    if ji is not None and jf is not None:
        return abs(ji - jf)
    return None

def extract_rdco_and_gate(rdco_str: str) -> Tuple[Optional[float], Optional[str]]:
    """Extract R_DCO value and gate type [d] or [q]"""
    if '–' in rdco_str or rdco_str.strip() == '' or rdco_str == '':
        return None, None
    match = re.search(r'([\d.]+)', rdco_str)
    if match:
        value = float(match.group(1))
        gate = None
        if '[d]' in rdco_str:
            gate = 'd'
        elif '[q]' in rdco_str:
            gate = 'q'
        return value, gate
    return None, None

def extract_pol(pol_str: str) -> Optional[float]:
    """Extract POL (polarization) value"""
    if '–' in pol_str or pol_str.strip() == '' or pol_str == '':
        return None
    match = re.search(r'(-?[\d.]+)', pol_str)
    if match:
        return float(match.group(1))
    return None

def classify_dco(rdco_val: Optional[float], gate: Optional[str], dj: Optional[float], ji: Optional[float], jf: Optional[float]) -> str:
    """
    Classify transition as D, Q, ΔJ=0, or Mixed based on DCO decision rules.
    
    Gate types:
    - 'd': gated on stretched dipole (ΔJ=1)
    - 'q': gated on stretched quadrupole (ΔJ=2)
    """
    if rdco_val is None:
        return "–"
    
    # Special case: J_i = J_f means ΔJ = 0
    if ji is not None and jf is not None and abs(ji - jf) < 0.01:
        return "ΔJ=0"
    
    if gate == 'q':  # Gate on stretched quadrupole
        # Expected values: Q~1.0, D~0.56, Mixed D+Q~0.2-1.3, Unstretched~1.0-1.8
        if 0.95 <= rdco_val <= 1.05:
            return "Q"
        elif 0.50 <= rdco_val <= 0.65:
            return "D"
        elif 0.2 <= rdco_val <= 1.3:
            return "Mixed"
        else:
            return "Mixed"
    
    elif gate == 'd':  # Gate on stretched dipole
        # Expected values: Q~1.8, D~1.0, Unstretched~1.8
        if 0.95 <= rdco_val <= 1.05:
            return "D"
        elif 1.70 <= rdco_val <= 1.90:
            return "Q"
        elif rdco_val > 1.5:
            return "Q"
        else:
            return "Mixed"
    
    return "Mixed"

def assign_multipolarity(dco_class: str, pol_val: Optional[float], dj: Optional[float]) -> str:
    """
    Assign multipolarity based on DCO classification and POL.
    
    POL sign rule:
    - Positive POL: Electric dominant (E1, E2, E3, ...)
    - Negative POL: Magnetic dominant (M1, M2, M3, ...)
    """
    if dco_class == "–":
        return "–"
    
    if pol_val is None:
        # No POL data - assign only multipolarity character from DCO
        if dco_class == "D":
            return "D"
        elif dco_class == "Q":
            return "Q"
        elif dco_class == "Mixed":
            return "D+Q" if dj is not None and (dj < 2) else "Q"
        else:
            return "D"
    
    # Apply POL to assign electromagnetic character
    is_electric = pol_val > 0
    
    if dco_class == "D":
        return "E1" if is_electric else "M1"
    elif dco_class == "Q":
        return "E2" if is_electric else "M2"
    elif dco_class == "ΔJ=0":
        # ΔJ=0 typically allows D or mixed
        return "E1" if is_electric else "M1"
    elif dco_class == "Mixed":
        if dj is not None:
            if dj == 0 or abs(dj) < 0.5:
                return "E1+M2" if is_electric else "M1+E2"
            elif dj == 1 or abs(dj - 1) < 0.5:
                return "E1+E2" if is_electric else "M1+M2"
            else:
                return "E2+E3" if is_electric else "M2+M3"
        return "D+Q"
    
    return "–"

# Test with a few transitions
test_data = [
    ("54.7(3)", "$17/2- \\to 13/2-$", "–", "–"),
    ("88.8(2)", "$31/2- \\to 31/2-$", "–", "–"),
    ("103.1(2)", "$11/2- \\to 13/2-$", "0.65(9) [q]", "–"),
    ("186.3(1)", "$31/2- \\to 29/2+$", "0.77(3) [q]", "0.07(6)"),
    ("206.2(1)", "$25/2+ \\to 23/2+$", "1.05(3) [d]", "-0.16(4)"),
]

print("E(keV) | Jπ_i → Jπ_f | ΔJ | R_DCO [gate] | POL | DCO Class | Multipolarity")
print("------|---|---|---|---|---|---")
for eg, jpis, rdco_str, pol_str in test_data:
    ji_str, jf_str = jpis.split('\\to')
    ji = extract_j_value(ji_str)
    jf = extract_j_value(jf_str)
    dj = calc_delta_j(ji_str, jf_str)
    rdco_val, gate = extract_rdco_and_gate(rdco_str)
    pol_val = extract_pol(pol_str)
    
    dco_class = classify_dco(rdco_val, gate, dj, ji, jf)
    mult = assign_multipolarity(dco_class, pol_val, dj)
    
    gate_str = f"[{gate}]" if gate else "–"
    print(f"{eg} | {jpis} | {dj:.1f} | {rdco_val} {gate_str} | {pol_val} | {dco_class} | {mult}")
