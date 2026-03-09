#!/usr/bin/env python3
"""
Verify DRI (Relative Intensity Uncertainty) values added by GPT 5.4.

Rule:
- Weak transitions (RI <= 5.0): ~50% uncertainty
- Strong transitions (RI > 5.0): ~10% uncertainty

Expected DRI encoding:
- For RI with n decimal places, DRI = int(round(0.5 or 0.1 * RI * 10^n))
"""

import re
from decimal import Decimal, ROUND_HALF_UP

def round_half_up_decimal(value, quantum):
    """Round to nearest quantum using ROUND_HALF_UP."""
    return (value / quantum).quantize(Decimal('1'), rounding=ROUND_HALF_UP) * quantum

def compute_expected_dri(ri_text, dri_text):
    """Compute expected DRI based on RI value and rule."""
    if dri_text in {'LT', 'GT'}:
        return dri_text, 'LT/GT marker (preserve)'
    
    try:
        ri = Decimal(ri_text.strip())
    except:
        return dri_text, f'ERROR: unparseable RI={ri_text}'
    
    # Determine weak/strong threshol
    threshold = Decimal('5')
    use_percent = Decimal('0.5') if ri <= threshold else Decimal('0.1')
    
    # Compute uncertainty
    uncertainty = ri * use_percent
    
    # Determine decimal places in RI
    decimals = 0
    if '.' in ri_text:
        decimals = len(ri_text.strip().split('.')[1])
    
    # Compute quantum (10^-decimals)
    if decimals == 0:
        quantum_str = '1'
    else:
        quantum_str = '0.' + ('0' * (decimals - 1)) + '1'
    
    quantum = Decimal(quantum_str)
    
    # Round to quantum
    rounded = round_half_up_decimal(uncertainty, quantum)
    
    # Compute DRI digits
    scale = 10 ** decimals
    dri_digits = int((rounded * scale).to_integral_value(rounding=ROUND_HALF_UP))
    
    expected_dri = str(dri_digits)
    
    rule_type = 'WEAK (50%)' if ri <= threshold else 'STRONG (10%)'
    
    return expected_dri, rule_type

def main():
    filename = r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02.ens'
    
    mismatches = []
    total_checked = 0
    weak_count = 0
    strong_count = 0
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    unbound_started = False
    for lineno, line in enumerate(lines, 1):
        # Detect start of unbound block
        if '34CL  L 6134' in line:
            unbound_started = True
        
        if not unbound_started:
            continue
        
        # Stop at end of file or next header
        if line.strip() and not line.startswith(' 34CL'):
            break
        
        # Parse G-records only
        if len(line) > 8 and line[7] == 'G':
            # Extract fields
            ri_field = line[22:29].strip()   # Columns 23-29 (0-indexed: 22-29)
            dri_field = line[29:31].strip()  # Columns 30-31 (0-indexed: 29-31)
            
            if not ri_field:
                continue
            
            total_checked += 1
            
            # Check if numeric DRI (not LT/GT)
            if dri_field and dri_field not in {'LT', 'GT'}:
                expected, rule = compute_expected_dri(ri_field, dri_field)
                
                if rule != 'LT/GT marker (preserve)':
                    ri_val = Decimal(ri_field.strip())
                    if ri_val <= Decimal('5'):
                        weak_count += 1
                    else:
                        strong_count += 1
                    
                    if expected != dri_field:
                        mismatches.append({
                            'line': lineno,
                            'ri': ri_field,
                            'dri_actual': dri_field,
                            'dri_expected': expected,
                            'rule': rule
                        })
    
    print("=" * 80)
    print("DRI VERIFICATION REPORT FOR UNBOUND BLOCK (34CL L 6134 - 7079)")
    print("=" * 80)
    print(f"\nTotal numeric G-records checked: {total_checked}")
    print(f"Weak transitions (RI <= 5.0, 50% rule): {weak_count}")
    print(f"Strong transitions (RI > 5.0, 10% rule): {strong_count}")
    print(f"\nMismatches found: {len(mismatches)}")
    
    if mismatches:
        print("\n" + "=" * 80)
        print("MISMATCHES (DRI value does not match expected value):")
        print("=" * 80)
        for m in mismatches[:20]:  # Show first 20
            print(f"\nLine {m['line']}: RI={m['ri']} DRI_actual={m['dri_actual']} DRI_expected={m['dri_expected']} [{m['rule']}]")
        
        if len(mismatches) > 20:
            print(f"\n... and {len(mismatches) - 20} more mismatches")
    else:
        print("\n✓ ALL DRI VALUES MATCH EXPECTED VALUES")
    
    print("\n" + "=" * 80)

if __name__ == '__main__':
    main()
