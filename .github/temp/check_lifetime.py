from pathlib import Path
import math

p = Path(r'd:\X\ND\ENSDF\A34\P34\new\P34_18o_18o_png_E_20-44_mev.ens')
lines = p.read_text().splitlines()

# Parse L-records with T and DT
levels = []
for i, l in enumerate(lines):
    if ' L ' in l[:10] and l[0:5].strip() == '34P':
        parts = l.split()
        e = parts[3]
        if e == '0.0':
            continue
        t_text = l[39:49].strip()
        dt_text = l[49:55].strip()
        levels.append({'energy': e, 'line': i, 'T': t_text, 'DT': dt_text})

# Parse cL T$ comments (find nearest after L record)
print(f"{'E_level':>8} {'T(rec)':>14} {'DT(rec)':>8} {'tau_comment':>35} {'Match?':>10}")
print('-' * 80)

for lev in levels:
    # Find cL T$ within next 5 lines
    cl_text = ''
    for j in range(lev['line'] + 1, min(lev['line'] + 6, len(lines))):
        if 'cL T' in lines[j][:10] and '|t' in lines[j]:
            cl_text = lines[j]
            break
    
    t_text = lev['T']
    dt_text = lev['DT']
    
    # Parse T as half-life
    t_parts = t_text.split()
    if len(t_parts) >= 2:
        t_val = float(t_parts[0])
        t_unit = t_parts[1]
    else:
        t_val = 0
        t_unit = ''
    
    # Parse DT as uncertainty
    dt_val = None
    is_lim = False
    lim_type = ''
    if dt_text in ['LT', 'GT']:
        is_lim = True
        lim_type = dt_text
    elif dt_text:
        try:
            dt_val = float(dt_text)
        except:
            pass
    
    # Convert to lifetime and compare with comment
    tau_val = t_val / math.log(2)
    
    result = 'OK'
    if cl_text:
        # Extract tau value from comment
        # format: |t=VALUE UNIT {IUNC} or |t>VALUE UNIT
        import re
        m = re.search(r'\|t[=<>]\s*([\d.]+)\s*(\w+)\s*\{?I?(\d*)\}?', cl_text)
        if m:
            c_tau_val = float(m.group(1))
            c_tau_unit = m.group(2)
            
            # Check unit consistency
            if c_tau_unit != t_unit:
                result = f'UNIT: {c_tau_unit} vs {t_unit}'
            
            # If not a limit, check value
            if not is_lim:
                # Accept within 10% for simple conversion check
                ratio = tau_val / c_tau_val if c_tau_val > 0 else 0
                if ratio < 0.9 or ratio > 1.1:
                    result = f'RATIO: {ratio:.2f}'
            
            # For limits, just check direction
            if is_lim:
                if '<' in cl_text:
                    expected = tau_val * 1.0  # tau < expected
                    if c_tau_val > tau_val * 1.5:
                        pass  # rough check
                elif '>' in cl_text:
                    if c_tau_val < tau_val * 0.5:
                        result = f'LIMIT: {c_tau_val} vs >{tau_val:.1f}'
        
        print(f"{lev['energy']:>8} {t_text:>14} {dt_text:>8} {cl_text[43:70]:>35} {result:>10}")
    else:
        print(f"{lev['energy']:>8} {t_text:>14} {dt_text:>8} {'NO cL T$ COMMENT':>35} {'MISSING':>10}")
