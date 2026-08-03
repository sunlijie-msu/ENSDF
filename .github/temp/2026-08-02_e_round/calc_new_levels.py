"""Compute feeding split and log ft for new levels 4074, 4889.

Method: empirical f(E0) from calibration points (file log ft values),
plus beta+/EC ratio from the numerical calculation (robust to normalization).
"""
import math
from logft_calc import f_beta_plus, f_ec, f_total

MC2 = 511.0
Q = 5491.60
T12 = 1919.4  # s

# calibration points from file: (E0_keV, log10 f_total)
cal = [
    (3364.036, 2.154),
    (2187.388, 0.9615),
    (1376.787, -0.542),
    (802.62, -1.325),
    (614.761, -1.523),
]

def interp_logf(E0):
    """Linear interpolation/extrapolation of log10 f_total vs log10 E0."""
    import math
    le = math.log10(E0)
    # sort by E0 ascending
    pts = sorted(cal)
    if le <= math.log10(pts[0][0]):
        # extrapolate below using first two points
        e0a, fa = pts[0]
        e0b, fb = pts[1]
        slope = (fb - fa) / (math.log10(e0b) - math.log10(e0a))
        return fa + slope * (le - math.log10(e0a))
    if le >= math.log10(pts[-1][0]):
        e0a, fa = pts[-2]
        e0b, fb = pts[-1]
        slope = (fb - fa) / (math.log10(e0b) - math.log10(e0a))
        return fa + slope * (le - math.log10(e0a))
    for i in range(len(pts) - 1):
        e0a, fa = pts[i]
        e0b, fb = pts[i + 1]
        if e0a <= E0 <= e0b:
            la, lb = math.log10(e0a), math.log10(e0b)
            t = (le - la) / (lb - la)
            return fa + t * (fb - fa)
    raise ValueError(f"E0={E0} out of calibration range")

def feeding_logft(E0, feeding_pct):
    logf = interp_logf(E0)
    t_partial = T12 / (feeding_pct / 100.0)
    return logf + math.log10(t_partial), 10 ** logf

for name, E_level, feeding in [
    ("4889", 4889.756, 0.0305),   # 0.018+0.011+0.0015 (sum of limits)
    ("4074", 4074.667, 0.00081),
]:
    E0 = Q - E_level
    lf, f = feeding_logft(E0, feeding)
    print(f"=== {name}: E_level={E_level} E0={E0:.2f} keV feeding<{feeding}% ===")
    print(f"  empirical f_total={f:.4f}  log ft > {lf:.2f}")
    # beta+/EC ratio from numerical calc
    fb = f_beta_plus(16, E0)
    fe = f_ec(16, E0)
    ftot = fb + fe
    print(f"  numeric f_beta+={fb:.4f} f_EC={fe:.4f} ratio_beta/EC={fb/fe:.3f}")
    print()
