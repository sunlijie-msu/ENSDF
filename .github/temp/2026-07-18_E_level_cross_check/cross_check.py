"""
Cross-check: ENSDF L-record energies vs Table I level energies.
Generates markdown report.
"""
import re, os
from collections import OrderedDict

ENSDF_PATH = 'd:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd.ens'
TABLE_I_PATH = 'd:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd_Table_I.md'
REPORT_PATH = 'd:/X/ND/ENSDF/.github/temp/2026-07-18_E_level_cross_check/report.md'

os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)

# ── Parse Table I ──────────────────────────────────────────────
def parse_table_I_levels(path):
    """Extract all level entries from Table I. Returns OrderedDict of {E_key: {data}}.
    A 'level' appears as first row with that Ei; subsequent same-Ei rows are gammas."""
    levels = OrderedDict()
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line.startswith('|') or 'none' in line or '---' in line:
                continue
            parts = [p.strip() for p in line.split('|')]
            if len(parts) < 11:
                continue
            ei_raw = parts[1]   # e.g. "344.37 (3)" or "615.51 (3)"
            jpi    = parts[2]   # e.g. "0+" or "2+"
            eg_raw = parts[3]   # gamma energy
            ig_raw = parts[4]   # gamma intensity
            ef_raw = parts[5]   # final level energy
            jpf    = parts[6]   # final Jpi
            mult   = parts[7]   # multipolarity
            delta  = parts[8]   # mixing ratio
            alpha  = parts[9]   # conversion coefficient
            
            # Parse Ei
            ei_match = re.match(r'^([\d.]+)\s*\((\d+)\)$', ei_raw)
            if ei_match:
                ei_val = float(ei_match.group(1))
                ei_unc = int(ei_match.group(2))
                ei_dp  = len(ei_match.group(1).split('.')[1]) if '.' in ei_match.group(1) else 0
            else:
                # No uncertainty (e.g. "0")
                try:
                    ei_val = float(ei_raw)
                    ei_unc = None
                    ei_dp  = 0
                except:
                    continue
            
            key = round(ei_val)  # rounded keV for matching
            if key not in levels:
                levels[key] = {
                    'ei_raw': ei_raw,
                    'ei_val': ei_val,
                    'ei_unc': ei_unc,
                    'ei_dp': ei_dp,
                    'jpi': jpi,
                    'gammas': []
                }
            levels[key]['gammas'].append({
                'eg_raw': eg_raw,
                'ig_raw': ig_raw,
                'ef_raw': ef_raw,
                'mult': mult,
                'delta': delta,
                'alpha': alpha
            })
    return levels

# ── Parse ENSDF L-records ──────────────────────────────────────
def parse_ensdf_L_records(path):
    """Extract L-record energies from ENSDF file."""
    levels = OrderedDict()
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    cur_level = None
    for i, line in enumerate(lines):
        # L-record: col 6=space, col 7=space, col 8='L'
        if len(line) >= 9 and line[5:6] == ' ' and line[6:7] == ' ' and line[7:8] == 'L':
            e_field = line[9:19]  # cols 10-19
            de_field = line[19:21]  # cols 20-21
            
            e_str = e_field.strip()
            de_str = de_field.strip()
            
            if not e_str:
                continue
            
            try:
                e_val = float(e_str)
            except:
                continue
            
            # Parse uncertainty
            e_unc = None
            if de_str:
                try:
                    e_unc = int(de_str)
                except:
                    pass
            
            # Decimal places
            e_dp = len(e_str.split('.')[1]) if '.' in e_str else 0
            
            key = round(e_val)
            levels[key] = {
                'e_field': e_field,
                'e_val': e_val,
                'e_unc': e_unc,
                'e_dp': e_dp,
                'de_field': de_field,
                'line_num': i + 1,
                'full_line': line.rstrip('\n\r')
            }
    
    return levels

# ── Main ────────────────────────────────────────────────────────
t1_levels = parse_table_I_levels(TABLE_I_PATH)
ensdf_levels = parse_ensdf_L_records(ENSDF_PATH)

print(f"Table I levels: {len(t1_levels)}")
print(f"ENSDF L-records: {len(ensdf_levels)}")

# ── Match and compare ───────────────────────────────────────────
report_lines = []
report_lines.append("# Level Energy Cross-Check: ENSDF vs Table I")
report_lines.append("")
report_lines.append(f"**Source:** `2026OSAA_CT11035_152Gd_Table_I.md` (Table I)")
report_lines.append(f"**Target:** `2026OSAA_CT11035_152Gd.ens` (ENSDF L-records)")
report_lines.append(f"**Date:** 2026-07-18")
report_lines.append(f"**Matching:** rounded keV (exact integer match)")
report_lines.append("")
report_lines.append(f"| Category | Count |")
report_lines.append(f"|:----------|------:|")
report_lines.append(f"| Table I levels | {len(t1_levels)} |")
report_lines.append(f"| ENSDF L-records | {len(ensdf_levels)} |")

# Match and compare
matched = []
t1_only = []
ensdf_only = []
mismatches = []

for key, t1d in t1_levels.items():
    if key in ensdf_levels:
        matched.append(key)
        ed = ensdf_levels[key]
        
        issues = []
        # Check value
        if abs(t1d['ei_val'] - ed['e_val']) > 0.01:
            issues.append(f"Value: T1={t1d['ei_val']} vs ENSDF={ed['e_val']}")
        
        # Check uncertainty
        t1_unc = t1d['ei_unc']
        e_unc = ed['e_unc']
        if t1_unc is not None and e_unc is not None:
            if t1_unc != e_unc:
                issues.append(f"Uncertainty: T1={t1_unc} vs ENSDF={e_unc}")
        elif t1_unc is not None and e_unc is None:
            issues.append(f"Uncertainty: T1 has {t1_unc}, ENSDF has none")
        elif t1_unc is None and e_unc is not None:
            issues.append(f"Uncertainty: T1 has none, ENSDF has {e_unc}")
        
        # Check decimal places
        if t1d['ei_dp'] != ed['e_dp']:
            issues.append(f"Decimal places: T1={t1d['ei_dp']}dp vs ENSDF={ed['e_dp']}dp")
        
        if issues:
            mismatches.append((key, t1d, ed, issues))
    else:
        t1_only.append(key)

for key in ensdf_levels:
    if key not in t1_levels:
        ensdf_only.append(key)

report_lines.append(f"| Matched levels | {len(matched)} |")
report_lines.append(f"| Table I only (not in ENSDF) | {len(t1_only)} |")
report_lines.append(f"| ENSDF only (not in Table I) | {len(ensdf_only)} |")
report_lines.append(f"| Mismatches (matched but differ) | {len(mismatches)} |")
report_lines.append("")

# ── Detailed Results ────────────────────────────────────────────

if t1_only:
    report_lines.append("## Table I Only (not in ENSDF)")
    report_lines.append("")
    report_lines.append("| E (keV) | Jπ |")
    report_lines.append("|:---------|:----|")
    for key in sorted(t1_only):
        d = t1_levels[key]
        report_lines.append(f"| {d['ei_raw']} | {d['jpi']} |")
    report_lines.append("")

if ensdf_only:
    report_lines.append("## ENSDF Only (not in Table I)")
    report_lines.append("")
    report_lines.append("| E (keV) | L-record line |")
    report_lines.append("|:---------|:---------------|")
    for key in sorted(ensdf_only):
        d = ensdf_levels[key]
        report_lines.append(f"| {d['e_val']} | L{d['line_num']} |")
    report_lines.append("")

if mismatches:
    report_lines.append("## Mismatches (matched but differ)")
    report_lines.append("")
    for key, t1d, ed, issues in sorted(mismatches):
        report_lines.append(f"### Level ~{key} keV")
        report_lines.append("")
        report_lines.append(f"| Field | Table I | ENSDF (L{ed['line_num']}) | Issue |")
        report_lines.append(f"|:------|:---------|:---------------------------|:------|")
        report_lines.append(f"| Energy | {t1d['ei_raw']} | `{ed['e_field'].strip()}` | |")
        report_lines.append(f"| Unc | {t1d['ei_unc']} | {ed['e_unc'] if ed['e_unc'] is not None else 'none'} | |")
        report_lines.append(f"| DP | {t1d['ei_dp']}dp | {ed['e_dp']}dp | |")
        for issue in issues:
            report_lines.append(f"| | | | **{issue}** |")
        report_lines.append("")
else:
    report_lines.append("## All Matched Levels Consistent")
    report_lines.append("")
    report_lines.append("No value, uncertainty, or decimal-place mismatches found among matched levels.")
    report_lines.append("")

# ── Detail Table of All Matched Levels ──────────────────────────
report_lines.append("## Detailed Match Table")
report_lines.append("")
report_lines.append("| Level (keV) | T1 E | T1 Unc | ENSDF E | ENSDF Unc | Status |")
report_lines.append("|:-------------|:------|:-------|:---------|:----------|:-------|")
for key in sorted(matched):
    t1d = t1_levels[key]
    ed = ensdf_levels[key]
    has_issues = key in [m[0] for m in mismatches]
    status = "⚠️ MISMATCH" if has_issues else "✅ OK"
    report_lines.append(f"| {key} | {t1d['ei_raw']} | {t1d['ei_unc'] if t1d['ei_unc'] is not None else '-'} | {ed['e_val']} | {ed['e_unc'] if ed['e_unc'] is not None else '-'} | {status} |")
report_lines.append("")

# ── Write Report ────────────────────────────────────────────────
with open(REPORT_PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(report_lines))

print(f"\nReport written to: {REPORT_PATH}")
print(f"Summary: {len(matched)} matched, {len(mismatches)} mismatches, {len(t1_only)} T1-only, {len(ensdf_only)} ENSDF-only")

# Print mismatches to console
if mismatches:
    print("\nMISMATCHES:")
    for key, t1d, ed, issues in sorted(mismatches):
        print(f"  Level ~{key} keV: {'; '.join(issues)}")
