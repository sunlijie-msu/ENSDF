"""Cross-check B(E2) values from ruler.rpt vs Table II markdown"""
import re

with open(r'D:\X\ND\Files\ruler.rpt', 'r', encoding='utf-8') as f:
    rpt = f.read()

# Table II data: (Eg, B(E2), +unc, -unc, is_limit, band_name)
md_data = [
    (486.7, 0.46, 0.04, 0.04, False, 'QB1'),
    (792.4, 0.30, 0.02, 0.02, False, 'QB1'),
    (1044.0, 0.22, 0.02, 0.02, False, 'QB1'),
    (1239.5, 0.09, 0.01, 0.01, False, 'QB1'),
    (1468.0, 0.02, 0, 0, True, 'QB1'),
    (1205.2, 0.05, 0, 0, True, 'QB1'),
    (457.2, 0.48, 0.08, 0.07, False, 'QB2'),
    (748.2, 0.47, 0.04, 0.04, False, 'QB2'),
    (841.4, 0.42, 0.05, 0.05, False, 'QB2'),
    (938.3, 0.35, 0.03, 0.03, False, 'QB2'),
    (1040.2, 0.26, 0.03, 0.02, False, 'QB2'),
    (1164.1, 0.17, 0, 0, True, 'QB2'),
    (679.9, 0.25, 0.04, 0.03, False, 'QB3'),
    (783.7, 0.27, 0.04, 0.03, False, 'QB3'),
    (918.8, 0.26, 0.03, 0.03, False, 'QB3'),
    (1108.5, 0.24, 0.03, 0.03, False, 'QB3'),
    (1328.4, 0.20, 0, 0, True, 'QB3'),
]

sections = re.split(r'--->gamma#', rpt)
print(f'{"Eg":>8} {"Band":>4} {"MD_BE2":>14} {"Ruler_BE2DOWN":>22} {"Match":>10}')
print('-' * 82)

for sec in sections[1:]:
    eg_m = re.search(r'EG=([\d.]+)', sec)
    if not eg_m:
        continue
    eg = float(eg_m.group(1))

    md_match = None
    for md in md_data:
        if abs(md[0] - eg) < 0.5:
            md_match = md
            break
    if not md_match:
        continue

    src_v, src_p, src_m, is_lim, band = md_match

    # Find MINIMUM and MAXIMUM section
    idx2 = sec.find('MINIMUM and MAXIMUM')
    if idx2 < 0:
        idx2 = sec.find('<2>')
    if idx2 < 0:
        continue

    mm_text = sec[idx2:]
    end_idx = mm_text.find('<3>')
    if end_idx > 0:
        mm_text = mm_text[:end_idx]

    if is_lim:
        # Find GT or > value
        gt_m = re.search(r'BE2\(DOWN\)\s*>\s*([\d.]+)', mm_text)
        if not gt_m:
            gt_m = re.search(r'BE2\(DOWN\)\s*>\s*([\d.]+)', sec)
        if gt_m:
            gt_val = float(gt_m.group(1))
            flag = 'OK' if gt_val > src_v * 0.9 else 'LIMIT_LOWER'
            print(f'{eg:>8.1f} {band:>4} {"GT"+str(src_v):<14} {"GT"+str(gt_val):<22} {flag:>10}')
        else:
            print(f'{eg:>8.1f} {band:>4} {"GT"+str(src_v):<14} {"NOT FOUND":<22}')
        continue

    # Extract BE2(DOWN) with uncertainties
    be2down = re.search(r'BE2\(DOWN\)\s*=\s*([\d.]+)\s+([+-]\d+)\s*([+-]\d+)?', mm_text)
    if not be2down:
        be2down = re.search(r'BE2\(DOWN\)\s*=\s*([\d.]+)\s+([+-]\d+)\s*([+-]\d+)?', sec)
    if not be2down:
        print(f'{eg:>8.1f} {band:>4} {src_v:<14} {"NOT FOUND":<22}')
        continue

    v_str = be2down.group(1)
    d_plus_str = be2down.group(2)
    d_minus_str = be2down.group(3) if be2down.lastindex and be2down.lastindex >= 3 else d_plus_str
    if d_minus_str is None:
        d_minus_str = d_plus_str

    v = float(v_str)
    d_plus = int(d_plus_str)
    d_minus = int(d_minus_str)

    # Count decimal places from raw string
    ndec = len(v_str.split('.')[1]) if '.' in v_str else 0
    d_plus_abs = abs(d_plus) * 10**(-ndec)
    d_minus_abs = abs(d_minus) * 10**(-ndec)

    # Compare ranges
    src_lo = src_v - src_m
    src_hi = src_v + src_p
    ruler_lo = v - d_minus_abs
    ruler_hi = v + d_plus_abs

    overlap = not (src_hi < ruler_lo or src_lo > ruler_hi)

    flag = 'OK' if overlap else 'MISMATCH'
    print(f'{eg:>8.1f} {band:>4} {src_v}+{src_p}-{src_m:<7} {v:.4f}+{d_plus_abs:.4f}-{d_minus_abs:.4f} {flag:>10}')

print()
print("Note: MINIMUM and MAXIMUM method used per user request.")
