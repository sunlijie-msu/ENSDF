"""Generate the exact new block for level 6931.5 in Cl34_33s_p_g.ens

New normalization: G 2321.7 = 100 (1983Wa27 standard)
Old normalization: G 2325.6 = 100 (1977Da02 standard)
Scale factor for Da02: 100/91 = 1.09890...
"""
import math

factor = 100 / 91

def sig_fig_unc(unc_raw):
    """Return (rounded_unc_int, n_decimals) per ENSDF convention."""
    lead2 = float(f'{unc_raw:.2e}'.split('e')[0]) * 10  # first two sig digits as int
    # Compare the two-digit leading value: <35 → 2 sig, >=35 → 1 sig
    if lead2 < 35:
        nsig = 2
    else:
        nsig = 1
    magnitude = math.floor(math.log10(unc_raw))
    n_dec = max(0, -(magnitude - nsig + 1))
    rounded_unc = round(unc_raw, -magnitude + nsig - 1)
    unc_int = round(rounded_unc * 10**n_dec)
    return int(unc_int), n_dec

def scale(ri, dri_raw):
    """Scale a Da02 RI and its uncertainty. dri_raw is the integer DRI field value."""
    # Interpret dri: for RI with n decimal places, unc = dri_raw * 10^(-n_dec_of_value)
    # We'll directly use: unc = dri_raw (ENSDF DRI = uncertainty in last digit(s) of value)
    # The actual unc = dri_raw * 10^(-nDP(ri))
    # But for scaling, we scale unc directly in the same units as ri then re-express
    # e.g. ri=13.0, dri=65 → unc=6.5 in same units as RI
    ri_str = str(ri)
    if '.' in ri_str:
        n_dec_ri = len(ri_str.split('.')[1])
    else:
        n_dec_ri = 0
    unc = dri_raw * 10**(-n_dec_ri)
    scaled_ri = ri * factor
    scaled_unc = unc * factor
    unc_int, n_dec = sig_fig_unc(scaled_unc)
    value = round(scaled_ri, n_dec)
    return value, n_dec, unc_int

def g_line_wa27(energy, ri_wa27, no_dec=False):
    """G record with Wa27 RI (no uncertainty, no D flag)."""
    nucid = ' 34CL  G '
    e_field = energy.ljust(10)
    de = '  '
    sep = ' '
    ri_field = str(ri_wa27).ljust(7)
    dri = '  '
    rest = ' ' * 49
    line = nucid + e_field + de + sep + ri_field + dri + rest
    assert len(line) == 80, f"len={len(line)}"
    return line

def g_line_da02_only(energy, ri_scaled, unc_int, n_dec, lt=False):
    """G record with Da02 only (D flag, scaled value)."""
    nucid = ' 34CL  G '
    e_field = energy.ljust(10)
    de = '  '
    sep = ' '
    ri_str = f'{ri_scaled:.{n_dec}f}'
    if lt:
        ri_field = ri_str.ljust(7)
        dri = 'LT'
    else:
        ri_field = ri_str.ljust(7)
        dri = str(unc_int).ljust(2)
    rest = ' '*45 + 'D' + '   '
    line = nucid + e_field + de + sep + ri_field + dri + rest
    assert len(line) == 80, f"len={len(line)}"
    return line

def g_line_lt(energy, ri_wa27):
    """G record with LT limit from Wa27 (no D flag)."""
    nucid = ' 34CL  G '
    e_field = energy.ljust(10)
    de = '  '
    sep = ' '
    ri_field = str(ri_wa27).ljust(7)
    dri = 'LT'
    rest = ' ' * 49
    line = nucid + e_field + de + sep + ri_field + dri + rest
    assert len(line) == 80, f"len={len(line)}"
    return line

def g_line_lt_da02_unchanged(energy, ri_wa27):
    """G record with LT from Wa27 (no D, value stays)."""
    return g_line_lt(energy, ri_wa27)

def cg_ri(content):
    line = (' 34CL cG ' + content).ljust(80)
    assert len(line) == 80, f"len={len(line)}"
    return line

def fmt_scaled(value, n_dec, unc_int):
    return f'{value:.{n_dec}f} {{I{unc_int}}}'

# ---- Compute all scaled Da02 values ----
gammas = [
    ('2214.0', 13.0, 65,  24),    # (energy, Da02_ri, Da02_dri, Wa27_ri)
    ('2321.7', 91,   9,   100),   # normalization gamma
    ('2325.6', 100,  10,  64),
    ('2415.7', 4.4,  22,  8.2),
    ('2470.0', None, None, 9.1),  # LT -> becomes exact from Wa27
    ('2577.2', 8.7,  44,  9.1),
    ('2948.4', 17.4, 87,  15),
    ('3331.0', 8.7,  44,  4.6),
    ('3386.2', 13.0, 65,  21),
    ('3548.0', 61,   6,   55),
    ('4209.9', 13.0, 65,  13),
    ('4350.9', 8.7,  44,  19),
    ('4773.2', 8.7,  44,  19),
    # ('5043.8', 8.7,  44,  None), # Da02 only
    ('6265.6', 17.4, 87,  46),
    ('6784.4', 61,   6,   50),
]

print("=== Scaled Da02 values (to G 2321.7=100 norm, scale=100/91) ===")
for row in gammas:
    eg = row[0]
    ri02, dri02, riwa = row[1], row[2], row[3]
    if ri02 is None:
        # LT: scale the limit value
        scaled = 8.7 * factor
        print(f'G{eg}: Da02=8.7 LT → {scaled:.2f} LT → {round(scaled,1):.1f} LT | Wa27={riwa}')
    else:
        v, nd, ui = scale(ri02, dri02)
        print(f'G{eg}: Da02={ri02}({dri02}) → scaled={ri02*factor:.3f}±{(dri02*10**(-len(str(ri02).split(".")[-1]) if "." in str(ri02) else 0))*factor:.3f} → {fmt_scaled(v,nd,ui)} | Wa27={riwa}')

# G5043.8 Da02 only
ri02_5043, dri02_5043 = 8.7, 44
v5, nd5, ui5 = scale(ri02_5043, dri02_5043)
print(f'\nG5043.8: Da02={ri02_5043}({dri02_5043}) → {fmt_scaled(v5,nd5,ui5)} [Da02 only, D flag]')

print()
print("=== New block (correct order) ===")
# Build individual lines dict first, then assemble in original order
# Original order: 2214, 2321.7, 2325.6, 2415.7, 2470.0, 2577.2, 2948.4,
#                 3331.0, 3386.2, 3548.0, 4209.9, 4350.9, 4773.2, 5043.8,
#                 6265.6, 6469.6, 6784.4, 6930.7

# Precompute all scaled Da02 values
def make_wa27_pair(eg, riwa, da02_comment):
    return [g_line_wa27(eg, riwa), cg_ri('RI$' + da02_comment)]

def make_wa27_only(eg, riwa):
    return [g_line_wa27(eg, riwa)]

def make_lt_wa27(eg, riwa):
    return [g_line_lt(eg, riwa)]

block = []

# G 2214.0: Wa27=24, Da02 scaled=14 {I7}
v,nd,ui = scale(13.0, 65)
block += make_wa27_pair('2214.0', 24, f'{fmt_scaled(v,nd,ui)} (1977Da02)')
# G 2321.7: Wa27=100, Da02 scaled=100 {I10}
v,nd,ui = scale(91, 9)
block += make_wa27_pair('2321.7', 100, f'{fmt_scaled(v,nd,ui)} (1977Da02)')
# G 2325.6: Wa27=64, Da02 scaled=110 {I11}
v,nd,ui = scale(100, 10)
block += make_wa27_pair('2325.6', 64, f'{fmt_scaled(v,nd,ui)} (1977Da02)')
# G 2415.7: Wa27=8.2, Da02 scaled=4.8 {I24}
v,nd,ui = scale(4.4, 22)
block += make_wa27_pair('2415.7', 8.2, f'{fmt_scaled(v,nd,ui)} (1977Da02)')
# G 2470.0: Wa27=9.1 (exact), Da02 scaled LT=9.6 LT
block += [g_line_wa27('2470.0', 9.1), cg_ri(f'RI${round(8.7*factor,1)} LT (1977Da02)')]
# G 2577.2: Wa27=9.1, Da02 scaled=10 {I5}
v,nd,ui = scale(8.7, 44)
block += make_wa27_pair('2577.2', 9.1, f'{fmt_scaled(v,nd,ui)} (1977Da02)')
# G 2948.4: Wa27=15, Da02 scaled=19 {I10}
v,nd,ui = scale(17.4, 87)
block += make_wa27_pair('2948.4', 15, f'{fmt_scaled(v,nd,ui)} (1977Da02)')
# G 3331.0: Wa27=4.6, Da02 scaled=10 {I5}
v,nd,ui = scale(8.7, 44)
block += make_wa27_pair('3331.0', 4.6, f'{fmt_scaled(v,nd,ui)} (1977Da02)')
# G 3386.2: Wa27=21, Da02 scaled=14 {I7}
v,nd,ui = scale(13.0, 65)
block += make_wa27_pair('3386.2', 21, f'{fmt_scaled(v,nd,ui)} (1977Da02)')
# G 3548.0: Wa27=55, Da02 scaled=67 {I7}
v,nd,ui = scale(61, 6)
block += make_wa27_pair('3548.0', 55, f'{fmt_scaled(v,nd,ui)} (1977Da02)')
# G 4209.9: Wa27=13, Da02 scaled=14 {I7}
v,nd,ui = scale(13.0, 65)
block += make_wa27_pair('4209.9', 13, f'{fmt_scaled(v,nd,ui)} (1977Da02)')
# G 4350.9: Wa27=19, Da02 scaled=10 {I5}
v,nd,ui = scale(8.7, 44)
block += make_wa27_pair('4350.9', 19, f'{fmt_scaled(v,nd,ui)} (1977Da02)')
# G 4773.2: Wa27=19, Da02 scaled=10 {I5}
v,nd,ui = scale(8.7, 44)
block += make_wa27_pair('4773.2', 19, f'{fmt_scaled(v,nd,ui)} (1977Da02)')
# G 5043.8: Da02 only → D flag, scaled value
v5,nd5,ui5 = scale(8.7, 44)
block += [g_line_da02_only('5043.8', v5, ui5, nd5)]
# G 6265.6: Wa27=46, Da02 scaled=19 {I10}
v,nd,ui = scale(17.4, 87)
block += make_wa27_pair('6265.6', 46, f'{fmt_scaled(v,nd,ui)} (1977Da02)')
# G 6469.6: Wa27 LT (unchanged)
block += [g_line_lt('6469.6', 9.1)]
# G 6784.4: Wa27=50, Da02 scaled=67 {I7}
v,nd,ui = scale(61, 6)
block += make_wa27_pair('6784.4', 50, f'{fmt_scaled(v,nd,ui)} (1977Da02)')
# G 6930.7: Wa27 LT (unchanged)
block += [g_line_lt('6930.7', 6.8)]

print(f"Total lines: {len(block)}")
for i, line in enumerate(block):
    print(f'{i+1:2d}: {repr(line)}')
print()
print("=== Visual check ===")
for line in block:
    print(line)
