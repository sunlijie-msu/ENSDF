"""
For each multi-value $E(p)(lab)= cL line in Cl34_33s_p_g.ens:
  1. Parse all values with uncertainties (skip Other: values)
  2. Run Java_Average.py to get weighted/unweighted adopted result
  3. Build new cL line:
       $E(p)(lab)=AVG {IUNC}: [weighted/unweighted] average of V1 {I} (CIT1) and V2 {I} (CIT2)[. Other: ...].
  4. Output replacements as JSON for human review
"""
import re, subprocess, json, sys

FILE = r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens'
JAVA_AVG = r'd:\X\ND\ENSDF\.github\scripts\Java_Average.py'

# ---------- helpers ----------------------------------------------------------

def decimal_places(val_str):
    """Count decimal places in a numeric string like '1255.4' or '507'."""
    if '.' in val_str:
        return len(val_str.split('.')[1])
    return 0

def to_abs_unc(val_str, iunc_digits):
    """Convert {IUNC} last-digit notation to absolute uncertainty."""
    dec = decimal_places(val_str)
    return iunc_digits * (10 ** (-dec))

def fmt_abs_unc(abs_unc):
    """Format absolute uncertainty for Java command-line (avoid float repr issues)."""
    # Use enough decimal places
    s = f'{abs_unc:.10f}'.rstrip('0').rstrip('.')
    if not s:
        s = '0'
    return s

def run_java(pairs):
    """pairs: list of (value_str, abs_unc_float). Returns stdout."""
    args = []
    for v, u in pairs:
        args += [v, fmt_abs_unc(u)]
    cmd = [sys.executable, JAVA_AVG] + args
    result = subprocess.run(cmd, capture_output=True, text=True,
                            cwd=r'd:\X\ND\ENSDF')
    return result.stdout

def parse_java_output(stdout):
    """Extract: recommended method ('weighted'/'unweighted'), adopted value, adopted unc_str."""
    # Find suggestion line
    m_sug = re.search(r'\*\*\* Suggested Adopted Result: (\S+) \*\*\*', stdout)
    if not m_sug:
        return None, None, None
    result_str = m_sug.group(1)   # e.g. "1255.3(13)"

    # Parse VALUE(UNC) or VALUE
    m_res = re.match(r'([\d.+-]+)\((\d+)\)$', result_str)
    if m_res:
        adopted_value = m_res.group(1)
        adopted_unc   = m_res.group(2)   # last-digit notation string
    else:
        # No uncertainty in parens (rare)
        adopted_value = result_str
        adopted_unc   = None

    # Find method
    m_rec = re.search(r'RECOMMENDATION: Use (WEIGHTED|UNWEIGHTED)', stdout, re.IGNORECASE)
    if m_rec:
        method = m_rec.group(1).lower()
    else:
        method = 'weighted'   # fallback per user instruction

    return method, adopted_value, adopted_unc

# ---------- parse Ep line ----------------------------------------------------

# Pattern: one measurement token  "VALUE {IUNC} (CIT[,CIT2])"
# optionally followed by comma/and, then more tokens
# "Other: ..." at end

EP_TOKEN_RE = re.compile(
    r'([\d.]+)\s+\{I(\d+)\}\s+\(([^)]+)\)'
)

def parse_ep_line(ep_body):
    """
    ep_body: everything after '$E(p)(lab)='
    Returns:
      measured   : list of {'val':str, 'iunc':str, 'cit':str, 'abs_unc':float}
      other_str  : string like 'Other: 1098 (1971Hy02,1973An13).' or ''
    """
    # Split off 'Other:' part
    other_str = ''
    other_m = re.search(r'\.\s+Other:\s+(.+)', ep_body)
    if other_m:
        other_str = 'Other: ' + other_m.group(1).rstrip('.')
        ep_body = ep_body[:other_m.start()]

    measured = []
    for m in EP_TOKEN_RE.finditer(ep_body):
        val   = m.group(1)
        iunc  = m.group(2)
        cit   = m.group(3)
        abs_u = to_abs_unc(val, int(iunc))
        measured.append({'val': val, 'iunc': iunc, 'cit': cit, 'abs_unc': abs_u})

    return measured, other_str

def build_citation_list(measured):
    """Build natural-language list: 'V1 {I} (CIT1), V2 {I} (CIT2), and V3 {I} (CIT3)'"""
    parts = [f"{e['val']} {{I{e['iunc']}}} ({e['cit']})" for e in measured]
    if len(parts) == 1:
        return parts[0]
    elif len(parts) == 2:
        return f"{parts[0]} and {parts[1]}"
    else:
        return ', '.join(parts[:-1]) + f', and {parts[-1]}'

# ---------- main loop --------------------------------------------------------

raw = open(FILE, 'rb').read()
content = raw.decode('ascii')
lines = content.split('\r\n')

marker = 'cL $E(p)(lab)='
results = []
special_cases = []

for i, line in enumerate(lines, 1):
    if marker not in line:
        continue
    stripped = line.rstrip()

    # Must have at least 2 {Innn} patterns to warrant averaging
    iunc_count = len(re.findall(r'\{I\d+\}', stripped))
    if iunc_count < 2:
        continue

    # Extract the body after '$E(p)(lab)='
    idx = stripped.index('$E(p)(lab)=') + len('$E(p)(lab)=')
    ep_body = stripped[idx:]

    measured, other_str = parse_ep_line(ep_body)

    if len(measured) < 2:
        print(f'WARNING L{i}: Only {len(measured)} measured values found, skipping: {stripped[-70:]}')
        continue

    # Run Java Average
    pairs = [(e['val'], e['abs_unc']) for e in measured]
    java_out = run_java(pairs)
    method, avg_val, avg_unc = parse_java_output(java_out)

    if avg_val is None:
        print(f'ERROR L{i}: Could not parse Java output for: {stripped[-70:]}')
        print(java_out)
        continue

    # Determine if this is a special case (unweighted, or chi^2 issues flagged)
    is_special = False
    if method == 'unweighted':
        is_special = True
        special_cases.append({'line': i, 'old': stripped, 'method': method,
                               'avg': f'{avg_val}({avg_unc})', 'reason': 'Java recommended UNWEIGHTED'})

    # Check for chi-square issues
    if 'inconsistent' in java_out.lower() or 'UNWEIGHTED' in java_out:
        if method == 'unweighted':
            note = 'INCONSISTENT data - Java recommends UNWEIGHTED'
        else:
            note = None
        if note and not is_special:
            special_cases.append({'line': i, 'old': stripped, 'method': method,
                                   'avg': f'{avg_val}({avg_unc})', 'reason': note})
            is_special = True

    # Build new line
    citation_list = build_citation_list(measured)
    avg_notation  = f'{avg_val} {{I{avg_unc}}}'
    method_word   = 'weighted' if method == 'weighted' else 'unweighted'

    new_body = f'{avg_notation}: {method_word} average of {citation_list}.'
    if other_str:
        new_body += f' {other_str}.'

    # Prefix: match original line prefix (cols 1-11: ' 34CL cL $')
    prefix = stripped[:stripped.index('$E(p)(lab)=')]
    new_line = prefix + '$E(p)(lab)=' + new_body

    results.append({
        'line_num': i,
        'old': stripped,
        'new': new_line,
        'method': method_word,
        'avg': f'{avg_val}({avg_unc})',
        'is_special': is_special
    })

    print(f'L{i:4d} [{method_word[:1].upper()}] {avg_val}({avg_unc}): {stripped[20:60]}...')

# ---------- save -------------------------------------------------------------

out = {
    'replacements': [{'old': r['old'], 'new': r['new']} for r in results],
    'details': results,
    'special_cases': special_cases
}
with open(r'd:\X\ND\ENSDF\.github\temp\ep_averages.json', 'w') as f:
    json.dump(out, f, indent=2)

print(f'\nTotal multi-value Ep lines: {len(results)}')
print(f'Special cases (unweighted/inconsistent): {len(special_cases)}')
print('Results written to ep_averages.json')
