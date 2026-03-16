"""Analysis script for 1971Hy02 RI data mapping."""
with open(r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens') as f:
    lines = f.readlines()

# Build map of L-records and their associated G-records
l_blocks = {}
cur_l = None
for i, line in enumerate(lines):
    if len(line) >= 9 and line[5:9] == '  L ':
        e_str = line[9:19].strip()
        try:
            e_val = float(e_str)
            cur_l = i+1
            l_blocks[cur_l] = {'e': e_val, 'gammas': []}
        except:
            pass
    elif cur_l is not None and len(line) >= 9 and line[5:9] == '  G ':
        eg_str = line[9:19].strip()
        try:
            eg_val = float(eg_str)
            l_blocks[cur_l]['gammas'].append({'line': i+1, 'eg': eg_val})
        except:
            pass

ei_to_lline = {
    1887: 211,
    2158: 228,
    2181: 267,
    2376: 285,
    2611: 326,
    2722: 344,
    3545: 422,
    3601: 458,
    3632: 499,
    3771: 540,
    3983: 577,
    4076: 621,
    4140: 645,
    4353: 681,
    4417: 695,
    4515: 723,
    6169: 1265,
    6207: 1395,
    6229: 1458,
}

transitions = [
    (1887, 150, 1738, '40 {I4}'),
    (1887, 461, 1428, '60 {I4}'),
    (2158, 0, 2158, '13 {I3}'),
    (2158, 150, 2008, '13 {I6}'),
    (2158, 461, 1698, '67 {I6}'),
    (2158, 665, 1488, '<1'),
    (2158, 1230, 928, '7 {I4}'),
    (2181, 150, 2030, '57 {I8}'),
    (2181, 461, 1720, '28 {I5}'),
    (2181, 665, 1510, '15 {I7}'),
    (2376, 150, 2227, '100'),
    (2611, 150, 2461, '45 {I9}'),
    (2611, 665, 1941, '5 {I4}'),
    (2611, 1230, 1381, '50 {I9}'),
    (2722, 0, 2722, '13 {I3}'),
    (2722, 150, 2572, '19 {I3}'),
    (2722, 461, 2262, '47 {I4}'),
    (2722, 665, 2052, '8 {I3}'),
    (2722, 1230, 1492, '3 {I1}'),
    (2722, 1888, 832, '2 {I1}'),
    (2722, 2158, 562, '8 {I3}'),
    (3545, 150, 3395, '100'),
    (3601, 150, 3451, '48 {I5}'),
    (3601, 2376, 1221, '8 {I4}'),
    (3601, 2722, 881, '44 {I5}'),
    (3632, 150, 3482, '48 {I7}'),
    (3632, 2376, 1252, '52 {I7}'),
    (3771, 0, 3771, '100'),
    (3983, 150, 3832, '65 {I6}'),
    (3983, 2158, 1822, '26 {I5}'),
    (3983, 2722, 1262, '8 {I4}'),
    (4076, 150, 3925, '100'),
    (4076, 2376, 1695, '<15'),
    (4140, 150, 3987, '72 {I10}'),
    (4140, 2158, 1977, '28 {I10}'),
    (4353, 0, 4353, '100'),
    (4417, 0, 4416, '100'),  # Note: table says 4416 keV = 4.416 MeV
    (4515, 150, 4364, '16 {I10}'),
    (4515, 665, 3844, '84 {I10}'),
    (6169, 150, 6017, '29 {I7}'),
    (6169, 1230, 4937, '3 {I1}'),
    (6169, 1888, 4277, '2 {I1}'),
    (6169, 2181, 3987, '5 {I2}'),
    (6169, 2611, 3557, '4 {I2}'),
    (6169, 2722, 3447, '8 {I4}'),
    (6169, 3550, 2617, '5 {I2}'),
    (6169, 3601, 2567, '7 {I4}'),
    (6169, 3983, 2187, '32 {I6}'),
    (6169, 4076, 2087, '5 {I2}'),
    (6169, 4140, 2027, 'tentative'),
    (6207, 2181, 4026, '4 {I1}'),
    (6207, 3545, 2656, '24 {I6}'),
    (6207, 3601, 2606, '49 {I10}'),
    (6207, 3632, 2576, '10 {I5}'),
    (6207, 3983, 2226, '6 {I2}'),
    (6207, 4076, 2126, '7 {I4}'),
    (6229, 0, 6229, '0.8 {I4}'),
    (6229, 461, 5766, '1 {I5}'),
    (6229, 2158, 4066, '5 {I2}'),
    (6229, 2722, 3506, '50 {I6}'),
    (6229, 3771, 2456, '13 {I3}'),
    (6229, 4140, 2086, '6 {I2}'),
    (6229, 4353, 1876, '8 {I3}'),
    (6229, 4417, 1806, '3 {I1}'),
    (6229, 4515, 1716, '11 {I3}'),
    (6229, 4639, 1586, '3 {I1}'),
]

print("Mapping 1971Hy02 transitions to G-records:")
print("="*90)
for ei, ef, eg, ri in transitions:
    lline_key = min(ei_to_lline.keys(), key=lambda x: abs(x-ei))
    lline = ei_to_lline[lline_key]
    block = l_blocks[lline]
    if block['gammas']:
        closest_g = min(block['gammas'], key=lambda x: abs(x['eg']-eg))
        diff = abs(closest_g['eg']-eg)
        gline = closest_g['line']
        match_status = 'OK' if diff < 5 else 'DIFF=%g' % diff

        # Check if RI comment for that G record already has 1971Hy02
        has_ri_1971 = False
        for k in range(gline, min(gline+8, len(lines)+1)):
            if len(lines[k-1]) > 9 and '1971Hy02' in lines[k-1] and 'cG RI' in lines[k-1]:
                has_ri_1971 = True
                break
            # Stop if we hit another G or L record
            if k > gline and len(lines[k-1]) >= 9 and lines[k-1][5:9] in ['  G ', '  L ']:
                break

        # Also check if any existing cG RI$ line is present for this gamma
        has_ri = False
        ri_content = ''
        for k in range(gline, min(gline+8, len(lines)+1)):
            if len(lines[k-1]) > 9 and 'cG RI' in lines[k-1]:
                has_ri = True
                ri_content = lines[k-1].rstrip()
                break
            if k > gline and len(lines[k-1]) >= 9 and lines[k-1][5:9] in ['  G ', '  L ']:
                break

        flag = 'NEED_ADD' if not has_ri_1971 else 'ALREADY_HAS'
        print(f"Ei={ei},Ef={ef},Eg={eg} -> G L{gline} Eg={closest_g['eg']} diff={diff:.1f} {match_status} | {flag} | RI={ri}")
        if has_ri:
            print(f"  Existing RI: {ri_content}")
    else:
        print(f"Ei={ei},Ef={ef},Eg={eg} -> NO GAMMAS")
