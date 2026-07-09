import math

ln2 = math.log(2)

# Data: (level, tau_str, sigma_tau, T_rec, DT_rec, lim_type)
data = [
    ('428.7', 1.4, 0, 0.97, 'LT', '<'),    # tau < 1.4
    ('1607.4', 1.3, 0.4, 0.90, 28, '='),
    ('2304.7', None, None, 1.4, 11, 'range'),  # range: 430-3600 ps
    ('2319.7', 2.1, 0, 2.1, 'GT', '>'),    # tau > 3 -> T > 2.08
    ('3352', 0.30, 0.15, 0.21, 10, '='),
    ('3950', 0.30, 0.15, 0.21, 10, '='),
    ('4629', 0.5, 0.2, 0.35, 14, '='),
    ('6191', 1.0, 0, 0.69, 'LT', '<'),    # tau < 1 -> T < 0.69
    ('6236', 3.0, 0, 2.08, 'GT', '>'),    # tau > 3 -> T > 2.08
]

print("Level  tau->T1/2 conv  L-rec T   DT    Status")
print("-" * 55)

for d in data:
    name = d[0]
    tau = d[1]
    sigma_tau = d[2]
    trec = d[3]
    dtrec = d[4]
    lim = d[5]
    
    if lim == 'range':
        # 2304.7: tau = 430-3600 ps
        t_low = 0.430 * ln2  # ns
        t_high = 3.600 * ln2  # ns
        rec_t = trec
        rec_dt = dtrec
        # T = 1.4 ns, DT=11 -> 1.4 +/- 1.1 ns
        lo = rec_t - rec_dt/10.0
        hi = rec_t + rec_dt/10.0
        status = "OK" if (abs(t_low - lo) < 0.05 and abs(t_high - hi) < 0.05) else "CHECK"
        print(f"{name:>6}  430-3600 ps -> {t_low:.2f}-{t_high:.2f} ns  {rec_t:.1f}+/-{rec_dt/10:.1f} ns  {status}")
        continue
    
    if lim == '<':
        t_half_max = tau * ln2
        rec_t = trec
        status = "OK" if abs(t_half_max - rec_t) < 0.02 else f"CHECK ({t_half_max:.2f} vs {rec_t:.2f})"
        print(f"{name:>6}  tau<{tau} -> T<{t_half_max:.2f} ps   T={rec_t} DT={dtrec}  {status}")
        continue
    
    if lim == '>':
        t_half_min = tau * ln2
        rec_t = trec
        status = "OK" if abs(t_half_min - rec_t) < 0.1 else f"CHECK ({t_half_min:.2f} vs {rec_t:.2f})"
        print(f"{name:>6}  tau>{tau} -> T>{t_half_min:.2f} ps   T={rec_t} DT={dtrec}  {status}")
        continue
    
    # Exact values
    t_half = tau * ln2
    sigma_t = sigma_tau * ln2
    
    # Rounding check
    # T field: 0.21 PS -> T=0.21
    # DT field: 10 -> uncertainty = 0.10
    rec_t = trec
    rec_sigma = dtrec if isinstance(dtrec, (int, float)) else 0
    rec_sigma_val = rec_sigma * 10**(-1)  # assumes 2 decimal places match
    
    # Check value
    val_ok = abs(t_half - rec_t) < 0.02
    sig_ok = abs(sigma_t * 100 - rec_sigma) < 5
    
    if val_ok and sig_ok:
        status = "OK"
    else:
        status = ""
        if not val_ok: status += f"VAL({t_half:.3f} vs {rec_t:.2f})"
        if not sig_ok: status += f" SIG({sigma_t:.3f} vs {rec_sigma:.0f})"
    
    print(f"{name:>6}  tau={tau}+-{sigma_tau} -> T={t_half:.3f}+-{sigma_t:.3f}  T={rec_t:.2f} DT={rec_sigma:3d}  {status}")
