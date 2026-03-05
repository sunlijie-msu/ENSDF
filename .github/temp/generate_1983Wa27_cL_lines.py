#!/usr/bin/env python3
"""
Process 1983Wa27 resonance strength data and create ENSDF mapping
"""

import re

# Data from user (39 entries after excluding c) entries)
data_table = [
    (447, 0.4, 0.1),
    (507.6, 0.7, 0.2),
    (546, 0.7, 0.3),
    (639, 0.06, 0.03),
    (662, 0.4, 0.2),
    (683, 0.4, 0.2),
    (731.4, 0.5, 0.2),
    (777, 0.5, 0.2),
    (822, 0.8, 0.2),
    (914, 0.4, 0.2),
    (976, 1.0, 0.3),
    (1023, 0.7, 0.2),
    (1029, 1.1, 0.3),
    (1057, 1.8, 0.5),
    #(1069.7, 3.6, 0.5),  # SKIP c)
    (1097, 1.4, 0.3),
    (1118.5, 1.2, 0.3),
    (1158, 0.4, 0.2),
    (1165, 3.3, 0.7),
    (1215, 2.2, 0.9),
    (1264.4, 2.7, 0.6),
    (1347.3, 0.9, 0.3),
    (1386, 0.6, 0.3),
    (1448, 1.4, 0.4),
    (1477, 0.7, 0.3),
    (1528, 0.4, 0.1),
    #(1543.6, 3.8, 0.6),  # SKIP c)
    (1629.4, 1.0, 0.4),
    (1644, 0.7, 0.3),
    (1698, 0.2, 0.1),
    (1706, 4.8, 1.0),
    (1738, 0.4, 0.1),
    (1762, 2.1, 0.5),
    (1752, 4.7, 2.0),
    (1780.7, 0.4, 0.2),
    (1798.1, 2.9, 1.0),
    (1812.3, 2.4, 0.6),
    #(1829, 11, 2),        # SKIP c)
    (1843, 0.8, 0.3),
    #(1974.4, 8, 2),       # SKIP c)
    (1997, 1.7, 0.4),
]

def get_uncertainty_notation(wg_val, wg_unc):
    """
    Convert uncertainty to {In} notation for comment lines
    
    For comment lines: {In} where n is the uncertainty in the last digit
    - 1 decimal place: 0.4 ± 0.1 → {I1} (uncertainty is 1 in the last digit)
    - 1 decimal place: 0.4 ± 0.2 → {I2}
    - 1 decimal place: 3.6 ± 0.5 → {I5}
    """
    # Check if value has 1 decimal place
    val_str = f"{wg_val:.1f}"
    if '.' in val_str:
        decimal_places = len(val_str.split('.')[1])
        if decimal_places == 1:
            # Uncertainty in last digit (ones place for 1 decimal)
            unc_int = round(wg_unc * 10)
            return val_str, unc_int
    
    # For 2+ decimals or special cases
    val_str = str(wg_val)
    if '.' in val_str:
        parts = val_str.split('.')
        decimal_places = len(parts[1])
        # Shift uncertainty by 10^decimal_places
        unc_int = round(wg_unc * (10 ** decimal_places))
        return val_str, unc_int
    else:
        # No decimal
        unc_int = round(wg_unc)
        return str(int(wg_val)), unc_int

print("=" * 80)
print("1983Wa27 RESONANCE STRENGTH DATA - CORRECTED UNCERTAINTY NOTATION")
print("=" * 80)
print()

for ep, wg_val, wg_unc in data_table:
    val_str, unc_int = get_uncertainty_notation(wg_val, wg_unc)
    cL_line = f" 34CL  cL $ |w|g={val_str} {{I{unc_int}}} (1983Wa27)"
    
    print(f"Ep={ep:8.1f} keV:  |w|g={wg_val:.2f}±{wg_unc:.2f}")
    print(f"  Format: {cL_line}")
    print()
