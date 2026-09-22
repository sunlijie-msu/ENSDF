import json

with open(r"d:\X\ND\ENSDF\.github\temp\2026-09-22_s34_level_trace\trace_report.json") as f:
    report = json.load(f)

flags = []
for r in report:
    ms = [m for m in r['matches'] if m['match'] is not None]
    if not ms:
        flags.append((r, "NO_MATCH_AT_ALL"))
        continue
    vals = [m['match'][0] for m in ms]
    avg = sum(vals) / len(vals)
    try:
        adopted_e = float(r['adopted_E'])
    except Exception:
        adopted_e = None
    diff = None if adopted_e is None else abs(adopted_e - avg)
    de = r['adopted_DE']
    de_val = float(de) if de not in (None, '') else None
    # tolerance: 3x reported DE (min 3 keV), else flat 8 keV if no DE
    if de_val is not None:
        tol = max(3.0, 3 * de_val * (10 ** -(len(r['adopted_E'].split('.')[1]) if '.' in r['adopted_E'] else 0)))
    tol = 8.0 if de_val is None else max(6.0, de_val * 0.05 + 3)  # simplistic; refine per-decimal below
    # Better: DE is in units of last decimal digit of E. Determine decimal places of E.
    if '.' in r['adopted_E']:
        decimals = len(r['adopted_E'].split('.')[1])
    else:
        decimals = 0
    if de_val is not None:
        de_abs = de_val * (10 ** -decimals)
        tol = max(3 * de_abs, 1.0)
    else:
        tol = 8.0
    if diff is not None and diff > tol:
        flags.append((r, f"DIFF={diff:.2f} keV > tol={tol:.2f} (avg={avg:.2f}, n_src={len(vals)})"))

print(f"Total flagged (diff exceeds tolerance): {len(flags)}")
for r, reason in flags:
    print(r['lineno'], r['adopted_E'], r['adopted_DE'], r['xref'], '->', reason)
    for m in r['matches']:
        print('    ', m)
