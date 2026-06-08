"""Produce sorted DCO(D) and DCO(Q) lists for 2026BAAA_CR11022_209Po.ens."""
import re, os

path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'XUNDL', '2026BAAA_CR11022_209Po.ens')
if not os.path.exists(path):
    path = 'd:\\X\\ND\\ENSDF\\XUNDL\\2026BAAA_CR11022_209Po.ens'

lines = open(path, 'r', encoding='utf-8').readlines()

# Build level lookup: energy -> Jπ string
# Also store Jnum (float) and parity sign
levels_jpi = {}  # energy -> (J_str, J_float, parity: -1/0/+1)
for line in lines:
    if len(line) < 20:
        continue
    # Level record: col 8 (idx 7) = 'L', col 7 (idx 6) = ' ', col 9 (idx 8) = ' '
    if line[6] != ' ':
        continue
    if line[7] != 'L':
        continue
    e_str = line[9:19].strip()
    j_str = line[21:39].strip()
    if not e_str or not j_str:
        continue
    try:
        e = float(e_str)
    except:
        continue
    # Parse Jπ: e.g., "1/2-", "(5/2+)", "0+,1+,2+,3+,4+", "(0:3)"
    clean = j_str.replace('(', '').replace(')', '')
    first_j = clean.split(',')[0].split(':')[0]
    parity = 0
    if '-' in first_j:
        parity = -1
    elif '+' in first_j:
        parity = 1
    jnum = None
    fp = first_j.split('+')[0].split('-')[0]
    if '/' in fp:
        try:
            n, d = fp.split('/')
            jnum = float(n) / float(d)
        except:
            pass
    else:
        try:
            jnum = float(fp)
        except:
            pass
    levels_jpi[e] = (j_str, jnum, parity)

# Find nearest level for a given energy
def find_level(energy, levels):
    best = None
    best_diff = 999
    for le in levels:
        diff = abs(le - energy)
        if diff < best_diff:
            best_diff = diff
            best = le
    if best_diff < 1.0:  # within 1 keV
        return best
    return None

# Parse gamma records
dco_d = []
dco_q = []

current_level_E = None
for i, line in enumerate(lines):
    if len(line) < 20:
        continue
    if line[6] != ' ':
        continue

    if line[7] == 'L':
        e_str = line[9:19].strip()
        if e_str:
            try:
                current_level_E = float(e_str)
            except:
                pass
        continue

    if line[7] != 'G':
        continue

    e_str = line[9:19].strip()
    m_str = line[32:42].strip()
    if not e_str:
        continue
    try:
        e_gamma = float(e_str)
    except:
        continue
    final_e = current_level_E - e_gamma

    # Look for DCO/POL in following comment lines (stop at next G or L record)
    dco_gate = None
    dco_val = None
    dco_digits = None
    pol_val = None
    pol_digits = None
    for j in range(i+1, min(i+8, len(lines))):
        c_line = lines[j]
        # Stop if we hit another G, L, or X record (or empty line)
        if len(c_line) >= 10 and c_line[6] == ' ' and c_line[7] in ('G', 'L', 'X'):
            break
        m_dco = re.search(r'R\{-DCO\}\(([QD])\)=(\d+\.?\d*)\s*\{I(\d+)\}', c_line)
        if m_dco:
            dco_gate = m_dco.group(1)
            dco_val = float(m_dco.group(2))
            dco_digits = int(m_dco.group(3))
        m_pol = re.search(r'POL=([+-]?\d+\.\d+)\s*\{I(\d+)\}', c_line)
        if m_pol:
            pol_val = float(m_pol.group(1))
            pol_digits = int(m_pol.group(2))

    if dco_gate is None:
        continue

    # Find initial and final level Jπ
    ji = find_level(current_level_E, levels_jpi)
    jf = find_level(final_e, levels_jpi)
    ji_str = levels_jpi[ji][0] if ji else '?'
    jf_str = levels_jpi[jf][0] if jf else '?'

    row = {
        'Egamma': e_gamma,
        'Ei': current_level_E,
        'Ef': final_e,
        'Ji': ji_str,
        'Jf': jf_str,
        'M': m_str,
        'DCO': dco_val,
        'DCOerr': dco_digits,
        'POL': pol_val,
        'POLerr': pol_digits,
        'gate': dco_gate,
    }

    if dco_gate == 'Q':
        dco_q.append(row)
    else:
        dco_d.append(row)

# Sort by DCO value
dco_d.sort(key=lambda r: r['DCO'])
dco_q.sort(key=lambda r: r['DCO'])

# Print DCO(D) list
print("=" * 100)
print("GAMMAS WITH R_DCO(D) — sorted from smallest to largest")
print("=" * 100)
header = f"{'R_DCO(D)':>10} {'POL':>10} {'Eγ':>8} {'E(level)':>9} {'E(final)':>9} {'Ji':>18} {'Jf':>18} {'M':>14}"
print(header)
print("-" * len(header))
for r in dco_d:
    dco_str = f"{r['DCO']:.2f}({r['DCOerr']})"
    pol_str = f"{r['POL']:+.2f}({r['POLerr']})" if r['POL'] is not None else "—"
    print(f"{dco_str:>10} {pol_str:>10} {r['Egamma']:>8.1f} {r['Ei']:>9.2f} {r['Ef']:>9.2f} {r['Ji']:>18} {r['Jf']:>18} {r['M']:>14}")

print()
print("=" * 100)
print("GAMMAS WITH R_DCO(Q) — sorted from smallest to largest")
print("=" * 100)
header = f"{'R_DCO(Q)':>10} {'POL':>10} {'Eγ':>8} {'E(level)':>9} {'E(final)':>9} {'Ji':>18} {'Jf':>18} {'M':>14}"
print(header)
print("-" * len(header))
for r in dco_q:
    dco_str = f"{r['DCO']:.2f}({r['DCOerr']})"
    pol_str = f"{r['POL']:+.2f}({r['POLerr']})" if r['POL'] is not None else "—"
    print(f"{dco_str:>10} {pol_str:>10} {r['Egamma']:>8.1f} {r['Ei']:>9.2f} {r['Ef']:>9.2f} {r['Ji']:>18} {r['Jf']:>18} {r['M']:>14}")

print()
print(f"Count: DCO(D)={len(dco_d)}, DCO(Q)={len(dco_q)}, total={len(dco_d)+len(dco_q)}")
