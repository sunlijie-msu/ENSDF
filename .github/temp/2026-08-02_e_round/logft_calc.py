"""Compute log ft for 34Clm -> 34S beta decay, calibrated against existing E records.

Parent: 34Clm (3+, T1/2 = 31.99 m = 1919.4 s), Q = 5491.60 keV.
Daughter Z = 16.

Method:
  f_beta+ = int_1^W0 F(Z,W) p W (W0-W)^2 dW   (screened point-nucleus)
  f_EC    = f_K + f_L1 (K + L1 capture), standard K-capture formula
  log ft  = log10( f_total * t_partial ), t_partial = T1/2(parent) / feeding_frac
Calibrates against known (E0, feeding, logft) from existing E records.
"""
import math
import cmath

ALPHA = 1 / 137.035999084
MC2 = 511.0  # keV
R_NUC = 1.2 * (34 ** (1 / 3)) / 386.159  # nuclear radius in natural units (hbar/mc)


def gamma_func_complex(gamma, y):
    """|Gamma(gamma + i y)|^2 using infinite product:
    |Gamma(gamma+iy)|^2 = Gamma(gamma)^2 * prod_n 1/(1+(y/(gamma+n))^2)
    """
    g2 = math.gamma(gamma) ** 2
    prod = 1.0
    n = 0
    while True:
        term = 1.0 / (1.0 + (y / (gamma + n)) ** 2)
        prod *= term
        n += 1
        if n > 2000 or abs(term - 1.0) < 1e-15:
            break
    return g2 * prod


def fermi_fermi(Z, W, p, screening=True):
    """Fermi function (point nucleus + Rose screening) for positron (beta+)."""
    gamma = math.sqrt(1 - (ALPHA * Z) ** 2)
    # Rose screening: for positrons, V0 positive (repulsion reduced)
    V0 = 0.0
    if screening:
        # screening potential V0 (in mc2 units); standard value ~ 1.13*alpha^2*Z^(4/3)
        V0 = 1.13 * ALPHA ** 2 * Z ** (4 / 3)
    Ws = W - V0
    if Ws <= 1.0:
        return 0.0
    ps = math.sqrt(Ws * Ws - 1)
    y = -ALPHA * Z * Ws / ps
    F0 = 2 * (1 + gamma) * (2 * ps * R_NUC) ** (2 * (gamma - 1))
    F0 *= math.exp(math.pi * y) * gamma_func_complex(gamma, y)
    F0 /= math.gamma(2 * gamma + 1) ** 2
    # additional screening factor (approximate)
    if screening:
        F0 *= ((Ws * Ws - 1) / (W * W - 1)) ** (gamma - 0.5) if W > 1 else 1.0
    return F0


def integrate(f, a, b, n=20000):
    """Simpson's rule integration."""
    if b <= a:
        return 0.0
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        x = a + i * h
        s += (4 if i % 2 else 2) * f(x)
    return s * h / 3


def f_beta_plus(Z, Q_EC_keV):
    """beta+ f-value; requires Q_EC > 1022 keV."""
    E0 = Q_EC_keV - 2 * MC2  # max positron kinetic energy
    if E0 <= 0:
        return 0.0
    W0 = E0 / MC2 + 1.0
    def integrand(W):
        p = math.sqrt(W * W - 1)
        F = fermi_fermi(Z, W, p)
        return F * p * W * (W0 - W) ** 2
    return integrate(integrand, 1.0, W0)


def f_ec(Z, Q_EC_keV):
    """K + L1 capture f-value (EC uses full Q_EC)."""
    if Q_EC_keV <= 0.0:
        return 0.0
    gamma = math.sqrt(1 - (ALPHA * Z) ** 2)
    W0 = Q_EC_keV / MC2 + 1.0
    W_K = 2.472 / MC2
    W_L = 0.230 / MC2
    gK2 = (2 * ALPHA * Z) ** (2 * gamma + 1) * (1 + gamma)
    gK2 *= (2 * R_NUC) ** (2 * (gamma - 1)) / math.gamma(2 * gamma + 1) ** 2
    f_K = (math.pi / 2) * gK2 * (W0 + W_K) ** 2
    # L1 capture (standard L/K ratio for low Z ~ 0.1-0.15)
    f_L1 = (math.pi / 2) * gK2 * (W0 + W_L) ** 2 * 0.12
    return f_K + f_L1


def f_total(Z, Q_EC_keV):
    return f_beta_plus(Z, Q_EC_keV) + f_ec(Z, Q_EC_keV)


def logft(Q, E_level, feeding_pct, T12_s=1919.4):
    """log ft for decay to level at E_level (keV) with feeding (%)."""
    Q_EC = Q - E_level
    f = f_total(16, Q_EC)
    if feeding_pct <= 0:
        return None
    t_partial = T12_s / (feeding_pct / 100.0)
    return math.log10(f * t_partial)


if __name__ == "__main__":
    # ---- calibration: existing levels (E_level, feeding, file logft) ----
    cal = [
        (2127.564, 28.5, 5.982),
        (3304.212, 26.4, 4.823),
        (4114.813, 0.457, 5.081),
        (4688.98, 0.033, 5.44),
        (4876.839, 0.038, 5.18),
    ]
    print("=== CALIBRATION (Q=5491.60, T1/2=1919.4s) ===")
    for E, feed, file_lf in cal:
        calc = logft(5491.60, E, feed)
        print(f"E_level={E:9.3f} feed={feed:6.3f}% file_logft={file_lf:6.3f} calc_logft={calc:6.3f} diff={calc-file_lf:+.3f}")

    print()
    print("=== NEW LEVELS ===")
    # 4889: E0 = 5491.60-4889.756; feeding = sum of gamma limits = 0.018+0.011+0.0015 = 0.0305 (upper limit)
    E4889 = 4889.756
    feed4889 = 0.018 + 0.011 + 0.0015
    lf4889 = logft(5491.60, E4889, feed4889)
    print(f"4889: E0={5491.60-E4889:.2f} keV feed(limit)={feed4889:.4f}% logft(limit)={lf4889:.2f}")

    # 4074: E0 = 5491.60-4074.667; feeding = 0.00081 (upper limit, gs gamma only)
    E4074 = 4074.667
    feed4074 = 0.00081
    lf4074 = logft(5491.60, E4074, feed4074)
    print(f"4074: E0={5491.60-E4074:.2f} keV feed(limit)={feed4074:.5f}% logft(limit)={lf4074:.2f}")
