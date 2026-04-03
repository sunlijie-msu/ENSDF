"""
XREF cross-check: MRG '*new XREF new tags' vs ENS '34CLX L XREF=' for levels < 5400 keV.
Matching tolerance: ±3 keV.
"""
import re, sys

MRG = r"A34\Cl34\raw\34_20260331.mrg"
ENS = r"A34\Cl34\new\Cl34_adopted.ens"
E_CUT   = 5400.0
E_TOL   = 3.0

# ── Parse MRG ─────────────────────────────────────────────────────────────────
# Structure (per level block):
#   LEVEL****  34CL  L <energy>  ...
#   *new XREF new tags    34CLX L XREF=<value>
def parse_mrg(path):
    """Return list of (energy_str, float_energy, xref_str, lineno)."""
    results = []
    lines = open(path, encoding='utf-8', errors='replace').readlines()
    current_energy = None
    current_eline  = None
    for i, raw in enumerate(lines):
        line = raw.rstrip()
        # Detect level header: " LEVEL****  34CL  L <energy>"
        m = re.match(r'^ LEVEL\*+\s+34CL\s+L\s+(\S+)', line)
        if m:
            current_energy = m.group(1)
            current_eline  = i + 1
        # Detect '*new XREF new tags' line
        if '*new XREF new tags' in line and '34CLX L XREF=' in line:
            xm = re.search(r'34CLX L XREF=(\S+)', line)
            if xm and current_energy is not None:
                try:
                    e_float = float(re.sub(r'[^\d.\-+E]', '', current_energy))
                except ValueError:
                    e_float = None
                results.append({
                    'e_str':  current_energy,
                    'e':      e_float,
                    'xref':   xm.group(1),
                    'lineno': i + 1,
                    'level_lineno': current_eline,
                })
    return results

# ── Parse ENS ─────────────────────────────────────────────────────────────────
# Structure:
#   34CL  L <energy> ...
#   34CLX L XREF=<value>
def parse_ens(path):
    """Return list of (energy_str, float_energy, xref_str, lineno)."""
    results = []
    lines = open(path, encoding='utf-8', errors='replace').readlines()
    current_energy = None
    current_eline  = None
    for i, raw in enumerate(lines):
        line = raw.rstrip()
        if len(line) < 10:
            continue
        nucid = line[0:5]   # ' 34CL' for Cl-34
        cont  = line[5]     # col 6: blank = first record, 'X' = XREF cont
        rtype = line[7]     # col 8: record type
        # L-record: NUCID=' 34CL', CONT=blank, TYPE='L'
        if nucid == ' 34CL' and cont == ' ' and rtype == 'L':
            e_field = line[9:19].strip()
            if e_field:
                current_energy = e_field
                current_eline  = i + 1
        # XREF line: NUCID=' 34CL', CONT='X', TYPE='L', contains XREF=
        if nucid == ' 34CL' and cont == 'X' and rtype == 'L' and 'XREF=' in line:
            xm = re.search(r'XREF=(\S+)', line)
            if xm and current_energy is not None:
                try:
                    e_float = float(re.sub(r'[^\d.\-+E]', '', current_energy))
                except ValueError:
                    e_float = None
                results.append({
                    'e_str':  current_energy,
                    'e':      e_float,
                    'xref':   xm.group(1),
                    'lineno': i + 1,
                    'level_lineno': current_eline,
                })
    return results

# ── Main ──────────────────────────────────────────────────────────────────────
mrg_levels = [x for x in parse_mrg(MRG) if x['e'] is not None and x['e'] < E_CUT]
ens_levels = [x for x in parse_ens(ENS) if x['e'] is not None and x['e'] < E_CUT]

print(f"MRG levels < {E_CUT} keV: {len(mrg_levels)}")
print(f"ENS levels < {E_CUT} keV: {len(ens_levels)}")
print()

# Match each MRG level to nearest ENS level within tolerance
def find_match(e, candidates, tol):
    best, best_d = None, tol + 1
    for c in candidates:
        if c['e'] is not None:
            d = abs(c['e'] - e)
            if d < best_d:
                best_d = d
                best = c
    return best if best_d <= tol else None

mismatches = []
unmatched_mrg = []
matched_ens_linenos = set()

for m in mrg_levels:
    e = m['e']
    match = find_match(e, ens_levels, E_TOL)
    if match is None:
        unmatched_mrg.append(m)
        continue
    matched_ens_linenos.add(match['lineno'])
    if m['xref'] != match['xref']:
        mismatches.append({
            'e_mrg':     m['e_str'],
            'e_ens':     match['e_str'],
            'xref_mrg':  m['xref'],
            'xref_ens':  match['xref'],
            'mrg_line':  m['lineno'],
            'ens_line':  match['lineno'],
        })

unmatched_ens = [x for x in ens_levels if x['lineno'] not in matched_ens_linenos]

# ── Report ───────────────────────────────────────────────────────────────────
print(f"{'='*72}")
print(f"MISMATCHES (XREF differs): {len(mismatches)}")
print(f"{'='*72}")
if mismatches:
    for mm in mismatches:
        print(f"  E(MRG)={mm['e_mrg']:<12} E(ENS)={mm['e_ens']:<12}")
        print(f"    MRG XREF (line {mm['mrg_line']:4}): {mm['xref_mrg']}")
        print(f"    ENS XREF (line {mm['ens_line']:4}): {mm['xref_ens']}")
        print()
else:
    print("  None — all XREFs match.")
    print()

print(f"{'='*72}")
print(f"MRG levels with NO match in ENS (within ±{E_TOL} keV): {len(unmatched_mrg)}")
print(f"{'='*72}")
for u in unmatched_mrg:
    print(f"  E={u['e_str']:<12} XREF={u['xref']}  (MRG line {u['lineno']})")

print()
print(f"{'='*72}")
print(f"ENS levels with NO match in MRG (within ±{E_TOL} keV): {len(unmatched_ens)}")
print(f"{'='*72}")
for u in unmatched_ens:
    print(f"  E={u['e_str']:<12} XREF={u['xref']}  (ENS line {u['lineno']})")

print()
total_levels = len(mrg_levels)
spot_n = max(10, -(-total_levels * 15 // 100))  # ceil(15%)
print(f"{'='*72}")
print(f"SPOT-CHECK INFO: {total_levels} MRG levels → 15% = {spot_n} samples")

# Print all matched pairs for spot-check reference
print(f"\nAll matched pairs (MRG E → ENS E → MRG XREF → ENS XREF):")
count = 0
for m in mrg_levels:
    match = find_match(m['e'], ens_levels, E_TOL)
    if match:
        count += 1
        status = "OK" if m['xref'] == match['xref'] else "MISMATCH"
        print(f"  {count:3}. {m['e_str']:<12} -> {match['e_str']:<12}  MRG:{m['xref']:<35} ENS:{match['xref']:<35} [{status}]")
