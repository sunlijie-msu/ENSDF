"""
Generate 1971HY02.ens ENSDF raw dataset for 34Cl.
Gamma energies = Ei(adopted) - Ef(adopted) from Cl34_33s_p_g.ens.
RI values and uncertainties from 1971Hy02 Table I.
"""

# Adopted level energies (keV), keyed by 1971Hy02 approximate MeV label
# The key is a tuple of (1971Hy02 Ei_str, 1971Hy02 Ef_str) identifying each row
# All energies below are adopted (from Cl34_33s_p_g.ens)

adopted = {
    '0':     0.0,
    '0.15':  146.4,
    '0.46':  461.2,
    '0.67':  665.3,
    '1.23':  1230.33,
    '1.89':  1887.29,
    '1.888': 1887.29,
    '2.16':  2157.9,
    '2.158': 2157.9,
    '2.18':  2181.1,
    '2.180': 2181.1,
    '2.38':  2375.7,
    '2.377': 2375.7,
    '2.61':  2611.03,
    '2.611': 2611.03,
    '2.72':  2721.3,
    '2.722': 2721.3,
    '3.545': 3545.08,
    '3.55':  3545.08,
    '3.60':  3600.28,
    '3.601': 3600.28,
    '3.63':  3631.7,
    '3.632': 3631.7,
    '3.771': 3773.72,
    '3.77':  3773.72,
    '3.98':  3983.0,
    '3.982': 3983.0,
    '4.075': 4076.2,
    '4.08':  4076.2,
    '4.137': 4139.7,
    '4.14':  4139.7,
    '4.353': 4354.2,
    '4.35':  4354.2,
    '4.416': 4417.3,
    '4.42':  4417.3,
    '4.514': 4515.7,
    '4.51':  4515.7,
    '4.64':  4638.9,
    '6.167': 6169.4,
    '6.206': 6208.2,
    '6.226': 6229.5,
}

# Table I from 1971Hy02: (Ei_label, Ef_label, RI_str, DRI_str or None)
# RI given as strings exactly as in paper. DRI=None means no uncertainty.
# "tentative" entries are excluded (per instruction: skip tentative).
table = [
    # Ei=6.226 (6229.5 keV)
    ('6.226', '0',    '0.8', '0.4'),
    ('6.226', '0.46', '1.0', '5'),
    ('6.226', '2.16', '5',   '2'),
    ('6.226', '2.72', '50',  '6'),
    ('6.226', '3.77', '13',  '3'),
    ('6.226', '4.14', '6',   '2'),
    ('6.226', '4.35', '8',   '3'),
    ('6.226', '4.42', '3',   '1'),
    ('6.226', '4.51', '11',  '3'),
    ('6.226', '4.64', '3',   '1'),
    # Ei=6.206 (6208.2 keV)
    ('6.206', '2.18', '4',   '1'),
    ('6.206', '3.55', '24',  '6'),
    ('6.206', '3.60', '49',  '10'),
    ('6.206', '3.63', '10',  '5'),
    ('6.206', '3.98', '6',   '2'),
    ('6.206', '4.08', '7',   '4'),
    # Ei=6.167 (6169.4 keV)
    ('6.167', '0.15', '29',  '7'),
    ('6.167', '1.23', '3',   '1'),
    ('6.167', '1.89', '2',   '1'),
    ('6.167', '2.18', '5',   '2'),
    ('6.167', '2.61', '4',   '2'),
    ('6.167', '2.72', '8',   '4'),
    ('6.167', '3.55', '5',   '2'),
    ('6.167', '3.60', '7',   '4'),
    ('6.167', '3.98', '32',  '6'),
    ('6.167', '4.08', '5',   '2'),
    # tentative: ('6.167', '4.14', '5', None) -- EXCLUDED
    # Ei=4.514 (4515.7 keV)
    ('4.514', '0.15', '16',  '10'),
    ('4.514', '0.67', '84',  '10'),
    # Ei=4.416 (4417.3 keV)
    ('4.416', '0',    '100', None),
    # Ei=4.353 (4354.2 keV)
    ('4.353', '0',    '100', None),
    # Ei=4.137 (4139.7 keV)
    ('4.137', '0.15', '72',  '10'),
    ('4.137', '2.16', '28',  '10'),
    # Ei=4.075 (4076.2 keV)
    ('4.075', '0.15', '100', None),
    ('4.075', '2.38', 'LT15',None),   # <15, upper limit
    # Ei=3.982 (3983.0 keV)
    ('3.982', '0.15', '65',  '6'),
    ('3.982', '2.16', '26',  '5'),
    ('3.982', '2.72', '8',   '4'),
    # Ei=3.771 (3773.72 keV)
    ('3.771', '0',    '100', None),
    # Ei=3.632 (3631.7 keV)
    ('3.632', '0.15', '48',  '7'),
    ('3.632', '2.38', '52',  '7'),
    # Ei=3.601 (3600.28 keV)
    ('3.601', '0.15', '48',  '5'),
    ('3.601', '2.38', '8',   '4'),
    ('3.601', '2.72', '44',  '5'),
    # Ei=3.545 (3545.08 keV)
    ('3.545', '0.15', '100', None),
    # Ei=2.722 (2721.3 keV)
    ('2.722', '0',    '13',  '3'),
    ('2.722', '0.15', '19',  '3'),
    ('2.722', '0.46', '47',  '4'),
    ('2.722', '0.67', '8',   '3'),
    ('2.722', '1.23', '3',   '1'),
    ('2.722', '1.89', '2',   '1'),
    ('2.722', '2.16', '8',   '3'),
    # Ei=2.611 (2611.03 keV)
    ('2.611', '0.15', '45',  '9'),
    ('2.611', '0.67', '5',   '4'),
    ('2.611', '1.23', '50',  '9'),
    # Ei=2.377 (2375.7 keV)
    ('2.377', '0.15', '100', None),
    # Ei=2.180 (2181.1 keV)
    ('2.180', '0.15', '57',  '8'),
    ('2.180', '0.46', '28',  '5'),
    ('2.180', '0.67', '15',  '7'),
    # Ei=2.158 (2157.9 keV)
    ('2.158', '0',    '13',  '3'),
    ('2.158', '0.15', '13',  '6'),
    ('2.158', '0.46', '67',  '6'),
    ('2.158', '0.67', 'LT1', None),   # <1, upper limit
    ('2.158', '1.23', '7',   '4'),
    # Ei=1.888 (1887.29 keV)
    ('1.888', '0.15', '40',  '4'),
    ('1.888', '0.46', '60',  '4'),
]

def fmt_energy(e_kev):
    """Format energy for ENSDF E field (10 chars, left-justified)."""
    if e_kev == int(e_kev):
        s = f'{int(e_kev)}'
    else:
        # Use enough decimal places to represent the value precisely
        # but not more than needed
        s = f'{e_kev:.2f}'.rstrip('0').rstrip('.')
    return s

def fmt_ri(ri_str, dri_str):
    """
    Returns (RI_field, DRI_field) where:
      RI_field  = 7 chars (cols 23-29), left-justified
      DRI_field = 2 chars (cols 30-31)
    Handles:
      - plain number with uncertainty
      - plain number without uncertainty (no DRI)
      - LT value (upper limit <N)

    dri_str is either:
      - None (no uncertainty)
      - integer string already in "last-digit" notation (e.g. '3', '10')
      - decimal string from paper (e.g. '0.4') that needs conversion
    """
    if ri_str.startswith('LT'):
        val = ri_str[2:]  # strip 'LT'
        ri_f = f'{val:<7s}'
        dri_f = 'LT'
        return ri_f, dri_f
    # Normal value
    ri_f = f'{ri_str:<7s}'
    if dri_str is None:
        dri_f = '  '
    elif '.' in dri_str:
        # Fractional DRI from paper — convert to integer-in-last-digits notation
        # matching the decimal places of ri_str
        ri_ndec = len(ri_str.split('.')[1]) if '.' in ri_str else 0
        dri_num = float(dri_str)
        dri_int = round(dri_num * (10 ** ri_ndec))
        dri_f = f'{dri_int:<2}'
    else:
        # Integer DRI string — use directly (already in last-digit notation)
        dri_f = f'{dri_str:<2}'
    return ri_f, dri_f

def build_g_record(nucid, eg_kev, ri_str, dri_str):
    """Build an 80-char ENSDF G-record."""
    # NUCID: cols 1-5
    # col 6: blank (first occurrence)
    # col 7: blank
    # col 8: 'G'
    # col 9: blank
    # E field cols 10-19 (10 chars)
    # DE cols 20-21 (2 chars) - blank (no energy uncertainty in this dataset)
    # col 22: readability space
    # RI cols 23-29 (7 chars)
    # DRI cols 30-31 (2 chars)
    # rest: blank to col 80

    eg_str = fmt_energy(eg_kev)
    ri_f, dri_f = fmt_ri(ri_str, dri_str)

    # Build line character by character
    line = (
        f'{nucid:<5s}'   # cols 1-5
        f' '             # col 6: blank (CONT)
        f' '             # col 7: blank
        f'G'             # col 8: TYPE
        f' '             # col 9: blank
        f'{eg_str:<10s}' # cols 10-19: E
        f'  '            # cols 20-21: DE (blank)
        f' '             # col 22: space
        f'{ri_f}'        # cols 23-29: RI (7 chars)
        f'{dri_f}'       # cols 30-31: DRI (2 chars)
    )
    # Pad to exactly 80 chars
    line = f'{line:<80s}'
    assert len(line) == 80, f'G-record length {len(line)}: {repr(line)}'
    return line

def build_l_record(nucid, e_kev):
    """Build an 80-char ENSDF L-record (energy only, no J/T)."""
    e_str = fmt_energy(e_kev)
    line = (
        f'{nucid:<5s}'   # cols 1-5
        f' '             # col 6
        f' '             # col 7
        f'L'             # col 8
        f' '             # col 9
        f'{e_str:<10s}'  # cols 10-19: E
    )
    line = f'{line:<80s}'
    assert len(line) == 80
    return line

def build_id_record(nucid, ref, reaction):
    """Build identification record."""
    # XA record: cols 1-5 NUCID, col 8 'X', cols 9+ dataset name
    line = f'{nucid:<5s}  XA{ref:<72s}'
    line = f'{line:<80s}'
    assert len(line) == 80
    return line

# nucid for 34CL
NUCID = ' 34CL'

# Group table by Ei
from collections import OrderedDict
levels = OrderedDict()
for row in table:
    ei_label = row[0]
    if ei_label not in levels:
        levels[ei_label] = []
    levels[ei_label].append(row)

# Sort levels by ascending adopted energy
levels = OrderedDict(sorted(levels.items(), key=lambda x: adopted[x[0]]))

# Build the ENSDF lines
output_lines = []

# Identification record: cols 1-5 NUCID, col6 blank, col7 blank, col8='X', col9='A', cols10-80=dataset name
id_body = '1971HY02'
id_line = f'{NUCID}  XA{id_body:<71s}'
assert len(id_line) == 80, f'ID len={len(id_line)}: {repr(id_line)}'
output_lines.append(id_line)

for ei_label, rows in levels.items():
    ei_kev = adopted[ei_label]

    # L-record
    output_lines.append(build_l_record(NUCID, ei_kev))

    # G-records: sort by Eg ascending (= Ei - Ef, so ascending Eg = descending Ef)
    g_rows = []
    for (ei_l, ef_l, ri_str, dri_str) in rows:
        ef_kev = adopted[ef_l]
        eg_kev = round(ei_kev - ef_kev, 4)
        g_rows.append((eg_kev, ri_str, dri_str))
    g_rows.sort(key=lambda x: x[0])  # ascending Eg

    for (eg_kev, ri_str, dri_str) in g_rows:
        output_lines.append(build_g_record(NUCID, eg_kev, ri_str, dri_str))

# Write output
out_path = r'A34\Cl34\raw\1971HY02.ens'
with open(out_path, 'w', newline='\n') as f:
    for line in output_lines:
        f.write(line + '\n')

print(f'Written {len(output_lines)} lines to {out_path}')
# Print all lines for inspection
for i, line in enumerate(output_lines):
    print(f'{i+1:3d}: {line}')
