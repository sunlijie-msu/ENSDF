import re, json

with open(r"d:\X\ND\ENSDF\.github\temp\2026-09-22_s34_level_trace\adopted_levels.json") as f:
    adopted = json.load(f)
with open(r"d:\X\ND\ENSDF\.github\temp\2026-09-22_s34_level_trace\dataset_levels.json") as f:
    dataset_levels = json.load(f)

xref_token_re = re.compile(r'([A-Za-z])(\((\d+(?:\.\d+)?)(\*|\?)?\))?')

def parse_xref(xref):
    """Return list of (letter, paren_energy_or_None)."""
    if not xref:
        return []
    out = []
    i = 0
    while i < len(xref):
        ch = xref[i]
        if ch.isalpha():
            m = re.match(r'\((\d+(?:\.\d+)?)(\*|\?)?\)', xref[i+1:])
            if m:
                out.append((ch, float(m.group(1))))
                i += 1 + m.end()
            else:
                out.append((ch, None))
                i += 1
        else:
            i += 1
    return out

def closest_level(letter, target_e, tol=15.0):
    levels = dataset_levels.get(letter, [])
    best = None
    bestdiff = None
    for ef, e_str, de_str, lineno in levels:
        diff = abs(ef - target_e)
        if bestdiff is None or diff < bestdiff:
            bestdiff = diff
            best = (ef, e_str, de_str, lineno)
    if best and bestdiff <= tol:
        return best, bestdiff
    return None, bestdiff

report = []
for r in adopted:
    if r['n_gam'] != 0 and r['gam_with_unc'] != 0:
        continue  # only check no-gamma levels or levels whose gammas all lack uncertainty
    if not r['E']:
        continue
    try:
        adopted_e = float(re.match(r'^-?\d+\.?\d*', r['E']).group(0))
    except Exception:
        continue
    xref = r['xref']
    tokens = parse_xref(xref) if xref else []
    matches = []
    for letter, paren_e in tokens:
        target = paren_e if paren_e is not None else adopted_e
        tol = 30.0 if paren_e is None else 3.0
        best, diff = closest_level(letter, target, tol=tol)
        matches.append({"letter": letter, "paren_e": paren_e, "match": best, "diff": diff})
    report.append({"lineno": r['lineno'], "adopted_E": r['E'], "adopted_DE": r['DE'], "xref": xref, "matches": matches})

with open(r"d:\X\ND\ENSDF\.github\temp\2026-09-22_s34_level_trace\trace_report.json", "w") as f:
    json.dump(report, f, indent=1)

# Print summary of PROBLEMATIC levels: no match found for ANY xref letter
untraceable = []
for r in report:
    if not r['matches']:
        untraceable.append(r)
        continue
    any_match = any(m['match'] is not None for m in r['matches'])
    if not any_match:
        untraceable.append(r)

print(f"Total no-gamma levels checked: {len(report)}")
print(f"Untraceable (no dataset match found within tolerance): {len(untraceable)}")
for r in untraceable:
    print(r['lineno'], r['adopted_E'], r['adopted_DE'], r['xref'], r['matches'])
