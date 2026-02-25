import math

f = 100/43  # scaling factor
print(f"Scaling factor: 100/43 = {f:.10f}")
print()

def round_ri(x):
    """Round Half-Up (5-up): digit >= 5 rounds up."""
    return math.floor(x + 0.5)

def round_dri(x):
    """Uncertainty rounding: 4-up threshold. Digit >= 4 rounds up, digit <= 3 rounds down."""
    frac = x - math.floor(x)
    if frac >= 0.4:
        return math.floor(x) + 1
    else:
        return math.floor(x)

# Gammas under 9157.1 level
# (E_gamma, RI_value, DRI_value_or_None, RI_field_str, DRI_field_str)
gammas = [
    ('3941.1',  7.4,  1.9,  '7.4',  '19'),
    ('4386.9',  6.9,  1.7,  '6.9',  '17'),
    ('4978.8',  16,   None, '16',   'LT'),
    ('4983.3',  16,   None, '16',   'LT'),
    ('5993.6',  9.6,  2.4,  '9.6',  '24'),
    ('6153.8',  8.4,  2.1,  '8.4',  '21'),
    ('6462.6',  1.3,  0.7,  '1.3',  '7'),
    ('6510.8',  2.9,  1.5,  '2.9',  '15'),
    ('7393.1',  7.5,  1.9,  '7.5',  '19'),
    ('9155.8',  43,   4.0,  '43',   '4'),
]

print(f"{'Gamma':<10} {'RI_old':>8} {'DRI_old':>9}  {'RI_scaled':>12} {'DRI_scaled':>12}  {'New RI (5up)':>13} {'New DRI (4up)':>14}")
print('-'*88)
for (eg, ri, dri, ri_str, dri_str) in gammas:
    ri_scaled = f * ri
    if dri is None:
        ri_new = round_ri(ri_scaled)
        print(f"G {eg:<10} {ri_str:>8} {'<(LT)':>9}  {ri_scaled:>12.4f} {'LT':>12}  {ri_new:>13} {'LT':>14}")
    else:
        dri_scaled = f * dri
        ri_new = round_ri(ri_scaled)
        dri_new = round_dri(dri_scaled)
        # Show the fractional part for DRI to clarify rounding decision
        frac_dri = dri_scaled - math.floor(dri_scaled)
        rule = '4up->UP' if frac_dri >= 0.4 else '3dn->DN'
        print(f"G {eg:<10} {ri_str:>8} ({'+/-'+str(dri)+')':>8}  {ri_scaled:>12.6f} {dri_scaled:>12.6f} ({frac_dri:.4f},{rule})  {ri_new:>8} {dri_new:>9}")

print()
print("Notes:")
print("  - RI rounding: Round Half-Up (5-up)")
print("  - DRI rounding: 4-up threshold (frac >= 0.4 rounds up)")
print("  - LT entries: scale RI value only, keep LT marker")

# Also check doublet comment: total Ig=13(3)
print()
print("Doublet cG RI$ comment check (total Ig=13(3) for 4173+4178 doublet):")
ig_total = 13 * f
ig_dri = 3 * f
ig_frac = ig_total - math.floor(ig_total)
dri_frac = ig_dri - math.floor(ig_dri)
print(f"  Ig_scaled = 13 x {f:.6f} = {ig_total:.6f}  -> New RI = {round_ri(ig_total)} (frac={ig_frac:.4f})")
print(f"  DRI_scaled = 3 x {f:.6f} = {ig_dri:.6f}  -> New DRI = {round_dri(ig_dri)} (frac={dri_frac:.4f}, {'4up->UP' if dri_frac >= 0.4 else '3dn->DN'})")
