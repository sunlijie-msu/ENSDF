"""
Comprehensive cross-check of 1971Hy02 A2 data in Cl34_33s_p_g.ens
against source 1971HY02_A2.md.

Also checks:
1. Formatting issues (typos like =)1058)
2. Whether each A2 data point is placed under the correct G-record
"""

import re

ENS_FILE  = r'A34\Cl34\new\Cl34_33s_p_g.ens'
A2_FILE   = r'A34\Cl34\raw\1971HY02_A2.md'

# -----------------------------------------------------------------------
# Parse source A2 table from 1971HY02_A2.md
# Each row: Ep(keV) | Ei(MeV) | Ef(MeV) | Eg(MeV) | Ji->Jf | a2 ± da2
# -----------------------------------------------------------------------
source_rows = []
with open(A2_FILE, encoding='utf-8') as f:
    lines = f.readlines()

for line in lines:
    # Skip header/separator lines
    if not line.strip().startswith('|'):
        continue
    parts = [p.strip() for p in line.strip().split('|')]
    parts = [p for p in parts if p]  # remove empty
    if len(parts) < 6:
        continue
    try:
        ep   = float(parts[0])
    except ValueError:
        continue  # header row
    try:
        ei_raw = parts[1].strip()
        ei = float(re.search(r'[\d.]+', ei_raw).group())
        ef_raw = parts[2].strip()
        ef = float(re.search(r'[\d.]+', ef_raw).group())
        eg_raw = parts[3].strip()
        eg = float(re.search(r'[\d.]+', eg_raw).group())
    except Exception:
        continue
    
    a2_raw = parts[5].strip()
    # E.g. "$+0.28 \pm 0.03$" or "$-0.20(3)$" or "$(+0.32 \pm 0.16)$"
    # Clean up LaTeX
    a2_clean = a2_raw.replace('$','').replace('\\pm','±').strip()
    a2_match = re.search(r'([+-]?\d+\.?\d*)\s*±\s*(\d+\.?\d*)', a2_clean)
    if not a2_match:
        continue
    a2_val = float(a2_match.group(1))
    a2_unc = float(a2_match.group(2))
    
    source_rows.append({
        'ep': ep,
        'ei': ei,
        'ef': ef,
        'eg': eg,
        'a2': a2_val,
        'da2': a2_unc,
        'raw': line.strip()
    })

print(f"Parsed {len(source_rows)} source A2 rows from 1971HY02_A2.md\n")

# -----------------------------------------------------------------------
# Parse ENSDF file: find all cG $ lines containing 1971Hy02 A2 data
# Track which G-record (energy, parent level) each belongs to
# -----------------------------------------------------------------------
with open(ENS_FILE, encoding='utf-8') as f:
    ens_lines = f.readlines()

# Build structure: list of (line_no, level_E, gamma_E, comment_text)
# Walk through lines tracking current level and current gamma
current_level_E = None
current_gamma_E = None

a2_entries = []  # Each entry: (line_no, level_E, gamma_E, a2_line_content)

for i, line in enumerate(ens_lines, 1):
    if len(line) < 8:
        continue
    
    # Identify level records (col[5]=' ', col[7]='L')
    if line[5] == ' ' and line[6] == ' ' and len(line) > 9 and line[7] == 'L':
        # Extract level energy from cols 9-18
        e_str = line[9:19].strip()
        try:
            current_level_E = float(re.search(r'[\d.]+', e_str).group()) if e_str else None
        except:
            current_level_E = None
        current_gamma_E = None
    
    # Identify gamma records (col[5]=' ', col[7]='G')
    elif line[5] == ' ' and line[6] == ' ' and len(line) > 9 and line[7] == 'G':
        e_str = line[9:19].strip()
        try:
            current_gamma_E = float(re.search(r'[\d.]+', e_str).group()) if e_str else None
        except:
            current_gamma_E = None
    
    # Look for cG $ lines with 1971Hy02 A2 data
    if '1971Hy02' in line and 'A{-2}' in line:
        a2_entries.append({
            'lineno': i,
            'level_E': current_level_E,
            'gamma_E': current_gamma_E,
            'text': line.rstrip()
        })
    # Also catch continuation lines that continue a 1971Hy02 A2 comment
    elif 'A{-2}' in line and '1971Hy02' not in line:
        # Check if prior line was a 1971Hy02 A2 line (continuation)
        if a2_entries and a2_entries[-1]['lineno'] == i - 1:
            # Add continuation info inline
            a2_entries[-1]['text'] += ' | CONT: ' + line.rstrip()

print("=" * 80)
print("1971Hy02 A2 entries found in ENSDF file:")
print("=" * 80)
for e in a2_entries:
    ge = f"{e['gamma_E']:8.2f}" if e['gamma_E'] is not None else "    None"
    print(f"  Line {e['lineno']:4d}: Level={e['level_E']:8.2f} keV  Gamma={ge} keV")
    print(f"           {e['text']}")
    print()

# -----------------------------------------------------------------------
# Cross-check each ENSDF A2 entry against source data
# For each entry: extract Ep, A2, uncertainty; find matching source row;
# verify that the gamma energy matches the level/gamma in the ENSDF
# -----------------------------------------------------------------------
print("=" * 80)
print("CROSS-CHECK RESULTS:")
print("=" * 80)

ISSUES = []

def find_source_row(ep, a2_val, a2_unc, tol_ep=5.0, tol_a2=0.005):
    """Find matching source row by Ep and A2 value."""
    candidates = []
    for row in source_rows:
        if abs(row['ep'] - ep) <= tol_ep:
            if abs(row['a2'] - a2_val) <= tol_a2 and abs(row['da2'] - a2_unc) <= tol_a2:
                candidates.append(row)
    return candidates

for e in a2_entries:
    text = e['text']
    level_E = e['level_E']
    gamma_E = e['gamma_E']
    lineno = e['lineno']
    
    # Extract all A2 values and Ep from the text
    # Pattern: A{-2}=(val) {I(unc)} (1971Hy02, ... E{-p}(lab)=EP)
    # Also: continuation lines
    full_text = text.replace(' | CONT: ', ' ')
    
    # Find Ep values mentioned
    ep_matches = re.findall(r'E\{-p\}\(lab\)=\)?(\d+)', full_text)
    a2_matches = re.findall(r'A\{-2\}=([+-]?\d+\.\d*(?:E[+-]?\d+)?)\s+\{I(\d+)\}', full_text)
    
    if not a2_matches:
        continue
    
    for (a2_str, unc_str), ep_str in zip(a2_matches, ep_matches if ep_matches else ['?']*len(a2_matches)):
        try:
            a2_float = float(a2_str)
            unc_float = float(unc_str) / 100.0  # {I3} means ± 0.03
            ep_float = float(ep_str) if ep_str != '?' else None
        except:
            continue
        
        # Find source row
        hits = []
        if ep_float is not None:
            hits = find_source_row(ep_float, a2_float, unc_float)
        
        # Expected: gamma energy from source should match gamma_E in ENSDF
        eg_from_source = [(h['eg'] * 1000) for h in hits]  # convert MeV -> keV
        ei_from_source = [(h['ei'] * 1000) for h in hits]
        ef_from_source = [(h['ef'] * 1000) for h in hits]
        
        status = "OK"
        issue_msg = ""
        
        if not hits:
            status = "NO_SOURCE_MATCH"
            issue_msg = f"No source row found for Ep={ep_float}, A2={a2_float}, unc={unc_float:.3f}"
        else:
            # Check if any source hit matches the current gamma energy
            matched_gamma = False
            for h in hits:
                if gamma_E is not None:
                    if abs(h['eg'] * 1000 - gamma_E) < 5.0:  # within 5 keV
                        matched_gamma = True
                        break
            
            if not matched_gamma and gamma_E is not None:
                status = "GAMMA_MISMATCH"
                issue_msg = (f"Source says Eg(keV)={[f'{x:.1f}' for x in eg_from_source]} "
                            f"(from Ei={[f'{x:.0f}' for x in ei_from_source]}->Ef={[f'{x:.0f}' for x in ef_from_source]}) "
                            f"but ENSDF gamma is {gamma_E:.1f} keV (L={level_E:.2f})")
        
        # Check for formatting issues
        if '=)' in e['text']:
            status += "+TYPO"
            issue_msg += " | TYPO: '=)' found in text"
        
        ep_str2 = f"{ep_float:5.0f}" if ep_float is not None else "    ?"
        ge_str = f"{gamma_E:8.1f}" if gamma_E is not None else "    None"
        print(f"Line {lineno:4d}: Level={level_E:8.1f}  Gamma={ge_str}  "
              f"Ep={ep_str2}  A2={a2_float:+.2f}±{unc_float:.2f}  [{status}]")
        if issue_msg:
            print(f"         *** {issue_msg}")
            ISSUES.append({'lineno': lineno, 'status': status, 'msg': issue_msg,
                          'level_E': level_E, 'gamma_E': gamma_E, 'text': e['text']})

print()
print("=" * 80)
print(f"SUMMARY: {len(ISSUES)} issues found")
print("=" * 80)
for iss in ISSUES:
    print(f"  Line {iss['lineno']}: [{iss['status']}] Level={iss['level_E']}, Gamma={iss['gamma_E']}")
    print(f"    {iss['msg']}")
    print()
