"""
For each multi-value $E(p)(lab)= cL line in Cl34_33s_p_g.ens:
  - Handle 2-line (cL + 2cL) and 1-line cases
  - Parse all values with uncertainties
  - Run Java_Average.py  
  - Build new single-line cL:
      $E(p)(lab)=AVG {IUNC}: [weighted/unweighted] average of V1 {I} (CIT1) and V2 {I} (CIT2).
  - Output replacements JSON
"""
import re, subprocess, json, sys

FILE = r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens'
JAVA_AVG = r'd:\X\ND\ENSDF\.github\scripts\Java_Average.py'
NUCID_PREFIX = ' 34CL'   # 5-char NUCID

# ---------- helpers ----------------------------------------------------------

def decimal_places(val_str):
    if '.' in val_str:
        return len(val_str.split('.')[1])
    return 0

def to_abs_unc(val_str, iunc_digits):
    dec = decimal_places(val_str)
    return iunc_digits * (10 ** (-dec))

def fmt_abs_unc(abs_unc):
    s = f'{abs_unc:.10f}'.rstrip('0').rstrip('.')
    return s or '0'

def run_java(pairs):
    args = []
    for v, u in pairs:
        args += [v, fmt_abs_unc(u)]
    cmd = [sys.executable, JAVA_AVG] + args
    result = subprocess.run(cmd, capture_output=True, text=True,
                            cwd=r'd:\X\ND\ENSDF')
    return result.stdout

def parse_java_output(stdout):
    m_sug = re.search(r'\*\*\* Suggested Adopted Result: (\S+) \*\*\*', stdout)
    if not m_sug:
        return None, None, None
    result_str = m_sug.group(1)
    m_res = re.match(r'([\d.+-]+)\((\d+)\)$', result_str)
    if m_res:
        adopted_value = m_res.group(1)
        adopted_unc   = m_res.group(2)
    else:
        adopted_value = result_str
        adopted_unc   = None
    m_rec = re.search(r'RECOMMENDATION: Use (WEIGHTED|UNWEIGHTED)', stdout, re.IGNORECASE)
    method = m_rec.group(1).lower() if m_rec else 'weighted'
    return method, adopted_value, adopted_unc

EP_TOKEN_RE = re.compile(r'([\d.]+)\s+\{I(\d+)\}\s+\(([^)]+)\)')

def parse_ep_body(ep_body):
    """Returns (measured_list, other_str)."""
    other_str = ''
    other_m = re.search(r'\.\s+Other:\s+(.+)', ep_body)
    if other_m:
        other_str = 'Other: ' + other_m.group(1).rstrip('.')
        ep_body = ep_body[:other_m.start()]
    measured = []
    for m in EP_TOKEN_RE.finditer(ep_body):
        val, iunc, cit = m.group(1), m.group(2), m.group(3)
        measured.append({'val': val, 'iunc': iunc, 'cit': cit,
                         'abs_unc': to_abs_unc(val, int(iunc))})
    return measured, other_str

def build_citation_list(measured):
    parts = [f"{e['val']} {{I{e['iunc']}}} ({e['cit']})" for e in measured]
    if len(parts) == 1:
        return parts[0]
    elif len(parts) == 2:
        return f"{parts[0]} and {parts[1]}"
    else:
        return ', '.join(parts[:-1]) + f', and {parts[-1]}'

def get_2cL_prefix(nucid5):
    """Return the 2cL line prefix, e.g. ' 34CL2cL '"""
    return nucid5 + '2cL '

# ---------- load file --------------------------------------------------------

raw = open(FILE, 'rb').read()
content = raw.decode('ascii')
lines = content.split('\r\n')

marker     = 'cL $E(p)(lab)='
results    = []
special_cases = []

i = 0
while i < len(lines):
    i += 1   # 1-based
    line = lines[i - 1]
    if marker not in line:
        continue

    cL_raw   = line          # full raw line (may be 80-char padded)
    cL_strip = line.rstrip()

    # Count {I} occurrences in this line alone
    iunc_here = len(re.findall(r'\{I\d+\}', cL_strip))

    # Check if next line is a 2cL continuation of this Ep comment
    # (True when iunc_here < expected, or line ends without a period)
    extra_raw   = ''
    extra_strip = ''
    if (i < len(lines)):
        next_line = lines[i]    # 0-based index = line i (next 1-based)
        nucid5 = cL_strip[:5]   # e.g. ' 34CL'
        cont_prefix = nucid5 + '2cL '     # ' 34CL2cL '
        if next_line.startswith(cont_prefix):
            extra_raw   = next_line
            extra_strip = next_line[len(cont_prefix):].rstrip()
            # advance i so we don't process 2cL as a separate line
            i += 1

    # Build full ep body by joining primary + continuation
    if extra_strip:
        # The cL_strip may end mid-token (e.g. '...1347.3    ') — rstrip it first
        full_body_prefix = cL_strip[cL_strip.index('$E(p)(lab)=') + len('$E(p)(lab)='):]
        full_body = full_body_prefix.rstrip() + ' ' + extra_strip
    else:
        idx = cL_strip.index('$E(p)(lab)=') + len('$E(p)(lab)=')
        full_body = cL_strip[idx:]

    # Count total {I} patterns in reconstructed body
    total_iunc = len(re.findall(r'\{I\d+\}', full_body))
    if total_iunc < 2:
        continue

    measured, other_str = parse_ep_body(full_body)
    if len(measured) < 2:
        print(f'WARNING L{i}: Only {len(measured)} parsed from: {repr(full_body[:80])}')
        continue

    # Run Java Average
    pairs    = [(e['val'], e['abs_unc']) for e in measured]
    java_out = run_java(pairs)
    method, avg_val, avg_unc = parse_java_output(java_out)

    if avg_val is None:
        print(f'ERROR L{i}: Could not parse Java output')
        print(java_out)
        continue

    # Special-case detection
    is_special = method == 'unweighted'
    if is_special:
        special_cases.append({'line': i, 'method': method,
                              'avg': f'{avg_val}({avg_unc})',
                              'measured': measured,
                              'reason': 'Java recommended UNWEIGHTED'})

    # Build new line
    citation_list = build_citation_list(measured)
    method_word   = 'weighted' if method == 'weighted' else 'unweighted'
    new_body      = f'{avg_val} {{I{avg_unc}}}: {method_word} average of {citation_list}.'
    if other_str:
        new_body += f' {other_str}.'

    line_prefix = cL_strip[:cL_strip.index('$E(p)(lab)=')]
    new_line    = line_prefix + '$E(p)(lab)=' + new_body

    # old_string: 2 lines if continuation existed, else 1 line
    if extra_raw:
        old_str = cL_raw + '\r\n' + extra_raw
    else:
        old_str = cL_raw

    n_measured = len(measured)
    print(f'L{i-1 if extra_raw else i:4d} [{method_word[:1].upper()}]'
          f' N={n_measured} avg={avg_val}({avg_unc}): {full_body[:50]}...')

    results.append({
        'line_num': i,
        'n_measured': n_measured,
        'old': old_str,
        'new': new_line,
        'method': method_word,
        'avg': f'{avg_val}({avg_unc})',
        'is_special': is_special,
        'extra_line': bool(extra_raw)
    })

# ---------- save -------------------------------------------------------------

out = {'replacements': [{'old': r['old'], 'new': r['new']} for r in results],
       'details': results,
       'special_cases': special_cases}

with open(r'd:\X\ND\ENSDF\.github\temp\ep_averages2.json', 'w') as f:
    json.dump(out, f, indent=2)

print(f'\nTotal processed: {len(results)} | Special cases: {len(special_cases)}')
print(f'2-line Ep entries: {sum(1 for r in results if r["extra_line"])}')
print(f'1-line Ep entries: {sum(1 for r in results if not r["extra_line"])}')
if special_cases:
    print('\nSPECIAL CASES:')
    for s in special_cases:
        print(f'  L{s["line"]}: {s["reason"]} avg={s["avg"]}')
