"""Check 209Po DCO/POL vs assigned multipolarities."""
import re

lines = open('XUNDL/2026BAAA_CR11022_209Po.ens', 'r', encoding='utf-8').readlines()

# Parse levels
levels = {}  # energy -> (J_num/den, parity_sign, J_raw_string)
for i, line in enumerate(lines):
    if len(line) >= 20 and line[7] == 'L' and line[8] == ' ' and line[6] == ' ':
        E_str = line[9:19].strip()
        J_str = line[22:39].strip()
        if E_str:
            E = float(E_str)
            levels[E] = J_str

# Parse gamma records and their DCO/POL comments
gammas = []
current_level_E = None
for i, line in enumerate(lines):
    if len(line) >= 20 and line[7] == 'L' and line[8] == ' ' and line[6] == ' ':
        E_str = line[9:19].strip()
        if E_str:
            current_level_E = float(E_str)
    elif len(line) >= 20 and line[7] == 'G' and line[8] == ' ' and line[6] == ' ':
        E_str = line[9:19].strip()
        M_str = line[32:41].strip()
        if E_str:
            E_gamma = float(E_str)
            # Find which comment lines follow (DCO/POL)
            dco_gate = None
            dco_val = None
            dco_err = None
            pol_val = None
            pol_err = None
            has_S = 'S' in line[75:80]
            has_P = 'P' in line[75:80]
            # Look at following comment lines
            for j in range(i+1, min(i+5, len(lines))):
                c_line = lines[j]
                if 'cG $R{-DCO}' in c_line:
                    m = re.search(r'R\{-DCO\}\(([QD])\)=([\d.]+)\s*\{I(\d+)\}', c_line)
                    if m:
                        dco_gate = m.group(1)
                        dco_val = float(m.group(2))
                        dco_err = int(m.group(3))
                if 'POL=' in c_line:
                    m = re.search(r'POL=([+-]\d+\.\d+)\s*\{I(\d+)\}', c_line)
                    if m:
                        pol_val = float(m.group(1))
                        pol_err = int(m.group(2))
            
            # Calculate final level energy
            final_E = round(current_level_E - E_gamma, 2)
            
            gammas.append({
                'E_gamma': E_gamma,
                'level_E': current_level_E,
                'final_E': final_E,
                'M': M_str,
                'flags': ('S' if has_S else '') + ('P' if has_P else ''),
                'dco_gate': dco_gate,
                'dco_val': dco_val,
                'dco_err': dco_err,
                'pol_val': pol_val,
                'pol_err': pol_err,
            })

# Parse J values for ΔJ calculation
def parse_J(J_str):
    """Extract numerical J value from Jπ string."""
    # Remove parentheses and commas
    s = J_str.replace('(', '').replace(')', '')
    # Get first spin value
    parts = s.split(',')
    first = parts[0]
    # Check for fraction
    if '/' in first:
        num, den = first.split('/')
        try:
            return float(num) / float(den)
        except:
            return None
    try:
        return float(first)
    except:
        return None

print(f"{'Gamma':>8} {'Level':>8} {'Final':>8} {'Ji':>8} {'Jf':>8} {'ΔJ':>4} {'M':>12} {'Gate':>4} {'R_DCO':>8} {'POL':>8} {'Flags':>4} {'Issue':>20}")
print("="*120)
issues = []
for g in gammas:
    Ji_str = levels.get(g['level_E'], '?')
    Jf_str = levels.get(g['final_E'], '?')
    Ji = parse_J(Ji_str)
    Jf = parse_J(Jf_str)
    delta_J = abs(Ji - Jf) if (Ji and Jf) else None
    
    # Check R_DCO against expected
    issue = ''
    if g['dco_gate'] and g['dco_val']:
        v = g['dco_val']
        e = g['dco_err'] / 100.0  # Convert from {In} notation
        
        if g['dco_gate'] == 'Q':
            # Q-gate: 0.76=ΔJ=1, 1.0=ΔJ=2/0
            d1_sig = abs(v - 0.76) / e
            d2_sig = abs(v - 1.0) / e
            if d1_sig < 2.0:
                classify = 'D'
            elif d2_sig < 2.0:
                classify = 'Q/Δ0'
            else:
                classify = f'MIX(d1={d1_sig:.1f}σ,d2={d2_sig:.1f}σ)'
        else:  # D-gate
            # D-gate: 1.0=ΔJ=1, 1.33=ΔJ=2/0
            d1_sig = abs(v - 1.0) / e
            d2_sig = abs(v - 1.33) / e
            if d1_sig < 2.0:
                classify = 'D'
            elif d2_sig < 2.0:
                classify = 'Q/Δ0'
            else:
                classify = f'MIX(d1={d1_sig:.1f}σ,d2={d2_sig:.1f}σ)'
    else:
        classify = ''
    
    pol_str = ''
    if g['pol_val'] is not None:
        pv = g['pol_val']
        pe = g['pol_err'] / 100.0
        if pe > 0:
            sig = abs(pv) / pe
            pol_str = f"{pv:+.2f}({pe*100:.0f})"
            if sig >= 2.0:
                pol_str += f"({'pos' if pv>0 else 'neg'})"
    
    # Check consistency
    if 'MIX' in classify and g['M'] and g['M'] not in ['D', ''] and g['M'] not in ['(D+Q)'] and not g['flags']:
        issue = 'DCO Mixed≠M field'
    if delta_J is not None and g['M']:
        if 'M1' in g['M'] and 'E2' not in g['M']:
            pass  # M1 allows ΔJ=0,1
        if 'E2' in g['M'] and 'M1' not in g['M']:
            if delta_J != 2:
                issue += ' E2≠ΔJ=2'
    
    if g['pol_val'] is not None and g['M']:
        pv = g['pol_val']
        pe = g['pol_err'] / 100.0
        sig = abs(pv) / pe if pe > 0 else 0
        if sig >= 2.0:
            if pv > 0 and ('M1' in g['M'] or 'M2' in g['M']):
                issue += ' POL+≠magnetic'
            elif pv < 0 and ('E1' in g['M'] or 'E2' in g['M'] or 'E3' in g['M']):
                issue += ' POL-≠electric'
    
    print(f"{g['E_gamma']:>8.1f} {g['level_E']:>8.2f} {g['final_E']:>8.2f} {str(Ji or '?'):>8} {str(Jf or '?'):>8} {str(delta_J or '?'):>4} {g['M']:>12} {g['dco_gate'] or '':>4} {classify:>8} {pol_str:>8} {g['flags']:>4} {issue:>20}")

print("\n\nSUMMARY OF ISSUES:")
for g in gammas:
    Ji_str = levels.get(g['level_E'], '?')
    Jf_str = levels.get(g['final_E'], '?')
    Ji = parse_J(Ji_str)
    Jf = parse_J(Jf_str)
    delta_J = abs(Ji - Jf) if (Ji and Jf) else None
    
    issues_found = []
    
    # 1. Check DCO classification
    if g['dco_gate'] and g['dco_val']:
        v = g['dco_val']
        e = g['dco_err'] / 100.0
        if g['dco_gate'] == 'Q':
            d1 = abs(v - 0.76)/e
            d2 = abs(v - 1.0)/e
        else:
            d1 = abs(v - 1.0)/e
            d2 = abs(v - 1.33)/e
        if d1 >= 2.0 and d2 >= 2.0:
            issues_found.append(f"DCO Mixed ({g['dco_gate']}-gate: {v}±{g['dco_err']}, neither ΔJ=1 nor ΔJ=2/0)")
    
    # 2. Check POL vs M
    if g['pol_val'] is not None and g['M']:
        pv = g['pol_val']
        pe = g['pol_err'] / 100.0
        sig = abs(pv) / pe if pe > 0 else 0
        if sig >= 2.0:
            is_magnetic = any(m in g['M'] for m in ['M1', 'M2', 'M3'])
            is_electric = any(e in g['M'] for e in ['E1', 'E2', 'E3'])
            if pv > 0 and is_magnetic and not is_electric:
                issues_found.append(f"POL=+{pv:.2f}±{g['pol_err']} ({sig:.1f}σ positive=electric) but M={g['M']} magnetic dominant")
            elif pv < 0 and is_electric and not is_magnetic:
                issues_found.append(f"POL={pv:.2f}±{g['pol_err']} ({sig:.1f}σ negative=magnetic) but M={g['M']} electric dominant")
    
    # 3. Check ΔJ vs M (for clear cases)
    if delta_J is not None and g['M']:
        if 'M1' in g['M'] and delta_J == 2:
            issues_found.append(f"M1+E2 but ΔJ={delta_J} forbids M1 component (ΔJ=0,1 only)")
    
    if issues_found:
        print(f"\nG {g['E_gamma']:.1f} (L {g['level_E']:.2f}→L {g['final_E']:.2f}, {Ji_str}→{Jf_str}, ΔJ={delta_J}):")
        for iss in issues_found:
            print(f"  ⚠ {iss}")
