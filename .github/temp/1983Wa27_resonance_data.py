#!/usr/bin/env python3
"""
Extract and process 1983Wa27 resonance strength data for Cl34_33s_p_g.ens
Excludes entries with c) footnotes. Converts to ENSDF {In} uncertainty notation.
"""

import re

# Raw data from user
data = """
| 447 | 0.4 ± 0.1 |
| 507.6 ± 0.2 | 0.7 ± 0.2 |
| 546 | 0.7 ± 0.3 |
| 639 | 0.06 ± 0.03 |
| 662 | 0.4 ± 0.2 |
| 683 | 0.4 ± 0.2 |
| 731.4 ± 0.3 | 0.5 ± 0.2 |
| 777 | 0.5 ± 0.2 |
| 822 | 0.8 ± 0.2 |
| 914 | 0.4 ± 0.2 |
| 976 | 1.0 ± 0.3 |
| 1023 | 0.7 ± 0.2 |
| 1029 | 1.1 ± 0.3 |
| 1057 | 1.8 ± 0.5 |
| 1069.7 ± 0.2 | 3.6 ± 0.5 $^c$) |
| 1097 | 1.4 ± 0.3 |
| 1118.5 ± 0.3 | 1.2 ± 0.3 |
| 1158 | 0.4 ± 0.2 |
| 1165 | 3.3 ± 0.7 |
| 1215 | 2.2 ± 0.9 |
| 1264.4 ± 0.2 | 2.7 ± 0.6 |
| 1347.3 ± 0.2 | 0.9 ± 0.3 |
| 1386 | 0.6 ± 0.3 |
| 1448 | 1.4 ± 0.4 |
| 1477 | 0.7 ± 0.3 |
| 1528 | 0.4 ± 0.1 |
| 1543.6 ± 0.2 | 3.8 ± 0.6 $^c$) |
| 1629.4 ± 0.3 | 1.0 ± 0.4 |
| 1644 | 0.7 ± 0.3 |
| 1698 | 0.2 ± 0.1 |
| 1706 | 4.8 ± 1.0 |
| 1738 | 0.4 ± 0.1 |
| 1762 | 2.1 ± 0.5 |
| 1752 | 4.7 ± 2.0 |
| 1780.7 ± 0.3 | 0.4 ± 0.2 |
| 1798.1 ± 0.3 | 2.9 ± 1.0 |
| 1812.3 ± 0.3 | 2.4 ± 0.6 |
| 1829 | 11 ± 2 $^c$) |
| 1843 | 0.8 ± 0.3 |
| 1974.4 ± 0.3 | 8 ± 2 $^c$) |
| 1997 | 1.7 ± 0.4 |
"""

entries = []
for line in data.strip().split('\n'):
    if '|' not in line:
        continue
    
    # Skip lines with footnote markers
    if '$^c$)' in line or '$^c' in line.lower():
        print(f"SKIPPED (footnote): {line.strip()}")
        continue
    
    # Parse Ep and |w|g values
    parts = [p.strip().replace('|', '') for p in line.split('|')[1:-1]]
    if len(parts) >= 2:
        ep_raw = parts[0]
        wg_raw = parts[1]
        
        # Extract Ep energy (take numeric part before ±)
        ep_match = re.search(r'([\d.]+)', ep_raw)
        ep = float(ep_match.group(1)) if ep_match else None
        
        # Extract |w|g value and uncertainty
        wg_match = re.search(r'([\d.]+)\s*±\s*([\d.]+)', wg_raw)
        if wg_match and ep:
            wg_val = float(wg_match.group(1))
            wg_unc = float(wg_match.group(2))
            
            # Convert uncertainty to {In} notation
            # Determine sig figs: if leading digits < 35, use 2 digits
            if wg_val >= 0.35:
                # 1 significant figure
                unc_int = round(wg_unc / (10 ** (len(str(int(wg_val))) - 1)))
            else:
                # 2 significant figures
                # Count decimal places needed
                decimal_places = len(str(wg_val).split('.')[1]) if '.' in str(wg_val) else 0
                unc_int = round(wg_unc * (10 ** decimal_places))
            
            entries.append({
                'ep': ep,
                'wg_val': wg_val,
                'wg_unc': wg_unc,
                'unc_int': unc_int,
                'ep_raw': ep_raw,
                'wg_raw': wg_raw
            })
            print(f"OK: Ep={ep:8.1f}, |w|g={wg_val:.1f}±{wg_unc:.1f} → {{I{unc_int}}}")

# Sort by Ep
entries.sort(key=lambda x: x['ep'])

print(f"\n=== TOTAL ENTRIES TO ADD: {len(entries)} ===\n")
print("ENSDF Comment Line Format:")
print(" 34CL  cL $ |w|g=X.X {In} (1983Wa27)")
print()

for e in entries[:5]:  # Show first 5
    print(f" 34CL  cL $ |w|g={e['wg_val']:.1f} {{I{e['unc_int']}}} (1983Wa27)")
